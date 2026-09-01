"""MASKARAD - high-tech minimal techno at 127 BPM, F# minor.

A masquerade is not a party where nobody knows who you are. It is a party
where everybody knows and has agreed to pretend otherwise for four hours,
which is also a fair description of a good club at two in the morning. The
mask is the point: the record is playful on the surface and never once leaves
a minor key.

Everything here is built the way the Brejcha school builds it - by
subtraction. The kick is clean and short (200 ms, so 270 ms of every beat is
empty), the bass rolls sixteenths through the hole it leaves, and the top of
the mix is twenty quiet, tiny, precisely placed things: rims on a three-step
cycle that only comes back around every three bars, tuned wood, FM bleeps
walking on a nine-note cycle over a sixteen-step bar, dust. Nothing up there
is loud. When the plucked melody finally arrives at bar 64 there is a hole
the exact size of it.

One tune, stated four ways. The cell is the same five sixteenths every bar -
0, 3, 6, 10, 13 - and only the pitches move: a descent, the same descent a
step lower, a lift to the top note, and a fall home. In the last section the
D natural becomes a D#, which turns F# Aeolian into F# Dorian for one bar
out of four; that raised sixth is the whole reason the record reads as
playful rather than sad, and it is the only note in the piece from outside
the key.

    COLD OPEN | FLOOR | ROLL | HIGH-TECH | FIRST FACE (32)
    | STRIP | MASQUERADE - breakdown (16) + build (16)
    | THE DROP (48) | OUTRO

208 bars, 6:33. The lowest point is bar 112 and the highest starts at bar
144 - 69% of the way in, which is where a peak belongs.
"""
import numpy as np
from minimallib import *

np.random.seed(127)

# ---- the material ----
TUNE = 46.25                                   # F#1 - the kick, and the floor
# F# natural minor. i - i - bVI - bVII, four bars, all the harmony there is.
CHORDS = [[42, 54, 61, 64, 68],                # F#m9
          [42, 54, 61, 64, 68],                # F#m9
          [38, 50, 57, 61, 66],                # Dmaj9  (bVI)
          [40, 52, 59, 66, 68]]                # E add9 (bVII)

# ---- the bass: one continuous four-bar oscillator ----
ROLL_A = (2, 3, 6, 7, 10, 11, 14, 15)
ROLL_B = (2, 3, 5, 6, 7, 10, 11, 13, 14, 15)
NOTES_A = [[30, 30, 30, 30, 30, 37, 30, 30],
           [30, 30, 30, 30, 30, 30, 33, 30],
           [30, 30, 30, 30, 33, 33, 30, 30],
           [30, 30, 28, 28, 28, 28, 28, 35]]
NOTES_B = [[30, 30, 30, 30, 30, 30, 37, 30, 30, 30],
           [30, 30, 30, 30, 30, 30, 30, 33, 30, 30],
           [30, 30, 33, 30, 30, 33, 33, 30, 30, 30],
           [30, 30, 30, 30, 30, 28, 28, 28, 35, 35]]

# Velocity per sixteenth. The kick owns the beat; every roll note is below
# it, and inside each beat the first sixteenth after the kick is louder than
# the one just before the next. A roll where every note is the same level is
# a row of identical events, and the body loses the pulse - which is the one
# thing a four-to-the-floor record cannot afford.
ROLLVEL = {2: 0.86, 3: 0.66, 5: 0.60, 6: 0.80, 7: 0.63,
           10: 0.86, 11: 0.68, 13: 0.62, 14: 0.82, 15: 0.70}

def _roll(steps_, notes, dur=1.35):
    """four bars of the roll as one 64-step pattern"""
    out = []
    for bar in range(4):
        for st, n in zip(steps_, notes[bar]):
            v = ROLLVEL[st] * (1.0 if bar % 2 == 0 else 0.94)
            out.append((bar * 16 + st, n, dur, 0, 0, v))
    return out

BASS_A = _roll(ROLL_A, NOTES_A)
BASS_B = _roll(ROLL_B, NOTES_B)

# ---- the tune: the same five sixteenths every bar, only the pitches move ----
CELL = (0, 3, 6, 10, 13)
VELS  = (1.00, 0.52, 0.66, 0.86, 0.48)
HOOK  = [[73, 71, 69, 66, 69],                 # a descent
         [71, 69, 66, 64, 66],                 # the same, a step lower
         [74, 73, 71, 69, 71],                 # the lift - D5 is the top note
         [71, 66, 64, 66, 61]]                 # and the fall home
