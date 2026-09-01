"""Machine funk: the Noisia end of drum & bass, rebuilt from the filter up.

`neurolib` is the first attempt at 174 in this repo and it does not survive
measurement. Against two Magnetude records its tracks sit 4-5 dB quiet, put
19.5% of their energy in 400-1500 Hz where the reference puts 13%, hold only
half the reference's weight in 60-120 Hz, and leave holes in the low band -
a per-16th peak grid that falls to 0.30 where the reference never drops below
0.6. Three causes, and each one is a design decision rather than a mix
setting, which is why this is a new module and not a patch:

1. **The filter cannot resonate.** `core.morph_lp` crossfades a bank of
   static lowpasses. It is smooth, cheap and completely unable to scream:
   no self-oscillation, no peak that tracks the cutoff at Q>2, and the
   crossfade smears anything that moves faster than about 30 Hz. Neurofunk
   is a genre about a resonant filter being driven into distortion.
   This module is built on `core.svf` - a real time-varying biquad whose
   coefficients are recomputed every 64 samples with the state carried
   across the boundary - and stacks moving notches and formants on it.

2. **The bass is rendered note by note.** Each event was an independent
   segment, so overlapping tails at unrelated phases cancelled and the
   fundamental broke into pieces. Here the bass is ONE oscillator per phrase
   with an unbroken phase and a per-sample frequency track; the notes are
   changes in a parameter timeline, not new calls.

3. **The motion came from LFOs.** An LFO gives a shape that repeats; this
   music moves because every 16th of the bar has its OWN filter cutoff,
   resonance, drive, sync ratio, vowel and waveshape. That is what a `lane`
   is - a per-sample parameter timeline built from one value per step.

The chain, and the order matters:

    freq track -> phase -> PD/sync/FM oscillator stack   (2x oversampled)
      -> multiband split: sub kept clean and mono, everything else destroyed
      -> moving notch bank (reese) or moving formants (talk)
      -> resonant svf -> multiband drive -> resample -> svf again

Usage:
    from machinelib import *
    s = Session(64, tail=3.0)
    t = s.pos(0); s.hit(t)
    s.place(t, mkick(), bus='drums')
    s.place(t, subbar(((0, 29, 8), (8, 31, 8))), bus='sub')
    s.place(t, bassbar(((0, 41), (4, 41), (6, 44), (10, 39)), cut=[...]), bus='bass')
    s.render('neurofunk_something_174.wav', clip=0.9, limit=0.85)
"""
import numpy as np
import core
from core import *
from core import _lfo01, _reverb_ir, _bq, _ftrack, _amp
from scipy.signal import lfilter, fftconvolve
from scipy.ndimage import uniform_filter1d, maximum_filter1d

BAR, STEP = core.set_grid(bpm=174.0)
BPM = core.BPM

# The sub and the mid bass are one instrument in two bands and duck as one.
# At 174 BPM anything sustained that does not move out of the way turns the
# holes the drums were engineered to leave into fog.
Session.DUCKED = {'sub': 1.0, 'bass': 0.85, 'body': 0.9, 'music': 0.55,
                  'texture': 0.6, 'pad': 0.65, 'atmos': 0.4}


# ====================================================== the filter rack
def notchbank(seg, cut, spread=(1.0, 2.13, 3.47, 4.92), q=2.4, depth=1.0, block=96):
    """Four notches at non-harmonic spacing, all moving together.

    This is the reese - and it is not a phaser plugin. Two detuned saws only
    beat; what makes the sound is a set of gaps travelling up through their
    harmonics, and the ear tracks the gaps rather than the tone. Harmonic
    spacing would just sound like a comb filter on a pitch; 1 : 2.13 : 3.47
    is deliberately unrelated to the note.
    """
    cut = np.asarray(cut, dtype=np.float64)
    if cut.ndim == 0:
        cut = np.full(len(seg), float(cut))
    y = np.asarray(seg, dtype=np.float32)
    for m in spread:
        y = (1 - depth) * y + depth * svf(y, np.clip(cut * m, 40, 14000),
                                          q, 'notch', block)
    return y.astype(np.float32)


VOWELS = {'oo': (300, 870, 2240), 'oh': (570, 840, 2410), 'ah': (730, 1090, 2440),
          'eh': (530, 1840, 2480), 'ee': (270, 2290, 3010), 'ih': (390, 1990, 2550),
          'uh': (640, 1190, 2390), 'ae': (660, 1720, 2410)}


def formants(seg, v, q=7.0, gain=1.35, block=96):
    """A moving vocal tract. `v` is a list of vowel names, one per step - the
    formant pair jumps where the lane jumps, so the bass says a word per
    sixteenth instead of sliding through one long vowel."""
    n = len(seg)
    f1 = steplane([VOWELS[x][0] for x in v], n, 'exp', 0.006)
    f2 = steplane([VOWELS[x][1] for x in v], n, 'exp', 0.006)
    f3 = steplane([VOWELS[x][2] for x in v], n, 'exp', 0.006)
    out = (svf(seg, f1, q, 'bp', block) * 1.0
           + svf(seg, f2, q * 0.9, 'bp', block) * 0.72
           + svf(seg, f3, q * 0.8, 'bp', block) * 0.34)
    return (out * gain).astype(np.float32)


# ============================================================ the rack
def mbands(seg, xo=(105.0, 620.0, 2800.0)):
    """Four bands. Everything in this file that distorts does it per band -
    a full-range tanh on a bass turns the sub into intermodulation mud and
    makes the low end smaller, which is the opposite of the intent."""
    a = lp(seg, xo[0], 4)
    b = bandpass(seg, xo[0], xo[1], 2)
    c = bandpass(seg, xo[1], xo[2], 2)
    d = hp(seg, xo[2], 2)
    return a, b, c, d


def mbdrive(seg, g=(1.0, 2.5, 6.0, 3.0), mix=(1.0, 1.0, 1.0, 1.0),
            xo=(105.0, 620.0, 2800.0), fold_=(0.0, 0.0, 0.35, 0.0)):
    """Multiband distortion: the sub passes clean, the low mids get warmth,
    the mids get destroyed, the top gets edge. Folding only in band 3, where
    the inharmonic partials a wavefolder makes land in the range a phone can
    reproduce and a club system will not turn into rumble."""
    out = np.zeros_like(np.asarray(seg, dtype=np.float32))
    for band, gi, mi, fi in zip(mbands(seg, xo), g, mix, fold_):
        if gi <= 0:                      # drive 0 drops the band entirely
            continue
        y = band
        if fi:
            y = (1 - fi) * y + fi * fold(y, 1.4)
        if gi != 1.0:
            y = np.tanh(gi * y) / np.tanh(gi)
        out += (y * mi).astype(np.float32)
    return out


def rmod(seg, hz, mix=1.0):
    """Ring modulation. `hz` may be a lane, which is the point - a fixed ring
    mod is a novelty, one that steps to a new frequency every sixteenth is a
    rhythm made of inharmonic sidebands."""
    n = len(seg)
    hz = np.asarray(hz, dtype=np.float64)
    if hz.ndim == 0:
        hz = np.full(n, float(hz))
    c = np.sin(2 * np.pi * np.cumsum(hz) / SR)[:, None]
    return ((1 - mix) * seg + mix * seg * c).astype(np.float32)


def spread(seg, hz=380.0, f_l=740.0, f_r=1310.0, amount=0.45):
    """Width above `hz` by notching the channels at different frequencies.
    Summed to mono this leaves two shallow dips; a Haas delay would leave a
    comb with a fixed null, and half the audience is standing in it."""
    low, high = split(seg, hz)
    l = notch(high, f_l, 0.28, amount)
    r = notch(high, f_r, 0.28, amount)
    return (low + np.stack([l[:, 0], r[:, 1]], 1)).astype(np.float32)


def snoise(n, rs):
    """Two independent noise streams: genuinely wide and genuinely mono-safe."""
    return np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)


