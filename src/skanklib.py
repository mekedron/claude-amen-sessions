"""The big beat module: a live kit read off a 16-step pattern, a 12-bit
sampler, a compressor you are meant to hear, and a stiff steel string.

Big beat is a rock drummer's kit sampled into a cheap box, chopped, pushed
through a compressor hard enough that the room breathes between the hits, and
put under a fuzz bass and a 303. The distortion is not an effect on top of the
record - it is what the record is made of. Every voice here comes out clean
and is dirtied on purpose, and the one thing that makes it sound like 1998
rather than like a demo is `squash` on the drum bus with the release timed to
a sixteenth.

The floor is four on the floor. That is the one thing taken from techno and it
is deliberate: the funk break carries the swagger, the quarter-note kick
carries the room. A break on its own halves the felt pulse, and at these
tempos that reads as a slow record no matter how busy the hats are.

Two tempos live here. 131 is "Gangster Trippin" territory, where a funk break
still swings; 153 is where the surf guitar and the accelerating chop belong.
`set_tempo()` moves the grid and clears the segment cache, because every
cached voice was measured against the old bar.

Everything general - oscillators, filters, reverb, the compressor, the
sequencer - comes from core. What lives here is only what this genre is made
of, and where core already had something close, this module has its own
anyway: `steel` is not `ks`, because a Karplus-Strong string is perfectly
harmonic and a steel one is not, and that difference is the whole sound of a
guitar.

Usage:
    from skanklib import *
    set_tempo(153)
    s = Session(64, tail=3.0)
    for b in range(8):
        kitbar(s, b, GROOVE, swing=0.56, seed=b)
        s.place(s.pos(b), fuzzbar(RIFF, gain=0.9), 1.0, 'bass')
    s.bus['drums'] = squash(crush(s.bus['drums'], bits=11), 0.26, 6.0,
                            attack=0.014, release=0.1145)
    s.render('skank.wav', clip=1.2, limit=0.9)
"""
import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import uniform_filter1d
import core
from core import *

BAR, STEP = core.set_grid(bpm=131)
BPM = core.BPM


def set_tempo(bpm, beats=4):
    """Move the grid. Clears the segment cache, because every cached voice was
    rendered against the old bar and would come back the wrong length."""
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP


# ---- the sampler ----
def crush(seg, bits=12, sr_div=1, pre=13000.0, hiss=0.0, seed=0):
    """What a 12-bit sampler did to a drum loop.

    Truncating to 12 bits without dither leaves a quantisation error that
    tracks the signal instead of hiding under it, which is why the grit rides
    the hits and vanishes in the gaps. `sr_div` throws away sample rate on top
    of that, and the pre-filter is deliberately set ABOVE half the new rate,
    so a little of the top folds back down as inharmonic garbage. That fold is
    most of the character; filter below sr/2 and you get a clean-sounding
    downsample, which is not what the box did."""
    x = seg
    if sr_div > 1:
        x = lp(x, pre, order=4)
        x = np.repeat(x[::sr_div], sr_div, axis=0)[:len(seg)]
    q = 2.0 ** (bits - 1)
    x = np.trunc(x * q) / q
    if hiss:
        rs = np.random.default_rng(seed + 17)
        x = x + hp(stereo(rs.standard_normal(len(x))), 1200) * hiss * 0.004
    return x.astype(np.float32)


def room(buf, decay=0.62, wet=0.20, tone=5400, predelay=0.007, hp_hz=250.0,
         block_bars=16):
    """The tail ONLY - add it to the bus, do not replace it.

    One room for the whole kit, because one pair of overheads heard all of it.
    Short and bright: a live room with the drums close-mic'd, not a hall.
    Convolved in blocks so a four-minute buffer does not need a four-minute
    FFT.

    The return is high-passed at `hp_hz` and that is not a tone choice. The
    impulse is decorrelated noise in the two channels, so any low end that
    survives into the tail comes back as a SIDE signal - which means a kick
    through an unfiltered room is a kick whose bottom half cancels the moment
    a club system sums the low end."""
    out = np.zeros_like(buf)
    ir = core._reverb_ir(decay, tone)
    pre = int(predelay * SR)
    blk = int(block_bars * BAR)
    for a in range(0, len(buf), blk):
        seg = buf[a:a + blk]
        if np.abs(seg).max() < 1e-6:
            continue
        for c in range(2):
            w = wet * fftconvolve(seg[:, c], ir[:, c])
            b, e = a + pre, min(a + pre + len(w), len(out))
            if b < len(out):
                out[b:e, c] += w[:e - b].astype(np.float32)
    return hp(out, hp_hz, order=2)


# ---- automation ----
def ramp(b, b0, b1, v0, v1, curve=1.0, geom=False):
    """A section-long automation curve, sampled at the two ends of bar `b`.

    Returns (value at the start of the bar, value at the end of it), which is
    exactly the pair a per-bar voice needs to render a move that continues
    across the bar line instead of stepping at it. `geom` interpolates in
    octaves rather than in hertz - the only correct way to sweep a filter."""
    def at(x):
        u = float(np.clip((x - b0) / max(b1 - b0, 1e-9), 0.0, 1.0)) ** curve
        return v0 * (v1 / v0) ** u if geom else v0 + (v1 - v0) * u
    return at(b), at(b + 1)


def sweep_bars(buf, b0, b1, f0, f1, curve=1.0, res=0.0, bands=11):
    """The sixteen-bar filter opening, done to a whole bus in place. In this
    genre that automation is not a transition, it IS the arrangement: the same
    four bars under a cutoff walking from 200 Hz to open is an intro, a build
    and a drop without a single note changing."""
    a, e = int(b0 * BAR), min(int(b1 * BAR), len(buf))
    if e <= a:
        return buf
    env = np.linspace(0, 1, e - a) ** curve
    buf[a:e] = morph_lp(buf[a:e], f0, f1, env, bands=bands, res=res)
    return buf


def gap(s, b, st=14.0, length=2.0, depth=1.0, soft=0.003,
        buses=('drums', 'bass', 'music', 'keys', 'horn', 'vox', 'gtr')):
    """Take the last beat out, across every bus at once.

    The cheapest and most effective device in the arrangement, and the one
    thing a build cannot do without. It works for three reasons: the ear stops
    being masked and meets the drop rested; the prediction the build spent
    sixteen bars establishing is withheld at the moment it is most certain;
    and 0 dB against -10 dB feels enormous whatever the drop measures.
    Applied before the bus effects, so the room and the delay tails still ring
    through the hole - which is what stops it sounding like a dropout.

    Twice per record. A third time and the ear stops falling for it."""
    a, e = s.pos(b, st), s.pos(b, st + length)
    k = max(int(soft * SR), 3)
    for name in buses:
        buf = s.bus.get(name)
        if buf is None or e - a < 2 * k:
            continue
        env = np.full(e - a, 1.0 - depth, dtype=np.float32)
        env[:k] = np.linspace(1.0, 1.0 - depth, k)
        env[-k:] = np.linspace(1.0 - depth, 1.0, k)
        buf[a:e] *= env[:, None]