HOOK_D = [r[:] for r in HOOK]
HOOK_D[2][0] = 75                              # D# - Dorian, once every four bars

# ---- the 303, two bars ----
# The grammar of the machine, not of a melody: the root hammered, octave
# jumps taken as slides, accents where the bar needs weight. Slides are what
# make a 303 liquid - the oscillator never restarts, so the pitch really
# travels instead of stepping.
ACID = [(0, 54, 1.5, 1, 0), (2, 54, 1.0, 0, 0), (3, 66, 1.5, 0, 1),
        (5, 54, 1.0, 0, 0), (6, 57, 1.0, 0, 0), (7, 57, 1.0, 0, 1),
        (8, 54, 1.5, 1, 0), (10, 61, 1.0, 0, 0), (11, 54, 1.0, 0, 1),
        (13, 64, 1.5, 0, 1), (15, 56, 1.0, 0, 0),
        (16, 54, 1.0, 1, 0), (17, 66, 1.0, 0, 1), (19, 57, 1.0, 0, 0),
        (21, 54, 1.5, 0, 1), (23, 61, 1.0, 0, 0), (24, 66, 2.0, 1, 1),
        (26, 64, 1.0, 0, 0), (27, 61, 1.0, 0, 1), (29, 57, 1.0, 0, 0),
        (30, 54, 2.0, 1, 0)]
# the drop version: denser, and it climbs to the octave instead of sitting
ACID_HOT = [(0, 54, 1.0, 1, 0), (1, 54, 1.0, 0, 0), (2, 66, 1.5, 0, 1),
            (4, 54, 1.0, 0, 0), (5, 61, 1.0, 0, 1), (6, 54, 1.0, 0, 1),
            (7, 57, 1.0, 0, 0), (8, 54, 1.0, 1, 0), (9, 66, 1.5, 0, 1),
            (11, 61, 1.0, 0, 0), (12, 54, 1.0, 0, 1), (13, 64, 1.0, 0, 0),
            (14, 66, 1.0, 0, 1), (15, 69, 1.0, 1, 1),
            (16, 54, 1.0, 1, 0), (17, 57, 1.0, 0, 0), (18, 54, 1.0, 0, 1),
            (19, 66, 1.5, 0, 1), (21, 54, 1.0, 0, 0), (22, 61, 1.0, 0, 1),
            (24, 66, 1.0, 1, 0), (25, 69, 1.0, 0, 1), (26, 66, 1.0, 0, 1),
            (27, 64, 1.0, 0, 0), (28, 61, 1.0, 0, 1), (29, 57, 1.0, 0, 0),
            (30, 54, 2.0, 1, 1)]

# The mallet line. Eight bars, and every bar is anchored on steps 2, 8 and
# 14 - an offbeat eighth, beat three, an offbeat eighth. That is the whole
# difference between a counter-melody and a part that floats: a figure whose
# hits all sit on the weakest sixteenths has no metrical reference, so the
# ear cannot attach it to the beat and hears it as a separate, unrelated
# machine. None of those three steps is used by the hook (0, 3, 6, 10, 13),
# so this answers the tune instead of doubling it.
#
# The pitches are a sentence, not a rotation: a rising figure over F#m, the
# same figure sequenced through the bVI and bVII, a lift to F#6 in bar 4 -
# the climax, at the half - and four bars of descent that end on the second
# degree, which leaves the loop needing to start again.
#                 step  note  velocity   (velocity follows the metrical tier)
MARIMBA = [
    [(2, 78, 0.72), (8, 81, 0.88), (11, 85, 0.46), (14, 83, 0.66)],   # F#m
    [(2, 81, 0.70), (8, 85, 0.88), (14, 78, 0.64)],                   # F#m
    [(2, 81, 0.72), (5, 83, 0.42), (8, 86, 0.88), (14, 85, 0.66)],    # D
    [(2, 83, 0.70), (8, 88, 0.90), (11, 85, 0.46), (14, 80, 0.62)],   # E
    [(2, 85, 0.74), (8, 88, 0.90), (12, 90, 0.62), (14, 88, 0.68)],   # F#m - the top
    [(2, 88, 0.72), (8, 85, 0.86), (11, 83, 0.46), (14, 81, 0.64)],   # F#m
    [(2, 81, 0.70), (5, 83, 0.42), (8, 78, 0.86), (14, 76, 0.62)],    # D
    [(2, 76, 0.68), (8, 78, 0.84), (15, 80, 0.40)],                   # E - hanging
]
MALPAN = (-0.34, 0.28, 0.40, -0.22)

