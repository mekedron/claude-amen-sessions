"""The big beat layer: a surf guitar, a spring tank, a voice and a huge kit.

Sets the grid to 152 BPM and builds the things Brighton 1998 was made of - a
twanging guitar loop played too fast, a spoken phrase chopped to pieces, and
drums compressed until they distort.

Four ideas run through it.

**An amplifier is a speaker, not a distortion.** `_amp` normalises before
its gain stage and clips asymmetrically, because a symmetric clipper driven
hard turns a string into a square wave - which is exactly how a chiptune is
made. Then `_cab`: everything the clipping produced above 5 kHz is fizz that
a real cone cannot move, so it never reaches the microphone.

**A spring is not a room.** Its impulse response is not decaying noise, it is
a train of chirps: a transient entering a coiled spring disperses, the high
frequencies arriving before the low ones, so every echo is a falling
whistle. That "boing" is the entire sound of surf guitar and no ordinary
reverb makes it.

**The record is an instrument.** `scratch()` reads any segment through a
rate that can slow, stop and go negative, which is what a hand on a platter
does; the crossfader gates it.

**Speed is a parameter.** `varispeed()` plays a segment at a rate that
ramps, taking the pitch with it, the way a tape or a turntable does and a
time-stretcher does not. The genre's signature move is a loop winding up to
speed.

Usage:
    from bigbeatlib import *
    s = Session(32, tail=2.0)
    v = say(RIGHT_ABOUT_NOW, fit=8)
    for b in range(8):
        s.pat(b, [(0, bkick()), (4, bsnare()), (10, bkick()), (12, bsnare())],
              bus='drums')
        s.place(s.pos(b), surf((45, 52, 57), 16), 0.4, 'gtr')
    s.place(s.pos(2), v, 0.5, 'vox')
    s.render('bigbeat_test_152.wav', drive=1.1)
"""
import numpy as np
import core
from core import *
from scipy.signal import fftconvolve
from scipy.ndimage import uniform_filter1d

BAR, STEP = core.set_grid(bpm=152)
BPM = core.BPM

SWING = 0.0          # big beat is a sampled break played straight


# =======================================================================
# the voice
# =======================================================================
# A formant synthesiser. It measures well - F1 and F2 land within about 10%
# of the table and /r/ is exact - and it still reads as a machine reciting
# phonemes rather than a person saying words, which is the honest limit of
# three resonances and no articulatory model. Kept because it is a working
# instrument; `track_razgon` does not use it.
# A phoneme is (F1, F2, F3, kind, seconds, level). `kind` decides what the
# source is:
#   v  voiced - the glottis, through all three formants
#   n  nasal - voiced, dark, quiet: the mouth is shut and the sound is
#      coming out of the nose
#   f  unvoiced fricative - noise only, and no F1, because there is no
#      resonating cavity behind the constriction
#   z  voiced fricative - both at once
#   s  unvoiced stop - silence, then a burst
#   b  voiced stop - silence with the vocal folds still going, then a burst
#   _  silence
PHONES = {
    'iy': (270, 2290, 3010, 'v', 0.105, 1.00),
    'ih': (390, 1990, 2550, 'v', 0.075, 0.95),
    'eh': (530, 1840, 2480, 'v', 0.095, 1.00),
    'ae': (660, 1720, 2410, 'v', 0.115, 1.00),
    'aa': (730, 1090, 2440, 'v', 0.115, 1.00),
    'ah': (640, 1190, 2390, 'v', 0.070, 0.88),
    'ao': (570, 840, 2410, 'v', 0.105, 1.00),
    'ow': (450, 800, 2830, 'v', 0.100, 0.95),
    'uh': (440, 1020, 2240, 'v', 0.075, 0.90),
    'uw': (300, 870, 2240, 'v', 0.090, 0.88),
    # /r/ is the one phoneme with an unmistakable acoustic signature: the
    # third formant collapses from 2500 Hz to about 1600. Nothing else does
    # that, and without it "brother" is "buhthuh".
    'er': (490, 1350, 1690, 'v', 0.110, 0.92),
    'r':  (310, 1060, 1380, 'v', 0.055, 0.80),
    'l':  (380, 880, 2575, 'v', 0.060, 0.82),
    'w':  (300, 610, 2150, 'v', 0.050, 0.80),
    'y':  (280, 2200, 3000, 'v', 0.045, 0.78),
    'n':  (250, 1700, 2600, 'n', 0.060, 0.55),
    'm':  (250, 1100, 2300, 'n', 0.060, 0.55),
    'ng': (250, 2000, 2900, 'n', 0.070, 0.52),
    's':  (900, 5600, 7600, 'f', 0.090, 0.75),
    'sh': (900, 2400, 3800, 'f', 0.090, 0.90),
    'f':  (900, 1500, 5000, 'f', 0.070, 0.38),
    'th': (900, 1800, 5500, 'f', 0.060, 0.32),
    'v':  (280, 1300, 2400, 'z', 0.055, 0.45),
    'dh': (280, 1600, 2600, 'z', 0.045, 0.48),
    'z':  (280, 4800, 6800, 'z', 0.070, 0.60),
    'k':  (900, 1900, 2800, 's', 0.060, 0.70),
    't':  (900, 3800, 5200, 's', 0.050, 0.72),
    'p':  (900, 900,  2200, 's', 0.050, 0.58),
    'b':  (260, 900,  2200, 'b', 0.050, 0.68),
    'd':  (260, 2600, 3000, 'b', 0.050, 0.70),
    'g':  (260, 1700, 2500, 'b', 0.055, 0.66),
    'ch': (900, 2400, 3800, 's', 0.080, 0.85),
    'jh': (280, 2400, 3200, 'b', 0.070, 0.72),
    '-':  (500, 1500, 2500, '_', 0.055, 0.00),
}

