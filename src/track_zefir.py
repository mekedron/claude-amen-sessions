"""ZEFIR - light club house at 120 BPM, E major with a Lydian fourth.

The companion to `barhat`, and deliberately its opposite in every dimension
except the discipline. That record is velvet and midnight; this one is the
west wind - the same room four hours earlier, with the doors open.

Same two pitched instruments and no third. A bass and a GUITAR, one harmonic
voice, no pad and no lead ([[minimal-means-fewer-voices]]). What differs:

  KEY       E major, four sharps, as far from G Dorian as the circle goes
            without leaving the neighbourhood. The two records share two
            notes out of seven, so this is a different set of pitches rather
            than a transposition of the same one.
  MODE      major, and lifted. The IV chord carries its #11 - D#, which is
            the leading tone of E and therefore already in the key, so the
            Lydian sky costs nothing and borrows nothing.
  MELODY    `barhat` pedals one note on top of four chords. This one moves:
            B4 - C#5 - D#5 - C#5, an arch, and the D# at the top of it is
            that #11. The tune is in the top voice of the harmony instrument,
            which is the only place a record with no lead can put one.
  HAND      the same guitar, fingerpicked. `barhat` is a plectrum crossing
            four strings; this is broken chords, one note at a time, with the
            chord itself struck only once every four bars. A different right
            hand is a different instrument, and it costs no new voice.
  SHAPE     two short breaths at 80 and 104 instead of one long breakdown.
            Nothing here is meant to be dramatic.

    Emaj9  ->  C#m9  ->  Amaj9(#11)  ->  F#m11        I - vi - IV - ii

Every voice arches with the melody: all four rise across the first half of the
loop and fall across the second. Two of the four changes move one or two
voices and no more.

THE BAND BUDGET IS DECIDED HERE, NOT AT THE MIX.

Sections differ in WHICH BANDS THEY USE, not only in how loud they are, and
every band is empty somewhere in the record
(`theory/00-foundations/20-spectral-arrangement.md`):

    band       OPEN AIR FLOOR SWIM WIDE SUN HOLD DRIFT DIP PEAK EASE OUT
    20-60       -    -    x    x    x    x   -    x     -   X    x    -
    60-120      -    -    x    X    X    X   -    X     -   X    X    x
    120-800     x    x    x    x    x    x   x    x     x   X    x    x
    800-2.5k    x    x    x    x    X    X   x    X     x   X    X    x
    2.5-6k      -    x    x    x    x    X   -    x     -   X    x    x
    6-12k       -    -    x    x    x    X   -    x     -   X    x    -
    12k+        -    -    -    -    x    x   -    x     -   X    -    -

The bottom two octaves are absent for the first sixteen bars, absent through
both breaths, and absent again for the four bars before the peak. They are not
turned down there - the kick and the bass do not play. That is why bar 108
arrives, and it is a thing a gain ride cannot do.

    OPEN (8) | AIR (8) | FLOOR (16) | SWIM (16) | WIDE (16) | SUN (16)
    | HOLD (8) | DRIFT (16) | DIP (4) | ZEFIR (32) | EASE (12) | OUT (8)

160 bars, 5:20. The peak starts at 108 - 67% of the way in - and the four bars
in front of it have no bottom and no top.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
import houselib
from houselib import *

BAR, STEP = houselib.set_tempo(120)
houselib.SWING = 0.070

np.random.seed(1200)
rs = np.random.RandomState(1200)

# ============================================================== material ===
# E major: E F# G# A B C# D#. Roots leap up once and then walk home.
ROOTS = [28, 37, 33, 30]                       # E1  C#2  A1  F#1

# The comp. Four notes, and read the last column down: B4 C#5 D#5 C#5 - the
# tune, and the D# is the #11 of the A chord underneath it.
#   Emaj9      D#3 F#3 G#3 B3    maj7  9   3    5
#   C#m9       E3  G#3 B3  C#4   b3    5   b7   root
#   Amaj9#11   E3  G#3 C#4 D#4   5     maj7 3    #11
#   F#m11      E3  F#3 B3  C#4   b7    root 11   5
COMP = [(51, 54, 56, 59),
        (52, 56, 59, 61),
        (52, 56, 61, 63),
        (52, 54, 59, 61)]

RIM_HI, RIM_LO = 85, 80
BON_M, BON_H = 75, 68


# ================================================================= bass ===
# Three notes and two long holes. The fifth on the last offbeat rings past the
# bar line into the next chord, because `hbass` renders six steps of overhang.
def bassbar(root, sparse=False):
    if sparse:
        return [(0, root, 5.4, 0, 0, 1.00), (10, root + 7, 4.2, 0, 0, 0.66)]
    return [(0,  root,      3.6, 0, 0, 1.00),
            (6,  root + 12, 2.0, 0, 0, 0.66),
            (8,  root,      2.4, 0, 0, 0.82),
            (14, root + 7,  3.4, 0, 0, 0.66)]

BASS = [bassbar(r) for r in ROOTS]
BASS_SPARSE = [bassbar(r, sparse=True) for r in ROOTS]


# ============================================================ the picking ===
# (step, which voice of the chord, velocity). One note at a time: the chord is
# implied by the order the fingers arrive in rather than stated. Voice 3 is the
# top - the tune - so it lands where the ear is already listening, and it is
# given a longer decay than the notes underneath it.
PICK = {
    1: [(2, 1, 0.52), (6, 3, 0.60), (12, 0, 0.44)],
    2: [(0, 0, 0.50), (3, 2, 0.44), (6, 3, 0.62), (11, 1, 0.46)],
    3: [(0, 0, 0.52), (2, 2, 0.44), (6, 3, 0.64), (8, 1, 0.46), (14, 3, 0.50)],
    4: [(0, 0, 0.54), (2, 2, 0.44), (4, 1, 0.40), (6, 3, 0.66),
        (8, 2, 0.44), (11, 1, 0.42), (14, 3, 0.54)],
}

def picks(level, b):
    """the bar's notes - and, one bar in eight, none at all"""
    if b % 8 == 6 and level <= 3:
        return []
    return PICK[level]


