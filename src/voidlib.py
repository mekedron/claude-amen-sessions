"""voidlib - the ЧЁРНЫЕ ЗВЁЗДЫ kit: darkstep and neurofunk at 174.

A dead universe, and a drum machine in it. The brief is a far-future
dystopia where the stars are going out - cyber implants, traffic, ships
leaving, and nobody arriving. Musically that is two decisions:

  DARKSTEP is what the DRUMS do. A two-step at 174 with the second kick
  pushed late, no funk in it, no room on it, and long stretches where the
  only thing above 3 kHz is the snare's own crack. Techstep's grandchild:
  machined, cold, and sparse enough that the silence between the kick and
  the snare is a place the bass can live.

  NEUROFUNK is what the BASS does, and it is not a note pattern. The
  defining sound of the genre is ONE HELD NOTE whose modulation rate
  changes inside it - slow, then doubling, then doubling again, then
  released. Writing that as a run of short notes produces something busy
  that is not this genre (see theory/30-patterns/11-signature-techniques.md
  and theory/90-memories/dnb-bass-is-gestures-not-notes.md). So the unit of
  composition here is not a note, it is a GESTURE: half a bar of lane
  values that say how fast the timbre is travelling, and a phrase is four
  or eight of them concatenated over a single oscillator that never
  restarts.

WHAT IS IN HERE

    the kit      kick, snare, ghost, chat, ohat, ride, plate, rev
    the bass     creature() - the phrase renderer, GEST - the vocabulary
    the void     star, hull, sheet, siren, transit, impact, sink, lift, code

`kick` and `snare` deliberately shadow the ones in `core`; this module's
kit is its own and the core's named voices are not part of it.

THE BASS, IN DETAIL

One phase track for the whole phrase, and everything hangs off it:

    body      sin(ph) + h2 + h3, mono, clean, lowpassed at 130.
              The creature carries its OWN fundamental - there is no
              separate sub oscillator to cancel against it, because two
              continuous oscillators at 49 Hz with unrelated phases do
              exactly that (theory/90-memories/bass-must-keep-its-own-
              fundamental.md).
    character 2 spectral wavetables read with a moving scan position, plus
              an optional hard-synced saw and an optional FM partner,
              highpassed at 90 so the drive never touches the sub, then a
              moving resonant lowpass, formants, and a wavefolder.
    talon     the screamer: two octaves up, four resonances that TRACK the
              note and sweep on four unrelated rates, folded. This is the
              layer that carries 800 Hz - 11 kHz, and without it the record
              measures 6 dB down across the whole top half and reads as
              "глухой" (theory/90-memories/neuro-needs-a-screamer-over-
              the-reese.md). It is also where the stereo width comes from:
              the resonance sweeps differ per channel, which is
              decorrelation rather than a delay, so it survives mono.

Nothing is retriggered. The gates cut holes in a note that is still
sounding, and every attack adds a real 4 ms transient AFTER the filters,
because a zero-phase filter smears one in both directions.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import resample_poly

import core
from core import *                                            # noqa: F401,F403
from core import _ftrack, _amp                                # noqa: F401


def set_tempo(bpm=174.0):
    """174 is the middle of the genre and the number the drums were written
    against. Everything in this module measures its durations in steps, so
    this is the only place the tempo appears."""
    global BAR, STEP
    BAR, STEP = core.set_grid(bpm=bpm)
    return BAR, STEP


BAR, STEP = core.BAR, core.STEP


# ============================================================== lanes ======
# core.steplane maps k values over n samples, which stretches a lane when a
# segment is rendered with an overhang. These map a lane onto the GRID: step
# 5 is step 5 whatever the tail length, so a phrase can ring past its own
# last bar without its automation sliding with it.

def slane(values, n, kind='hold', smooth=0.004):
    """one value per 16th step -> one value per sample, anchored to the grid"""
    v = np.atleast_1d(np.asarray(values, dtype=np.float64))
    if len(v) == 1:
        return np.full(n, float(v[0]))
    x = np.arange(n) / STEP
    if kind == 'hold':
        out = v[np.minimum(x.astype(np.intp), len(v) - 1)]
    elif kind == 'exp':
        out = np.exp(np.interp(x, np.arange(len(v)) + 0.5, np.log(np.maximum(v, 1e-6))))
    else:
        out = np.interp(x, np.arange(len(v)) + 0.5, v)
    if smooth:
        out = uniform_filter1d(out, max(int(smooth * SR), 3))
    return out


def scan(n, rates, shape='sine', phase0=0.0, smooth=0.006):
    """A modulator whose RATE is sequenced, in cycles per beat, on the grid.

    0 holds the timbre still, 0.25 is one cycle per bar, 1 a quarter, 2 an
    eighth, 4 a sixteenth, 2.667 an eighth triplet, 8 a thirty-second. The
    phase is the running integral of the rate, so a rate change accelerates
    a gesture that is already moving instead of restarting it - which is the
    difference between a bass line speeding up and two loops cut together.
    """
    r = slane(rates, n, 'hold', 0.030)
    ph = phase0 + 2 * np.pi * np.cumsum(r * (core.BPM / 60.0 / SR))
    if shape == 'saw':
        u = (ph / (2 * np.pi)) % 1.0
    elif shape == 'sawdown':
        u = 1.0 - ((ph / (2 * np.pi)) % 1.0)
    elif shape == 'tri':
        u = 2 * np.abs(((ph / (2 * np.pi)) % 1.0) - 0.5)
    else:
        u = 0.5 - 0.5 * np.cos(ph)
    return uniform_filter1d(np.clip(u, 0, 1), max(int(smooth * SR), 3))


def sweep_bp(seg, f_lo, f_hi, env, bands=5, width=0.14):
    """A resonant band whose centre MOVES, as a crossfade of static bands.

    A resonance parked on a fixed harmonic is a comb, and a comb's gaps
    measure as clearly as its peaks. Four of these on unrelated rates cross
    each other's gaps and the time-average fills in, which is what makes a
    neuro bass read as flat from 300 Hz to 11 kHz rather than as a filter.
    """
    n = len(seg)
    fs = np.geomspace(max(f_lo, 40.0), min(f_hi, SR * 0.45), bands)
    u = np.clip(np.asarray(env, dtype=np.float64), 0, 1)[:n] * (bands - 1)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(fs):
        w = np.clip(1 - np.abs(u - i), 0, 1)
        if w.max() < 1e-4:
            continue
        out += (bandpass(seg, f * (1 - width), f * (1 + width)) * w[:, None]).astype(np.float32)
    return out


def _os_saw(ph, ratio, os_=4):
    """A hard-synced saw from a phase array, computed oversampled.

    Sync tears the waveform on every master cycle, so the naive saw it is
    built from has energy well past Nyquist and folds it straight back down
    as inharmonic fizz. Four times up, decimate, and the tearing survives
    while the fizz does not.
    """
    n = len(ph)
    xi = np.arange(n * os_) / os_
    p = np.interp(xi, np.arange(n), ph) / (2 * np.pi)
    r = np.interp(xi, np.arange(n), np.asarray(ratio, dtype=np.float64) * np.ones(n))
    y = 2 * (((p % 1.0) * r) % 1.0) - 1
    return resample_poly(y, 1, os_)[:n]


def edge(n, at, gain=1.0, seed=0, lo=700.0, hi=7000.0, tau=0.0035):
    """The 4 ms front edge of an attack, added after every zero-phase filter.

    What separates a bass that hits from one that is merely loud is the
    ratio of the first ten milliseconds to the body - +10 to +18 dB. A
    forward-backward filter smears a transient in both directions, so the
    transient has to arrive after them.
    """
    rs = np.random.RandomState(seed)
    x = np.zeros(n)
    t = np.arange(int(0.030 * SR)) / SR
    for i, k in enumerate(at):
        k = int(k)
        if 0 <= k < n:
            e = min(n, k + len(t))
            x[k:e] += (rs.randn(e - k) * np.exp(-t[:e - k] / tau)
                       + np.sin(2 * np.pi * 1450 * t[:e - k]) * np.exp(-t[:e - k] / 0.0025))
    return bandpass(stereo(x), lo, hi) * gain


# ============================================================== the kit ====
# Everything takes a `seed`. A short bright sound whose noise is bit-identical
# on every one of four thousand hits stops being heard as an instrument and
# starts being heard as a metronome tick, so the caller varies the seed with
# the position (theory/90-memories/a-repeated-hit-must-not-be-identical.md).

@cached
def kick(dur_steps=2.4, tune=51.0, gain=1.0, punch=1.0, click=1.0, grit=0.55,
         decay=0.100, seed=0):
    """Short, tight, machined. At 174 a beat is 345 ms and this is done in
    170 of them, which is what leaves the hole the bass lives in."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    f = tune * (1 + 2.7 * np.exp(-t / 0.013))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    body = np.tanh(1.9 * body) / np.tanh(1.9)
    out = lp(stereo(body), 190, 4) * 0.86
    kf = tune * 2.2 + (640 - tune * 2.2) * np.exp(-t / 0.0095)
    kn = np.tanh(4.0 * np.sin(2 * np.pi * np.cumsum(kf) / SR)) * np.exp(-t / 0.030)
    out = out + punch * 1.15 * bandpass(stereo(kn), 72, 290)
    if grit:
        # band-passed noise, not a swept saw. A saw whose fundamental starts
        # four octaves above where it ends has partials at 60 kHz for the
        # first ten milliseconds, and the fold-down is identical every hit.
        g = rs.randn(n) * np.exp(-t / 0.020)
        out = out + grit * 0.62 * bandpass(stereo(g), 300, 2900)
    ck = rs.randn(n) * np.exp(-t / 0.0015)
    out = out + click * 0.42 * hp(stereo(ck), 2800)
    return norm(hp(out, 28) * adsr(n, a=0.0004, r=0.012)[:, None], 0.97) * gain


