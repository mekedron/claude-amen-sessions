"""Razgon (~3:49, 143 bars @152) - big beat, A minor, instrumental.

The name means the run-up, and it is how the record starts: a guitar loop
played from a stopped turntable, the pitch climbing with the rate, arriving
in time exactly at bar 8. That gesture is the genre.

There is no vocal. The riff is the hook, a horn stab answers it every other
bar, and the third voice is the record itself under a hand - a rate that
slows, stops and goes negative, with the crossfader chopping it.

Everything was built for this record, in `bigbeatlib`:

  surf       a steel string picked near the bridge into a blackface combo.
             The level is normalised BEFORE the gain stage and the valve
             clips asymmetrically, because a symmetric clipper driven hard
             turns a string into a square wave - and a square wave with a
             treble boost on it is a chiptune, not a guitar. Then a speaker:
             everything the clipping made above 5 kHz is fizz a real cone
             cannot move, and a guitar with no cabinet is a buzzsaw
  spring     a real spring tank. Its impulse response is a train of falling
             chirps, not a cloud of noise, because a transient inside a
             coiled spring disperses - the highs arrive first. That boing is
             the whole sound of surf guitar and no room reverb makes it
  bkick/bsnare  a 1971 kit in a room, then crushed. Big beat drums are not
             loud, they are FLAT, with the room pulled up between the hits
  fuzzbass   an octave-fuzz on a bass: rectifying a wave doubles it, so the
             octave up is the same string folded and tracks perfectly
  scratch    a hand on the platter, with the fader gating it
  varispeed  a rate ramp that takes the pitch with it, the way tape does
  stab       a horn section off a record: short, band-limited, driven

  b0-7     the run-up: the riff alone, winding up from a dead stop
  b8-15    the beat lands, the fuzz bass underneath it
  b16-31   verse 1 - the horns start answering, the record gets rubbed
  b32-39   build: the loop stutters, faster and then a semitone at a time
  b40-55   drop 1 - four on the floor underneath the break, riff an octave up
  b56-63   breakdown: the guitar alone in the spring tank
  b64-79   verse 2 - scratching on every fourth bar and every eighth
  b80-87   build 2
  b88-103  drop 2, the big one
  b104-111 the interlude: half time, toms, siren, the horns an octave down
  b112-127 last drop - the answer figure on every other bar
  b128-142 outro: subtract, then the turntable is switched off
"""
import numpy as np
from bigbeatlib import *

rng = np.random.default_rng(1998)
np.random.seed(1998)
s = Session(143, tail=3.0)

# ---- the harmony -------------------------------------------------------
# A minor, and mostly one chord. The riff is the harmony; the eight-bar
# cycle only leaves home for its last two bars, which is what makes coming
# back to A feel like the drop landing.
A, F, G, C, D = 33, 29, 31, 36, 38
CYCLE = [A, A, A, A, A, A, F, G]          # i x6, bVI, bVII


def root(b): return CYCLE[b % 8]


def rel(b): return root(b) - A            # transpose the riff with the chord


# ---- the guitar --------------------------------------------------------
# A descending blues run with the flat five in it, tremolo-picked on the
# long notes. The whammy on the last note is the surf player's full stop.
RIFF = (
    (0,  (45, 57), 3.0, 14.0, 0.0),
    (3,  (48,),    1.0, 0.0,  0.0),
    (4,  (50,),    2.0, 0.0,  0.0),
    (6,  (51,),    1.0, 0.0,  0.0),        # the blue note, passed through
    (7,  (52,),    3.0, 14.0, 0.0),
    (10, (55,),    2.0, 0.0,  0.0),
    (12, (52,),    2.0, 0.0,  0.0),
    (14, (50,),    2.0, 0.0,  0.9),
)
RIFF_B = (
    (0,  (45, 57), 2.0, 0.0,  0.0),
    (2,  (55,),    2.0, 0.0,  0.0),
    (4,  (52,),    2.0, 0.0,  0.0),
    (6,  (51,),    1.0, 0.0,  0.0),
    (7,  (50,),    1.0, 0.0,  0.0),
    (8,  (48,),    3.0, 14.0, 0.0),
    (11, (50,),    1.0, 0.0,  0.0),
    (12, (52,),    4.0, 14.0, 1.2),
)