# The phrases, written phonetically. A diphthong is two phonemes, because
# that is what a diphthong is: "now" is /n aa uw/ and the glide between the
# two vowels is the whole word.
RIGHT_ABOUT_NOW = ('r', 'aa', 'iy', 't', '-',
                   'ah', 'b', 'aa', 'uw', 't', '-',
                   'n', 'aa', 'uw', '-')
CHECK_IT_OUT    = ('ch', 'eh', 'k', '-', 'ih', 't', '-', 'aa', 'uw', 't', '-')
BIG_BEAT_ROLLIN = ('dh', 'ah', '-', 'b', 'ih', 'g', '-',
                   'b', 'iy', 't', '-', 'r', 'ow', 'l', 'ih', 'ng', '-')
TURN_IT_UP      = ('t', 'er', 'n', '-', 'ih', 't', '-', 'ah', 'p', '-')
ONE_MORE_TIME   = ('w', 'ah', 'n', '-', 'm', 'ao', 'r', '-', 't', 'aa', 'iy', 'm', '-')


def _movebp(seg, ftrack, lo=180.0, hi=6000.0, bands=15, q=0.15):
    """A bandpass whose centre frequency MOVES, as a crossfade across a bank
    of static ones. This is the vocal tract: three of these in parallel, all
    travelling, is the difference between speech and a vowel."""
    n = len(seg)
    fs = np.geomspace(lo, hi, bands)
    u = np.interp(np.log(np.clip(np.asarray(ftrack, dtype=np.float64), lo, hi)),
                  np.log(fs), np.arange(bands, dtype=np.float64))
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(fs):
        w = np.clip(1 - np.abs(u - i), 0, 1)
        if w.max() < 1e-4:
            continue
        out += (bandpass(seg, f * (1 - q), f * (1 + q), order=2) * w[:, None]).astype(np.float32)
    return out


