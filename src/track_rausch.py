"""RAUSCH - acid breakbeat at 138 BPM, D minor. 1992, more or less.

Rausch is German for the state of being high, and also for a rushing noise.
Both apply.

This is deliberately the opposite of Spirale and Saeure, and the difference
is not the tempo or the key - it is the grid. There is no kick on every beat.
A breakbeat states the pulse by leaving it out: the kick lands on 1, on the
'and' of 2, and wherever else it feels like, and the listener supplies the
rest. Ghost snares at a fifth of the velocity fill the gaps, and they are
inaudible as events while being the entire groove.

The 303 is still here, but it is one voice among several instead of the whole
record - because in 1992 the acid line shared the bar with hoovers, orchestra
hits, a piano playing major triads over a minor key, and a diva who had
wandered in from a different genre entirely.

    ANKUNFT | AUFBAU | ERSTER RAUSCH | ATEM | AUFBAU II | ZWEITER RAUSCH
            | TAUMEL | FINALE | ABGANG

192 bars, 5:34.
"""
import numpy as np
from ravelib import *

np.random.seed(1992)

# D minor: i - bVI - bIII - bVII, the loop every rave record was built on
PROG = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]
ROOTS = [38, 34, 41, 36]
STABN = [62, 58, 65, 60]                       # the hoover stab, up where it belongs

# the 303, in D
LINE = [(0, 38, 2, 1, 0), (2, 38, 1, 0, 0), (3, 50, 1.5, 0, 1), (5, 38, 1, 0, 0),
        (6, 41, 2, 0, 0), (8, 38, 2, 1, 0), (10, 45, 1, 0, 0), (11, 38, 1, 0, 0),
        (13, 48, 1.5, 0, 1), (15, 39, 1, 0, 0)]
LINE2 = [(0, 38, 1.5, 1, 0), (2, 45, 1, 0, 0), (3, 38, 1, 0, 0), (5, 50, 1.5, 1, 1),
         (7, 38, 1, 0, 0), (8, 41, 1.5, 0, 0), (10, 38, 1, 0, 0), (11, 48, 1, 0, 1),
         (13, 38, 1, 0, 0), (14, 45, 2, 1, 0)]
BREAKS = [BREAK_A, BREAK_B, BREAK_A, BREAK_C]

s = Session(192, tail=4.0)

