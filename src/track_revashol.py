"""РЕВАШОЛЬ - disco at 120 BPM, D minor, and it ends in E minor.

Revachol is the city in *Disco Elysium*: a place where a revolution was lost
fifty years ago, where everyone is still living in the rubble of it, and
where a broken man can nevertheless stand in a ruined church at dawn and
discover that his soul is tearing itself toward disco. That is the whole
brief. The record has to be ABBA and it has to be a-ha and it has to hurt.

Which is, conveniently, what disco already is. The genre's central trick -
and it is ABBA's above everyone's - is EUPHORIA IN A MINOR KEY. "Gimme!
Gimme! Gimme!" is D minor. "Money, Money, Money" is A minor with a raised
seventh. The four-to-the-floor says dance and the harmony says something else
entirely, and the listener does both.

    Dm11  -  Gm11  -  Bbmaj9  -  A7b9         i - iv - bVI - V
    Dm11  -  Gm11  -  Bbmaj9  -  Csus4/C      i - iv - bVI - bVII

Eight bars, one chord each, and the same three chords twice. Only the fourth
changes, and that is the whole sentence: the first half asks with a leading
tone (C# - theatrical, unresolved, the thing that makes minor-key ABBA ache),
the second half answers modally with no leading tone at all, which does not
resolve so much as LIFT. Question, then answer.

THE TOP VOICE OF THE GUITAR NEVER MOVES.

A4 sits on top of all four chords - the 5th of Dm, the 9th of Gm, the major
7th of Bb, the root of A7. One note, four meanings, and the harmony is heard
as a colour changing rather than as a sequence of blocks. It moves exactly
once, in bar 8, to say the loop is starting again.

The verses are somewhere else entirely: a two-chord Dorian vamp, `Dm9 - G13`,
where the B natural is the natural sixth. That is Chic, and it is cool rather
than sad - so the record spends its verses cool and its choruses grieving,
and the chorus arriving is a mode change as much as a section change.

THE SINGER IS A SYNTHESISER, ON PURPOSE.

There is a topline and no vocalist. Formant synthesis would produce a robot
pronouncing vowels. So the tune is given to `voice()` - three saws on one
continuous phase - and what makes it read as singing is not its spectrum, it
is that it SLIDES between notes and that its vibrato arrives a fifth of a
second after the note does, never with it. In the last chorus the string
section doubles it two octaves apart, which is the oldest way there is of
saying that everybody is singing now.

The tune, over the chorus:

    D5 C5 A4 ---- | Bb4 A4 G4 ---- | D5 ---- F5 ---- | E5 D5 C#5 ----
    D5 C5 A4 ---- | Bb4 A4 G4 ---- | D5 - F5 - G5 -- | E5 ---- D5 ------

An arch: it falls twice, climbs to F5, is held on the leading tone; then the
same two bars again and this time it goes past F to G5 before it comes down.
The peak is in bar 7 of 8 and it lands on the 13th of Bb.

AND THEN IT GOES UP A TONE.

The bridge modulates to F major - the relative major, the light - and holds
there for sixteen bars while the drums are gone. Its last bar is B7: a
semitone above the Bb that preceded it, and the dominant of a key the record
has not been in yet. Eight bars of build sit on that chord, and bar 128
arrives in E MINOR and stays there for thirty-two.

That is the truck-driver modulation, it is the cheapest device in pop music,
and it is what the last third of this record is for.

THE BAND BUDGET IS DECIDED HERE, NOT AT THE MIX.

    band       RUIN PULS BAND VERS CH1 VER2 BRK CH2 BRIDGE BUILD REVACHOL OUT
    20-60       -    x    X    X    X   X    X   X   -  x    -     X       x
    60-120      -    x    X    X    X   X    X   X   -  x    x     X       x
    120-800     x    x    x    x    X   x    x   X   x  x    x     X       x
    800-2.5k    x    x    x    X    X   X    x   X   x  x    X     X       x
    2.5-6k      -    x    x    x    X   x    x   X   -  x    X     X       x
    6-12k       -    x    X    X    X   X    X   X   -  -    X     X       -
    12k+        -    -    x    x    X   x    x   X   -  -    x     X       -

The bottom two octaves are ABSENT for the first eight bars and again for the
eight bars of the bridge where the drums stop - not turned down, not playing.
That is why bar 128 arrives, and it is a thing a gain ride cannot do.

    RUINS 8 | PULSE 8 | BAND 16 | VERSE 16 | CHORUS 16 | VERSE 2 16
    | BREAK 8 | CHORUS 2 16 | BRIDGE 16 | BUILD 8 | REVACHOL 32 | OUT 16

176 bars, 5:52 at 120 BPM. The peak starts at 128 - 73% of the way in - and
the sixteen bars in front of it have no bottom for half their length.

Mastered to about -10 LUFS. This genre is played by people and the dynamic
range is part of it; a disco record crushed to -7 stops being one.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d

import discolib as D
from discolib import *

BAR, STEP = D.set_tempo(120)
D.SWING = 0.055                     # 53.4% - the whole of disco's swing

np.random.seed(1977)
rs = np.random.RandomState(1977)

NB = 176
P = lambda b, s=0.0: int(round(b * BAR + s * STEP))


# ============================================================== material ===
# D natural minor: D E F G A Bb C.   D2 = 38, and the roots stay in 33-45,
# which is where a Precision is loudest and where a club system is flattest.
#
# The chorus. Read the last column down - A4, A4, A4, A4 - and then bar 8.
#   Dm11     G3 C4 F4 A4      11   b7   b3   5
#   Gm11     G3 C4 F4 A4      root 11   b7   9      (the same four notes)
#   Bbmaj9   A3 C4 F4 A4      maj7 9    5    maj7
#   A7b9     A3 C#4 G4 Bb4    root 3    b7   b9
#   Csus4    G3 C4 F4 G4      5    root 4    5
#   C        G3 C4 E4 G4      5    root 3    5
CH_DM   = (55, 60, 65, 69)
CH_GM   = (55, 60, 65, 69)
CH_BB   = (57, 60, 65, 69)
CH_A7   = (57, 61, 67, 70)
CH_CS   = (55, 60, 65, 67)
CH_C    = (55, 60, 64, 67)
# the Dorian vamp - the B natural in G13 is the character note of the verses
CH_DM9  = (55, 60, 65, 69)
CH_G13  = (55, 59, 65, 69)

CHORUS = [(CH_DM, 38), (CH_GM, 43), (CH_BB, 34), (CH_A7, 33),
          (CH_DM, 38), (CH_GM, 43), (CH_BB, 34), (CH_C,  36)]
VAMP   = [(CH_DM9, 38), (CH_G13, 43)]

# the bridge, in F major - I iii IV V, and the last bar is a semitone lift
# out of the key the record has been in for two minutes
CH_F    = (57, 60, 65, 69)          # A3 C4 F4 A4   Fmaj9 rootless: 3 5 root 3
CH_AM   = (57, 60, 64, 67)          # A3 C4 E4 G4   Am7
CH_BBB  = (57, 60, 65, 69)          # A3 C4 F4 A4   Bbmaj9: maj7 9 5 maj7
CH_C7   = (55, 60, 64, 67)
CH_B7   = (56, 59, 63, 69)          # G#3 B3 D#4 A4  B7: 6 root 3 b7
BRIDGE = [(CH_F, 41), (CH_AM, 33), (CH_BBB, 34), (CH_C7, 36),
          (CH_F, 41), (CH_AM, 33), (CH_BBB, 34), (CH_B7, 35)]

# E minor: everything above plus two, and the strings go with it
CHORUS_E = [(tuple(n + 2 for n in c), r + 2) for c, r in CHORUS]

# solina holds the same harmony an octave lower and wider
PAD_DM = (38, 50, 57, 62, 65)
def padof(chord, root):
    return tuple(sorted({root, root + 12} | {n - 12 for n in chord[:2]} | set(chord[1:])))


# ================================================================= tune ===
# (step, midi, length_steps, velocity). Two four-bar halves that begin the
# same and end differently - a period, and the second consequent goes higher.
TUNE = [
    ((0, 74, 3, 0.95), (3, 72, 2, 0.80), (6, 69, 8, 1.00)),
    ((0, 70, 3, 0.95), (3, 69, 2, 0.80), (6, 67, 9, 0.95)),
    ((0, 74, 6, 1.00), (6, 77, 9, 1.00)),
    ((0, 76, 3, 0.95), (3, 74, 2, 0.85), (6, 73, 9, 0.92)),
    ((0, 74, 3, 0.95), (3, 72, 2, 0.80), (6, 69, 8, 1.00)),
    ((0, 70, 3, 0.95), (3, 69, 2, 0.80), (6, 67, 9, 0.95)),
    ((0, 74, 4, 1.00), (4, 77, 4, 1.00), (8, 79, 8, 1.00)),
    ((0, 76, 6, 1.00), (6, 74, 11, 0.95)),
]
# The bridge tune is not a transposition. It is the one place on the record
# where the harmony is major, so it is allowed to be simple and to sit high.
TUNE_BR = [
    ((0, 72, 6, 0.82), (6, 74, 8, 0.86)),
    ((0, 76, 4, 0.88), (4, 74, 4, 0.82), (8, 72, 8, 0.86)),
    ((0, 70, 6, 0.88), (6, 74, 8, 0.92)),
    ((0, 76, 13, 0.95),),
    ((0, 77, 6, 0.98), (6, 76, 8, 0.90)),
    ((0, 74, 4, 0.88), (4, 72, 4, 0.84), (8, 69, 8, 0.86)),
    ((0, 70, 7, 0.92), (8, 72, 8, 0.94)),
    ((0, 71, 15, 1.00),),                       # B4 - the semitone lift into B7
]
TUNE_E = [tuple((s, n + 2, l, v) for s, n, l, v in bar) for bar in TUNE]

# The string section's answer: it plays in the holes the tune leaves, and it
# descends where the tune climbs. Four bars, then it rests for four.
ANSWER = [
    (),
    ((10, 62, 5, 0.55), (14, 65, 4, 0.60)),
    (),
    ((10, 69, 4, 0.62), (14, 67, 5, 0.66)),
    (),
    ((10, 62, 5, 0.55), (14, 65, 4, 0.60)),
    (),
    ((8, 72, 4, 0.70), (12, 70, 5, 0.72)),
]
# The lift: the whole section walking up in the last bar of a four, which is
# the transition device of the entire genre.
LIFT = ((0, 69, 2, 0.60), (2, 70, 2, 0.66), (4, 72, 2, 0.72),
        (6, 74, 2, 0.80), (8, 77, 4, 0.92), (12, 79, 6, 1.00))


# ================================================================= bass ===
# Octave eighths, the definitive disco gesture: root, octave, root, octave,
# every one of them half-muted so the hole between them is as loud as the
# note. The last eighth of the bar leaves the root and walks - chromatically
# where the next chord is a semitone away, by step where it is not - which is
# the single habit that turns a root-note bass into a line.
def bassbar(root, nxt=None, drive=1.0, sparse=False, walk=True):
    dec = 0.155 if not sparse else 0.30
    ev = []
    for i, s in enumerate(range(0, 16, 2)):
        if sparse and s in (6, 10, 14):
            continue
        hi = (i % 2 == 1)
        v = (0.72 if hi else 1.0) * (0.86 + 0.14 * (s % 8 == 0))
        ev.append((s, root + (12 if hi else 0), dec, v * drive))
    if walk and nxt is not None:
        d = nxt - root
        app = nxt - 1 if abs(d) > 2 else root + (1 if d > 0 else -1)
        ev[-1] = (14, root + 12, 0.11, 0.60 * drive)
        ev.append((15, app, 0.13, 0.66 * drive))
    return tuple(ev)


# ============================================================== the chank ==
# Sixteen strokes a bar and the hand never stops moving, so an "off" step is
# not a rest - it is the same stroke with the strings choked. Downstrokes on
# the beats, upstrokes between them; that alternation is the difference
# between a hand and a sequencer.
CHANK_FULL = tuple((s, 0.95 if s % 4 == 0 else (0.70 if s % 2 == 0 else 0.52),
                    s % 2 == 1) for s in range(16))
CHANK_HALF = tuple(e for e in CHANK_FULL if e[0] % 2 == 0)
CHANK_SKANK = tuple(e for e in CHANK_FULL if e[0] % 4 == 2)


# ================================================================ session ==
S = Session(NB, tail=3.0)
S.DUCKED = {'bass': 0.55, 'mach': 0.40, 'strings': 0.22}


def kit(b, level=1.0, opens=(2, 10), hats=True, clap=True, tamb=1.0,
        ghosts=True, sixteen=False, fill=False):
    """One bar of the kit. Every voice gets a seed derived from its position,
    because four hundred identical transients a minute is a metronome and not
    a drummer ([[a-repeated-hit-must-not-be-identical]])."""
    sd = lambda k: (b * 37 + k) % 89
    for beat in range(4):
        s = beat * 4
        S.place(P(b, s), dkick(4, seed=sd(s), gain=0.98 if beat in (0, 2) else 0.90),
                level, 'drums')
        S.hit(P(b, s))
    for s in (4, 12):
        S.place(P(b, s), dsnare(4, seed=sd(s + 3), gain=1.0), level * 0.88, 'drums')
        if clap:
            S.place(P(b, s + 0.06), dclap(3, seed=sd(s + 5)), level * 0.72, 'perc')
    if ghosts:
        for s in (7, 11, 15):
            if (b * 3 + s) % 5:
                S.place(P(b, D.sw(s)), dsnare(2, seed=sd(s + 7), ghost=1.0, room=0.5),
                        level * 0.30, 'drums')
    if hats:
        for s in range(16):
            if s in opens:
                S.place(P(b, s), dopen(3, seed=sd(s + 11)), level * 0.92, 'hats')
            elif s % 2 == 0 or sixteen:
                v = 0.88 if s % 4 == 0 else (0.62 if s % 2 == 0 else 0.44)
                S.place(P(b, D.sw(s)), dhat(1, seed=sd(s + 13),
                                            foot=0.35 if s % 4 == 2 else 0.0),
                        level * v, 'hats')
    if tamb:
        for s in range(0, 16, 2):
            v = 1.0 if s % 4 == 0 else 0.58
            S.place(P(b, D.sw(s)), dtamb(1, seed=sd(s + 17), ring=0.25,
                                         shake=0.5 if s % 4 == 0 else 0.0),
                    level * tamb * v, 'perc')
    if fill:
        for i, (s, tn) in enumerate(((10, 210), (11, 186), (12, 160), (13, 160),
                                     (14, 132), (15, 132))):
            S.place(P(b, s), dtom(2, tune=tn, seed=sd(s + 19)),
                    level * (0.55 + 0.09 * i), 'drums')


def percbar(b, level=1.0, quinto=True):
    """Congas. The tumbadora keeps the tumbao, the quinto answers it."""
    sd = lambda k: (b * 53 + k) % 97
    for s, st, g in ((0, 'heel', 0.42), (3, 'open', 0.62), (6, 'open', 0.70),
                     (8, 'heel', 0.40), (11, 'open', 0.60), (14, 'slap', 0.72)):
        S.place(P(b, D.sw(s)), conga(CONGA, st, 2.4, seed=sd(s)), level * g, 'perc')
    if quinto and b % 2 == 1:
        for s, st, g in ((10, 'slap', 0.50), (12, 'open', 0.44), (15, 'slap', 0.46)):
            S.place(P(b, D.sw(s)), conga(QUINTO, st, 1.8, seed=sd(s + 5)),
                    level * g, 'perc')


def chankbar(b, chord, pat=CHANK_FULL, level=1.0, mute=0.85, bright=1.0):
    for s, v, up in pat:
        S.place(P(b, D.sw(s)), chank(chord, 1.2, take=(b * 16 + s) % 5,
                                     mute=mute, bright=bright, up=up),
                level * v, 'gtr')


# ================================================================ arrange ==
# ---- RUINS (0-7): the string machine alone, and one bass note ------------
S.place(P(0), solina([padof(CH_DM, 38)] * 4 + [padof(CH_BB, 34)] * 2
                     + [padof(CH_GM, 43)] * 2, level=1.0, attack=0.9,
                     release=1.6, tail_steps=14), 1.35, 'mach')
S.place(P(0, 2), dbass(((0, 26, 3.2, 0.55),), 8, tail=10, take=1, decay=3.2,
                       growl=0.25, bright=0.5), 1.05, 'bass')
S.place(P(4), dbass(((0, 34, 3.0, 0.50),), 8, tail=10, take=2, decay=3.0,
                    growl=0.25, bright=0.5), 1.00, 'bass')
S.place(P(6), violins(((0, 69, 26, 0.42), (26, 65, 14, 0.38)), 2, tail=12,
                      octave=0.5, seed=11, attack=0.45, vib=0.7), 0.82, 'strings')

# ---- PULSE (8-15): the heartbeat, and nothing else ----------------------
for b in range(8, 16):
    lv = D.ramp(0.55, 1.0, b - 8, 8, 0.8)
    sd = lambda k: (b * 37 + k) % 89
    for beat in range(4):
        S.place(P(b, beat * 4), dkick(4, seed=sd(beat * 4)), lv, 'drums')
        S.hit(P(b, beat * 4))
    for s in (4, 12):
        S.place(P(b, s), drim(2, seed=sd(s)), lv * 0.7, 'drums')
    if b >= 10:
        for s in range(0, 16, 2):
            S.place(P(b, D.sw(s)), dhat(1, seed=sd(s + 13)),
                    lv * (0.80 if s % 4 == 0 else 0.50), 'hats')
    if b >= 12:
        S.place(P(b), solina([padof(CH_DM, 38)] * 2 + [padof(CH_GM, 43)] * 2,
                             level=1.0, attack=0.5, tail_steps=10)
                if b == 12 else np.zeros((1, 2), np.float32), 0.85, 'mach')
S.place(P(14), solina([padof(CH_BB, 34)] * 1 + [padof(CH_A7, 33)] * 1,
                      level=1.0, attack=0.4, tail_steps=10), 0.85, 'mach')

# ---- BAND (16-31) and VERSE (32-47): the Dorian vamp ---------------------
for b in range(16, 48):
    i = b - 16
    ch, root = VAMP[(b // 2) % 2]
    nxt = VAMP[((b // 2) + (1 if b % 2 else 0)) % 2][1] if b % 2 else None
    lv = D.ramp(0.70, 1.0, min(i, 8), 9)
    kit(b, level=lv, opens=(2, 10) if b < 24 else (2, 6, 10, 14),
        clap=b >= 20, tamb=0.0 if b < 22 else 1.0, ghosts=b >= 24,
        fill=(b % 16 == 15))
    S.place(P(b), dbass(bassbar(root, nxt, sparse=b < 18), 16, tail=6,
                        take=b % 4), lv * 0.95, 'bass')
    if b >= 20:
        chankbar(b, ch, CHANK_SKANK if b < 26 else CHANK_FULL,
                 level=lv * (0.85 if b < 32 else 1.0))
    if b >= 24:
        percbar(b, level=lv * 0.9, quinto=b >= 32)
    if b >= 28 and b % 4 == 0:
        S.place(P(b), solina([padof(ch, root)] * 2
                             + [padof(VAMP[1 - (b // 2) % 2][0],
                                      VAMP[1 - (b // 2) % 2][1])] * 2,
                             level=1.0, attack=0.45, tail_steps=12), 0.70, 'mach')
# the strings arrive at 40 - a bed, not a tune, and only for the second half
for b in range(40, 48, 4):
    ch, root = VAMP[(b // 2) % 2]
    S.place(P(b), violins(((0, 69, 30, 0.42), (32, 67, 30, 0.44)), 4, tail=10,
                          seed=b, octave=0.42, attack=0.35, vib=0.8),
            0.55, 'strings')
S.place(P(46), sweep(57, 72, 8, seed=3), 0.26, 'fx')

# ---- CHORUS 1 (48-63) ----------------------------------------------------
def chorus_block(b0, chords, tune, level=1.0, strings_mel=0.0, horns=True,
                 answer=True, lifts=(3, 7), key=0, take=0):
    for j in range(8):
        b = b0 + j
        ch, root = chords[j]
        nxt = chords[(j + 1) % 8][1]
        kit(b, level=level, opens=(2, 6, 10, 14), fill=(j == 7))
        S.place(P(b), dbass(bassbar(root, nxt), 16, tail=6, take=(b + take) % 4),
                level * 0.98, 'bass')
        chankbar(b, ch, CHANK_FULL, level=level * 1.0)
        percbar(b, level=level * 0.95)
    for j in range(0, 8, 2):
        b = b0 + j
        pads = [padof(chords[k][0], chords[k][1]) for k in (j, j + 1)]
        S.place(P(b), solina([pads[0]] * 2 + [pads[1]] * 2, level=1.0,
                             attack=0.40, tail_steps=12), level * 0.72, 'mach')
    # the tune
    for j in range(8):
        b = b0 + j
        if tune[j]:
            S.place(P(b), voice(tune[j], 1, tail=8, take=(b0 + j) % 4,
                                cut_hi=5800, glide=0.042),
                    level * 1.0, 'lead')
    # the section: an answer in the holes, a lift in the last bar of a four,
    # and - only in the last chorus - the tune itself, in octaves
    for j in range(8):
        b = b0 + j
        if strings_mel and tune[j]:
            mel = tuple((s, n + 12, l, v) for s, n, l, v in tune[j])
            S.place(P(b), violins(mel, 1, tail=8, seed=b, octave=0.75,
                                  attack=0.040, vib=1.0, gliss=0.014),
                    level * strings_mel, 'strings')
        elif answer and ANSWER[j]:
            a = tuple((s, n + key, l, v) for s, n, l, v in ANSWER[j])
            S.place(P(b), violins(a, 1, tail=8, seed=b, octave=0.5,
                                  attack=0.075), level * 0.85, 'strings')
        if j in lifts:
            lf = tuple((s, n + key, l, v) for s, n, l, v in LIFT)
            S.place(P(b), violins(lf, 1, tail=8, seed=b + 7, octave=0.35,
                                  attack=0.035, vib=0.8), level * 0.80, 'strings')
    if horns:
        for j, (s, notes) in enumerate((
                (1, (62, 65, 69)), (3, (60, 65, 69)),
                (5, (62, 65, 70)), (7, (60, 64, 67)))):
            b = b0 + s
            nn = tuple(n + key for n in notes)
            S.place(P(b, 10), brass(nn, 2, take=(b + j) % 4, scoop=1.0),
                    level * 0.62, 'horns')
            S.place(P(b, 14), brass(nn, 2, take=(b + j + 2) % 4, scoop=0.7,
                                    fall=1.4 if j == 3 else 0.0),
                    level * 0.55, 'horns')

# Sixteen bars: the eight-bar sentence twice. The second time through adds
# the string doubling and a bigger fill - a chorus repeats by definition, and
# the second pass earns its place by being one element bigger.
chorus_block(48, CHORUS, TUNE, level=1.00, answer=True, horns=True)
chorus_block(56, CHORUS, TUNE, level=1.00, answer=True, horns=True, take=2)
for j in (6, 7):
    b = 56 + j
    mel = tuple((st, n + 12, l, v) for st, n, l, v in TUNE[j])
    S.place(P(b), violins(mel, 1, tail=8, seed=b + 3, octave=0.7,
                          attack=0.048, gliss=0.014), 0.52, 'strings')
S.place(P(47, 10), sweep(64, 79, 6, seed=5), 0.26, 'fx')
S.place(P(48), dcrash(16, seed=2, decay=1.2), 0.40, 'perc')

# ---- VERSE 2 (64-79): the voice leaves, the guitar takes the front -------
for b in range(64, 80):
    i = b - 64
    ch, root = VAMP[(b // 2) % 2]
    nxt = VAMP[((b // 2) + (1 if b % 2 else 0)) % 2][1] if b % 2 else None
    lv = 0.90
    kit(b, level=lv, opens=(2, 6, 10, 14) if i >= 8 else (2, 10),
        tamb=0.85, fill=(i == 15))
    S.place(P(b), dbass(bassbar(root, nxt), 16, tail=6, take=b % 4), lv * 0.95, 'bass')
    chankbar(b, ch, CHANK_FULL, level=1.12, bright=1.1)
    percbar(b, level=lv)
    if b % 4 == 0:
        S.place(P(b), solina([padof(ch, root)] * 2
                             + [padof(VAMP[1 - (b // 2) % 2][0],
                                      VAMP[1 - (b // 2) % 2][1])] * 2,
                             level=1.0, attack=0.45, tail_steps=12), 0.58, 'mach')
    if i in (6, 14):
        S.place(P(b), violins(LIFT, 1, tail=8, seed=b, octave=0.4,
                              attack=0.045), 0.70, 'strings')

# ---- BREAK (80-87): bass, drums, hands, congas. Nothing else. ------------
for b in range(80, 88):
    i = b - 80
    ch, root = VAMP[(b // 2) % 2]
    nxt = VAMP[((b // 2) + (1 if b % 2 else 0)) % 2][1] if b % 2 else None
    kit(b, level=1.0, opens=(2, 6, 10, 14), tamb=1.15, clap=(i >= 4),
        sixteen=(i >= 6), fill=(i == 7))
    S.place(P(b), dbass(bassbar(root, nxt, drive=1.05), 16, tail=6,
                        take=b % 4, bright=1.15), 1.02, 'bass')
    percbar(b, level=1.15)
    for s in (5, 13):
        S.place(P(b, D.sw(s)), conga(TUMBA, 'open', 2.4, seed=(b * 7 + s) % 91),
                0.55, 'perc')

# ---- CHORUS 2 (88-103) ---------------------------------------------------
chorus_block(88, CHORUS, TUNE, level=1.0, strings_mel=0.0, answer=True,
             horns=True, take=2)
chorus_block(96, CHORUS, TUNE, level=1.0, strings_mel=0.0, answer=True,
             horns=True, take=1)
# the strings double the tune - one new element, which is what a second
# chorus is allowed and a first one is not
for b in (90, 91, 94, 95, 98, 99, 102, 103):
    j = b % 8
    mel = tuple((st, n + 12, l, v) for st, n, l, v in TUNE[j])
    S.place(P(b), violins(mel, 1, tail=8, seed=b + 3, octave=0.7,
                          attack=0.042, gliss=0.014), 0.58, 'strings')
S.place(P(88), dcrash(16, seed=4, decay=1.2), 0.40, 'perc')
S.place(P(87, 10), sweep(64, 81, 6, seed=7), 0.30, 'fx')

# ---- BRIDGE (104-119): F major. The drums stop. -------------------------
for j in range(8):
    b = 104 + j
    ch, root = BRIDGE[j]
    S.place(P(b), voice(TUNE_BR[j], 1, tail=8, take=(b + 1) % 4, cut_hi=5200,
                        glide=0.050, vib=1.15), 0.92, 'lead')
    if j % 2 == 0:
        pads = [padof(BRIDGE[k][0], BRIDGE[k][1]) for k in (j, j + 1)]
        S.place(P(b), solina([pads[0]] * 2 + [pads[1]] * 2, level=1.0,
                             attack=0.75, release=1.3, tail_steps=14), 0.95, 'mach')
    S.place(P(b), dbass(((0, root, 2.6, 0.62), (10, root + 7, 1.6, 0.44)), 16,
                        tail=8, take=j % 4, decay=2.6, growl=0.35, bright=0.7),
            0.62, 'bass')
    S.place(P(b), violins(((0, ch[2] + 12, 28, 0.40), (30, ch[3] + 12, 28, 0.44)),
                          2, tail=10, seed=b, octave=0.55, attack=0.42, vib=0.85)
            if j % 2 == 0 else np.zeros((1, 2), np.float32), 0.58, 'strings')
    for s in (2, 6, 10, 14):
        S.place(P(b, s), dtamb(1, seed=(b * 11 + s) % 83, ring=0.5),
                0.32 if j >= 4 else 0.0, 'perc')
# the drums walk back in for the second half of the bridge
for j in range(8, 16):
    b = 104 + j
    ch, root = BRIDGE[j - 8]
    lv = D.ramp(0.50, 0.95, j - 8, 8, 0.9)
    kit(b, level=lv, opens=(2, 10) if j < 12 else (2, 6, 10, 14),
        clap=(j >= 12), tamb=0.7, ghosts=(j >= 12))
    S.place(P(b), dbass(bassbar(root, BRIDGE[(j - 7) % 8][1], drive=0.9,
                                sparse=(j < 11)), 16, tail=6, take=j % 4),
            lv * 0.92, 'bass')
    S.place(P(b), voice(TUNE_BR[j - 8], 1, tail=8, take=(b + 2) % 4,
                        cut_hi=5600, glide=0.046), 0.96, 'lead')
    if j >= 11:
        chankbar(b, ch, CHANK_HALF if j < 13 else CHANK_FULL, level=lv * 0.85)
    if j >= 12:
        percbar(b, level=lv * 0.8, quinto=False)
    if j % 2 == 0:
        pads = [padof(BRIDGE[k][0], BRIDGE[k][1]) for k in (j - 8, j - 7)]
        S.place(P(b), solina([pads[0]] * 2 + [pads[1]] * 2, level=1.0,
                             attack=0.55, tail_steps=12), 0.75, 'mach')
    if j in (10, 14):
        S.place(P(b), violins(LIFT, 1, tail=8, seed=b, octave=0.4,
                              attack=0.05), 0.62, 'strings')

# ---- BUILD (120-127): eight bars on B7, and the last beat is empty -------
for j in range(8):
    b = 120 + j
    lv = D.ramp(0.72, 1.15, j, 8, 1.25)
    sd = lambda k: (b * 41 + k) % 89
    for beat in range(4):
        if j < 7 or beat < 3:
            S.place(P(b, beat * 4), dkick(4, seed=sd(beat * 4)), lv * 0.95, 'drums')
            S.hit(P(b, beat * 4))
    for s in (4, 12):
        if j < 7:
            S.place(P(b, s), dsnare(4, seed=sd(s + 3)), lv * 0.85, 'drums')
    rate = (2 if j < 2 else (1 if j < 5 else 1))
    for s in range(0, 16, rate):
        if j >= 6 and s >= 12 and j == 7:
            continue
        S.place(P(b, D.sw(s)), dtamb(1, seed=sd(s + 17), ring=0.15),
                lv * (1.0 if s % 4 == 0 else 0.62), 'perc')
    if j >= 4:
        step = 2 if j < 6 else 1
        for s in range(0, 16, step):
            if j == 7 and s >= 12:
                continue
            S.place(P(b, s), dsnare(1, seed=sd(s + 23), ghost=0.72, room=0.30),
                    lv * (0.20 + 0.028 * (s / 2)), 'drums')
    S.place(P(b), dbass(((0, 35, 0.42, 0.9), (4, 35, 0.42, 0.8),
                         (8, 35, 0.42, 0.9), (12, 35, 0.42, 0.8),
                         (14, 47, 0.30, 0.7)), 16, tail=6, take=j % 4,
                        drive=1.15 + 0.06 * j), lv * 0.92, 'bass')
    if j >= 1:
        chankbar(b, CH_B7, CHANK_HALF if j < 4 else CHANK_FULL,
                 level=lv * 0.85, bright=1.0 + 0.06 * j)
S.place(P(120), solina([padof(CH_B7, 35)] * 8, level=1.0, attack=0.9,
                       release=0.5, tail_steps=8), 0.85, 'mach')
S.place(P(120), sweep(59, 79, 64, seed=9, shape=2.1), 0.34, 'fx')
S.place(P(124), sweep(66, 83, 32, seed=13, shape=1.7), 0.22, 'fx')
S.place(P(126), violins(((0, 71, 12, 0.6), (12, 73, 8, 0.7), (20, 74, 8, 0.85),
                         (28, 78, 4, 1.0)), 2, tail=6, seed=21, octave=0.5,
                        attack=0.03, gliss=0.05), 0.78, 'strings')

# ---- REVACHOL (128-159): E minor, four times through --------------------
for k in range(4):
    b0 = 128 + k * 8
    chorus_block(b0, CHORUS_E, TUNE_E, level=1.0,
                 strings_mel=0.0 if k == 0 else 0.66,
                 answer=(k == 0), horns=True, key=2, take=k)
    if k in (0, 2):
        S.place(P(b0), dcrash(16, seed=30 + k), 0.60, 'perc')
# the last time through, the tune is doubled two octaves apart: everybody sings
for j in range(8):
    b = 152 + j
    if TUNE_E[j]:
        low = tuple((s, n - 12, l, v * 0.8) for s, n, l, v in TUNE_E[j])
        S.place(P(b), violins(low, 1, tail=8, seed=b + 5, octave=0.0,
                              attack=0.05, cutoff=5200), 0.44, 'strings')
        S.place(P(b), voice(TUNE_E[j], 1, tail=8, take=(b + 3) % 4,
                            cut_hi=6200, det=13.0, glide=0.038), 0.42, 'lead')

# ---- OUT (160-175): subtract; the machine is last -----------------------
for j in range(16):
    b = 160 + j
    ch, root = CHORUS_E[j % 8]
    nxt = CHORUS_E[(j + 1) % 8][1]
    lv = D.ramp(0.95, 0.30, j, 16, 1.35)
    kit(b, level=lv, opens=(2, 6, 10, 14) if j < 8 else (2, 10),
        clap=(j < 6), tamb=1.0 if j < 10 else 0.0, ghosts=(j < 8))
    if j < 12:
        S.place(P(b), dbass(bassbar(root, nxt, sparse=(j >= 8)), 16, tail=6,
                            take=j % 4), lv * 0.92, 'bass')
    if j < 10:
        chankbar(b, ch, CHANK_FULL if j < 6 else CHANK_SKANK, level=lv * 0.95)
    if j < 8:
        percbar(b, level=lv * 0.9, quinto=False)
    if j % 4 == 0:
        pads = [padof(CHORUS_E[(j + i) % 8][0], CHORUS_E[(j + i) % 8][1])
                for i in (0, 2)]
        S.place(P(b), solina([pads[0]] * 2 + [pads[1]] * 2, level=1.0,
                             attack=0.5, release=1.4, tail_steps=14),
                (0.75 if j < 12 else 0.95), 'mach')
    if j in (0, 4):
        S.place(P(b), violins(tuple((s, n + 12, l, v) for s, n, l, v in TUNE_E[j % 8]),
                              1, tail=8, seed=b, octave=0.6, attack=0.05), 0.50, 'strings')
S.place(P(172), violins(((0, 71, 40, 0.45), (44, 66, 20, 0.40)), 3, tail=12,
                        seed=41, octave=0.6, attack=0.9, vib=0.6), 0.52, 'strings')

# ---- seams --------------------------------------------------------------
for b in (16, 32, 64, 80, 104, 160):
    S.place(P(b), dcrash(16, seed=(b + 3) % 71, decay=0.95), 0.26, 'perc')
# and where a seam wants to be marked, the section does it: four notes of the
# chord walking up, which is a part rather than an effect
for b in (31, 63, 79, 103, 159):
    S.place(P(b, 8), violins(((0, 62, 3, 0.5), (3, 65, 3, 0.6), (6, 69, 4, 0.7)),
                             1, tail=6, seed=b, octave=0.4, attack=0.05,
                             cutoff=4200), 0.34, 'strings')
D.throw(S, P(103, 14), voice(((0, 74, 4, 0.9),), 1, tail=4, take=1), 0.42,
        steps_=3.0, times=5, fb=0.52)
D.throw(S, P(79, 14), brass((62, 65, 69), 2, take=1, fall=2.0), 0.40,
        steps_=3.0, times=4, fb=0.50)


# =================================================================== mix ===
print('rendered; mixing')

# The drum bus is one room, one console. `squash` is a bus compressor, not a
# limiter: 2-4 dB on the peaks is what makes a kit sound like a record.
S.bus['drums'] = squash(S.bus['drums'], thresh=0.40, ratio=2.8, attack=0.018,
                        release=0.135, mix=0.85, report='drums')
S.bus['perc'] = squash(S.bus['perc'], thresh=0.16, ratio=3.0, attack=0.009,
                       release=0.130, mix=0.70, report='perc')
S.bus['bass'] = squash(S.bus['bass'], thresh=0.22, ratio=3.6, attack=0.014,
                       release=0.105, mix=0.88, report='bass')
S.bus['gtr'] = squash(S.bus['gtr'], thresh=0.14, ratio=2.6, attack=0.010,
                      release=0.140, mix=0.66, report='gtr')
S.bus['lead'] = squash(S.bus['lead'], thresh=0.16, ratio=2.8, attack=0.012,
                       release=0.120, mix=0.72, report='lead')

# The wah is a PEDAL, and a pedal is rocked - so it is on the part, not in
# the voice. A fixed filter position on every hit would be a formant, which
# is to say a vowel, and a guitar that pronounces the same vowel sixteen
# times a bar for six minutes is the thing this is avoiding.
t_all = np.arange(S.total) / SR
wah_env = 0.5 - 0.5 * np.cos(2 * np.pi * (BPM / 60 / 4) * t_all)      # one bar
S.bus['gtr'] = phaser(S.bus['gtr'], lo=420, hi=2400, stages=4, depth=0.72,
                      env=wah_env * 0.85 + 0.08)
S.bus['gtr'] = S.bus['gtr'] - 0.22 * bandpass(S.bus['gtr'], 300, 620, order=2)

# one room for the band
S.bus['drums'] = D.droom(S.bus['drums'], decay=0.58, wet=0.17, tone=6400)
S.bus['perc'] = D.droom(S.bus['perc'], decay=0.72, wet=0.22, tone=7200)
S.bus['gtr'] = D.droom(S.bus['gtr'], decay=0.85, wet=0.16, tone=5600)
S.bus['horns'] = D.droom(S.bus['horns'], decay=1.05, wet=0.28, tone=5200)
S.bus['strings'] = bus_reverb(S.bus['strings'], decay=2.6, wet=0.40, tone=4800)
S.bus['lead'] = bus_reverb(S.bus['lead'], decay=1.5, wet=0.20, tone=5000)
S.bus['mach'] = bus_reverb(S.bus['mach'], decay=3.2, wet=0.30, tone=4200)
S.bus['fx'] = bus_reverb(S.bus['fx'], decay=3.0, wet=0.36, tone=5200)

# the lead gets the dotted eighth every record from this decade has
S.bus['lead'] = S.bus['lead'] + 0.26 * np.roll(
    lp(narrow(S.bus['lead'], 0.5), 3600, order=2), int(3.0 * STEP), axis=0)

for k in ('mach', 'strings', 'gtr', 'horns', 'fx', 'lead'):
    S.bus[k] = mono_below(S.bus[k], 165)
S.bus['bass'] = mono_below(S.bus['bass'], 170)
S.bus['drums'] = mono_below(S.bus['drums'], 150)
S.bus['strings'] = narrow(S.bus['strings'], 0.80)
S.bus['mach'] = narrow(S.bus['mach'], 0.62)
S.bus['fx'] = narrow(S.bus['fx'], 0.82)
S.bus['hats'] = narrow(S.bus['hats'], 0.70)
S.bus['lead'] = narrow(S.bus['lead'], 0.80)

# ---- the ride ------------------------------------------------------------
# Per-part gains do not sum to a section. This is the master fader, written
# in dB per bar, and the dip in front of every arrival is the point of it.
#
# The arrangement is already doing most of the work: the bridge has no drums,
# no guitar and no percussion in it, and that is worth six or seven dB on its
# own. Riding it down another eleven on top - which a first pass did - put
# the section THIRTEEN dB under the choruses, which is not contrast, it is a
# hole. The rule is 3-6 dB between the quietest section and the loudest, and
# the ride's job here is only the part the arrangement cannot do: the dip in
# the bar before each arrival.
ARC = [(0, -4.2), (7, -3.6), (8, -3.4), (15, -3.0), (16, -3.0), (31, -2.4),
       (32, -2.0), (44, -1.7), (46, -3.0), (47, -3.6),
       (48, -0.5), (62, -0.5), (63, -1.6),
       (64, -2.4), (78, -2.2), (79, -3.4),
       (80, -1.7), (86, -1.5), (87, -2.8),
       (88, -0.3), (102, -0.3), (103, -1.8),
       (104, -4.6), (111, -4.2), (112, -3.0), (119, -2.4),
       (120, -1.3), (125, -1.0), (126, -1.8), (127, -5.0),
       (128, 0.0), (151, 0.0), (152, 0.2), (159, 0.2),
       (160, -2.2), (168, -4.5), (175, -11.0), (NB, -20.0)]
t_bars = np.arange(S.total) / BAR
db = np.interp(t_bars, [p[0] for p in ARC], [p[1] for p in ARC])
ride = np.maximum(uniform_filter1d(10 ** (db / 20.0), int(0.030 * SR)), 0.0)
for k in S.bus:
    S.bus[k] = S.bus[k] * ride[:, None].astype(np.float32)
print(f'  ride: {db.min():.1f} to {db.max():.1f} dB across {NB} bars')

# ---- two-inch tape -------------------------------------------------------
for k, dv in (('drums', 0.85), ('bass', 0.70), ('gtr', 0.55), ('perc', 0.45),
              ('horns', 0.60), ('mach', 0.35), ('strings', 0.30)):
    S.bus[k] = D.tape(S.bus[k], drive=dv, hiss=0.0, wow=0.6, seed=hash(k) % 97)

# ---- the faders ----------------------------------------------------------
# `Session.loudness` over the whole track is the wrong number for a part that
# only plays in the choruses - its 90th percentile across six minutes says
# the horn section is 30 dB down when the ear puts it 11. So every bus is
# measured over the SAME sixteen bars, the loudest ones, and set against the
# balance table in `theory/00-foundations/16-mixing-process.md`.
# Measured against `funk_pyatnica` - the closest thing in this repository to
# a live band on tape - which carries 9% of its energy in 800-3000 Hz where
# a first pass of this record carried 6.5%. That band is the strings and the
# horns, and the strings and the horns are what make a disco record one.
TARGET = {'drums': 0.0, 'bass': -3.2, 'perc': -6.0, 'lead': -6.2,
          'strings': -6.8, 'gtr': -8.8, 'horns': -9.2, 'mach': -12.0,
          'hats': -14.0, 'fx': -17.0}
# The percentile matters more than the window. A horn section plays sixteen
# short stabs in sixteen bars - a five percent duty cycle - so its 90th
# percentile is silence and the fader comes out thirty dB wrong. The 99th
# asks how loud the part is at its loudest, which is the question a fader
# answers for a sparse part and gives nearly the same answer for a dense one.
_w = slice(P(136), P(152))
_ref = S.loudness(S.bus['drums'][_w], pct=99)
GAINS = {}
for k in S.bus:
    lv = S.loudness(S.bus[k][_w], pct=99)
    GAINS[k] = (float(np.clip(10 ** ((_ref + TARGET[k] - lv) / 20), 0.05, 12.0))
                if lv > -70 else 1.0)
GAINS['fx'] = 0.85
print('  faders: ' + '  '.join(f'{k} {v:.2f}' for k, v in sorted(GAINS.items())))

# The clipper is meant to shave the tip of a transient, not to be the mix's
# level control. At 14% of samples shaped it is distorting everything, and
# THAT is what "cuts the ears" - not any single sound. So the bus sum is
# scaled to a known peak first and the clipper only ever sees the top of it.
_sum = np.zeros_like(S.bus['drums'])
for _k, _b in S.bus.items():
    _sum += _b * GAINS[_k]
_scale = 2.00 / max(float(np.abs(_sum).max()), 1e-9)
GAINS = {k: v * _scale for k, v in GAINS.items()}
print(f'  master trim: {20*np.log10(_scale):+.1f} dB -> bus sum peaks 2.00')
del _sum

S.report(GAINS)
S.ownership(3000, 16000, GAINS)
# -10 LUFS, and that is the point. This genre was played by people and its
# dynamic range is part of what it is; a disco record crushed to -5 stops
# being one, and the streaming platform turns it down anyway.
S.render('disco_revashol_120.wav', drive=0.0, duck=0.14, duck_rel=0.13,
         clip=1.50, peak=0.89, fade=3.0, gains=GAINS,
         comp=dict(thresh=0.30, ratio=1.8, attack=0.022, release=0.17),
         brick=dict(gain=1.55, ceiling=0.89))
