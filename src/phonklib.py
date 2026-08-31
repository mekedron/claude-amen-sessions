"""The phonk layer: the cowbell and the car, on top of the shared engine.

Sets the grid to 160 BPM and adds the voices the genre is made of - a cowbell
driven until it clangs, power chords, memphis vocal chops, tyres and an
engine. The 808 drum machine and the 808 bass are generic enough to live in
core, along with the filters, reverb, the Session sequencer and the rest of
the palette; `sampler.Sample` is still there if a track wants to layer a
break over it.

Usage:
    from phonklib import *
    s = Session(100, tail=2.5)
    s.hit(s.pos(0, 0))                                  # sidechain trigger
    s.place(s.pos(0, 0), kick(), bus='drums')
    s.place(s.pos(0, 0), cowbell(66, 2), bus='music')
    s.render('phonk_drift_160.wav', drive=1.5, limit=0.94)
"""
import numpy as np
import core
from core import *

BAR, STEP = core.set_grid(bpm=160)
BPM = core.BPM

# ---- the cowbell ----
def cowbell(note, dur_steps=2.0, gain=1.0, drive=6.0, decay=0.24, bright=1.0,
            folded=0.0, ring=0.0):
    """The 808 cowbell at phonk strength: squares at f and 1.4815f, bandpassed,
    then driven until it clangs. folded>0 adds wavefolding grit; ring>0 detunes
    the upper oscillator so the two beat against each other."""
    n, t = steps(dur_steps)
    f = midi(note)
    x = square(f, t) + 0.85 * square(f * (1.4815 + ring), t)
    x = x * 0.5 * np.exp(-t / decay) + np.random.randn(n) * np.exp(-t / 0.004) * 0.18
    x = np.tanh(drive * x)
    if folded:
        x = (1 - folded) * x + folded * fold(x, 1.5 + drive * 0.1)
    out = bandpass(stereo(x), max(f * 0.85, 150), min(f * 12.0 * bright, 16000))
    out += 0.55 * hp(out, f * 2.6)                     # the clang, where the pitch really lives
    # dead centre on purpose: a Haas delay here combs the clang away in mono
    return out * adsr(n, a=0.0012, r=0.02)[:, None] * gain * 0.62

# ---- melodic ----
def guitar(note, dur_steps, gain=1.0, drive=7.0, fifth=True, cutoff=4200):
    """distorted power chord: root, fifth, octave, palm-muted decay"""
    n, t = steps(dur_steps)
    f = midi(note)
    x = saw(f, t) + (0.9 * saw(f * 1.4983, t) if fifth else 0) + 0.6 * saw(f * 2, t)
    out = hp(lp(stereo(np.tanh(drive * x / 2.5)), cutoff), 110)
    env = (0.45 + 0.55 * np.exp(-t / 0.28)) * adsr(n, a=0.003, r=0.05)
    return widen(out, 0.5) * env[:, None] * gain * 0.55

def screamlead(note, dur_steps, gain=1.0, drive=5.0, vib=5.5):
    """hard-clipped supersaw top-line for the last drop"""
    n, t = steps(dur_steps)
    f = midi(note)
    vibr = 1 + 0.007 * np.sin(2 * np.pi * vib * t) * np.minimum(t / 0.12, 1)
    x = np.zeros(n)
    for d in (0.988, 0.995, 1.0, 1.006, 1.013):
        x += saw_ph(2 * np.pi * np.cumsum(f * d * vibr) / SR, f * d)
    out = lp(hp(stereo(np.tanh(drive * x / 5)), 180), 6500)
    return widen(out, 0.7) * adsr(n, a=0.006, r=0.06)[:, None] * gain * 0.5

