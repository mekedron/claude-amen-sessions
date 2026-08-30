"""Shared engine for the beat_*.py scripts: Amen break slicing + synths.

On import: makes amen_174.wav from the source mp3 if missing (trim silence,
take 4 exact bars @140, sox speed to 174 BPM - pitch rises, jungle-style),
then loads it and exposes the slice library.

Slice map (4 bars x 16 steps, from spectral analysis of the sample):
bars 0/1 identical: kick 0,2; snare 4; ghosts 6-9; kicks 10-11; snare 12.
bar 2 ends with kick@12 snare@14. bar 3 is the shifted bar, crash accent @10.

Usage:
    from amenlib import *
    s = Session(22)                     # 22 bars + tail
    s.place(s.pos(0), bar_of(0))        # whole bar
    s.pat(1, [(0, K), (4, SN), (12, S2, 0.8)])   # (step, slice[, gain])
    s.place(s.pos(2, 0), sub(55.0, 4), 0.3)      # synth bass
    s.render('my_beat.wav')
"""
import os, subprocess, numpy as np, wave
from scipy.signal import butter, sosfiltfilt, fftconvolve

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, 'samples')
RENDERS = os.path.join(ROOT, 'renders')
SRC_MP3 = os.path.join(SAMPLES, 'axel_bfdi2025-amen-break-140-bpm-333318.mp3')
BREAK_WAV = os.path.join(SAMPLES, 'amen_174.wav')

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

if not os.path.exists(BREAK_WAV):
    raw = os.path.join(SAMPLES, '_amen_raw.wav')
    trim = os.path.join(SAMPLES, '_amen_trim.wav')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', SRC_MP3, '-ar', '44100', raw], check=True)
    # 0.03118 = detected onset of the first hit; 6.85714 = 4 bars at 140 BPM
    subprocess.run(['sox', raw, trim, 'trim', '0.03118', '6.85714'], check=True)
    subprocess.run(['sox', trim, BREAK_WAV, 'speed', '1.2428571'], check=True)  # 174/140
    os.remove(raw); os.remove(trim)

brk = load(BREAK_WAV)
BAR = len(brk) / 4.0
STEP = BAR / 16.0

# ---- slice tools ----
def fade_edges(seg, ms=3.0):
    seg = seg.copy()
    k = min(int(SR * ms / 1000), len(seg) // 2)
    if k > 0:
        seg[:k] *= np.linspace(0, 1, k)[:, None]
        seg[-k:] *= np.linspace(1, 0, k)[:, None]
    return seg

def get(b, s, ns=1):
    a = int(round(b * BAR + s * STEP))
    e = int(round(b * BAR + (s + ns) * STEP))
    return fade_edges(brk[a:e])

def rev(seg): return fade_edges(seg[::-1])

def pitched(seg, factor):
    """factor<1 -> slower+lower, >1 -> faster+higher."""
    n = len(seg)
    idx = np.arange(0, n - 1, factor)
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], axis=1)
    return fade_edges(out.astype(np.float32))

