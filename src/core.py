"""The engine both music modules share: synths, effects, mixer.

Everything here is pure synthesis and knows nothing about any sample. A module
picks the grid once with `set_grid()` and every `dur_steps` argument in the
library is measured against it; one grid (one engine) per process.

    src/core.py      this file - oscillators, ~50 synths, effects, Session
    src/amenlib.py   the Amen module: the break, its slices, 174 BPM
    src/phonklib.py  the phonk module: the 808 kit and cowbell, 160 BPM

Both modules re-export this one, so `from amenlib import *` and
`from phonklib import *` give you the same core API plus that module's kit.
"""
import os, numpy as np, wave
from scipy.signal import butter, sosfiltfilt, fftconvolve
from scipy.ndimage import uniform_filter1d

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, 'samples')
RENDERS = os.path.join(ROOT, 'renders')

# ---- the grid ----
BPM = 174.0
BAR = SR * 60.0 / BPM * 4
STEP = BAR / 16.0

def set_grid(bar_samples=None, bpm=None, beats=4):
    """define the bar. Either give it a length in samples (the Amen module
    measures its break) or a tempo. Returns (BAR, STEP) in samples."""
    global BAR, STEP, BPM
    if bar_samples is None:
        bar_samples = SR * 60.0 / bpm * beats
    BAR = float(bar_samples)
    STEP = BAR / 16.0
    BPM = float(bpm) if bpm else SR * 60.0 * beats / BAR
    return BAR, STEP

def steps(dur_steps, floor=8):
    """(n_samples, time_axis) for a duration given in 16th-note steps"""
    n = max(floor, int(dur_steps * STEP))
    return n, np.arange(n, dtype=np.float64) / SR

# ---- i/o ----
def load(path):
    w = wave.open(path, 'rb')
    n, ch = w.getnframes(), w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch).astype(np.float32) / 32768
    w.close()
    return x

def save(path, x):
    x = np.clip(x, -1, 1)
    w = wave.open(path, 'wb')
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes())
    w.close()

# ---- primitives ----
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

def stereo(x): return np.stack([x, x], 1).astype(np.float32)

def lp(seg, hz, order=4):
    sos = butter(order, min(float(hz), SR * 0.49), 'low', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def hp(seg, hz, order=2):
    sos = butter(order, max(float(hz), 12.0), 'high', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def bandpass(seg, lo_hz, hi_hz, order=2):
    lo = max(float(lo_hz), 15.0)
    hi = min(float(hi_hz), SR * 0.48)
    if hi <= lo * 1.05:
        hi = min(lo * 1.5, SR * 0.48)
    sos = butter(order, [lo, hi], 'band', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def adsr(n, a=0.008, r=0.06):
    a = min(int(a * SR), n // 2); r = min(int(r * SR), n // 2)
    env = np.ones(n)
    if a: env[:a] = np.linspace(0, 1, a)
    if r: env[-r:] *= np.linspace(1, 0, r)
    return env

def fade_edges(seg, ms=3.0):
    seg = seg.copy()
    k = min(int(SR * ms / 1000), len(seg) // 2)
    if k > 0:
        seg[:k] *= np.linspace(0, 1, k)[:, None]
        seg[-k:] *= np.linspace(1, 0, k)[:, None]
    return seg

def _lfo01(t, hz):
    """unipolar cosine LFO starting at 0"""
    return 0.5 - 0.5 * np.cos(2 * np.pi * hz * t)

def norm(x, peak=0.95):
    return (x * (peak / max(np.abs(x).max(), 1e-9))).astype(np.float32)

# ---- waveshaping ----
def dirty(seg, g=2.0):
    """tanh drive, level-compensated"""
    return (np.tanh(g * seg) / np.tanh(g)).astype(np.float32)

sat = dirty

def fold(seg, g=1.6):
    """wavefolder: nastier than tanh - the sound of a cowbell pushed too far"""
    return np.sin(g * np.pi * 0.5 * np.clip(seg, -2, 2)).astype(np.float32)

def bitcrush(seg, bits=6, downsample=4):
    """lo-fi glitch: amplitude quantize + sample-rate reduction"""
    q = 2 ** (bits - 1)
    x = np.round(seg * q) / q
    if downsample > 1:
        x = np.repeat(x[::downsample], downsample, axis=0)[:len(seg)]
    return x.astype(np.float32)

# ---- caching ----
_SEG_CACHE = {}
def cached(fn):
    """A drum machine plays one recording of a kick, not four hundred fresh
    ones. Wrap a deterministic voice in this and the same arguments give back
    the same segment, so a six-minute track renders in seconds. Never wrap a
    voice that relies on fresh randomness per call - `pad`, `strings`, `vox`
    and `drone` all randomise their phases on purpose."""
    def wrap(*a, **kw):
        key = (fn.__name__, a, tuple(sorted(kw.items())))
        if key not in _SEG_CACHE:
            _SEG_CACHE[key] = fn(*a, **kw)
        return _SEG_CACHE[key]
    wrap.__name__ = fn.__name__
    wrap.__doc__ = fn.__doc__
    wrap.uncached = fn
    return wrap

# ---- oscillators ----
def square(f, t, nyq=16500.0, kmax=60):
    """band-limited square: odd harmonics only, nothing above nyq"""
    x = np.zeros(len(t)); k = 1
    while f * k < nyq and k < kmax:
        x += np.sin(2 * np.pi * f * k * t) / k
        k += 2
    return x * (4 / np.pi)

def saw(f, t, nyq=16500.0, kmax=80, phase=0.0):
    """band-limited sawtooth"""
    x = np.zeros(len(t)); k = 1
    while f * k < nyq and k < kmax:
        x += np.sin(2 * np.pi * f * k * t + phase) / k
        k += 1
    return x * (2 / np.pi)

def saw_ph(ph, f, nyq=16500.0, kmax=80):
    """band-limited sawtooth from a phase array - for glides and vibrato.
    ph = 2*pi*cumsum(f_inst)/SR; f is the highest frequency it reaches."""
    x = np.zeros(len(ph)); k = 1
    while f * k < nyq and k < kmax:
        x += np.sin(k * ph) / k
        k += 1
    return x * (2 / np.pi)

# ---- segment tools ----
def pitched(seg, factor):
    """factor<1 -> slower+lower, >1 -> faster+higher."""
    n = len(seg)
    idx = np.arange(0, n - 1, factor)
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], axis=1)
    return fade_edges(out.astype(np.float32))

def rev(seg): return fade_edges(seg[::-1])

def panned(seg, p):
    """equal-power pan: p in [-1 (left), +1 (right)]"""
    out = seg.copy()
    a = (p + 1) * np.pi / 4
    out[:, 0] *= np.cos(a) * 1.41
    out[:, 1] *= np.sin(a) * 1.41
    return out

def mono_below(seg, hz=120, order=4):
    """Fold everything under `hz` to the centre.

    The ear locates low frequencies by arrival time, not level, so there is
    no width down there to lose - but a club system that sums the bass, or a
    single earbud, will cancel whatever was out of phase. Reverb tails and
    Haas delays leak stereo into the sub without anyone hearing it until the
    track is on a big rig and the low end is quietly gone."""
    mid = seg.mean(axis=1)
    side = (seg[:, 0] - seg[:, 1]) * 0.5
    side = hp(np.stack([side, side], 1), hz, order)[:, 0]
    return np.stack([mid + side, mid - side], 1).astype(np.float32)

def widen(seg, ms=0.9):
    """Haas widening: nudge the right channel late"""
    out = seg.copy()
    out[:, 1] = np.roll(out[:, 1], int(SR * ms / 1000))
    return out

def wah(seg, lfo_hz=2.0, lo=400, hi=3200):
    """funky wah: LFO crossfade between dark and bright filterings of a segment"""
    t = np.arange(len(seg)) / SR
    m = _lfo01(t, lfo_hz)[:, None]
    return (lp(seg, lo) * (1 - m) + lp(seg, hi) * m).astype(np.float32)

def shelf(seg, hz, db, kind='high'):
    """gentle shelving EQ: add (or subtract) a filtered copy of the signal"""
    g = 10 ** (db / 20) - 1
    part = hp(seg, hz) if kind == 'high' else lp(seg, hz)
    return (seg + g * part).astype(np.float32)

def sweep_lp(seg, f0, f1, curve=1.0):
    """filter sweep: crossfade a dark and a bright copy over the segment"""
    u = (np.linspace(0, 1, len(seg)) ** curve)[:, None]
    return (lp(seg, f0) * (1 - u) + lp(seg, f1) * u).astype(np.float32)

def morph_lp(seg, f_lo, f_hi, env, bands=9, res=0.0, order=4):
    """A lowpass whose cutoff MOVES, approximated by crossfading a bank of
    static filters; `env` is 0..1 per sample and picks where in the bank each
    sample sits. `res` adds a resonant peak that travels with the cutoff.

    This is the difference between an instrument and a beep. A fixed filter
    with an envelope on the amplitude only changes how loud a note is; a
    moving filter changes what it is made of while it sounds, which is what
    every plucked or struck thing in the physical world does."""
    n = len(seg)
    fs = np.geomspace(max(f_lo, 40), min(f_hi, SR * 0.45), bands)
    u = np.clip(np.asarray(env, dtype=np.float64), 0, 1)[:n] * (bands - 1)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(fs):
        w = np.clip(1 - np.abs(u - i), 0, 1)
        if w.max() < 1e-4:
            continue
        y = lp(seg, f, order)
        if res:
            y = y + res * bandpass(seg, f * 0.82, f * 1.22, order=2)
        out += (y * w[:, None]).astype(np.float32)
    return out

def wow(seg, depth_ms=1.8, rate=0.7):
    """cassette wow: slow pitch drift from an uneven tape speed"""
    n = len(seg)
    t = np.arange(n) / SR
    idx = np.clip(np.arange(n) + depth_ms / 1000 * SR * np.sin(2 * np.pi * rate * t), 0, n - 1)
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], 1)
    return out.astype(np.float32)

def tape_stop(seg, stop_s=0.55):
    """the deck loses power: read rate falls 1 -> 0 and the pitch goes with it"""
    n = len(seg)
    m = max(int(stop_s * SR), 2)
    idx = np.cumsum(np.linspace(1.0, 0.0, m) ** 1.4)
    idx = idx[idx < n - 1]
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], 1)
    out *= (np.linspace(1, 0.15, len(out)) ** 0.7)[:, None]
    return out.astype(np.float32)