def riff(b, pat=RIFF, level=0.42, oct_=0, bus='gtr', pan=0.0, bright=1.0,
         gain=3.2, at=None):
    """`b` picks the chord, `at` picks the bar it is placed in - they differ
    only when the riff is being rendered into a scratch buffer."""
    tr = rel(b) + oct_
    at = b if at is None else at
    for st, notes, dur, trem, dip in pat:
        seg = surf(tuple(n + tr for n in notes), dur, take=(b + int(st)) % 3,
                   trem=trem, dip=dip, bright=bright, gain=gain)
        if pan:
            seg = panned(seg, pan)
        s.place(s.pos(at, st), seg, level, bus)


# ---- the hook -----------------------------------------------------------
# A horn figure that answers the guitar. With no voice on the record the
# riff cannot carry the whole hook by itself - something has to reply to it,
# and in this genre that is a sampled brass stab, short and driven.
STABV = {A: (69, 72, 76), F: (65, 69, 72), G: (67, 71, 74)}
HOOK_A = ((8, 2), (11, 1), (14, 2))
HOOK_B = ((0, 2), (3, 1), (6, 3), (12, 2))
HOOK_C = ((0, 2), (2, 1), (4, 2), (8, 2), (10, 1), (12, 4))


def hook(b, fig, level=0.5, oct_=0, dirt=1.0):
    nts = tuple(n + oct_ for n in STABV[root(b)])
    for st, ln in fig:
        s.place(s.pos(b, st), stab(nts, ln, take=(b + int(st)) % 3, dirt=dirt),
                level, 'stab')


# ---- the machine -------------------------------------------------------
# The big beat pattern: kick on the one and pushed off the two, snare on the
# backbeat, and the ghost notes between them that came off a funk record.
GHOSTS = ((6, 0.14), (7, 0.10), (11, 0.12), (14, 0.09), (15, 0.15))


def beat(b, level=1.0, floor=False, hats=True, ghost=True, open_=(2, 10),
         busy=0):
    for st in (0, 6, 10):
        s.place(s.pos(b, st), bkick(seed=b % 3), 0.62 * level, 'drums')
    if busy:
        s.place(s.pos(b, 3), bkick(click=0.7, seed=1), 0.34 * level, 'drums')
    if floor:
        # Under the break, not instead of it. The break keeps the swagger and
        # the four on the floor gives the room something to step on.
        for st in (0, 4, 8, 12):
            s.place(s.pos(b, st), bkick(tune=50.0, room=0.15, seed=2),
                    0.40 * level, 'drums')
            s.hit(s.pos(b, st))
    for st in (4, 12):
        s.place(s.pos(b, st), bsnare(seed=b % 3), 0.52 * level, 'drums')
    if ghost:
        for st, v in GHOSTS:
            if st != 11 or b % 2:
                s.place(s.pos(b, st), bsnare(2, room=0.35, crack=0.6,
                                             decay=0.055, seed=(b + st) % 4),
                        v * level * (0.85 + 0.3 * rng.random()), 'drums')
    if hats:
        for i in range(0, 16, 2):
            s.place(s.pos(b, i), bhat(seed=i % 4),
                    0.30 * level * (1.0 if i % 4 == 0 else 0.62), 'perc')
        for i in (1, 5, 9, 13):
            s.place(s.pos(b, i), bhat(seed=(i + 1) % 4), 0.13 * level, 'perc')
    for i in open_:
        s.place(s.pos(b, i), bhat(3, open_=True, seed=i % 3), 0.26 * level, 'perc')


def toms(b, level=1.0):
    for i, (st, tn) in enumerate(((0, 190), (3, 160), (6, 130), (8, 190),
                                  (11, 160), (14, 110))):
        s.place(s.pos(b, st), panned(btom(2, tune=tn, seed=i), 0.45 - 0.18 * i),
                0.40 * level, 'drums')