def bus_reverb(buf, decay=2.0, wet=0.2, tone=4200, block_bars=24):
    """Reverb across a bus in blocks, so a five-minute buffer never asks for
    a five-minute FFT."""
    n = len(buf)
    out = np.array(buf, dtype=np.float32, copy=True)
    ir = _reverb_ir(decay, tone)
    step_n = max(int(block_bars * BAR), 1)
    for a in range(0, n, step_n):
        seg = buf[a:a + step_n]
        if np.abs(seg).max() < 1e-5:
            continue
        for c in range(2):
            y = fftconvolve(seg[:, c], ir[:, c])
            e = min(a + len(y), n)
            out[a:e, c] += (wet * y[:e - a]).astype(np.float32)
    return out


# ============================================================ the kit
@cached
def mkick(dur_steps=3.0, tune=57.0, gain=1.0, click=1.0, knock=1.0,
          decay=0.075, drive=3.4, seed=0):
    """A kick in three parts, because it has three jobs.

    The **thump** is a sine diving from 3.2x the tune to the tune in 14 ms
    and gone in 75 - that is the part you hear as an event, and it has to be
    over before the bass note it announces has finished its first sixteenth.
    The **weight** is a second clean sine at the tune, lowpassed under 95 Hz,
    holding for 130 ms; you do not hear it as length, you feel it, and it is
    where the 60-120 Hz density the reference records carry actually comes
    from. The **knock** at 3.2x the tune plus the beater click is everything
    above 200 Hz, and it is what survives a phone.

    Saturation is applied to the knock and the click only. Distorting the
    thump generates intermodulation with the sub underneath it and makes the
    low end measurably smaller.
    """
    n, t = steps(dur_steps, floor=int(0.22 * SR))
    rs = np.random.RandomState(seed)
    f = tune * (1 + 2.2 * np.exp(-t / 0.014))
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    weight = np.sin(2 * np.pi * tune * t) * np.exp(-t / 0.130) * 0.85
    kn = (np.sin(2 * np.pi * tune * 3.15 * t) * np.exp(-t / 0.028) * 0.55
          + np.sin(2 * np.pi * tune * 5.4 * t) * np.exp(-t / 0.013) * 0.30) * knock
    tick = rs.randn(n) * np.exp(-t / 0.0022)
    tick += np.sin(2 * np.pi * 3050 * t) * np.exp(-t / 0.0035) * 0.7
    tick += np.sin(2 * np.pi * 1180 * t) * np.exp(-t / 0.0085) * 0.5
    top = hp(stereo(tick), 900, 2) * 1.35 * click + stereo(kn)
    top = np.tanh(drive * top) / np.tanh(drive)
    top = top + 0.7 * bandpass(top, 2200, 5600, 2) + 0.4 * bandpass(top, 320, 780, 2)
    low = lp(stereo(weight), 95, 4) + stereo(thump)
    out = low * 1.0 + top * 0.62
    out = softclip(hp(out, 30, 2), 0.98, 0.7)
    return (out * adsr(n, a=0.0004, r=0.012)[:, None]).astype(np.float32) * gain * 0.95


@cached
def msnare(dur_steps=5.0, tune=192.0, gain=1.0, snap=1.0, body=1.0,
           wires=1.0, room=0.5, decay=0.115, seed=0):
    """A snare drum, modelled rather than sampled from a memory of one.

    A circular membrane's modes are not harmonic: 1, 1.594, 2.136, 2.296,
    2.653. Stacking those five and damping the high ones faster is what makes
    the shell read as a drum instead of as a tuned beep - and the difference
    between this and a filtered noise burst is that the pitch is audible and
    tuneable, which matters when the snare has to sit in the key.

    The wires start 2.2 ms LATE. The head moves first and drags the snares
    into it, and that gap is most of what "snare" means; a noise layer
    aligned to the transient sounds like a clap.

    The room is a gated ambience, cut at 90 ms. In this genre the snare is
    the second-loudest thing on the record and the only one allowed to be
    wide - so it is also the only one with a tail.
    """
    n, t = steps(dur_steps, floor=int(0.35 * SR))
    rs = np.random.RandomState(seed)
    modes = [(1.000, 1.00, 0.090), (1.594, 0.62, 0.058), (2.136, 0.44, 0.040),
             (2.296, 0.31, 0.034), (2.653, 0.24, 0.026)]
    shell = np.zeros(n)
    for r, a, tau in modes:
        ph = rs.rand() * 2 * np.pi
        shell += a * np.sin(2 * np.pi * tune * r * t + ph) * np.exp(-t / tau)
    shell *= body

    lag = int(0.0022 * SR)
    w = snoise(n, rs)
    wenv = np.zeros(n)
    wenv[lag:] = np.exp(-np.arange(n - lag) / SR / decay)
    wenv *= (1 - 0.55 * np.exp(-t / 0.004))                 # the drag-in
    wire = bandpass(w, 1500, 8600, 2) * wenv[:, None] * wires
    wire += bandpass(w, 340, 1200, 2) * (wenv * 0.5)[:, None]

    crack = snoise(n, rs) * np.exp(-t / 0.0016)[:, None]
    crack = hp(crack, 2600, 2) * 1.30 * snap

    dry = stereo(shell) * 0.9 + wire * 1.15 + crack
    dry = np.tanh(2.1 * dry) / np.tanh(2.1)
    dry = dry + 0.65 * bandpass(dry, 180, 340, 2) + 0.55 * bandpass(dry, 1800, 4200, 2)

    if room:
        amb = reverb(dry, decay=1.1, wet=1.0, tone=5200, predelay=0.006)[:n]
        g = np.ones(n)
        k = int(0.090 * SR)
        if n > k:
            g[k:] = np.exp(-np.arange(n - k) / SR / 0.010)   # the gate
        dry = dry + amb * (g * room)[:, None]
    out = hp(dry, 150, 2) * adsr(n, a=0.0003, r=0.02)[:, None]
    return norm(out, 0.95).astype(np.float32) * gain


@cached
def mghost(dur_steps=1.0, gain=1.0, tune=210.0, seed=0):
    """The quiet hits between the backbeats. A drummer's ghost notes are not
    a quieter snare - the stick barely leaves the head, so there is almost no
    shell and almost all wires."""
    return msnare(dur_steps, tune=tune, gain=gain * 0.34, snap=0.35, body=0.25,
                  wires=1.0, room=0.0, decay=0.045, seed=seed + 71)


@cached
def mhat(dur_steps=0.7, open_=False, gain=1.0, tone=1.0, seed=0):
    """Six square waves at inharmonic ratios through a highpass - the 808's
    method, because a noise burst has no pitch and a hi-hat does. The ratios
    are jittered per seed, so no two hits in a bar are the same cymbal."""
    n, t = steps(dur_steps, floor=200)
    rs = np.random.RandomState(seed)
    base = 318.0 * tone * (1 + 0.03 * rs.randn())
    rat = np.array([1.0, 1.342, 1.615, 1.995, 2.445, 2.796]) * (1 + 0.02 * rs.randn(6))
    x = np.zeros(n)
    for r in rat:
        x += np.sign(np.sin(2 * np.pi * base * r * t + rs.rand() * 6.28))
    tau = 0.20 if open_ else 0.024 + 0.012 * rs.rand()
    x *= np.exp(-t / tau) / 6
    y = hp(stereo(x) + snoise(n, rs) * np.exp(-t / (tau * 0.7))[:, None] * 0.22,
           5600, 2)
    y = y + 0.5 * bandpass(y, 9000, 13000, 2)
    return (norm(y, 0.9) * adsr(n, a=0.0002, r=0.006)[:, None]).astype(np.float32) * gain