def rewind(seg, accel=3.0):
    """DJ rewind: play the segment backwards, spinning faster as it goes"""
    n = len(seg)
    rate = np.linspace(1.0, accel, n)
    idx = np.cumsum(rate); idx = idx[idx < n - 1]
    r = seg[::-1]
    out = np.stack([np.interp(idx, np.arange(n), r[:, c]) for c in range(2)], axis=1)
    return fade_edges(out.astype(np.float32))

# ---- space ----
_IR_CACHE = {}
def _reverb_ir(decay, tone):
    key = (round(decay, 2), int(tone))
    if key not in _IR_CACHE:
        n = int(decay * SR)
        t = np.arange(n) / SR
        rs = np.random.RandomState(hash(key) & 0xffff)
        ir = rs.randn(n, 2).astype(np.float32) * np.exp(-3 * t / decay)[:, None]
        ir = hp(lp(ir, tone), 150)          # dark tail, no low-end mud
        ir /= np.sqrt((ir ** 2).sum(axis=0, keepdims=True))
        _IR_CACHE[key] = ir
    return _IR_CACHE[key]

def reverb(seg, decay=3.0, wet=0.5, tone=4000, predelay=0.015):
    """space: convolution with a synthetic stereo IR; output rings past the input"""
    ir = _reverb_ir(decay, tone)
    pre = int(predelay * SR)
    out = np.zeros((len(seg) + pre + len(ir), 2), dtype=np.float32)
    out[:len(seg)] += seg
    for c in range(2):
        out[pre:pre + len(seg) + len(ir) - 1, c] += wet * fftconvolve(seg[:, c], ir[:, c])
    return out

def delay(seg, steps_=3.0, times=4, fb=0.45, ping=True, damp=400):
    """echoes ringing off into the mix, alternating channels when ping=True"""
    d = int(steps_ * STEP)
    out = np.zeros((len(seg) + d * times + 1, 2), dtype=np.float32)
    out[:len(seg)] += seg
    for i in range(1, times + 1):
        e = lp(seg, max(4200 - damp * i, 700)) * fb ** i
        if ping:
            e = panned(e, 0.6 if i % 2 else -0.6)
        out[i * d:i * d + len(seg)] += e
    return out