# low tuned drums on the notes of the key: the 120-300 Hz band is otherwise
# empty here, because the kick stops at 60 and the percussion box starts at 1500
TOMS = [[(9, 54, 0.42, 0.26)],
        [(3, 49, 0.34, -0.42), (11, 54, 0.30, 0.20)],
        [(9, 50, 0.40, 0.30)],
        [(6, 57, 0.32, -0.34), (12, 49, 0.44, 0.14)]]

# the FM blips walk on a nine-note cycle over a sixteen-step bar, so the
# pattern starts somewhere new every bar and does not repeat for nine
BLIP = arp_seq([78, 81, 85, 88], bars=4, shape='updown', rate=2.0, cycle=9,
               octaves=(0, 1), gate=(1, 1, 0, 1, 1, 1, 0, 1, 1),
               accents=(0, 5), jitter=0.02, seed=5)

# Where each small thing stands. Fixed, not random: the image has to be the
# same every bar or the ear reads it as noise rather than as a room.
RIMPAN  = (-0.55, 0.42, -0.28, 0.62, 0.14)
BLIPPAN = (0.70, -0.52, 0.36, -0.74, 0.18)
SHKPAN  = (-0.18, 0.34, 0.16, -0.40)

s = Session(208, tail=5.0)

# ---- the parts ----
def floor(b, gain=1.0, lpf=None, tail=1.0, steps_=(0, 4, 8, 12), decay=0.20):
    """kick and its sub tail. Register every hit - the bass ducks to them."""
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = mkick(tune=TUNE, decay=decay)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if tail:
            s.place(t, ktail(tune=TUNE), tail * gain, 'sub')

def tops(b, gain=1.0, opens=(2, 6, 10, 14), sixteenths=True, shakers=True,
         claps=(4, 12), clapg=0.85, ride=False):
    for st in claps:
        s.place(s.pos(b, st), mclap(seed=b % 3), gain * clapg, 'drums')
    for st in opens:
        s.place(s.pos(b, st), mhat(open_=True, seed=st), gain * 0.55, 'drums')
    if sixteenths:
        for i in range(16):
            if i % 4 == 0 or i in opens:
                continue
            v = 0.55 if i % 2 else 0.34                # loud/soft: the cheapest groove
            s.place(s.pos(b, i), panned(mhat(seed=i), 0.22 * (1 if i % 4 == 1 else -1)),
                    gain * v * 0.8, 'drums')
    if shakers:
        for i in range(16):
            v = 0.62 if i % 4 == 2 else (0.44 if i % 2 == 0 else 0.26)
            s.place(s.pos(b, i + 0.035), panned(shaker(seed=i, bright=1.0),
                                                SHKPAN[i % 4]),
                    gain * v * 0.7, 'drums')
    if ride:
        for i in (0, 2, 4, 6, 8, 10, 12, 14):
            s.place(s.pos(b, i), panned(mride(seed=i), -0.28 if i % 4 else -0.12),
                    gain * (0.5 if i % 4 else 0.7), 'drums')

def perc(b, gain=1.0, rims=True, blips=True, congas=False):
    """the high-tech layer. Six quiet things on six different sixteenths."""
    if rims:
        # A dotted-eighth cycle that runs THROUGH the bar line rather than
        # restarting at it: on bar b it starts wherever bar b-1 left off, so
        # the pattern only comes back to the same place every three bars.
        base = (-16 * b) % 3
        for st in range(base, 16, 3):
            if st % 4 == 0:
                continue
            s.place(s.pos(b, st), panned(rimtick(f=1620 + 90 * (st % 5), seed=st),
                                         RIMPAN[st % 5]),
                    gain * (0.5 if st % 2 else 0.34), 'perc')
    if blips:
        for (st, note, dur, v) in BLIP:
            if int(st) // 16 != b % 4:
                continue
            s.place(s.pos(b, st - (b % 4) * 16),
                    panned(bleep(note=int(note), ratio=2.41 if note % 2 else 1.73,
                                 bend=0.02 * (note % 3)), BLIPPAN[int(note) % 5]),
                    gain * v * 0.55, 'perc')
    if congas:
        for st, note, v, sl, pn in ((5, 45, 0.55, 0, -0.30), (13, 40, 0.45, 0, 0.34),
                                    (7, 52, 0.35, 1, 0.55)):
            s.place(s.pos(b, st), panned(conga(note=note, slap=sl, seed=st), pn),
                    gain * v, 'perc')
        for st, note, v, pn in TOMS[b % 4]:
            s.place(s.pos(b, st), panned(tom(note=note, seed=st), pn), gain * v, 'perc')