@cached
def mride(dur_steps=2.0, gain=1.0, tone=1.0, seed=0):
    """A ride with an audible ping - the strike partial an octave and a fifth
    over the wash. Rides carry continuous energy without the hiss of hats,
    which is how a 174 BPM track keeps its subdivision legible under a bass
    that is using all the mids."""
    n, t = steps(dur_steps, floor=int(0.3 * SR))
    rs = np.random.RandomState(seed)
    base = 470.0 * tone
    x = np.zeros(n)
    for r in [1.0, 1.51, 2.31, 3.07, 4.13, 5.44, 6.9]:
        x += np.sin(2 * np.pi * base * r * (1 + 0.01 * rs.randn()) * t
                    + rs.rand() * 6.28) * np.exp(-t / (0.34 / r ** 0.75))
    ping = np.sin(2 * np.pi * base * 3.02 * t) * np.exp(-t / 0.055) * 1.6
    y = bandpass(stereo(x / 7 + ping * 0.42), 2400, 12000, 2)
    # Eight of these a bar was two thirds of the record's entire top end. A
    # ride is a struck object with a ping and a short wash, not a cymbal
    # sustaining under the whole groove - the noise layer is a tenth of what
    # it was and dies in 60 ms.
    y += bandpass(snoise(n, rs), 5000, 13000, 2) * np.exp(-t / 0.060)[:, None] * 0.11
    return (norm(y, 0.85) * adsr(n, a=0.0004, r=0.02)[:, None]).astype(np.float32) * gain


@cached
def mclank(freq=740.0, dur_steps=3.0, gain=1.0, bright=1.0, seed=0, damp=1.0,
           note=None):
    """Struck metal. Partials at 1, 2.76, 5.40, 8.93, 13.34 - a bar, not a
    string - each with its own decay, the high ones dying first because that
    is what happens when you hit something.

    This is the percussion layer that makes machine funk sound like machinery
    rather than like a drum kit: an object with a pitch, no attack envelope
    of its own, and a decay that is not exponential in the ear because five
    partials fading at five rates never is.

    Pass `note` rather than `freq`. The partials are inharmonic but the
    fundamental is not free: a struck object at 980 Hz over an F minor track
    is a wrong note that happens to be made of metal.
    """
    if note is not None:
        freq = midi(note)
    n, t = steps(dur_steps, floor=int(0.25 * SR))
    rs = np.random.RandomState(seed)
    x = np.zeros(n)
    for i, r in enumerate([1.0, 2.76, 5.40, 8.93, 13.34, 18.6]):
        f = freq * r * (1 + 0.004 * rs.randn())
        tau = (0.42 / (1 + 0.9 * i)) / damp
        x += np.sin(2 * np.pi * f * t + rs.rand() * 6.28) * np.exp(-t / tau) / (1 + 0.7 * i)
    strike = rs.randn(n) * np.exp(-t / 0.0016) * 0.5
    y = stereo(x) + hp(stereo(strike), 2000, 2) * bright
    y = np.tanh(1.9 * y)
    return (norm(y, 0.9) * adsr(n, a=0.0003, r=0.02)[:, None]).astype(np.float32) * gain


@cached
def mtok(dur_steps=0.8, freq=1420.0, gain=1.0, seed=0, note=None):
    """Wood. One damped mode plus a click; the thing that fills a sixteenth
    without adding either weight or hiss."""
    if note is not None:
        freq = midi(note)
    n, t = steps(dur_steps, floor=200)
    rs = np.random.RandomState(seed)
    x = (np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.011)
         + np.sin(2 * np.pi * freq * 2.4 * t) * np.exp(-t / 0.005) * 0.5)
    y = stereo(x) + hp(stereo(rs.randn(n) * np.exp(-t / 0.0012)), 1800, 2) * 0.5
    return (norm(bandpass(y, 500, 8000, 2), 0.8)
            * adsr(n, a=0.0002, r=0.006)[:, None]).astype(np.float32) * gain


@cached
def mshake(dur_steps=1.0, gain=1.0, seed=0):
    """Filtered noise with a fast rise and a fast fall - the layer that turns
    a grid of hits into a groove without occupying a band anything else wants."""
    n, t = steps(dur_steps, floor=200)
    rs = np.random.RandomState(seed)
    env = np.exp(-t / 0.020) * (1 - np.exp(-t / 0.0025))
    y = bandpass(snoise(n, rs), 4200, 11000, 2) * env[:, None]
    return (norm(y, 0.7) * adsr(n, a=0.0006, r=0.008)[:, None]).astype(np.float32) * gain


def roll(s, b, st, count, spacing=0.5, bus='drums', gain=0.8, accel=False,
         voice=None, seed=0, **kw):
    """A retrigger. `accel` halves the spacing across the roll, which is what
    a snare roll into a drop actually does and what a fixed 32nd grid does
    not."""
    voice = voice or mghost
    pos, sp = st, spacing
    for i in range(count):
        g = gain * (0.55 + 0.45 * (i + 1) / count)
        s.place(s.pos(b, pos), voice(seed=seed + i, **kw), g, bus)
        pos += sp
        if accel:
            sp *= 0.86


# ============================================================ the bass
from scipy.signal import butter, resample_poly, sosfiltfilt as _sff


def _down(x, os_):
    """Decimate the oversampled oscillator stage. Hard sync and wavefolding
    generate partials far above Nyquist; generated at 4x and lowpassed here,
    they fold back at -60 dB instead of landing in the middle of the note as
    inharmonic whistles."""
    if os_ == 1:
        return x
    sos = butter(8, 17500, 'low', fs=SR * os_, output='sos')
    return _sff(sos, x, axis=0)[::os_].astype(np.float32)


def _pd(p, warp):
    """Phase distortion. Read the first `warp` of the cycle fast and the rest
    slow and a sine becomes a saw - Casio's answer to a patent, and the only
    way to sweep from a pure tone to a bright one without a filter and
    without a discontinuity to alias on. warp=0.5 is a sine, warp=0.05 is
    almost a resonant saw."""
    w = np.clip(warp, 0.03, 0.97)
    y = np.where(p < w, p / (2 * w), 0.5 + (p - w) / (2 * (1 - w)))
    return np.sin(2 * np.pi * y)


def sawspread(ph, fmax, voices=5, detune=18.0, seed=0, width=1.0, kmax=120):
    """A detuned saw stack that is stereo by construction.

    Each voice is panned by its own detune offset: the flat voices go left,
    the sharp ones go right, the centre one stays put. Nothing is delayed and
    nothing is phase-inverted, so summed to mono every voice is still there -
    this is the supersaw's own width mechanism and it is the only one that
    survives a club system. A Haas delay or an inverted side channel would
    measure wider and disappear in the room.

    The width is real for a second reason: the beat rate between two voices
    rises with the partial number, so at 18 cents the fundamental throbs at
    0.9 Hz in the centre while the 30th partial shimmers at 27 Hz across the
    whole field. The bottom stays solid and the top moves.
    """
    rs = np.random.RandomState(seed)
    offs = np.linspace(-1, 1, voices) if voices > 1 else np.zeros(1)
    out = np.zeros((len(ph), 2))
    for o in offs:
        r = 2.0 ** (o * detune / 1200.0)
        v = saw_ph(ph * r + rs.rand() * 2 * np.pi, fmax * r, kmax=kmax)
        ang = (o * width + 1) * np.pi / 4
        out[:, 0] += v * np.cos(ang) * 1.41
        out[:, 1] += v * np.sin(ang) * 1.41
    return (out / voices).astype(np.float32)


def _shape(x, dl, os_=2):
    """The pre-filter drive, oversampled. tanh on a saw generates harmonics
    above Nyquist that fold back into the passband, and the filter after it
    cannot remove what has already landed at 4 kHz."""
    n = len(x)
    y = resample_poly(x, os_, 1, axis=0)
    d = np.interp(np.linspace(0, n - 1, len(y)), np.arange(n), dl)[:, None]
    y = np.tanh(d * y) / np.tanh(d)
    return resample_poly(y, 1, os_, axis=0)[:n].astype(np.float32)


