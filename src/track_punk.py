"""Grip Tape (~2:55, 136 bars @186) - skate punk, no vocals, E major.

Everything is a guitar or a drum. The rhythm guitars are double tracked and
hard panned; the melody a singer would have had is played by a lead guitar,
which is why the chorus tune is written to be singable and stays inside an
octave. Structure is the genre's own: two verses, two choruses, a bridge that
takes the distortion away, a harmonised twin lead, and a last chorus with
everybody shouting.

  b0-3     the count-in: four on the hats and one open chord
  b4-11    intro on the chorus riff - state the hook before anyone asks
  b12-27   verse 1: palm-muted eighths, C#-A-E-B, the bass carries the tune
  b28-35   pre-chorus: chords open up, snare climbs, sits on B and refuses
  b36-51   chorus 1: I-V-vi-IV wide open, lead guitar sings the topline
  b52-63   verse 2: d-beat kick, the lead answers between the phrases
  b64-71   pre-chorus 2
  b72-87   chorus 2, octave lead doubling
  b88-95   bridge: half time, distortion off, clean arpeggios, ride
  b96-111  the solo: fast lick, then harmonised in diatonic thirds
  b112-131 last chorus: gang shouts, octave lead, crashes on every downbeat
  b132-135 outro: one more riff and a chord left ringing
"""
import numpy as np
from punklib import *

rng = np.random.default_rng(7)
np.random.seed(7)
s = Session(136, tail=3.0)

# ---- the harmony -------------------------------------------------------
# E major. Power chords, so nothing here is major or minor by itself - the
# bass and the melody decide, which is how one four-chord loop can be the
# verse riff and the chorus at the same time.
E, B, Cs, A, Fs, Gs = 40, 47, 49, 45, 42, 44
CHORUS = [E, B, Cs, A]                       # I  V  vi IV - one bar each
VERSE  = [Cs, A, E, B, Cs, A, B, B]          # vi IV I  V  ... and V twice, to pull
PRE    = [A, B, Cs, Cs, A, B, B, B]          # climbs, then hangs on the dominant
BRIDGE = [Cs, Cs, A, A, E, E, B, B]

def ch(prog, b, b0):  return prog[(b - b0) % len(prog)]