# ---- bass ----
def sub(freq, dur_steps, gain=1.0):
    """clean sub sine with a tiny downward glide for punch"""
    n, t = steps(dur_steps)
    glide = freq * (1 + 0.12 * np.exp(-t / 0.02))
    ph = 2 * np.pi * np.cumsum(glide) / SR
    x = np.tanh(1.5 * (np.sin(ph) + 0.15 * np.sin(2 * ph))) * 0.75
    return stereo(x * adsr(n)) * gain

def wobble(freq, dur_steps, lfo_hz, gain=1.0):
    """jungle 'wow' sub: pitch + amp LFO"""
    n, t = steps(dur_steps)
    l = np.sin(2 * np.pi * lfo_hz * t)
    ph = 2 * np.pi * np.cumsum(freq * (1 + 0.03 * l)) / SR
    x = np.tanh(1.6 * np.sin(ph)) * (0.6 + 0.4 * (l * 0.5 + 0.5))
    return stereo(x * adsr(n, r=0.1)) * gain

def reese(freq, dur_steps, cutoff=350, gain=1.0):
    """two detuned saws, lowpassed - dark rolling bass"""
    n, t = steps(dur_steps)
    def s(f): return 2 * ((f * t) % 1.0) - 1
    x = s(freq * 0.995) + s(freq * 1.005) + 0.5 * s(freq * 2.003)
    x = lp(stereo(np.tanh(1.2 * x / 2.5)), cutoff)
    x[:, 1] = np.roll(x[:, 1], int(SR * 0.0008))
    return x * adsr(n, a=0.012, r=0.08)[:, None] * gain

def sawbass(freq, dur_steps, lfo_hz=2.0, gain=1.0):
    """jump-up mid saw: detuned saws + talky filter wobble (layer sub() under it)"""
    n, t = steps(dur_steps)
    x = sum(2 * ((freq * d * t) % 1.0) - 1 for d in (0.994, 1.0, 1.006)) / 3
    x = np.tanh(2.5 * x)
    dark, bright = lp(stereo(x), 300), lp(stereo(x), 3000)
    m = _lfo01(t, lfo_hz)[:, None]
    out = np.tanh(1.5 * (dark * (1 - m) + bright * m))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0006))
    return out * adsr(n, a=0.01, r=0.05)[:, None] * gain

def growl(freq, dur_steps, lfo_hz=4.0, fm=3.0, gain=1.0):
    """neuro growl: FM sine+saw, moving bandpass character, heavy tanh"""
    n, t = steps(dur_steps)
    depth = fm * (0.4 + 0.6 * _lfo01(t, lfo_hz))
    x = np.sin(2 * np.pi * freq * t + depth * np.sin(2 * np.pi * freq * 1.5 * t))
    x += 0.5 * (2 * ((freq * t) % 1.0) - 1)
    x = np.tanh(3 * x)
    dark, bright = lp(stereo(x), 180), lp(stereo(x), 2500)
    m = _lfo01(t, lfo_hz)[:, None]
    out = np.tanh(1.3 * (dark * (1 - m * 0.9) + bright * m))
    return out * adsr(n, a=0.006, r=0.05)[:, None] * gain

def funkbass(freq, dur_steps, gain=1.0, pop=False):
    """staccato slap-style pluck: saw+square, filter chirp, fast decay.
    pop=True -> brighter/snappier (octave-pop accents)."""
    n, t = steps(dur_steps)
    x = 0.6 * (2 * ((freq * t) % 1.0) - 1) + 0.4 * np.sign(np.sin(2 * np.pi * freq * t))
    x = np.tanh(1.8 * x)
    dark, bright = lp(stereo(x), 250), lp(stereo(x), 2200 if not pop else 3500)
    m = np.exp(-t / (0.05 if pop else 0.08))[:, None]     # filter chirp: bright attack
    out = dark * (1 - m) + bright * m
    env = np.exp(-t / (0.1 if pop else 0.16)) * adsr(n, a=0.004, r=0.02)
    return out * env[:, None] * gain

def upright(freq, dur_steps, gain=1.0):
    """double bass pluck: warm decaying body, finger thump, slight scoop into pitch"""
    n, t = steps(dur_steps)
    scoop = freq * (1 - 0.03 * np.exp(-t / 0.015))
    ph = 2 * np.pi * np.cumsum(scoop) / SR
    x = (np.sin(ph) + 0.6 * np.sin(2 * ph) * np.exp(-t / 0.35)
         + 0.3 * np.sin(3 * ph) * np.exp(-t / 0.2)
         + 0.12 * np.sin(4 * ph) * np.exp(-t / 0.1))     # upper partials carry the pitch
    x += lp(stereo(np.random.randn(n)), 300)[:, 0] * np.exp(-t / 0.015) * 0.4
    x = np.tanh(1.4 * x)
    out = stereo(x)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0007))
    return out * (np.exp(-t / 0.55) * adsr(n, a=0.004, r=0.04))[:, None] * gain