def ch(b):   return [midi(n) for n in PROG[(b // 4) % 4]]
def root(b): return ROOTS[(b // 4) % 4]
def stab_n(b): return STABN[(b // 4) % 4]

def brk(b, gain=1.0, hats=True, pat=None, swing=0.06, lpf=None, kg=1.0, sg=1.0):
    if lpf is None:
        play_break(s, b, pat or BREAKS[b % 4], gain=gain, hats=hats, swing=swing,
                   kick_gain=kg, snare_gain=sg, seed=b % 4)
    else:
        sub = Session(2, tail=0.1)
        play_break(sub, 0, pat or BREAKS[b % 4], gain=gain, hats=hats, swing=swing,
                   kick_gain=kg, snare_gain=sg, seed=b % 4)
        s.place(s.pos(b), lp(sub.bus['drums'][:int(BAR)], lpf), 1.0, 'drums')
        for st, what, _ in (pat or BREAKS[b % 4]):
            if what == 'k':
                s.hit(s.pos(b, st))

def line(b0, bars, pat=None, knob=(0.5, 1.0), res=4.2, dec=0.16, drive=4.0,
         gain=1.0, f_hi=4800, hard=0.0, wave='saw'):
    p = poly_pattern(pat or LINE, 16, bars)
    kw = dict(f_lo=220, f_hi=f_hi, res=res, drive=drive, low=80, decay=dec,
              wave=wave, knob=knob)
    seg = acid_hard(p, bars, fold_amt=hard, bite=0.9, **kw) if hard else acid(p, dur_bars=bars, **kw)
    s.place(s.pos(b0), seg, gain, 'acid')

def stabs(b, gain=1.0, steps_=(0, 6), dur=3, sweep=0.30):
    for st in steps_:
        s.place(s.pos(b, st), ravestab(stab_n(b), dur, sweep=sweep, seed=b), gain, 'stab')

def keys(b, gain=1.0, steps_=(2, 6, 10, 14), dur=2):
    for st in steps_:
        s.place(s.pos(b, st), piano(ch(b), dur), gain, 'music')

def bass(b, gain=1.0, steps_=(0, 6, 10), dur=3):
    for st in steps_:
        s.place(s.pos(b, st), sub(midi(root(b) - 12), dur), gain, 'bass')

# ================= ANKUNFT: 0-15 =================
s.place(s.pos(0), pad(ch(0), 64, cutoff=1400, gain=0.30, wide=1.2), 1.0, 'pad')
s.place(s.pos(4), pad(ch(4), 64, cutoff=1600, gain=0.30, wide=1.2), 1.0, 'pad')
s.place(s.pos(0), crackle(64, gain=0.5), 1.0, 'air')
for b in range(4, 16):
    brk(b, gain=0.42 + 0.34 * ((b - 4) / 11), hats=b >= 8,
        lpf=500 + 420 * (b - 4) if b < 13 else None)
s.place(s.pos(8), ravesiren(16, f0=430, lfo=1.8, gain=0.5), 1.0, 'fx')
s.place(s.pos(12), pad(ch(12), 32, cutoff=2200, gain=0.34, wide=1.4), 1.0, 'pad')
s.place(s.pos(15, 8), reverse_crash(8, gain=0.6), 1.0, 'fx')

# ================= AUFBAU: 16-31 =================
for b in range(16, 32):
    brk(b, gain=0.85, kg=1.0, sg=0.95)
    bass(b, gain=0.5 if b < 24 else 0.62)
    if b >= 20:
        s.place(s.pos(b), pad(ch(b), 16, cutoff=2600, gain=0.26), 1.0, 'pad')
line(16, 8, knob=(0.20, 0.46), res=3.4, dec=0.20, drive=3.6, f_hi=3400, gain=0.62)
line(24, 8, knob=(0.44, 0.74), res=3.8, dec=0.18, drive=3.8, f_hi=4000, gain=0.80)
s.place(s.pos(28), ravesiren(16, f0=520, lfo=2.4, gain=0.55), 1.0, 'fx')
s.place(s.pos(31), riser(16, gain=0.8, f0=180, f1=1600), 1.0, 'fx')

# ================= ERSTER RAUSCH: 32-63 =================
for b in range(32, 64):
    ph = b - 32
    brk(b, gain=1.0)
    bass(b, gain=0.72)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(18, gain=0.4), 1.0, 'drums')
    if ph >= 8:
        stabs(b, gain=0.62, steps_=(0, 6) if ph % 2 == 0 else (0,))
    if ph >= 16:
        s.place(s.pos(b), pad(ch(b), 16, cutoff=3200, gain=0.24), 1.0, 'pad')
line(32, 16, knob=(0.70, 1.0, 0.78, 0.96), res=4.2, dec=0.16, drive=4.0, f_hi=4800)
line(48, 16, pat=LINE2, knob=(0.86, 0.62, 1.0, 0.80), res=4.4, dec=0.15, drive=4.2,
     f_hi=5200)
s.place(s.pos(40), orchhit(50, 3, gain=0.5), 1.0, 'stab')
s.place(s.pos(56), orchhit(53, 3, gain=0.5), 1.0, 'stab')
s.place(s.pos(63, 8), whoosh(8, gain=0.75), 1.0, 'fx')

# ================= ATEM: 64-79 =================
# Drums out. Piano and a diva, both of them in the wrong genre, which is
# exactly what a 1992 breakdown was for.
s.place(s.pos(64), downlifter(16, gain=0.8), 1.0, 'fx')
for b in range(64, 80, 4):
    s.place(s.pos(b), pad(ch(b), 64, cutoff=2400, gain=0.42, wide=1.6), 1.0, 'pad')
for b in range(64, 76):
    keys(b, gain=0.30 if b < 70 else 0.40, steps_=(2, 6, 10, 14))
for b, note, ln in ((66, 69, 8), (69, 72, 6), (72, 74, 8), (75, 69, 10)):
    s.place(s.pos(b, 4), reverb(diva(midi(note), ln, gain=0.5), decay=3.6, wet=0.5,
                                tone=5200), 0.7, 'music')
line(64, 12, knob=(0.30, 0.70, 0.44), res=4.6, dec=0.20, drive=3.4, f_hi=4400,
     gain=0.55)
for b in range(76, 80):
    brk(b, gain=0.5 + 0.14 * (b - 76), hats=b >= 78, sg=0.8)
    bass(b, gain=0.5)
s.place(s.pos(76), riser(64, gain=0.9, f0=160, f1=1900), 1.0, 'fx')
s.place(s.pos(79, 8), reverse_crash(8, gain=0.9), 1.0, 'fx')

# ================= AUFBAU II: 80-95 =================
for b in range(80, 96):
    ph = b - 80
    brk(b, gain=0.92 + 0.08 * (ph / 15))
    bass(b, gain=0.72)
    keys(b, gain=0.26, steps_=(2, 10))
    if ph >= 8:
        stabs(b, gain=0.55, steps_=(6,))
line(80, 16, knob=(0.56, 0.88, 0.70, 1.0), res=4.4, dec=0.16, drive=4.2, f_hi=5000)
s.place(s.pos(88), ravesiren(16, f0=560, lfo=3.0, gain=0.5), 1.0, 'fx')
s.place(s.pos(94), riser(32, gain=0.95, f0=170, f1=2000), 1.0, 'fx')
s.place(s.pos(95, 12), reverse_crash(4, gain=0.95), 1.0, 'fx')

# ================= ZWEITER RAUSCH: 96-127 =================
for b in range(96, 128):
    ph = b - 96
    brk(b, gain=1.0)
    bass(b, gain=0.78)
    stabs(b, gain=0.70, steps_=(0, 6) if ph % 2 == 0 else (0, 11))
    keys(b, gain=0.28, steps_=(2, 6, 10, 14))
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(18, gain=0.42), 1.0, 'drums')
    if ph >= 16:
        s.place(s.pos(b), pad(ch(b), 16, cutoff=3600, gain=0.24), 1.0, 'pad')
line(96,  16, pat=LINE2, knob=(0.80, 1.0, 0.66, 0.94), res=4.6, dec=0.15, drive=4.4,
     f_hi=5400, hard=0.28)
line(112, 16, knob=(0.92, 0.70, 1.0, 0.86), res=4.8, dec=0.14, drive=4.6, f_hi=5800,
     hard=0.34)
for b in (100, 108, 116, 124):
    s.place(s.pos(b), orchhit(PROG[(b // 4) % 4][0], 3, gain=0.55), 1.0, 'stab')
for b, note in ((104, 74), (120, 77)):
    s.place(s.pos(b, 8), reverb(diva(midi(note), 6, gain=0.45), decay=3.0, wet=0.4),
            0.6, 'music')
s.place(s.pos(127, 8), whoosh(8, gain=0.8), 1.0, 'fx')

# ================= TAUMEL: 128-143 =================
s.place(s.pos(128), downlifter(14, gain=0.8), 1.0, 'fx')
for b in range(128, 144, 4):
    s.place(s.pos(b), pad(ch(b), 64, cutoff=2000, gain=0.40, wide=1.6), 1.0, 'pad')
line(128, 12, pat=LINE2, knob=(0.24, 0.86, 0.50, 1.0), res=4.8, dec=0.19, drive=3.8,
     f_hi=5200, gain=0.75)
for b in range(128, 138):
    keys(b, gain=0.34, steps_=(0, 6, 10))
for b, note in ((130, 72), (134, 76)):
    s.place(s.pos(b, 4), reverb(diva(midi(note), 8, gain=0.5), decay=4.0, wet=0.55),
            0.68, 'music')
s.place(s.pos(133), ravesiren(24, f0=480, lfo=2.0, gain=0.5), 1.0, 'fx')
for b in range(138, 144):
    brk(b, gain=0.62 + 0.08 * (b - 138), hats=b >= 140, sg=0.85)
    bass(b, gain=0.6)
    if b >= 141:
        stabs(b, gain=0.5, steps_=(0,))
s.place(s.pos(140), riser(64, gain=1.0, f0=150, f1=2100), 1.0, 'fx')
s.place(s.pos(143, 12), reverse_crash(4, gain=1.0), 1.0, 'fx')

# ================= FINALE: 144-183 =================
for b in range(144, 184):
    ph = b - 144
    pat = BREAK_C if ph % 8 == 7 else None
    brk(b, gain=1.0, pat=pat)
    bass(b, gain=0.82, steps_=(0, 6, 10, 14) if ph % 4 == 3 else (0, 6, 10))
    stabs(b, gain=0.78, steps_=(0, 6) if ph % 2 == 0 else (0, 11), sweep=0.34)
    keys(b, gain=0.30, steps_=(2, 6, 10, 14))
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(18, gain=0.45), 1.0, 'drums')
line(144, 16, knob=(0.90, 1.0, 0.74, 1.0), res=4.8, dec=0.15, drive=4.6, f_hi=6000,
     hard=0.38)
line(160, 16, pat=LINE2, knob=(1.0, 0.76, 1.0, 0.88), res=5.0, dec=0.13, drive=4.8,
     f_hi=6400, hard=0.44)
line(176, 8,  knob=(0.94, 1.0), res=4.8, dec=0.15, drive=4.6, f_hi=6200, hard=0.40)
for b in (148, 156, 164, 172, 180):
    s.place(s.pos(b), orchhit(PROG[(b // 4) % 4][0], 3, gain=0.6), 1.0, 'stab')
for b, note in ((152, 77), (168, 81), (178, 74)):
    s.place(s.pos(b, 8), reverb(diva(midi(note), 6, gain=0.5), decay=3.2, wet=0.45),
            0.66, 'music')
for b in (160, 176):
    s.place(s.pos(b), ravesiren(16, f0=600, lfo=3.4, gain=0.45), 1.0, 'fx')
s.place(s.pos(183, 8), whoosh(8, gain=0.8), 1.0, 'fx')

# ================= ABGANG: 184-191 =================
for b in range(184, 192):
    ph = b - 184
    u = ph / 7
    brk(b, gain=0.9 - 0.7 * u, hats=ph < 5, lpf=6000 - 700 * ph if ph >= 2 else None)
    if ph < 4:
        bass(b, gain=0.7 - 0.15 * ph)
        stabs(b, gain=0.5 - 0.12 * ph, steps_=(0,))
    if ph < 6:
        s.place(s.pos(b), pad(ch(b), 16, cutoff=2400 - 300 * ph, gain=0.30), 1.0, 'pad')
line(184, 6, knob=(0.80, 0.12), res=4.4, dec=0.18, drive=4.0, f_hi=4600, gain=0.7)
s.place(s.pos(184), crackle(64, gain=0.45), 1.0, 'air')
s.place(s.pos(191), downlifter(16, gain=0.6), 1.0, 'fx')

# ---- bus space, then the master ----
Session.DUCKED = dict(Session.DUCKED, acid=0.4, stab=0.45, bass=1.0, pad=0.7,
                      music=0.5)
s.bus['stab'] = bus_reverb(s.bus['stab'], decay=1.6, wet=0.22, tone=4600)
s.bus['music'] = bus_reverb(s.bus['music'], decay=2.4, wet=0.26, tone=5000)
s.bus['pad'] = bus_reverb(s.bus['pad'], decay=3.2, wet=0.30, tone=4200)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=3.0, wet=0.30, tone=4000)
s.bus['drums'] = bus_reverb(s.bus['drums'], decay=0.55, wet=0.13, tone=5200)
s.bus['acid'] = autopan(s.bus['acid'], cycle_bars=11.0, depth=0.26, phase=1.1)
s.bus['pad'] = hp(s.bus['pad'], 200)
s.bus['stab'] = hp(s.bus['stab'], 110)
s.bus['drums'] = softclip(s.bus['drums'], 1.2, knee=0.85)
# a broad cut through the fatigue zone: this kit is all snare and hat, and
# 11% of the mix was sitting in 2-4 kHz against 1.7% on the other records
s.bus['drums'] = peak_eq(s.bus['drums'], 3000, -3.0, width=0.5)
s.bus['drums'] = peak_eq(s.bus['drums'], 5000, -1.2, width=0.4)
for b in ('drums', 'music', 'fx', 'pad'):
    s.bus[b] = shelf(s.bus[b], 9000, -2.5)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 140)

GAINS = {'drums': 0.78, 'bass': 0.46, 'acid': 0.60, 'stab': 1.15, 'music': 1.00,
         'pad': 0.95, 'air': 0.60, 'fx': 0.46}
s.report(GAINS)
s.render('acid_rausch_138.wav', drive=1.0, duck=0.22, clip=1.10, limit=0.94,
         peak=0.95, fade=2.5, gains=GAINS)