def fill(b, kind='snare', level=1.0):
    if kind == 'snare':
        for i, st in enumerate((12, 13, 13.5, 14, 14.5, 15, 15.5)):
            s.place(s.pos(b, st), bsnare(seed=i % 3), (0.26 + 0.05 * i) * level, 'drums')
    elif kind == 'toms':
        for i, (st, tn) in enumerate(((10, 240), (11, 205), (12, 170),
                                      (13, 145), (14, 120), (15, 98))):
            s.place(s.pos(b, st), panned(btom(2, tune=tn, seed=i), 0.5 - 0.2 * i),
                    (0.40 + 0.03 * i) * level, 'drums')
    elif kind == 'stop':
        for st in (12, 14.5, 15):
            s.place(s.pos(b, st), bsnare(seed=int(st) % 3), 0.50 * level, 'drums')


def crash(b, st=0, level=0.5):
    s.place(s.pos(b, st), bcrash(seed=b % 3), level, 'drums')


# ---- the bass ----------------------------------------------------------
B_MAIN = ((0, 0), (3, 0), (6, 12), (7, 0), (10, 0), (11, 10), (14, 0))
B_DRIVE = ((0, 0), (2, 0), (4, 0), (6, 12), (8, 0), (10, 0), (12, 7), (14, 10))
B_HOLD = ((0, 0), (8, 0), (14, 12))


def bass(b, pat=B_MAIN, level=0.48, **kw):
    r = root(b) - 12 if root(b) > 33 else root(b)
    s.place(s.pos(b), fuzzbass(tuple((st, r + off) for st, off in pat),
                               take=b % 3, **kw), level, 'bass')


# ---- the record under the hand ----
# One bar of the riff, rendered into a buffer so it can be treated as what
# it is on this kind of record: a piece of vinyl.
_scr = Session(1, tail=0.0)
_save, s = s, _scr
riff(0, RIFF, 0.9, bus='main', at=0)
s = _save
SCR = _scr.bus['main']

BABY = ((1.0, 1.0), (0.5, -1.7), (0.5, 1.9), (0.5, -1.4), (0.5, 1.6), (1.0, -1.0))
CHOP = ((1.0, 1.0), (0.5, 1.0), (0.5, 0.0), (0.5, 1.0), (0.5, 0.0), (1.0, 1.0))
TRANSFORM = ((0.5, 1.4), (0.5, -1.4), (0.5, 1.4), (0.5, -1.4),
             (0.5, 1.6), (0.5, -1.6), (0.5, 1.8), (0.5, -1.8))
TGATE = ((0.25, 1.0), (0.25, 0.0)) * 8


def rub(b, st=8, level=0.55, moves=BABY, gate=CHOP):
    s.place(s.pos(b, st), scratch(SCR, moves, gate=gate), level, 'scr')


# =======================================================================
# the arrangement
# =======================================================================

# ---- b0-7: the run-up ----
# Seven bars of the riff played through a rate that ramps from a dead stop,
# built as one continuous segment and placed so that its END lands exactly on
# bar 8 - which is the moment the record is finally in time.
_wind = Session(4, tail=0.0)
_save, s = s, _wind
for _b in range(4):
    riff(_b, RIFF if _b % 2 == 0 else RIFF_B, 0.9, bus='main')
s = _save
_w = varispeed(_wind.bus['main'], 0.42, 1.0, curve=0.7)
_w = lp(_w, 1400, order=2) * 0.55 + _w * np.linspace(0, 0.45, len(_w))[:, None]
s.place(s.pos(8) - len(_w), _w, 0.40, 'gtr')
s.place(s.pos(0), crackle(16 * 8, gain=0.5), 0.30, 'fx')
for _b in range(4, 8):
    s.place(s.pos(_b, 12), bhat(seed=_b), 0.10 * (_b - 3), 'perc')
s.place(s.pos(6), sweep(32, up=True, f0=200, f1=7000), 0.20, 'fx')
s.place(s.pos(8) - int(4 * STEP), reverse_crash(4), 0.32, 'drums')

# ---- b8-15: the beat lands ----
for b in range(8, 16):
    beat(b, hats=(b >= 10))
    bass(b, B_MAIN, 0.46)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.40, pan=-0.25)
    if b >= 12:
        riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.22, oct_=12, pan=0.45,
             bright=1.3)
crash(8, 0, 0.46)
hook(14, HOOK_A, 0.44)
rub(15, 12, 0.40, TRANSFORM, TGATE)
fill(15, 'snare')