def subdrop(dur_steps=8, f0=75.0, f1=28.0, gain=1.0, drive=1.5, decay=1.1):
    """bass-drop boom: sine falling f0->f1 with a long decay"""
    n, t = steps(dur_steps)
    f = f1 + (f0 - f1) * np.exp(-t / 0.25)
    x = np.tanh(drive * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return stereo(x * np.exp(-t / decay) * adsr(n, a=0.004, r=0.1)) * gain

# ---- keys, leads, voices ----
def clav(notes, dur_steps, gain=1.0):
    """short funky clav/organ chord stab (notes = list of freqs)"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        x += (2 * ((f * t) % 1.0) - 1) + 0.3 * np.sign(np.sin(2 * np.pi * f * 2 * t))
    x /= len(notes)
    out = hp(lp(stereo(np.tanh(1.5 * x)), 4000), 300)
    env = np.exp(-t / 0.12) * adsr(n, a=0.003, r=0.02)
    return out * env[:, None] * gain

def rhodes(notes, dur_steps, gain=1.0):
    """soft e-piano chord: sine body + decaying 'tine' ping, light tremolo"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        x += (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.9)
              + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.35)
              + 0.18 * np.sin(2 * np.pi * 7 * f * t) * np.exp(-t / 0.05))
    x = np.tanh(1.3 * x / len(notes)) * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t))
    out = lp(stereo(x), 5000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return out * adsr(n, a=0.004, r=0.08)[:, None] * gain

def piano(notes, dur_steps, gain=1.0):
    """90s rave/house piano stab: bright, punchy, slightly detuned"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        for d, g in ((0.997, 0.8), (1.0, 1.0), (1.004, 0.8)):
            x += g * (2 * ((f * d * t) % 1.0) - 1) * 0.6
        x += 0.5 * np.sin(2 * np.pi * f * t)
        x += 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.4)
    x = np.tanh(1.6 * x / (len(notes) * 2))
    out = hp(lp(stereo(x), 5200), 160)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0007))
    env = (0.4 * np.exp(-t / 0.06) + 0.6 * np.exp(-t / 0.5)) * adsr(n, a=0.002, r=0.04)
    return out * env[:, None] * gain

def pluck(freq, dur_steps, gain=1.0):
    """gentle melodic pluck (pairs well with Session.place_echo)"""
    n, t = steps(dur_steps)
    x = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * 2 * freq * t)
    out = stereo(np.tanh(x) * np.exp(-t / 0.22))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0012))
    return out * adsr(n, a=0.003, r=0.03)[:, None] * gain

# ---- arpeggios ----
# The metrical hierarchy of a 4/4 bar, as velocities. Beat 1 is strongest,
# beat 3 next, then 2 and 4, then the "and"s, then the remaining 16ths. An
# arpeggio that ignores this is a row of identical events, not a part.
_STEP_WEIGHT = {0: 1.00, 4: 0.78, 8: 0.88, 12: 0.74,
                2: 0.60, 6: 0.56, 10: 0.60, 14: 0.56}

def arp_seq(notes, bars=1, shape='up', rate=1.0, cycle=None, octaves=(0,),
            gate=None, ratchets=(), accents=(), tail=0.95, rotate=0,
            jitter=0.0, swing=0.0, seed=0):
    """Turn a chord into a part instead of a loop of itself.

    Returns [(step, midi_note, dur_steps, velocity), ...] across `bars` bars,
    ready to hand to any voice.

    The one decision that matters is `cycle`. A four-note pattern on a
    sixteen-step bar divides the bar exactly, so it lands identically every
    half-bar for the length of the track - that is what "all the arps sound
    the same" means, and no amount of reverb fixes it. Give the cycle a length
    coprime with 16 (5, 7, 9, 11) and the pattern walks: it starts on a
    different note every bar and does not come back around until bar 5, 7, 9
    or 11. Same notes, same synth, and it stops being wallpaper.

    shape    order the pool is played in
    cycle    notes before the pattern repeats - use 5/7/9/11, not 4 or 8
    octaves  octave offsets folded into the pool
    gate     0/1 mask over the cycle: which steps are silent (holes matter)
    ratchets indices in the cycle that fire twice at double speed
    accents  indices in the cycle that hit at full velocity
    tail     note length as a fraction of the step
    rotate   start the cycle somewhere other than its first note
    jitter   timing humanisation in steps (keep under ~0.06)
    swing    delay of every second note, as a fraction of a step
    """
    rs = np.random.RandomState(seed + 1)
    pool = [n + 12 * o for o in octaves for n in notes]
    if shape == 'down':
        pool = pool[::-1]
    elif shape == 'updown':
        pool = pool + pool[-2:0:-1]
    elif shape == 'downup':
        pool = pool[::-1] + pool[1:-1]
    elif shape == 'converge':                      # outside in: low, high, low, high
        lo, hi = pool[:], pool[::-1]
        pool = [x for pair in zip(lo, hi) for x in pair][:len(pool)]
    elif shape == 'thumb':                         # Alberti: root between every note
        root = pool[0]
        pool = [x for n in pool[1:] for x in (root, n)]
    elif shape == 'random':
        pool = list(rs.permutation(pool))
    cyc = int(cycle or len(pool))
    seq = [pool[i % len(pool)] for i in range(cyc)]

    out = []
    total = 16.0 * bars
    st = 0.0
    i = 0
    while st < total - 1e-6:
        k = (i + rotate) % cyc
        if gate is None or gate[k % len(gate)]:
            grid = int(round(st)) % 16
            v = _STEP_WEIGHT.get(grid, 0.42)
            if k in accents:
                v = min(1.0, v + 0.35)
            v *= 1.0 + 0.06 * rs.randn()
            pos = st + (swing * rate if int(st / rate) % 2 else 0.0)
            pos += jitter * rs.randn()
            if k in ratchets:                      # one step, two hits
                out.append((pos, seq[k], rate * 0.45 * tail, float(np.clip(v, 0.05, 1.2))))
                out.append((pos + rate * 0.5, seq[k], rate * 0.45 * tail,
                            float(np.clip(v * 0.72, 0.05, 1.2))))
            else:
                out.append((pos, seq[k], rate * tail, float(np.clip(v, 0.05, 1.2))))
        st += rate
        i += 1
    return out

@cached
def arpvoice(freq, dur_steps, gain=1.0, wave='saw', detune=0.007, f_lo=300,
             f_hi=6500, res=1.5, decay=0.11, open_=1.0, floor_=0.05, sub=0.0,
             drive=1.6, bands=7):
    """An arp note whose spectrum moves while it sounds: detuned oscillators
    through a filter that closes as the note decays.

    `pluck` and `bell` hold one timbre for the whole note and only get
    quieter - fine once, but sixteen of them a bar is the sound people call
    raw. Here the filter starts at `f_hi` and falls to `f_lo` on every single
    note, which is what a plucked string does and what a 303 does."""
    n, t = steps(dur_steps)
    if wave == 'square':
        x = square(freq * (1 - detune), t) + square(freq * (1 + detune), t)
    elif wave == 'tri':
        x = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * freq * t)) * 2
    else:
        x = saw(freq * (1 - detune), t) + saw(freq * (1 + detune), t)
    if sub:
        x = x + sub * np.sin(np.pi * freq * t * 2 * 0.5)
    cut = floor_ + (open_ - floor_) * np.exp(-t / decay)
    out = morph_lp(stereo(x / 2), f_lo, f_hi, cut, bands=bands, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    env = np.exp(-t / max(decay * 1.9, 0.02)) * adsr(n, a=0.0025, r=0.02)
    return out * env[:, None] * gain * 0.5

def bell(freq, dur_steps, gain=1.0):
    """icy glass bell: sine + inharmonic shimmer partials, long ring"""
    n, t = steps(dur_steps)
    x = (np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.8)
         + 0.5 * np.sin(2 * np.pi * freq * 2.756 * t) * np.exp(-t / 0.3)
         + 0.25 * np.sin(2 * np.pi * freq * 5.404 * t) * np.exp(-t / 0.12))
    out = stereo(np.tanh(x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0014))
    return out * adsr(n, a=0.002, r=0.05)[:, None] * gain

def lead(freq, dur_steps, gain=1.0, vib=5.5):
    """bright detuned-saw game lead with delayed vibrato"""
    n, t = steps(dur_steps)
    vibr = 1 + 0.008 * np.sin(2 * np.pi * vib * t) * np.minimum(t / 0.15, 1)
    x = np.zeros(n)
    for d in (0.99, 1.0, 1.01):
        ph = np.cumsum(freq * d * vibr) / SR
        x += 2 * (ph % 1.0) - 1
    x = np.tanh(1.5 * x / 3)
    out = lp(stereo(x), 3800)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0010))
    return out * adsr(n, a=0.01, r=0.06)[:, None] * gain

def hoover(freq, dur_steps, gain=1.0, sweep=0.35):
    """rave hoover stab: thick detuned saw stack with a falling pitch sweep.
    sweep = how far above the note the attack starts (0.35 = siren, ~0.1 = in-tune)"""
    n, t = steps(dur_steps)
    penv = 1 + sweep * np.exp(-t / 0.09)
    x = np.zeros(n)
    for d in (0.985, 0.992, 1.0, 1.008, 1.015):
        ph = np.cumsum(freq * d * penv) / SR
        x += 2 * (ph % 1.0) - 1
    x /= 5
    ph = np.cumsum(freq * 0.5 * penv) / SR
    x += 0.4 * (2 * (ph % 1.0) - 1)                       # octave below
    x = np.tanh(2 * x)
    out = lp(stereo(x), 3500)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0011))
    env = np.exp(-t / 0.35) * adsr(n, a=0.005, r=0.04)
    return out * env[:, None] * gain

def acid(freq, dur_steps, cutoff=900, res=4.0, gain=1.0, accent=False):
    """303-ish squelch: saw through a narrow resonant band + drive"""
    n, t = steps(dur_steps)
    x = 2 * ((freq * t) % 1.0) - 1
    fc = float(np.clip(cutoff * (1.6 if accent else 1.0), 150, 8000))
    st = stereo(x)
    out = lp(st, fc * 1.2) + res * bandpass(st, fc * 0.85, fc * 1.18)
    out = np.tanh(1.8 * out / (1 + res * 0.5))
    env = np.exp(-t / (0.09 if accent else 0.16)) * adsr(n, a=0.003, r=0.02)
    return out * env[:, None] * gain

def orchhit(root_midi, dur_steps=3, gain=1.0):
    """jungle orchestra hit: minor stab across octaves + noise burst, fast decay"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for off in (-12, 0, 3, 7, 12, 15):
        f = midi(root_midi + off)
        x += (2 * ((f * t) % 1.0) - 1) * (1.4 if off <= 0 else 1.0)
    x = np.tanh(x / 4)
    x += 0.25 * np.random.randn(n) * np.exp(-t / 0.02)
    out = lp(stereo(x), 4500)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0008))
    return out * (np.exp(-t / 0.25) * adsr(n, a=0.003, r=0.03))[:, None] * gain