def bassbar(notes, dur_steps=16, gain=1.0, cut=1200, q=2.6, drive=2.4,
            wide=1.0, warp=0.5, sync=1.0, fm=0.0, fmr=2.0,
            mix=(1.0, 0.20, 0.85, 0.70), voices=5, detune=18.0, top=0.30,
            vowel=None, nk=None, nkq=2.2, gatep=None, decay=0.0,
            drives=(0.0, 1.7, 3.2, 1.9), rs=1.0, rsmix=0.32, sat=1.15,
            hpf=95, glide=0.022, spr=0.45, width=1.0, smooth=0.016, os_=4,
            seed=0):
    """One bar of mid bass as ONE oscillator, with a parameter timeline.

    **The core is three detuned saw stacks at once**, at 45%, 100% and 220%
    of `detune`, crossfaded by the `wide` lane - so the bass changes not only
    its filter but the *width and thickness of its own oscillator* from step
    to step. A narrow stack is a single hard tone; the same notes on the wide
    stack are a chorus of them. Moving between the two per sixteenth is a
    kind of motion a filter cannot produce, and it is what stops a reese
    sounding like one preset held down for four minutes.

    On top of those sits a saw an octave up at `top`, which is where a bass
    gets its presence on a small speaker, and a phase-distortion oscillator
    at `mix[1]` for body. Hard sync and phase modulation are mixed in BY
    THEIR OWN LANES: a step whose sync ratio is 1.0 hears none of the sync
    oscillator at all. Reaching for them as the *body* of the sound produces
    a record scratch, not a bass line - a timbre rebuilt from scratch every
    sixteenth has no continuous tone left to modulate.

    Every argument that names a sound takes either a number or a list of
    numbers, one per step, smoothed over `smooth` seconds - at 16 ms a step
    change is a fast glide, which is a filter being played rather than a
    sample being chopped.

    The rack, in order: oversampled drive, highpass off the sub, moving
    notches or moving formants, the resonant filter, multiband distortion,
    one resampling pass, and the filter again.
    """
    n = int(dur_steps * STEP)
    m = n * os_
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fmax = float(f.max())

    # Only synthesise the partials the filter will let through. At a maximum
    # cutoff of 4.6 kHz on an 87 Hz note that is 116 of them, not 190, and
    # the stack is the expensive part of the whole module.
    cmax = float(np.max(cut)) if np.ndim(cut) else float(cut)
    kmax = int(np.clip(2.4 * cmax / max(fmax, 30.0), 24, 190))

    wl = np.clip(steplane(wide, n, 'hold', smooth), 0, 2)[:, None]
    x = np.zeros((n, 2), dtype=np.float32)
    for i, (d, c) in enumerate(((0.45, 0), (1.0, 1), (2.2, 2))):
        w = np.clip(1 - np.abs(wl - c), 0, 1)
        if w.max() < 1e-3:
            continue
        x += w * sawspread(ph, fmax, voices, detune * d, seed + 17 * i,
                           width * (0.55 + 0.35 * c), kmax) * mix[0]
    if top:
        x += top * sawspread(ph * 2, fmax * 2, 3, detune * 0.6, seed + 91,
                             width * 0.8, max(kmax // 2, 16))
    if mix[1]:
        x += mix[1] * _pd((ph / (2 * np.pi)) % 1.0,
                          steplane(warp, n, 'hold', smooth))[:, None]
    sl = steplane(sync, n, 'hold', smooth)
    il = steplane(fm, n, 'hold', smooth)
    if mix[2] and sl.max() > 1.02:
        ph4 = 2 * np.pi * np.cumsum(np.repeat(f, os_)) / (SR * os_)
        p4 = (ph4 / (2 * np.pi)) % 1.0
        s4 = np.interp(np.linspace(0, n - 1, m), np.arange(n), sl)
        tear = _down(2 * ((p4 * s4) % 1.0) - 1, os_)[:n]
        x += (mix[2] * np.clip((sl - 1.0) / 2.4, 0, 1) * tear)[:, None]
    if mix[3] and il.max() > 0.02:
        x += (mix[3] * np.clip(il / 3.0, 0, 1)
              * np.sin(ph + il * np.sin(fmr * ph)))[:, None]

    y = hp(_shape(x, steplane(drive, n, 'hold', smooth)), hpf, 2)

    if nk is not None:
        y = notchbank(y, steplane(nk, n, 'exp', max(smooth, 0.008)), q=nkq)
    if vowel is not None:
        y = (0.45 * y + 0.90 * formants(y, vowel)).astype(np.float32)

    cl = steplane(cut, n, 'exp', smooth)
    ql = steplane(q, n, 'hold', smooth)
    y = svf(y, cl, ql, 'lp', sat=sat)
    y = mbdrive(y, drives)

    if rs != 1.0:
        pre = lp(y, 12000, 4) if rs > 1 else y
        y = ((1 - rsmix) * y + rsmix * resample(pre, rs)).astype(np.float32)
        y = svf(y, np.minimum(cl * 1.4, 15000), np.maximum(ql * 0.7, 0.8), 'lp',
                sat=sat * 0.7)

    y = y * _amp(notes, n, decay, 0.004, 0.0)[:, None]
    if gatep is not None:
        y = gate(y, gatep, smooth=0.010)
    y = lp(spread(y, 380, amount=spr), 16500, 4)
    y = softclip(hp(y, hpf, 2), 0.95, 0.72)
    return (y * adsr(n, a=0.003, r=0.006)[:, None]).astype(np.float32) * gain


def screech(note, dur_steps=4, gain=1.0, r0=2.0, r1=9.0, cut=(2200, 9000),
            q=6.0, drive=4.0, seed=0):
    """The upward tear. Hard sync with the ratio climbing from `r0` to `r1`
    across the note while the pitch stands still, through a resonant filter
    opening at the same time. Two brightnesses moving together read as one
    gesture; either alone reads as a preset."""
    n = int(dur_steps * STEP)
    m = n * 4
    t = np.arange(m) / (SR * 4)
    ph = 2 * np.pi * midi(note) * t
    p = (ph / (2 * np.pi)) % 1.0
    u = np.linspace(0, 1, m) ** 1.4
    ratio = r0 + (r1 - r0) * u
    x = 0.7 * (2 * ((p * ratio) % 1.0) - 1) + 0.4 * _pd(p, 0.5 - 0.4 * u)
    y = stereo(_down(x, 4))
    cl = np.geomspace(cut[0], cut[1], n)
    y = svf(y, cl, q, 'lp', sat=drive * 0.4)
    y = np.tanh(drive * y) / np.tanh(drive)
    y = hp(bandpass(y, 300, 13000, 2), 260, 2)
    env = np.exp(-np.arange(n) / SR / (dur_steps * STEP / SR * 0.8))
    return (spread(y, 500, amount=0.5) * (env * adsr(n, 0.003, 0.02))[:, None]
            ).astype(np.float32) * gain * 0.7


def revfx(seg, tail=0.0, cut=(300, 9000), q=1.4):
    """A riser made out of the material it leads into, not out of noise. Take
    the bar the drop starts with, reverse it and open a filter across it: the
    build then predicts the drop instead of merely announcing one."""
    y = rev(np.asarray(seg, dtype=np.float32))
    n = len(y)
    y = svf(y, np.geomspace(cut[0], cut[1], n), q, 'lp')
    env = np.linspace(0.05, 1.0, n) ** 1.6
    return (y * env[:, None]).astype(np.float32)


# ============================================================ music and air
def mstab(notes, dur_steps=2.0, gain=1.0, cut=(5200, 700), q=3.4, warp=0.18,
          drive=3.2, decay=0.10, spr=0.6, seed=0):
    """A chord as one gesture. Every voice shares one filter and one drive
    stage, so the chord distorts as a chord - three separately saturated
    notes are three sounds that happen to be in tune, and the intermodulation
    between them is exactly the glue that makes a stab read as one hit."""
    n = int(dur_steps * STEP)
    m = n * 2
    t = np.arange(m) / (SR * 2)
    rs = np.random.RandomState(seed)
    x = np.zeros(m)
    for i, nt in enumerate(notes):
        for d in (-1, 1):
            f = midi(nt) * (1 + d * 0.004 * (1 + 0.4 * rs.rand()))
            p = (f * t + rs.rand()) % 1.0
            x += _pd(p, warp) * 0.6 + (2 * p - 1) * 0.4
    y = stereo(_down(x / (2 * len(notes)), 2))
    env = np.exp(-np.arange(n) / SR / decay)
    y = svf(y, np.geomspace(cut[0], cut[1], n), q, 'lp', sat=1.6)
    y = np.tanh(drive * y) / np.tanh(drive)
    y = y + 0.5 * bandpass(y, 900, 2600, 2)
    y = hp(spread(y, 420, amount=spr), 190, 2)
    return (y * (env * adsr(n, 0.0015, 0.01))[:, None]).astype(np.float32) * gain * 0.5


def mbell(note, dur_steps=4, gain=1.0, ratio=2.0, idx=(3.4, 0.15), decay=0.55,
          shimmer=0.5, seed=0):
    """An FM bell. At the default ratio of 2 the sidebands land ON the
    harmonic series, so the note has an unambiguous pitch and can carry a
    melody; ratios like 3.47 put them between the harmonics, which is metal
    rather than music and belongs on percussion, not on a tune.

    The index falls across the note - the brightness dies before the amplitude
    does, which is what a struck thing does and what an amplitude envelope
    alone cannot fake."""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    f = midi(note)
    ie = idx[1] + (idx[0] - idx[1]) * np.exp(-t / (decay * 0.22))
    x = np.sin(2 * np.pi * f * t + ie * np.sin(2 * np.pi * f * ratio * t))
    x += 0.35 * np.sin(2 * np.pi * f * 2.01 * t
                       + ie * 0.6 * np.sin(2 * np.pi * f * ratio * 1.5 * t))
    x *= np.exp(-t / decay)
    y = stereo(x)
    if shimmer:
        y = y + shimmer * 0.4 * resample(y, 0.5)                # an octave under
    return (hp(y, 180, 2) * adsr(n, 0.001, 0.03)[:, None]).astype(np.float32) * gain * 0.55


def mlead(notes, dur_steps=8, gain=1.0, cut=4200, q=4.5, sync=(1.0, 2.6),
          warp=0.22, glide=0.014, decay=0.0, drive=2.0, seed=0):
    """The topline, built like the bass and voiced an octave and a half up.
    One continuous oscillator per phrase, so a repeated note re-excites
    rather than restarts, and a hard-sync ratio that steps per note - the
    timbre gets its own rhythm on top of the pitch's."""
    n = int(dur_steps * STEP)
    m = n * 4
    f = _ftrack(notes, n, glide, 4)
    ph = 2 * np.pi * np.cumsum(f) / (SR * 4)
    p = (ph / (2 * np.pi)) % 1.0
    sl = steplane(sync, m, 'hold', 0.004)
    x = (0.45 * _pd(p, warp) + 0.55 * (2 * ((p * sl) % 1.0) - 1)
         + 0.30 * np.sin(ph * 2.002))
    y = stereo(_down(x, 4))
    y = svf(y, steplane(cut, n, 'exp', 0.005), q, 'lp', sat=1.5)
    y = np.tanh(drive * y) / np.tanh(drive)
    y = y * _amp(notes, n, decay, 0.004)[:, None]
    y = hp(spread(y, 600, f_l=1100, f_r=1900, amount=0.5), 220, 2)
    return (y * adsr(n, 0.003, 0.02)[:, None]).astype(np.float32) * gain * 0.5


def mpad(notes, dur_steps=16, gain=1.0, cut=1500, wide=1.0, seed=0, drift=1.0):
    """Eight detuned voices with independent slow pitch drift. The drift is
    the difference between a pad and a chord: nothing holds still, so the
    beating between the voices never settles into a rate the ear can name."""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    rs = np.random.RandomState(seed)
    x = np.zeros((n, 2))
    for nt in notes:
        for v in range(4):
            det = 1 + (0.004 * (v - 1.5) + 0.0016 * rs.randn()) * drift
            dr = 1 + 0.0025 * drift * np.sin(2 * np.pi * (0.06 + 0.05 * rs.rand()) * t
                                             + rs.rand() * 6.28)
            ph = 2 * np.pi * np.cumsum(midi(nt) * det * dr) / SR
            w = _pd((ph / (2 * np.pi)) % 1.0, 0.30)
            pan = np.clip(0.5 + 0.5 * wide * (v - 1.5) / 1.5, 0, 1)
            x[:, 0] += w * (1 - pan)
            x[:, 1] += w * pan
    y = lp(x.astype(np.float32) / max(len(notes), 1) * 0.5, cut, 4)
    y = hp(y, 190, 2)
    env = np.minimum(1.0, t / 0.35) * np.minimum(1.0, (n / SR - t) / 0.35)
    return (y * np.clip(env, 0, 1)[:, None]).astype(np.float32) * gain


def slam(dur_steps=16, gain=1.0, tune=44.0, seed=0):
    """The downbeat impact: a sine that dives, a filtered noise bloom, and a
    reversed tail glued in front of it so the hit starts before it lands."""
    n, t = steps(dur_steps, floor=int(0.6 * SR))
    rs = np.random.RandomState(seed)
    f = tune * (1 + 3.5 * np.exp(-t / 0.030))
    low = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.34)
    nz = bandpass(snoise(n, rs), 120, 3400, 2) * np.exp(-t / 0.19)[:, None]
    y = stereo(low) * 1.0 + nz * 0.55
    y = np.tanh(2.2 * y)
    half = n // 2
    pre = rev(reverb(y[:half], decay=1.4, wet=1.0, tone=3000)[:half]) * 0.5
    y[:len(pre)] += pre
    return (softclip(hp(y, 26, 2), 0.98, 0.7)
            * adsr(n, 0.001, 0.05)[:, None]).astype(np.float32) * gain


def subdive(dur_steps=8, f0=90.0, f1=26.0, gain=1.0, curve=1.7):
    """The sub drop. One sine falling below hearing - the sound of the floor
    being taken away, and the only place in the record where the low end is
    allowed a gesture instead of a note."""
    n, t = steps(dur_steps, floor=int(0.3 * SR))
    u = (t / max(t[-1], 1e-9)) ** curve
    f = f0 * (f1 / f0) ** u
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (n / SR * 0.7))
    return (lp(stereo(np.tanh(1.4 * x)), 160, 4)
            * adsr(n, 0.004, 0.04)[:, None]).astype(np.float32) * gain * 0.9