def lp(seg, hz, order=4):
    sos = butter(order, hz, 'low', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def hp(seg, hz, order=2):
    sos = butter(order, hz, 'high', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def dirty(seg, g=2.0):
    return (np.tanh(g * seg) / np.tanh(g)).astype(np.float32)

def bitcrush(seg, bits=6, downsample=4):
    """lo-fi glitch: amplitude quantize + sample-rate reduction"""
    q = 2 ** (bits - 1)
    x = np.round(seg * q) / q
    if downsample > 1:
        x = np.repeat(x[::downsample], downsample, axis=0)[:len(seg)]
    return x.astype(np.float32)

# ---- slice library ----
K   = get(0, 0)        # kick + ride
K2  = get(0, 2)        # second kick
SN  = get(0, 4, 2)     # snare with tail
SN1 = get(0, 4)        # tight snare (rolls)
G   = get(0, 6)        # ghost/hat
S2  = get(0, 12, 2)    # second snare
CR  = get(3, 10, 2)    # crash accent from bar 4
def bar_of(b): return fade_edges(brk[int(round(b*BAR)):int(round((b+1)*BAR))], 2)

# ---- small helpers ----
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

def stereo(x): return np.stack([x, x], 1).astype(np.float32)

def adsr(n, a=0.008, r=0.06):
    a = int(a * SR); r = min(int(r * SR), n)
    env = np.ones(n)
    if a: env[:a] = np.linspace(0, 1, a)
    if r: env[-r:] *= np.linspace(1, 0, r)
    return env

def _lfo01(t, hz):
    """unipolar cosine LFO starting at 0"""
    return 0.5 - 0.5 * np.cos(2 * np.pi * hz * t)

# ---- synths (all return stereo float32, length dur_steps*STEP) ----
def sub(freq, dur_steps, gain=1.0):
    """clean sub sine with a tiny downward glide for punch"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    glide = freq * (1 + 0.12 * np.exp(-t / 0.02))
    ph = 2 * np.pi * np.cumsum(glide) / SR
    x = np.tanh(1.5 * (np.sin(ph) + 0.15 * np.sin(2 * ph))) * 0.75
    return stereo(x * adsr(n)) * gain

def wobble(freq, dur_steps, lfo_hz, gain=1.0):
    """jungle 'wow' sub: pitch + amp LFO"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    l = np.sin(2 * np.pi * lfo_hz * t)
    ph = 2 * np.pi * np.cumsum(freq * (1 + 0.03 * l)) / SR
    x = np.tanh(1.6 * np.sin(ph)) * (0.6 + 0.4 * (l * 0.5 + 0.5))
    return stereo(x * adsr(n, r=0.1)) * gain

def reese(freq, dur_steps, cutoff=350, gain=1.0):
    """two detuned saws, lowpassed - dark rolling bass"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    def saw(f): return 2 * ((f * t) % 1.0) - 1
    x = saw(freq * 0.995) + saw(freq * 1.005) + 0.5 * saw(freq * 2.003)
    x = lp(stereo(np.tanh(1.2 * x / 2.5)), cutoff)
    x[:, 1] = np.roll(x[:, 1], int(SR * 0.0008))
    return x * adsr(n, a=0.012, r=0.08)[:, None] * gain

def sawbass(freq, dur_steps, lfo_hz=2.0, gain=1.0):
    """jump-up mid saw: detuned saws + talky filter wobble (layer sub() under it)"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = sum(2 * ((freq * d * t) % 1.0) - 1 for d in (0.994, 1.0, 1.006)) / 3
    x = np.tanh(2.5 * x)
    dark, bright = lp(stereo(x), 300), lp(stereo(x), 3000)
    m = _lfo01(t, lfo_hz)[:, None]
    out = np.tanh(1.5 * (dark * (1 - m) + bright * m))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0006))
    return out * adsr(n, a=0.01, r=0.05)[:, None] * gain

def growl(freq, dur_steps, lfo_hz=4.0, fm=3.0, gain=1.0):
    """neuro growl: FM sine+saw, moving bandpass character, heavy tanh"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    depth = fm * (0.4 + 0.6 * _lfo01(t, lfo_hz))
    x = np.sin(2 * np.pi * freq * t + depth * np.sin(2 * np.pi * freq * 1.5 * t))
    x += 0.5 * (2 * ((freq * t) % 1.0) - 1)
    x = np.tanh(3 * x)
    dark, bright = lp(stereo(x), 180), lp(stereo(x), 2500)
    m = _lfo01(t, lfo_hz)[:, None]
    out = np.tanh(1.3 * (dark * (1 - m * 0.9) + bright * m))
    return out * adsr(n, a=0.006, r=0.05)[:, None] * gain

def hoover(freq, dur_steps, gain=1.0, sweep=0.35):
    """rave hoover stab: thick detuned saw stack with a falling pitch sweep.
    sweep = how far above the note the attack starts (0.35 = siren, ~0.1 = in-tune)"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
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

def funkbass(freq, dur_steps, gain=1.0, pop=False):
    """staccato slap-style pluck: saw+square, filter chirp, fast decay.
    pop=True -> brighter/snappier (octave-pop accents)."""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = 0.6 * (2 * ((freq * t) % 1.0) - 1) + 0.4 * np.sign(np.sin(2 * np.pi * freq * t))
    x = np.tanh(1.8 * x)
    dark, bright = lp(stereo(x), 250), lp(stereo(x), 2200 if not pop else 3500)
    m = np.exp(-t / (0.05 if pop else 0.08))[:, None]     # filter chirp: bright attack
    out = dark * (1 - m) + bright * m
    env = np.exp(-t / (0.1 if pop else 0.16)) * adsr(n, a=0.004, r=0.02)
    return out * env[:, None] * gain