# ---- the kit ----
# A big beat kick is a 22-inch drum with a blanket in it, mic'd close, tuned
# low and then compressed until the shell rings. It has to hold a quarter-note
# floor without ever sounding like a synthesised club kick, so the pitch dive
# is short and the sustain is a real drum decay, not an 808 tail.
@cached
def bkick(dur_steps=4, tune=54.0, gain=1.0, click=1.0, decay=0.24, thump=1.0,
          seed=0):
    n, t = steps(dur_steps, floor=int(0.25 * SR))
    rng = np.random.default_rng(seed + 3)
    f = tune * (1 + 2.1 * np.exp(-t / 0.013))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    weight = np.sin(2 * np.pi * tune * 0.995 * t) * np.exp(-t / (decay * 1.6)) * 0.45
    knock = np.sin(2 * np.pi * tune * 3.1 * t) * np.exp(-t / 0.042) * 0.60 * thump
    shell = np.sin(2 * np.pi * tune * 5.4 * t) * np.exp(-t / 0.018) * 0.26 * thump
    beater = rng.standard_normal(n) * np.exp(-t / 0.0026)
    beater += np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.0055) * 0.55
    out = stereo(body + weight + knock + shell) + hp(stereo(beater), 1300) * 1.55 * click
    out = np.tanh(1.7 * out)
    # The 60-130 band is what a laptop reproduces of a 54 Hz drum, and the
    # 2-4 kHz beater is what a phone reproduces of it. Both are boosted after
    # the saturation, so the drive does not swallow them.
    out = out + 0.42 * bandpass(out, 60, 130) + 0.85 * bandpass(out, 1900, 4400)
    return norm(hp(out, 30, order=2) * adsr(n, a=0.0004, r=0.02)[:, None], 0.95) * gain


@cached
def bsnare(dur_steps=4, gain=1.0, tune=172.0, snap=1.0, decay=0.155, fat=1.0,
           seed=0):
    """The snare, and in this genre it is the loudest thing on the record.

    Tuned lower than a rock snare and left to ring longer, because it is going
    to be squashed - and a compressor turns a long decay into size and a short
    one into a click. The 180-320 Hz band is boosted last, after the
    saturation, which is where 'fat' lives; take that out and the same drum
    reads as drum & bass."""
    n, t = steps(dur_steps, floor=int(0.22 * SR))
    rng = np.random.default_rng(seed + 5)
    pd = 1 + 0.20 * np.exp(-t / 0.009)
    shell = (np.sin(2 * np.pi * tune * pd * t) * np.exp(-t / 0.075)
             + 0.58 * np.sin(2 * np.pi * tune * 1.58 * pd * t) * np.exp(-t / 0.050)
             + 0.28 * np.sin(2 * np.pi * tune * 2.41 * t) * np.exp(-t / 0.030))
    nz = rng.standard_normal(n)
    wires = bandpass(stereo(nz), 1400, 7600) * np.exp(-t / decay)[:, None] * 1.25 * snap
    stick = bandpass(stereo(nz * np.exp(-t / 0.0020)), 1800, 6800) * 0.60
    out = np.tanh(1.9 * (stereo(shell * 1.1) + wires + stick))
    out = out + 0.30 * bandpass(out, 2100, 4600)
    out = out + 0.34 * fat * bandpass(out, 180, 320)
    return norm(hp(out, 95, order=2) * adsr(n, a=0.0004, r=0.02)[:, None], 0.95) * gain


@cached
def bghost(dur_steps=1.0, gain=1.0, tune=172.0, seed=0):
    """The quiet hits between the backbeats. They are not audible as events
    and the break is dead without them - this is the whole difference between
    a funk drummer and a drum machine."""
    n, t = steps(dur_steps, floor=int(0.05 * SR))
    rng = np.random.default_rng(seed + 7)
    nz = rng.standard_normal(n)
    body = np.sin(2 * np.pi * tune * 1.02 * t) * np.exp(-t / 0.018) * 0.5
    out = bandpass(stereo(nz), 1100, 5200) * np.exp(-t / 0.028)[:, None] + stereo(body)
    return norm(hp(np.tanh(1.4 * out), 200) * adsr(n, a=0.0004, r=0.012)[:, None],
                0.55) * gain


@cached
def bhat(dur_steps=1, open_=False, gain=1.0, tone=1.0, loose=0.0, seed=0):
    """A real hi-hat, half open. `loose` lets the two cymbals rattle against
    each other after the stick - the sizzle a drum machine has never had."""
    n, t = steps(dur_steps, floor=int(0.04 * SR))
    rng = np.random.default_rng(seed + 11)
    ratios = (1.0, 1.34, 1.61, 1.99, 2.44, 2.79)
    x = sum(np.sign(np.sin(2 * np.pi * 820 * r * tone * t)) for r in ratios) / 6
    x = x * 1.05 + rng.standard_normal(n) * 0.75
    d = (0.30 if open_ else 0.028) * (1 + 1.6 * loose)
    out = hp(stereo(x), 3600 if open_ else 4400)
    out = out + 0.55 * bandpass(out, 5200, 9500)
    out = lp(out, 13000, order=2) * (np.exp(-t / d) * adsr(n, a=0.0006, r=0.012))[:, None]
    return norm(out, 0.9) * gain * 0.55


@cached
def bride(dur_steps=2, gain=1.0, bell=0.0, seed=0):
    """Ride: mostly ping. Big beat runs it under the drop where a hat would
    hiss - the same subdivision, five kHz lower, and the mix stops fatiguing."""
    n, t = steps(dur_steps, floor=int(0.1 * SR))
    rng = np.random.default_rng(seed + 13)
    ratios = (1.0, 1.47, 2.09, 2.71, 3.4) if not bell else (1.0, 2.0, 2.97, 4.1)
    base = 900 if not bell else 1160
    x = sum(np.sin(2 * np.pi * base * r * t + rng.random() * 6) for r in ratios) / 5
    x = x * (1.0 if bell else 0.7) + rng.standard_normal(n) * (0.2 if bell else 0.42)
    out = hp(stereo(x), 1500) * (np.exp(-t / (0.55 + 0.7 * bell))
                                 * adsr(n, a=0.0006, r=0.06))[:, None]
    return norm(out, 0.85) * gain * 0.38