@cached
def say(phones, fit=None, pitch=112.0, fall=0.72, level=1.0, take=0,
        rate=1.0, breath=1.0, grit=0.0, tilt=1.0):
    """Speak a phrase. `phones` is a tuple of keys into PHONES; `fit` scales
    the whole utterance to that many 16th steps.

    The source is a glottal pulse train with a -12 dB/octave tilt - the
    folds, which have no formants of their own - and white noise for
    anything the tongue does to the airstream. Everything that makes it a
    word happens in the three resonances on top, and specifically in how
    they MOVE: a 40 ms glide from one target to the next carries more
    information than either target does.

    `fall` is the declination: a spoken phrase's pitch drops steadily from
    beginning to end, and one that does not sounds like a robot reading."""
    rng = np.random.default_rng(770 + take)
    durs = np.array([PHONES[p][4] for p in phones], dtype=np.float64) * rate
    if fit:
        durs *= (fit * STEP / SR) / durs.sum()
    edge = np.concatenate([[0], np.cumsum(durs)])
    n = max(int(edge[-1] * SR), 64)
    t = np.arange(n) / SR
    idx = np.clip((edge[:-1] * SR).astype(int), 0, n - 1)
    idx = np.concatenate([idx, [n]])

    F = np.zeros((n, 3))
    av = np.zeros(n)          # how open the glottis is
    an = np.zeros(n)          # how much noise the tongue is making
    dark = np.zeros(n)        # nasals: the mouth is shut
    for i, p in enumerate(phones):
        f1, f2, f3, kind, _, lv = PHONES[p]
        a, b = idx[i], idx[i + 1]
        if b <= a:
            continue
        F[a:b] = (f1, f2, f3)
        if kind == 'v':
            av[a:b] = lv
        elif kind == 'n':
            av[a:b] = lv
            dark[a:b] = 1.0
        elif kind == 'f':
            an[a:b] = lv
        elif kind == 'z':
            av[a:b] = lv * 0.55
            an[a:b] = lv * 0.7
        elif kind in ('s', 'b'):
            # a stop is a hole in the sound followed by an explosion. The
            # silence is not a gap in the writing, it IS the consonant.
            k = a + int((b - a) * 0.62)
            if kind == 'b':
                av[a:k] = 0.22                    # the voice bar, through the throat
                dark[a:k] = 1.0
            an[k:b] = lv * 1.6
            av[k:b] = lv * 0.3 if kind == 'b' else 0.0
    # the glides. 35 ms is about how fast a tongue moves, and it is also what
    # turns a row of steady vowels into speech.
    g = max(int(0.035 * SR), 3)
    for j in range(3):
        F[:, j] = uniform_filter1d(F[:, j], g)
    av = uniform_filter1d(av, max(int(0.012 * SR), 3))
    an = uniform_filter1d(an, max(int(0.006 * SR), 3))
    dark = uniform_filter1d(dark, g)

    # intonation: a declining contour with a lift on every voiced onset, and
    # a little jitter, because a perfectly steady pitch is a synthesiser
    f0 = pitch * (fall + (1 - fall) * np.exp(-t / max(edge[-1] * 0.55, 0.05)))
    f0 = f0 * (1 + 0.010 * np.sin(2 * np.pi * 4.6 * t) + 0.006 * rng.standard_normal(n))
    f0 = uniform_filter1d(f0, 400)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    # saw_ph wants the FUNDAMENTAL, not a ceiling - it band-limits itself
    # against Nyquist. Give it a ceiling and it renders three harmonics, and
    # three harmonics is not enough for a formant to have anything to
    # resonate: the vowel disappears and what is left is the noise.
    glot = saw_ph(ph, float(f0.max()))
    glot = lp(stereo(glot), 850 * tilt, order=2)[:, 0] * 3.2      # -12 dB/oct
    noise = rng.standard_normal(n)

    src_v = stereo(glot * av)
    src_n = stereo(noise * an)
    out = (_movebp(src_v, F[:, 0], 180, 1400, bands=11) * 0.85
           + _movebp(src_v, F[:, 1], 500, 3000, bands=13) * 1.05
           + _movebp(src_v, F[:, 2], 1200, 4200, bands=11) * 0.58)
    # a fricative has no cavity behind the constriction, so no F1 - which is
    # why /s/ is all top and /sh/ is not
    out = out + (_movebp(src_n, F[:, 1], 900, 7000, bands=13) * 0.85
                 + _movebp(src_n, F[:, 2], 1800, 9000, bands=11) * 0.55)
    out = out - 0.55 * lp(out, 500) * dark[:, None]              # the shut mouth
    out = hp(out, 90, order=2) + 0.55 * hp(out, 1800, order=2)   # the lips radiate
    out = out + hp(stereo(noise), 4000) * (av * 0.012 * breath)[:, None]
    if grit:
        out = out * (1 - grit) + dirty(out, 3.0 + 6 * grit) * grit
    return norm(out * adsr(n, a=0.004, r=0.02)[:, None], 0.92) * level * 0.8