def acidbar(b, u, pattern=ACID, gain=1.0, cut=(0.06, 0.45), res=(3.6, 6.4),
            emod=(0.70, 0.95), drv=(3.6, 7.0), bite=0.0):
    """Two bars of 303 with the knobs where the arc says they are.

    `u` is 0..1 across the section. Cutoff, resonance, env-mod and drive all
    travel together, because that is how the machine is played: nobody turns
    one knob on a 303. `bite` adds a late kick of resonance and drive for
    the bars where it is supposed to scream."""
    e = u ** 0.8
    s.place(s.pos(b), acid(pattern, 2,
                           cutoff=round(cut[0] + (cut[1] - cut[0]) * e, 3),
                           res=round(res[0] + (res[1] - res[0]) * e + 1.6 * bite, 2),
                           envmod=round(emod[0] + (emod[1] - emod[0]) * e, 3),
                           drive=round(drv[0] + (drv[1] - drv[0]) * e + 2.0 * bite, 2),
                           gain=gain), 1.0, 'acid')


def marimba(b, gain=1.0, full=True, hard=0.30, dur=5.5, ring=1.0):
    """The mallet counter-line. `full=False` plays only the three anchors,
    which is how it is introduced: the frame first, the decoration later."""
    for st, note, v in MARIMBA[b % 8]:
        if not full and st not in (2, 8, 14):
            continue
        s.place(s.pos(b, st),
                panned(mallet(note, dur * ring, hard=hard, seed=st), MALPAN[st % 4]),
                gain * v, 'mallet')


def bassbar(b, pattern=BASS_A, gain=1.0, mid=1.0, **kw):
    """Four bars at a time - one oscillator, one unbroken phase, twice: the
    sub that is felt and the octave above it that is heard."""
    s.place(s.pos(b), rollbass(pattern, 4, **kw), gain, 'bass')
    if mid:
        s.place(s.pos(b), midbass(pattern, 4), gain * mid, 'mid')

def hook(b, gain=1.0, table=HOOK, oct_=0, dur=2.2, echo=True, decay=0.085,
         f_hi=7200.0, ring=0.30):
    """one bar of the tune"""
    row = table[b % 4]
    for st, note, v in zip(CELL, row, VELS):
        f = midi(note + 12 * oct_)
        seg = plink(f, dur, decay=decay, f_hi=f_hi, ring=ring)
        t = s.pos(b, st)
        if echo and st in (10, 13):
            s.place_echo(t, seg, gain * v, times=2, delay_steps=3.0, fb=0.40,
                         bus='music')
        else:
            s.place(t, seg, gain * v, 'music')

def chord(b, gain=1.0, dur=16, cutoff=2600, wide=1.8, gated=0.0):
    c = [midi(n) for n in CHORDS[b % 4]]
    p = glasspad(c, dur, cutoff=cutoff, wide=wide, seed=b, attack=0.35)
    if gated:
        p = gate(p, 1.0, gated)
    s.place(s.pos(b), p, gain, 'pad')


# ================= COLD OPEN  bars 0-15 =================
# kick, dust, and a sweep four bars long. Nothing else for half a minute.
for b in range(0, 16):
    u = b / 15
    floor(b, gain=0.34 + 0.50 * u, lpf=700 + 560 * b,
          tail=0.0 if b < 6 else 0.35 * (b - 6) / 9)
    if b >= 4:
        tops(b, gain=0.30 + 0.45 * u, opens=(2, 6, 10, 14) if b >= 8 else (6, 14),
             sixteenths=b >= 12, shakers=b >= 8, claps=())
    if b >= 10:
        perc(b, gain=0.35, rims=True, blips=b >= 12)
for b in range(0, 16, 4):
    s.place(s.pos(b), dust(64, gain=0.7, seed=b), 1.0, 'air')
s.place(s.pos(0), sweepnoise(64, gain=0.55, f0=260, f1=5200, seed=1), 1.0, 'air')
s.place(s.pos(8), sweepnoise(64, gain=0.6, f0=400, f1=8000, seed=2), 1.0, 'air')
s.place(s.pos(14), revblip(88, 8, gain=0.5), 1.0, 'fx')