# E major as MIDI, and the diatonic third above every degree of it - the
# harmony part for the twin lead writes itself from this.
SCALE = [64, 66, 68, 69, 71, 73, 75]
def third(n):
    i = SCALE.index((n - 64) % 12 + 64)
    return SCALE[(i + 2) % 7] + 12 * ((n - 64) // 12) + (12 if i + 2 > 6 else 0)

# ---- guitars -----------------------------------------------------------
# Double tracking is two performances, not one performance copied: different
# seeds, different string detune, a few milliseconds apart. It is the only
# reason a guitar record sounds wide, and no stereo plugin substitutes for it.
SPREAD = 0.88
SLIP = int(0.0035 * SR)

def wall(b, root, dur=16, gain=1.0, st=0.0, shape='power'):
    """an open power chord, left and right"""
    t = s.pos(b, st)
    s.place(t, panned(gtr(root, dur, take=b % 3, shape=shape), -SPREAD), gain, 'gtr')
    s.place(t + SLIP, panned(gtr(root, dur, take=10 + (b + 1) % 3, shape=shape),
                             SPREAD), gain * 0.98, 'gtr')

def chug(b, root, pattern, gain=1.0, dur=2):
    """palm-muted eighths: the engine of the genre"""
    for i, st in enumerate(pattern):
        t = s.pos(b, st)
        v = gain * (1.0 if st % 4 == 0 else 0.86 + 0.06 * rng.random())
        s.place(t, panned(mute(root, dur, take=(i + b) % 3), -SPREAD), v, 'gtr')
        s.place(t + SLIP, panned(mute(root, dur, take=10 + (i + b + 2) % 3), SPREAD),
                v * 0.98, 'gtr')

EIGHTHS = [0, 2, 4, 6, 8, 10, 12, 14]

def sing(events, gain=0.62, bus='lead', pan=0.0, harmony=False, oct_=False,
         ring=1.1, arc=True):
    """(bar, step, note, length[, bend]) - the line the singer would have had.

    Two things make this a phrase rather than a row of notes. Every note is
    held `ring` steps past its written length so it overlaps the next one -
    a guitarist does not damp a string before fretting the following note.
    And the loudness follows the line: high notes and downbeats are played
    harder, which is the difference between a melody and a sequence."""
    notes = [e[2] for e in events]
    lo, hi = min(notes), max(notes)
    for ev in events:
        b, st, note, ln = ev[:4]
        bend = ev[4] if len(ev) > 4 else 0.0
        v = 1.0
        if arc:
            v = 0.70 + 0.30 * ((note - lo) / max(hi - lo, 1))     # the contour
            v *= 1.10 if st % 4 == 0 else 0.94                    # the metre
            v = min(v, 1.05)
        seg = solo(note, ln + ring, take=(b + int(st)) % 3, bend=bend)
        gain_, gain = gain, gain * v
        s.place(s.pos(b, st), panned(seg, pan), gain, bus)
        if oct_:
            s.place(s.pos(b, st) + 90,
                    panned(solo(note - 12, ln + ring, take=(b + 1) % 3, bend=bend),
                           -pan * 0.6), gain * 0.5, bus)
        if harmony:
            s.place(s.pos(b, st) + 40,
                    panned(solo(third(note), ln + ring, take=(b + 2) % 3, bend=bend),
                           -pan), gain * 0.78, bus)
        gain = gain_

# ---- bass --------------------------------------------------------------
# Straight eighths on the root, and a walk into every chord change. The walk
# is the whole reason a punk bassline is a part and not a drone: two notes at
# the end of a bar that say where the next bar is going.
def bassline(b, root, busy=True, walk_to=None, gain=0.9):
    """A whole bar at a time, so the note never stops between picks."""
    note = root - 12                                    # E2 -> E1, the open string
    pat = EIGHTHS if busy else [0, 4, 8, 12]
    evs = [(st, note) for st in pat]
    if walk_to is not None:                             # walk into the next chord
        tgt = walk_to - 12
        d = 1 if tgt > note else -1
        evs = [e for e in evs if e[0] < 12] + [(12, tgt - 2 * d), (14, tgt - d)]
    s.place(s.pos(b), bassbar(tuple(evs), take=b % 3), gain, 'bass')

# ---- drums -------------------------------------------------------------
# Acoustic kit, played by a person: velocity alternates on the hats, the
# snare lands a hair late, the kick does not move. Nothing is sidechained -
# this is a band in a room, not a club record.
def hats(b, open_at=(), gain=0.9, rate=2):
    for st in range(0, 16, rate):
        o = st in open_at
        v = gain * (1.0 if st % 4 == 0 else 0.62 + 0.08 * rng.random())
        s.place(s.pos(b, st) + int(rng.integers(-70, 70)),
                phat(1.4 if o else 1, open_=o, seed=(st + b) % 5), v * (1.15 if o else 1),
                'drums')

def kicks(b, pat, gain=1.0):
    for st in pat:
        s.place(s.pos(b, st) + int(rng.integers(-25, 25)),
                pkick(seed=(int(st) + b) % 4), gain * (1.0 if st == 0 else 0.94), 'drums')

def snares(b, pat=(4, 12), gain=1.0, ghost=()):
    for st in pat:
        s.place(s.pos(b, st) + int(0.0025 * SR) + int(rng.integers(-60, 60)),
                psnare(seed=(int(st) + b) % 5), gain * (0.97 + 0.06 * rng.random()), 'drums')
    for st in ghost:
        s.place(s.pos(b, st), psnare(2, seed=2), gain * 0.20, 'drums')

def beat(b, kind, crash=False, gain=1.0):
    # A kick on every beat, in every pattern that is not deliberately empty.
    # The syncopated extras sit BETWEEN those four, they never replace them:
    # a pattern that only kicks on 1 and 3 makes the listener count in half
    # notes, and then 186 BPM feels like 93 whatever the hats are doing.
    if kind == 'punk':                                  # eighths, backbeat
        kicks(b, (0, 4, 8, 12)); snares(b); hats(b, gain=0.85 * gain)
    elif kind == 'dbeat':                               # the syncopated one
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b); hats(b, gain=0.85 * gain)
    elif kind == 'skank':                               # fast: snare on every offbeat
        kicks(b, (0, 4, 8, 12)); snares(b, (2, 6, 10, 14), gain=0.8)
        hats(b, gain=0.8 * gain)
    elif kind == 'chorus':                              # ride, open hats, driving
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b, ghost=(7,) if b % 2 else ())
        for st in range(0, 16, 2):
            s.place(s.pos(b, st) + int(rng.integers(-70, 70)),
                    pride(2, seed=(st + b) % 4), (0.95 if st % 4 == 0 else 0.62) * gain, 'drums')
    elif kind == 'open':                                # open hats: maximum push
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b)
        hats(b, open_at=(2, 6, 10, 14), gain=0.7 * gain)
    elif kind == 'half':                                # the bridge - still a
        kicks(b, (0, 8)); snares(b, (8,), gain=0.85)    # pulse, just a wider one
        for st in range(0, 16, 2):
            s.place(s.pos(b, st), pride(2, seed=st % 3),
                    (0.8 if st % 4 == 0 else 0.5) * gain, 'drums')
    elif kind == 'tom':                                 # floor toms, no cymbals
        kicks(b, (0, 4, 8, 12)); snares(b, (4, 12), gain=0.9)
        for st in (2, 6, 10, 14):
            s.place(s.pos(b, st), ptom(2, tune=110), 0.5 * gain, 'drums')
    if crash:
        s.place(s.pos(b), pcrash(24, seed=b % 3), 0.55 * gain, 'drums')