# ---- b16-31: verse 1, the call and the answer ----
for b in range(16, 32):
    i = b - 16
    beat(b, busy=(i % 4 == 3))
    bass(b, B_MAIN if i % 4 != 3 else B_DRIVE, 0.48)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.40, pan=-0.25)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.20, oct_=12, pan=0.45, bright=1.3)
    if i % 8 == 1:
        hook(b, HOOK_A, 0.46)
    if i % 8 == 3:
        hook(b, HOOK_B, 0.44)
    if i % 8 == 5:
        rub(b, 10, 0.46)
    if i % 8 == 7:
        hook(b, HOOK_C, 0.48)
crash(16, 0, 0.44)
crash(24, 0, 0.32)
fill(31, 'toms')

# ---- b32-39: build 1 ----
for b in range(32, 40):
    i = b - 32
    beat(b, level=1.0 + 0.03 * i, ghost=(i < 6), open_=(2, 6, 10, 14))
    if i < 5:
        bass(b, B_DRIVE, 0.46, cutoff=1800 - 260 * i)
    riff(b, RIFF, 0.38 + 0.02 * i, pan=-0.25, bright=1.0 + 0.1 * i)
    if i >= 4:
        s.place(s.pos(b, 0), siren(16, rate=0.5 + 0.25 * i, take=i), 0.16, 'fx')
# the loop comes apart: the same beat of it fired faster and faster, then
# climbing a semitone at a time, which is the edit this genre is made of
s.place(s.pos(36), stutter(SCR, times=4, steps_=2.0, decay=0.1), 0.42, 'scr')
s.place(s.pos(37), stutter(SCR, times=8, steps_=1.0, decay=0.1), 0.42, 'scr')
s.place(s.pos(38), stutter(SCR, times=8, steps_=1.0, pitch=1.0), 0.44, 'scr')
s.place(s.pos(39), stutter(SCR, times=16, steps_=0.5, pitch=1.0), 0.48, 'scr')
s.place(s.pos(32), sweep(8 * 16, up=True, f0=250, f1=9000, take=1), 0.22, 'fx')
fill(39, 'snare', 1.15)
s.place(s.pos(39, 15), downlifter(4, f0=2200, f1=70), 0.26, 'fx')

# ---- b40-55: drop 1 ----
for b in range(40, 56):
    i = b - 40
    beat(b, floor=True, busy=(i % 4 == 3), open_=(2, 6, 10, 14))
    bass(b, B_DRIVE, 0.52)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.42, pan=-0.30)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.30, oct_=12, pan=0.50, bright=1.4)
    if i % 4 == 1:
        hook(b, HOOK_A, 0.52)
    if i % 4 == 3:
        hook(b, HOOK_B, 0.54)
    if i % 8 == 6:
        rub(b, 10, 0.50)
crash(40, 0, 0.55)
crash(48, 0, 0.38)
fill(55, 'stop', 1.05)

# ---- b56-63: the breakdown, the guitar alone in the tank ----
for b in range(56, 64):
    i = b - 56
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.44 if i < 4 else 0.40,
         bus='tank', bright=0.8, gain=2.4)
    if i >= 2:
        for st in (4, 12):
            s.place(s.pos(b, st), bsnare(room=1.4, seed=b % 3), 0.30, 'drums')
    if i >= 4:
        for st in (0, 6, 10):
            s.place(s.pos(b, st), bkick(seed=b % 3), 0.42, 'drums')
        bass(b, B_HOLD, 0.34, decay=0.9)
    if i >= 6:
        beat(b, level=0.85, hats=True, ghost=True)
        bass(b, B_MAIN, 0.44)
hook(60, HOOK_A, 0.42, dirt=0.5)
rub(62, 8, 0.44, TRANSFORM, TGATE)
s.place(s.pos(62), sweep(32, up=True, f0=300, f1=8000, take=2), 0.20, 'fx')
fill(63, 'toms', 1.1)