# ================= THE FLOOR  bars 16-31 =================
for b in range(16, 32):
    u = (b - 16) / 15
    floor(b, gain=1.0, tail=1.0)
    tops(b, gain=0.75 + 0.25 * u, claps=(4, 12) if b >= 24 else (), clapg=0.8)
    perc(b, gain=0.55 + 0.3 * u, congas=b >= 28)
    if b >= 20:                       # the frame of the mallet line, no decoration
        marimba(b, gain=0.40 + 0.30 * u, full=False, hard=0.22, ring=0.8)
for b in range(16, 32, 4):
    s.place(s.pos(b), dust(64, gain=0.8, seed=b), 1.0, 'air')
s.place(s.pos(16), sweepnoise(64, gain=0.5, f0=500, f1=9000, seed=3), 1.0, 'air')
s.place(s.pos(30), sweepnoise(32, gain=0.7, f0=6000, f1=700, seed=4, rev_=True), 1.0, 'air')

# ================= THE ROLL  bars 32-47 =================
# the bass arrives and the groove is finished. Nothing else is added for
# sixteen bars, on purpose: this is the loop the whole record is made of.
for b in range(32, 48):
    floor(b)
    tops(b, ride=b >= 44)
    perc(b, gain=0.9, congas=True)
    marimba(b, gain=0.72, full=b >= 40, hard=0.26)
for b in range(32, 48, 4):
    bassbar(b, BASS_A, gain=0.8 if b < 36 else 1.0)
    s.place(s.pos(b), dust(64, gain=0.8, seed=b), 1.0, 'air')
s.place(s.pos(40), sweepnoise(64, gain=0.5, f0=300, f1=7000, seed=6), 1.0, 'air')

# ================= HIGH-TECH  bars 48-63 =================
for b in range(48, 64):
    floor(b)
    tops(b, ride=True)
    perc(b, gain=1.0, congas=True)
    marimba(b, gain=0.85, hard=0.30)
    if b % 4 == 3:
        s.place(s.pos(b, 14), bleep(note=93, ratio=3.11, index=3.4, bend=0.06),
                0.5, 'perc')
for b in range(48, 64, 4):
    bassbar(b, BASS_A)
    s.place(s.pos(b), dust(64, gain=0.9, seed=b), 1.0, 'air')
# the tune, once, filtered almost shut - a promise, not a statement
for b in range(56, 64):
    hook(b, gain=0.34, f_hi=1500.0, decay=0.05, ring=0.15, echo=False)
s.place(s.pos(56), sweepnoise(64, gain=0.6, f0=400, f1=9000, seed=7), 1.0, 'air')
s.place(s.pos(63), revblip(85, 8, gain=0.6), 1.0, 'fx')

# ================= FIRST FACE  bars 64-95 =================
for b in range(64, 96):
    u = (b - 64) / 31
    floor(b)
    tops(b, ride=True)
    perc(b, gain=1.0, congas=True)
    marimba(b, gain=0.66, hard=0.28)          # under the tune once the tune is here
    hook(b, gain=0.85, f_hi=3200 + 4000 * min(u * 2.2, 1.0),
         decay=0.06 + 0.03 * min(u * 2.2, 1.0))
    if b >= 80:
        chord(b, gain=0.30, cutoff=1900, gated=0.5)
for b in range(64, 96, 4):
    bassbar(b, BASS_A)
    s.place(s.pos(b), dust(64, gain=0.9, seed=b), 1.0, 'air')
for b in range(80, 96, 2):
    acidbar(b, (b - 80) / 14, gain=0.72, cut=(0.03, 0.30), res=(3.4, 5.2),
            emod=(0.62, 0.86), drv=(3.2, 5.4))
s.place(s.pos(64), mcrash(24, gain=0.55), 1.0, 'fx')
s.place(s.pos(72), sweepnoise(64, gain=0.5, f0=600, f1=11000, seed=8), 1.0, 'air')
s.place(s.pos(88), sweepnoise(64, gain=0.6, f0=350, f1=8000, seed=9), 1.0, 'air')

# ================= STRIP  bars 96-111 =================
# the tune goes away and does not come back for forty-eight bars. The
# percussion box is left holding the record on its own.
for b in range(96, 112):
    u = (b - 96) / 15
    floor(b, gain=1.0, tail=1.0 - 0.35 * u)
    tops(b, gain=1.0 - 0.25 * u, ride=b < 106, claps=(4, 12) if b < 108 else ())
    perc(b, gain=1.05, congas=True)
    marimba(b, gain=0.95, hard=0.34)          # the tune is gone; this carries it
    if b >= 104:
        chord(b, gain=0.22 + 0.4 * u, cutoff=1400 + 130 * (b - 104), gated=0.55)