@cached
def bcrash(dur_steps=16, gain=1.0, size=1.0, seed=0):
    """18-inch crash. One per eight bars, on the downbeat, and never two."""
    n, t = steps(dur_steps, floor=int(0.6 * SR))
    rng = np.random.default_rng(seed + 21)
    ratios = (1.0, 1.41, 1.83, 2.31, 2.77, 3.42, 4.11, 5.3, 6.7, 8.1)
    x = sum(np.sin(2 * np.pi * 740 * r * t + rng.random() * 6) for r in ratios) / 10
    x = x * 1.2 + rng.standard_normal(n) * 0.8
    out = hp(stereo(x), 1600)
    out = out + 0.45 * bandpass(out, 3800, 9000)
    out = out * (np.exp(-t / (1.25 * size)) * adsr(n, a=0.0008, r=0.25))[:, None]
    out = out + hp(stereo(rng.standard_normal(n) * np.exp(-t / 0.004)), 5000) * 0.5
    return norm(widen(out, 1.1), 0.85) * gain * 0.44


@cached
def btom(dur_steps=2, tune=125.0, gain=1.0, seed=0):
    n, t = steps(dur_steps, floor=int(0.18 * SR))
    rng = np.random.default_rng(seed + 41)
    f = tune * (1 + 0.32 * np.exp(-t / 0.022))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.24)
    x += 0.42 * np.sin(2 * np.pi * tune * 1.52 * t) * np.exp(-t / 0.11)
    head = bandpass(stereo(rng.standard_normal(n) * np.exp(-t / 0.011)), 800, 4800)
    out = np.tanh(1.5 * (stereo(x) + head * 0.5))
    return norm(hp(out, 55) * adsr(n, a=0.0006, r=0.02)[:, None], 0.92) * gain


@cached
def tambo(dur_steps=2, gain=1.0, seed=0, jingles=14):
    """Tambourine. Fourteen pairs of steel discs that do not hit at the same
    instant, which is why one sample looped sounds fake and this does not. On
    the offbeat eighths it is the whole reason a fast record still moves."""
    n, t = steps(dur_steps, floor=int(0.08 * SR))
    rng = np.random.default_rng(seed + 51)
    x = np.zeros(n)
    for _ in range(jingles):
        k = int(rng.uniform(0, 0.0045) * SR)
        m = n - k
        if m < 16:
            continue
        f = rng.uniform(3100, 9400)
        x[k:] += (np.sin(2 * np.pi * f * t[:m] + rng.random() * 6)
                  * np.exp(-t[:m] / rng.uniform(0.020, 0.085)) * rng.uniform(0.5, 1.0))
    x = x / jingles + rng.standard_normal(n) * np.exp(-t / 0.010) * 0.45
    out = hp(stereo(x), 2600)
    out = out + 0.5 * bandpass(out, 5000, 10000)
    return norm(widen(out, 0.7) * adsr(n, a=0.0005, r=0.02)[:, None], 0.85) * gain * 0.5


@cached
def bclap(dur_steps=3, gain=1.0, hands=5, seed=0):
    """Real hands, not a 909. Five people who do not clap together, in the
    same room, and the spread between them is the sound."""
    n, t = steps(dur_steps, floor=int(0.15 * SR))
    rng = np.random.default_rng(seed + 61)
    burst = np.zeros(n)
    for _ in range(hands):
        k = int(abs(rng.normal(0, 0.011)) * SR)
        m = n - k
        if m < 16:
            continue
        burst[k:] += rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.010)
    body = bandpass(stereo(burst / hands), 900, 5600)
    tail = bandpass(stereo(rng.standard_normal(n)), 1100, 4400) * np.exp(-t / 0.075)[:, None] * 0.4
    out = np.tanh(2.0 * (body * 1.4 + tail))
    return norm(widen(out, 0.9) * adsr(n, a=0.0008, r=0.025)[:, None], 0.85) * gain * 0.55


# ---- the pattern language ----
# The same 16-step notation the theory library is written in, so a groove can
# be read off the page and typed in: x = accent, + = normal, . = ghost,
# o = open, - = rest.
LEVEL = {'x': 1.00, '+': 0.68, '.': 0.34, 'o': 1.00}

GROOVE = {                                   # the main break, two bars
    'kick':  ('x---x---x---x---', 'x---x---x---x---'),
    'snare': ('----x-------x---', '----x-------x-+-'),
    'ghost': ('..-...-..-.-..-.', '..-...-.-..-..-.'),
    'hat':   ('x-+-x-+-x-+-x-+-', 'x-+-x-+-x-+-x-++'),
    'ohat':  ('--------o-------', '----------------'),
    'tamb':  ('--+---+---+---+-', '--+---+---+---+-'),
}


def _row(pat, row, b):
    """a pattern value may be one string or a tuple of them, one per bar"""
    v = pat.get(row)
    if v is None:
        return ''
    return v if isinstance(v, str) else v[b % len(v)]


def kitbar(s, b, pat, gain=1.0, swing=0.0, bus='drums', seed=0, jitter=2.5,
           tune=54.0, snare_tune=172.0, hats=1.0, fat=1.0, ghosts=1.0,
           register=True, decay=0.24):
    """One bar of the kit, read off a pattern dict.

    Swing is applied to the odd sixteenths only - never to the kick, which
    stays on the grid, because the whole point of a swung break over straight
    quarters is that the two disagree. Every hit gets its own velocity and a
    couple of milliseconds of timing error; a break with neither is a machine
    playing a drummer's part, and the ear hears the difference immediately."""
    rng = np.random.default_rng(seed * 977 + b * 31 + 7)
    sw = (swing - 0.5) * 2.0 * STEP if swing else 0.0
    for row in ('kick', 'snare', 'ghost', 'hat', 'ohat', 'ride', 'tamb', 'clap', 'tom'):
        chars = _row(pat, row, b)
        for i, ch in enumerate(chars):
            if ch == '-':
                continue
            v = LEVEL.get(ch, 1.0)
            t = s.pos(b, i)
            if row != 'kick':
                t += int((sw if i % 2 else 0) + rng.normal(0, jitter) * SR / 1000)
                v *= 1.0 + rng.normal(0, 0.09)
            sd = int(rng.integers(0, 4))                     # four takes per voice
            if row == 'kick':
                if register:
                    s.hit(t)
                seg, g = bkick(4.0, tune=tune, decay=decay, seed=sd), v
            elif row == 'snare':
                seg, g = bsnare(4.0, tune=snare_tune, fat=fat, seed=sd), v * 0.92
            elif row == 'ghost':
                seg, g = bghost(1.0, tune=snare_tune, seed=sd), v * 0.85 * ghosts
            elif row == 'hat':
                seg, g = bhat(1.0, open_=False, loose=0.25, seed=sd), v * 0.62 * hats
            elif row == 'ohat':
                seg, g = bhat(3.0, open_=True, seed=sd), v * 0.50 * hats
            elif row == 'ride':
                seg, g = bride(2.0, bell=1.0 if ch == 'o' else 0.0, seed=sd), v * 0.55
            elif row == 'tamb':
                seg, g = tambo(2.0, seed=sd), v * 0.50
            elif row == 'clap':
                seg, g = bclap(3.0, seed=sd), v * 0.60
            else:
                seg, g = btom(2.0, tune=125.0 - 22 * (i % 3), seed=sd), v * 0.7
            s.place(t, seg, g * gain, bus)