def clav(notes, dur_steps, gain=1.0):
    """short funky clav/organ chord stab (notes = list of freqs)"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in notes:
        x += (2 * ((f * t) % 1.0) - 1) + 0.3 * np.sign(np.sin(2 * np.pi * f * 2 * t))
    x /= len(notes)
    out = hp(lp(stereo(np.tanh(1.5 * x)), 4000), 300)
    env = np.exp(-t / 0.12) * adsr(n, a=0.003, r=0.02)
    return out * env[:, None] * gain

def wah(seg, lfo_hz=2.0, lo=400, hi=3200):
    """funky wah: LFO crossfade between dark and bright filterings of a segment"""
    t = np.arange(len(seg)) / SR
    m = _lfo01(t, lfo_hz)[:, None]
    return (lp(seg, lo) * (1 - m) + lp(seg, hi) * m).astype(np.float32)

def rhodes(notes, dur_steps, gain=1.0):
    """soft e-piano chord: sine body + decaying 'tine' ping, light tremolo"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in notes:
        x += (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.9)
              + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.35)
              + 0.18 * np.sin(2 * np.pi * 7 * f * t) * np.exp(-t / 0.05))
    x = np.tanh(1.3 * x / len(notes)) * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t))
    out = lp(stereo(x), 5000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return out * adsr(n, a=0.004, r=0.08)[:, None] * gain

def pluck(freq, dur_steps, gain=1.0):
    """gentle melodic pluck (pairs well with Session.place_echo)"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * 2 * freq * t)
    out = stereo(np.tanh(x) * np.exp(-t / 0.22))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0012))
    return out * adsr(n, a=0.003, r=0.03)[:, None] * gain

def hat(dur_steps=0.6, open_=False, gain=1.0):
    """synth hi-hat / shaker tick for sections without the break"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = hp(stereo(np.random.randn(n)), 8000)
    return x * (np.exp(-t / (0.05 if open_ else 0.014)) * adsr(n, a=0.001, r=0.01))[:, None] * gain * 0.5

def riser(dur_steps, gain=1.0):
    """build-up sweep: noise opening up + rising tone, quadratic swell"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    u = (t / t[-1])[:, None]
    noise = np.random.randn(n)
    x = (lp(stereo(noise), 400) * (1 - u) ** 2
         + lp(stereo(noise), 2500) * 2 * u * (1 - u)
         + hp(stereo(noise), 1200) * u ** 2)
    ph = 2 * np.pi * np.cumsum(np.linspace(180, 760, n)) / SR
    x += 0.3 * stereo(np.sin(ph)) * u
    return x * (u ** 2) * gain * 0.55

def subdrop(dur_steps=8, f0=75.0, f1=28.0, gain=1.0):
    """bass-drop boom: sine falling f0->f1 with a long decay"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.25)
    x = np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return stereo(x * np.exp(-t / 1.1) * adsr(n, a=0.004, r=0.1)) * gain

def bell(freq, dur_steps, gain=1.0):
    """icy glass bell: sine + inharmonic shimmer partials, long ring"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.8)
         + 0.5 * np.sin(2 * np.pi * freq * 2.756 * t) * np.exp(-t / 0.3)
         + 0.25 * np.sin(2 * np.pi * freq * 5.404 * t) * np.exp(-t / 0.12))
    out = stereo(np.tanh(x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0014))
    return out * adsr(n, a=0.002, r=0.05)[:, None] * gain

def lead(freq, dur_steps, gain=1.0, vib=5.5):
    """bright detuned-saw game lead with delayed vibrato"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    vibr = 1 + 0.008 * np.sin(2 * np.pi * vib * t) * np.minimum(t / 0.15, 1)
    x = np.zeros(n)
    for d in (0.99, 1.0, 1.01):
        ph = np.cumsum(freq * d * vibr) / SR
        x += 2 * (ph % 1.0) - 1
    x = np.tanh(1.5 * x / 3)
    out = lp(stereo(x), 3800)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0010))
    return out * adsr(n, a=0.01, r=0.06)[:, None] * gain