for b in range(96, 112, 4):
    bassbar(b, BASS_A if b < 104 else BASS_B, gain=1.0 if b < 108 else 0.7)
    s.place(s.pos(b), dust(64, gain=1.0, seed=b), 1.0, 'air')
for b in range(96, 112, 2):
    u = (b - 96) / 14
    acidbar(b, u, gain=0.95 if b < 108 else 0.80, cut=(0.28, 0.62),
            res=(5.0, 7.2), emod=(0.80, 0.96), drv=(5.0, 8.0),
            bite=max(0.0, (b - 104) / 8))
s.place(s.pos(104), sweepnoise(128, gain=0.75, f0=300, f1=12000, seed=10, curve=2.4),
        1.0, 'air')
s.place(s.pos(110), whisper(32, gain=0.5, v0='oo', v1='ah', note=66, seed=11), 1.0, 'air')
s.place(s.pos(111, 12), mdown(8, gain=0.7, f0=2800, f1=200), 1.0, 'fx')

# ================= MASQUERADE - breakdown  bars 112-127 =================
# no kick for sixteen bars. The tune, exposed, with a room around it.
for b in range(112, 128):
    u = (b - 112) / 15
    chord(b, gain=0.58 + 0.22 * u, cutoff=1500 + 2200 * u, wide=2.2)
    hook(b, gain=0.40 + 0.28 * u, dur=3.4, decay=0.13, f_hi=6200, ring=0.45)
    if b >= 118:
        for st in (2, 6, 10, 14):
            s.place(s.pos(b, st), mhat(open_=True, seed=st), 0.18 * (u + 0.2), 'drums')
    marimba(b, gain=0.45 + 0.25 * u, full=b >= 120, hard=0.18, dur=7.0)
    if b >= 122:
        perc(b, gain=0.35 * (u + 0.2), rims=True, blips=True)
s.place(s.pos(112) - int(12 * STEP), rev(mcrash(16, gain=0.9)), 1.0, 'fx')
s.place(s.pos(112), mimpact(32, tune=TUNE, gain=0.85, decay=0.9), 1.0, 'fx')
s.place(s.pos(112), whisper(64, gain=0.55, v0='oo', v1='eh', note=66, seed=12), 1.0, 'air')
s.place(s.pos(118), whisper(48, gain=0.6, v0='ah', v1='ee', note=73, seed=13), 1.0, 'air')
for b in range(116, 128, 4):
    s.place(s.pos(b), chime(midi(HOOK[b % 4][0] + 12), 8, gain=0.45), 1.0, 'music')
for b in range(112, 128, 4):
    s.place(s.pos(b), dust(64, gain=0.6, seed=b), 1.0, 'air')
s.place(s.pos(120), sweepnoise(128, gain=0.7, f0=250, f1=10000, seed=14, curve=2.0),
        1.0, 'air')

# ================= MASQUERADE - build  bars 128-143 =================
for b in range(128, 144):
    ph = b - 128
    u = ph / 15
    chord(b, gain=0.80 - 0.22 * u, cutoff=3600 + 2400 * u, wide=2.0,
          gated=0.0 if ph < 8 else 0.55)
    hook(b, gain=0.9, dur=3.0 - 1.0 * u, decay=0.13 - 0.05 * u,
         f_hi=6800, ring=0.45 - 0.2 * u)
    if ph >= 4:                                     # the kick walks back in
        floor(b, gain=0.35 + 0.65 * min((ph - 4) / 8, 1.0),
              lpf=200 + 700 * (ph - 4) if ph < 12 else None,
              tail=0.2 + 0.8 * min((ph - 4) / 8, 1.0))
    tops(b, gain=0.35 + 0.6 * u, sixteenths=ph >= 6, shakers=ph >= 4,
         claps=(4, 12) if ph >= 8 else (), opens=(2, 6, 10, 14) if ph >= 2 else (6, 14))
    perc(b, gain=0.5 + 0.5 * u, congas=ph >= 8)
    marimba(b, gain=0.7 + 0.2 * u, hard=0.24 + 0.12 * u)
    if ph >= 8 and ph % 2 == 0:
        acidbar(b, (ph - 8) / 6, gain=0.55 + 0.09 * (ph - 8),
                cut=(0.10, 0.58), res=(4.2, 7.0), emod=(0.75, 0.96),
                drv=(4.0, 7.6))