def fill(b, kind='toms'):
    """the last bar of a phrase: a drummer telling you a section is ending"""
    if kind == 'toms':
        kicks(b, (0, 4, 8)); snares(b, (4,))
        for i, (st, tune) in enumerate(((8, 200), (9, 200), (10, 160), (11, 160),
                                        (12, 128), (13, 128), (14, 100), (15, 100))):
            s.place(s.pos(b, st), ptom(2, tune=tune), 0.65 + 0.05 * i, 'drums')
    elif kind == 'snare':
        kicks(b, (0,))
        for i, st in enumerate(range(0, 16)):
            s.place(s.pos(b, st), psnare(2, seed=i % 3), 0.42 + 0.045 * i, 'drums')
    elif kind == 'roll32':
        kicks(b, (0,))
        for i in range(16):
            st = 8 + i * 0.5
            s.place(s.pos(b, st), psnare(1.5, seed=i % 3), 0.45 + 0.035 * i, 'drums')
        snares(b, (4,))
    elif kind == 'stop':                                # one hit, then nothing
        kicks(b, (0,)); snares(b, (0,), gain=1.0)
        s.place(s.pos(b), pcrash(28, seed=1), 0.6, 'drums')

# ================= the amp, then the count-in (b0-3) =================
# Mains hum, a string left touching a pickup until it feeds back, and four on
# the hats. A record that opens with 2.6 seconds of digital silence has
# already lost; a record that opens with an amp being switched on has not.
_n, _t = steps(48)
hum = stereo(np.sin(2 * np.pi * 50 * _t) + 0.35 * np.sin(2 * np.pi * 150 * _t)
             + 0.15 * np.sin(2 * np.pi * 100 * _t))