def fill(s, b, kind='roll', gain=1.0, bus='drums', seed=0, tune=54.0):
    """The bar-end. Big beat fills are edits, not drum solos: the same hit
    retriggered faster, or the last beat of the bar played twice."""
    rng = np.random.default_rng(seed + b)
    if kind == 'roll':
        st = [12, 13, 13.5, 14, 14.5, 15, 15.25, 15.5, 15.75]
        for i, x in enumerate(st):
            v = 0.55 + 0.45 * i / (len(st) - 1)
            s.place(s.pos(b, x), bsnare(2.0, seed=int(rng.integers(0, 4))), v * gain, bus)
    elif kind == 'toms':
        for i, (x, tn) in enumerate(zip((12, 13, 14, 15), (150, 128, 108, 92))):
            s.place(s.pos(b, x), btom(2.0, tune=tn, seed=i), (0.8 + 0.06 * i) * gain, bus)
    elif kind == 'stutter':
        for i, x in enumerate((14, 14.5, 15, 15.5)):
            s.place(s.pos(b, x), bsnare(2.0, tune=172 * (1 + 0.06 * i), seed=1),
                    (0.7 + 0.1 * i) * gain, bus)
    elif kind == 'break':
        s.place(s.pos(b, 14), bcrash(8, gain=0.7), gain, bus)
    elif kind == 'kicks':
        for x in (12, 13, 14, 15):
            t = s.pos(b, x)
            s.hit(t)
            s.place(t, bkick(3.0, tune=tune), 0.9 * gain, bus)


# ---- the bass ----
# A fuzz bass is one string through one blown-up amp. Rendered as eight
# separate notes per bar it comes out shattered - the fundamental dies in
# every gap and the overlaps cancel - so a whole bar is one oscillator whose
# pitch bends between the notes and whose amplitude swells at each pick. The
# split at 135 Hz is the other half of it: the fuzz never touches the sub,
# because distortion down there is intermodulation, not harmonics, and it
# makes the low end smaller.
@cached
def fuzzbar(notes, dur_steps=16, gain=1.0, fuzz=5.5, glide=0.012, decay=0.40,
            cut=2400.0, wah=0.0, wah_lo=280.0, wah_hi=2200.0, sub=1.0,
            grind=1.0, take=0):
    """One bar of fuzz bass. `notes` is a tuple of (step, midi)."""
    n, t = steps(dur_steps)
    evs = sorted(notes)
    edge = [min(int(st * STEP), n) for st, _ in evs] + [n]

    f = np.empty(n)                                    # one frequency track...
    f[:edge[0]] = midi(evs[0][1])
    for i, (_, nt) in enumerate(evs):
        f[edge[i]:edge[i + 1]] = midi(nt)
    f = uniform_filter1d(f, max(int(glide * SR), 3))   # ...smoothed = portamento
    ph = 2 * np.pi * np.cumsum(f) / SR                 # one unbroken phase

    amp = np.zeros(n)                                  # swells at each pick,
    for k in edge[:-1]:                                # never returns to zero
        np.maximum(amp[k:], np.exp(-np.arange(n - k) / SR / decay), out=amp[k:])
    amp = uniform_filter1d(amp, max(int(0.004 * SR), 3))

    low = (np.sin(ph) + 0.10 * np.sin(2 * ph)) * amp
    top = (saw_ph(ph, float(f.max())) + 0.5 * np.sin(2 * ph)) * amp
    st = stereo(np.tanh(fuzz * top))                   # the amp
    st = st + grind * 0.55 * np.tanh(3.0 * bandpass(st, 400, 2400))
    if wah:
        # `wah` is cycles per BAR, not hertz - a wah pedal is played in time
        # with the part, and a free-running LFO drifts against the riff.
        env = core._lfo01(t, wah * SR / BAR)
        st = morph_lp(st, wah_lo, wah_hi, env, bands=7, res=0.9)
    st = lp(hp(st, 135, order=2), cut)

    pick = np.zeros(n)                                 # the attacks, discrete
    rng = np.random.default_rng(600 + take)
    for k in edge[:-1]:
        m = min(n - k, int(0.010 * SR))
        if m > 32:
            pick[k:k + m] += rng.standard_normal(m) * np.exp(
                -np.arange(m) / SR / 0.0022) * 0.45

    out = lp(stereo(low), 115, order=4) * 1.30 * sub + st + hp(stereo(pick), 900) * 0.5
    out = np.tanh(1.3 * hp(out, 32, order=2))
    return (out * adsr(n, a=0.0012, r=0.004)[:, None]).astype(np.float32) * gain * 0.80


@cached
def bstab(note, dur_steps=2, gain=1.0, fuzz=6.0, take=0):
    """One bass note on its own, for a stab or a pickup"""
    return fuzzbar(((0, note),), dur_steps=dur_steps, gain=gain, fuzz=fuzz,
                   decay=dur_steps * 0.06, take=take)