# =======================================================================
# the spring tank
# =======================================================================
_SPRING = {}


def _spring_ir(decay=2.2, seed=0, taps=0.030, tone=4200.0):
    """A spring's impulse response is a train of falling whistles, not a
    cloud of noise. A transient entering a coiled spring DISPERSES - the high
    frequencies travel faster than the low ones - so what comes out the far
    end is a chirp, and what comes out after that is the same chirp again
    having gone up and back. Model the chirps and you have the boing; model
    it as a small room and you have a small room."""
    key = (round(decay, 2), seed, round(taps, 4), int(tone))
    if key in _SPRING:
        return _SPRING[key]
    n = int(decay * SR)
    rs = np.random.RandomState(1234 + seed)
    ir = np.zeros((n, 2), dtype=np.float64)
    for c in range(2):
        pos = 0.004 + 0.003 * c
        while pos < decay:
            L = int(pos * SR)
            m = min(int(0.05 * SR), n - L)
            if m < 64:
                break
            tt = np.arange(m) / SR
            f = 850 + 3400 * np.exp(-tt / 0.011)          # the dispersion
            ch = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.016)
            ir[L:L + m, c] += ch * np.exp(-pos / (decay * 0.32)) * (1 + 0.25 * rs.randn())
            pos += taps * (1 + 0.22 * rs.rand()) + 0.0015 * c
    out = hp(lp(ir.astype(np.float32), tone), 320)
    out /= np.sqrt((out ** 2).sum(axis=0, keepdims=True)) / 0.42
    _SPRING[key] = out
    return out


def spring(seg, wet=0.5, decay=2.2, seed=0, tone=4200.0, block_bars=8):
    """The tail only - add it to what you already have."""
    ir = _spring_ir(decay, seed, tone=tone)
    out = np.zeros_like(seg)
    blk = int(block_bars * BAR)
    for a in range(0, len(seg), blk):
        part = seg[a:a + blk]
        if np.abs(part).max() < 1e-6:
            continue
        for c in range(2):
            w = wet * fftconvolve(part[:, c], ir[:, c])
            e = min(a + len(w), len(out))
            out[a:e, c] += w[:e - a].astype(np.float32)
    return out


# =======================================================================
# the record as an instrument
# =======================================================================
def varispeed(seg, r0=0.72, r1=1.0, curve=1.0):
    """Play a segment at a rate that ramps. The pitch goes with it, because
    on a turntable and on tape it always did - and the genre's signature
    move is a loop winding up to speed, which a time-stretcher cannot do."""
    n = len(seg)
    m = int(n / max(min(r0, r1), 0.05) * 1.4) + 16
    u = np.linspace(0, 1, m) ** curve
    idx = np.cumsum(r0 + (r1 - r0) * u)
    idx = idx[idx < n - 1]
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], 1)
    return fade_edges(out.astype(np.float32), ms=1.5)


def scratch(seg, moves, gate=None, level=1.0):
    """A hand on the platter. `moves` is ((steps, rate), ...) - rate 1.0 is
    the record playing, 0 is a hand holding it still, negative is pulling it
    backwards. `gate` is the crossfader: a tuple of (steps, open) pairs, and
    cutting the fader while the record moves backwards is what makes the
    difference between a scratch and a rewind."""
    n = len(seg)
    total = int(sum(d for d, _ in moves) * STEP)
    rate = np.zeros(total)
    p = 0
    for d, r in moves:
        m = int(d * STEP)
        rate[p:p + m] = r
        p += m
    rate = uniform_filter1d(rate, max(int(0.004 * SR), 3))       # the wrist
    idx = np.cumsum(rate) + n * 0.12
    idx = np.clip(idx, 0, n - 1)
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], 1)
    if gate is not None:
        g = np.zeros(total)
        p = 0
        for d, o in gate:
            m = int(d * STEP)
            g[p:p + m] = o
            p += m
        out *= uniform_filter1d(g, max(int(0.0015 * SR), 3))[:, None]
    return fade_edges(out.astype(np.float32), ms=2.0) * level