def air(dur_steps=16, gain=1.0, seed=0, lo=900.0, hi=7000.0, move=0.09):
    """Room tone. Digital silence between events is the loudest tell that a
    record was assembled rather than recorded; this fills it at -55 dB."""
    n, t = steps(dur_steps, floor=1024)
    rs = np.random.RandomState(seed)
    y = bandpass(snoise(n, rs), lo, hi, 2)
    env = 1 + 0.6 * np.sin(2 * np.pi * move * t + rs.rand() * 6.28)
    return (y * env[:, None] * gain * 0.06).astype(np.float32)


# ============================================================ bass tablature
# One character per sixteenth, describing what the FILTER and the DRIVE do to
# a detuned saw - not what oscillator to use. The core stays the same tone all
# the way through the bar; a bass line is a voice being played, and a voice
# that is rebuilt from scratch every sixteenth is a record being scratched.
#
#   .  a hole - the gate almost shut, the saw still running underneath
#   -  silence
# The cutoffs are where two measured reese samples put them, not where a
# synth preset does: 270 Hz for the resting state, 480 for the open reese,
# and only the accent characters go past 1.5 kHz. A neurofunk bass has 92-95%
# of its energy below 400 Hz - what reads as "bright" in one is a resonant
# hump on the fifth harmonic, not a filter in the mids.
#
#   o  round: the filter almost closed. the resting state, and most of a bar
#   O  open
#   w  the reese: notches moving through the detuned partials
#   W  the reese, brighter
#   g  growl: the same, with the filter ringing at Q 4.4
#   G  big growl
#   m  metal: the first character that adds hard sync - an accent
#   S  screech: sync at 3.4 and a little phase modulation. use two a bar
#   x  blast: heavy FM, briefly inharmonic. use one a phrase
#
# Each character also carries a `wide` value, 0 to 2, which crossfades the
# three saw stacks: 0 is one hard tone, 2 is a chorus of them. Stepping from
# `o` to `w` is a transition between two different oscillators, not a filter
# move, and it is the cheapest way to stop a reese sounding like one preset.
#
CHARS = {
    '.': dict(wide=1.0, cut=200,  q=1.6, sync=1.00, warp=0.50, fm=0.0, nk=320,  drive=1.3, gate=0.12),
    '-': dict(wide=0.0, cut=180,  q=1.4, sync=1.00, warp=0.50, fm=0.0, nk=300,  drive=1.2, gate=0.00),
    'o': dict(wide=0.4, cut=270,  q=2.0, sync=1.00, warp=0.50, fm=0.0, nk=380,  drive=1.5, gate=1.00),
    'O': dict(wide=1.0, cut=390,  q=2.6, sync=1.00, warp=0.46, fm=0.0, nk=480,  drive=1.7, gate=1.00),
    'w': dict(wide=2.0, cut=480,  q=3.0, sync=1.00, warp=0.42, fm=0.0, nk=560,  drive=1.8, gate=1.00),
    'W': dict(wide=2.0, cut=720,  q=3.2, sync=1.00, warp=0.38, fm=0.0, nk=800,  drive=2.0, gate=1.00),
    'g': dict(wide=1.2, cut=620,  q=5.0, sync=1.00, warp=0.34, fm=0.0, nk=620,  drive=2.4, gate=1.00),
    'G': dict(wide=1.5, cut=980,  q=6.0, sync=1.00, warp=0.30, fm=0.0, nk=920,  drive=2.8, gate=1.00),
    'm': dict(wide=0.8, cut=1550, q=5.5, sync=2.20, warp=0.22, fm=0.0, nk=1400, drive=3.0, gate=1.00),
    'S': dict(wide=1.6, cut=2700, q=7.0, sync=3.40, warp=0.14, fm=1.4, nk=2100, drive=3.4, gate=1.00),
    'x': dict(wide=1.0, cut=1250, q=3.0, sync=1.00, warp=0.50, fm=3.2, nk=800,  drive=2.6, gate=1.00),
}


