"""ОГНИ - stadium disco at 126 BPM, A major, and it ends in B major.

The companion to `revashol`, and deliberately its opposite in everything
except the band. That record is a ruined city at dawn and it grieves in D
minor; this one is a field with forty thousand people in it and their hands
up, and it is in A major and it does not grieve at all.

ABBA, then - the up-tempo half of them, not the sad half. Which means the
production is the composition:

  THE WALL OF VOICES.  Michael Tretow's trick, and it is why a record made
  by two women sounds like thirty: the second and third takes were cut with
  the tape machine running at a slightly different speed, so the doubles are
  detuned AND fractionally longer. `voices()` deals seven singers into three
  such takes at about -14, 0 and +14 cents, with their own delays on top -
  a spread far wider than intonation drift, which is heard as a crowd and
  not as a chorus pedal. There are no words: one vowel, held. A vowel is a
  texture; a sequence of them is a robot mumbling.

  THE PIANO IS PLAYED IN OCTAVES.  Benny Andersson's right hand, and the one
  instrument that has to be an acoustic grand. It doubles the hook every
  time the hook arrives.

  THE TWELVE-STRING.  `strum()` gives each of the four lower courses a second
  wire an octave up, a few cents off and struck a millisecond later, because
  they are two strings under one plectrum. That shimmer is not a chorus
  pedal; it is the instrument.

  AND IT GOES UP A TONE AT THE END.  The cheapest device in pop music. Used
  once, at 73% of the way through, on the fourth arrival of the same chorus.

    A  -  E/G#  -  F#m7  -  D             I - V6 - vi - IV
    A  -  E/G#  -  F#m7  -  D  -  Dm  -  E7

The four chords, and everyone alive knows them. The bass walks A - G# - F#
down under the first three, so the loop leans forward before it has done
anything else; and the second time through, bar 15 is a Dm - the BORROWED
MINOR IV, the one chord in the record that is not in the key. It is a
quarter of a second of grief inside four minutes of joy, and it is the
reason the last chorus means anything.

The verses start on F#m - the relative minor - so the chorus arriving on A
is a mode change as well as a section change: dark to bright, and the tune
jumps a fifth at the same moment.

THE HOOK IS FIVE NOTES AND FORTY THOUSAND PEOPLE CAN SING IT.

    E5  E5  F#5 - E5 ------- C#5 -----

A repeated note, one step up, and a fall. That is the whole thing. It
climbs to A5 in bar 6 - the flat third of the F#m underneath it, which is
the ache inside the euphoria - and comes down to B4 to leave the loop open.
A second singer runs a diatonic third below throughout, because two women
singing in thirds is what this genre sounds like.

THE BAND BUDGET IS DECIDED HERE, NOT AT THE MIX.

    band      OPEN V1 LIFT CH1 V2 LIFT CH2 BRK BRIDGE BUILD FINALE OUT
    20-60      -   x   x    X   x   x   X   X    -     x      X     x
    60-120     -   X   X    X   X   X   X   X    -     x      X     x
    120-800    x   x   x    X   x   x   X   x    x     x      X     x
    800-2.5k   x   x   X    X   X   X   X   x    x     X      X     x
    2.5-6k     x   x   x    X   x   x   X   x    -     X      X     x
    6-12k      -   X   X    X   X   X   X   X    -     x      X     -
    12k+       -   x   x    X   x   x   X   x    -     -      X     -

The bottom two octaves are absent for the first eight bars and again for
the eight bars of the bridge where the drums stop.

    OPEN 8 | VERSE 16 | LIFT 8 | CHORUS 16 | VERSE 16 | LIFT 8
    | CHORUS 16 | BREAK 8 | BRIDGE 16 | BUILD 8 | FINALE 32 | OUT 12

164 bars, 5:12 at 126 BPM. Mastered to about -9 LUFS.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d

import discolib as D
from discolib import *
# `core.ep` is a generic FM electric piano; this is funklib's, whose tine is a
# modulator at fourteen times the carrier dying in 60 ms and whose VELOCITY
# moves the index rather than the volume - hit it harder and it gets brighter,
# which is the one thing a sampled Rhodes from this decade could not do
from funklib import ep as rhodes

BAR, STEP = D.set_tempo(126)
D.SWING = 0.040                     # 52.5% - less than `revashol`; this one drives

np.random.seed(1979)
rs = np.random.RandomState(1979)

NB = 164
P = lambda b, s=0.0: int(round(b * BAR + s * STEP))
KEY = 0                             # +2 for the last third of the record


# ============================================================== material ===
# A major: A B C# D E F# G#.  Guitar voicings live in MIDI 55-70, where a
# chank belongs; the bass roots walk A1 - G#1 - F#1 and then leap to D2.
# F major: F G A Bb C D E.  Guitar voicings live in MIDI 55-70; the bass
# roots walk F - E - D and then leap to Bb, all inside 33-45 where a
# Precision is loudest and a club system is flattest.
V_F    = (57, 60, 65, 69)           # A3  C4  F4  A4    3    5    root 3
V_CE   = (55, 60, 64, 67)           # G3  C4  E4  G4    5    root 3    5
V_DM7  = (57, 60, 65, 69)           # A3  C4  F4  A4    5    b7   b3   5
V_BB   = (58, 62, 65, 70)           # Bb3 D4  F4  Bb4   root 3    5   root
V_BBM  = (58, 61, 65, 70)           # Bb3 Db4 F4  Bb4   root b3   5   root
V_GM7  = (58, 62, 65, 67)           # Bb3 D4  F4  G4    b3   5    b7   root
V_C7   = (58, 60, 64, 67)           # Bb3 C4  E4  G4    b7   root 3    5
V_AM7  = (57, 60, 64, 67)           # A3  C4  E4  G4    root b3   5    b7
V_C    = (55, 60, 64, 67)
V_CSUS = (55, 60, 65, 67)           # G3  C4  F4  G4    5    root 4    5
V_D7   = (57, 60, 62, 66)           # A3  C4  D4  F#4   5    b7   root 3
V_BBMAJ= (58, 62, 65, 72)           # Bb3 D4  F4  C5    root 3    5    9
V_A7   = (57, 61, 64, 67)           # A3  C#4 E4  G4    root 3    5    b7

# THE BORROWED CHORD IS APPROACHED FROM ITS OWN MAJOR SELF.
#
# A first pass went `C#m7 - Dm`, and that is wrong in a way no single note is
# wrong: the two chords share NOTHING, their roots are a semitone apart, and
# the second is not in the key. The ear gets a chromatic root move and a
# foreign chord in the same instant and has nowhere to stand.
#
# `Bb - Bbm` is the same borrowed chord done properly. They share Bb and F,
# so ONE voice moves - D falls to Db - and the whole band does it together.
# It happens in the tune as well, in the top voice, where nobody can miss it:
# bar 14 sings D and bar 15 sings Db, and it is the same phrase both times.
CHORUS_A = [(V_F, 41), (V_F, 41), (V_CE, 40), (V_CE, 40),
            (V_DM7, 38), (V_DM7, 38), (V_BB, 34), (V_BB, 34)]
CHORUS_B = [(V_F, 41), (V_F, 41), (V_CE, 40), (V_CE, 40),
            (V_DM7, 38), (V_BB, 34), (V_BBM, 34), (V_C7, 36)]
# ii - V - iii - vi - ii - V - IV - iv.  Every change here has common tones,
# which the ladder it replaces did not.
LIFT   = [(V_GM7, 43), (V_C7, 36), (V_AM7, 33), (V_DM7, 38),
          (V_GM7, 43), (V_C7, 36), (V_BB, 34), (V_BBM, 34)]
VERSE  = [(V_DM7, 38), (V_BB, 34), (V_F, 41), (V_C, 36),
          (V_DM7, 38), (V_BB, 34), (V_GM7, 43), (V_C7, 36)]
# D minor, and the last two bars are D7 - the V of the key the record has
# not been in yet
BRIDGE = [(V_DM7, 38), (V_DM7, 38), (V_BBMAJ, 34), (V_BBMAJ, 34),
          (V_GM7, 43), (V_GM7, 43), (V_A7, 33), (V_A7, 33),
          (V_DM7, 38), (V_DM7, 38), (V_BBMAJ, 34), (V_BBMAJ, 34),
          (V_GM7, 43), (V_A7, 33), (V_D7, 38), (V_D7, 38)]

def up(sec, k):
    return [(tuple(n + k for n in v), r + k) for v, r in sec]

def padof(chord, root):
    """The string machine's job is the TOP of the chord, not the middle.

    Voiced down to the root it spans MIDI 34 to 70 and lands squarely on the
    guitar - and 200-800 Hz already has an owner. Everything here sits at 60
    and above, so the pad is the air over the band rather than a second
    rhythm guitar holding its notes down."""
    return tuple(sorted(set(chord[1:]) | {n + 12 for n in chord[:3]}))


# ================================================================= tune ===
# ONE RHYTHMIC CELL, AND IT IS A TRESILLO.
#
#     step:  0  .  .  3  .  .  6  .  8  ...............
#            x        x        x     X———————————————
#
# 3 + 3 + 2, and then the fourth note holds for half the bar. It is the most
# widespread rhythm on earth, a crowd can clap it, and every ODD bar of the
# chorus is that cell and nothing else. The even bars answer it in long
# notes. So the listener learns the rhythm in bar 1 and hears it three more
# times before the section is over - which is what a hook is, and what a
# melody whose rhythm changes every bar can never be.
def cell(a, b, c, d, v=1.0):
    # The held note stops at step 14, not at the bar line. A singer breathes,
    # and two sixteenths of silence at the end of every cell is the
    # difference between a phrase and a drone.
    return ((0, a, 3, v), (3, b, 3, v * 0.94), (6, a, 2, v * 0.90),
            (8, d, 6, v))

def answer(*ns, v=1.0):
    """long notes, and the last one ends before the bar does"""
    L = 16 // len(ns)
    return tuple((i * L, n, L - (3 if i == len(ns) - 1 else 0), v - 0.04 * i)
                 for i, n in enumerate(ns))

MEL_A = [
    cell(69, 72, 69, 77),               # F     3  5  3  root(8)
    answer(76, 74, 72),                 # F     maj7 6 5
    cell(67, 72, 67, 76),               # C/E   5  root 5  3
    answer(74, 72),                     # C/E   9  root
    cell(69, 74, 69, 77),               # Dm7   5  root 5  b3
    answer(79, 77, 76),                 # Dm7   11 b3 9    <- the peak, G5
    cell(74, 77, 74, 70),               # Bb    3  5  3  root
    answer(72, 69),                     # Bb    9  maj7
]
# the second time through, one note in the cell flattens and that is the
# whole point of the record
MEL_B = MEL_A[:5] + [
    answer(74, 77, 74),                 # Bb    3  5  3
    cell(73, 77, 73, 70),               # Bbm   b3 5  b3 root   <- D became Db
    answer(72, 70, 69),                 # C7    root b7 13
]
# the pre-chorus does not use the cell - the cell is saved for the chorus -
# and it ends on the same D-to-Db, so the gesture arrives twice
MEL_L = [
    ((0, 65, 6, 0.85), (6, 67, 9, 0.88)),      # Gm7  b7 root
    ((0, 67, 6, 0.88), (6, 72, 9, 0.92)),      # C7   5  root
    ((0, 72, 6, 0.90), (6, 69, 9, 0.88)),      # Am7  b3 root
    ((0, 69, 13, 0.90),),                      # Dm7  5
    ((0, 70, 6, 0.90), (6, 72, 9, 0.92)),      # Gm7  b3 4
    ((0, 74, 6, 0.95), (6, 72, 9, 0.95)),      # C7   9  root
    ((0, 74, 8, 1.00), (8, 74, 6, 0.95)),      # Bb   3, held
    ((0, 73, 14, 1.00),),                      # Bbm  b3 - the D falls to Db
]
MEL_V = [
    ((2, 62, 3, 0.80), (5, 65, 3, 0.85), (8, 69, 7, 0.88)),   # Dm7
    ((0, 70, 4, 0.85), (4, 69, 3, 0.80), (8, 65, 8, 0.82)),   # Bb
    ((2, 65, 3, 0.82), (5, 69, 3, 0.85), (8, 72, 8, 0.90)),   # F
    ((0, 71, 6, 0.86), (8, 67, 8, 0.82)),                     # C   (B natural = 3)
    ((2, 62, 3, 0.80), (5, 65, 3, 0.85), (8, 69, 7, 0.88)),   # Dm7
    ((0, 70, 4, 0.85), (4, 74, 3, 0.88), (8, 70, 8, 0.86)),   # Bb
    ((2, 65, 4, 0.84), (6, 67, 4, 0.88), (10, 70, 6, 0.90)),  # Gm7
    ((0, 72, 8, 0.92), (8, 70, 8, 0.86)),                     # C7
]
MEL_BR = [
    ((0, 69, 8, 0.82), (8, 72, 8, 0.86)),      # Dm  5  b7
    ((0, 74, 12, 0.88),),                      # Dm  root
    ((0, 72, 8, 0.86), (8, 69, 8, 0.82)),      # Bb  9  maj7
    ((0, 70, 12, 0.84),),                      # Bb  root
    ((0, 70, 8, 0.86), (8, 74, 8, 0.90)),      # Gm7 b3 5
    ((0, 77, 12, 0.94),),                      # Gm7 b7
    ((0, 76, 8, 0.90), (8, 73, 8, 0.86)),      # A7  5  3
    ((0, 69, 12, 0.92),),                      # A7  root
    ((0, 69, 8, 0.88), (8, 72, 8, 0.92)),      # Dm
    ((0, 74, 12, 0.94),),
    ((0, 77, 8, 0.96), (8, 74, 8, 0.92)),      # Bb  5  3
    ((0, 70, 12, 0.94),),
    ((0, 74, 8, 0.92), (8, 77, 8, 0.94)),      # Gm7 5  b7
    ((0, 76, 12, 0.96),),                      # A7  5
    ((0, 74, 8, 1.00), (8, 78, 8, 1.00)),      # D7  root 3   <- the F# arrives
    ((0, 74, 14, 1.00),),                      # D7  root - the pivot into G
]


# The second singer, and she sings CHORD TONES.
#
# A fixed table - "a diatonic third below, in the key" - is right for every
# chord that is in the key and catastrophically wrong for the one that is
# not. Two women at one microphone do not transpose the tune, they find the
# note under it that is IN THE CHORD, and which note that is changes bar by
# bar. Preference order is a third first, then a fourth or fifth, then a
# sixth. Never a second and never a tritone.
def pcs(voicing, root):
    return {n % 12 for n in voicing} | {root % 12}

def under(bar, tones):
    out = []
    for s, n, l, v in bar:
        below = next((n - d for d in (3, 4, 5, 7, 8, 9, 12)
                      if (n - d) % 12 in tones), n - 4)
        out.append((s, below, l, v * 0.88))
    return tuple(out)


# ================================================================= bass ===
# Octave eighths half-muted, and the last eighth of the bar walks into the
# next root. At 126 this is the engine of the whole record.
def bassbar(root, nxt=None, sparse=False, drive=1.0, walk=True):
    dec = 0.30 if sparse else 0.145
    ev = []
    for i, s in enumerate(range(0, 16, 2)):
        if sparse and s in (6, 10, 14):
            continue
        hi = (i % 2 == 1)
        v = (0.74 if hi else 1.0) * (0.87 + 0.13 * (s % 8 == 0))
        ev.append((s, root + (12 if hi else 0), dec, v * drive))
    if walk and nxt is not None and nxt != root:
        d = nxt - root
        app = nxt - 1 if abs(d) > 2 else root + (1 if d > 0 else -1)
        ev[-1] = (14, root + 12, 0.10, 0.62 * drive)
        ev.append((15, app, 0.12, 0.68 * drive))
    return tuple(ev)


CHANK_FULL = tuple((s, 0.95 if s % 4 == 0 else (0.70 if s % 2 == 0 else 0.52),
                    s % 2 == 1) for s in range(16))
CHANK_HALF = tuple(e for e in CHANK_FULL if e[0] % 2 == 0)
CHANK_OFF = tuple(e for e in CHANK_FULL if e[0] % 4 == 2)


# ================================================================ session ==
S = Session(NB, tail=3.0)
S.DUCKED = {'bass': 0.55, 'mach': 0.40, 'strings': 0.20, 'vox': 0.18}


# FOUR OPEN HATS A BAR IS HALF THE TOP END OF THE RECORD.
#
# Measured on one chorus bar, weighted by count and gain: dopen x4 was 49.6%
# of everything between 3 and 16 kHz, against 23.3% for the snare and 15.2%
# for the tambourine. Each hat does stop before the next one arrives - it
# rings 258 ms and they are 476 ms apart - and four of them a bar is STILL a
# continuous sheet of sand, because the question is not whether one overlaps
# the next, it is how much of the spectrum they own between them.
#
# So: open on the "and" of 1 and 3 only, the other two offbeats closed. That
# is still unmistakably the genre, it drops the open hat to about a fifth of
# the top end, and it leaves all four as something the last chorus can spend.
def kit(b, level=1.0, opens=(2, 10), hats=True, clap=True, tamb=1.0,
        ghosts=True, sixteen=False, fill=False, ride=0.0):
    sd = lambda k: (b * 37 + k) % 89
    for beat in range(4):
        s = beat * 4
        S.place(P(b, s), dkick(4, seed=sd(s), gain=0.98 if beat in (0, 2) else 0.91),
                level, 'drums')
        S.hit(P(b, s))
    for s in (4, 12):
        S.place(P(b, s), dsnare(4, seed=sd(s + 3)), level * 0.90, 'drums')
        if clap:
            S.place(P(b, s + 0.05), dclap(3, seed=sd(s + 5)), level * 0.76, 'perc')
    if ghosts:
        for s in (7, 11, 15):
            if (b * 3 + s) % 5:
                S.place(P(b, D.sw(s)), dsnare(2, seed=sd(s + 7), ghost=1.0, room=0.5),
                        level * 0.30, 'drums')
    if ride:
        # Quarter notes with a short wash. Eighths at the stock 1.9 s decay
        # measured 536 ms of ring against a 238 ms gap - each hit landing on
        # top of the two before it, which is a noise bed and not a cymbal.
        for s in range(0, 16, 4):
            S.place(P(b, D.sw(s)), dride(4, seed=sd(s + 29), decay=0.95,
                                         bell=1.0 if s == 0 else 0.0),
                    level * ride * (0.95 if s == 0 else 0.66), 'hats')
    if hats:
        for s in range(16):
            if s in opens:
                S.place(P(b, s), dopen(3, seed=sd(s + 11), tail=0.140),
                        level * 0.70, 'hats')
            elif s % 2 == 0 or sixteen:
                v = 0.88 if s % 4 == 0 else (0.62 if s % 2 == 0 else 0.44)
                S.place(P(b, D.sw(s)), dhat(1, seed=sd(s + 13),
                                            foot=0.35 if s % 4 == 2 else 0.0),
                        level * v, 'hats')
    if tamb:
        for s in range(0, 16, 2):
            S.place(P(b, D.sw(s)), dtamb(1, seed=sd(s + 17), ring=0.16,
                                         shake=0.45 if s % 4 == 0 else 0.0),
                    level * tamb * (0.80 if s % 4 == 0 else 0.42), 'perc')
    if fill:
        for i, (s, tn) in enumerate(((10, 218), (11, 192), (12, 165), (13, 165),
                                     (14, 136), (15, 136))):
            S.place(P(b, s), dtom(2, tune=tn, seed=sd(s + 19)),
                    level * (0.56 + 0.09 * i), 'drums')


def percbar(b, level=1.0, quinto=True):
    sd = lambda k: (b * 53 + k) % 97
    for s, st, g in ((0, 'heel', 0.42), (3, 'open', 0.62), (6, 'open', 0.70),
                     (8, 'heel', 0.40), (11, 'open', 0.60), (14, 'slap', 0.72)):
        S.place(P(b, D.sw(s)), conga(CONGA, st, 2.4, seed=sd(s)), level * g, 'perc')
    if quinto and b % 2 == 1:
        for s, st, g in ((10, 'slap', 0.50), (12, 'open', 0.44), (15, 'slap', 0.46)):
            S.place(P(b, D.sw(s)), conga(QUINTO, st, 1.8, seed=sd(s + 5)),
                    level * g, 'perc')


def chankbar(b, chord, pat=CHANK_FULL, level=1.0, mute=0.85, bright=1.0):
    for s, v, u in pat:
        S.place(P(b, D.sw(s)), chank(chord, 1.2, take=(b * 16 + s) % 5,
                                     mute=mute, bright=bright, up=u),
                level * v, 'gtr')


# Benny's right hand: the chord in the left, the HOOK in octaves in the right.
def pianobar(b, chord, root, mel=None, level=1.0, oct_=True, vel=0.80):
    """Benny's two hands, and they are not in the same place.

    The left is a SHELL - the root and its fifth, two notes, nothing between
    them. A block chord down there sits at MIDI 43-58, which is exactly where
    the guitar's fundamentals are, and a fifth part in that octave is how a
    record ends up with no edges in it. The right plays the TUNE in octaves,
    up where nothing else is."""
    ev = [(0, (root + 12, root + 19), 0.85), (8, (root + 12, root + 19), 0.58)]
    if mel and oct_:
        for s, n, l, v in mel:
            ev.append((s, (n, n + 12), 0.55 + 0.45 * v))
    S.place(P(b), grand(tuple(ev), 16, level=level, vel=vel,
                        seed=(b * 7) % 61), 1.0, 'keys')


def stadium(bars, roar=0.5, seed=0, tone=1900):
    """Forty thousand people, heard from the stage.

    `core.crowd` is band-limited noise centred on 300-2600 Hz, and that is
    correct - a crowd IS noise. But it was placed here for eight bars under
    the break and THIRTY-TWO under the finale, where it stops being an event
    and becomes a bed: background sand, in the one band the band itself is
    trying to be heard in.

    Two fixes and neither is a fader. Air absorbs high frequencies over
    distance, so a crowd forty metres away has nothing above about 2 kHz -
    lowpass it and it moves from being in the room to being out there. And
    it is used where it MEANS something: the moment a section lands, and the
    moment it ends. Never underneath one."""
    return lp(crowd(16 * bars, gain=1.0, roar=roar, seed=seed), tone, order=2)


def sing(b, bar_notes, tones=None, level=1.0, vowel='ah', harm=True, take=0,
         seed=0):
    """Two singers, each tripled by a tape machine. `tones` is the chord they
    are standing on, because the lower voice is chosen out of it."""
    if not bar_notes:
        return
    # ABBA is TWO women tripled by a tape machine - six voices, not fourteen.
    # Seven singers a part, holding long notes, measured 36% of 200-800 Hz and
    # 42% of 800-3000: more than three times the guitar, and a sustained
    # source that owns two bands is not a choir, it is a bed of noise that
    # everything else has to be heard through.
    S.place(P(b), voices(bar_notes, 1, tail=8, vowel=vowel, seed=b + seed,
                         singers=4, take=take), level, 'vox')
    if harm and tones:
        # and the lower voice sits IN the crowded band, so it is the one that
        # has to give: three singers, well under the tune, further off centre
        S.place(P(b), voices(under(bar_notes, tones), 1, tail=8, vowel=vowel,
                             seed=b + seed + 41, singers=3, take=take + 1),
                level * 0.50, 'vox')


# ================================================================ arrange ==
# ---- OPEN (0-7): the hook stated once, and forty thousand people ---------
S.place(P(0), stadium(4, roar=0.22, seed=5), 0.30, 'fx')
for j, b in enumerate((0, 2, 4, 6)):
    ch, root = CHORUS_A[j * 2]
    S.place(P(b), grand(((0, tuple(n - 12 for n in ch[:3]) + (root + 12,), 0.80),
                         (8, tuple(n - 12 for n in ch[:3]), 0.55)), 32,
                        level=1.0, vel=0.70, seed=b), 0.95, 'keys')
    S.place(P(b), solina([padof(ch, root)] * 2, level=1.0, attack=0.8,
                         release=1.5, tail_steps=14), 1.10, 'mach')
for j in range(4, 8):
    S.place(P(j), violins(MEL_A[j], 1, tail=8, seed=j, octave=0.55,
                          attack=0.35, vib=0.9), 0.78, 'strings')
S.place(P(6), strum((45, 52, 57, 61, 64, 69), 16, take=1, twelve=0.9), 0.60, 'gtr')

# ---- VERSE 1 (8-23) -----------------------------------------------------
for b in range(8, 24):
    j = (b - 8) % 8
    ch, root = VERSE[j]
    nxt = VERSE[(j + 1) % 8][1]
    lv = D.ramp(0.72, 1.0, min(b - 8, 8), 9)
    kit(b, level=lv, opens=(2, 10),
        clap=b >= 12, tamb=0.0 if b < 12 else 0.9, ghosts=b >= 16,
        ride=0.55 if b >= 16 else 0.0, fill=(b == 23))
    S.place(P(b), dbass(bassbar(root, nxt, sparse=b < 10), 16, tail=6,
                        take=b % 4), lv * 0.96, 'bass')
    chankbar(b, ch, CHANK_OFF if b < 12 else CHANK_FULL, level=lv * 0.92)
    if b >= 16:
        percbar(b, level=lv * 0.85, quinto=b >= 20)
    if b >= 12:
        S.place(P(b), rhodes(tuple(n - 12 for n in ch), 8, level=0.55, vel=0.7,
                             take=b % 4), 0.62, 'keys')
    if b >= 16:
        sing(b, MEL_V[j], pcs(ch, root), level=0.70, vowel='oo',
             harm=(b >= 20), seed=3)

# ---- LIFT (24-31): the pre-chorus, and it ends on a held leading tone ----
def liftblock(b0, key=0, level=1.0, seed=0, into=41):
    """`into` is the root of the bar AFTER this block - the chorus's first
    chord. Left to wrap around to its own bar 0 the bass walks into the wrong
    note at the one seam where everybody is listening."""
    for j in range(8):
        b = b0 + j
        ch, root = up(LIFT, key)[j]
        nxt = up(LIFT, key)[j + 1][1] if j < 7 else into
        lv = level * D.ramp(0.86, 1.10, j, 8, 1.2)
        kit(b, level=lv, opens=(2, 10), tamb=1.00,
            sixteen=(j >= 6), fill=(j == 7))
        S.place(P(b), dbass(bassbar(root, nxt), 16, tail=6, take=b % 4),
                lv * 0.96, 'bass')
        chankbar(b, ch, CHANK_FULL, level=lv * 1.0, bright=1.0 + 0.03 * j)
        percbar(b, level=lv * 0.9)
        pianobar(b, ch, root, level=0.55, oct_=False, vel=0.72)
        m = tuple((s, n + key, l, v) for s, n, l, v in MEL_L[j])
        sing(b, m, pcs(ch, root), level=0.86 * lv, vowel='ah', seed=seed)
        S.place(P(b), violins(m, 1, tail=8, seed=b + seed, octave=0.5,
                              attack=0.05), 0.62 * lv, 'strings')
        if j >= 4:
            S.place(P(b), solina([padof(ch, root)] * 2, level=1.0, attack=0.35,
                                 tail_steps=10), 0.60, 'mach')
liftblock(24)

# ---- CHORUS -------------------------------------------------------------
def chorusblock(b0, chords, mel, key=0, level=1.0, strings_mel=0.85,
                horns=True, twelve=0.85, take=0, seed=0, big=False):
    ch8 = up(chords, key)
    for j in range(8):
        b = b0 + j
        ch, root = ch8[j]
        nxt = ch8[(j + 1) % 8][1]
        m = tuple((s, n + key, l, v) for s, n, l, v in mel[j])
        kit(b, level=level, opens=(2, 6, 10, 14) if big else (2, 10),
            tamb=1.05, ride=0.40 if big else 0.0, fill=(j == 7))
        S.place(P(b), dbass(bassbar(root, nxt), 16, tail=6, take=(b + take) % 4),
                level * 0.98, 'bass')
        chankbar(b, ch, CHANK_FULL, level=level * 1.0)
        percbar(b, level=level * 0.95)
        pianobar(b, ch, root, mel=m, level=0.72, vel=0.86)
        sing(b, m, pcs(ch, root), level=1.0 * level, vowel='ah', seed=seed,
             take=take)
        if strings_mel:
            S.place(P(b), violins(tuple((s, n + 12, l, v) for s, n, l, v in m),
                                  1, tail=8, seed=b + seed, octave=0.7,
                                  attack=0.042, gliss=0.014),
                    level * strings_mel, 'strings')
        if twelve and j % 2 == 0:
            S.place(P(b), strum(tuple(n - 12 for n in ch) + (ch[3],), 16,
                                take=(b + j) % 4, twelve=twelve,
                                up=(j % 4 == 2)), level * 0.72, 'gtr')
        if j % 2 == 0:
            pads = [padof(ch8[k][0], ch8[k][1]) for k in (j, j + 1)]
            S.place(P(b), solina([pads[0]] * 2 + [pads[1]] * 2, level=1.0,
                                 attack=0.35, tail_steps=12), level * 0.66, 'mach')
    if horns:
        for j in (0, 2, 4, 6):                      # the cell bars only
            b = b0 + j
            ch, root = ch8[j]
            tones = pcs(ch, root)
            m = tuple((s, n + key, l, v) for s, n, l, v in mel[j])
            mid = under(m, tones)
            low = under(mid, tones)
            for (s, n, l, v), (_, n2, _, _), (_, n3, _, _) in zip(m, mid, low):
                S.place(P(b, s), brass((n3, n2, n),
                                       max(l, 1.5), take=(b * 4 + int(s)) % 4,
                                       scoop=1.0, hold=0.45,
                                       fall=1.8 if (j == 6 and s >= 8) else 0.0),
                        level * 0.72 * v, 'horns')

chorusblock(32, CHORUS_A, MEL_A, level=1.0, strings_mel=0.0, seed=0)
chorusblock(40, CHORUS_B, MEL_B, level=1.0, strings_mel=0.80, seed=7, take=2)
S.place(P(32), dcrash(16, seed=2, decay=1.2), 0.42, 'perc')
S.place(P(31, 10), sweep(64, 79, 6, seed=5), 0.26, 'fx')
S.place(P(32), stadium(2, roar=0.8, seed=11), 0.34, 'fx')

# ---- VERSE 2 (48-63) ----------------------------------------------------
for b in range(48, 64):
    j = (b - 48) % 8
    ch, root = VERSE[j]
    nxt = VERSE[(j + 1) % 8][1]
    kit(b, level=0.94, opens=(2, 10), tamb=0.90, ride=0.0,
        fill=(b == 63))
    S.place(P(b), dbass(bassbar(root, nxt), 16, tail=6, take=b % 4), 0.94, 'bass')
    chankbar(b, ch, CHANK_FULL, level=1.06, bright=1.08)
    percbar(b, level=0.92)
    S.place(P(b), rhodes(tuple(n - 12 for n in ch), 8, level=0.60, vel=0.75,
                         take=b % 4), 0.66, 'keys')
    sing(b, MEL_V[j], pcs(ch, root), level=0.82, vowel='oo', seed=13)
    if b % 4 == 0:
        S.place(P(b), strum(tuple(n - 12 for n in ch) + (ch[3],), 16,
                            take=b % 4, twelve=0.7), 0.50, 'gtr')
    if j in (6, 7):
        S.place(P(b), violins(MEL_V[j], 1, tail=8, seed=b, octave=0.45,
                              attack=0.06), 0.52, 'strings')

# ---- LIFT (64-71) and CHORUS 2 (72-87) ----------------------------------
liftblock(64, seed=17)
chorusblock(72, CHORUS_A, MEL_A, level=1.0, strings_mel=0.85, seed=21, take=1,
            twelve=0.9)
chorusblock(80, CHORUS_B, MEL_B, level=1.0, strings_mel=0.90, seed=27, take=3,
            twelve=0.9, big=True)
S.place(P(72), dcrash(16, seed=4, decay=1.2), 0.42, 'perc')

# ---- BREAK (88-95): bass, drums, hands, and the crowd -------------------
for b in range(88, 96):
    i = b - 88
    j = i % 8
    ch, root = CHORUS_A[j]
    nxt = CHORUS_A[(j + 1) % 8][1]
    kit(b, level=1.0, opens=(2, 6, 10, 14), tamb=1.05, clap=(i >= 4),
        sixteen=(i >= 6), fill=(i == 7))
    S.place(P(b), dbass(bassbar(root, nxt, drive=1.06), 16, tail=6,
                        take=b % 4, bright=1.15), 1.02, 'bass')
    percbar(b, level=1.15)
    for s in (5, 13):
        S.place(P(b, D.sw(s)), conga(TUMBA, 'open', 2.4, seed=(b * 7 + s) % 91),
                0.58, 'perc')
    if i >= 4:
        chankbar(b, ch, CHANK_OFF, level=0.70, mute=0.92)
# nothing under the break. It is bass, drums and hands, and the reason
# it works is that there is nothing else in it.
S.place(P(87, 12), stadium(1, roar=0.7, seed=17), 0.26, 'fx')

# ---- BRIDGE (96-111): F# minor, the drums stop for eight ----------------
for j in range(16):
    b = 96 + j
    ch, root = BRIDGE[j]
    nxt = BRIDGE[(j + 1) % 16][1]
    m = MEL_BR[j]
    if j < 8:
        S.place(P(b), dbass(((0, root, 2.4, 0.62), (10, root + 7, 1.5, 0.42)),
                            16, tail=8, take=j % 4, decay=2.4, growl=0.35,
                            bright=0.7), 0.64, 'bass')
        for s in (2, 6, 10, 14):
            S.place(P(b, s), dtamb(1, seed=(b * 11 + s) % 83, ring=0.5),
                    0.30 if j >= 4 else 0.0, 'perc')
        if j >= 4:
            S.place(P(b), strum(tuple(n - 12 for n in ch) + (ch[3],), 16,
                                take=j % 4, twelve=0.8), 0.46, 'gtr')
    else:
        lv = D.ramp(0.52, 1.00, j - 8, 8, 0.95)
        kit(b, level=lv, opens=(2, 10),
            clap=(j >= 12), tamb=0.75, ghosts=(j >= 12), ride=0.4 if j >= 12 else 0)
        S.place(P(b), dbass(bassbar(root, nxt, sparse=(j < 11)), 16, tail=6,
                            take=j % 4), lv * 0.94, 'bass')
        chankbar(b, ch, CHANK_HALF if j < 12 else CHANK_FULL, level=lv * 0.88)
        if j >= 12:
            percbar(b, level=lv * 0.8, quinto=False)
    pianobar(b, ch, root, level=0.62, oct_=False, vel=0.74)
    sing(b, m, pcs(ch, root), level=0.90,
         vowel='ah' if j >= 8 else 'oh', seed=31)
    if j % 2 == 0:
        pads = [padof(BRIDGE[k][0], BRIDGE[k][1]) for k in (j, j + 1)]
        S.place(P(b), solina([pads[0]] * 2 + [pads[1]] * 2, level=1.0,
                             attack=0.7, release=1.3, tail_steps=14), 0.90, 'mach')
    if j in (5, 7, 13, 15):
        S.place(P(b), violins(m, 1, tail=8, seed=b, octave=0.55, attack=0.05),
                0.66, 'strings')

# ---- BUILD (112-119): eight bars on F#7, and the last beat is empty ------
for j in range(8):
    b = 112 + j
    lv = D.ramp(0.76, 1.16, j, 8, 1.25)
    sd = lambda k: (b * 41 + k) % 89
    for beat in range(4):
        if j < 7 or beat < 3:
            S.place(P(b, beat * 4), dkick(4, seed=sd(beat * 4)), lv * 0.96, 'drums')
            S.hit(P(b, beat * 4))
    for s in (4, 12):
        if j < 7:
            S.place(P(b, s), dsnare(4, seed=sd(s + 3)), lv * 0.86, 'drums')
    for s in range(0, 16, 2 if j < 2 else 1):
        if j == 7 and s >= 12:
            continue
        S.place(P(b, D.sw(s)), dtamb(1, seed=sd(s + 17), ring=0.14),
                lv * (1.0 if s % 4 == 0 else 0.60), 'perc')
    if j >= 4:
        for s in range(0, 16, 2 if j < 6 else 1):
            if j == 7 and s >= 12:
                continue
            S.place(P(b, s), dsnare(1, seed=sd(s + 23), ghost=0.72, room=0.30),
                    lv * (0.20 + 0.028 * (s / 2)), 'drums')
    S.place(P(b), dbass(((0, 38, 0.40, 0.9), (4, 38, 0.40, 0.8),
                         (8, 38, 0.40, 0.9), (12, 38, 0.40, 0.8),
                         (14, 50, 0.28, 0.7)), 16, tail=6, take=j % 4,
                        drive=1.12 + 0.05 * j), lv * 0.92, 'bass')
    if j >= 1:
        chankbar(b, V_D7, CHANK_HALF if j < 4 else CHANK_FULL,
                 level=lv * 0.88, bright=1.0 + 0.05 * j)
    sing(b, ((0, 69 if j < 4 else 74, 15, 0.75 + 0.03 * j),), pcs(V_D7, 38),
         level=0.72, vowel='ah', harm=(j >= 4), seed=37)
S.place(P(112), solina([padof(V_D7, 38)] * 8, level=1.0, attack=0.9,
                       release=0.5, tail_steps=8), 0.88, 'mach')
S.place(P(112), sweep(50, 74, 64, seed=9, shape=2.1), 0.34, 'fx')
S.place(P(116), sweep(62, 79, 32, seed=13, shape=1.7), 0.22, 'fx')
S.place(P(118), stadium(2, roar=0.95, seed=23), 0.34, 'fx')
S.place(P(118), violins(((0, 62, 12, 0.6), (12, 66, 8, 0.7), (20, 69, 8, 0.85),
                         (28, 74, 4, 1.0)), 2, tail=6, seed=21, octave=0.5,
                        attack=0.03, gliss=0.05), 0.80, 'strings')

# ---- FINALE (120-151): B MAJOR, four times through ----------------------
KEY = 2
for k in range(4):
    b0 = 120 + k * 8
    chorusblock(b0, CHORUS_A if k % 2 == 0 else CHORUS_B,
                MEL_A if k % 2 == 0 else MEL_B, key=KEY, level=1.0,
                strings_mel=0.85 if k else 0.0, seed=40 + 5 * k, take=k,
                twelve=0.95, big=(k >= 2))
    if k in (0, 2):
        S.place(P(b0), dcrash(16, seed=30 + k, decay=1.3), 0.46, 'perc')
S.place(P(120), stadium(3, roar=0.9, seed=29), 0.36, 'fx')
# last time through, the choir opens into octaves: everybody is singing
for j in range(8):
    b = 144 + j
    m = tuple((s, n + KEY, l, v) for s, n, l, v in (MEL_A if 1 % 2 else MEL_B)[j])
    S.place(P(b), voices(tuple((s, n - 12, l, v * 0.75) for s, n, l, v in m),
                         1, tail=8, vowel='ah', seed=b + 71, take=2), 0.55, 'vox')
    S.place(P(b), violins(tuple((s, n - 12, l, v) for s, n, l, v in m), 1,
                          tail=8, seed=b + 9, octave=0.0, attack=0.05,
                          cutoff=5400), 0.40, 'strings')

# ---- OUT (152-163) ------------------------------------------------------
for j in range(12):
    b = 152 + j
    ch8 = up(CHORUS_A, KEY)
    ch, root = ch8[j % 8]
    nxt = ch8[(j + 1) % 8][1]
    lv = D.ramp(0.95, 0.34, j, 12, 1.3)
    kit(b, level=lv, opens=(2, 10),
        clap=(j < 5), tamb=1.0 if j < 8 else 0.0, ghosts=(j < 6))
    if j < 9:
        S.place(P(b), dbass(bassbar(root, nxt, sparse=(j >= 6)), 16, tail=6,
                            take=j % 4), lv * 0.92, 'bass')
    if j < 7:
        chankbar(b, ch, CHANK_FULL if j < 4 else CHANK_OFF, level=lv * 0.95)
    if j < 6:
        percbar(b, level=lv * 0.9, quinto=False)
    if j < 8:
        pianobar(b, ch, root, level=0.55, oct_=False, vel=0.70)
    if j % 4 == 0:
        pads = [padof(ch8[(j + i) % 8][0], ch8[(j + i) % 8][1]) for i in (0, 2)]
        S.place(P(b), solina([pads[0]] * 2 + [pads[1]] * 2, level=1.0,
                             attack=0.5, release=1.5, tail_steps=14),
                (0.80 if j < 8 else 1.00), 'mach')
    if j in (0, 4):
        m = tuple((s, n + KEY, l, v) for s, n, l, v in MEL_A[j % 8])
        sing(b, m, pcs(ch, root), level=0.70, vowel='ah', seed=61)
S.place(P(160), violins(((0, 73, 40, 0.45), (44, 68, 20, 0.40)), 3, tail=12,
                        seed=41, octave=0.6, attack=0.9, vib=0.6), 0.55, 'strings')
S.place(P(158), stadium(6, roar=0.30, seed=31), 0.34, 'fx')

# ---- seams --------------------------------------------------------------
for b in (23, 47, 63, 87, 95, 111, 151):
    S.place(P(b, 8), violins(((0, 64, 3, 0.5), (3, 68, 3, 0.6), (6, 71, 4, 0.7)),
                             1, tail=6, seed=b, octave=0.4, attack=0.05,
                             cutoff=4200), 0.32, 'strings')
for b in (8, 48, 88, 96, 152):
    S.place(P(b), dcrash(16, seed=(b + 3) % 71, decay=0.95), 0.26, 'perc')
D.throw(S, P(87, 14), brass((60, 65, 69), 2, take=1, fall=2.2), 0.40,
        steps_=3.0, times=4, fb=0.50)


# =================================================================== mix ===
print('rendered; mixing')

S.bus['drums'] = squash(S.bus['drums'], thresh=0.40, ratio=2.8, attack=0.018,
                        release=0.128, mix=0.85, report='drums')
S.bus['perc'] = squash(S.bus['perc'], thresh=0.16, ratio=3.0, attack=0.009,
                       release=0.124, mix=0.70, report='perc')
S.bus['bass'] = squash(S.bus['bass'], thresh=0.22, ratio=3.6, attack=0.014,
                       release=0.100, mix=0.88, report='bass')
S.bus['gtr'] = squash(S.bus['gtr'], thresh=0.14, ratio=2.6, attack=0.010,
                      release=0.132, mix=0.66, report='gtr')
S.bus['vox'] = squash(S.bus['vox'], thresh=0.15, ratio=3.2, attack=0.012,
                      release=0.115, mix=0.78, report='vox')
S.bus['keys'] = squash(S.bus['keys'], thresh=0.20, ratio=2.4, attack=0.014,
                       release=0.140, mix=0.60, report='keys')

t_all = np.arange(S.total) / SR
wah_env = 0.5 - 0.5 * np.cos(2 * np.pi * (BPM / 60 / 4) * t_all)
S.bus['gtr'] = phaser(S.bus['gtr'], lo=440, hi=2500, stages=4, depth=0.70,
                      env=wah_env * 0.85 + 0.08)
S.bus['gtr'] = S.bus['gtr'] - 0.20 * bandpass(S.bus['gtr'], 300, 620, order=2)

S.bus['drums'] = D.droom(S.bus['drums'], decay=0.52, wet=0.15, tone=6400)
S.bus['perc'] = D.droom(S.bus['perc'], decay=0.75, wet=0.22, tone=7200)
S.bus['gtr'] = D.droom(S.bus['gtr'], decay=0.70, wet=0.12, tone=5600)
S.bus['horns'] = D.droom(S.bus['horns'], decay=0.85, wet=0.20, tone=5200)
S.bus['keys'] = D.droom(S.bus['keys'], decay=0.95, wet=0.15, tone=5000)
# A stadium is a PLATE, and a big one. The voices live in it - a choir that
# is dry is a choir standing in a cupboard.
# FOUR THREE-SECOND TAILS IN A 1.9-SECOND BAR IS THE WASH.
#
# A convolution returns the whole spectrum, so an unfiltered reverb on four
# different buses lays four decaying copies of 200-800 Hz - the most crowded
# band there is - under everything, permanently. Every dry part is then
# competing with the ROOM of the parts beside it as well as with the parts
# themselves, and that is what "everything blurs into one indistinct noise"
# actually is. It is not an EQ problem and no fader fixes it.
#
# So: tails shorter than a bar, the wet path high-passed out of the mud, and
# 18-30 ms of pre-delay so the dry transient always arrives first.
S.bus['vox'] = bus_reverb(S.bus['vox'], decay=1.6, wet=0.30, tone=5200,
                          pre=0.028, hp_hz=430)
S.bus['strings'] = bus_reverb(S.bus['strings'], decay=1.9, wet=0.34, tone=4800,
                              pre=0.024, hp_hz=400)
S.bus['mach'] = bus_reverb(S.bus['mach'], decay=2.2, wet=0.26, tone=4200,
                           pre=0.020, hp_hz=460)
S.bus['fx'] = bus_reverb(S.bus['fx'], decay=2.6, wet=0.36, tone=5000,
                         pre=0.030, hp_hz=380)

S.bus['vox'] = S.bus['vox'] + 0.22 * np.roll(
    lp(narrow(S.bus['vox'], 0.5), 3400, order=2), int(3.0 * STEP), axis=0)

# One primary owner per band. The GUITAR owns 200-800 Hz - it is the
# sixteenth-note engine and that is where a chank lives - so everything else
# is cut there, and the guitar is cut at 2.4-3.2 kHz where the choir's
# singer's formant is, which is the one band a voice must have to itself.
S.bus['mach'] = S.bus['mach'] - 0.34 * bandpass(S.bus['mach'], 240, 620, order=2)
S.bus['keys'] = S.bus['keys'] - 0.30 * bandpass(S.bus['keys'], 300, 700, order=2)
S.bus['vox'] = S.bus['vox'] - 0.26 * bandpass(S.bus['vox'], 260, 540, order=2)
S.bus['horns'] = S.bus['horns'] - 0.24 * bandpass(S.bus['horns'], 280, 600, order=2)
S.bus['strings'] = S.bus['strings'] - 0.30 * bandpass(S.bus['strings'], 220, 600, order=2)
S.bus['gtr'] = S.bus['gtr'] - 0.28 * bandpass(S.bus['gtr'], 2400, 3200, order=2)
S.bus['mach'] = S.bus['mach'] - 0.22 * bandpass(S.bus['mach'], 2400, 3200, order=2)

for k in ('mach', 'strings', 'gtr', 'horns', 'fx', 'vox', 'keys'):
    S.bus[k] = mono_below(S.bus[k], 165)
S.bus['bass'] = mono_below(S.bus['bass'], 170)
S.bus['drums'] = mono_below(S.bus['drums'], 150)
# The air, and it is put in ABOVE the fatigue band on purpose. 2-5 kHz is
# where a record starts cutting; 11 kHz is where it starts sounding like it
# was made in a big room with expensive microphones.
for k in ('vox', 'strings', 'hats', 'perc'):
    S.bus[k] = shelf(S.bus[k], 11000, 2.4, 'high')
S.bus['strings'] = narrow(S.bus['strings'], 0.82)
S.bus['mach'] = narrow(S.bus['mach'], 0.62)
S.bus['fx'] = narrow(S.bus['fx'], 0.70)
S.bus['vox'] = narrow(S.bus['vox'], 0.68)
S.bus['hats'] = narrow(S.bus['hats'], 0.72)

# ---- the ride ------------------------------------------------------------
# The arrangement does the contrast; this only does the part it cannot -
# the dip in the bar before an arrival, and the climb across the intro.
ARC = [(0, -4.6), (7, -4.0), (8, -3.2), (22, -2.4), (23, -3.4),
       (24, -2.0), (30, -1.2), (31, -3.8),
       (32, -0.4), (46, -0.4), (47, -1.8),
       (48, -2.6), (62, -2.4), (63, -3.6),
       (64, -1.8), (70, -1.0), (71, -3.6),
       (72, -0.3), (86, -0.3), (87, -2.0),
       (88, -1.6), (94, -1.4), (95, -2.8),
       (96, -4.4), (103, -4.0), (104, -2.8), (111, -2.2),
       (112, -1.8), (117, -0.9), (118, -1.6), (119, -5.2),
       (120, 0.0), (143, 0.0), (144, 0.2), (151, 0.2),
       (152, -2.2), (158, -5.0), (163, -12.0), (NB, -20.0)]
t_bars = np.arange(S.total) / BAR
db = np.interp(t_bars, [p[0] for p in ARC], [p[1] for p in ARC])
ride = np.maximum(uniform_filter1d(10 ** (db / 20.0), int(0.030 * SR)), 0.0)
for k in S.bus:
    S.bus[k] = S.bus[k] * ride[:, None].astype(np.float32)
print(f'  ride: {db.min():.1f} to {db.max():.1f} dB across {NB} bars')

for k, dv in (('drums', 0.85), ('bass', 0.70), ('gtr', 0.55), ('perc', 0.45),
              ('horns', 0.60), ('keys', 0.45), ('mach', 0.35),
              ('strings', 0.30), ('vox', 0.35)):
    S.bus[k] = D.tape(S.bus[k], drive=dv, hiss=0.0, wow=0.55, seed=hash(k) % 97)

# ---- the faders ----------------------------------------------------------
TARGET = {'drums': 0.0, 'bass': -3.4, 'vox': -5.0, 'perc': -6.2,
          'strings': -7.0, 'keys': -8.0, 'gtr': -9.0, 'horns': -9.5,
          'mach': -12.5, 'hats': -13.2, 'fx': -18.0}
_w = slice(P(136), P(152))
_ref = S.loudness(S.bus['drums'][_w], pct=99)
GAINS = {}
for k in S.bus:
    lv = S.loudness(S.bus[k][_w], pct=99)
    GAINS[k] = (float(np.clip(10 ** ((_ref + TARGET[k] - lv) / 20), 0.05, 12.0))
                if lv > -70 else 1.0)
print('  faders: ' + '  '.join(f'{k} {v:.2f}' for k, v in sorted(GAINS.items())))

_sum = np.zeros_like(S.bus['drums'])
for _k, _b in S.bus.items():
    _sum += _b * GAINS[_k]
_scale = 2.00 / max(float(np.abs(_sum).max()), 1e-9)
GAINS = {k: v * _scale for k, v in GAINS.items()}
print(f'  master trim: {20*np.log10(_scale):+.1f} dB -> bus sum peaks 2.00')
del _sum

S.report(GAINS)
S.ownership(200, 800, GAINS, label='200-800 Hz (the crowded band)')
S.ownership(800, 3000, GAINS, label='800-3000 Hz (where a voice lives)')
S.ownership(3000, 16000, GAINS)
S.render('disco_ogni_126.wav', drive=0.0, duck=0.13, duck_rel=0.12,
         clip=1.50, peak=0.89, fade=3.0, gains=GAINS,
         comp=dict(thresh=0.30, ratio=1.8, attack=0.022, release=0.16),
         brick=dict(gain=1.24, ceiling=0.89))