# ---- the 303 ----
@cached
def acidbar(notes, dur_steps=16, cutoff=520.0, peak=3600.0, res=1.6, decay=0.13,
            drive=3.4, glide=0.045, gain=1.0, wave='saw', accent_lift=1.9,
            cut1=None, peak1=None, gain1=None):
    """One bar of 303, and the reason it is one bar and not sixteen notes is
    the whole design of the machine.

    The oscillator never stops and never retriggers; slides are a bend in one
    unbroken phase. All the articulation is the filter: a decay envelope
    reopens the cutoff at each note, an accent opens it further and holds it
    longer, and the resonant peak riding on top is what squelches. Notes are
    (step, midi, accent, slide) - a slid note inherits the envelope of the one
    before it, which is why a 303 line can have a note with no attack at all.

    `cut1`, `peak1` and `gain1` let the knob move ACROSS the bar rather than
    between bars. Hand the same curve its value at bar b and at bar b+1 and
    consecutive renders join with no step at the bar line - which is what
    turns a filtered arpeggio into acid over sixteen bars instead of into
    sixteen slightly different arpeggios."""
    n, t = steps(dur_steps)
    evs = sorted(notes)
    edge = [min(int(e[0] * STEP), n) for e in evs] + [n]

    f = np.empty(n)
    f[:edge[0]] = midi(evs[0][1])
    for i, e in enumerate(evs):
        f[edge[i]:edge[i + 1]] = midi(e[1])
    slid = np.zeros(n, dtype=bool)
    for i, e in enumerate(evs):
        if len(e) > 3 and e[3]:
            a = max(edge[i] - int(glide * SR), 0)
            slid[a:min(edge[i] + int(glide * SR), n)] = True
    fs = uniform_filter1d(f, max(int(glide * SR), 3))
    f = np.where(slid, fs, uniform_filter1d(f, max(int(0.003 * SR), 3)))
    ph = 2 * np.pi * np.cumsum(f) / SR

    fenv = np.zeros(n)                                 # the filter, per note
    amp = np.zeros(n)
    for i, e in enumerate(evs):
        acc = len(e) > 2 and e[2]
        if len(e) > 3 and e[3] and i:                  # slide: no new envelope
            continue
        k = edge[i]
        d = np.exp(-np.arange(n - k) / SR / (decay * (1.6 if acc else 1.0)))
        np.maximum(fenv[k:], d * (accent_lift if acc else 1.0), out=fenv[k:])
    for i, e in enumerate(evs):
        k = edge[i]
        hold = np.exp(-np.arange(n - k) / SR / (dur_steps * STEP / SR))
        np.maximum(amp[k:], np.minimum(hold + 0.55, 1.0), out=amp[k:])
    fenv = uniform_filter1d(np.clip(fenv / max(accent_lift, 1.0), 0, 1),
                            max(int(0.002 * SR), 3))
    amp = uniform_filter1d(amp, max(int(0.004 * SR), 3))

    x = saw_ph(ph, float(f.max())) if wave == 'saw' else np.sign(np.sin(ph))
    st = stereo(x * amp)

    # Where the cutoff knob is, per sample, and where the envelope takes it.
    # Both interpolated geometrically: a filter is heard in octaves, so a
    # linear ramp in hertz crawls at the bottom and bolts at the top.
    u = np.linspace(0.0, 1.0, n)
    c1 = cutoff if cut1 is None else cut1
    p1 = peak if peak1 is None else peak1
    base = cutoff * (c1 / cutoff) ** u
    top = np.maximum(peak * (p1 / peak) ** u, base * 1.02)
    f_t = base * (top / base) ** fenv
    F_LO = max(min(cutoff, c1) * 0.94, 40.0)
    F_HI = min(max(peak, p1) * 1.06, SR * 0.45)
    env = np.log(np.clip(f_t, F_LO, F_HI) / F_LO) / np.log(F_HI / F_LO)

    out = morph_lp(st, F_LO, F_HI, env, bands=13, res=res)
    out = np.tanh(drive * out / (1 + res * 0.42)) / np.tanh(drive)
    out = hp(out, 90, order=2)
    g = gain if gain1 is None else np.linspace(gain, gain1, n)
    env_a = adsr(n, a=0.002, r=0.01)
    return (out * (env_a * g)[:, None]).astype(np.float32) * 0.55


# ---- the organ ----
DRAWBARS = ((0.5, 1.0), (1.5, 0.55), (1.0, 1.0), (2.0, 0.7),
            (3.0, 0.35), (4.0, 0.45), (5.0, 0.15), (6.0, 0.15), (8.0, 0.25))