def stutter(seg, times=4, steps_=1.0, decay=0.0, pitch=0.0, offset=0.0):
    """Take the front of a segment and fire it repeatedly, optionally
    climbing in pitch. The oldest edit in sampled music."""
    m = int(steps_ * STEP)
    o = int(offset * STEP)
    piece = fade_edges(seg[o:o + m], ms=1.5)
    out = np.zeros((m * times + len(seg) // 4, 2), dtype=np.float32)
    for i in range(times):
        p = piece if not pitch else pitched(piece, 2 ** (pitch * i / 12))
        e = min(i * m + len(p), len(out))
        out[i * m:e] += p[:e - i * m] * (1.0 - decay * i / max(times, 1))
    return out


# =======================================================================
# the guitar
# =======================================================================
def _cab(x, low=74.0, high=5000.0, thump=0.95, body=0.80, presence=0.65,
         dip=0.28):
    """A 12-inch speaker in a wooden box. This is not a finishing touch: a
    clipped guitar with no cabinet is a buzzsaw, because everything the
    clipping made above 5 kHz is fizz that a real cone physically cannot
    move, and it never reaches the microphone. The cone resonance near
    120 Hz and the dip around 900 Hz are the rest of what makes an amplified
    guitar sound like one."""
    y = hp(x, low, order=3)
    y = lp(y, high, order=6)
    y = y + thump * bandpass(y, 95, 180)          # cone resonance
    y = y + body * bandpass(y, 190, 470)          # the box, and the guitar's own body
    y = y - dip * bandpass(y, 700, 1080)          # the dip every 12" has
    y = y + presence * bandpass(y, 2000, 3400)    # and the peak above it
    return lp(y, 6000, order=4).astype(np.float32)


def _amp(x, gain=1.7, bright=1.0, body=1.0, cab=True):
    """A blackface combo turned up until it is just starting to give.

    The level is normalised BEFORE the gain stage, so `gain` means what it
    says. Without that, a Karplus-Strong burst arrives with peaks well over
    unity and a tanh at 3 squares it - and a squared string with a treble
    boost on it is not a guitar, it is a chiptune. The clipping is also
    asymmetric, because a valve conducts one way: symmetric clipping makes
    only odd harmonics, which is exactly the spectrum of a square wave."""
    st = x if x.ndim == 2 else stereo(x)
    st = st / max(float(np.abs(st).max()), 1e-9)
    y = hp(st, 78, order=2)
    y = y + 0.30 * bright * bandpass(y, 2200, 4200)     # the bright cap
    y = np.where(y >= 0, np.tanh(gain * y), np.tanh(0.74 * gain * y) * 0.87)
    y = (y - y.mean(axis=0)).astype(np.float32)
    y = y + 0.25 * body * bandpass(y, 230, 520)
    return _cab(y) if cab else lp(y, 6000, order=4)


@cached
def surf(notes, dur_steps=4, take=0, level=1.0, decay=1.6, trem=0.0,
         dip=0.0, bright=1.0, pick=0.17, gain=1.7, repick=0.34):
    """The twang. A steel string picked hard right by the bridge, which is a
    comb notch at 1/11 of its length and the reason this sounds like a
    telecaster and not a nylon guitar.

    `trem` is tremolo picking - the same note struck twelve times a second,
    the surf player's whole right hand. The repeats are quiet (`repick`)
    because a plectrum returning to a string that is already ringing
    RE-EXCITES it; strike it again at full force and the note restarts, and
    twelve restarts a second of a bright noise burst is a buzz, not a
    guitar. `dip` is the whammy bar, in semitones, pushed and released."""
    n, t = steps(dur_steps, floor=int(0.12 * SR))
    rng = np.random.default_rng(200 * take + sum(notes))
    x = np.zeros(n)
    strikes = [0.0]
    if trem:
        period = 1.0 / trem
        strikes = list(np.arange(0, dur_steps * STEP / SR, period))
    for k, when in enumerate(strikes):
        a = int(when * SR)
        if a >= n - 64:
            break
        for i, nt in enumerate(notes):
            d = a + int(0.0022 * i * SR)
            if d >= n - 64:
                continue
            x[d:] += ks(midi(nt) * (1 + 0.0018 * (rng.random() - 0.5)), n - d,
                        decay=decay * (1 - 0.06 * i), damp=0.36, pick=pick,
                        hardness=0.55, seed=int(311 * take + 13 * nt + 7 * k)) \
                * (1 - 0.10 * i) * (1.0 if k == 0 else repick * (0.85 + 0.3 * rng.random()))
    y = _amp(x / max(len(notes), 1), gain=gain, bright=bright)
    if dip:
        # the whammy: pushed down over 80 ms and let back up. It is a pitch
        # bend of the whole instrument, so it is done to the audio.
        bend = 1 - (2 ** (-dip / 12) - 1) * -1 * np.minimum(t / 0.08, 1) * np.exp(-t / 0.30)
        pos = np.clip(np.cumsum(bend), 0, n - 1)
        y = np.stack([np.interp(pos, np.arange(n), y[:, c]) for c in range(2)], 1)
    return norm(y.astype(np.float32) * adsr(n, a=0.001, r=0.02)[:, None], 0.9) * level


# =======================================================================
# the kit
# =======================================================================
@cached
def bkick(dur_steps=4, tune=54.0, gain=1.0, click=1.0, decay=0.26, seed=0,
          room=0.5):
    """A 24-inch kick with the front head on, in a room with a microphone
    some distance away. Longer and woodier than a drum machine's, because in
    this genre it came off a record made in 1971."""
    n, t = steps(dur_steps, floor=int(0.3 * SR))
    rng = np.random.default_rng(seed + 3)
    f = tune * (1 + 1.9 * np.exp(-t / 0.017))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    body += 0.40 * np.sin(2 * np.pi * tune * 1.98 * t) * np.exp(-t / 0.07)
    body += 0.18 * np.sin(2 * np.pi * tune * 3.1 * t) * np.exp(-t / 0.030)
    beat = rng.standard_normal(n) * np.exp(-t / 0.0035) * click
    beat += np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.006) * 0.35 * click
    out = stereo(body) + hp(stereo(beat), 1100) * 0.7
    out = out + 0.55 * bandpass(out, 62, 130) + 0.35 * bandpass(out, 240, 520)
    out = np.tanh(1.9 * out)
    if room:
        out = out + room * 0.4 * lp(reverb(out, decay=0.34, wet=0.5, tone=3200)[:n], 2600)
    return norm(hp(out, 32, order=2) * adsr(n, a=0.0006, r=0.02)[:, None], 0.95) * gain


@cached
def bsnare(dur_steps=4, gain=1.0, tune=188.0, snap=1.0, decay=0.14, seed=0,
           room=1.0, crack=1.0):
    """The loudest thing on the record. A wide wooden shell, wires wound
    loose, hit in the middle of the head, in the same room as the kick - and
    then compressed until the room comes up behind it, which is the sound
    this whole genre is built on."""
    n, t = steps(dur_steps, floor=int(0.45 * SR))
    rng = np.random.default_rng(seed + 5)
    pd = 1 + 0.24 * np.exp(-t / 0.009)
    shell = (np.sin(2 * np.pi * tune * pd * t) * np.exp(-t / 0.070)
             + 0.55 * np.sin(2 * np.pi * tune * 1.61 * pd * t) * np.exp(-t / 0.045)
             + 0.30 * np.sin(2 * np.pi * tune * 2.51 * t) * np.exp(-t / 0.028))
    nz = rng.standard_normal(n)
    wires = bandpass(stereo(nz), 1400, 9000) * np.exp(-t / decay)[:, None] * 1.35 * snap
    stick = bandpass(stereo(nz * np.exp(-t / 0.0018)), 1800, 7000) * 0.55 * crack
    dry = np.tanh(1.8 * (stereo(shell * 1.05) + wires + stick))
    if room:
        wet = reverb(dry, decay=0.55, wet=0.85, tone=5200)[:n]
        dry = dry + room * 0.55 * wet.astype(np.float32)
    # the compressor everybody used, doing what everybody used it for
    pk = float(np.abs(dry).max()) or 1.0
    dry = softclip(dry / pk * 2.4, 1.0, knee=0.45) * pk * 0.62
    return norm(hp(dry, 105, order=2) * adsr(n, a=0.0006, r=0.03)[:, None], 0.94) * gain


@cached
def bhat(dur_steps=1, open_=False, gain=1.0, tone=1.0, seed=0):
    n, t = steps(dur_steps, floor=int(0.04 * SR))
    rng = np.random.default_rng(seed + 11)
    ratios = (1.0, 1.36, 1.63, 1.98, 2.42, 2.83)
    x = sum(np.sign(np.sin(2 * np.pi * 810 * r * tone * t)) for r in ratios) / 6
    x = x * 0.9 + rng.standard_normal(n) * 0.95
    out = hp(stereo(x), 3400 if open_ else 4800)
    out = out + 0.45 * bandpass(out, 6000, 11000)
    d = 0.26 if open_ else 0.026
    out = out * (np.exp(-t / d) * adsr(n, a=0.0005, r=0.01))[:, None]
    return norm(out, 0.9) * gain * 0.5


@cached
def btom(dur_steps=2, tune=150.0, gain=1.0, seed=0):
    n, t = steps(dur_steps, floor=int(0.25 * SR))
    rng = np.random.default_rng(seed + 41)
    f = tune * (1 + 0.30 * np.exp(-t / 0.030))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.26)
    x += 0.40 * np.sin(2 * np.pi * tune * 1.55 * t) * np.exp(-t / 0.12)
    head = bandpass(stereo(rng.standard_normal(n) * np.exp(-t / 0.009)), 700, 4200)
    out = np.tanh(1.6 * (stereo(x) + head * 0.5))
    out = out + 0.45 * reverb(out, decay=0.4, wet=0.5, tone=3600)[:n]
    return norm(hp(out, 58, order=2) * adsr(n, a=0.0007, r=0.02)[:, None], 0.93) * gain