@cached
def snare(dur_steps=3.2, gain=1.0, tune=187.0, bottom=1.0, crack=1.0,
          snap=1.0, drive=1.6, decay=0.095, room=0.20, seed=0):
    """The most important sound on the record, and the one with a 95 Hz
    thud inside it.

    A two-step puts its backbeat on 2 and 4 and its kicks on 1 and the late
    half of 3. If the snare has nothing under 160 Hz then the low band -
    which is what the body counts - has no event on either backbeat, and the
    groove measures as pulseless however busy it is
    (theory/90-memories/the-felt-pulse-is-in-the-low-band.md)."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    th = np.sin(2 * np.pi * np.cumsum(95.0 * (1 + 0.55 * np.exp(-t / 0.006))) / SR)
    th *= np.exp(-t / 0.055)
    bd = (np.sin(2 * np.pi * np.cumsum(tune * (1 + 0.30 * np.exp(-t / 0.008))) / SR)
          * np.exp(-t / 0.052)
          + 0.45 * np.sin(2 * np.pi * tune * 1.63 * t) * np.exp(-t / 0.038))
    nz = rs.randn(n)
    cr = bandpass(stereo(nz), 620, 7400) * np.exp(-t / decay)[:, None]
    md = bandpass(stereo(nz), 300, 1100) * np.exp(-t / (decay * 1.5))[:, None] * 0.55
    sp = hp(np.stack([nz, rs.randn(n)], 1), 7600) * np.exp(-t / 0.026)[:, None]
    out = (lp(stereo(th), 165) * bottom * 1.45 + stereo(bd) * 0.58
           + cr * crack * 1.10 + md * crack + sp * snap * 0.74)
    out = np.tanh(drive * out) / np.tanh(drive)
    if room:
        out = out + room * reverb(out, decay=0.28, wet=1.0, tone=5400,
                                  predelay=0.004)[:n]
    return norm(out * adsr(n, a=0.0006, r=0.02)[:, None], 0.95) * gain


@cached
def ghost(dur_steps=1.0, gain=1.0, seed=0, tone=1.0):
    """The quiet hits between the strokes. Take these out and a two-step is
    a pattern; leave them in and it is drumming."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    x = bandpass(rs.randn(n, 2), 900 * tone, 4600 * tone) * np.exp(-t / 0.017)[:, None]
    x = x + stereo(np.sin(2 * np.pi * 205 * t) * np.exp(-t / 0.014)) * 0.30
    return x * adsr(n, a=0.0005, r=0.01)[:, None] * gain * 0.55


@cached
def chat(dur_steps=0.8, gain=1.0, seed=0, tone=1.0, decay=0.020):
    """closed hat: a noise tick with a little metal in it"""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    met = sum(np.sin(2 * np.pi * 3100 * r * tone * t) for r in
              (1.0, 1.41, 1.87, 2.34, 2.91)) / 5
    x = hp(rs.randn(n, 2) * 0.9 + met[:, None] * 0.5, 6600)
    return x * (np.exp(-t / decay) * adsr(n, a=0.0004, r=0.008))[:, None] * gain * 0.5


@cached
def ohat(dur_steps=3.0, gain=1.0, seed=0, tone=1.0, decay=0.130, cut=0.30):
    """An open hat is two discs, not a closed hat with a longer envelope.

    Six inharmonic partials for the metal and noise for the sizzle, the
    high modes shedding first so the colour changes while it rings, and the
    whole thing truncated to a window - a sample ends, an exponential does
    not, and four offbeat hats whose tails overlap are sand."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    R = (1.0, 1.34, 1.63, 2.02, 2.47, 2.83)
    x = np.zeros(n)
    for i, r in enumerate(R):
        x += np.sin(2 * np.pi * 2650 * r * tone * t) * np.exp(-t / (decay * (1 - 0.11 * i)))
    x = x[:, None] / len(R) + rs.randn(n, 2) * np.exp(-t / (decay * 1.15))[:, None] * 0.85
    y = hp(np.tanh(1.5 * x).astype(np.float32), 5200)
    k = int(min(cut, 0.95) * n)
    w = np.ones(n)
    w[k:] = np.cos(np.linspace(0, np.pi / 2, n - k)) ** 2
    return y * (w * adsr(n, a=0.0004, r=0.010))[:, None] * gain * 0.42


@cached
def ride(dur_steps=4.0, gain=1.0, seed=0):
    """a ping with a short wash - the top of a roller, used sparingly"""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    png = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, d in
              ((2870, 0.10), (4130, 0.07), (5990, 0.05), (8210, 0.035)))
    wash = hp(stereo(rs.randn(n)), 7200) * np.exp(-t / 0.16)[:, None]
    return (hp(stereo(png) * 0.30 + wash * 0.35, 3000)
            * adsr(n, a=0.0006, r=0.03)[:, None]) * gain * 0.5


@cached
def plate(dur_steps=2.0, gain=1.0, seed=0, lo=2600.0, hi=11000.0, decay=0.09,
          thud=0.5):
    """Struck metal with NO pitch in it - a hull panel, a rail, a door.

    Untuned on purpose. A bright ringing pitched object above 3 kHz reads
    as a glockenspiel and makes a dark record cheerful; broadband noise
    through a bank of high resonances reads as a room with machinery in it,
    which is the whole difference (theory/90-memories/pitched-metal-reads-
    as-cheerful.md)."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    nz = rs.randn(n, 2).astype(np.float32)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(np.geomspace(lo, hi, 5) * (0.9 + 0.2 * rs.rand(5))):
        out += bandpass(nz, f * 0.94, f * 1.07) * np.exp(-t / (decay * (1 - 0.13 * i)))[:, None]
    if thud:
        out = out + thud * lp(stereo(rs.randn(n) * np.exp(-t / 0.020)), 220)  # the thud stays centred
    return norm(out * adsr(n, a=0.0006, r=0.02)[:, None], 0.9) * gain


@cached
def rev(dur_steps=6.0, gain=1.0, seed=0, lo=900.0, hi=9000.0):
    """a reversed swell into a downbeat"""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    x = bandpass(stereo(rs.randn(n)), lo, hi)
    u = (np.arange(n) / n) ** 2.2
    return np.ascontiguousarray((x * u[:, None] * adsr(n, a=0.01, r=0.006)[:, None])[::-1]) * gain * 0.6


# ============================================================== the bass ===
# Built the way the genre is actually played - as a modern wavetable synth,
# not as a stack of resonances.
#
#   OSC     one wavetable, three unison voices 16-22 cents apart, read
#           through WARP: the phase is bent, pulse-width-shifted, hard
#           synced, phase-modulated and quantised BEFORE the wave is read.
#           That is where a modern synth's character comes from and it is
#           something no filter can do. Computed at four times the sample
#           rate and decimated, because every one of those warps tears the
#           waveform and a torn waveform aliases.
#
#   SUB     a locked sine at the note. Never warped, never gated, never
#           modulated. The mids swirl and the low end does not move - which
#           is the whole recipe, and the reason the unison stack is
#           highpassed off the fundamental instead of fighting it.
#
#   FILTER  24 dB/octave, resonant, with drive inside it, and ITS CUTOFF
#           LIVES BETWEEN 140 AND 1800 Hz. That range is the difference
#           between a bass and a squeal: the growl of this genre is a
#           filter moving through the MIDS, and every harmonic above it is
#           a consequence, not a layer.
#
#   DRIVE   distortion after the filter, then a lowpass at 5 kHz, because
#           anything above that belongs to the drums.

