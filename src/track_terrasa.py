"""TERRASA - minimal deep house at 123 BPM, F Dorian.

A terrace at golden hour, and almost nothing on it. House is the one dance
genre with no drop: the shape is an accumulation followed by a subtraction, so
everything it has to say it says through timbre and groove over five and a
half minutes, and the fewer things there are, the more each of them means.

Six things carry the whole record - a kick, a hat, a shaker, a rim, a bass and
a CHORD - and the chord is not in front. It is a bank of string-machine
oscillators sitting low, dark and far back, with a soft four-note stab landing
on it every bar or two. There is no lead instrument anywhere in the piece. A
saxophone, a vibraphone and an FM electric piano were all tried and all
removed: each of them put something in front of the thing the record is
actually about, and a minimal house record is defined by what is not in it.

123 BPM is chosen for the body rather than from a genre chart. 488 ms a beat
is a walking pace - fast enough that the shoulders move on their own and slow
enough that nothing is being asked of anybody. The kick is on all four, so the
felt pulse is the tempo and not half of it.

F DORIAN, which is the whole mood. Dorian is a minor scale with a natural
sixth, and that one note is the difference between sad and cool. It has to be
audible or the piece is just F minor, so it is put where nobody can miss it:
the fourth chord of the loop is a IV MAJOR - Bb13 - and its third IS the D.

    Fm9  ->  Ebmaj9  ->  Abmaj9  ->  Bb13  ->  (Fm9)

Voiced low - MIDI 48 to 67, between the bass and nothing at all - and nothing
moves more than two semitones. Two of the four root moves are down a fifth,
which is the strongest motion there is, and the return is the quietest thing
in the piece: from Bb13 back to Fm9 three voices do not move at all and the
fourth goes D -> Eb. One semitone, and the Dorian sixth becomes the minor
seventh of home. That semitone is the hook.

THE DEVELOPMENT HAS NO NEW PARTS IN IT.

  COLOUR   The string bank's filter opens from 2.2 kHz to 3.6 kHz across five
           minutes and closes again, and the stab's from 1.0 kHz to 2.2 kHz.
           That sweep is the arrangement; in this genre it usually is.
  DENSITY  The stab lands on one offbeat a bar, then two, then three, then
           all four - and back down for the last section, so the record ends
           somewhere it has already been.
  TOP END  Open hats on two of the four offbeats, then on all four, then two
           again; the shaker runs eighths and only doubles to sixteenths for
           the two loudest sections. Two noise sources covering every
           subdivision is a record made of sand.

    DOOR (16) | FLOOR (16) | GROOVE (16) | ROOM (16) | OPEN (16)
    | BREAK (16) | RETURN (16) | DEEP (32) | AFTER (16) | OUT (16)

176 bars, 5:43. The lowest point is bar 80 and the peak starts at bar 112 -
64% of the way in, which is where a peak belongs.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
from houselib import *

np.random.seed(123)
rs = np.random.RandomState(123)

# ============================================================== material ===
# F Dorian: F G Ab Bb C D Eb. The D is the whole point.
ROOTS = [29, 27, 32, 34]                       # F1  Eb1  Ab1  Bb1

# The string bank - the harmonic spine, five voices between C3 and G4. Read
# down the last column: Eb4 F4 Eb4 D4, which is as much tune as this record
# has and it is made of nothing but the top note of a chord.
PAD = [[48, 51, 56, 60, 63],                   # Fm9     C3  Eb3 Ab3 C4  Eb4
       [50, 55, 58, 62, 65],                   # Ebmaj9  D3  G3  Bb3 D4  F4
       [48, 51, 55, 60, 63],                   # Abmaj9  C3  Eb3 G3  C4  Eb4
       [48, 53, 56, 60, 62]]                   # Bb13    C3  F3  Ab3 C4  D4

# The stab: the same harmony as four voices, lower still, so it reads as the
# strings being struck rather than as a second instrument.
STAB = [[51, 56, 60, 63],                      # Fm9     Eb3 Ab3 C4  Eb4
        [50, 55, 58, 62],                      # Ebmaj9  D3  G3  Bb3 D4
        [51, 55, 58, 60],                      # Abmaj9  Eb3 G3  Bb3 C4
        [53, 56, 60, 62]]                      # Bb13    F3  Ab3 C4  D4

CONGA_HI, CONGA_MID, CONGA_LO = 60, 53, 46


# ================================================================= bass ===
# Root on 1 and on 3 so the kick has something under it, the octave on the
# offbeat 8th for the bounce, and the fifth on the last offbeat of the bar -
# which rings PAST the bar line into the next chord, because `hbass` renders
# six steps of overhang. Cut at the bar line that note dies at the moment it
# is meant to arrive and the first half of every bar goes quiet.
def bassbar(root, walk=False, sparse=False):
    if sparse:
        return [(0, root, 4.0, 0, 0, 1.00), (6, root + 12, 2.0, 0, 0, 0.70),
                (8, root, 4.0, 0, 0, 0.90), (14, root + 7, 2.6, 0, 0, 0.72)]
    p = [(0, root, 3.0, 0, 0, 1.00), (3, root, 1.2, 0, 0, 0.70),
         (6, root + 12, 2.0, 0, 0, 0.78), (8, root, 3.0, 0, 0, 0.92),
         (11, root, 1.2, 0, 0, 0.66)]
    if walk:
        # Bb -> C -> Eb -> E -> F. The E is the only note in the record from
        # outside the key, and it is a chromatic approach on the last 16th of
        # a four-bar loop, which is the one place a bass is allowed one.
        p += [(13, root + 2, 1.0, 0, 0, 0.70), (14, root + 5, 1.0, 0, 0, 0.76),
              (15, root + 6, 1.6, 0, 0, 0.88)]
    else:
        p += [(14, root + 7, 2.6, 0, 0, 0.80)]
    return p

BASS = [bassbar(r, walk=(i == 3)) for i, r in enumerate(ROOTS)]
BASS_SPARSE = [bassbar(r, sparse=True) for r in ROOTS]


# ============================================================== the stab ===
# (bar of the four-bar loop, step, length in steps, velocity)
#
# This is the house chord and it is PRESSED AND RELEASED: about 300 ms of
# sound and then nothing, on the offbeat, with more silence in the bar than
# chord. A sustained chord under a four-to-the-floor kick is techno, whatever
# the harmony is - what makes the same four chords read as house is that they
# arrive on the "and" and are gone before the next kick.
def _P(pat, dur=2.6):
    return [(bb, st, dur, v) for bb, st, v in pat]

P0 = []
P1 = _P([(0, 2, 0.62), (1, 2, 0.48), (2, 2, 0.58), (3, 2, 0.46)])
P2 = _P([(0, 2, 0.66), (0, 10, 0.44), (1, 2, 0.50), (1, 10, 0.40),
         (2, 2, 0.62), (2, 10, 0.44), (3, 2, 0.48), (3, 10, 0.38)])
P3 = _P([(0, 2, 0.68), (0, 10, 0.46), (0, 14, 0.40), (1, 2, 0.52), (1, 10, 0.42),
         (2, 2, 0.64), (2, 10, 0.46), (2, 14, 0.38), (3, 2, 0.50), (3, 10, 0.42)])
P4 = _P([(0, 2, 0.70), (0, 6, 0.44), (0, 10, 0.50), (0, 14, 0.42),
         (1, 2, 0.54), (1, 6, 0.38), (1, 10, 0.44), (1, 14, 0.36),
         (2, 2, 0.66), (2, 6, 0.42), (2, 10, 0.48), (2, 14, 0.40),
         (3, 2, 0.52), (3, 6, 0.36), (3, 10, 0.42), (3, 14, 0.34)])


# ============================================================== sections ===
# (bar, name, gain, stab pattern, stab cutoff, pad tone, pad level,
#  open hats per bar, shaker hits per bar)
#
# Written as a gain per section, not only as a set of parts, because contrast
# is relative and the ear judges each section against the one before it. A
# section that both loses its parts AND gets turned down loses twice, which
# reads as a fault rather than as a fall.
SEC = [(0,   'DOOR',   0.52, P0, 1000, 2200, 0.34, 0,  8),
       (4,   'DOOR',   0.62, P0, 1000, 2200, 0.34, 0,  8),
       (8,   'DOOR',   0.70, P1, 1050, 2350, 0.32, 2,  8),
       (12,  'DOOR',   0.76, P1, 1050, 2350, 0.28, 4,  8),
       (16,  'FLOOR',  0.86, P1, 1200, 2400, 0.00, 4,  8),
       (32,  'GROOVE', 0.92, P2, 1350, 2600, 0.00, 4,  8),
       (48,  'ROOM',   0.90, P2, 1500, 2800, 0.22, 4, 16),
       (64,  'OPEN',   0.94, P3, 1700, 3100, 0.24, 4, 16),
       (80,  'BREAK',  0.84, P1, 1400, 3000, 0.52, 0,  8),
       (88,  'BREAK',  0.88, P2, 1550, 3200, 0.32, 2,  8),
       (96,  'RETURN', 0.95, P2, 1650, 2900, 0.00, 4,  8),
       (104, 'RETURN', 0.98, P3, 1800, 2900, 0.00, 4, 16),
       (112, 'DEEP',   1.00, P4, 2050, 3300, 0.26, 4, 16),
       (128, 'DEEP',   1.00, P4, 2050, 3300, 0.26, 4, 16),
       (144, 'AFTER',  0.92, P3, 1800, 3100, 0.24, 4, 16),
       (160, 'OUT',    0.84, P2, 1450, 2600, 0.20, 2,  8),
       (168, 'OUT',    0.64, P1, 1150, 2300, 0.18, 2,  8)]

def sec(b):
    cur = SEC[0]
    for row in SEC:
        if b >= row[0]:
            cur = row
    return cur


# ================================================================ render ===
S = Session(176, tail=4.0)
P = S.pos

def jit(ms=4.0):
    """a few milliseconds of humanisation. Never on the kick and never on the
    sub: the pulse is the one thing the body is counting."""
    return int(rs.normal(0, ms / 1000.0 * SR))


for b in range(176):
    _, secname, g, STB, SCUT, _pt, _pl, NOPEN, NSHK = sec(b)
    ci = b % 4

    kick_on = (4 <= b < 80) or (92 <= b)
    clap_on = (20 <= b < 80) or (96 <= b < 168)
    chat_on = (b < 80) or (88 <= b)
    conga_on = (48 <= b < 80) or (112 <= b < 160)
    rim_on = (16 <= b < 80) or (96 <= b < 172)
    shak_on = (b >= 2) and not (80 <= b < 84)
    # the open hat lands on the "and" of 1 and 3 first; the other two offbeats
    # stay closed until the record needs the lift
    opens = () if NOPEN == 0 else ((2, 10) if NOPEN == 2 else (2, 6, 10, 14))

    if kick_on:
        for st in (0, 4, 8, 12):
            t = P(b, st)
            S.hit(t)                                   # the sidechain trigger
            S.place(t, hkick(), g * (0.80 if st in (0, 8) else 0.76), 'drums')
    if clap_on:
        for st in (4, 12):
            t = P(b, st) + jit(3)
            S.place(t, hclap(seed=(b + st) % 6), g * 1.10, 'drums')
            S.place(t, hsnare(seed=(b + st) % 4), g * 0.86, 'drums')
    if chat_on:
        for st in (0, 4, 8, 12):
            S.place(P(b, st) + jit(2.5), hhat(seed=(b * 4 + st) % 11),
                    g * (1.30 if st in (0, 8) else 1.02), 'drums')
        for st in (2, 6, 10, 14):
            if st not in opens:
                S.place(P(b, sw(st)) + jit(3), hhat(seed=(b * 4 + st) % 11),
                        g * 0.86, 'drums')
    for st in opens:
        S.place(P(b, sw(st)) + jit(3), hhat(open_=True, seed=(b + st) % 9),
                g * (1.45 if st in (2, 10) else 1.20), 'drums')
    if shak_on:
        for st in range(0, 16, 1 if NSHK == 16 else 2):
            v = (0.95 if st % 4 == 0 else 0.58 if st % 2 == 0 else 0.40)
            v *= 1 + 0.10 * rs.randn()
            S.place(P(b, sw(st)) + jit(3.5),
                    shaker(vel=max(v, 0.15), seed=(b * 5 + st) % 13),
                    g * (0.42 if NSHK == 16 else 0.50), 'perc')
    if rim_on:
        S.place(P(b, sw(6)) + jit(4), rimtick(seed=b % 7), g * 1.30, 'perc')
        if b % 2 == 1:
            S.place(P(b, sw(14)) + jit(4), rimtick(seed=(b + 2) % 7), g * 0.92, 'perc')
    if conga_on:
        # Three hits a bar and two shapes. In a record with six elements a
        # conga playing a full tumbao is a seventh one; this is a comment.
        pat = (((6, CONGA_MID, 'open', 0.74), (10, CONGA_HI, 'open', 0.56),
                (15, CONGA_HI, 'tip', 0.40))
               if b % 2 == 0 else
               ((6, CONGA_MID, 'open', 0.72), (8, CONGA_LO, 'open', 0.60),
                (14, CONGA_HI, 'tip', 0.46)))
        for st, nt, stk, v in pat:
            S.place(P(b, sw(st)) + jit(5), conga(nt, stk, vel=v,
                    seed=(b * 3 + st) % 9), g * 0.68, 'perc')

    # ---- the bass --------------------------------------------------------
    if b >= 32:
        sparse = (80 <= b < 92) or (b >= 168)
        pat = (BASS_SPARSE if sparse else BASS)[ci]
        S.place(P(b), hbass(tuple(pat)), g * (0.62 if sparse else 0.78), 'bass')

    # ---- the stab: an accent on the strings, not a part -------------------
    for bb, st, dur, v in STB:
        if bb != ci:
            continue
        S.place(P(b, sw(st)) + jit(6),
                chord(tuple(STAB[ci]), dur, vel=v, cutoff=SCUT,
                      attack=0.028, decay=0.185, take=b % 3),
                g * 0.90, 'keys')

print('  floor, percussion, bass and the stab placed')


# ---- the string bank: the harmonic spine --------------------------------
# It plays almost the whole record, because it IS the record - dark, low and a
# long way back, which is the one thing about this piece a listener asked for
# by name. The only hole is bars 96-111: the drums come back after the
# breakdown and the strings do NOT, so sixteen bars drive dry before they
# return with the peak at 112.
# One render per contiguous run, not per section: the whole point of a
# divide-down bank is that its oscillators never restart, and cutting it at
# every filter change puts a retrigger back in every four bars. So the tone is
# fixed across a run and the LEVEL is written in per bar as a gain.
runs, a = [], 0
while a < 176:
    if sec(a)[6] <= 0:
        a += 1
        continue
    z = a
    while z < 176 and sec(z)[6] > 0:
        z += 1
    runs.append((a, z))
    a = z
for a, z in runs:
    tone = sum(sec(b)[5] for b in range(a, z)) / (z - a)
    seg = solina([PAD[b % 4] for b in range(a, z)], level=1.0, tone=tone, seed=a)
    lv = np.repeat([sec(b)[2] * sec(b)[6] for b in range(a, z)], int(round(BAR)))
    lv = uniform_filter1d(np.asarray(lv, dtype=np.float32), int(0.25 * SR))
    if len(lv) < len(seg):
        lv = np.concatenate([lv, np.full(len(seg) - len(lv), lv[-1])])
    S.place(P(a), (seg * lv[:len(seg), None]).astype(np.float32), 1.0, 'pad')
print(f'  strings: {len(runs)} spans - ' + ', '.join(f'{a}-{z}' for a, z in runs))

# ---- seams ---------------------------------------------------------------
# House does not detonate, so the joins are a breath: a reversed swell of
# broadband noise over the last beat, and two chords thrown into a long delay
# and abandoned - the dub move, and the cheapest way to make a loop that has
# played forty times feel like something just happened.
for b in (15, 31, 47, 63, 79, 95, 111, 127, 143, 159):
    S.place(P(b, 12), whoosh(4, gain=0.30, rev_=True), sec(b)[2] * 0.50, 'air')
for b, v in ((79, 0.55), (111, 0.46)):
    throw(S, P(b, 14), chord(tuple(STAB[3]), 7.0, vel=0.75, cutoff=1500, take=1),
          gain=v, steps_=3.0, times=6, fb=0.55)


# ================================================================== mix ===
# The buses get their own compression before the master sees them, which is
# the only way to arrive at the clipper without a stack of transients for it
# to eat. `squash`'s release is one sixteenth at this tempo, so the gain
# climbs back between beats and the breathing is in time.
S.bus['drums'] = squash(S.bus['drums'], thresh=0.44, ratio=2.6, attack=0.016,
                        release=0.122, mix=0.80, report='drums')
S.bus['perc'] = squash(S.bus['perc'], thresh=0.14, ratio=3.6, attack=0.008,
                       release=0.122, mix=0.68, report='perc')
# `squash` gives back what a full-scale peak lost, which on a bus this
# transient is a factor of four - so one conga hit arrives at the master above
# 2.0 and the clipper spends its whole budget on it. Loudness comes from
# removing one peak, not from clipping harder.
S.bus['perc'] = softclip(S.bus['perc'], 0.85, knee=0.55)
S.bus['perc'] = shelf(S.bus['perc'], 9000, 1.5)

# One room and two distances. The stab is sent a long way back on purpose -
# it is meant to be heard as the strings being struck somewhere behind the
# drums, not as a keyboard in front of them - so it is more wet than dry.
# A 2.8-second tail at 62% wet turns a chord every two sixteenths back into
# exactly the continuous wash the short stabs exist to avoid. Short and
# moderately wet puts it behind the drums without refilling the gaps.
S.bus['keys'] = bus_reverb(S.bus['keys'], decay=1.5, wet=0.30, tone=3600)
S.bus['pad'] = bus_reverb(S.bus['pad'], decay=3.6, wet=0.34, tone=3000)
S.bus['perc'] = bus_reverb(S.bus['perc'], decay=0.62, wet=0.11, tone=6500)
S.bus['air'] = bus_reverb(S.bus['air'], decay=3.4, wet=0.30, tone=4600)
for k in ('pad', 'air', 'keys'):
    S.bus[k] = mono_below(S.bus[k], 150)
# Several decorrelated buses sum to an image no record has. A trim on each is
# the fix; less reverb on all of them is not.
S.bus['air'] = narrow(S.bus['air'], 0.72)
S.bus['pad'] = narrow(S.bus['pad'], 0.86)

# Balanced by measurement. `Session.loudness` is the 90th percentile of a
# 300 ms window - how loud a part is WHEN IT PLAYS - so the numbers are
# comparable across buses however transient the part is. Target, against the
# floor: bass -4, strings -8, percussion -10, the stab -14, returns -18. The
# stab is the quietest thing on the record that is not an effect.
GAINS = {'drums': 0.62, 'perc': 2.30, 'bass': 0.66, 'keys': 8.50,
         'pad': 4.40, 'air': 3.40}

S.report(GAINS)
S.render('house_terrasa_123.wav', drive=0.0, duck=0.62, duck_rel=0.20,
         clip=1.34, limit=0.92, peak=0.76, fade=2.4, gains=GAINS)