# ============================================================== sections ===
# (bar, name, picking level, amp tone, velocity scale, ring, open hats,
#  tambourine, percussion tier)
SEC = [(0,   'OPEN',  1, 3000, 0.66, 1, 0, 0, 0),
       (8,   'AIR',   2, 3300, 0.74, 1, 0, 0, 1),
       (16,  'FLOOR', 2, 3600, 0.84, 1, 2, 0, 1),
       (32,  'SWIM',  3, 3900, 0.92, 1, 2, 0, 2),
       (48,  'WIDE',  3, 4300, 1.00, 1, 2, 1, 2),
       (64,  'SUN',   4, 4800, 1.08, 1, 2, 1, 3),
       (80,  'HOLD',  1, 3500, 0.70, 1, 0, 0, 0),
       (88,  'DRIFT', 3, 4400, 1.02, 0, 2, 1, 2),
       (104, 'DIP',   1, 3600, 0.72, 1, 0, 0, 0),
       (108, 'ZEFIR', 4, 5300, 1.16, 1, 2, 2, 3),
       (140, 'EASE',  3, 4200, 1.00, 1, 2, 1, 2),
       (152, 'OUT',   2, 3500, 0.80, 1, 0, 0, 1)]

def sec(b):
    cur = SEC[0]
    for row in SEC:
        if b >= row[0]:
            cur = row
    return cur

# The gain ride, in decibels per bar, with a dip immediately before every
# arrival rather than a climb into it ([[section-contrast-belongs-in-level]]).
ARC = [(0, -9.2), (4, -8.2), (7.5, -8.8), (8, -7.4), (12, -7.0),
       (15.5, -9.6), (16, -6.2), (24, -5.4),
       (31.5, -6.8), (32, -4.0), (40, -3.6),
       (47.5, -4.6), (48, -2.8), (56, -2.5),
       (63.5, -3.4), (64, -1.6), (72, -1.4),
       (79.5, -1.8), (80, -6.2), (84, -5.6),
       (87.5, -6.4), (88, -3.2), (96, -2.6),
       (103.5, -3.2), (104, -5.4), (107.0, -6.6), (107.9, -6.6),
       (108, 0.0), (124, 0.0), (136, -0.4),
       (139.5, -1.0), (140, -2.8), (148, -3.2),
       (151.5, -3.8), (152, -6.4), (156, -8.4), (160, -12.5)]