def organbar(notes, dur_steps=16, gain=1.0, draw=None, click=1.0, drive=2.0,
             seed=0):
    """A drawbar organ: nine sine partials per key at fixed footages, which is
    additive synthesis built in 1935. It is rendered a whole bar at a time and
    then gated into stabs by `chop`, because the tonewheels never stop turning
    and re-striking the key does not restart them - only the drawbar contacts
    open and close, and that click is the attack."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(seed + 71)
    bars = draw or DRAWBARS
    x = np.zeros(n)
    for f in notes:
        for mult, a in bars:
            if f * mult > 15000 or a <= 0:
                continue
            x += a * np.sin(2 * np.pi * f * mult * (1 + 0.0006 * rng.standard_normal())
                            * t + rng.random() * 6)
    x /= max(len(notes), 1) * 3.2
    tick = hp(stereo(rng.standard_normal(n) * np.exp(-t / 0.0035)), 2200) * 0.35 * click
    out = np.tanh(drive * stereo(x)) / np.tanh(drive) + tick
    return (out * adsr(n, a=0.004, r=0.02)[:, None]).astype(np.float32) * gain * 0.85


def leslie(seg, rate=6.4, drum_rate=5.4, depth=0.30, cents=26.0, split_hz=800.0,
           mix=1.0):
    """A rotating speaker: the horn spins fast and bright, the bass drum in the
    cabinet spins slower, and they are not in phase with each other.

    Each band gets Doppler pitch modulation, amplitude modulation and panning
    from the same rotation - it is one physical thing doing all three, which is
    why a plain tremolo never sounds like this."""
    n = len(seg)
    t = np.arange(n) / SR
    base = np.arange(n, dtype=np.float64)
    out = np.zeros_like(seg)
    for band, r in ((hp(seg, split_hz, order=2), rate),
                    (lp(seg, split_hz, order=2), drum_rate)):
        for c in range(2):
            ang = 2 * np.pi * r * t + (0 if c == 0 else np.pi * 0.55)
            d = (cents / 1200.0) * np.sin(ang) * 0.020 * SR
            y = np.interp(np.clip(base + d, 0, n - 1), base, band[:, c])
            out[:, c] += (y * (1 - depth * 0.5 * (1 - np.cos(ang)))).astype(np.float32)
    return (out * mix + seg * (1 - mix)).astype(np.float32)


def chop(seg, hits, soft=0.0035, tail=0.0, depth=1.0):
    """Gate a continuous bar onto the grid. `hits` is (step, length_in_steps).

    This is how a held organ becomes stabs without a single note being
    retriggered: the tonewheels keep running underneath and only the gate
    moves, so consecutive stabs are phase-continuous and the chord never
    flickers the way sixteen separate renders do."""
    n = len(seg)
    env = np.zeros(n)
    k = max(int(soft * SR), 3)
    for st, ln in hits:
        a = max(int(st * STEP), 0)
        e = min(int((st + ln) * STEP) + int(tail * SR), n)
        if e - a < 2 * k:
            continue
        env[a:e] = 1.0
        env[a:a + k] = np.linspace(0, 1, k)
        env[e - k:e] = np.linspace(1, 0, k)
    return (seg * (1 - depth * (1 - env))[:, None]).astype(np.float32)


# ---- the horns ----
@cached
def horns(notes, dur_steps=3, gain=1.0, drive=3.0, scoop=0.55, bright=1.0, seed=0):
    """A three-piece horn section hitting one chord (`notes` is a tuple of
    frequencies - this voice is cached). The scoop is the whole thing: a real
    section slides up into the note over about thirty milliseconds, and they
    never all arrive together."""
    n, t = steps(dur_steps, floor=int(0.15 * SR))
    rng = np.random.default_rng(seed + 81)
    x = np.zeros(n)
    for f in notes:
        late = int(rng.uniform(0, 0.012) * SR)
        m = n - late
        if m < 32:
            continue
        bend = 1 - (scoop / 12.0) * np.exp(-t[:m] / 0.030)
        vib = 1 + 0.006 * np.sin(2 * np.pi * 5.1 * t[:m]) * np.minimum(t[:m] / 0.15, 1)
        ph = 2 * np.pi * np.cumsum(f * bend * vib) / SR
        x[late:] += (0.65 * saw_ph(ph, f * 14) + 0.35 * np.sign(np.sin(ph)))
    st = stereo(np.tanh(drive * x / max(len(notes), 1)))
    out = bandpass(st, 420, 3800 * bright) * 1.6 + 0.4 * bandpass(st, 3800, 7000) * bright
    out = out + hp(stereo(rng.standard_normal(n) * 0.06), 3000) * np.minimum(t / 0.02, 1)[:, None]
    env = np.exp(-t / (dur_steps * STEP / SR * 0.55)) * adsr(n, a=0.008, r=0.03)
    return norm(widen(out, 0.8) * env[:, None], 0.9) * gain * 0.6


# ---- the voice ----
# Consonant: (lo, hi, seconds, level). A syllable is a burst of shaped noise
# followed by a pitched vowel, and getting only the vowel is why synthesised
# vocals sound like pads. The consonant is 30 ms long and it is what the ear
# uses to decide there is a person there.
CONS = {'h': (900, 5000, 0.045, 0.5), 's': (4200, 9500, 0.075, 0.85),
        'sh': (2200, 6500, 0.070, 0.8), 'k': (1400, 5200, 0.014, 1.0),
        't': (3000, 8500, 0.009, 0.95), 'p': (600, 2600, 0.010, 0.7),
        'f': (2600, 7000, 0.055, 0.5), 'ch': (2000, 7500, 0.030, 0.9),
        'r': (700, 2000, 0.030, 0.35), 'n': (250, 1200, 0.030, 0.30),
        'th': (1600, 6200, 0.040, 0.35), 'b': (400, 2000, 0.012, 0.6),
        'd': (1800, 6000, 0.010, 0.8), 'l': (350, 1600, 0.025, 0.30)}


@cached
def syl(note, dur_steps=2, vowel=('ah', 'ah'), cons='', gain=1.0, bend=0.0,
        rasp=0.35, seed=0, decay=0.0):
    """One sung syllable, chopped out of a record that never existed.

    Two vowels crossfaded across the note, because a held vowel is a synth and
    a moving one is a word; a pitch bend at the start, because nobody lands on
    a note dead centre; a consonant burst in front."""
    n, t = steps(dur_steps, floor=int(0.08 * SR))
    rng = np.random.default_rng(seed + 91)
    f = midi(note) * (2 ** (bend / 12.0 * np.exp(-t / 0.045)))
    vib = 1 + 0.013 * np.sin(2 * np.pi * 5.4 * t) * np.minimum(t / 0.12, 1)
    x = np.zeros(n)
    for d in (0.996, 1.0, 1.004):
        ph = np.cumsum(f * d * vib) / SR
        x += 2 * ((ph + rng.random()) % 1.0) - 1
    x = x / 3 + rng.standard_normal(n) * rasp * 0.05
    st = stereo(x)
    u = np.clip(np.linspace(-0.25, 1.15, n), 0, 1) ** 0.8
    out = morph_formant(st, vowel[0], vowel[1], env=u, wet=1.0, gain=1.5)
    out = out + 0.35 * bandpass(st, 2400, 3400)
    if cons:
        lo, hi, d, lv = CONS[cons]
        m = min(n, int(d * SR))
        burst = rng.standard_normal(m) * np.exp(-np.arange(m) / SR / (d * 0.45))
        out[:m] += bandpass(stereo(burst), lo, hi)[:m] * lv * 1.2
    dec = decay or dur_steps * STEP / SR * 0.75
    env = np.minimum(t / 0.012, 1.0) * np.exp(-t / dec)
    out = out + 0.40 * bandpass(out, 1500, 4000)
    out = np.tanh(1.8 * hp(out, 150, order=2)) * (env * adsr(n, a=0.003, r=0.03))[:, None]
    return norm(out, 0.9) * gain * 0.62


def voxline(s, b, events, gain=1.0, bus='vox', seed=0, transpose=0, **kw):
    """place a line of syllables: (step, note, dur, vowel_pair, consonant)"""
    for i, ev in enumerate(events):
        st, note, dur, vow, cn = ev
        s.place(s.pos(b, st), syl(note + transpose, dur, vowel=vow, cons=cn,
                                  seed=seed + i, **kw), gain, bus)


@cached
def speak(words, dur_steps=16, note=52, gain=1.0, fall=4.0, rasp=0.5,
          bright=1.0, growl=0.30, seed=0):
    """A SPOKEN line, rendered as one continuous utterance.

    `syl` sings: it holds a pitch and crossfades two vowels. Speech does
    neither. The pitch falls across a whole sentence (declination) with a
    small rise on each stressed syllable; the vowel track never rests on one
    target, it is always travelling towards the next; and the syllables are
    not separate events, they are gates cut into one unbroken voice. Render
    speech as N little sung notes and you get a robot chanting - the words
    only appear when the formants are allowed to glide between them.

    `words` is a tuple of (step, length_steps, vowel_in, vowel_out, consonant,
    semitone_accent)."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(seed + 401)
    evs = sorted(words)

    # ---- one pitch track for the whole sentence ----
    semi = np.zeros(n)
    decl = -fall * np.linspace(0, 1, n) ** 0.75            # the sentence falls
    for st, ln, _, _, _, acc in evs:
        a = int(st * STEP)
        e = min(int((st + ln) * STEP), n)
        if e <= a:
            continue
        # a stressed syllable is a small rise that decays inside the syllable
        semi[a:e] = acc * np.exp(-np.arange(e - a) / SR / 0.09)
    semi = uniform_filter1d(semi + decl, max(int(0.020 * SR), 3))
    jit = uniform_filter1d(rng.standard_normal(n), max(int(0.012 * SR), 3)) * 0.18
    f = midi(note) * 2.0 ** ((semi + jit) / 12.0)
    ph = np.cumsum(f) / SR
    src = sum(2 * ((ph * d + rng.random()) % 1.0) - 1 for d in (0.997, 1.0, 1.003)) / 3
    src = src + rng.standard_normal(n) * rasp * 0.045      # breath in the glottis
    st_ = stereo(src)

    # ---- one vowel track, always travelling ----
    used = sorted({v for _, _, v0, v1, _, _ in evs for v in (v0, v1)} | {'uh'})
    w = np.zeros((n, len(used)))
    w[:, used.index('uh')] = 1.0                           # the resting mouth
    for st, ln, v0, v1, _, _ in evs:
        a = int(st * STEP)
        e = min(int((st + ln) * STEP), n)
        if e <= a:
            continue
        u = np.linspace(0, 1, e - a) ** 0.8
        w[a:e] = 0.0
        w[a:e, used.index(v0)] = 1 - u
        w[a:e, used.index(v1)] = u
    # 35 ms of smoothing IS the intelligibility: the tongue takes that long to
    # get from one target to the next, and the transition is what names the
    # consonant the ear thinks it heard.
    k = max(int(0.035 * SR), 3)
    w = np.stack([uniform_filter1d(w[:, i], k) for i in range(w.shape[1])], 1)
    w /= np.maximum(w.sum(axis=1, keepdims=True), 1e-6)

    out = np.zeros((n, 2), dtype=np.float32)
    for i, v in enumerate(used):
        if w[:, i].max() < 1e-3:
            continue
        band = sum(bandpass(st_, fc * 0.74, fc * 1.30) * g
                   for fc, g in zip(FORMANTS[v], (1.0, 0.72, 0.34)))
        out += (band * w[:, i][:, None]).astype(np.float32)
    out = out + 0.40 * bandpass(st_, 2400, 3400) * bright   # the singer's formant

    # ---- the gates and the consonants ----
    amp = np.zeros(n)
    for st, ln, _, _, cn, _ in evs:
        a = int(st * STEP)
        e = min(int((st + ln) * STEP), n)
        if e <= a:
            continue
        amp[a:e] = 1.0
        if cn:
            lo, hi, d, lv = CONS[cn]
            m = min(n - a, max(int(d * SR), 8))
            burst = rng.standard_normal(m) * np.exp(-np.arange(m) / SR / (d * 0.45))
            out[a:a + m] += bandpass(stereo(burst), lo, hi) * lv * 1.15
            amp[max(a - int(0.004 * SR), 0):a] = 0.0       # the stop before a plosive
    amp = uniform_filter1d(amp, max(int(0.008 * SR), 3))
    out = out * amp[:, None]
    out = np.tanh((1.4 + 2.6 * growl) * hp(out, 150, order=2))
    out = out + 0.35 * bandpass(out, 1600, 4200) * bright
    return norm(out * adsr(n, a=0.004, r=0.02)[:, None], 0.92) * gain * 0.60