FORMANTS = {'ah': (700, 1220, 2600), 'oh': (450, 800, 2830), 'oo': (325, 700, 2530),
            'eh': (560, 1900, 2550), 'ih': (390, 1990, 2550)}

def vox(notes, dur_steps, gain=1.0, vowel='ah'):
    """formant choir pad: saw stack through vowel bandpasses, slow attack, vibrato"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        vibr = 1 + 0.006 * np.sin(2 * np.pi * 4.8 * t + np.random.rand() * 6)
        for d in (0.995, 1.0, 1.005):
            ph = np.cumsum(f * d * vibr) / SR
            x += 2 * (ph % 1.0) - 1
    x /= 3 * len(notes)
    st = stereo(x)
    out = sum(bandpass(st, fc * 0.75, fc * 1.3) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.6, 0.25)))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0016))
    a = int(0.3 * SR); r = int(0.35 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, min(a, n)); env[-r:] *= np.linspace(1, 0, min(r, n))
    return out * env[:, None] * gain * 1.6

def diva(freq, dur_steps, gain=1.0):
    """gospel diva wail: single-voice formant lead with deep delayed vibrato"""
    n, t = steps(dur_steps)
    vibr = 1 + 0.018 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(t / 0.35, 1)
    x = np.zeros(n)
    for d in (0.997, 1.0, 1.003):
        ph = np.cumsum(freq * d * vibr) / SR
        x += 2 * (ph % 1.0) - 1
    st = stereo(x / 3)
    out = sum(bandpass(st, fc * 0.72, fc * 1.32) * g
              for fc, g in zip((800, 1150, 2900), (1.0, 0.7, 0.35)))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0012))
    a = min(int(0.06 * SR), n // 2); r = min(int(0.15 * SR), n // 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain * 1.8

def horn(freq, dur_steps, gain=1.0, fall=0.0):
    """harmon-muted trumpet: reedy tone through a tight bandpass, breath,
    delayed vibrato; fall = semitones to drop at the phrase end (noir fall-off)"""
    n, t = steps(dur_steps)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 4.7 * t) * np.minimum(t / 0.4, 1)
    fenv = np.ones(n)
    if fall > 0:
        k = int(n * 0.75)
        fenv[k:] = 2 ** (-fall / 12 * np.linspace(0, 1, n - k))
    f = freq * vib * fenv
    ph = np.cumsum(f) / SR
    x = 0.6 * (2 * (ph % 1.0) - 1) + 0.4 * np.sign(np.sin(2 * np.pi * ph))
    st = stereo(np.tanh(1.3 * x))
    out = bandpass(st, 700, 2600) * 1.8
    out += hp(stereo(np.random.randn(n) * 0.05), 3000) * np.minimum(t / 0.1, 1)[:, None]
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0010))
    return out * adsr(n, a=0.04, r=0.09)[:, None] * gain

def strings(notes, dur_steps, gain=1.0):
    """ensemble strings: wide detuned saw stack, brighter and faster than pad"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        for d in (0.992, 0.997, 1.003, 1.008):
            x += 2 * ((f * d * t + np.random.rand()) % 1.0) - 1
    x /= 4 * len(notes)
    out = hp(lp(stereo(x), 5500), 200)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0013))
    a = int(0.09 * SR); r = int(0.2 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, min(a, n)); env[-r:] *= np.linspace(1, 0, min(r, n))
    return out * env[:, None] * gain