# ---- b64-79: verse 2, the record gets scratched ----
for b in range(64, 80):
    i = b - 64
    beat(b, busy=(i % 2 == 1), open_=(2, 6, 10, 14))
    bass(b, B_DRIVE if i % 4 != 2 else B_MAIN, 0.50)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.40, pan=-0.30)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.26, oct_=12, pan=0.50, bright=1.35)
    if i % 8 == 1:
        hook(b, HOOK_A, 0.50)
    if i % 8 == 3:
        rub(b, 8, 0.58)                 # the hand on the platter and the fader
    if i % 8 == 5:
        hook(b, HOOK_C, 0.52)
    if i % 8 == 7:
        rub(b, 10, 0.54, TRANSFORM, TGATE)
crash(64, 0, 0.46)
crash(72, 0, 0.32)
fill(79, 'snare', 1.1)

# ---- b80-87: build 2 ----
for b in range(80, 88):
    i = b - 80
    beat(b, level=1.0 + 0.035 * i, ghost=(i < 6), open_=(2, 6, 10, 14),
         busy=(i >= 4))
    if i < 5:
        bass(b, B_DRIVE, 0.48, cutoff=1900 - 280 * i)
    riff(b, RIFF, 0.40 + 0.02 * i, pan=-0.25, bright=1.0 + 0.12 * i)
    if i >= 3:
        s.place(s.pos(b, 0), siren(16, rate=0.6 + 0.3 * i, take=i + 4), 0.18, 'fx')
for k, b in enumerate((84, 85, 86, 87)):
    s.place(s.pos(b), stutter(SCR, times=4 * (k + 1), steps_=4.0 / (k + 1),
                              offset=4.0, pitch=0.5 * k), 0.46, 'scr')
s.place(s.pos(80), sweep(8 * 16, up=True, f0=300, f1=10000, take=3), 0.24, 'fx')
fill(87, 'snare', 1.2)
s.place(s.pos(87, 15), downlifter(4, f0=2400, f1=65), 0.28, 'fx')

# ---- b88-103: drop 2, the big one ----
for b in range(88, 104):
    i = b - 88
    beat(b, floor=True, busy=True, open_=(2, 6, 10, 14))
    bass(b, B_DRIVE, 0.54)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.44, pan=-0.32)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.32, oct_=12, pan=0.52, bright=1.45)
    if i % 4 == 1:
        hook(b, HOOK_A, 0.54)
    if i % 4 == 3:
        hook(b, HOOK_B, 0.56)
    if i % 8 == 6:
        rub(b, 8, 0.54)
crash(88, 0, 0.58)
crash(96, 0, 0.40)
fill(103, 'toms', 1.1)

# ---- b104-111: the interlude ----
# Half the machine and none of the bass: the room gets a moment to notice how
# loud the last thirty-two bars were.
for b in range(104, 112):
    i = b - 104
    s.place(s.pos(b, 0), bkick(seed=1), 0.52, 'drums')
    s.place(s.pos(b, 8), bsnare(room=1.5, seed=b % 3), 0.46, 'drums')
    toms(b, 0.55 if i < 4 else 0.75)
    for j in (2, 6, 10, 14):
        s.place(s.pos(b, j), bhat(3, open_=True, seed=j % 3), 0.20, 'perc')
    if i >= 2:
        riff(b, RIFF_B, 0.34, bus='tank', bright=0.9, gain=2.6)
    if i >= 4:
        bass(b, B_HOLD, 0.40, decay=1.1, fuzz=0.5)
    s.place(s.pos(b, 0), siren(16, f0=300 + 60 * i, f1=1200 + 200 * i,
                               rate=0.5, take=i), 0.15, 'fx')
hook(107, HOOK_C, 0.46, oct_=-12, dirt=0.4)
rub(110, 8, 0.48, TRANSFORM, TGATE)
s.place(s.pos(110), sweep(32, up=True, f0=280, f1=11000, take=5), 0.26, 'fx')
fill(111, 'snare', 1.2)
s.place(s.pos(111, 15), downlifter(4, f0=2600, f1=60), 0.30, 'fx')