def voicing(tab, cut=1.0, q=1.0, sync=1.0, fm=1.0, nk=1.0, gate=1.0, drive=1.0,
            wide=1.0):
    """Expand a tablature into the lanes `bassbar` wants.

    The multipliers are how one riff becomes three: the same tablature with
    `cut=0.55` is the first drop's darker version of the third drop's, and
    the two are recognisably the same line rather than two different ones.
    """
    ch = [CHARS[c] for c in tab if c in CHARS]
    return dict(wide=[min(2.0, c['wide'] * wide) for c in ch],
                cut=[c['cut'] * cut for c in ch],
                q=[c['q'] * q for c in ch],
                sync=[1 + (c['sync'] - 1) * sync for c in ch],
                warp=[c['warp'] for c in ch],
                fm=[c['fm'] * fm for c in ch],
                nk=[c['nk'] * nk for c in ch],
                drive=[c['drive'] * drive for c in ch],
                gatep=[min(1.0, c['gate'] * gate) for c in ch])


_BARS = {}


def bassbar_c(notes, tab, dur_steps=16, **kw):
    """`bassbar` with a cache keyed on everything that reaches it. A two-bar
    riff repeated sixteen times costs two bars of synthesis."""
    key = (notes, tab, dur_steps, tuple(sorted((k, str(v)) for k, v in kw.items())))
    if key not in _BARS:
        v = voicing(tab, **{k: kw.pop(k) for k in list(kw)
                            if k in ('cut', 'q', 'sync', 'fm', 'nk', 'gate',
                                     'drive', 'wide')})
        v.update(kw)
        _BARS[key] = bassbar(notes, dur_steps, **v)
    return _BARS[key]


def mgloom(notes, dur_steps=16, gain=1.0, cut=(500, 1500), gliss=0.10,
           fifth=0.5, glint=0.07, breath=0.30, vib=4.4, seed=0, width=1.0,
           decay=0.0):
    """The dark voice: bowed metal and a choir that never quite arrives.

    Everything about a bell is wrong for this music. A bell has an instant
    attack, a bright inharmonic front and a decay - it is a small hard object,
    and over a track this heavy it reads as a triangle someone dropped on the
    desk. This is the opposite in every dimension: a slow bowed attack, a
    fifth underneath (organum - the interval Western music used before it had
    thirds, which is most of why it sounds ancient), a filter that opens
    across the phrase instead of closing, and a vibrato that fades IN, the way
    a player leans into a long note rather than starting with it.

    The `glint` layer is where the fantasy is: three inharmonic partials at
    1 : 2.76 : 5.4, twenty decibels down and lowpassed, so there is metal in
    the sound without there being a bell in it.
    """
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    f = _ftrack(notes, n, gliss)
    vamp = np.minimum(1.0, t / 0.9) * 0.006                # the vibrato arrives
    ph = 2 * np.pi * np.cumsum(f * (1 + vamp * np.sin(2 * np.pi * vib * t))) / SR
    fmax = float(f.max())

    y = sawspread(ph, fmax, 6, 12.0, seed, width, kmax=90)
    if fifth:
        y = y + fifth * sawspread(ph * 0.6674, fmax * 0.6674, 4, 9.0,
                                  seed + 5, width * 0.7, kmax=70)
    if glint:
        g = sum(np.sin(ph * r + i) / (1 + 2 * i)
                for i, r in enumerate((1.0, 2.76, 5.40)))
        y = y + glint * lp(stereo(g), 3200, 4)
    if breath:
        rs_ = np.random.RandomState(seed + 3)
        y = y + breath * bandpass(snoise(n, rs_), 700, 5200, 2) * 0.35

    env = _amp(notes, n, decay, 0.10, 0.0)
    swell = np.minimum(1.0, t / 0.55) * np.minimum(1.0, (n / SR - t) / 0.7)
    y = svf(y, np.geomspace(cut[0], cut[1], n), 1.6, 'lp', block=256)
    y = hp(y, 130, 2) * (env * np.clip(swell, 0, 1))[:, None]
    return (np.tanh(1.3 * y) * adsr(n, 0.03, 0.12)[:, None]).astype(np.float32) * gain * 0.5