# ---- the string ----
@cached
def steel(note, dur_steps=4, gain=1.0, decay=1.7, stiff=8e-5, pick_pos=0.17,
          pu_pos=0.11, damp=1.0, bright=1.0, tilt=0.80, partials=64,
          tension=1.0, take=0):
    """A struck steel string, built partial by partial.

    A Karplus-Strong string is a delay line, so its partials are exact
    multiples of the fundamental and they all decay through the same filter.
    A real steel string is neither, and the two differences are most of what
    makes one sound like metal and the other like a rubber band:

    STIFFNESS. Steel resists bending, so the restoring force on a partial has
    a term that grows with the square of its mode number and its frequency
    lands SHARP: f_k = k*f0*sqrt(1 + B*k^2). The 20th partial of a wound
    guitar string sits a quarter-tone above where a harmonic series would put
    it. That stretch is why a piano is tuned stretched and why a guitar chord
    high up the neck beats against itself. No delay line can produce it.

    PER-PARTIAL DECAY. Energy leaves a high mode far faster than a low one, so
    the spectrum is not merely filtered as it decays, it changes shape - the
    note starts as a metallic clang and settles into a near-sine. Here each
    partial gets its own time constant.

    Two more that also cannot come out of one delay line: the string vibrates
    in TWO PLANES at once, a fraction of a hertz apart and coupling to the
    bridge differently, which gives the slow beating and the long second tail;
    and it is heard through a magnetic pickup at one fixed point, so partials
    with a node there are missing - a second comb on top of the pick's."""
    n, t = steps(dur_steps, floor=int(0.12 * SR))
    f0 = midi(note)
    rng = np.random.default_rng(take * 977 + int(note))
    # A hard pluck stretches the string: the tension is up while the amplitude
    # is large, so the note is sharp for the first thirty milliseconds and
    # settles. It is the sound of a string being hit rather than bowed.
    ph1 = 2 * np.pi * np.cumsum(1.0 + 0.011 * tension * np.exp(-t / 0.026)) / SR
    x = np.zeros(n)
    tot = 1e-9
    for k in range(1, partials + 1):
        fk = k * f0 * np.sqrt(1.0 + stiff * k * k)
        if fk > 16500.0:
            break
        # A magnetic pickup senses velocity, not displacement, so the
        # partials of a pluck roll off at about 1/k and not 1/k^2. Steeper
        # than that and the string comes out sounding like a nylon one.
        a = abs(np.sin(np.pi * k * pick_pos)) / k ** tilt   # where it was hit
        a *= abs(np.sin(np.pi * k * pu_pos))                # where it is heard
        if a < 5e-4:
            continue
        tau = decay / (1.0 + damp * 0.17 * k ** 1.28)
        rise = 1.0 - np.exp(-t / (0.0011 + 0.0016 / k))     # highs arrive first
        # The second polarisation rings on after the first, but it couples to
        # the bridge less and less as the mode number rises - so the tail is a
        # low aftersound, not a high one. Weight it flat and the note gets
        # BRIGHTER as it decays, which no string has ever done.
        for det, w, ts in ((0.0, 1.0, 1.0),
                           (rng.uniform(0.5, 2.2), 0.70 / (1 + 0.075 * k), 2.3)):
            env = np.exp(-t / (tau * ts)) * rise
            x += a * w * np.sin((fk + det) * ph1 + rng.random() * 6) * env
        tot += a * 1.7
    x /= tot
    # the pick leaving the string: broadband, four milliseconds, and it is
    # what the ear locates the attack by
    m = min(n, int(0.005 * SR))
    click = rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.0013)
    st = stereo(x)
    st[:m] += bandpass(stereo(click), 1500, 8000)[:m] * 0.48 * bright
    return norm(st * adsr(n, a=0.0004, r=0.02)[:, None], 0.92) * gain


# ---- the surf guitar ----
@cached
def twang(note, dur_steps=4, gain=1.0, decay=1.4, trem=0.0, bend=0.0,
          bright=1.0, dirt=0.30, pick_pos=0.13, pu_pos=0.09, take=0):
    """A wound steel string on a bridge single-coil through a clean valve amp
    with the treble wound up.

    Everything that makes it a SURF guitar is after the string: the pickup is
    close to the bridge (a low `pu_pos`, so the comb keeps the top), it has a
    resonant peak at 3 kHz where its own inductance rings, and the amp is only
    just breaking up. The spring goes on the bus, not here. `trem` re-strikes
    the string that many times a second, which is how a surf player sustains a
    note at all; `bend` slides into the pitch from that many semitones below."""
    n, t = steps(dur_steps, floor=int(0.14 * SR))
    rng = np.random.default_rng(take * 131 + int(note))
    if trem:
        x = np.zeros((n, 2), dtype=np.float32)
        period = max(int(SR / trem), 96)
        for i, k in enumerate(range(0, n, period)):
            m = n - k
            if m < 96:
                break
            seg = steel(note, (m / STEP), decay=decay * 0.5, pick_pos=pick_pos,
                        pu_pos=pu_pos, take=int(take * 7 + i) % 5)[:m]
            x[k:k + len(seg)] += seg * (0.78 + 0.22 * rng.random())
        x /= 1.7
    else:
        x = steel(note, dur_steps, decay=decay, pick_pos=pick_pos,
                  pu_pos=pu_pos, take=take)[:n]
    if bend:
        rate = 2.0 ** (-bend / 12.0 * np.exp(-t / 0.055))
        idx = np.cumsum(rate)
        idx = idx[idx < n - 1]
        if len(idx) > 64:
            x = np.stack([np.interp(np.arange(n), np.arange(len(idx)),
                                    np.interp(idx, np.arange(n), x[:, c]))
                          for c in range(2)], 1).astype(np.float32)
    st = hp(x, 165, order=2)
    st = st + 1.05 * bright * bandpass(st, 2100, 4300)      # the pickup rings
    st = st + 0.42 * bandpass(st, 620, 1500)                # the body
    g = 1.0 + 3.4 * dirt
    st = np.tanh(g * st) / np.tanh(g)                       # an amp, barely on
    st = st + 0.28 * bright * bandpass(st, 4200, 7200)
    return norm(lp(st, 8500, order=2), 0.92) * gain * 0.55