# ---- b112-127: the last drop ----
for b in range(112, 128):
    i = b - 112
    beat(b, floor=True, busy=True, open_=(2, 6, 10, 14), level=1.05)
    bass(b, B_DRIVE, 0.56)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.46, pan=-0.34)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.34, oct_=12, pan=0.54, bright=1.5)
    s.place(s.pos(b, 12 if i % 2 else 8), stab((69, 72, 76), 3, take=b % 3),
            0.36, 'stab')
    if i % 4 == 1:
        hook(b, HOOK_A, 0.56)
    if i % 4 == 3:
        hook(b, HOOK_C, 0.58)
    if i % 8 == 5:
        rub(b, 8, 0.56, TRANSFORM, TGATE)
crash(112, 0, 0.60)
crash(120, 0, 0.42)

# ---- b128-143: the outro ----
for b in range(128, 140):
    i = b - 128
    beat(b, level=1.0 - 0.06 * i, floor=(i < 4), hats=(i < 8),
         ghost=(i < 6), busy=(i < 3))
    if i < 9:
        bass(b, B_MAIN, 0.46 - 0.03 * i)
    riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.42 - 0.02 * i, pan=-0.30)
    if i < 6:
        riff(b, RIFF if b % 2 == 0 else RIFF_B, 0.24, oct_=12, pan=0.50,
             bright=1.3)
    if i == 2:
        hook(b, HOOK_A, 0.46)
    if i == 6:
        hook(b, HOOK_B, 0.40)
# the turntable is switched off: the last two bars of the riff slow to a stop
_out = Session(4, tail=0.0)
_save, s = s, _out
for _b in range(4):
    riff(_b + 140, RIFF if _b % 2 == 0 else RIFF_B, 0.9, bus='main', at=_b)
s = _save
_o = tape_stop(_out.bus['main'], stop_s=3.2)
s.place(s.pos(140), _o, 0.42, 'gtr')
s.place(s.pos(140), tape_stop(spring(_out.bus['main'], wet=0.5), stop_s=3.2),
        0.30, 'tank')
s.place(s.pos(140, 0), bcrash(16, seed=2), 0.42, 'drums')
s.place(s.pos(140, 0), bkick(), 0.55, 'drums')
s.place(s.pos(140), fuzzbass(((0, A),), decay=1.6), 0.44, 'bass')
s.place(s.pos(140), crackle(16 * 4, gain=0.6), 0.26, 'fx')

# =======================================================================
# the mix
# =======================================================================
# ---- the spring tank ----
# The guitar's own reverb, not the room's. `tank` is the breakdown guitar,
# which is nearly all spring; the main guitar gets a smaller dose of the
# same tank so the two read as one instrument in one amp.
s.bus['tank'] += spring(s.bus['tank'], wet=0.60, decay=2.4)
s.bus['gtr'] += spring(s.bus['gtr'], wet=0.30, decay=1.8)

# ---- the room, and then the crusher ----
# Big beat drums are compressed until the room comes up behind the hits.
# That is not a mastering decision, it is the instrument.
s.bus['drums'] += bigroom(s.bus['drums'], decay=0.9, wet=0.20, tone=5600)
s.bus['perc'] += bigroom(s.bus['perc'], decay=0.55, wet=0.12, tone=8000)
s.bus['drums'] = crush(s.bus['drums'], 3.4, 0.52, knee=0.35)
s.bus['perc'] = crush(s.bus['perc'], 2.4, 0.60)

# ---- the turntable ----
# A scratch is a piece of vinyl going through a mixer, so it gets what that
# does to it: band-limited, compressed flat, and thrown into a quarter-note
# slapback that is itself part of the performance.
s.bus['scr'] = bandpass(s.bus['scr'], 190, 7000, order=2)
s.bus['scr'] = s.bus['scr'] + 0.75 * bandpass(s.bus['scr'], 1300, 3800)
s.bus['scr'] = crush(s.bus['scr'], 2.8, 0.56, knee=0.4)
s.bus['scr'] += delay(s.bus['scr'], steps_=4.0, times=2, fb=0.28, ping=True,
                      damp=1100)[:s.total] * 0.30

s.bus['stab'] += reverb(s.bus['stab'], decay=1.3, wet=0.22, tone=5000)[:s.total]
s.bus['gtr'] = crush(s.bus['gtr'], 2.4, 0.60)
s.bus['stab'] = crush(s.bus['stab'], 2.8, 0.56)
s.bus['tank'] = crush(s.bus['tank'], 1.6, 0.70)