@cached
def bcrash(dur_steps=16, gain=1.0, seed=0, size=1.0):
    n, t = steps(dur_steps, floor=int(0.7 * SR))
    rng = np.random.default_rng(seed + 71)
    ratios = (1.0, 1.42, 1.85, 2.29, 2.86, 3.51, 4.3, 5.5, 6.8, 8.4, 10.2)
    x = sum(np.sin(2 * np.pi * 690 * r * t + rng.random() * 6) for r in ratios) / 11
    x = x * 1.15 + rng.standard_normal(n) * 0.85
    out = hp(stereo(x), 1400)
    out = out + 0.45 * bandpass(out, 3500, 9000)
    out = out * (np.exp(-t / (1.25 * size)) * adsr(n, a=0.001, r=0.3))[:, None]
    return norm(widen(out, 1.3), 0.85) * gain * 0.45


def bigroom(buf, decay=0.85, wet=0.22, tone=5200, block_bars=8):
    """One room for the whole kit, convolved in blocks."""
    out = np.zeros_like(buf)
    ir = core._reverb_ir(decay, tone)
    pre = int(0.008 * SR)
    blk = int(block_bars * BAR)
    for a in range(0, len(buf), blk):
        seg = buf[a:a + blk]
        if np.abs(seg).max() < 1e-6:
            continue
        for c in range(2):
            w = wet * fftconvolve(seg[:, c], ir[:, c])
            b = a + pre
            e = min(b + len(w), len(out))
            if b < len(out):
                out[b:e, c] += w[:e - b].astype(np.float32)
    return out