_WTT = {}


def wt_time(name, frames=24, K=200, size=2048):
    """The wavetable as single cycles in TIME, not as harmonic amplitudes.

    A spectral table can only be read by summing partials, and summing
    partials cannot be warped - the moment the read pointer is bent, the
    harmonic relationship the sum assumed is gone. Every modern synth
    stores time-domain cycles for exactly this reason."""
    key = (name, frames, K, size)
    if key in _WTT:
        return _WTT[key]
    A = wtable(name, K, f0=90.0, frames=frames)
    T = np.zeros((frames + 1, size), dtype=np.float32)
    for i in range(frames):
        spec = np.zeros(size // 2 + 1, dtype=complex)
        spec[1:K + 1] = -1j * A[i, 1:K + 1] * (size / 2)
        w = np.fft.irfft(spec, size)
        T[i] = w / max(float(np.abs(w).max()), 1e-9)
    T[frames] = T[frames - 1]
    _WTT[key] = T
    return T


def _warp(p, bend=None, pwm=None, sync=None, fm=None, quant=None):
    """Serum's warp section, on the read pointer.

    THE PHASE IS WRAPPED TO [0,1) FIRST, and that line is not a detail. The
    running phase of a three-second note at 49 Hz reaches 150; every warp
    below is a function OF ONE CYCLE, so handing it 150 gives - depending on
    the warp - a clamp to a constant, or a number that is then taken modulo
    one and lands somewhere unrelated to where the wave actually was. The
    audible result is a bass whose character changes as the note runs on and
    whose rate of change scales with its pitch, because a higher note eats
    cycles faster. That is exactly the "pitch it up and it gets faster"
    coupling, and it is what turned this instrument into boiling mud.

    bend   p**k  - pinches the cycle toward one end (Bend+/-)
    pwm    a two-piece stretch - the pulse-width shift, on any waveform
    sync   (p*r) % 1 - the cycle restarts inside itself, and the tearing
           that leaves is the sound no filter makes
    fm     phase modulation at an integer ratio, which stays a pitch
    quant  floor(p*q)/q - sample-rate reduction that tracks the note, so
           the aliasing is harmonic instead of inharmonic
    """
    p = p % 1.0
    if bend is not None:
        p = np.clip(p, 1e-6, 1.0) ** np.exp2(2.0 * bend)
    if pwm is not None:
        w = np.clip(pwm, 0.06, 0.94)
        p = np.where(p < w, 0.5 * p / w, 0.5 + 0.5 * (p - w) / (1 - w))
    if fm is not None:
        p = p + fm * np.sin(2 * np.pi * 2.0 * p) * 0.5
    if sync is not None:
        p = (p * sync) % 1.0
    if quant is not None:
        q = np.maximum(quant, 2.0)
        p = np.floor(p * q) / q
    return p % 1.0


def wt_read(T, pos, p):
    """bilinear over (frame, phase)"""
    frames, size = T.shape
    pf = np.clip(pos, 0, frames - 1.001)
    i0 = pf.astype(np.intp)
    fr = (pf - i0)[:, None] if False else (pf - i0)
    x = (p % 1.0) * size
    j0 = x.astype(np.intp) % size
    j1 = (j0 + 1) % size
    fx = x - np.floor(x)
    a = T[i0, j0] * (1 - fx) + T[i0, j1] * fx
    b = T[i0 + 1, j0] * (1 - fx) + T[i0 + 1, j1] * fx
    return a * (1 - fr) + b * fr


def ladder(x, cut, res=0.5, drive=1.0, poles=2, block=96):
    """A resonant lowpass with drive inside it, 12 or 24 dB per octave.

    TWELVE IS THE DEFAULT AND THAT IS A MEASUREMENT, not a preference. The
    reference reese in `samples/` falls at about six decibels per octave
    above 1 kHz - which is a saw's own slope, barely filtered. A 24 dB/oct
    ladder at 600 Hz leaves 40 dB less than that at 2 kHz, and a bass with
    nothing between 1 and 4 kHz is a sub with a hum on top: no teeth, and
    no way to hear what the filter is doing.

    A lowpassed copy of the input goes back in because a resonant filter
    loses its bottom exactly when the resonance is doing the most work."""
    q = 0.72 + 8.5 * float(np.clip(res, 0, 1))
    y = svf(x, cut, q=q, kind='lp', block=block, sat=drive if drive > 1.01 else 0.0)
    if poles >= 4:
        y = svf(y, cut * 1.06, q=0.72, kind='lp', block=block)
    if res > 0.25:
        y = y + 0.30 * res * lp(x, np.clip(float(np.median(cut)) * 0.45, 60, 400), 2)
    return y


def osc(ph, table, pos, L, n, voices=3, detune=19.0, seed=0, os_=4, spread=0.75):
    """the unison stack, warped, at four times the sample rate"""
    m = n * os_
    xi = np.arange(m) / os_
    idx = np.arange(n, dtype=np.float64)
    php = np.interp(xi, idx, ph) / (2 * np.pi)

    def up(v):
        return np.interp(xi, idx, v)

    pos_o = up(pos)
    bend = up(L['bend_l']) if L['bend_l'] is not None else None
    pwm = up(L['pwm_l']) if L['pwm_l'] is not None else None
    sync = up(L['sync_l']) if L['sync_l'] is not None else None
    fm = up(L['fm_l']) if L['fm_l'] is not None else None
    qz = up(L['quant_l']) if L['quant_l'] is not None else None

    rs = np.random.RandomState(seed + 5)
    offs = np.linspace(-1, 1, voices) if voices > 1 else np.zeros(1)
    outL = np.zeros(m)
    outR = np.zeros(m)
    for k, o in enumerate(offs):
        r = 2.0 ** (o * detune / 1200.0)
        p = _warp(php * r + rs.rand(), bend, pwm, sync, fm, qz)
        w = wt_read(table, pos_o, p)
        pan = o * spread
        ang = (pan + 1) * np.pi / 4
        outL += w * np.cos(ang) * 1.41
        outR += w * np.sin(ang) * 1.41
    y = np.stack([resample_poly(outL, 1, os_)[:n],
                  resample_poly(outR, 1, os_)[:n]], 1) / voices
    return y.astype(np.float32)


# A BASSLINE IS A RHYTHM. This is the correction that matters most on this
# record, and it took three passes to find.
#
# The obvious way to build this sound - and what half the writing about the
# genre says - is one long note whose modulation rate changes inside it. Do
# that and you get dubstep: a continuous churn with no events in it, which
# is heard as boiling mud rather than as a bass line. What the genre
# actually does is play NOTES, with SILENCE between them:
#
#     тум ---- пауза ---- тум ---- пауза ---- тум-тум, ту-тум
#
# So there is no LFO anywhere in this instrument. Each note gets its own
# filter envelope - a sweep that happens once, across that note - and the
# variation across a bar is which notes, how long, and which of the eight
# characters below each one uses. A long note sweeping its filter upward is
# the "вУУууу"; a one-step note with the filter slamming shut is the stab;
# and the gap after either is as much a part of the line as they are.
#
# Two warps survive from the modern-synth section above: BEND and PWM, both
# of which shape a waveform smoothly. Hard sync does not - swept over a
# note it is the sound of a needle being dragged across a record - and
# neither does quantise, which is where the boiling came from.

# EACH CHARACTER IS A DIFFERENT WAVEFORM, not the same one at a different
# pitch. `tab` is which spectral table it reads and `det` how far its three
# unison voices are spread, so a stab and a swell are two instruments that
# happen to share a filter - which is the whole reason a wavetable synth has
# more than one table in it.
VOICE = {
    # The filter's whole travel lives between 140 and 1200 Hz. The bass line
    # sits just above the kick and it is a LOW instrument: everything above
    # the cutoff is what the distortion makes of it, not where the notes are.
    #
    # name      the filter's travel        how long it takes    the table
    'L': dict(c0=115, c1=471, tau=0.30, rise=True,  pos=(0.05, 0.72),
              res=0.52, dist=0.62, bend=0.25, pwm=0.0,  amp=1.00,
              tab='reeseb', det=26.0),                               # вУУууу
    'W': dict(c0=533, c1=124, tau=0.085, rise=False, pos=(0.62, 0.14),
              res=0.58, dist=0.67, bend=0.30, pwm=0.0,  amp=1.00,
              tab='growl', det=19.0),                                # tum
    'G': dict(c0=335, c1=205, tau=0.18, rise=False, pos=(0.35, 0.70),
              res=0.66, dist=0.90, bend=0.0,  pwm=0.34, amp=0.98,
              tab='rip', det=15.0),                                  # growl
    'T': dict(c0=291, c1=174, tau=0.16, rise=False, pos=(0.22, 0.55),
              res=0.55, dist=0.54, bend=0.35, pwm=0.0,  amp=0.95,
              vow=0.75, tab='vowel', det=12.0),                      # talking
    'S': dict(c0=713, c1=161, tau=0.030, rise=False, pos=(0.80, 0.32),
              res=0.62, dist=0.74, bend=0.0,  pwm=0.28, amp=1.00,
              tab='hollow', det=9.0),                                # stab
    'B': dict(c0=180, c1=102, tau=0.20, rise=False, pos=(0.10, 0.04),
              res=0.42, dist=0.40, bend=0.0,  pwm=0.0,  amp=1.00,
              tab='morph', det=22.0),                                # round
    'R': dict(c0=236, c1=608, tau=0.12, rise=True,  pos=(0.25, 0.88),
              res=0.68, dist=0.84, bend=0.0,  pwm=0.40, amp=1.00,
              tab='metal', det=17.0),                                # rip up
    'D': dict(c0=434, c1=90, tau=0.13, rise=False, pos=(0.58, 0.02),
              res=0.50, dist=0.52, bend=0.40, pwm=0.0,  amp=1.00,
              tab='witch', det=24.0),                                # falling
}


def _noteenv(n, ev, atk=0.004, rel=0.055, floor=0.0):
    """One amplitude envelope for the whole phrase, max-accumulated.

    Every note ends - that is the point of this instrument - but two notes
    that overlap must not restart the oscillator, so the envelope is built
    by taking the maximum rather than by concatenating segments."""
    amp = np.full(n, float(floor))
    a = max(int(atk * SR), 8)
    r = max(int(rel * SR), 32)
    for st, ln, _, _ in ev:
        k = min(int(st * STEP), n - 1)
        h = max(int(ln * STEP) - a, a)
        seg = np.concatenate([np.linspace(0, 1, a) ** 0.6, np.ones(h),
                              np.cos(np.linspace(0, np.pi / 2, r)) ** 2])
        e = min(n, k + len(seg))
        np.maximum(amp[k:e], seg[:e - k], out=amp[k:e])
    return uniform_filter1d(amp, max(int(0.003 * SR), 3))


def _pernote(n, ev, key, default=0.0, per_sample=None):
    """a lane that holds one value per note, and the default in the gaps"""
    out = np.full(n, float(default))
    for st, ln, _, kind in ev:
        v = VOICE[kind]
        k = min(int(st * STEP), n - 1)
        e = min(n, k + int((ln + 4) * STEP))
        out[k:e] = v.get(key, default)
    return uniform_filter1d(out, max(int(0.006 * SR), 3))


def _cutlane(n, ev, bright=1.0):
    """The filter envelope, once per note. This is where the sound is: a
    sweep that HAPPENS ONCE across a note is an articulation, and the same
    sweep repeating four times a beat is a wobble."""
    cut = np.full(n, 200.0)
    pos = np.full(n, 0.1)
    for st, ln, _, kind in ev:
        v = VOICE[kind]
        k = min(int(st * STEP), n - 1)
        e = min(n, k + int((ln + 5) * STEP))
        if e <= k:
            continue
        t = np.arange(e - k) / SR
        u = 1 - np.exp(-t / v['tau'])
        cut[k:e] = v['c0'] * bright * (v['c1'] / v['c0']) ** u
        pos[k:e] = v['pos'][0] + (v['pos'][1] - v['pos'][0]) * u
    return (uniform_filter1d(cut, max(int(0.005 * SR), 3)),
            uniform_filter1d(pos, max(int(0.008 * SR), 3)))


def bassline(events, bars=2, seed=0, gain=1.0, tail=6, tab='growl',
             voices=3, detune=19.0, spread=0.9, sub=1.0, drive=1.0,
             top=6500.0, hpf=112.0, glide=0.024, h2=0.95, h3=0.34,
             subrel=0.13, edge_=1.0, char=1.0, teeth=0.55, deep=1.0,
             h4=0.22, sublp=255.0, subsub=0.0, keyref=31,
             oct_=0.42, octcut=3.0, keytrack=0.5, subfold=38, bends=(),
             bright=1.0, air=0.0, airband=(2600.0, 9500.0), oct_hi=3000.0,
             hall=0.0, halldecay=3.2, hallcut=250.0, hallpre=0.038,
             halltone=2400.0, move=0.0, notchd=0.0, notchrate=0.25,
             stage2=0.0):
    """events: (step, length_in_steps, midi, character). Rests are simply
    steps no event covers, and they are the half of this that people hear.

    THREE BANDS, one instrument. They share a phase track and a note
    envelope, so they cannot disagree about the note or about when it ends,
    and each is filtered for the octave it lives in:

        sub     a locked sine, 20-120 Hz. `deep` is its weight.
        body    the wavetable through the ladder, 110-900 Hz. The notes.
        oct     the same oscillator an octave up through its own ladder at
                `octcut` times the cutoff, band-passed 340-3200 Hz. This is
                what makes the instrument span five octaves instead of two,
                and it is a BAND-LIMITED layer following the same envelope -
                not a separate voice with a spectrum of its own.
    """
    n = int((bars * 16 + tail) * STEP)
    ev = sorted(events)
    # `bends` go into the PITCH track and not into the note envelope, so the
    # line changes note without re-articulating. That is legato, and on this
    # instrument it is the difference between a phrase and a list of events:
    # the oscillator never stops, so the slide is the sound of one thing
    # moving rather than of two things next to each other.
    pp = sorted([(st, m) for st, _, m, _ in ev] + [(float(a), int(b)) for a, b in bends])
    f = _ftrack(pp, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    # The sub folds down an octave for anything the line plays above
    # `subfold`, so the bottom of the instrument stays where it was while
    # the line moves up. Without it a phrase an octave up has no weight and
    # reads as a different, smaller instrument.
    fs = _ftrack([(st, m - 12 if m >= subfold else m) for st, m in pp], n, glide)
    phs = 2 * np.pi * np.cumsum(fs) / SR

    amp = _noteenv(n, ev)
    cut, pos = _cutlane(n, ev, bright)
    L = {'bend_l': None, 'pwm_l': None, 'sync_l': None, 'fm_l': None,
         'quant_l': None}
    bl = _pernote(n, ev, 'bend', 0.0)
    pl = _pernote(n, ev, 'pwm', 0.0)
    if bl.max() > 0.01:
        L['bend_l'] = bl * (2 * scan(n, 0.25, 'sine', phase0=1.0) - 1) * 0.6 + bl * 0.4
    if pl.max() > 0.01:
        L['pwm_l'] = 0.5 + pl * (scan(n, 0.5, 'sine', phase0=2.2) - 0.5)

    used = []
    for _, _, _, k in ev:
        t = VOICE[k].get('tab', tab)
        if t not in used:
            used.append(t)
    x = np.zeros((n, 2), dtype=np.float32)
    for ti, t in enumerate(used):
        T = wt_time(t)
        m = np.zeros(n)
        dt = detune
        for st, ln, _, k in ev:
            if VOICE[k].get('tab', tab) != t:
                continue
            a = min(int(st * STEP), n - 1)
            e = min(n, a + int((ln + 4) * STEP))
            m[a:e] = 1.0
            dt = detune * VOICE[k].get('det', 19.0) / 19.0
        m = uniform_filter1d(m, max(int(0.010 * SR), 3))
        x += osc(ph, T, np.clip(pos, 0, 1) * (T.shape[0] - 2), L, n, voices,
                 dt, seed + 3 * ti, spread=spread) * m[:, None]
    x = hp(x, hpf, 2)

    if move:
        # A held note with one filter sweep across it is one gesture, and a
        # bar of one gesture is bland however good the gesture is. This
        # steps the wavetable position and the cutoff at every EIGHTH inside
        # any note long enough to have an inside - a stepped sequence, not
        # an LFO, so it is heard as the sound changing on the grid rather
        # than as a wobble. Seeded per note, so it repeats when the bar does.
        seq = np.zeros(n)
        for st, ln, _, kk in ev:
            if ln < 3:
                continue
            rs2 = np.random.RandomState(int(st * 7 + seed) % 997)
            ns = max(2, int(ln // 2))
            vals = rs2.uniform(-1, 1, ns)
            a = min(int(st * STEP), n - 1)
            e = min(n, a + int(ln * STEP))
            if e <= a:
                continue
            idx = np.clip((np.arange(e - a) / (e - a) * ns).astype(int), 0, ns - 1)
            seq[a:e] = vals[idx]
        seq = uniform_filter1d(seq, max(int(0.010 * SR), 3)) * move
        pos = np.clip(pos + seq * 0.32, 0, 1)
        cut = cut * (2.0 ** (seq * 0.75))

    res = float(np.median(_pernote(n, ev, 'res', 0.5)))
    # Key tracking. A cutoff fixed in hertz means an octave up has half the
    # harmonics under it and reads as a duller instrument rather than as the
    # same one higher; every synth has this control and it is why a line can
    # move register without changing character.
    kt = (f / midi(keyref)) ** keytrack if keytrack else 1.0
    y = ladder(x, np.clip(cut * kt, 90, 9000), res, 1.5 * drive, poles=2)
    vw = _pernote(n, ev, 'vow', 0.0)
    if float(vw.max()) > 0.02:
        y = y * (1 - vw[:, None]) + vw[:, None] * morph_formant(
            y, 'oo', 'aw', np.clip((cut - 200) / 900, 0, 1), 1.0, 1.4)
    if notchd:
        # One gap travelling through the harmonics. A swept lowpass reads as
        # brightness; a swept notch reads as MOTION, and it is the thing
        # that separates a reese from a detuned saw - the ear tracks the
        # gap rather than the tone. One cycle per bar, so it is a phrase.
        ne = scan(n, notchrate, 'sine', phase0=0.6)
        y = y - notchd * sweep_bp(y, 420.0, 2800.0, ne, bands=6, width=0.20)
    dl = _pernote(n, ev, 'dist', 0.3)
    y = y / max(float(np.abs(y).max()), 1e-9)
    y = y * (1 - dl[:, None]) + dl[:, None] * drive_asym(y, 7.0, 0.24)
    if stage2:
        # A second gain stage with an EQ in front of it. Every stage after
        # an EQ makes harmonics that were not there before, which is where
        # the grit of this genre comes from - one saturator, however hard,
        # only ever makes the same ones.
        y = y + stage2 * bandpass(y, 400.0, 1800.0)
        y = y / max(float(np.abs(y).max()), 1e-9)
        y = drive_asym(y, 3.4, 0.20)
    if teeth:
        # An EQ between two gain stages, which is where a neuro bass gets
        # the part of it a phone can reproduce. The reference carries 3.7%
        # of its energy in 800-3000 Hz and a filter this low leaves 1.5%.
        y = y + teeth * bandpass(y, 700, 2600) + teeth * 0.55 * bandpass(y, 2200, 5200)
        y = y / max(float(np.abs(y).max()), 1e-9)
        y = np.tanh(1.7 * y) / np.tanh(1.7)
    _pk = max(float(np.abs(y).max()), 1e-9)
    y = compress(y, thresh=0.30, ratio=3.5, attack=0.005, release=0.085)
    y = y * (_pk / max(float(np.abs(y).max()), 1e-9))
    y = lp(y, top, 4) * amp[:, None] * char * 1.30

    # the sub, gated with the same notes but let go more slowly, so the low
    # end thins between them instead of switching off
    samp = _noteenv(n, ev, atk=0.006, rel=subrel)
    body = (np.sin(phs) + h2 * np.sin(2 * phs) + h3 * np.sin(3 * phs)
            + h4 * np.sin(4 * phs))
    if subsub:
        # An octave under the root. On a rig it is the difference between a
        # low note and a room moving; on a laptop it is nothing at all, and
        # it costs headroom either way - so it is a knob and not a default.
        body = body + subsub * np.sin(0.5 * phs)
    body = np.tanh(1.3 * body / (1 + h2 + h3 + h4 + subsub)) / np.tanh(1.3)
    low = lp(stereo(body * samp), sublp, 4) * sub * 1.05 * deep

    if oct_:
        xo = osc(ph * 2.0, T, np.clip(pos * 0.8 + 0.15, 0, 1) * (T.shape[0] - 2),
                 L, n, max(voices - 1, 2), detune * 0.7, seed + 7, spread=1.0)
        yo = ladder(hp(xo, 230, 2), np.clip(cut * kt * octcut, 200, 13000),
                    res * 0.8, 1.3 * drive, poles=2)
        yo = yo / max(float(np.abs(yo).max()), 1e-9)
        yo = yo * (1 - dl[:, None]) + dl[:, None] * drive_asym(yo, 5.5, 0.24)
        y = y + bandpass(yo, 420, oct_hi) * amp[:, None] * oct_

    if air:
        # The top layer. Two octaves up, band-limited, and following the
        # same note envelope - so its spectrum FALLS above its band instead
        # of being flattened into it. That distinction is the whole
        # difference between a bright bass and a needle on a record.
        Ta = wt_time('rip')
        xa = osc(ph * 4.0, Ta, np.clip(pos * 0.6 + 0.35, 0, 1) * (Ta.shape[0] - 2),
                 L, n, 2, detune * 0.45, seed + 13, spread=1.0)
        ya = ladder(hp(xa, 700, 2), np.clip(cut * kt * octcut * 2.4, 700, 15000),
                    res * 0.55, 1.2, poles=2)
        ya = ya / max(float(np.abs(ya).max()), 1e-9)
        ya = drive_asym(ya, 4.5, 0.22)
        y = y + bandpass(ya, airband[0], airband[1]) * amp[:, None] * air

    if hall:
        # Depth, and only the band that can take it. A concert hall on the
        # whole instrument smears the low end into a wash - the tail of a
        # 49 Hz note is still sounding two bars later and every note after
        # it sums against it at an unrelated phase. So the split is at 250
        # Hz: everything under it stays dry and mono, and the room is put
        # on the character. The pre-delay lets the dry attack land first,
        # which is what makes a sound far away rather than blurred.
        _, hb = split(y, hallcut)
        y = y + hall * reverb(hb, decay=halldecay, wet=1.0, tone=halltone,
                              predelay=hallpre)[:n]

    if edge_:
        y = y + edge(n, [int(st * STEP) for st, _, _, _ in ev],
                     0.26 * edge_, seed + 11, lo=400, hi=3400)
    return ((low + y) * 0.62).astype(np.float32) * gain


def parse(pat, note=31, unit=1):
    """A bar of bass as sixteen characters.

        'L...-...W-..S-s-'

    A letter starts a note of that character, '.' holds it, '-' is silence,
    and silence is written explicitly because it is the thing this line is
    made of. Lower case is the same character at two thirds the length.
    Returns (step, length, midi, kind) events."""
    ev = []
    i = 0
    while i < len(pat):
        c = pat[i]
        if c in '-. ':
            i += 1
            continue
        j = i + 1
        while j < len(pat) and pat[j] == '.':
            j += 1
        ln = (j - i) * unit
        ev.append((i * unit, ln * (0.66 if c.islower() else 1.0), note,
                   c.upper()))
        i = j
    return ev


def line(bars_pat, notes=None, root=31, bars=None, moves=(), slides=(),
         push=(), **kw):
    """A phrase: one pattern string per bar, one note per bar, and `moves` -
    (bar, step, midi) - for the places the line jumps register inside a bar.

    Register is half of what makes a bass line dynamic rather than a loop,
    and it costs nothing here: the sub folds an octave down above `subfold`
    and the filter key-tracks, so the line can go up an octave and the
    instrument stays the same size.

    `slides` - (bar, step, midi) - bend the pitch mid-note with no attack.
    `push`   - (bar, step, delta) - move one event off the grid, in steps.
               A sixteenth-note line where every event is exactly on its
               step is the thing that reads as monotonous however good the
               notes are; a third of a step late on one hit per bar is not
               heard as lateness, it is heard as a player."""
    pats = bars_pat if isinstance(bars_pat, (list, tuple)) else [bars_pat]
    bars = bars or len(pats)
    mv = sorted((int(b) * 16 + float(st), int(m)) for b, st, m in moves)
    ev = []
    for b, p in enumerate(pats):
        nt = root if notes is None else notes[b % len(notes)]
        # A bar written with 32 characters is read in thirty-seconds, which
        # is what a group of fast stabs needs: at 174 one of them is 43 ms.
        for st, ln, _, k in parse(p, nt, unit=16.0 / len(p)):
            a = st + 16 * b
            m = nt
            for pos, mm in mv:
                if pos <= a + 1e-6:
                    m = mm
            ev.append((a, ln, m, k))
    for pb, ps, d in push:
        a0 = int(pb) * 16 + float(ps)
        ev = [(st + d, ln, m, k) if abs(st - a0) < 1e-6 else (st, ln, m, k)
              for st, ln, m, k in ev]
    bd = [(int(b) * 16 + float(st), int(m)) for b, st, m in slides]
    return bassline(sorted(ev), bars=bars, bends=bd, **kw)
def subline(notes, bars=2, gain=1.0, tail=4, glide=0.030, h2=0.90, h3=0.32,
            gatep=None, drive=1.3, decay=0.0):
    """The clean mono sub for the sections where the creature is absent or
    sparse. One sine, one phase, no distortion worth the name, lowpassed at
    140 - and it never plays at the same time as the creature's own body."""
    n = int((bars * 16 + tail) * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + h2 * np.sin(2 * ph) + h3 * np.sin(3 * ph)
    x = x * _amp(notes, n, decay, 0.005, 0.0)
    if gatep is not None:
        x = x * np.clip(slane(gatep, n, 'hold', 0.006), 0, 1)
    k = int(bars * 16 * STEP)
    if k < n:
        x[k:] *= np.cos(np.linspace(0, np.pi / 2, n - k)) ** 2
    y = np.tanh(drive * x / (1 + h2 + h3)) / np.tanh(drive)
    return (lp(stereo(y), 175, 4) * adsr(n, a=0.005, r=0.010)[:, None]) * gain * 0.95


# ============================================================== the void ===
# Everything above is an instrument. This is the place they are in: a hull,
# a room tone, an alarm four streets away, something enormous passing.

def star(notes, bars=4, gain=1.0, cutoff=900.0, attack=1.6, seed=0, tail=6,
         space=0.55, decay=6.0, drift=1.0):
    """A collapsing star: inharmonic partials that never quite agree.

    Not a pad and not a bell. The partials sit at 1, 1.5, 2, 3, 4 and 6
    times the root - the low end of a struck object's series - each panned
    somewhere different, each drifting a few cents against the others at a
    rate of its own, and the whole thing arrives over a second and a half so
    it has no attack to identify it by. Above 900 Hz there is nothing, which
    is what keeps it from reading as a bell (theory/90-memories/pitched-
    metal-reads-as-cheerful.md)."""
    n = int((bars * 16 + tail) * STEP)
    t = np.arange(n) / SR
    rs = np.random.RandomState(seed)
    L = np.zeros(n)
    R = np.zeros(n)
    for m in notes:
        f = midi(m)
        for j, r in enumerate((1.0, 1.5, 2.0, 3.01, 4.02, 5.98)):
            det = 2 ** (rs.uniform(-11, 11) * drift / 1200.0)
            slow = 0.72 + 0.28 * np.sin(2 * np.pi * rs.uniform(0.02, 0.09) * t + rs.rand() * 6)
            a = (0.62 / (1 + j * 0.95)) * slow
            x = a * np.sin(2 * np.pi * f * r * det * t + rs.rand() * 6)
            p = (rs.rand() * 2 - 1) * 0.9
            ang = (p + 1) * np.pi / 4
            L += x * np.cos(ang) * 1.41
            R += x * np.sin(ang) * 1.41
    env = np.ones(n)
    a = min(int(attack * SR), n // 2)
    env[:a] = (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a)))
    k = int(bars * 16 * STEP)
    if k < n:
        env[k:] *= np.cos(np.linspace(0, np.pi / 2, n - k)) ** 2
    y = lp(np.stack([L, R], 1).astype(np.float32) * env[:, None] * 0.30, cutoff, 4)
    if space:
        y = y + space * reverb(y, decay=decay, wet=1.0, tone=2400, predelay=0.03)[:n]
    return mono_below(y, 170) * gain


def hull(bars=8, gain=1.0, seed=0, tail=2, tone=1.0, swell=1.0):
    """Room tone for somewhere with machinery in it: brown noise through
    three slow resonances, breathing. Fills 60-700 Hz with something that is
    not a note, which is what makes the silences sound like a place rather
    than like an empty file."""
    n = int((bars * 16 + tail) * STEP)
    t = np.arange(n) / SR
    rs = np.random.RandomState(seed)
    nz = np.cumsum(rs.randn(n, 2) * 0.02, axis=0)
    nz = nz - uniform_filter1d(nz, int(0.05 * SR), axis=0)
    y = (nz / max(float(np.abs(nz).max()), 1e-9)).astype(np.float32)
    out = np.zeros((n, 2), dtype=np.float32)
    for f, rate, ph0 in ((88.0, 0.031, 0.0), (232.0, 0.019, 1.7), (547.0, 0.043, 3.1)):
        e = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t + ph0)
        out += sweep_bp(y, f * 0.72 * tone, f * 1.5 * tone, e, bands=4, width=0.22)
    env = 0.62 + 0.38 * swell * (0.5 - 0.5 * np.cos(2 * np.pi * 0.023 * t + 2.0))
    return mono_below(out * env[:, None], 150) * gain * 0.5


def sheet(bars=8, gain=1.0, seed=0, tail=2, lo=3400.0, hi=12500.0, rate=0.05):
    """The top of the room: broad noise through four high resonances that
    drift against each other.

    An industrial or darkstep palette is dark by construction - a driven
    sine, a reverb tail, a closed hat - and measures 1-2% above 3 kHz, which
    a rig hears as a blanket over the record. An air shelf multiplies a band
    that is empty; this puts something in it. It has to be UNTUNED: a bright
    ringing pitched object up there is a glockenspiel, an untuned one is a
    room (theory/90-memories/industrial-techno-measures-too-dark.md)."""
    n = int((bars * 16 + tail) * STEP)
    t = np.arange(n) / SR
    rs = np.random.RandomState(seed)
    y = rs.randn(n, 2).astype(np.float32)          # independent per channel
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(np.geomspace(lo, hi, 4)):
        e = 0.5 - 0.5 * np.cos(2 * np.pi * rate * (1 + 0.4 * i) * t + i * 1.9)
        out += sweep_bp(y, f * 0.8, f * 1.35, e, bands=4, width=0.10) / (1 + 0.3 * i)
    env = 0.55 + 0.45 * (0.5 - 0.5 * np.cos(2 * np.pi * 0.017 * t))
    return (out * env[:, None]) * gain * 0.35


@cached
def siren(dur_steps=32, gain=1.0, f0=760.0, sweep=0.22, rate=0.33, seed=0,
          space=0.8):
    """An alarm several streets away. Narrow, filtered, drenched, and at a
    constant level - a rising sweep that also gets louder is a scream, and
    this is supposed to be someone else's emergency."""
    n, t = steps(dur_steps)
    f = f0 * (1 + sweep * (0.5 - 0.5 * np.cos(2 * np.pi * rate * t)))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    x = x + 0.35 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    y = bandpass(stereo(x.astype(np.float32)), f0 * 0.7, f0 * 3.4)
    y = y * (adsr(n, a=0.25, r=0.6))[:, None] * 0.25
    if space:
        y = y + space * reverb(y, decay=3.2, wet=1.0, tone=2600, predelay=0.05)[:n]
    return narrow(y, 1.15) * gain


@cached
def transit(dur_steps=12, gain=1.0, seed=0, f0=520.0, low=0.6, pan=1.0):
    """Something enormous going past: a band of noise whose centre falls as
    it passes, level a bell curve, panned across. A doppler, not a riser."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    u = np.arange(n) / n
    y = rs.randn(n, 2).astype(np.float32)
    e = np.clip(1.15 - u * 1.25, 0, 1)
    y = sweep_bp(y, f0 * 0.42, f0 * 1.9, e, bands=6, width=0.55)
    y = y + low * lp(stereo(np.cumsum(rs.randn(n)) * 0.0006), 130, 4)
    amp = np.exp(-((u - 0.42) / 0.26) ** 2)
    ang = ((np.clip(-pan + 2 * pan * u, -1, 1)) + 1) * np.pi / 4
    out = np.stack([y[:, 0] * np.cos(ang) * 1.41, y[:, 1] * np.sin(ang) * 1.41], 1)
    return (out * (amp * adsr(n, a=0.02, r=0.05))[:, None]).astype(np.float32) * gain


@cached
def impact(dur_steps=16, gain=1.0, seed=0, tune=58.0, tail=1.0):
    """The arrival: a low sine dropping, a lowpassed burst, and a reversed
    tail placed so it ends on the downbeat."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    f = tune * (1 + 1.4 * np.exp(-t / 0.05))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.55)
    y = lp(stereo(np.tanh(1.8 * x)), 220, 4)
    y = y + 0.55 * lp(stereo(rs.randn(n) * np.exp(-t / 0.30)), 900, 4)
    y = y + tail * 0.35 * reverb(y, decay=2.4, wet=1.0, tone=2000)[:n]
    return norm(y * adsr(n, a=0.001, r=0.2)[:, None], 0.95) * gain


@cached
def plunge(dur_steps=8, gain=1.0, f0=98.0, f1=23.0, drive=1.7):
    """The sub drop before an arrival: 98 Hz to 23 over half a bar, so the
    bottom of the sweep lands just before the downbeat."""
    n, t = steps(dur_steps)
    u = np.arange(n) / n
    f = f0 * (f1 / f0) ** (u ** 0.8)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - 0.35 * u)
    y = np.tanh(drive * x) / np.tanh(drive)
    return lp(stereo(y), 180, 4) * adsr(n, a=0.004, r=0.05)[:, None] * gain * 0.9


@cached
def lift(dur_steps=16, gain=1.0, seed=0, f0=300.0, f1=2500.0, tone=0.5):
    """A build that rises in PITCH and not in level.

    The ear is most sensitive at 2-5 kHz, so a rising sweep is heard as a
    crescendo before any fader is touched. Putting a real one under it
    doubles a curve that was already there and the result is a scream
    (theory/90-memories/a-rising-sweep-must-not-also-crescendo.md). So the
    level holds and the brightness CLOSES as the pitch climbs."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    u = (np.arange(n) / n) ** 1.35
    y = stereo(rs.randn(n).astype(np.float32))
    y = sweep_bp(y, f0, f1, u, bands=7, width=0.30)
    if tone:
        ft = f0 * (f1 / f0) ** u
        y = y + tone * 0.5 * stereo(np.sin(2 * np.pi * np.cumsum(ft) / SR).astype(np.float32))
    y = morph_lp(y, f1 * 1.4, f1 * 4.5, 1 - 0.78 * u, bands=6)
    env = 0.86 + 0.14 * u
    return (y * (env * adsr(n, a=0.03, r=0.008))[:, None]).astype(np.float32) * gain * 0.5


def code(bars=4, gain=1.0, seed=0, tail=1, density=0.30, bits=5, lo=2200.0,
         hi=8000.0):
    """Data bursts: short bitcrushed ticks ON THE GRID.

    A texture of scattered high-frequency clicks is what the ear reports as
    crackle rather than as brightness, and the thing that separates a part
    from a fault is whether the ticks share a phase within the step. These
    land on sixteenths (theory/90-memories/do-not-fix-a-band-number-with-a-
    texture.md)."""
    n = int((bars * 16 + tail) * STEP)
    rs = np.random.RandomState(seed)
    x = np.zeros((n, 2))
    ln = int(0.022 * SR)
    te = np.arange(ln) / SR
    for st in range(bars * 16):
        if rs.rand() > density:
            continue
        k = int(st * STEP)
        d = rs.uniform(0.002, 0.010)
        p = rs.rand()
        x[k:k + ln, 0] += rs.randn(ln) * np.exp(-te / d) * rs.uniform(0.4, 1.0) * (1.3 - p)
        x[k:k + ln, 1] += rs.randn(ln) * np.exp(-te / d) * rs.uniform(0.4, 1.0) * (0.3 + p)
    y = bandpass(x.astype(np.float32), lo, hi)
    return bitcrush(y, bits=bits, downsample=2) * gain * 0.45


def lead(notes, bars=4, gain=1.0, tail=6, glide=0.055, cut=(420.0, 2400.0),
         crate=0.5, res=0.35, detune=14.0, voices=3, sub=0.35, dist=0.22,
         seed=0, space=0.6, decay=0.0, top=5200.0):
    """The other voice: a cold, detuned line that is not the bass.

    Two things keep it out of the bass's way. It lives between 300 Hz and
    2.5 kHz, which is the band the bass only visits when its filter is
    open; and it SLIDES - one continuous oscillator with portamento, so
    what identifies it is the movement between notes rather than the
    attack of them. It is a signal from something far away, not a hook.
    """
    n = int((bars * 16 + tail) * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fmax = float(f.max())
    rs = np.random.RandomState(seed + 3)
    L = np.zeros(n)
    R = np.zeros(n)
    for i, o in enumerate(np.linspace(-1, 1, voices)):
        r = 2.0 ** (o * detune / 1200.0)
        w = saw_ph(ph * r + rs.rand() * 6, fmax * r, kmax=90)
        ang = (o * 0.8 + 1) * np.pi / 4
        L += w * np.cos(ang) * 1.41
        R += w * np.sin(ang) * 1.41
    x = np.stack([L, R], 1).astype(np.float32) / voices
    if sub:
        x = x + sub * stereo(np.sin(ph).astype(np.float32))
    amp = _amp(notes, n, decay, 0.030, 0.0)
    k = int(bars * 16 * STEP)
    rel = np.ones(n)
    if k < n:
        rel[k:] = np.cos(np.linspace(0, np.pi / 2, n - k)) ** 2
    v = scan(n, crate, 'sine', phase0=0.4)
    y = ladder(x, cut[0] * (cut[1] / cut[0]) ** v, res, 1.0, poles=2)
    if dist:
        y = y / max(float(np.abs(y).max()), 1e-9)
        y = y * (1 - dist) + dist * drive_asym(y, 4.0, 0.2)
    y = lp(y, top, 4) * (amp * rel)[:, None]
    if space:
        y = y + space * reverb(y, decay=2.6, wet=1.0, tone=2600, predelay=0.035)[:n]
    return (y * 0.5).astype(np.float32) * gain


def scream(dur_steps=2.0, note=72, gain=1.0, seed=0, tau=0.045,
           v0='oh', v1='ah', drive=6.0, lo=230.0, hi=9000.0, decay=0.075,
           noise=0.22, up=False, space=0.35, rough=0.55, fry=0.40,
           overshoot=42.0, breakoff=65.0, vib=26.0, hold=0.80,
           sus=0.0, morph=None):
    """A shout, not a note in the top octave.

    Three detuned saws with a formant pair on them is a synthesiser playing
    high notes, and that is exactly what it sounds like. What separates a
    cry from that is not its spectrum, it is that it BEHAVES like something
    with a throat:

      the pitch overshoots by most of a semitone in the first fifteen
      milliseconds and falls back - nobody lands on a note when they shout;

      it is rough. Real shouting drives the folds into a nonlinear regime
      and the result is amplitude modulation in the twenties-to-seventies
      and a subharmonic underneath - vocal fry. Both of those are here and
      both decay, because the roughness is loudest at the start;

      there is breath before there is tone;

      the vibrato ARRIVES LATE, about a tenth of a second in, and grows;

      the formants are fixed in hertz and there are three of them. The
      third, at about 3 kHz, is the singer's formant - it is the reason a
      voice cuts through an orchestra, and a two-formant model has no way
      to do that;

      it BREAKS at the end rather than decaying: the pitch drops away over
      the last quarter and the tone goes with it.

    And the brightness follows the loudness, because a shout opens the
    tract as it gets louder rather than simply getting bigger.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    f0 = midi(note)
    u = t / max(t[-1], 1e-9)
    # THE CRY HAS TO SIT ON ITS NOTE. The overshoot is gone in thirty
    # milliseconds - it reads as an attack, not as a pitch - and the break
    # at the end only happens over the last fifth. In between, `hold` of the
    # note is at the written pitch, and if it is not the melody is simply
    # somewhere else than where it was written.
    cents = (overshoot * np.exp(-t / 0.011)
             - 7.0 * (1 - np.exp(-t / 0.10))
             - breakoff * np.clip((u - hold) / max(1 - hold, 1e-3), 0, 1) ** 2)
    if up:
        cents = cents + 70.0 * np.clip((u - 0.5) / 0.5, 0, 1)
    cents = cents + vib * np.sin(2 * np.pi * 5.9 * t) * np.clip((t - 0.060) / 0.12, 0, 1)
    f = f0 * 2 ** (cents / 1200.0)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fmax = float(f.max())

    x = sum(saw_ph(ph * 2 ** (d / 1200.0) + rs.rand() * 6, fmax, kmax=110)
            for d in (-19.0, 0.0, 19.0)) / 3
    if fry:                                  # the subharmonic, at the onset
        x = x + fry * saw_ph(0.5 * ph + rs.rand() * 6, fmax * 0.5, kmax=60) \
            * np.exp(-t / 0.055)
    # A sine at the written note, under everything. An 'ah' formant at 700
    # Hz boosts the second harmonic of a 392 Hz cry and leaves the first at
    # six percent, which is what a real throat does - and a real throat is
    # also being listened to by someone who can see a face. Here the pitch
    # has to be unambiguous, so the fundamental is put back explicitly.
    x = x + 0.55 * np.sin(ph) * np.exp(-t / 0.10)
    if noise:                                # breath before tone
        br = rs.randn(n) * (np.exp(-t / 0.018) + 0.25 * np.exp(-t / 0.12))
        x = x + noise * br
    if rough:                                # driven folds: AM in the 20-70 Hz
        rr = 38.0 + 26.0 * rs.rand()
        x = x * (1 - rough * 0.45 * np.exp(-t / 0.06)
                 * (0.5 + 0.5 * np.sin(2 * np.pi * rr * t + rs.rand() * 6)))

    y = stereo(x.astype(np.float32))
    if sus:
        # A held shout is not a longer decay. It falls to a plateau, sits
        # there while the vibrato grows into it, and then breaks - which is
        # what a voice does and what an exponential cannot.
        env = sus + (1 - sus) * np.exp(-t / decay)
        k = int(hold * n)
        if k < n:
            env[k:] *= np.cos(np.linspace(0, np.pi / 2, n - k)) ** 1.6
        env = env * adsr(n, a=0.0035, r=0.012)
    else:
        env = np.exp(-t / decay) * adsr(n, a=0.0025, r=0.02)
    # the tract opens with the level rather than after it; a held note
    # morphs across its own length instead
    e = (np.clip(u ** 0.75, 0, 1) if sus else
         np.clip(uniform_filter1d(env, max(int(0.004 * SR), 3)) ** 0.6, 0, 1))
    if morph is not None:
        e = np.clip(np.asarray(morph, dtype=np.float64) * np.ones(n), 0, 1)
    y = morph_formant(y, v0, v1, e, wet=0.85, gain=1.7)
    y = y + 0.45 * bandpass(y, 2750.0, 3350.0)          # the singer's formant
    y = y / max(float(np.abs(y).max()), 1e-9)
    y = drive_asym(y, drive, 0.26)
    # The highpass has to sit BELOW the note. At 520 Hz every cry written
    # under MIDI 72 lost its own fundamental and the ear then took the
    # second harmonic as the pitch - the melody was being heard an octave
    # above where it was written, which is what "совершенно не те ноты"
    # sounds like.
    y = bandpass(y, min(lo, midi(note) * 0.62), hi)
    y = y * env[:, None]
    if space:
        y = y + space * reverb(y, decay=1.6, wet=1.0, tone=4200, predelay=0.014)[:n]
    return norm(y, 0.95) * gain


def screams(pat, note=72, bar=0, gain=1.0, seed=0, hi_note=None, sus=0.62,
            **kw):
    """`'A.......a...----'` - one character per sixteenth, and it holds.

    A letter starts a cry, '.' holds it, '-' is a rest - the same convention
    the bass patterns use. A lower-case letter is quieter and lands on
    `note`, an upper-case one is louder and lands on `hi_note`. Anything
    longer than two steps is rendered as a HELD shout: it falls to a plateau
    and breaks at the end rather than simply decaying.

    BOTH NOTES ARE GIVEN, and neither is derived by adding an interval. A
    capital that is "a tone up" from whatever the lower one happens to be
    walks straight out of the mode about half the time - which is not heard
    as a variation, it is heard as the harmony going.
    """
    out = []
    i = 0
    while i < len(pat):
        c = pat[i]
        if c in '-. ':
            i += 1
            continue
        j = i + 1
        while j < len(pat) and pat[j] == '.':
            j += 1
        ln = j - i
        big = c.isupper()
        nt = (hi_note if hi_note else note) if big else note
        long_ = ln > 2
        seg = scream(ln + 1.6, nt, seed=(seed + bar * 16 + i) % 97,
                     decay=(0.24 if long_ else (0.115 if big else 0.085)),
                     drive=7.0 if big else 5.5,
                     sus=(sus if long_ else 0.0),
                     hold=0.80 if long_ else 0.80,
                     vib=34.0 if long_ else 26.0, **kw)
        out.append((i, seg, gain * (1.0 if big else 0.62)))
        i = j
    return out


def bark(dur_steps=2.0, note=43, gain=1.0, seed=0, drop=0.55, tau=0.013,
         decay=0.085, width=0.30, res=1.0, sync=0.0, drive=4.0, click=0.55,
         lo=110.0, hi=2800.0, body=1.0, cut=(2400.0, 340.0)):
    """The other instrument: something STRUCK, in the mid bass.

    A held bass note and a run of short ones are two different objects, and
    making the second out of the first - the same oscillator with a shorter
    envelope - is why a bass line can be rhythmically right and still read
    as one thing playing awkwardly. This is a different object: it has a
    pitch that DROPS when it is hit, a fixed body resonance that rings
    after the pitch has gone, a contact noise at the front, and no sustain
    at all.

    It is deliberately dry and deliberately mid - 110 Hz to 2.8 kHz - so it
    sits on top of the sustained bass rather than fighting it for the same
    octave.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    f0 = midi(note)
    f = f0 * (1 + drop * np.exp(-t / tau))
    ph = 2 * np.pi * np.cumsum(f) / SR
    fmax = float(f.max())
    # a band-limited pulse: two saws a fraction of a cycle apart
    x = (saw_ph(ph, fmax, kmax=90)
         - saw_ph(ph + 2 * np.pi * width, fmax, kmax=90)) * 0.5
    if sync:
        x = x * (1 - sync) + sync * _os_saw(ph, 1.0 + 3.0 * sync)
    if click:
        x = x + click * rs.randn(n) * np.exp(-t / 0.0035)
    y = stereo(x.astype(np.float32))
    env = np.exp(-t / decay)
    y = morph_lp(y, cut[1], cut[0], np.exp(-t / (decay * 0.55)), bands=7)
    if body:
        # the box it is mounted in: two fixed resonances that do not move
        # with the note, which is what makes it an object rather than a tone
        for fr, g, d in ((186.0, 0.9, 0.11), (327.0, 0.55, 0.07)):
            y = y + body * g * bandpass(y, fr * 0.92, fr * 1.10) \
                * np.exp(-t / d)[:, None]
    y = y / max(float(np.abs(y).max()), 1e-9)
    y = drive_asym(y, drive, 0.24)
    y = bandpass(y, lo, hi) * env[:, None]
    return norm(y * adsr(n, a=0.0006, r=0.012)[:, None], 0.95) * gain


def barks(pat, note=43, bar=0, gain=1.0, seed=0, hi_note=None, **kw):
    """`'W..S..G-W..S..s-'` read as strikes rather than as bass notes.

    Any letter is a hit; upper case is harder and lands on `hi_note` if one
    is given. The length a letter holds sets how long it rings."""
    out = []
    i = 0
    while i < len(pat):
        c = pat[i]
        if c in '-. ':
            i += 1
            continue
        j = i + 1
        while j < len(pat) and pat[j] == '.':
            j += 1
        ln = j - i
        big = c.isupper()
        nt = (hi_note if (big and hi_note) else note)
        kk = dict(decay=0.055 + 0.030 * min(ln, 4),
                  drive=5.0 if big else 3.6,
                  width=0.24 + 0.10 * ((bar + i) % 3))
        kk.update(kw)
        out.append((i, bark(min(ln + 1.2, 6.0), nt,
                            seed=(seed + bar * 16 + i) % 97, **kk),
                    gain * (1.0 if big else 0.72)))
        i = j
    return out
