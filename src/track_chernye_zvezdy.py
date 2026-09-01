"""ЧЁРНЫЕ ЗВЁЗДЫ - darkstep at 174, G Phrygian, and the stars are going out.

The brief: a very distant cyberpunk dystopia, people dying in numbers,
something enormous coming, the universe closing on itself. Black stars.
Hopelessness, rot, the abyss, the future. Cyber implants, cars, spaceflight.

So the record is not angry. Angry is a small feeling and this is a large
one - the thing arriving does not care, and the drums are what is left of a
civilisation that built machines better than it built anything else.

    THE KEY IS PHRYGIAN AND THE BASS BARELY MOVES. G1 = 49 Hz, and the
    second degree is Ab - a semitone above the root. The bass spends most of
    the record on one note; when it moves it moves by a semitone to that Ab,
    or it falls to Eb1 and the floor is simply lower than it was. Nothing
    modulates and nothing resolves: there is no cadence anywhere on this
    record, because a cadence is a promise.

    THE ARRANGEMENT IS SUBTRACTION, THREE TIMES OVER. Three drops, and the
    second is not the first plus a layer - it is the same machine with its
    panels off. Between them, КОЛЛАПС at bar 144: halftime, where the tempo
    does not change and the feeling of it halves.

THE BASS IS THE RECORD AND EVERYTHING ELSE GETS OUT OF ITS WAY

`src/voidlib.py` is the kit, written for this track. Its bass is built the
way the genre is actually played - as a modern wavetable synth:

    one wavetable, three unison voices 19 cents apart, read through WARP
    (the phase bent, pulse-width-shifted, hard synced, phase-modulated and
    quantised before the wave is read) -> a resonant 12 dB/octave ladder
    WHOSE CUTOFF LIVES BETWEEN 140 AND 1800 Hz -> heavy asymmetric
    distortion, which is where the top half of the spectrum comes from ->
    a compressor -> a lowpass at 7.5 kHz.

    Underneath it, and taking no part in any of that: a locked sine at the
    note. The mids swirl and the low end does not move.

That chain is measured against `samples/reese_witch_a1_56hz.wav` and lands
within about 2 dB of it from 800 Hz to 4 kHz, and within 3 dB of its band
balance. The two things that decide whether this is a bass or a squeal are
in that paragraph: the cutoff range, and the fact that all the brightness
above the cutoff is a CONSEQUENCE of distortion rather than a layer sitting
two octaves up.

And nothing else is allowed a noise bed. There are no rides, no cymbal
wash, no sheet of high noise anywhere the bass is playing; the hats are
eighths at -19 dB and go to sixteenths only where the bass is at its
sparsest. A record whose top end is full of hiss has no room left for a
bass whose whole character is a filter moving through the mids.

    kick   0, 10        two-step, the second one late
    kick   0, 6, 11     three, uneven
    kick   0, 3, 10     the early one
    snare  4, 12        never moves. It is the only thing on the record
                        that never moves.

Rendered by `python3 src/track_chernye_zvezdy.py`.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from scipy.ndimage import uniform_filter1d

import voidlib as V
from voidlib import *                                          # noqa: F401,F403

BAR, STEP = V.set_tempo(174.0)
NB = 224
P = lambda b, s=0.0: int(round(b * BAR + s * STEP))

S = Session(NB, tail=3.0)
S.DUCKED = {'sub': 1.0, 'bass': 0.45, 'void': 0.35, 'lead': 0.30}

# ================================================================ material =
# G Phrygian: G Ab Bb C Db D Eb F.
R = 31                                    # G1 = 49 Hz
b2, b3, P4, b5, P5, b6, b7 = 32, 34, 36, 37, 38, 39, 41
LOW6, LOW7 = 27, 29                       # Eb1, F1 - the floor giving way
KT = 49.0

PAT = {
    'a': dict(k=(0, 10),      s=(4, 12), g=(2, 7, 14),     o=(14,), p=()),
    'b': dict(k=(0, 6, 11),   s=(4, 12), g=(2, 9, 15),     o=(),    p=(6,)),
    'c': dict(k=(0, 3, 10),   s=(4, 12), g=(6, 9, 14),     o=(14,), p=()),
    'd': dict(k=(0, 10, 14),  s=(4, 12), g=(2, 6, 9),      o=(),    p=(11,)),
    'e': dict(k=(0, 8, 11),   s=(4, 12), g=(2, 6, 14, 15), o=(6,),  p=()),
    'f': dict(k=(0, 7, 10),   s=(4, 12), g=(3, 9, 13),     o=(14,), p=(2,)),
    'g': dict(k=(0, 10),      s=(4, 12, 14), g=(2, 6, 9),  o=(),    p=(6,)),
    'h': dict(k=(0, 11),      s=(4, 12), g=(2, 5, 9, 14),  o=(6, 14), p=()),
    # halftime, and the kick stays on 1 and 3
    'ht': dict(k=(0, 8),      s=(8,),    g=(4, 12, 14),    o=(),    p=(0,)),
    'hb': dict(k=(0, 8, 11),  s=(8,),    g=(4, 12, 6),     o=(14,), p=(8,)),
}
ROT = 'abcadbceafbdagch'


def beat(b, key, e=1.0, hats=1.0, gh=1.0, kg=1.0, sg=1.0, plates=1.0,
         hstep=2, duck=True, bus='drums'):
    """One bar of the kit. `hstep` is the hi-hat subdivision: 2 is eighths
    and it is the default, because sixteenths of noise across a whole record
    is a hiss bed the bass has to compete with."""
    p = PAT[key]
    for st in p['k']:
        sd = (b * 16 + st) % 89
        g = kg * (1.0 if st == 0 else 0.88 + 0.06 * ((b + st) % 3))
        S.place(P(b, st), V.kick(2.4, tune=KT, seed=sd, gain=0.92), e * g, bus)
        if duck:
            S.hit(P(b, st))
    for st in p['s']:
        sd = (b * 16 + st) % 83
        g = sg * (1.0 if st in (4, 12) else 0.62)
        S.place(P(b, st), V.snare(3.2, seed=sd, gain=0.80,
                                  crack=1.0 + 0.08 * ((b + st) % 3)), e * g, bus)
    if gh:
        for st in p['g']:
            S.place(P(b, st), V.ghost(1.0, seed=(b * 16 + st) % 71,
                                      tone=0.9 + 0.25 * ((b + st) % 3)),
                    e * gh * (0.30 + 0.10 * ((b * 3 + st) % 4)), 'perc')
    if hats:
        for st in range(0, 16, hstep):
            if st in p['o'] or (b * 16 + st) % 11 == 5:
                continue
            v = (1.00, 0.44, 0.68, 0.42)[(st // hstep) % 4]
            S.place(P(b, st), V.chat(0.8, seed=(b * 16 + st) % 67,
                                     tone=0.94 + 0.12 * (st % 3),
                                     decay=0.016 + 0.005 * (st % 2)),
                    e * hats * v * 0.5, 'hats')
        for st in p['o']:
            S.place(P(b, st), V.ohat(3.0, seed=(b * 16 + st) % 61),
                    e * hats * 0.45, 'hats')
    if plates:
        for st in p['p']:
            S.place(P(b, st), V.plate(2.0, seed=(b * 16 + st) % 53,
                                      lo=2300 + 400 * (st % 3), decay=0.075),
                    e * plates * 0.40, 'perc')


def fill(b, kind='roll', e=1.0):
    if kind == 'roll':
        for j, st in enumerate((12, 13, 14, 15)):
            S.place(P(b, st), V.ghost(1.0, seed=(b * 16 + st) % 71, tone=1.1),
                    e * (0.30 + 0.16 * j), 'perc')
        S.place(P(b, 15), V.snare(2.0, seed=(b * 7) % 83, gain=0.7, crack=1.15),
                e * 0.55, 'drums')
    elif kind == 'metal':
        for j, st in enumerate((10, 13, 15)):
            S.place(P(b, st), V.plate(2.0, seed=(b * 5 + st) % 53,
                                      lo=2600 + 900 * j, decay=0.06),
                    e * (0.32 + 0.11 * j), 'perc')


def swell(b, steps_=6, gain=0.55, seed=0, lo=900.0, hi=9000.0):
    seg = V.rev(steps_, seed=seed, lo=lo, hi=hi)
    S.place(P(b) - len(seg), seg, gain, 'fx')


# ---- the bass ------------------------------------------------------------
# One entry is TWO BARS: four gestures, half a bar each, and the notes
# underneath them. Two rules hold across all sixty-four of them.
#
#   No two rows are in the same order. An exact restatement of a two-bar
#   timbre figure is the same two seconds of noise again, and at 174 that
#   arrives eight times in sixteen bars.
#
#   Every row contains at least one DARK gesture - draw, still, sink, half,
#   talk, gap. A cell made of four bright ones measures 24% of its energy
#   in 800-3000 Hz and 4% under 120: the bass loses its bottom at exactly
#   the moment it is supposed to be at its most violent.
#
# The escalation across the record is in the MIX of the vocabulary, not in
# the level: drop 1 is three mid gestures against one dark, drop 2 puts a
# hot one in every cell, drop 3 puts two.
DROP1 = [
    (('draw',  'chew',  'lock',  'sink'),  [(0, R)]),
    (('roll',  'talk',  'chew',  'draw'),  [(0, R), (24, b2)]),
    (('lock',  'pau',   'roll',  'half'),  [(0, R)]),
    (('chew',  'roll',  'tear',  'sink'),  [(0, R), (16, b3)]),
    (('draw',  'lock',  'trip',  'roll'),  [(0, R)]),
    (('half',  'chew',  'roll',  'grind'), [(0, R), (20, b2)]),
    (('tear',  'lock',  'chew',  'draw'),  [(0, R)]),
    (('pau',   'roll',  'chew',  'sink'),  [(0, R), (24, LOW7)]),
    (('lock',  'chew',  'roll',  'talk'),  [(0, R)]),
    (('draw',  'roll',  'tear',  'lock'),  [(0, R), (16, b2), (28, R)]),
    (('chew',  'trip',  'pau',   'half'),  [(0, R)]),
    (('roll',  'lock',  'grind', 'draw'),  [(0, R), (20, b3)]),
    (('tear',  'chew',  'roll',  'sink'),  [(0, R)]),
    (('lock',  'pau',   'chew',  'half'),  [(0, R), (24, b2)]),
    (('chew',  'roll',  'shred', 'draw'),  [(0, R)]),
    (('roll',  'tear',  'lock',  'gap'),   [(0, R), (26, LOW6)]),
]
DROP2 = [
    (('shred', 'lock',  'chew',  'draw'),  [(0, R)]),
    (('grind', 'roll',  'tear',  'sink'),  [(0, R), (24, b2)]),
    (('bite',  'chew',  'roll',  'half'),  [(0, R), (16, LOW6)]),
    (('lock',  'stut',  'grind', 'draw'),  [(0, R)]),
    (('chew',  'shred', 'roll',  'talk'),  [(0, R), (20, b5)]),
    (('grind', 'tear',  'lock',  'sink'),  [(0, R)]),
    (('roll',  'bite',  'chew',  'half'),  [(0, R), (24, LOW7)]),
    (('stut',  'lock',  'shred', 'draw'),  [(0, R)]),
    (('chew',  'grind', 'roll',  'sink'),  [(0, LOW6), (16, R)]),
    (('bite',  'roll',  'tear',  'talk'),  [(0, R)]),
    (('shred', 'chew',  'lock',  'half'),  [(0, R), (22, b2)]),
    (('grind', 'stut',  'roll',  'draw'),  [(0, R)]),
    (('lock',  'bite',  'chew',  'sink'),  [(0, R), (16, b3), (28, b2)]),
    (('roll',  'shred', 'grind', 'half'),  [(0, R)]),
    (('tear',  'chew',  'stut',  'draw'),  [(0, R), (24, LOW6)]),
    (('grind', 'roll',  'bite',  'gap'),   [(0, R)]),
]
DROP3 = [
    (('shred', 'grind', 'roll',  'draw'),  [(0, R)]),
    (('bite',  'stut',  'chew',  'sink'),  [(0, R), (24, b2)]),
    (('grind', 'shred', 'lock',  'half'),  [(0, R), (16, LOW6)]),
    (('stut',  'bite',  'roll',  'draw'),  [(0, R)]),
    (('shred', 'chew',  'grind', 'talk'),  [(0, R), (20, b5)]),
    (('bite',  'roll',  'stut',  'sink'),  [(0, R)]),
    (('grind', 'lock',  'shred', 'half'),  [(0, LOW7), (16, R)]),
    (('stut',  'chew',  'bite',  'draw'),  [(0, R)]),
    (('shred', 'roll',  'grind', 'gap'),   [(0, R), (24, b2)]),
    (('bite',  'tear',  'stut',  'sink'),  [(0, R)]),
    (('grind', 'chew',  'shred', 'half'),  [(0, R), (16, b3)]),
    (('roll',  'stut',  'bite',  'draw'),  [(0, R), (28, LOW6)]),
    (('shred', 'grind', 'lock',  'sink'),  [(0, R)]),
    (('stut',  'roll',  'chew',  'talk'),  [(0, R), (22, b2)]),
    (('bite',  'shred', 'grind', 'half'),  [(0, R)]),
    (('roll',  'chew',  'stut',  'draw'),  [(0, R), (24, LOW6)]),
]
COLLAPSE = [
    (('still', 'draw',  'draw',  'sink'),  [(0, LOW6)]),
    (('draw',  'still', 'talk',  'draw'),  [(0, LOW6), (24, LOW7)]),
    (('draw',  'draw',  'lock',  'sink'),  [(0, LOW7)]),
    (('still', 'talk',  'draw',  'grind'), [(0, LOW6), (20, R)]),
    (('draw',  'lock',  'still', 'draw'),  [(0, R)]),
    (('talk',  'draw',  'grind', 'sink'),  [(0, LOW6)]),
    (('draw',  'still', 'chew',  'draw'),  [(0, LOW7), (24, LOW6)]),
    (('lock',  'draw',  'talk',  'roll'),  [(0, R)]),
]


def bass(b, spec, gain=1.0, bus='bass', **kw):
    cells, notes = spec
    S.place(P(b), V.creature(notes, list(cells), seed=(b * 7) % 97, **kw), gain, bus)


# ---- the other voice -----------------------------------------------------
# Between 300 Hz and 2.5 kHz, which is the band the bass only visits when
# its filter is open, and it slides rather than strikes. Three shapes, all
# of them falling: this record does not have a rising line in it.
MOT = {
    'far':  [(0, 67), (12, 68), (20, 67), (32, 63), (44, 62), (56, 63)],
    'fall': [(0, 74), (8, 72), (16, 68), (24, 67), (32, 63), (48, 62), (56, 60)],
    'hold': [(0, 63), (24, 62), (32, 63), (56, 67)],
    'sig':  [(0, 68), (6, 67), (12, 68), (16, 63), (28, 62), (32, 63), (40, 60), (56, 63)],
}


def air(b0, bars, hull_=1.0, sheet_=0.0, seed=0):
    if hull_:
        S.place(P(b0), V.hull(bars, seed=seed + 3, tone=0.9 + 0.2 * (seed % 3)),
                hull_, 'void')
    if sheet_:
        S.place(P(b0), V.sheet(bars, seed=seed + 11), sheet_, 'void')


def stars(b0, bars, chord, gain=1.0, cutoff=900.0, attack=1.6, seed=0):
    S.place(P(b0), V.star(chord, bars, cutoff=cutoff, attack=attack, seed=seed),
            gain, 'void')


CH = {'i': [43, 50, 58], 'bII': [44, 51, 56], 'bVI': [39, 51, 55],
      'lo': [31, 43, 50]}


print('ЧЁРНЫЕ ЗВЁЗДЫ   174 BPM   G Phrygian   224 bars')

# ============================================================ 0-15 ВАКУУМ ==
air(0, 16, hull_=1.0, sheet_=0.30, seed=1)
stars(0, 8, CH['i'], 0.85, cutoff=720, attack=2.8, seed=2)
stars(8, 8, CH['bII'], 0.85, cutoff=800, attack=2.2, seed=3)
S.place(P(1), V.siren(26, f0=690, sweep=0.20, rate=0.28), 0.42, 'fx')
S.place(P(10, 4), V.transit(15, seed=5, f0=460, pan=1.0), 0.75, 'fx')
S.place(P(5), V.code(4, seed=7, density=0.10), 0.40, 'fx')
S.place(P(13), V.code(3, seed=8, density=0.18), 0.45, 'fx')
S.place(P(7), V.impact(12, seed=9, tune=52.0), 0.30, 'fx')
for b in range(12, 16):
    beat(b, 'a', e=0.50, hats=0.0, gh=0.0, plates=0.0, duck=False)
_s = slice(P(12), P(16))
S.bus['drums'][_s] = lp(S.bus['drums'][_s], 430, 4)
swell(16, 8, 0.5, seed=10)

# =========================================================== 16-31 СИГНАЛ ==
for i, b in enumerate(range(16, 32)):
    beat(b, ROT[i], e=0.60 + 0.016 * i, hats=0.40 + 0.02 * i, gh=0.7,
         plates=0.6, sg=0.9, hstep=4 if b < 24 else 2)
    if b % 8 == 7:
        fill(b, 'roll' if b == 23 else 'metal', 0.8)
_s = slice(P(16), P(24))
S.bus['drums'][_s] = lp(S.bus['drums'][_s], 2600, 2)
air(16, 16, 1.0, 0.40, seed=21)
stars(16, 8, CH['i'], 0.68, cutoff=700, seed=22)
stars(24, 8, CH['bVI'], 0.68, cutoff=780, seed=23)
S.place(P(16), V.code(8, seed=24, density=0.14), 0.42, 'fx')
S.place(P(24), V.lead(MOT['far'], 8, seed=25, cut=(380, 1700), space=0.9,
                      dist=0.16), 0.62, 'lead')
for b in range(22, 32, 2):
    S.place(P(b), V.subline([(0, R)], 2, gain=0.5,
                            gatep=[1, 1, 0, 0, 1, 1, 1, 0] * 4), 1.0, 'sub')

# =========================================================== 32-47 РАЗГОН ==
for i, b in enumerate(range(32, 48)):
    beat(b, ROT[(i + 4) % 16], e=0.80 + 0.008 * i, hats=0.70, gh=0.85,
         plates=0.8, hstep=2)
    if b % 8 == 7:
        fill(b, 'roll', 0.9)
air(32, 16, 0.9, 0.35, seed=31)
stars(32, 8, CH['i'], 0.6, cutoff=820, attack=1.2, seed=32)
stars(40, 8, CH['bII'], 0.6, cutoff=900, attack=1.0, seed=33)
S.place(P(36), V.lead(MOT['hold'], 8, seed=34, cut=(400, 2000), space=0.7,
                      dist=0.22), 0.70, 'lead')
for b in range(32, 48, 2):
    S.place(P(b), V.subline([(0, R)], 2, gain=0.62,
                            gatep=([1, 1, 1, 0, 1, 1, 0, 1] if b % 4 else
                                   [1, 1, 0, 1, 1, 0, 1, 1]) * 4), 1.0, 'sub')
S.place(P(40), V.lift(96, seed=35, f0=280, f1=2200), 0.50, 'fx')
S.place(P(44), V.transit(12, seed=36, f0=560, pan=-1.0), 0.8, 'fx')
S.place(P(47, 8), V.plunge(8, f0=104, f1=23), 0.85, 'sub')
swell(48, 10, 0.7, seed=37)

# ======================================================== 48-79 ПАДЕНИЕ I ==
# The first drop is the most spacious one on the record: eighth-note hats,
# no metal above 3 kHz that is not a snare, and every second bar of the bass
# has a dark gesture in it. What arrives at 112 is the same thing with the
# panels off, and it can only read that way if this one has some panels.
S.place(P(48), V.impact(16, seed=40, tune=49.0), 0.50, 'fx')
for i, b in enumerate(range(48, 80, 2)):
    bass(b, DROP1[i], gain=1.0)
for i, b in enumerate(range(48, 80)):
    beat(b, ROT[i % 16], e=1.0, hats=0.62, gh=0.95, plates=0.7,
         hstep=2 if b < 64 else 1)
    if b % 8 == 7:
        fill(b, ('roll', 'metal', 'roll', 'stop')[(b // 8) % 4], 1.0)
air(48, 32, 0.45, 0.0, seed=41)
stars(48, 16, CH['i'], 0.30, cutoff=880, attack=1.0, seed=42)
stars(64, 16, CH['bVI'], 0.30, cutoff=940, attack=1.0, seed=43)
S.place(P(56), V.transit(14, seed=44, f0=430, pan=1.0), 0.55, 'fx')
swell(64, 6, 0.45, seed=46)
S.place(P(64), V.impact(12, seed=47, tune=52.0), 0.32, 'fx')

# ========================================================== 80-95 ТИШИНА ==
# The drums do not stop. This is where the lead is the subject and the bass
# is not: one line, sliding, a long way off.
for i, b in enumerate(range(80, 96)):
    beat(b, 'ht' if i % 4 != 3 else 'hb', e=0.52, hats=0.30, gh=0.5,
         plates=0.8, sg=0.75, hstep=2)
air(80, 16, 1.15, 0.55, seed=51)
stars(80, 8, CH['bVI'], 1.0, cutoff=700, attack=2.4, seed=52)
stars(88, 8, CH['bII'], 1.0, cutoff=760, attack=2.0, seed=53)
S.place(P(80), V.lead(MOT['fall'], 8, seed=54, cut=(360, 1900), space=0.7,
                      dist=0.18), 0.70, 'lead')
S.place(P(88), V.lead(MOT['far'], 8, seed=55, cut=(380, 2200), space=0.6,
                      dist=0.22), 0.62, 'lead')
S.place(P(82), V.siren(28, f0=640, sweep=0.24, rate=0.24), 0.50, 'fx')
S.place(P(86), V.transit(16, seed=56, f0=380, pan=-1.0), 0.85, 'fx')
for b in range(84, 96, 4):
    S.place(P(b), V.subline([(0, LOW6), (16, LOW7)], 4, gain=0.38,
                            gatep=[1, 1, 1, 1, 0, 0, 1, 1] * 8), 1.0, 'sub')

# =========================================================== 96-111 build ==
for i, b in enumerate(range(96, 112)):
    beat(b, ROT[(i + 9) % 16], e=0.66 + 0.020 * i, hats=0.50 + 0.02 * i,
         gh=0.9, plates=0.8, hstep=2)
    if b % 8 == 7:
        fill(b, 'roll', 1.0)
air(96, 16, 0.8, 0.40, seed=61)
stars(96, 16, CH['i'], 0.45, cutoff=880, attack=1.4, seed=62)
S.place(P(100), V.lead(MOT['sig'], 8, seed=63, cut=(420, 2400), space=0.55,
                       dist=0.28), 0.72, 'lead')
for b in range(96, 112, 2):
    S.place(P(b), V.subline([(0, R)], 2, gain=0.66,
                            gatep=[1, 1, 1, 0, 1, 1, 1, 0] * 4), 1.0, 'sub')
S.place(P(104), V.lift(96, seed=64, f0=320, f1=2400), 0.60, 'fx')
S.place(P(108), V.code(4, seed=65, density=0.30), 0.50, 'fx')
S.place(P(111, 8), V.plunge(8, f0=110, f1=22), 0.95, 'sub')
swell(112, 12, 0.80, seed=66)

# ====================================================== 112-143 ПАДЕНИЕ II ==
S.place(P(112), V.impact(16, seed=70, tune=49.0), 0.60, 'fx')
for i, b in enumerate(range(112, 144, 2)):
    bass(b, DROP2[i], gain=1.05, drive=1.15)
for i, b in enumerate(range(112, 144)):
    beat(b, ROT[(i + 6) % 16], e=1.0, hats=0.70, gh=1.0, plates=0.9,
         hstep=1 if b >= 128 else 2)
    if b % 8 == 7:
        fill(b, ('metal', 'roll', 'stop', 'roll')[(b // 8) % 4], 1.0)
air(112, 32, 0.40, 0.0, seed=71)
stars(112, 16, CH['bII'], 0.26, cutoff=900, attack=1.0, seed=72)
stars(128, 16, CH['i'], 0.26, cutoff=960, attack=1.0, seed=73)
# the lead answers the bass at the end of two phrases and is gone otherwise
S.place(P(126), V.lead([(0, 63), (8, 62), (16, 63), (24, 60)], 2, seed=74,
                       cut=(450, 2600), space=0.5, dist=0.30), 0.55, 'lead')
S.place(P(142), V.lead([(0, 68), (8, 67), (16, 63), (24, 62)], 2, seed=75,
                       cut=(480, 2700), space=0.5, dist=0.30), 0.58, 'lead')
S.place(P(120), V.transit(14, seed=76, f0=500, pan=1.0), 0.50, 'fx')
S.place(P(128), V.impact(12, seed=77, tune=52.0), 0.38, 'fx')
swell(128, 6, 0.5, seed=78)

# ========================================================= 144-159 КОЛЛАПС ==
S.place(P(144), V.impact(24, seed=80, tune=44.0), 0.95, 'fx')
for i, b in enumerate(range(144, 160, 2)):
    bass(b, COLLAPSE[i], gain=0.95, hold=0.86, drive=0.9, top=5200.0)
for i, b in enumerate(range(144, 160)):
    beat(b, 'hb' if i % 4 == 3 else 'ht', e=0.92, hats=0.26, gh=0.55,
         plates=1.0, sg=1.05, kg=1.08, hstep=2)
    if b % 8 == 7:
        fill(b, 'metal', 1.0)
air(144, 16, 1.2, 0.50, seed=81)
stars(144, 8, CH['lo'], 0.85, cutoff=620, attack=1.6, seed=82)
stars(152, 8, CH['bVI'], 0.9, cutoff=680, attack=1.4, seed=83)
S.place(P(146), V.lead(MOT['fall'], 8, seed=84, cut=(340, 1600), space=1.0,
                       dist=0.14), 0.85, 'lead')
S.place(P(154), V.lead(MOT['hold'], 6, seed=85, cut=(320, 1400), space=1.0,
                       dist=0.12), 0.75, 'lead')
S.place(P(148), V.transit(20, seed=86, f0=330, pan=-1.0), 0.95, 'fx')
S.place(P(152), V.impact(20, seed=87, tune=46.0), 0.65, 'fx')
S.place(P(156), V.siren(16, f0=560, sweep=0.30, rate=0.22), 0.42, 'fx')

# ========================================================== 160-175 build ==
for i, b in enumerate(range(160, 176)):
    beat(b, ROT[(i + 2) % 16], e=0.70 + 0.020 * i, hats=0.55 + 0.022 * i,
         gh=0.95, plates=0.8, hstep=2 if b < 168 else 1)
    if b % 8 == 7:
        fill(b, 'roll', 1.0)
air(160, 16, 0.75, 0.45, seed=91)
stars(160, 16, CH['bII'], 0.42, cutoff=900, attack=1.2, seed=92)
S.place(P(164), V.lead(MOT['sig'], 8, seed=93, cut=(430, 2600), space=0.5,
                       dist=0.30), 0.78, 'lead')
for i, b in enumerate(range(160, 176, 2)):
    S.place(P(b), V.subline([(0, R)], 2, gain=0.70,
                            gatep=([1, 1, 1, 0, 1, 1, 0, 1] if i % 2 else
                                   [1, 1, 1, 1, 0, 1, 1, 0]) * 4), 1.0, 'sub')
S.place(P(168), V.lift(128, seed=94, f0=300, f1=2600), 0.70, 'fx')
S.place(P(172), V.code(4, seed=95, density=0.38), 0.55, 'fx')
S.place(P(175, 8), V.plunge(8, f0=116, f1=21), 1.0, 'sub')
swell(176, 14, 0.90, seed=96)

# ===================================================== 176-207 ПАДЕНИЕ III ==
S.place(P(176), V.impact(16, seed=100, tune=49.0), 0.70, 'fx')
for i, b in enumerate(range(176, 208, 2)):
    bass(b, DROP3[i], gain=1.08, drive=1.25)
for i, b in enumerate(range(176, 208)):
    beat(b, ROT[(i + 11) % 16], e=1.0, hats=0.78, gh=1.05, plates=0.9,
         hstep=1)
    if b % 8 == 7:
        fill(b, ('roll', 'metal', 'roll', 'stop')[(b // 8) % 4], 1.0)
air(176, 32, 0.40, 0.0, seed=101)
stars(176, 16, CH['i'], 0.28, cutoff=980, attack=1.0, seed=102)
stars(192, 16, CH['bVI'], 0.30, cutoff=1000, attack=1.0, seed=103)
S.place(P(190), V.lead([(0, 68), (8, 67), (16, 63), (24, 62)], 2, seed=104,
                       cut=(470, 2700), space=0.5, dist=0.32), 0.58, 'lead')
S.place(P(206), V.lead([(0, 74), (8, 72), (16, 68), (24, 67)], 2, seed=105,
                       cut=(500, 2800), space=0.6, dist=0.32), 0.62, 'lead')
S.place(P(184), V.transit(14, seed=106, f0=540, pan=1.0), 0.50, 'fx')
S.place(P(192), V.impact(12, seed=107, tune=52.0), 0.42, 'fx')
swell(192, 6, 0.55, seed=108)

# ============================================================ 208-223 ВЫХОД =
for i, b in enumerate(range(208, 220)):
    beat(b, ROT[(i + 3) % 16], e=0.85 - 0.055 * i,
         hats=max(0.0, 0.55 - 0.07 * i), gh=max(0.0, 0.8 - 0.1 * i),
         plates=0.45, hstep=2, duck=i < 8)
S.place(P(208), V.subline([(0, R), (16, LOW6), (32, LOW7), (48, R)], 4, gain=0.5,
                          gatep=[1, 1, 1, 0, 1, 1, 0, 0] * 8), 1.0, 'sub')
air(208, 16, 1.15, 0.45, seed=111)
stars(208, 8, CH['bVI'], 0.9, cutoff=700, attack=2.0, seed=112)
stars(216, 8, CH['i'], 1.0, cutoff=620, attack=3.2, seed=113)
S.place(P(210), V.lead(MOT['fall'], 8, seed=114, cut=(330, 1500), space=1.0,
                       dist=0.10), 0.80, 'lead')
S.place(P(212), V.siren(24, f0=610, sweep=0.22, rate=0.2), 0.45, 'fx')
S.place(P(218), V.transit(18, seed=115, f0=300, pan=1.0), 0.65, 'fx')
S.place(P(219), V.impact(20, seed=116, tune=44.0), 0.42, 'fx')

print(f'  buses: {sorted(S.bus)}   kicks: {len(S.hits)}')


# ================================================================== the mix =
S.bus['sub'] = mono_below(S.bus['sub'], 150)
S.bus['bass'] = mono_below(S.bus['bass'], 150)
S.bus['drums'] = mono_below(S.bus['drums'], 130)
S.bus['void'] = narrow(S.bus['void'], 0.90)
S.bus['fx'] = narrow(S.bus['fx'], 0.88)
S.bus['hats'] = narrow(S.bus['hats'], 0.78)
S.bus['lead'] = narrow(S.bus['lead'], 0.72)

ARC = [(0, -1.8), (11, -1.4), (15, -1.2),
       (16, -3.2), (31, -2.4),
       (32, -1.6), (44, -1.0), (46, -2.2), (47, -3.4),
       (48, -0.3), (62, -0.3), (63, -1.3),
       (64, -0.1), (78, -0.1), (79, -1.5),
       (80, -6.0), (93, -5.4), (95, -6.2),
       (96, -3.4), (108, -2.2), (110, -3.2), (111, -4.6),
       (112, 0.0), (126, 0.0), (127, -1.1),
       (128, 0.1), (142, 0.1), (143, -1.3),
       (144, -2.8), (158, -2.4), (159, -3.4),
       (160, -3.2), (172, -2.2), (174, -3.4), (175, -5.0),
       (176, 0.2), (190, 0.2), (191, -0.9),
       (192, 0.3), (206, 0.3), (207, -0.7),
       (208, -2.2), (215, -4.2), (219, -8.5), (NB, -24.0)]
_t = np.arange(S.total) / BAR
_db = np.interp(_t, [p[0] for p in ARC], [p[1] for p in ARC])
_ride = np.maximum(uniform_filter1d(10 ** (_db / 20.0), int(0.030 * SR)), 0.0)
for k in S.bus:
    S.bus[k] = S.bus[k] * _ride[:, None].astype(np.float32)
print(f'  ride: {_db.min():.1f} to {_db.max():.1f} dB across {NB} bars')

# The bass is the reference and everything else is set against it. That is
# not a mixing convention, it is what the human asked for in as many words:
# the accent is on the bassline, and the cymbals that were filling the mids
# and highs with noise are what made it impossible to hear.
TARGET = {'bass': 0.0, 'drums': -1.2, 'sub': -7.0, 'lead': -9.5,
          'perc': -13.5, 'hats': -19.0, 'void': -17.0, 'fx': -18.0}
_w = slice(P(176), P(192))
_ref = S.loudness(S.bus['bass'][_w], pct=99)
GAINS = {}
for k in S.bus:
    lv = S.loudness(S.bus[k][_w], pct=99)
    GAINS[k] = (float(np.clip(10 ** ((_ref + TARGET[k] - lv) / 20), 0.05, 12.0))
                if lv > -70 else 1.0)
print('  faders: ' + '  '.join(f'{k} {v:.2f}' for k, v in sorted(GAINS.items())))

_sum = np.zeros_like(S.bus['drums'])
for _k, _b in S.bus.items():
    _sum += _b * GAINS[_k]
_pk = np.abs(_sum).max(axis=1)
print(f'  bus sum: peak {_pk.max():.2f} at bar {int(np.argmax(_pk)) / BAR:6.2f}, '
      f'99.9th pct {np.percentile(_pk, 99.9):.2f}')
# ...and the trim is set from the 99.99th percentile rather than that one
# sample, because shaving the tip of a single transient is what the clipper
# after it is for, and letting one fill decide the level of a five-minute
# record costs five decibels of it.
_scale = 1.90 / max(float(np.percentile(_pk, 99.99)), 1e-9)
GAINS = {k: v * _scale for k, v in GAINS.items()}
print(f'  master trim: {20*np.log10(_scale):+.1f} dB -> bus sum peaks 1.90')
del _sum

S.report(GAINS)
S.ownership(3000, 16000, GAINS)
S.render('darkstep_chernye_zvezdy_174.wav', drive=0.0, duck=0.52, duck_rel=0.095,
         clip=1.70, peak=0.89, fade=2.6, gains=GAINS,
         comp=dict(thresh=0.34, ratio=2.0, attack=0.012, release=0.14),
         brick=dict(gain=1.48, ceiling=0.89))