def reese(notes, dur_steps=16, gain=1.0, detune=45.0, voices=3, cut=470, q=3.0,
          nk=560, nkq=1.8, ndepth=0.5, drive=1.6, wide=1.0, width=0.62, sub=0.0,
          top=4200, tilt=0.32, gatep=None, decay=0.0, glide=0.030, smooth=0.020,
          seed=0, spr=0.30):
    """The reese, built from two measured samples rather than from memory.

    A witch-house / neurofunk reese analysed partial by partial says three
    things, and all three are the opposite of what a bright synth bass does:

    - **It is dark.** 92-95% of its energy is below 400 Hz and there is
      essentially nothing above 1.5 kHz. The resonant lowpass sits around
      300-500 Hz, which is between the fifth and the tenth partial of a
      49 Hz note - so what you hear as "the tone" is a resonant hump at the
      third to sixth harmonic, not a filter sweep in the mids.
    - **The detune is enormous.** The beat rate per partial says 32 cents in
      one sample and 55 in the other, against the 10-15 cents a supersaw
      uses. That is why it moves so slowly and so deeply: at 49 Hz, 55 cents
      is 1.6 Hz between the fundamentals, one full beat cycle every 620 ms,
      and the modulation depth measures 36-54%.
    - **It is wide in the bass too.** 43-60% side energy below 120 Hz. Here
      that width is kept above `sub`, where a mono sine holds the bottom,
      because a club system will lose anything wide underneath it.

    The notch is what makes it a reese rather than a detuned saw: the second
    sample's partials sit a saw's own 1/k up to the fourth, then dip 4-6 dB
    through the fifth to the fourteenth and come back - one broad gap
    travelling through the harmonics, exactly what a swept notch leaves.
    """
    n = int(dur_steps * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fmax = float(f.max())
    kmax = int(np.clip(3.0 * float(np.max(top)) / max(fmax, 30.0), 24, 200))

    # Three stacks at 0.4x, 1x and 1.8x the detune, crossfaded by the `wide`
    # lane: the oscillator itself narrows and widens from step to step, which
    # is a kind of motion no filter makes.
    wl = np.clip(steplane(wide, n, 'hold', smooth), 0, 2)[:, None]
    raw = np.zeros((n, 2), dtype=np.float32)
    for i, (d, c) in enumerate(((0.40, 0), (1.0, 1), (1.8, 2))):
        w = np.clip(1 - np.abs(wl - c), 0, 1)
        if w.max() < 1e-3:
            continue
        raw += w * sawspread(ph, fmax, voices, detune * d, seed + 23 * i,
                             width * (0.6 + 0.3 * c), kmax)
    y = svf(raw, steplane(cut, n, 'exp', smooth), steplane(q, n, 'hold', smooth),
            'lp', sat=1.25)
    # A 12 dB/oct filter falls twice as fast as the samples do above their
    # resonant hump - they lose about 1 dB per partial, which is 6 dB/oct.
    # Blending the unfiltered stack back in at `tilt` gives that slope
    # without giving up the resonance, which a one-pole filter cannot have.
    if tilt:
        y = (1 - tilt) * y + tilt * lp(raw, top, 2)
    if nk is not None:
        y = notchbank(y, steplane(nk, n, 'exp', max(smooth, 0.010)),
                      spread=(1.0, 2.35, 4.1), q=nkq, depth=ndepth)
    dl = steplane(drive, n, 'hold', smooth)[:, None]
    y = np.tanh(dl * y) / np.tanh(dl)
    y = lp(hp(y, 62, 2), float(np.max(top)), 4)
    if sub:
        x = np.sin(ph) + 0.28 * np.sin(2 * ph)
        y = y + sub * lp(stereo(np.tanh(1.2 * x)), 110, 4)

    y = y * _amp(notes, n, decay, 0.006, 0.0)[:, None]
    if gatep is not None:
        y = gate(y, gatep, smooth=0.012)
    y = spread(y, 300, f_l=640, f_r=1120, amount=spr)
    return (softclip(y, 0.96, 0.75)
            * adsr(n, a=0.004, r=0.008)[:, None]).astype(np.float32) * gain * 0.7


_RB = {}


def reese_c(notes, tab, dur_steps=16, **kw):
    """`reese` driven by a tablature, cached. The `bassbar` accent layer takes
    the same tablature, so the two are always articulating the same bar."""
    key = (notes, tab, dur_steps, tuple(sorted((k, str(v)) for k, v in kw.items())))
    if key not in _RB:
        v = voicing(tab, **{k: kw.pop(k) for k in list(kw)
                            if k in ('cut', 'q', 'nk', 'gate', 'drive', 'wide')})
        for k in ('sync', 'warp', 'fm'):
            v.pop(k, None)
        v.update(kw)
        _RB[key] = reese(notes, dur_steps, **v)
    return _RB[key]


# ============================================================ the neuro bass
def drivechain(seg, ws=2.2, sat=1.8, crush=0, fold_=0.0, hp_=100.0, lp_=8000.0,
               tone=(1.0, 1.0, 1.0)):
    """The serial distortion chain, with EQ between every stage.

    Three moderate stages beat one extreme one, and they are not
    interchangeable: waveshaping adds odd harmonics and aggression,
    saturation adds even harmonics and warmth, bit reduction adds inharmonic
    grit and fizz. Waveshaper first means everything after it is working on
    material that is already harmonically rich.

    The EQ between the stages is the part that is usually skipped and is the
    single reason a neuro patch turns to mud: every stage generates low end
    below the note and hash above the useful band, and without a highpass and
    a lowpass between them each stage amplifies the previous stage's rubbish
    rather than its music.
    """
    y = np.asarray(seg, dtype=np.float32)

    def clean(x, g=1.0):
        return (bandpass(x, hp_, lp_, 2) * g).astype(np.float32)

    y = clean(y)
    if ws:                                            # odd harmonics, hard
        y = np.tanh(ws * y) / np.tanh(ws)
        if fold_:
            y = (1 - fold_) * y + fold_ * fold(y, 1.35)
        y = clean(y, tone[0])
    if sat:                                           # even harmonics, warm
        y = (y + 0.32 * y * y - 0.10 * y ** 3)        # asymmetric, tube-ish
        y = np.tanh(sat * y) / np.tanh(sat)
        y = clean(y, tone[1])
    if crush:                                         # digital grit
        y = bitcrush(y, crush, 1)
        y = clean(y, tone[2])
    return y.astype(np.float32)


def repass(seg, pitch=1.0, rev_at=None, rev_len=0.5, grain=0.0, punch=0.0,
           seed=0):
    """One resampling pass: things that can only be done to audio.

    Once a patch is printed it stops being a synth and becomes a sample, and
    a sample can be pitched in sections, reversed in fragments, stretched
    until it grains, and transient-shaped hit by hit. Two or three of these
    passes are what put relationships into a neuro bass that no oscillator
    generated - which is the whole reason the workflow exists.
    """
    y = np.asarray(seg, dtype=np.float32).copy()
    n = len(y)
    if abs(pitch - 1.0) > 1e-6:
        y = resample(y, pitch)
    if rev_at is not None:
        a = int(rev_at * STEP)
        b = min(a + int(rev_len * STEP), n)
        if b - a > 64:
            y[a:b] = rev(y[a:b])
    if grain:
        rs_ = np.random.RandomState(seed)
        g = int(0.011 * SR)
        for a in range(0, n - 2 * g, g):
            if rs_.rand() < grain:
                y[a:a + g] = y[a + g:a + 2 * g] * np.hanning(g)[:, None] \
                    + y[a:a + g] * (1 - np.hanning(g))[:, None]
    if punch:
        env = maximum_filter1d(np.abs(y).max(axis=1), int(0.004 * SR))
        d = np.maximum(np.gradient(env), 0)
        d = d / max(d.max(), 1e-9)
        y = y * (1 + punch * uniform_filter1d(d, int(0.002 * SR)))[:, None]
    return y[:n].astype(np.float32)


def stitch(parts, plan, dur_steps, xfade=0.004):
    """Assemble one bar out of chunks of several finished patches.

    A neuro bass line is not played, it is edited: two or three resampled
    patches cut against each other at the half-bar, so bar 3 is a different
    instrument from bar 1 while the riff stays the same. `plan` is a list of
    (start_step, length_steps, which_part).
    """
    n = int(dur_steps * STEP)
    out = np.zeros((n, 2), dtype=np.float32)
    k = max(int(xfade * SR), 8)
    for st, ln, w in plan:
        a = min(int(st * STEP), n)
        b = min(a + int(ln * STEP), n)
        if b - a < 2 * k:
            continue
        seg = parts[w][a:b].copy()
        seg[:k] *= np.linspace(0, 1, k)[:, None]
        seg[-k:] *= np.linspace(1, 0, k)[:, None]
        out[a:b] += seg
    return out


def neurobass(notes, dur_steps=16, gain=1.0, table='growl', pos=6.0,
              detune=14.0, voices=3, width=0.75, cut=2600, q=2.2,
              ws=2.4, sat=1.9, crush=0, fold_=0.0, hp_=78.0, lp_=8000.0,
              vowel=None, vmix=0.55, gatep=None, decay=0.0, glide=0.020,
              passes=((0.5, 0.0), (2.0, 0.0)), grain=0.0, punch=0.5,
              smooth=0.014, spr=0.45, seed=0):
    """A neuro bass, built the way the genre actually builds one.

    The scan is the sound. `pos` is a per-step lane into a spectral wavetable
    and moving it changes the waveform's shape several times a bar - not how
    much of a fixed spectrum a filter is letting through. A patch whose
    position never moves is a subtractive patch with extra steps, and it is
    the single most common way this sound is got wrong.

    After the oscillator: a serial waveshaper / saturator / bit-reducer with
    EQ between every stage, a formant filter driven by THE SAME lane as the
    scan so the vowel and the waveform move together, a resonant filter, and
    two resampling passes with audio-level processing between them.

    `hp_` is at 78 Hz, not at 105. Cutting a bass off above its own
    fundamental leaves it made of harmonics: it reads as a mid-range
    instrument sitting on top of a separate sub rather than as one bass, and
    the thing that is missing is exactly what "deep" means. The sub below it
    is still a clean mono sine and still owns everything under about 70 Hz;
    what changes is that the note's own first and second harmonic are now in
    the same instrument as the growl.
    """
    n = int(dur_steps * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fmax = float(f.max())
    K = int(np.clip(0.45 * SR / max(fmax, 30.0), 24, 160))
    T = wtable(table, K, float(np.median(f)))
    pl = steplane(pos, n, 'hold', smooth) * (T.shape[0] - 1) / 8.0

    # Three voices, detuned, each reading the table a little further along:
    # the scan itself is what is spread across the stereo field, so the sides
    # are not just out of tune with the centre, they are a different waveform.
    y = np.zeros((n, 2), dtype=np.float32)
    offs = np.linspace(-1, 1, voices) if voices > 1 else np.zeros(1)
    for i, o in enumerate(offs):
        r = 2.0 ** (o * detune / 1200.0)
        v = wtscan(ph * r, T, np.clip(pl + o * 1.3, 0, T.shape[0] - 1))
        ang = (o * width + 1) * np.pi / 4
        y[:, 0] += v * np.cos(ang) * 1.41
        y[:, 1] += v * np.sin(ang) * 1.41
    y = (y / voices).astype(np.float32)

    y = drivechain(y, ws=ws, sat=sat, crush=crush, fold_=fold_, hp_=hp_, lp_=lp_)
    if vowel is not None:
        y = ((1 - vmix) * y + vmix * formants(y, vowel, q=6.0, gain=1.2)
             ).astype(np.float32)
    y = svf(y, steplane(cut, n, 'exp', smooth), steplane(q, n, 'hold', smooth),
            'lp', sat=1.2)

    for i, (pitch, revat) in enumerate(passes or ()):
        wet = repass(y, pitch=pitch, rev_at=revat if revat else None,
                     grain=grain, punch=punch if i == 0 else 0.0, seed=seed + i)
        y = (0.62 * y + 0.48 * wet).astype(np.float32)
        y = bandpass(y, hp_, lp_ * 1.2, 2)

    y = y * _amp(notes, n, decay, 0.004, 0.0)[:, None]
    if gatep is not None:
        y = gate(y, gatep, smooth=0.010)
    y = spread(y, 340, f_l=680, f_r=1240, amount=spr)
    return (softclip(hp(y, hp_, 2), 0.95, 0.72)
            * adsr(n, a=0.003, r=0.006)[:, None]).astype(np.float32) * gain * 0.8


# ============================================================ gestures
# A drum & bass bass line is not a sequence of notes and it is not one wobble
# held for eight bars. It is a handful of GESTURES cut against each other and
# recombined: a long stretched sweep, then two short stabs of a different
# timbre, then three more, then a stutter that accelerates. The note underneath
# barely moves. What changes is the rate at which the timbre is travelling and
# which of the two finished patches is speaking.
#
#   rate  cycles per beat: 0 holds the timbre still, 0.25 is one sweep per
#         bar, 2 an eighth, 4 a sixteenth, 8 a thirty-second, 2.667 a triplet
#   gate  amplitude per step - only the `pau` gestures use it, because that is
#         what makes a stab a stab; everything else stays open, because a
#         gated sustain is an arpeggio
#   pos   the range of the wavetable scan. lo == hi is a fixed timbre being
#         retriggered; lo != hi is the timbre travelling
#
GESTURES = {
    'stretch': dict(rate=[0.25], gate=[1.0], pos=(0.4, 7.6)),
    'swell':   dict(rate=[0.125], gate=[1.0], pos=(0.5, 7.8), curve=1.7),
    'accel':   dict(rate=[0.5, 0.5, 1, 1, 2, 2, 4, 4], gate=[1.0], pos=(0.6, 7.4)),
    'brake':   dict(rate=[4, 4, 2, 2, 1, 1, 0.5, 0.25], gate=[1.0], pos=(7.2, 0.8)),
    'roll8':   dict(rate=[2], gate=[1.0], pos=(1.0, 7.0)),
    'roll16':  dict(rate=[4], gate=[1.0], pos=(1.2, 7.2)),
    'stutter': dict(rate=[8], gate=[1.0], pos=(0.8, 7.6)),
    'trip':    dict(rate=[2.667], gate=[1.0], pos=(1.0, 7.0)),
    'dive':    dict(rate=[1], gate=[1.0], pos=(7.6, 0.4), shape='sawdown'),
    'climb':   dict(rate=[0.5], gate=[1.0], pos=(0.4, 7.8), shape='saw'),
    'pau':     dict(rate=[0], gate=[1, .06, .06, .06], pos=(5.2, 5.2)),
    'pau2':    dict(rate=[0], gate=[1, .06, 1, .06], pos=(3.0, 3.0)),
    'pau3':    dict(rate=[0], gate=[1, .05, 1, .05, 1, .05, .05, .05], pos=(6.4, 6.4)),
    'hold':    dict(rate=[0], gate=[1.0], pos=(2.4, 2.4)),
    'gap':     dict(rate=[0], gate=[0.0], pos=(1.0, 1.0)),
}


def _tile(v, n):
    return (list(v) * (n // len(v) + 1))[:n]


def phrase(cells, dur_steps=32):
    """Turn a list of (gesture, patch, steps) into the lanes and the edit plan.

    The lanes are shared by both patches, so the rhythm is continuous across a
    cut and only the instrument changes; the plan says which patch is heard
    over which steps. Writing a different cell list per two bars is what makes
    a thirty-two bar drop stop being a loop.
    """
    n = int(dur_steps * STEP)
    rates, gate, lo, hi, shp, crv, plan, at = [], [], [], [], [], [], [], 0
    for name, patch, ln in cells:
        g = GESTURES[name]
        rates += _tile(g['rate'], ln)
        gate += _tile(g['gate'], ln)
        lo += [g['pos'][0]] * ln
        hi += [g['pos'][1]] * ln
        shp += [g.get('shape', 'sine')] * ln
        crv += [g.get('curve', 1.0)] * ln
        plan.append((at, ln, patch))
        at += ln
    lo_l = steplane(lo, n, 'hold', 0.030)
    hi_l = steplane(hi, n, 'hold', 0.030)
    # One integrated phase for the whole phrase: a gesture that ends mid-cycle
    # hands the next one its position rather than snapping back to zero.
    pos = scanlane(n, rates, lo_l, hi_l, 'sine',
                   curve=float(np.mean(crv)), smooth=0.004)
    down = scanlane(n, rates, hi_l, lo_l, 'sawdown', smooth=0.004)
    m = steplane([1.0 if x == 'sawdown' else 0.0 for x in shp], n, 'hold', 0.02)
    pos = pos * (1 - m) + down * m
    return dict(pos=pos, gatep=gate, plan=plan, rates=rates, n=n)