def wind(dur_steps, gain=1.0):
    """mountain wind: dark noise with a slow drifting swell"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = lp(stereo(np.random.randn(n)), 900)
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t + np.random.rand() * 6)
    return x * (swell * np.hanning(n))[:, None] * gain * 0.6

def crackle(dur_steps, gain=1.0):
    """vinyl atmosphere: soft hiss + sparse dust pops"""
    n = int(dur_steps * STEP)
    hiss = hp(lp(stereo(np.random.randn(n) * 0.35), 7500), 1800)
    pops = np.zeros(n)
    idx = np.random.randint(0, n, size=max(4, int(n / SR * 9)))
    pops[idx] = np.random.uniform(0.4, 1.0, len(idx)) * np.random.choice([-1, 1], len(idx))
    return (hiss * 0.5 + lp(stereo(pops), 4200)) * adsr(n, a=0.05, r=0.1)[:, None] * gain * 0.5

def bandpass(seg, lo_hz, hi_hz, order=2):
    sos = butter(order, [lo_hz, hi_hz], 'band', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def vox(notes, dur_steps, gain=1.0, vowel='ah'):
    """formant choir pad: saw stack through vowel bandpasses, slow attack, vibrato"""
    FORM = {'ah': (700, 1220, 2600), 'oh': (450, 800, 2830), 'oo': (325, 700, 2530)}
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in notes:
        vibr = 1 + 0.006 * np.sin(2 * np.pi * 4.8 * t + np.random.rand() * 6)
        for d in (0.995, 1.0, 1.005):
            ph = np.cumsum(f * d * vibr) / SR
            x += 2 * (ph % 1.0) - 1
    x /= 3 * len(notes)
    st = stereo(x)
    out = sum(bandpass(st, fc * 0.75, fc * 1.3) * g
              for fc, g in zip(FORM[vowel], (1.0, 0.6, 0.25)))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0016))
    a = int(0.3 * SR); r = int(0.35 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, min(a, n)); env[-r:] *= np.linspace(1, 0, min(r, n))
    return out * env[:, None] * gain * 1.6

def strings(notes, dur_steps, gain=1.0):
    """ensemble strings: wide detuned saw stack, brighter and faster than pad"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
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

def orchhit(root_midi, dur_steps=3, gain=1.0):
    """jungle orchestra hit: minor stab across octaves + noise burst, fast decay"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for off in (-12, 0, 3, 7, 12, 15):
        f = midi(root_midi + off)
        x += (2 * ((f * t) % 1.0) - 1) * (1.4 if off <= 0 else 1.0)
    x = np.tanh(x / 4)
    x += 0.25 * np.random.randn(n) * np.exp(-t / 0.02)
    out = lp(stereo(x), 4500)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0008))
    return out * (np.exp(-t / 0.25) * adsr(n, a=0.003, r=0.03))[:, None] * gain

def zap(dur_steps=2, f0=2400.0, f1=70.0, gain=1.0):
    """laser zap FX: fast exponential pitch fall"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.045)
    x = np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return stereo(x * np.exp(-t / 0.11) * adsr(n, a=0.001, r=0.02)) * gain * 0.7

def acid(freq, dur_steps, cutoff=900, res=4.0, gain=1.0, accent=False):
    """303-ish squelch: saw through a narrow resonant band + drive"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = 2 * ((freq * t) % 1.0) - 1
    fc = cutoff * (1.6 if accent else 1.0) * (1 + 0.9 * np.exp(-0 * t))
    fc = float(np.clip(fc if np.isscalar(fc) else fc[0], 150, 8000))
    st = stereo(x)
    out = lp(st, fc * 1.2) + res * bandpass(st, fc * 0.85, fc * 1.18)
    out = np.tanh(1.8 * out / (1 + res * 0.5))
    env = np.exp(-t / (0.09 if accent else 0.16)) * adsr(n, a=0.003, r=0.02)
    return out * env[:, None] * gain

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

def panned(seg, p):
    """equal-power pan: p in [-1 (left), +1 (right)]"""
    out = seg.copy()
    a = (p + 1) * np.pi / 4
    out[:, 0] *= np.cos(a) * 1.41
    out[:, 1] *= np.sin(a) * 1.41
    return out

def drone(freq, dur_steps, gain=1.0):
    """deep space drone: sine layers breathing on slow independent LFOs"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
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