hum = hum * (0.055 * np.minimum(_t / 0.6, 1.0))[:, None]
hum += hp(stereo(np.random.randn(_n)), 3000) * 0.010
s.place(s.pos(0), hum, 1.0, 'gtr')
squeal = solo(88, 44, gain=26.0, decay=9.0, vib=5.0, vib_depth=0.02, take=1)
sw = np.linspace(0, 1, len(squeal)) ** 2.2
sw[-int(0.35 * SR):] *= np.linspace(1, 0.2, int(0.35 * SR))
s.place(s.pos(0, 6), reverb(squeal * sw[:, None], decay=2.2, wet=0.3), 0.30, 'gtr')
for i in range(4):                                          # "one-two-three-four"
    s.place(s.pos(3, i * 4), phat(2, seed=i), 0.62 if i else 0.9, 'drums')
    s.place(s.pos(3, i * 4), psnare(1.2, seed=i, rim=1.4), 0.36, 'drums')

# ================= intro (b4-11) =================
# The chorus riff, stated bare, so the hook is already familiar by 0:45.
for b in range(4, 12):
    root = ch(CHORUS, b, 4)
    nxt = ch(CHORUS, b + 1, 4)
    wall(b, root, 16, 0.95)
    bassline(b, root, walk_to=nxt if b % 4 == 3 else None)
    if b < 8:
        beat(b, 'punk', crash=(b == 4))
    else:
        beat(b, 'open', crash=(b == 8))
    if b == 11:
        fill(11, 'toms')
s.place(s.pos(4), pcrash(32, seed=0), 0.6, 'drums')

# ================= verse 1 (b12-27) =================
for b in range(12, 28):
    root = ch(VERSE, b, 12)
    nxt = ch(VERSE, b + 1, 12)
    chug(b, root, EIGHTHS, gain=0.92)
    if b % 8 == 7:                                      # let the last bar ring
        wall(b, root, 8, 0.6, st=8)
    bassline(b, root, walk_to=nxt if b % 8 == 7 else None)
    beat(b, 'punk' if b < 20 else 'dbeat', crash=(b in (12, 20)))
    if b == 19:
        fill(19, 'toms')
    if b == 27:
        fill(27, 'snare')
# a lead answer in the holes of verse 1
sing([(17, 8, 76, 4), (17, 12, 75, 4), (18, 0, 73, 6), (18, 8, 71, 8),
      (25, 8, 71, 4), (25, 12, 73, 4), (26, 0, 76, 8), (26, 8, 78, 8, 0.4)],
     gain=0.34, pan=0.25)

# ================= pre-chorus 1 (b28-35) =================
for b in range(28, 36):
    root = ch(PRE, b, 28)
    wall(b, root, 16, 0.95)
    bassline(b, root)
    beat(b, 'open' if b < 32 else 'skank', crash=(b == 28))
    if b == 34:
        fill(34, 'roll32')
    if b == 35:                                         # the bar before the drop:
        s.bus['drums'][s.pos(35):s.pos(36)] *= 0.0      # empty it out
        for i in range(8):
            st = 8 + i
            s.place(s.pos(35, st), psnare(1.5, seed=i % 3), 0.55 + 0.05 * i, 'drums')
        s.place(s.pos(35, 15.4), psnare(1, seed=1), 1.0, 'drums')
s.place(s.pos(36) - int(0.9 * SR), rev(pcrash(20, seed=2)), 0.5, 'drums')

# ================= chorus 1 (b36-51) =================
# The melody. An arch inside one octave, starting on the anticipation before
# the bar, resting where the guitars ring - it was written to be sung.
TUNE = [
    (0, 76, 6), (6, 75, 2), (8, 73, 4), (12, 71, 4),          # b0 over E
    (16 + 0, 73, 4), (16 + 4, 71, 4), (16 + 8, 78, 8),        # b1 over B
    (32 + 0, 76, 4), (32 + 4, 73, 4), (32 + 8, 71, 6), (32 + 14, 73, 2),
    (48 + 0, 76, 8), (48 + 8, 78, 4), (48 + 12, 76, 4),       # b3 over A
    (64 + 0, 76, 6), (64 + 6, 75, 2), (64 + 8, 73, 4), (64 + 12, 71, 4),
    (80 + 0, 73, 4), (80 + 4, 71, 4), (80 + 8, 68, 8),        # b5: lower, darker
    # G# is the fifth of C#m and it is already sounding at the end of the bar
    # before - so the chord changes underneath a held note, and the line then
    # climbs out of it. An A here would be a minor 9th against the guitar's G#.
    (96 + 0, 68, 4), (96 + 4, 71, 4), (96 + 8, 73, 4), (96 + 12, 75, 4),
    (112 + 0, 78, 10, 0.35), (112 + 10, 76, 6),               # b7: the top of the arch
]