def pad(notes, dur_steps, cutoff=1800, gain=1.0, wide=0.0):
    """soft detuned-saw chord, slow attack (notes = list of freqs)"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        for d in (0.996, 1.0, 1.004):
            x += 2 * ((f * d * t + np.random.rand()) % 1.0) - 1
    x /= 3 * len(notes)
    out = lp(stereo(x), cutoff)
    if wide:
        out = widen(out, wide)
    a = int(0.25 * SR); r = int(0.3 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain

def drone(freq, dur_steps, gain=1.0):
    """deep space drone: sine layers breathing on slow independent LFOs"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for mult, amp, rate in ((0.5, 0.5, 0.031), (1.0, 1.0, 0.043), (1.498, 0.4, 0.057),
                            (2.005, 0.25, 0.071), (2.997, 0.12, 0.089)):
        breath = 0.55 + 0.45 * np.sin(2 * np.pi * rate * t + np.random.rand() * 6)
        x += amp * np.sin(2 * np.pi * freq * mult * t + np.random.rand() * 6) * breath
    x += 0.15 * lp(stereo(2 * ((freq * t) % 1.0) - 1), 600)[:, 0]
    out = stereo(np.tanh(x / 2))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.002))
    a = min(int(2.0 * SR), n // 2); r = min(int(2.5 * SR), n // 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain

# ---- the 808 drum machine ----
def kick(dur_steps=4, tune=51.0, top=290.0, punch=1.0, drive=2.6, gain=1.0, decay=0.34):
    """808 kick: a fast pitch dive into a saturated sine, with a click on top"""
    n, t = steps(dur_steps)
    f = tune + (top - tune) * np.exp(-t / 0.028)
    x = np.tanh(drive * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / decay)
    click = np.random.randn(n) * np.exp(-t / 0.0018) * 0.5 * punch
    click += np.sin(2 * np.pi * 1700 * t) * np.exp(-t / 0.004) * 0.35 * punch
    out = stereo(x) + hp(stereo(click), 900)
    return norm(out * adsr(n, a=0.0006, r=0.02)[:, None], 0.95) * gain

def snare(dur_steps=3, gain=1.0, drive=2.4, bright=1.0, body=1.0):
    """phonk snare: a clap stack over a short tuned body, driven hard"""
    n, t = steps(dur_steps)
    nz = np.random.randn(n)
    tail = hp(stereo(nz), 1500 * bright) * np.exp(-t / 0.115)[:, None]
    burst = np.zeros(n)
    for d in (0.0, 0.009, 0.019, 0.030):
        k = int(d * SR)
        burst[k:] += np.random.randn(n - k) * np.exp(-np.arange(n - k) / SR / 0.011)
    claps = bandpass(stereo(burst), 900, 5200 * bright) * 0.55
    tone = (0.55 * np.sin(2 * np.pi * 195 * t) * np.exp(-t / 0.055)
            + 0.35 * np.sin(2 * np.pi * 330 * t) * np.exp(-t / 0.04)) * body
    out = np.tanh(drive * (stereo(tone) + tail * 1.15 + claps)) / np.tanh(drive)
    return out * adsr(n, a=0.0008, r=0.02)[:, None] * gain

def rim(dur_steps=1, gain=1.0):
    """rimshot tick for the in-between 16ths"""
    n, t = steps(dur_steps)
    x = np.sin(2 * np.pi * 1750 * t) * np.exp(-t / 0.008)
    x += np.random.randn(n) * np.exp(-t / 0.004) * 0.6
    out = bandpass(stereo(np.tanh(2 * x)), 700, 7000)
    return out * adsr(n, a=0.0005, r=0.01)[:, None] * gain * 0.7

HAT808 = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)   # the six 808 cymbal squares

def hat808(dur_steps=1, open_=False, gain=1.0, tone=1.0):
    """808 hat: six detuned squares through a highpass, noise for the sizzle"""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 3))
    x = sum(square(f * tone, t) for f in HAT808) / 6 + np.random.randn(n) * 0.55
    dec = 0.24 if open_ else 0.026
    out = hp(stereo(np.tanh(1.4 * x)), 5800 if open_ else 7000)
    return out * (np.exp(-t / dec) * adsr(n, a=0.0004, r=0.01))[:, None] * gain * 0.55

def crash808(dur_steps=16, gain=1.0):
    """cymbal wash for the top of a drop"""
    n, t = steps(dur_steps)
    x = sum(square(f * 2.1, t) for f in HAT808) / 6 + np.random.randn(n) * 1.4
    out = hp(stereo(np.tanh(1.2 * x)), 3800)
    return widen(out, 1.3) * (np.exp(-t / 0.9) * adsr(n, a=0.001, r=0.15))[:, None] * gain * 0.34

def reverse_crash(dur_steps=8, gain=1.0):
    return np.ascontiguousarray(crash808(dur_steps, gain)[::-1])