for b in range(136, 144, 4):
    bassbar(b, BASS_A, gain=0.5 if b < 140 else 0.85)
# the snare roll, doubling every four bars, and a riser under it
for ph, rate in ((0, 4.0), (4, 2.0), (8, 1.0), (12, 0.5)):
    b = 128 + ph
    st = 0.0
    while st < 16 * 4:
        bb = b + int(st // 16)
        if bb < 144:
            v = 0.16 + 0.42 * (st / 64) + 0.18 * (ph / 12)
            s.place(s.pos(bb, st % 16), mclap(seed=int(st) % 3), v * 0.38, 'fx')
        st += rate
s.place(s.pos(132), sweepnoise(192, gain=0.8, f0=300, f1=13000, seed=15, curve=2.6),
        1.0, 'air')
s.place(s.pos(136), mriser(128, gain=0.60, f0=350, f1=9000, rate_steps=2.0,
                          seed=1), 1.0, 'fx')
s.place(s.pos(142), mriser(32, gain=0.70, f0=800, f1=13000, rate_steps=0.5,
                          seed=2, tone=0.5), 1.0, 'fx')
# and the last beat is empty
s.place(s.pos(143, 12), mdown(6, gain=0.55, f0=3400, f1=220), 1.0, 'fx')

# ================= THE DROP  bars 144-191 =================
for b in range(144, 192):
    ph = b - 144
    floor(b)
    tops(b, ride=True, clapg=0.9)
    perc(b, gain=1.05, congas=True)
    table = HOOK_D if ph >= 32 else HOOK
    marimba(b, gain=0.78, hard=0.32)
    hook(b, gain=1.0, table=table, f_hi=7600, decay=0.09, ring=0.32)
    if ph >= 16:
        chord(b, gain=0.34, cutoff=2400, gated=0.5)
    if ph >= 32 and b % 2 == 0:                     # the second face, an octave up
        s.place(s.pos(b, 10), chime(midi(table[b % 4][3] + 12), 6, gain=0.34),
                1.0, 'music')
for b in range(144, 192, 4):
    bassbar(b, BASS_A if (b - 144) % 8 < 4 else BASS_B)
    s.place(s.pos(b), dust(64, gain=1.0, seed=b), 1.0, 'air')
# Forty bars, one pattern, four knobs. It opens, is pulled back at 168 so it
# has somewhere to go, then screams from 180 to the end of the section.
for b in range(152, 192, 2):
    ph = b - 152
    if ph < 16:
        acidbar(b, ph / 14, pattern=ACID, gain=0.85, cut=(0.16, 0.52),
                res=(4.4, 6.6), emod=(0.78, 0.94), drv=(4.4, 6.8))
    elif ph < 24:
        acidbar(b, (ph - 16) / 6, pattern=ACID, gain=0.62, cut=(0.20, 0.10),
                res=(4.0, 3.6), emod=(0.70, 0.62), drv=(3.6, 3.2))
    else:
        acidbar(b, (ph - 24) / 14, pattern=ACID_HOT, gain=1.0,
                cut=(0.14, 0.55), res=(5.2, 7.6), emod=(0.86, 0.99),
                drv=(5.4, 8.4), bite=max(0.0, (ph - 32) / 8))
s.place(s.pos(144), mcrash(28, gain=0.80), 1.0, 'fx')
s.place(s.pos(144), mimpact(24, tune=TUNE, gain=0.95), 1.0, 'fx')
s.place(s.pos(176), mcrash(24, gain=0.60), 1.0, 'fx')
for b in (152, 168, 184):
    s.place(s.pos(b), sweepnoise(128, gain=0.55, f0=400, f1=12000, seed=b), 1.0, 'air')
# one bar of the tune stuttered, at the seam
s.place(s.pos(175, 12), stutter(plink(midi(78), 2.0), 0.5, 4, 0.78, 1.055), 0.55, 'fx')

# ================= OUTRO  bars 192-207 =================
for b in range(192, 208):
    ph = b - 192
    u = ph / 15
    floor(b, gain=1.0 - 0.35 * u, lpf=None if ph < 8 else 7000 - 700 * (ph - 8),
          tail=1.0 - 0.5 * u)
    tops(b, gain=0.95 - 0.7 * u, sixteenths=ph < 8, shakers=ph < 11,
         claps=(4, 12) if ph < 6 else (), ride=ph < 4)
    perc(b, gain=0.9 - 0.7 * u, blips=ph < 8, congas=ph < 6)
    if ph < 12:
        marimba(b, gain=0.8 - 0.06 * ph, full=ph < 8, hard=0.28)
    if ph < 8:
        hook(b, gain=0.8 - 0.09 * ph, f_hi=6800 - 600 * ph, decay=0.08)
for b in range(192, 204, 4):
    bassbar(b, BASS_A, gain=1.0 - 0.25 * ((b - 192) / 12))
s.place(s.pos(192), dust(64, gain=0.8, seed=192), 1.0, 'air')
s.place(s.pos(196), sweepnoise(96, gain=0.5, f0=8000, f1=400, seed=20, rev_=True),
        1.0, 'air')
s.place(s.pos(204), whisper(48, gain=0.45, v0='ah', v1='oo', note=66, seed=21),
        1.0, 'air')
s.place(s.pos(207, 8), revblip(90, 8, gain=0.35), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['music']  = bus_reverb(s.bus['music'],  decay=1.9, wet=0.26, tone=5200)
s.bus['mallet'] = bus_reverb(s.bus['mallet'], decay=2.2, wet=0.30, tone=4800)
s.bus['perc']  = bus_reverb(s.bus['perc'],  decay=1.10, wet=0.24, tone=6800)
s.bus['pad']   = bus_reverb(s.bus['pad'],   decay=3.4, wet=0.34, tone=4200)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=2.6, wet=0.30, tone=4600)
s.bus['acid']  = bus_reverb(s.bus['acid'],  decay=1.1, wet=0.15, tone=5000)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.2, wet=0.18, tone=3600)

