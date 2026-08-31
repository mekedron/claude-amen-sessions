"""The rave layer: a breakbeat kit and the 1992 palette, at 138 BPM.

Built on top of the industrial module rather than beside it, because the 303
lives there and this is still acid - but almost nothing else is shared. The
grid is the difference: a breakbeat has no kick on every beat, so the pulse
has to be inferred from where the kick ISN'T, and that single change makes a
record sound like another genre far more than tempo or key ever will.

Everything here is what a breakbeat needs and a four-to-the-floor kit does
not: a short punchy kick, a snare with a room on it, ghost notes at a fifth
of the velocity, and the stabs that were sitting on every hardcore record of
1992 - hoovers, orchestra hits, a piano playing major chords in a minor key.

Usage:
    from ravelib import *
    s = Session(64, tail=3.0)
    s.place(s.pos(0, 0), breakkick(), bus='drums')
    s.place(s.pos(0, 4), breaksnare(), bus='drums')
    s.place(s.pos(0), acid(pattern), bus='acid')
"""
import numpy as np
import core
from industriallib import *

BAR, STEP = set_tempo(138)
BPM = 138.0

# ---- the break ----
@cached
def breakkick(dur_steps=2.0, tune=58.0, drive=4.0, decay=0.115, click=1.0,
              body=1.1, gain=1.0, seed=0):
    """Short, punchy, and not especially deep. A breakbeat kick is a drum in a
    room, not the floor of a club - it has to leave the low end for the bass
    and get out of the way of the snare that is coming 3/16 later."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 601)
    f = tune * (1 + 2.6 * np.exp(-t / 0.014))
    x = np.tanh(drive * np.sin(2 * np.pi * np.cumsum(f) / SR))
    st = lp(stereo(x), 6000)
    st = st + body * bandpass(st, tune * 0.8, tune * 2.4)
    st = st * np.exp(-t / decay)[:, None]
    if click:
        c = rs.randn(n) * np.exp(-t / 0.0016) * 0.7
        c += np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.003) * 0.4
        st = st + hp(stereo(c), 1800) * 0.45 * click
    return norm(hp(st, 36) * adsr(n, a=0.0005, r=0.012)[:, None], 0.95) * gain

@cached
def breaksnare(dur_steps=3.0, gain=1.0, tune=196.0, room=0.55, bright=1.0,
               ghost=False, seed=0):
    """A snare with a room on it. `ghost=True` gives the same drum at a fifth
    of the level and half the length - the quiet hits between the backbeats
    are what separates a breakbeat from a drum machine, and they are inaudible
    as events while being the entire groove."""
    n, t = steps(dur_steps if not ghost else max(dur_steps * 0.4, 0.6))
    rs = np.random.RandomState(seed + 631)
    tone = (0.6 * np.sin(2 * np.pi * tune * t) * np.exp(-t / 0.045)
            + 0.3 * np.sin(2 * np.pi * tune * 1.6 * t) * np.exp(-t / 0.03))
    nz = rs.randn(n)
    crack = bandpass(stereo(nz), 1200 * bright, 5200 * bright) * np.exp(-t / 0.085)[:, None]
    snap = bandpass(stereo(nz), 5000, 9000) * np.exp(-t / 0.018)[:, None] * 0.22
    out = stereo(tone) * 1.25 + crack * 0.85 + snap
    if room:
        out = out + room * reverb(lp(out, 6000), decay=0.42, wet=0.8, tone=4200)[:n]
    out = np.tanh(1.7 * out)
    g = gain * (0.2 if ghost else 1.0)
    return norm(out * adsr(n, a=0.0006, r=0.02)[:, None], 0.92) * g

@cached
def breakhat(dur_steps=0.6, open_=False, gain=1.0, seed=0):
    n, t = steps(dur_steps if not open_ else max(dur_steps, 2.4))
    rs = np.random.RandomState(seed + 661)
    x = bandpass(stereo(rs.randn(n)), 4600, 10500)
    dec = 0.17 if open_ else 0.024
    return x * (np.exp(-t / dec) * adsr(n, a=0.0005, r=0.008))[:, None] * gain * 0.46

# a Funky-Drummer-shaped bar: (step, what, gain). 'g' is a ghost snare.
BREAK_A = [(0, 'k', 1.0), (3, 'k', 0.8), (4, 's', 1.0), (6, 'g', 1.0), (7, 's', 0.55),
           (9, 'g', 1.0), (10, 'k', 0.9), (12, 's', 1.0), (14, 'g', 1.0), (15, 'k', 0.6)]
BREAK_B = [(0, 'k', 1.0), (2, 'g', 1.0), (4, 's', 1.0), (5, 'k', 0.7), (7, 'g', 1.0),
           (8, 'k', 0.85), (11, 'g', 1.0), (12, 's', 1.0), (13, 'k', 0.6), (15, 'g', 1.0)]
BREAK_C = [(0, 'k', 1.0), (3, 'g', 1.0), (4, 's', 1.0), (6, 'k', 0.8), (10, 'k', 0.9),
           (11, 'g', 1.0), (12, 's', 1.0), (14, 's', 0.5)]

def play_break(s, b, pat=None, gain=1.0, bus='drums', hats=True, swing=0.0,
               kick_gain=1.0, snare_gain=1.0, duck=True, seed=0):
    """One bar of breakbeat. Only the kicks register a sidechain trigger, so
    the pump follows the kick pattern rather than a grid that isn't there."""
    for st, what, g in (pat or BREAK_A):
        pos = st + (swing if st % 2 else 0.0)
        t = s.pos(b, pos)
        if what == 'k':
            if duck:
                s.hit(t)
            s.place(t, breakkick(seed=seed), gain * g * kick_gain, bus)
        elif what == 's':
            s.place(t, breaksnare(seed=seed), gain * g * snare_gain, bus)
        else:
            s.place(t, breaksnare(ghost=True, seed=seed + st), gain * g * 0.9, bus)
    if hats:
        for i in range(16):
            v = 0.5 if i % 2 else 0.28
            s.place(s.pos(b, i + (swing if i % 2 else 0.0)),
                    panned(breakhat(0.6), 0.35 if (i // 2) % 2 else -0.35),
                    gain * v * 0.8, bus)

# ---- the 1992 palette ----
@cached
def ravestab(root=50, dur_steps=3, gain=1.0, sweep=0.30, drive=2.2, seed=0):
    """Hoover and orchestra hit welded together: the detuned saw stack with a
    falling pitch sweep, plus the sampled-orchestra thud underneath it. Two
    records out of three in 1992 opened with this."""
    n, t = steps(dur_steps)
    f = midi(root)
    penv = 1 + sweep * np.exp(-t / 0.085)
    x = np.zeros(n)
    for d in (0.985, 0.993, 1.0, 1.007, 1.015):
        x += saw_ph(2 * np.pi * np.cumsum(f * d * penv) / SR, f * 1.4, kmax=40)
    x /= 5
    x += 0.45 * saw_ph(2 * np.pi * np.cumsum(f * 0.5 * penv) / SR, f * 0.8, kmax=40)
    hit = np.zeros(n)
    for off in (-12, 0, 3, 7, 12):
        hit += saw_ph(2 * np.pi * np.cumsum(np.full(n, midi(root + off))) / SR,
                      midi(root + off) * 1.2, kmax=24)
    hit = hit / 5 * np.exp(-t / 0.14)
    out = lp(stereo(np.tanh(drive * (x + 0.7 * hit) / 1.6)), 4200)
    out += 0.22 * hp(stereo(np.random.RandomState(seed + 701).randn(n)
                            * np.exp(-t / 0.02)), 2000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    env = np.exp(-t / 0.30) * adsr(n, a=0.004, r=0.04)
    return out * env[:, None] * gain * 0.5

@cached
def ravesiren(dur_steps=8, f0=520.0, lfo=2.4, gain=1.0, seed=0):
    """The siren that means the drop is coming. Square-ish LFO on the pitch so
    it warbles rather than glides."""
    n, t = steps(dur_steps)
    mod = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * lfo * t))
    f = f0 * (1 + 0.45 * mod)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.35 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    out = stereo(np.tanh(1.5 * x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0011))
    return out * adsr(n, a=0.02, r=0.15)[:, None] * gain * 0.4