# ---- 808 bass ----
def eight08(note, dur_steps, slide_from=None, glide=0.055, drive=2.4, gain=1.0,
            decay=0.75, click=True):
    """808 bass: a sine gliding into the note, saturated so it reads anywhere"""
    n, t = steps(dur_steps)
    f0 = midi(note)
    f = np.full(n, f0) if slide_from is None else f0 + (midi(slide_from) - f0) * np.exp(-t / glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.09 * np.sin(3 * ph)
    x = np.tanh(drive * x) / np.tanh(drive)
    if click:
        x = x + np.sin(4 * ph) * np.exp(-t / 0.009) * 0.35
    env = np.exp(-t / decay) * adsr(n, a=0.002, r=0.045)
    return norm(stereo(x * env), 0.92) * gain

def bass_drop(dur_steps=12, note=30, gain=1.0):
    """the hit that lands a drop: falling sub plus a noise blast"""
    n, t = steps(dur_steps)
    boom = subdrop(dur_steps, f0=midi(note) * 3.4, f1=midi(note), drive=1.9, decay=0.9)[:n]
    nz = np.random.randn(n)
    m = np.exp(-t / 0.35)[:, None]
    noise = (hp(stereo(nz), 2000) * m + lp(stereo(nz), 800) * (1 - m)) * np.exp(-t / 0.75)[:, None]
    return norm((boom + 0.45 * noise) * adsr(n, a=0.001, r=0.2)[:, None], 0.95) * gain

# ---- percussion and noise ----
def hat(dur_steps=0.6, open_=False, gain=1.0):
    """noise hi-hat / shaker tick"""
    n, t = steps(dur_steps)
    x = hp(stereo(np.random.randn(n)), 8000)
    return x * (np.exp(-t / (0.05 if open_ else 0.014)) * adsr(n, a=0.001, r=0.01))[:, None] * gain * 0.5

def crackle(dur_steps, gain=1.0):
    """vinyl atmosphere: soft hiss + sparse dust pops"""
    n, _ = steps(dur_steps)
    hiss = hp(lp(stereo(np.random.randn(n) * 0.35), 7500), 1800)
    pops = np.zeros(n)
    idx = np.random.randint(0, n, size=max(4, int(n / SR * 9)))
    pops[idx] = np.random.uniform(0.4, 1.0, len(idx)) * np.random.choice([-1, 1], len(idx))
    return (hiss * 0.5 + lp(stereo(pops), 4200)) * adsr(n, a=0.05, r=0.1)[:, None] * gain * 0.5

def wind(dur_steps, gain=1.0):
    """mountain wind: dark noise with a slow drifting swell"""
    n, t = steps(dur_steps)
    x = lp(stereo(np.random.randn(n)), 900)
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t + np.random.rand() * 6)
    return x * (swell * np.hanning(n))[:, None] * gain * 0.6

# ---- fx ----
def riser(dur_steps, gain=1.0, f0=180.0, f1=760.0):
    """build-up sweep: noise opening up + rising tone, quadratic swell"""
    n, t = steps(dur_steps)
    u = (t / t[-1])[:, None]
    noise = np.random.randn(n)
    x = (lp(stereo(noise), 400) * (1 - u) ** 2
         + lp(stereo(noise), 2500) * 2 * u * (1 - u)
         + hp(stereo(noise), 1200) * u ** 2)
    ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR
    x += 0.3 * stereo(np.sin(ph)) * u
    return x * (u ** 2) * gain * 0.55

def downlifter(dur_steps, gain=1.0, f0=1600.0, f1=60.0):
    """post-drop sweep down"""
    n, t = steps(dur_steps)
    u = t / t[-1]
    ph = 2 * np.pi * np.cumsum(f0 * (f1 / f0) ** u) / SR
    x = stereo(np.sin(ph) + 0.35 * np.sin(2 * ph)) + bandpass(stereo(np.random.randn(n)), 200, 3000) * 0.6
    return (widen(x, 1.5) * np.exp(-t / 0.6)[:, None] * gain * 0.4).astype(np.float32)

def whoosh(dur_steps, gain=1.0, rev_=False):
    """doppler pass-by: filtered noise sweeping across the head"""
    n, t = steps(dur_steps)
    u = t / t[-1]
    if rev_: u = u[::-1]
    nz = np.random.randn(n)
    x = (lp(stereo(nz), 500) * ((1 - u) ** 2)[:, None]
         + bandpass(stereo(nz), 700, 3500) * (2 * u * (1 - u))[:, None]
         + hp(stereo(nz), 3000) * (u ** 2)[:, None])
    p = np.linspace(-0.95, 0.95, n) * (-1 if rev_ else 1)
    a = (p + 1) * np.pi / 4
    x[:, 0] *= np.cos(a) * 1.41; x[:, 1] *= np.sin(a) * 1.41
    return (x * (np.sin(np.pi * (t / t[-1])) ** 1.2)[:, None] * gain * 0.45).astype(np.float32)

def impact(dur_steps=24, gain=1.0):
    """supernova: deep falling boom + noise blast darkening as it decays"""
    n, t = steps(dur_steps)
    f = 26 + (95 - 26) * np.exp(-t / 0.3)
    boom = np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 2.2)
    blast = np.random.randn(n)
    m = np.exp(-t / 0.5)[:, None]
    noise = (hp(stereo(blast), 1500) * m + lp(stereo(blast), 700) * (1 - m)) * np.exp(-t / 1.1)[:, None]
    out = stereo(boom) + 0.5 * noise
    return out * adsr(n, a=0.002, r=0.3)[:, None] * gain

def zap(dur_steps=2, f0=2400.0, f1=70.0, gain=1.0):
    """laser zap FX: fast exponential pitch fall"""
    n, t = steps(dur_steps)
    f = f1 + (f0 - f1) * np.exp(-t / 0.045)
    x = np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return stereo(x * np.exp(-t / 0.11) * adsr(n, a=0.001, r=0.02)) * gain * 0.7