s.bus['air']  = hp(s.bus['air'], 180)                    # the kick owns the bottom
s.bus['perc'] = hp(s.bus['perc'], 190)
s.bus['pad']  = hp(s.bus['pad'], 165)
s.bus['acid'] = shelf(s.bus['acid'], 240, -2.5, kind='low')
s.bus['mid']  = hp(s.bus['mid'], 78, order=4)    # the sub layer owns below it
s.bus['music'] = shelf(s.bus['music'], 300, -2.0, kind='low')
s.bus['mallet'] = hp(s.bus['mallet'], 330, order=2)   # the hook owns below it
s.bus['mallet'] = shelf(s.bus['mallet'], 2600, -1.5)  # leave the hats their air

# The pump is an instrument here, not a rescue: a release near a sixteenth
# (118 ms at 127 BPM) lets the bass bus climb back up just before the next
# kick, and that climb is what the body reads as the groove.
s.bus['perc'] = squash(s.bus['perc'], thresh=0.24, ratio=3.2, attack=0.004,
                       release=0.088, mix=0.85, makeup=1.25, report='perc')
s.bus['music'] = squash(s.bus['music'], thresh=0.30, ratio=3.0, attack=0.004,
                        release=0.118, mix=0.80, makeup=1.20, report='music')
s.bus['bass'] = squash(s.bus['bass'], thresh=0.32, ratio=4.0, attack=0.006,
                       release=0.118, report='bass')
s.bus['drums'] = squash(s.bus['drums'], thresh=0.40, ratio=2.6, attack=0.016,
                        release=0.118, mix=0.55, report='drums')
s.bus['drums'] = softclip(s.bus['drums'], 1.25, knee=0.85)
s.bus['fx'] = hp(s.bus['fx'], 42)                        # the impact is not a kick

# Everything with weight goes mono under 150 Hz. Reverb tails and the Haas
# nudges leak sub into the side channel where nobody hears it until a club
# system sums the low end and it quietly cancels.
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)
for b in ('drums', 'perc', 'air', 'fx'):
    s.bus[b] = shelf(s.bus[b], 11000, -1.5)

GAINS = {'drums': 0.90, 'sub': 0.15, 'bass': 0.60, 'mid': 1.60, 'perc': 2.05,
         'acid': 0.66, 'music': 1.95, 'mallet': 0.46, 'pad': 3.30, 'air': 1.70, 'fx': 1.40}
s.report(GAINS)
# 0.26 s of release is 2.2 sixteenths at 127 BPM: the bass is still held down
# when its first offbeat note arrives and has climbed most of the way back by
# the next kick. That climb is the pump, and it is why the beat stays findable.
s.render('minimal_maskarad_127.wav', drive=0.60, duck=0.16, clip=1.45,
         limit=0.90, peak=0.95, fade=2.5, gains=GAINS, duck_rel=0.26)
