"""The hardstyle layer: the kick, the reverse bass and the screech.

Sets the grid to 170 BPM - industrial hardcore tempo - and adds what the
genre is actually made of. The kick is the instrument here: a sine dives onto
its root note and then goes through a real distortion chain, drive into EQ
into drive into a wavefolder, because every stage after an EQ makes new
harmonics and that is where the scream comes from. The offbeat bass is
written to swell into the gaps the kick leaves. Everything else comes from
core.

Usage:
    from hardlib import *
    s = Session(100, tail=3.0)
    for st in (0, 4, 8, 12):
        t = s.pos(0, st); s.hit(t)
        s.place(t, hardkick(), bus='drums')
    for st in (2, 6, 10, 14):
        s.place(s.pos(0, st), revbass(33, 2), bus='bass')
    s.render('hard_ascension_150.wav', drive=1.1, limit=0.93)
"""
import numpy as np
import core
from core import *

BAR, STEP = core.set_grid(bpm=170)
BPM = core.BPM

# ---- the kick ----
# The chain lives in core as rawkick(): every hard-dance genre is built on the
# same kick, and it is the one voice worth sharing between them.
hardkick = rawkick

def kickroll(s, b, steps_, note_from=55.0, note_to=55.0, bus='drums', gain=1.0, **kw):
    """a run of kicks across the bar, optionally climbing in pitch"""
    for i, st in enumerate(steps_):
        u = i / max(len(steps_) - 1, 1)
        t = s.pos(b, st)
        s.hit(t)
        s.place(t, hardkick(tune=note_from + (note_to - note_from) * u, **kw), gain, bus)

# ---- the offbeat ----
def revbass(note, dur_steps=2, gain=1.0, cutoff=850, drive=2.2, swell=0.75, tail=0.012):
    """the reverse bass: swells up in the gap and is cut off by the next kick"""
    n, t = steps(dur_steps)
    f = midi(note)
    x = saw(f, t) * 0.7 + np.sin(2 * np.pi * f * t) + 0.4 * saw(f * 2.002, t)
    out = lp(stereo(np.tanh(drive * x / 1.8)), cutoff)
    env = np.linspace(0, 1, n) ** swell
    k = min(int(tail * SR), n // 2)
    env[-k:] *= np.linspace(1, 0, k)
    return out * env[:, None] * gain

# ---- leads ----
def supersaw(notes, dur_steps, gain=1.0, detune=0.012, voices=7, cutoff=7000,
             attack=0.01, release=0.08, sub=0.0):
    """the euphoric wall: `voices` saws per note, spread across the stereo field"""
    n, t = steps(dur_steps)
    l = np.zeros(n); r = np.zeros(n)
    for f in notes:
        for i in range(voices):
            d = 1 + detune * (i - (voices - 1) / 2) / max((voices - 1) / 2, 1)
            v = saw(f * d, t, phase=np.random.rand() * 6)
            p = (i / max(voices - 1, 1)) * 2 - 1
            l += v * np.cos((p + 1) * np.pi / 4)
            r += v * np.sin((p + 1) * np.pi / 4)
        if sub:
            b = np.sin(2 * np.pi * f * 0.5 * t) * sub
            l += b; r += b
    out = lp(np.stack([l, r], 1).astype(np.float32) / (voices * len(notes)), cutoff)
    a = min(int(attack * SR), n // 2); rl = min(int(release * SR), n // 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a) ** 1.5; env[-rl:] *= np.linspace(1, 0, rl)
    return out * env[:, None] * gain * 2.2

def screech(note, dur_steps, gain=1.0, drive=6.0, fm=2.2, f0=3200, f1=700, res=2.2):
    """hardstyle screech: phase-modulated saws through a bandpass falling f0 -> f1"""
    n, t = steps(dur_steps)
    f = midi(note)
    ph = 2 * np.pi * f * t
    x = np.sin(ph + fm * np.sin(1.5 * ph)) + 0.7 * saw(f * 1.004, t) + 0.7 * saw(f * 0.996, t)
    x = np.tanh(drive * x / 2)
    st = stereo(x)
    u = (np.linspace(0, 1, n) ** 0.7)[:, None]
    band = bandpass(st, f0 * 0.7, f0 * 1.4) * (1 - u) + bandpass(st, f1 * 0.7, f1 * 1.4) * u
    out = hp(np.tanh(1.4 * (lp(st, 5000) * 0.5 + res * band)), 300)   # stay out of the kick
    # centred: the screech is the hook, and a Haas delay would comb it in mono
    return out * adsr(n, a=0.004, r=0.04)[:, None] * gain * 0.5

def shout(dur_steps=2, note=57, gain=1.0, vowel='eh'):
    """a crowd shout: formants over a fast pitch drop"""
    n, t = steps(dur_steps)
    f = midi(note) * (1 + 0.35 * np.exp(-t / 0.05))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = saw_ph(ph, midi(note) * 1.4) + np.random.randn(n) * 0.25
    st = stereo(x)
    out = sum(bandpass(st, fc * 0.72, fc * 1.35) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.8, 0.45)))
    env = np.exp(-t / 0.16) * adsr(n, a=0.006, r=0.05)
    return widen(np.tanh(1.6 * out), 0.8) * env[:, None] * gain * 1.2

# ---- fx ----
def gate(seg, rate_steps=1.0, duty=0.55, depth=1.0, soft=0.004):
    """trance gate: chop a held sound into the grid"""
    n = len(seg)
    period = max(int(rate_steps * STEP), 8)
    on = int(period * duty)
    env = np.zeros(n)
    k = max(int(soft * SR), 2)
    for a in range(0, n, period):
        b = min(a + on, n)
        env[a:b] = 1.0
        if b - a > 2 * k:
            env[a:a + k] = np.linspace(0, 1, k)
            env[b - k:b] = np.linspace(1, 0, k)
    env = 1 - depth * (1 - env)
    return (seg * env[:, None]).astype(np.float32)

def clap(dur_steps=3, gain=1.0, spread=1.0):
    """big hardstyle clap: four bursts and a room"""
    n, t = steps(dur_steps)
    burst = np.zeros(n)
    for d in (0.0, 0.011, 0.022, 0.034):
        k = int(d * SR)
        burst[k:] += np.random.randn(n - k) * np.exp(-np.arange(n - k) / SR / 0.013)
    body = bandpass(stereo(burst), 800, 6000)
    tail = bandpass(stereo(np.random.randn(n)), 1200, 5000) * np.exp(-t / 0.09)[:, None] * 0.5
    return widen(np.tanh(1.5 * (body + tail)), 0.45 * spread) * adsr(n, a=0.001, r=0.03)[:, None] * gain * 0.55