# The second time through, the phrase does not end where it ended before: it
# climbs past the top of the first pass instead of settling. Repetition makes
# a hook; two identical repetitions make wallpaper.
TUNE_LIFT = [(112 + 0, 81, 8, 0.25), (112 + 8, 83, 8, 0.5)]

def topline(b0, gain=0.6, harmony=False, oct_=False, pan=0.0, lift=False):
    tune = [e for e in TUNE if e[0] < 112] + (TUNE_LIFT if lift else
                                              [e for e in TUNE if e[0] >= 112])
    sing([(b0 + e[0] // 16, e[0] % 16) + tuple(e[1:]) for e in tune],
         gain=gain, harmony=harmony, oct_=oct_, pan=pan)

def chorus(b0, bars=16, kind='chorus', gang_=False, oct_=False, crash_every=4,
           mel=0.58):
    for b in range(b0, b0 + bars):
        root = ch(CHORUS, b, b0)
        nxt = ch(CHORUS, b + 1, b0)
        wall(b, root, 16, 1.0)
        bassline(b, root, walk_to=nxt if (b - b0) % 4 == 3 else None)
        beat(b, kind, crash=((b - b0) % crash_every == 0))
        if (b - b0) % 8 == 7 and b - b0 < bars - 1:
            fill(b, 'toms')
    for k in range(bars // 8):
        topline(b0 + k * 8, gain=mel, oct_=oct_, lift=(k % 2 == 1))
    if gang_:
        for k in range(bars // 4):
            for i, note in enumerate((68, 66, 68, 69)):
                bb = b0 + k * 4 + i
                s.place(s.pos(bb, 0.4), gang(note, 14, seed=i), 0.30, 'gang')

chorus(36, 16, mel=0.72)
sing([(51, 8, 71, 4), (51, 12, 73, 4)], gain=0.4)               # pickup into verse 2

# ================= verse 2 (b52-63) =================
for b in range(52, 64):
    root = ch(VERSE, b, 52)
    nxt = ch(VERSE, b + 1, 52)
    chug(b, root, EIGHTHS, gain=0.92)
    bassline(b, root, walk_to=nxt if (b - 52) % 8 == 7 else None)
    beat(b, 'dbeat' if b < 60 else 'skank', crash=(b == 52))
    if b == 59:
        fill(59, 'toms')
    if b == 63:
        fill(63, 'snare')
sing([(54, 8, 73, 4), (54, 12, 71, 4), (55, 0, 69, 8), (55, 8, 71, 8),
      (57, 8, 76, 4), (57, 12, 78, 4), (58, 0, 80, 8, 0.3), (58, 8, 78, 8),
      (61, 8, 73, 4), (61, 12, 75, 4), (62, 0, 76, 12)],
     gain=0.38, pan=-0.25)

# ================= pre-chorus 2 (b64-71) =================
for b in range(64, 72):
    root = ch(PRE, b, 64)
    wall(b, root, 16, 0.95)
    bassline(b, root)
    beat(b, 'open' if b < 68 else 'skank', crash=(b == 64))
    if b == 70:
        fill(70, 'roll32')
    if b == 71:
        s.bus['drums'][s.pos(71):s.pos(72)] *= 0.0
        for i in range(12):
            s.place(s.pos(71, 4 + i), psnare(1.5, seed=i % 3), 0.5 + 0.04 * i, 'drums')
        s.place(s.pos(71, 15.4), psnare(1, seed=1), 1.0, 'drums')
sing([(70, 8, 71, 4), (70, 12, 73, 4), (71, 0, 76, 8)], gain=0.45)

# ================= chorus 2 (b72-87) =================
chorus(72, 16, oct_=True)

# ================= bridge (b88-95) =================
# The wall goes away. Everything that comes after it is louder for free.
s.place(s.pos(88), pcrash(40, seed=1), 0.5, 'drums')
for b in range(88, 96):
    root = ch(BRIDGE, b, 88)
    shape = 'min' if root in (Cs, Fs, Gs) else 'maj'
    s.place(s.pos(b), panned(clean(root, 16, shape, take=b % 3), -0.4), 0.5, 'gtr')
    s.place(s.pos(b, 8) + SLIP,
            panned(clean(root + 12, 8, shape, take=(b + 1) % 3, bright=1.3), 0.4),
            0.32, 'gtr')
    bassline(b, root, busy=False, gain=0.75)
    beat(b, 'half', gain=0.8)
    if b >= 92:                                          # the distortion creeps back
        chug(b, root, [0, 2, 4, 6, 8, 10, 12, 14][:2 * (b - 91)], gain=0.4 + 0.12 * (b - 92))
sing([(89, 8, 68, 8), (90, 0, 71, 8), (90, 8, 73, 8), (91, 8, 76, 12),
      (93, 8, 71, 4), (93, 12, 73, 4), (94, 0, 75, 8), (94, 8, 76, 16, 0.5)],
     gain=0.42, pan=0.15)
fill(95, 'roll32')

# ================= the solo (b96-111) =================
# Sixteenths over the chorus changes, E major pentatonic with the flat third
# borrowed from the blues, then the same lick harmonised a diatonic third up
# and panned against itself - the twin lead this whole genre inherited from
# 1980s metal.
SOLO_A = [                                                   # bars 0-3
    (0, 0, 76, 2), (0, 2, 78, 2), (0, 4, 80, 2), (0, 6, 78, 2),
    (0, 8, 76, 4), (0, 12, 73, 4),
    (1, 0, 75, 2), (1, 2, 76, 2), (1, 4, 78, 4), (1, 8, 76, 8),
    (2, 0, 80, 2), (2, 2, 81, 2), (2, 4, 83, 4), (2, 8, 81, 4), (2, 12, 80, 4),
    (3, 0, 78, 4), (3, 4, 76, 4), (3, 8, 73, 8),
]
SOLO_B = [                                                   # bars 4-7, faster
    (4, 0, 71, 1), (4, 1, 73, 1), (4, 2, 76, 1), (4, 3, 78, 1),
    (4, 4, 80, 1), (4, 5, 78, 1), (4, 6, 76, 1), (4, 7, 73, 1),
    (4, 8, 76, 4), (4, 12, 78, 4),
    (5, 0, 78, 1), (5, 1, 80, 1), (5, 2, 81, 1), (5, 3, 83, 1),
    (5, 4, 85, 4), (5, 8, 83, 4), (5, 12, 81, 4),
    (6, 0, 80, 2), (6, 2, 78, 2), (6, 4, 76, 2), (6, 6, 75, 2), (6, 8, 76, 8),
    (7, 0, 73, 4), (7, 4, 71, 4), (7, 8, 68, 8),
]
SOLO_C = [                                                   # bars 8-11, harmonised
    (8, 0, 76, 4), (8, 4, 78, 4), (8, 8, 80, 8),
    (9, 0, 78, 4), (9, 4, 76, 4), (9, 8, 78, 8),
    (10, 0, 80, 4), (10, 4, 81, 4), (10, 8, 83, 8),
    (11, 0, 81, 8), (11, 8, 80, 8),
]
SOLO_D = [                                                   # bars 12-15, the climb
    (12, 0, 76, 2), (12, 2, 78, 2), (12, 4, 80, 2), (12, 6, 81, 2), (12, 8, 83, 8),
    (13, 0, 81, 2), (13, 2, 83, 2), (13, 4, 85, 4), (13, 8, 83, 8),
    (14, 0, 85, 4), (14, 4, 83, 4), (14, 8, 81, 8),
    (15, 0, 83, 16, 1.0),
]
for b in range(96, 112):
    root = ch(CHORUS, b, 96)
    nxt = ch(CHORUS, b + 1, 96)
    wall(b, root, 16, 0.85)
    bassline(b, root, walk_to=nxt if (b - 96) % 4 == 3 else None)
    beat(b, 'skank' if b < 104 else 'open', crash=((b - 96) % 4 == 0))
    if b == 103:
        fill(103, 'toms')
def at(b0, evs):  return [(b0 + e[0],) + tuple(e[1:]) for e in evs]

sing(at(96, SOLO_A + SOLO_B), gain=0.60, pan=-0.15)
sing(at(96, SOLO_C), gain=0.55, pan=-0.55, harmony=True)   # the twin lead
sing(at(96, SOLO_D), gain=0.60, pan=0.0, harmony=True)

# ================= last chorus (b112-131) =================
chorus(112, 16, kind='open', gang_=True, oct_=True, crash_every=2)
# four extra bars: the tag, everything at once
for b in range(128, 132):
    root = ch(CHORUS, b, 128)
    wall(b, root, 16, 1.0)
    bassline(b, root)
    beat(b, 'open', crash=True)
sing([(128, 0, 76, 8), (128, 8, 78, 8), (129, 0, 80, 8), (129, 8, 78, 8),
      (130, 0, 76, 12), (130, 12, 78, 4), (131, 0, 80, 16, 0.6)],
     gain=0.62, harmony=True, oct_=True)
for i, note in enumerate((68, 66, 68, 69)):
    s.place(s.pos(128 + i, 0.4), gang(note, 15, seed=i), 0.34, 'gang')

# ================= outro (b132-135) =================
for b in range(132, 134):
    root = ch(CHORUS, b, 132)
    chug(b, root, EIGHTHS, gain=1.0)
    bassline(b, root)
    beat(b, 'skank')
fill(134, 'toms')
for b in (134,):
    chug(b, E, [0, 2, 4, 6], gain=1.0)
    bassline(b, E, busy=False)
# the last chord, left to ring out
s.place(s.pos(135), panned(gtr(E, 40, take=0), -SPREAD), 1.0, 'gtr')
s.place(s.pos(135) + SLIP, panned(gtr(E, 40, take=11), SPREAD), 0.98, 'gtr')
s.place(s.pos(135), pbass(E - 12, 24), 0.95, 'bass')
s.place(s.pos(135), pkick(), 1.0, 'drums')
s.place(s.pos(135), psnare(), 1.0, 'drums')
s.place(s.pos(135), pcrash(48, seed=0, size=1.7), 0.8, 'drums')

# ---- the fader ---------------------------------------------------------
# The one thing that separates a demo from a record. Without it a punk track
# is 175 seconds at the same loudness, and a chorus that is no bigger than
# the verse before it is not a chorus, whatever the chords do.
SECTIONS = [(0, 0.30), (2, 0.42), (4, 0.70), (8, 0.86),          # amp, count, intro
            (12, 0.70), (20, 0.78),                              # verse 1
            (28, 0.82), (32, 0.92),                              # pre-chorus 1
            (36, 1.00),                                          # CHORUS 1
            (52, 0.72), (60, 0.80),                              # verse 2
            (64, 0.84), (68, 0.94),                              # pre-chorus 2
            (72, 1.00),                                          # CHORUS 2
            (88, 0.42), (92, 0.62),                              # bridge
            (96, 0.90), (104, 0.97),                             # solo
            (112, 1.05),                                         # LAST CHORUS
            (132, 0.98), (136, 0.98)]

def fader():
    g = np.ones(s.total, dtype=np.float32)
    ramp = int(0.10 * SR)
    for (b0, v0), (b1, _) in zip(SECTIONS, SECTIONS[1:] + [(999, 0)]):
        a = s.pos(b0); e = min(s.pos(b1), s.total) if b1 < 999 else s.total
        if a >= s.total:
            break
        g[a:e] = v0
    for b, _ in SECTIONS[1:]:                                    # no fader clicks
        a = s.pos(b)
        if ramp < a < s.total - ramp:
            g[a - ramp:a + ramp] = np.linspace(g[a - ramp], g[a + ramp], 2 * ramp)
    return g[:, None]

# ---- the room ----------------------------------------------------------
# One space for the kit, a smaller one for the guitars. A band is a set of
# instruments that were all in the same room; give each of them its own
# reverb and the record falls apart into a collection of overdubs.
s.bus['drums'] += room(s.bus['drums'], decay=0.62, wet=0.30, tone=5600)
s.bus['gtr'] += room(s.bus['gtr'], decay=0.34, wet=0.13, tone=4200)
s.bus['lead'] += room(s.bus['lead'], decay=1.1, wet=0.22, tone=4800)
s.bus['gang'] += room(s.bus['gang'], decay=1.4, wet=0.40, tone=4000)

# ---- make room for the tune ----
# The melody was never quiet; it was masked. The rhythm guitars own 800-3000
# Hz and so does a lead, so raising the lead just makes both louder. Instead
# the guitars' midrange steps aside wherever the melody is playing - the same
# 2-3 dB a vocal takes out of an instrumental bus on any pop record, applied
# to one band instead of the whole thing so the wall keeps its weight.
def duck_band(target, trigger, lo=850, hi=3400, depth=0.38, sens=3.0):
    env = np.abs(trigger).max(axis=1)
    env = uniform_filter1d(env, int(0.025 * SR))
    env = np.clip(env / max(env.max(), 1e-9) * sens, 0, 1)
    g = uniform_filter1d(1 - depth * env, int(0.04 * SR)).astype(np.float32)
    return target - bandpass(target, lo, hi) * (1 - g)[:, None]

s.bus['gtr'] = duck_band(s.bus['gtr'], s.bus['lead'])
s.bus['gtr'] = duck_band(s.bus['gtr'], s.bus['gang'], lo=500, hi=2600, depth=0.35)

# The lead gets compressed hard and then an echo. Compression is what makes a
# lead guitar sustain: the quiet tail of a note is pulled up to meet the pick
# that started it, so the line sounds sung rather than struck. It also takes
# the crest factor off a part that was spiking 8:1 and forcing the master
# clipper to work on drum transients that had nothing to do with it.
_pk = float(np.abs(s.bus['lead']).max()) or 1.0
s.bus['lead'] = softclip(s.bus['lead'] / _pk * 2.4, 1.0, knee=0.35) * _pk * 0.50
s.bus['lead'] += delay(s.bus['lead'], steps_=6.0, times=2, fb=0.28,
                       ping=True, damp=900)[:s.total] * 0.45

# ---- bus tone ----
# What is left after the arrangement is right: the low end tidied so the kick
# and the bass are not both claiming 80 Hz, and the air a cymbal makes in a
# room that a synthesised one does not.
s.bus['bass'] = hp(s.bus['bass'], 33, order=2)
s.bus['drums'] = shelf(hp(s.bus['drums'], 32, order=2), 8500, 4.0, 'high')
s.bus['gtr'] = hp(s.bus['gtr'], 82, order=2)

AUTO = fader()
for _b in s.bus:
    s.bus[_b] *= AUTO

GAINS = {'drums': 0.30, 'gtr': 0.26, 'bass': 0.33, 'lead': 0.205, 'gang': 0.24}
s.report(GAINS)
s.render('punk_griptape_186.wav', drive=1.15, duck=0.0, limit=0.94,
         gains=GAINS, clip=1.18, fade=0.8)