def crush(buf, amount=3.0, out=0.5, knee=0.4):
    """The genre in one function: peak-normalise, drive into a soft knee,
    come back down. Big beat drums are not loud, they are FLAT - the room
    between the hits is pulled up to meet them."""
    pk = float(np.abs(buf).max()) or 1.0
    return (softclip(buf / pk * amount, 1.0, knee=knee) * pk * out).astype(np.float32)


# =======================================================================
# the bass
# =======================================================================
@cached
def fuzzbass(notes, dur_steps=16, level=1.0, glide=0.012, decay=0.55, take=0,
             fuzz=1.0, octave=0.55, cutoff=2600.0):
    """An octave-fuzz pedal on a bass guitar. Rectifying a waveform doubles
    its frequency, so the octave up is not a second oscillator - it is the
    same string folded, which is why it tracks perfectly and sounds broken.

    One bar, one oscillator: the string does not stop between notes."""
    n, t = steps(dur_steps)
    evs = sorted(notes)
    ed = [min(int(st * STEP), n - 1) for st, _ in evs] + [n]
    f = np.empty(n)
    f[:ed[0]] = midi(evs[0][1])
    for i, (_, nt) in enumerate(evs):
        f[ed[i]:ed[i + 1]] = midi(nt)
    f = uniform_filter1d(f, max(int(glide * SR), 3))
    ph = 2 * np.pi * np.cumsum(f) / SR
    amp = np.zeros(n)
    for k in ed[:-1]:
        d = np.exp(-np.arange(n - k) / SR / decay)
        np.maximum(amp[k:], d, out=amp[k:])
    amp = uniform_filter1d(amp, max(int(0.004 * SR), 3))

    low = (np.sin(ph) + 0.35 * np.sin(2 * ph)) * amp
    saw = saw_ph(ph, float(f.max()) * 1.02) * amp
    oct_ = np.abs(np.sin(ph)) * 2 - 1                       # rectified = an octave up
    x = saw + octave * oct_ * amp
    grind = np.tanh((2.0 + 7.0 * fuzz) * stereo(x)) / np.tanh(2.0 + 7.0 * fuzz)
    grind = lp(grind, cutoff, order=4)
    out = lp(stereo(low), 260, order=4) * 1.05 + hp(grind, 110, order=2) * 0.85
    out = out + 0.45 * bandpass(out, 700, 2000)
    out = np.tanh(1.4 * hp(out, 32, order=2))
    return (out * adsr(n, a=0.0015, r=0.005)[:, None]).astype(np.float32) * level * 0.7