# ---- make room for the voice ----
# The guitar and the voice both own 900-3000 Hz. The guitar steps out of that
# band wherever a word is happening and steps straight back in after it.
def duck_band(target, trigger, lo=850, hi=3200, depth=0.40, sens=3.0):
    env = np.abs(trigger).max(axis=1)
    env = uniform_filter1d(env, int(0.025 * SR))
    env = np.clip(env / max(env.max(), 1e-9) * sens, 0, 1)
    g = uniform_filter1d(1 - depth * env, int(0.045 * SR)).astype(np.float32)
    return target - bandpass(target, lo, hi) * (1 - g)[:, None]


_front = np.maximum(np.abs(s.bus['stab']), np.abs(s.bus['scr']))
s.bus['gtr'] = duck_band(s.bus['gtr'], _front, depth=0.48)
s.bus['tank'] = duck_band(s.bus['tank'], _front, depth=0.36)
# The drums are not turned down for anybody in this genre - but one band of
# them is. Taking 2 dB out of the kit at 1-4 kHz where the answer is
# happening costs the beat nothing and is what puts the hook in front.
s.bus['drums'] = duck_band(s.bus['drums'], _front, lo=1100, hi=4000, depth=0.22)

# ---- bus tone ----
s.bus['bass'] = mono_below(hp(s.bus['bass'], 32, order=2), 130)
s.bus['drums'] = shelf(hp(s.bus['drums'], 34, order=2), 8000, 3.0, 'high')
s.bus['perc'] = hp(s.bus['perc'], 340, order=2)
s.bus['gtr'] = hp(s.bus['gtr'], 150, order=2)
s.bus['tank'] = hp(s.bus['tank'], 200, order=2)
s.bus['scr'] = hp(s.bus['scr'], 190, order=2)
s.bus['stab'] = hp(s.bus['stab'], 280, order=2)
s.bus['fx'] = hp(s.bus['fx'], 200, order=2)

# ---- the section fader ----
# The arrangement gets the shape most of the way, but not all of it: a
# breakdown made of one instrument in a spring tank measures LOUDER than a
# drop full of transients, because the tank fills every gap and sits in the
# band the ear is most sensitive to. The last few dB of an energy curve are
# ridden on a fader, the way they always were.
SECT = [(0, 'runup'), (8, 'beat in'), (16, 'verse1'), (32, 'build1'),
        (40, 'DROP1'), (56, 'break'), (64, 'verse2'), (80, 'build2'),
        (88, 'DROP2'), (104, 'interlude'), (112, 'LAST'), (128, 'outro'),
        (144, 'end')]
LEVELS = {'runup': 0.0, 'beat in': -3.4, 'verse1': -3.6, 'build1': -2.5,
          'DROP1': 0.0, 'break': -4.5, 'verse2': -3.4, 'build2': -2.3,
          'DROP2': 0.4, 'interlude': -5.2, 'LAST': 0.5, 'outro': -1.2,
          'end': -1.2}


def fader():
    g = np.ones(s.total, dtype=np.float32)
    for (a, name), (b, _) in zip(SECT[:-1], SECT[1:]):
        g[s.pos(a):min(s.pos(b), s.total)] = 10 ** (LEVELS[name] / 20)
    g[s.pos(144):] = 10 ** (LEVELS['end'] / 20)
    ramp = int(0.10 * SR)                       # no fader clicks
    for a, _ in SECT[1:-1]:
        p = s.pos(a)
        if ramp < p < s.total - ramp:
            g[p - ramp:p + ramp] = np.linspace(g[p - ramp], g[p + ramp], 2 * ramp)
    return g[:, None]


AUTO = fader()
for _b in s.bus:
    s.bus[_b] *= AUTO

GAINS = {'drums': 0.42, 'perc': 1.95, 'bass': 0.55, 'gtr': 0.62, 'tank': 0.60,
         'scr': 0.70, 'stab': 1.15, 'fx': 0.60}
s.report(GAINS)
s.render('bigbeat_razgon_152.wav', drive=1.1, duck=0.30, limit=0.94,
         gains=GAINS, clip=0.95, fade=1.4)