def chop(note, dur_steps, vowels=('ah', 'oo'), gain=1.0, grit=0.0, breath=0.25):
    """memphis vocal chop: a formant-morphing voice, pitched low and gritty"""
    n, t = steps(dur_steps)
    f = midi(note)
    vibr = 1 + 0.012 * np.sin(2 * np.pi * 4.6 * t) * np.minimum(t / 0.25, 1)
    x = np.zeros(n)
    for d in (0.996, 1.0, 1.004):
        x += saw_ph(2 * np.pi * np.cumsum(f * d * vibr) / SR, f * d) / 3
    st = stereo(x)
    m = np.linspace(0, 1, n)[:, None]
    v0, v1 = FORMANTS[vowels[0]], FORMANTS[vowels[-1]]
    out = np.zeros_like(st)
    for i, g in enumerate((1.0, 0.65, 0.3)):
        out += (bandpass(st, v0[i] * 0.75, v0[i] * 1.3) * (1 - m)
                + bandpass(st, v1[i] * 0.75, v1[i] * 1.3) * m) * g
    out += hp(stereo(np.random.randn(n)), 4000) * breath * 0.12
    if grit:
        out = (1 - grit) * out + grit * bitcrush(np.tanh(2.5 * out), 6, 3)
    a = min(int(0.05 * SR), n // 2); r = min(int(0.12 * SR), n // 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return widen(out, 0.7) * env[:, None] * gain * 1.7

def whisper(dur_steps, gain=1.0, syllables=4):
    """breathy unpitched voice: noise through fixed formants, cut into syllables"""
    n, t = steps(dur_steps)
    nz = stereo(np.random.randn(n))
    out = sum(bandpass(nz, fc * 0.7, fc * 1.4) * g
              for fc, g in ((520, 1.0), (1500, 0.7), (2900, 0.4)))
    syl = np.abs(np.sin(np.pi * syllables * np.linspace(0, 1, n))) ** 1.6
    return out * (syl * adsr(n, a=0.02, r=0.05))[:, None] * gain * 0.5

def pitch_echo(seg, steps_=2.0, times=4, fb=0.62, semis=(7, 12, 19, 24), spread=0.85, damp=1.0):
    """echoes that climb in pitch and jump from ear to ear"""
    d = int(steps_ * STEP)
    echoes = []
    for i in range(1, times + 1):
        e = pitched(seg, 2 ** (semis[(i - 1) % len(semis)] / 12))    # faster read = higher pitch
        e = lp(panned(e, spread if i % 2 else -spread), max(9000 * damp ** i, 1200)) * fb ** i
        echoes.append((i * d, e))
    total = max([len(seg)] + [o + len(e) for o, e in echoes])
    out = np.zeros((total, 2), dtype=np.float32)
    out[:len(seg)] += seg
    for o, e in echoes:
        out[o:o + len(e)] += e
    return out

# ---- the car ----
def engine(dur_steps, rpm0=42.0, rpm1=120.0, gain=1.0, shape=1.0, grit=3.0):
    """engine: a firing-rate saw stack climbing rpm0 -> rpm1, with intake roar"""
    n, t = steps(dur_steps)
    u = (t / t[-1]) ** shape
    ph = 2 * np.pi * np.cumsum(rpm0 + (rpm1 - rpm0) * u) / SR
    x = np.zeros(n)
    for k, a in ((1, 1.0), (2, 0.7), (3, 0.5), (4, 0.35), (6, 0.2), (8, 0.12)):
        x += a * np.sin(k * ph + 0.4 * np.sin(0.5 * k * ph))
    x = np.tanh(grit * x / 3)
    nz = stereo(np.random.randn(n))
    roar = (lp(nz, 300) * (1 - u)[:, None] + lp(nz, 1400) * u[:, None])[:, 0] * (0.3 + 0.5 * u)
    out = lp(stereo(x + roar), 3000)
    return widen(out, 2.0) * adsr(n, a=0.05, r=0.12)[:, None] * gain * 0.5

def screech(dur_steps, gain=1.0, f0=1150.0):
    """tyres letting go: a resonant noise band under a wavering squeal"""
    n, t = steps(dur_steps)
    u = t / t[-1]
    warble = 1 + 0.11 * np.sin(2 * np.pi * 7.5 * t) + 0.05 * np.sin(2 * np.pi * 23 * t)
    ph = 2 * np.pi * np.cumsum(f0 * warble * (1 + 0.25 * np.sin(np.pi * u))) / SR
    tone = 0.6 * np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    nz = bandpass(stereo(np.random.randn(n)), 1100, 4200) * 0.8
    out = np.tanh(1.8 * (stereo(tone) + nz))
    return widen(out, 1.6) * (np.sin(np.pi * u) ** 0.6)[:, None] * gain * 0.42

def siren(dur_steps, f0=780.0, lfo=1.6, gain=1.0):
    """the cops, two blocks back"""
    n, t = steps(dur_steps)
    f = f0 * (1 + 0.4 * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * lfo * t)))
    x = np.tanh(1.4 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return widen(stereo(x), 0.8) * adsr(n, a=0.02, r=0.15)[:, None] * gain * 0.35