def dubsiren(dur_steps, f0=650.0, lfo=3.0, gain=1.0, shape='tri'):
    """dub siren: sine swept by a triangle/square pitch LFO (feed to place_echo)"""
    n, t = steps(dur_steps)
    if shape == 'square':
        mod = np.sign(np.sin(2 * np.pi * lfo * t))
    else:
        mod = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * lfo * t))
    f = f0 * (1 + 0.35 * mod)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    out = stereo(np.tanh(1.3 * x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return out * adsr(n, a=0.01, r=0.12)[:, None] * gain * 0.7

# ---- mix tools ----
def duck_env(n, hits, depth=0.35, hold=0.012, release=0.19, attack=0.0022):
    """sidechain curve: dip to `depth` on every registered kick, then recover.

    `attack` is not decoration. Dropping the gain from 1.0 to depth inside a
    single sample is a step discontinuity in the waveform - a click. Normally
    the kick that triggered it lands on top and masks it, so nobody hears it;
    the moment the kick is quiet or absent - an intro where the floor is still
    fading in, a ghost trigger keeping the pump alive through a breakdown -
    the click is the only thing left. 2 ms is still far faster than any real
    compressor and costs the pump nothing."""
    env = np.ones(n, dtype=np.float32)
    if not hits:
        return env
    h, r = int(hold * SR), int(release * SR)
    a = max(int(attack * SR), 2)
    curve = np.concatenate([np.linspace(1.0, depth, a),
                            np.full(h, depth),
                            depth + (1 - depth) * (1 - np.exp(-np.linspace(0, 4, r)))]).astype(np.float32)
    for t in hits:
        t = int(t); e = min(t + len(curve), n)
        if t < n:
            np.minimum(env[t:e], curve[:e - t], out=env[t:e])
    return env

def softclip(x, ceiling=1.0, knee=0.65):
    """rounds off the peaks and leaves the body alone: everything under
    knee*ceiling passes untouched, the rest curves into the ceiling"""
    a = knee * ceiling
    y = np.abs(x)
    out = np.array(x, dtype=np.float32, copy=True)
    over = y > a
    out[over] = np.sign(x[over]) * (a + (ceiling - a) * np.tanh((y[over] - a) / (ceiling - a)))
    return out

def limiter(x, thresh=0.92, smooth=0.02, report=False):
    """smoothed peak limiter: the gain reduction is averaged, so it pulls, not clicks"""
    pk = np.maximum(np.abs(x[:, 0]), np.abs(x[:, 1]))
    g = np.minimum(1.0, thresh / np.maximum(pk, 1e-6))
    g = uniform_filter1d(g, max(int(smooth * SR), 3))
    if report:
        print(f"  limiter: max {-20*np.log10(max(g.min(),1e-6)):.1f} dB, "
              f"mean {-20*np.log10(g.mean()):.2f} dB of gain reduction")
    return (x * g[:, None]).astype(np.float32)

# ---- sequencer ----
class Session:
    """Mixes on named buses. Buses listed in DUCKED are sidechained against
    every kick registered with hit(); everything else passes through."""
    DUCKED = {'bass': 1.0, 'music': 0.7, 'pad': 0.85}

    def __init__(self, nbars, tail=1.5):
        self.total = int(round(nbars * BAR)) + int(SR * tail)
        self.bus = {}
        self.hits = []

    def _buf(self, name):
        if name not in self.bus:
            self.bus[name] = np.zeros((self.total, 2), dtype=np.float32)
        return self.bus[name]

    def place(self, t, seg, gain=1.0, bus='main'):
        t = int(t); e = min(t + len(seg), self.total)
        if t < self.total and e > t:
            self._buf(bus)[t:e] += seg[:e - t] * gain

    def hit(self, t):
        """register a sidechain trigger (a kick) at t"""
        self.hits.append(int(t))

    def pos(self, b, s=0.0): return int(round(b * BAR + s * STEP))

    def pat(self, b, events, bus='main'):
        """events: (step, segment[, gain])"""
        for ev in events:
            g = ev[2] if len(ev) > 2 else 1.0
            self.place(self.pos(b, ev[0]), ev[1], g, bus)

    def place_echo(self, t, seg, gain=1.0, times=3, delay_steps=3.0, fb=0.5, bus='main'):
        """place seg plus decaying dub echoes"""
        for i in range(times + 1):
            self.place(t + int(i * delay_steps * STEP), seg, gain * fb ** i, bus)

    def report(self, gains=None):
        """what each bus is contributing - level, punch, and where it sits"""
        bands = [(20, 60), (60, 200), (200, 800), (800, 3000), (3000, 10000), (10000, 20000)]
        print(f"{'bus':8s} {'rms':>7s} {'peak':>6s} {'crest':>6s} {'side%':>6s} |"
              + "".join(f"{a//1:>7d}" for a, _ in bands))
        for name in sorted(self.bus):
            b = self.bus[name] * (gains or {}).get(name, 1.0)
            m = b.mean(axis=1)
            r = float(np.sqrt((m ** 2).mean())) or 1e-9
            spec = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
            f = np.fft.rfftfreq(len(m), 1 / SR)
            sh = [spec[(f >= lo) & (f < hi)].sum() / max(spec.sum(), 1e-9) * 100 for lo, hi in bands]
            side = float(np.sqrt(((b[:, 0] - b[:, 1]) ** 2).mean())) / r * 100
            print(f"{name:8s} {r:7.3f} {np.abs(m).max():6.3f} {np.abs(m).max()/r:6.2f} {side:6.0f} |"
                  + "".join(f"{v:7.1f}" for v in sh))

    def mixdown(self, drive=1.2, duck=0.34, limit=0.0, peak=0.94, gains=None,
                clip=0.0):
        env = duck_env(self.total, self.hits, depth=duck)
        mix = np.zeros((self.total, 2), dtype=np.float32)
        for name, buf in self.bus.items():
            g = (gains or {}).get(name, 1.0)
            if name in self.DUCKED and self.hits:
                buf = buf * (1 - (1 - env) * self.DUCKED[name])[:, None]
            mix += buf * g
        mix = hp(mix, 25)
        if clip:
            # Shave the sharpest transients before the saturator sees them.
            # A clipper takes 1-2 dB off the very tip of a kick, where the ear
            # is masked anyway, and leaves the body alone - which is exactly
            # what a wide tanh does not do.
            before = float(np.abs(mix).max())
            touched = float((np.abs(mix).max(axis=1) > 0.8 * clip).mean()) * 100
            mix = softclip(mix, clip, knee=0.8)
            print(f"  clipper: {before:.2f} -> {float(np.abs(mix).max()):.2f} peak, "
                  f"{touched:.2f}% of samples shaped "
                  f"({'transients only' if touched < 2 else 'THIS IS EATING THE BODY'})")
        pk = float(np.abs(mix).max())
        if drive:
            mix = np.tanh(drive * mix) / np.tanh(drive)
            after = float(np.abs(mix).max())
            print(f"  saturation: bus sum peaks {pk:.2f} -> {after:.2f} "
                  f"({20*np.log10(max(after,1e-9)/max(pk,1e-9)):+.1f} dB). "
                  f"More than about -1 dB here and the tanh is distorting every "
                  f"transient, not gluing the mix.")
        if limit:
            mix = limiter(mix, limit, report=True)
        return mix * (peak / max(np.abs(mix).max(), 1e-9))

    def render(self, filename, drive=1.2, duck=0.34, limit=0.0, peak=0.94,
               fade=1.2, gains=None, clip=0.0):
        m = self.mixdown(drive, duck, limit, peak, gains, clip)
        fi = int(0.01 * SR); m[:fi] *= np.linspace(0, 1, fi)[:, None]
        fo = int(fade * SR); m[-fo:] *= np.linspace(1, 0, fo)[:, None]
        os.makedirs(RENDERS, exist_ok=True)
        path = os.path.join(RENDERS, filename)
        save(path, m)
        print(f"{filename}: {self.total/SR:.2f}s rms={np.sqrt((m**2).mean()):.3f}")
        return path