def twangbar(s, b, notes, gain=1.0, bus='gtr', swing=0.0, seed=0, **kw):
    """a bar of the riff. `notes` is (step, midi, length[, dict of overrides])"""
    sw = (swing - 0.5) * 2.0 * STEP if swing else 0.0
    for i, ev in enumerate(notes):
        st, nt, ln = ev[0], ev[1], ev[2]
        extra = ev[3] if len(ev) > 3 else {}
        t = s.pos(b, st) + int(sw if st % 2 else 0)
        s.place(t, twang(nt, ln, take=(seed + i) % 5, **{**kw, **extra}), gain, bus)


# ---- the spring ----
_SPRING = {}


def _spring_ir(decay, tone, boing, seed):
    key = (round(decay, 2), int(tone), round(boing, 2), int(seed))
    if key not in _SPRING:
        n = int(decay * SR)
        t = np.arange(n) / SR
        rs = np.random.default_rng(seed + 1301)
        ir = np.zeros((n, 2), dtype=np.float32)
        # A spring is DISPERSIVE: steel carries high frequencies at a
        # different speed from low ones, so an impulse does not come back as
        # an impulse, it comes back as a chirp. That is the whole sound - one
        # reflection smeared across thirty milliseconds with its top arriving
        # first, and each later reflection smeared further than the last.
        d = 0.027
        for i in range(7):
            k = int(d * SR)
            m = min(int((0.020 + 0.011 * i) * SR), n - k)
            if m < 64:
                break
            u = np.arange(m) / SR
            span = m / SR
            f0, f1 = 3300.0 - 190 * i, 540.0 - 28 * i
            ch = np.sin(2 * np.pi * (f0 * u + (f1 - f0) / (2 * span) * u ** 2))
            ch = ch * np.exp(-u / (0.008 + 0.0035 * i)) * 0.82 ** i * boing
            ir[k:k + m, i % 2] += ch.astype(np.float32)
            ir[k:k + m, (i + 1) % 2] += (ch * 0.55).astype(np.float32)
            d *= 1.61
        ir += (rs.standard_normal((n, 2)) * np.exp(-3.4 * t / decay)[:, None]
               * 0.30).astype(np.float32)
        # Springs have almost no bandwidth. That is why a spring sits BEHIND a
        # guitar instead of on top of it: it cannot reach the frequencies the
        # pick attack lives at, so the attack stays dry and only the note wets.
        ir = bandpass(ir, 320, tone, order=2)
        ir /= np.sqrt((ir ** 2).sum(axis=0, keepdims=True)) + 1e-9
        _SPRING[key] = ir
    return _SPRING[key]


def spring(buf, decay=1.5, wet=0.30, tone=4200, boing=1.0, predelay=0.004,
           seed=0, block_bars=16):
    """Spring reverb - the tail ONLY, add it to the bus.

    Not a room. A room is thousands of reflections in air; this is seven
    reflections in three feet of coiled steel, each dispersed into a chirp and
    band-limited to what metal can carry. Surf guitar without it is a clean
    guitar, and no amount of plate or hall gets you there."""
    out = np.zeros_like(buf)
    ir = _spring_ir(decay, tone, boing, seed)
    pre = int(predelay * SR)
    blk = int(block_bars * BAR)
    for a in range(0, len(buf), blk):
        seg = buf[a:a + blk]
        if np.abs(seg).max() < 1e-6:
            continue
        for c in range(2):
            w = wet * fftconvolve(seg[:, c], ir[:, c])
            b, e = a + pre, min(a + pre + len(w), len(out))
            if b < len(out):
                out[b:e, c] += w[:e - b].astype(np.float32)
    return hp(out, 300, order=2)


# ---- the turntable ----
# `scratch` and `spin` moved to core: reading a segment with a varying rate
# is apparatus, not a taste decision, and it sits with `rewind` and
# `tape_stop`. They arrive here through `from core import *`.


def accel(s, t0, seg, total_steps=16.0, step0=2.0, step1=0.25, gain=1.0,
          gain1=None, bus='fx', rise=0.0, curve=1.0, clip_slice=True,
          fade=0.004):
    """The Rockafeller build: one slice retriggered at a rate that shrinks
    geometrically until the ear cannot count it any more.

    Not a roll and not a stutter effect. The spacing walks from `step0` to
    `step1` across `total_steps`, and each hit is truncated to its own spacing
    so the repeats never overlap into a drone - which is the difference between
    a loop speeding up and a loop being buried. `rise` pitches each repeat up
    by that many semitones over the whole run."""
    k = max(int(fade * SR), 3)
    pos, out = 0.0, []
    while pos < total_steps - 1e-6:
        u = (pos / total_steps) ** curve
        d = step0 * (step1 / step0) ** u
        out.append((pos, u, min(d, total_steps - pos)))
        pos += d
    for pos, u, d in out:
        piece = seg
        g = gain if gain1 is None else gain + (gain1 - gain) * u
        if rise:
            piece = pitched(piece, 2.0 ** (rise * u / 12.0))
        if clip_slice:
            m = max(int(d * STEP), 2 * k + 2)
            piece = piece[:m].copy()
            if len(piece) > 2 * k:
                piece[-k:] *= np.linspace(1, 0, k)[:, None]
        s.place(int(t0 + pos * STEP), piece, g, bus)
    return len(out)


def stab_riser(dur_steps=16, gain=1.0, f0=200.0, f1=4200.0, seed=0):
    """The big beat riser is a band of noise being opened, not a synth sweep -
    it is the same white noise the hats are made of, so it belongs."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(seed + 101)
    nz = stereo(rng.standard_normal(n))
    u = (np.linspace(0, 1, n) ** 1.6)
    out = morph_lp(hp(nz, f0), f0, f1, u, bands=11, res=1.4)
    out = out * (0.25 + 0.75 * u)[:, None]
    return widen(np.tanh(1.4 * out), 1.2) * gain * 0.35