# ================================================================ render ===
NB = 160
S = Session(NB, tail=4.0)
P = S.pos

def jit(ms=4.0):
    """a few milliseconds of humanisation. Never on the kick and never on the
    sub: the pulse is the one thing the body is counting."""
    return int(rs.normal(0, ms / 1000.0 * SR))


for b in range(NB):
    _, name, LVL, TONE, GV, RING, NOPEN, TAM, PERC = sec(b)
    ci = b % 4
    V = COMP[ci]

    # The bottom two octaves are a section-level decision, not a fader move.
    low_on  = (16 <= b < 80) or (88 <= b < 104) or (b >= 108)
    bass_on = (32 <= b < 80) or (88 <= b < 104) or (108 <= b < 156)
    hat_on  = (8 <= b < 80) or (88 <= b < 104) or (108 <= b < 152)
    clap_on = (32 <= b < 80) or (92 <= b < 104) or (108 <= b < 148)
    sparse  = (88 <= b < 92) or (b >= 148)
    opens   = (2, 10) if NOPEN else ()

    # ---- the floor -------------------------------------------------------
    if low_on:
        for st in (0, 4, 8, 12):
            t = P(b, st)
            S.hit(t)                                   # the sidechain trigger
            S.place(t, hkick(decay=0.166, sub=0.62, body=1.14),
                    0.78 if st in (0, 8) else 0.72, 'drums')
    if clap_on:
        for st in (4, 12):
            t = P(b, st) + jit(3)
            S.place(t, hclap(seed=(b + st) % 6), 1.00, 'drums')
            S.place(t, hsnare(seed=(b + st) % 4), 0.74, 'drums')
    if hat_on:
        for st in (2, 6, 10, 14):
            if st not in opens:
                S.place(P(b, sw(st)) + jit(3), hhat(tone=0.86, seed=(b * 4 + st) % 11),
                        1.02 if st in (6, 14) else 0.84, 'hats')
    for st in opens:
        S.place(P(b, sw(st)) + jit(3), hhat(open_=True, tone=0.90, seed=(b + st) % 9),
                1.26, 'hats')

    # ---- the box: one thing at a time, and a bar off in eight -------------
    quiet_bar = (b % 8 == 7)
    if PERC >= 1 and not quiet_bar:
        S.place(P(b, sw(11)) + jit(4), rimtick(note=RIM_HI, seed=b % 7),
                1.00, 'perc')
        if b % 4 == 2:
            S.place(P(b, sw(15)) + jit(4), rimtick(note=RIM_LO, seed=(b + 3) % 7),
                    0.70, 'perc')
    if PERC >= 2 and not quiet_bar:
        pat = (((3, BON_M, 'open', 0.54), (13, BON_H, 'open', 0.42))
               if b % 2 == 0 else
               ((7, BON_H, 'tip', 0.40), (11, BON_M, 'open', 0.48)))
        for st, nt, stk, v in pat:
            S.place(P(b, sw(st)) + jit(5),
                    bongo(nt, stk, vel=v, seed=(b * 3 + st) % 9), 0.62, 'perc')
    if TAM and b % 4 == 1:
        pat = ((14, 0.60),) if TAM < 2 else ((6, 0.58), (14, 0.48))
        for st, v in pat:
            S.place(P(b, sw(st)) + jit(4), tamb(seed=(b + st) % 8), v, 'perc')

    # ---- the bass --------------------------------------------------------
    if bass_on:
        pat = (BASS_SPARSE if sparse else BASS)[ci]
        S.place(P(b), hbass(tuple(pat), f_hi=2750.0, drive=1.90, res=0.80,
                            hold=0.22, decay=0.50, sub=0.58, tail_steps=6.0),
                0.62 if sparse else 0.74, 'bass')

    # ---- the guitar: fingers, not a plectrum -----------------------------
    # Single notes, so `strum` does nothing and there is no plectrum click to
    # speak of - a fingertip is softer and rounder than a pick, and `bright`
    # is what that costs. The top voice rings twice as long as the ones under
    # it, because it is carrying the tune.
    for st, vi, v in picks(LVL, b):
        vel = round(min(v * GV, 1.0), 2)
        top = (vi == 3)
        S.place(P(b, sw(st)) + jit(5),
                gtr((V[vi],), 7.0 if top else 4.0, vel=vel,
                    decay=0.85 if top else 0.46, damp=0.038, tone=TONE,
                    bright=0.55, res_hz=2300.0, presence=0.70, chorus=0.30,
                    tight=132.0, cone=0.68, warm=1.18, tilt_base=0.05,
                    take=b % 3),
                0.28, 'gtr')
    if RING and ci == 0:
        S.place(P(b, 0) + jit(4),
                gtr(V, 15.0, vel=round(min(0.46 * GV, 1.0), 2), decay=1.45,
                    damp=0.026, tone=TONE * 0.84, strum=0.0115, chorus=0.50,
                    res_hz=2300.0, presence=0.70, pick=0.28, pickup=0.19,
                    tight=110.0, cone=0.78, warm=1.18, tilt_base=0.02,
                    take=(b // 4) % 3),
                0.62, 'gtr')

print('  floor, box, bass and the picking placed')

# ---- seams ---------------------------------------------------------------
for b in (7, 15, 31, 47, 63, 79, 87, 103, 107, 139, 151):
    S.place(P(b, 12), whoosh(4, gain=0.28, rev_=True), 0.44, 'air')
for b, v in ((79, 0.56), (107, 0.50)):
    throw(S, P(b, 14),
          gtr(COMP[b % 4], 6.0, vel=0.58, decay=0.60, damp=0.042, tone=5200,
              tight=140.0),
          gain=v, steps_=3.0, times=6, fb=0.55)


# ================================================================== mix ===
S.bus['drums'] = squash(S.bus['drums'], thresh=0.44, ratio=2.6, attack=0.016,
                        release=0.125, mix=0.80, report='drums')
S.bus['perc'] = squash(S.bus['perc'], thresh=0.15, ratio=3.4, attack=0.008,
                       release=0.125, mix=0.66, report='perc')
S.bus['perc'] = softclip(S.bus['perc'], 0.85, knee=0.55)
S.bus['gtr'] = squash(S.bus['gtr'], thresh=0.22, ratio=2.4, attack=0.012,
                      release=0.148, mix=0.62, report='gtr')

# A picked note has its whole identity in the first 40 ms and its body in
# 300-800 Hz, so the same wide subtractive bell that stopped `barhat` sitting
# on the floor applies here, and a little harder: this record is meant to
# float and that band is what weighs it down.
S.bus['gtr'] = S.bus['gtr'] - 0.24 * bandpass(S.bus['gtr'], 300, 700, order=2)
S.bus['gtr'] = bus_reverb(S.bus['gtr'], decay=3.8, wet=0.48, tone=3800)
S.bus['perc'] = bus_reverb(S.bus['perc'], decay=0.58, wet=0.10, tone=6200)
S.bus['hats'] = bus_reverb(S.bus['hats'], decay=0.40, wet=0.07, tone=8000)
S.bus['hats'] = narrow(S.bus['hats'], 0.62)
S.bus['air'] = bus_reverb(S.bus['air'], decay=3.4, wet=0.34, tone=4600)
for k in ('gtr', 'air'):
    S.bus[k] = mono_below(S.bus[k], 170)
S.bus['air'] = narrow(S.bus['air'], 0.70)
S.bus['gtr'] = narrow(S.bus['gtr'], 0.74)

# ---- the ride ------------------------------------------------------------
t_bars = np.arange(S.total) / BAR
db = np.interp(t_bars, [p[0] for p in ARC], [p[1] for p in ARC])
ride = uniform_filter1d(10 ** (db / 20.0), int(0.030 * SR)).astype(np.float32)
for k in S.bus:
    S.bus[k] = S.bus[k] * ride[:, None]
print(f'  ride: {db.min():.1f} to {db.max():.1f} dB across {NB} bars')

GAINS = {'drums': 0.58, 'perc': 3.10, 'bass': 0.72, 'gtr': 1.20,
         'hats': 3.30, 'air': 1.85}

S.report(GAINS)
S.render('house_zefir_120.wav', drive=0.0, duck=0.66, duck_rel=0.20,
         clip=1.18, peak=0.89, fade=2.8, gains=GAINS,
         brick=dict(gain=1.08, ceiling=0.90))