def impact(dur_steps=24, gain=1.0):
    """supernova: deep falling boom + noise blast darkening as it decays"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    f = 26 + (95 - 26) * np.exp(-t / 0.3)
    boom = np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 2.2)
    blast = np.random.randn(n)
    m = np.exp(-t / 0.5)[:, None]
    noise = (hp(stereo(blast), 1500) * m + lp(stereo(blast), 700) * (1 - m)) * np.exp(-t / 1.1)[:, None]
    out = stereo(boom) + 0.5 * noise
    return out * adsr(n, a=0.002, r=0.3)[:, None] * gain

def piano(notes, dur_steps, gain=1.0):
    """90s rave/house piano stab: bright, punchy, slightly detuned"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
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

def diva(freq, dur_steps, gain=1.0):
    """gospel diva wail: single-voice formant lead with deep delayed vibrato"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
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

def dubsiren(dur_steps, f0=650.0, lfo=3.0, gain=1.0, shape='tri'):
    """dub siren: sine swept by a triangle/square pitch LFO (feed to place_echo)"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    if shape == 'square':
        mod = np.sign(np.sin(2 * np.pi * lfo * t))
    else:
        mod = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * lfo * t))
    f = f0 * (1 + 0.35 * mod)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    out = stereo(np.tanh(1.3 * x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return out * adsr(n, a=0.01, r=0.12)[:, None] * gain * 0.7

def rewind(seg, accel=3.0):
    """DJ rewind: play the segment backwards, spinning faster as it goes"""
    n = len(seg)
    rate = np.linspace(1.0, accel, n)
    idx = np.cumsum(rate); idx = idx[idx < n - 1]
    r = seg[::-1]
    out = np.stack([np.interp(idx, np.arange(n), r[:, c]) for c in range(2)], axis=1)
    return fade_edges(out.astype(np.float32))

def pad(notes, dur_steps, cutoff=1800, gain=1.0):
    """soft detuned-saw chord, slow attack (notes = list of freqs)"""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in notes:
        for d in (0.996, 1.0, 1.004):
            x += 2 * ((f * d * t + np.random.rand()) % 1.0) - 1
    x /= 3 * len(notes)
    out = lp(stereo(x), cutoff)
    a = int(0.25 * SR); r = int(0.3 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain

# ---- sequencer ----
class Session:
    def __init__(self, nbars, tail=1.5):
        self.total = int(round(nbars * BAR)) + int(SR * tail)
        self.mix = np.zeros((self.total, 2), dtype=np.float32)

    def place(self, t, seg, gain=1.0):
        t = int(t); e = min(t + len(seg), self.total)
        if t < self.total:
            self.mix[t:e] += seg[:e - t] * gain

    def pos(self, b, s=0.0): return int(round(b * BAR + s * STEP))

    def pat(self, b, events):
        """events: (step, slice[, gain])"""
        for ev in events:
            g = ev[2] if len(ev) > 2 else 1.0
            self.place(self.pos(b, ev[0]), ev[1], g)

    def place_echo(self, t, seg, gain=1.0, times=3, delay_steps=3.0, fb=0.5):
        """place seg plus decaying dub echoes"""
        for i in range(times + 1):
            self.place(t + int(i * delay_steps * STEP), seg, gain * fb ** i)

    def render(self, filename, drive=1.2):
        m = hp(self.mix, 25)
        m = np.tanh(drive * m) / np.tanh(drive)
        m *= 0.94 / max(np.abs(m).max(), 1e-9)
        fi = int(0.01 * SR); m[:fi] *= np.linspace(0, 1, fi)[:, None]
        fo = int(1.2 * SR); m[-fo:] *= np.linspace(1, 0, fo)[:, None]
        os.makedirs(RENDERS, exist_ok=True)
        path = os.path.join(RENDERS, filename)
        save(path, m)
        print(f"{filename}: {self.total/SR:.2f}s rms={np.sqrt((m**2).mean()):.3f}")