# =======================================================================
# the stabs and the noise
# =======================================================================
@cached
def stab(notes, dur_steps=2, level=1.0, take=0, bright=1.0, dirt=1.0):
    """A horn section off a record: bright, short, band-limited by whatever
    it was sampled through, and driven. It is a punctuation mark, not a
    chord."""
    n, t = steps(dur_steps, floor=int(0.08 * SR))
    rng = np.random.default_rng(640 * take + sum(notes))
    x = np.zeros(n)
    for i, nt in enumerate(notes):
        up = 1 - 0.045 * np.exp(-t / 0.026)
        ph = 2 * np.pi * np.cumsum(midi(nt) * (1 + 0.004 * (rng.random() - 0.5)) * up) / SR
        d = int(0.0028 * i * SR)
        seg = 0.6 * saw_ph(ph, midi(nt) * 1.8) + 0.4 * np.sign(np.sin(ph))
        x[d:] += seg[:n - d] * (1 - 0.08 * i)
    st = stereo(x / max(len(notes), 1))
    out = bandpass(st, 320, 5000 * bright, order=2)
    out = out + 1.0 * bandpass(out, 900, 2400)
    out = np.tanh((1.8 + 2.0 * dirt) * out)
    out = out + hp(stereo(rng.standard_normal(n) * np.exp(-t / 0.018)), 2400) * 0.10
    env = np.minimum(t / 0.010, 1.0) * (0.25 + 0.75 * np.exp(-t / (dur_steps * STEP / SR * 0.4)))
    return norm(out * (env * adsr(n, a=0.001, r=0.03))[:, None], 0.9) * level * 0.55


@cached
def siren(dur_steps=8, f0=420.0, f1=1500.0, gain=1.0, rate=0.6, take=0):
    """A rave siren: a square swept between two pitches, through a bandpass."""
    n, t = steps(dur_steps)
    u = 0.5 - 0.5 * np.cos(2 * np.pi * rate * BPM / 60 / 4 * t)
    f = f0 * (f1 / f0) ** u
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.5 + np.sin(ph)
    out = bandpass(stereo(x), 500, 5000, order=2)
    out = np.tanh(2.0 * out)
    return norm(out * adsr(n, a=0.02, r=0.08)[:, None], 0.85) * gain * 0.4


@cached
def sweep(dur_steps=16, gain=1.0, up=True, f0=180.0, f1=9000.0, res=1.4, take=0):
    """Filtered noise climbing or falling: the transition of the decade."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(90 + take)
    u = np.linspace(0, 1, n) ** 1.6
    if not up:
        u = u[::-1]
    nz = stereo(rng.standard_normal(n))
    out = morph_lp(nz, f0, f1, u, bands=9, res=res)
    env = (u if up else np.linspace(0.2, 1.0, n)[::-1]) * adsr(n, a=0.01, r=0.05)
    return norm(widen(out, 1.1) * env[:, None], 0.85) * gain * 0.4
