"""DESCARGA (~4:58, 216 bars @174) - Latin jungle in A minor.

174 BPM is a drum & bass tempo. It is also a salsa tempo. Two bars at 174 is
2.76 seconds, which is exactly one son clave, and the Amen break's own two-bar
shape sits on it without being retimed by a single sample. So this is not a
break with congas on top: it is one bar that two traditions both fit inside.

The joke underneath it is that they agree about where the hole goes. A jungle
bassline leaves beat 1 empty and lets the ear supply it. A Cuban tumbao leaves
beat 1 empty too, plays the fifth on the and-of-2, and puts the root of the
NEXT chord on beat 4 - the anticipation, which is why salsa leans forward.
Same silence, two names. The bass here plays a tumbao and it is also a jungle
sub, because there was never anything to reconcile.

THE CLAVE IS THE LAW. It is a two-bar timeline and every part has to agree
with it, the break included; a figure that contradicts it is `cruzado` and
reads as a mistake rather than as syncopation.

    three side (bar A):  0 . . . . . 6 . . . . . 12 . . .
    two side   (bar B):  . . . . 4 . . . 8 . . .  . . . .

And the break already almost plays it. The Amen's own map is kicks on 0, 2,
10, 11 and snares on 4 and 12; the three side wants 0, 6, 12, and the break
gives two of those for free. So the whole re-cut is:

    bar A   the break keeps its kick on 0, its snares on 4 and 12, and a kick
            moves onto 6 - the bombo of the clave. Nothing else changes.
    bar B   the two side wants 4 and 8. The snare is already on 4. The Amen's
            second kick moves from step 10 to step 8.

One sixteenth, once every two bars. That is the entire edit, and it is what
locks a 1969 funk drummer to a Cuban timeline written a century earlier.
Everything else in the break - the ghost notes between the anchors - is
re-dealt every bar so the roll never repeats while the count never moves.

Harmony: Am7 | Dm7 | E7b9 | Am7, one bar each, so the four-bar cycle is two
claves. One progression for the whole record, and exactly one note in it from
outside A natural minor: the G# of the E7, which arrives once every four bars,
on the two side. The F above it is the key's own flat sixth doing a second job
as the flat ninth of the dominant - the note that makes the chord Spanish
without being foreign to the scale.

The rhythm section is built rather than sampled: a tumbadora with four
strokes on three drums, a mambo bell struck on the mouth and on the neck, a
timbale shell, two rosewood sticks over a cupped hand, a scraped gourd, a
piano rendered a bar at a time with three strings to a note, and a three-man
horn section that gets brighter when it is blown harder because the wave
steepens in the bore. See `latinlib.py` for what each of those is and why the
engine did not already have it.

  b0-7      the clave alone in a room, then maracas, then the gourd
  b8-15     the rhythm section: shell, bell, congas. No break, no bass
  b16-31    the bass and the piano. So far this is a salsa record
  b32-63    DROP 1: the break arrives, cut to the clave
  b64-79    the mona - the horn section, answering the piano
  b80-95    the descarga: the drums stop, the piano and the quinto trade
  b96-103   the build, which in this music is a timbale fill
  b104-151  DROP 2, 48 bars: everything, and the horns take the tune
  b152-167  the mambo - the horns take the tune, the piano answers
  b168-199  DROP 3: a bombo on every beat under the break
  b200-215  the outro. The clave stops last, because it started first
"""
import numpy as np
from latinlib import *

rng = np.random.default_rng(0xC1A7E)
np.random.seed(0xC1A7E)
s = Session(216, tail=3.2)
# Salsa does not pump. The duck here is only deep enough to keep the sub out
# of the break's kick - anything more and the rhythm section starts breathing,
# which is a house record's gesture and wrong in this one.
s.DUCKED = {'bass': 0.75, 'music': 0.20}

# ----------------------------------------------------------------- key ----
# Am7 | Dm7 | E7b9 | Am7. Two claves per turn of the harmony.
ROOT = [33, 38, 40, 33]                    # A1 55, D2 73, E2 82, A1 55 Hz
FIFTH = [40, 33, 35, 40]                   # the and-of-2 note: a fifth, up or down
POOL = [(69, 72, 76, 79),                  # Am7   A4 C5 E5 G5
        (69, 74, 77, 81),                  # Dm7   A4 D5 F5 A5
        (68, 71, 74, 77),                  # E7b9  G#4 B4 D5 F5  (rootless)
        (69, 72, 76, 79)]
PAD_V = [(57, 60, 64, 67), (57, 62, 65, 69), (56, 59, 62, 65), (57, 60, 64, 67)]

def ci(b): return b % 4
def side(b): return b % 2                  # 0 = three side, 1 = two side

# The montuno's rhythm is two tresillos, 3+3+2 twice, which is where the
# accents of the clave's three side already are. On the two side one note
# moves from step 6 to step 4 - and that single sixteenth is the clave
# turning over. Nothing else in the figure changes all record.
RHY_A = (0, 3, 6, 8, 11, 14)
RHY_B = (0, 3, 4, 8, 11, 14)
# Four shapes on that one rhythm, turned over every sixteen bars. The rhythm
# is the hook and never changes; the line inside it does, which is how a
# guajeo stays relentless without becoming a loop.
FIGS = [((2, 1, 0, 1, 2, 3), (1, 0, 2, 1, 3, 2)),
        ((0, 2, 3, 2, 1, 2), (2, 3, 1, 2, 0, 1)),
        ((3, 2, 1, 2, 3, 1), (0, 1, 3, 2, 1, 0)),
        ((1, 2, 3, 1, 0, 2), (3, 1, 0, 2, 3, 2))]

# ghost slices for the break: four textures from three different bars of it,
# so a re-dealt roll is never the same sixteenth twice
GHOSTS = ([amen.get(0, st) for st in (6, 7, 8, 9)] +
          [amen.get(2, st) for st in (6, 7, 14, 15)] +
          [amen.get(1, st) for st in (6, 8, 9)])
GH_REV = [rev(g) for g in GHOSTS]
GH_LO = [pitched(g, 0.72) for g in GHOSTS[:6]]


# ============================================================ the break ====
def clavebreak(b, gain=1.0, ghost=0.55, heat=0.55, seed=0, kicks=1.0,
               snare=1.0, top=1.0, bus='main'):
    """The Amen, cut so its weight lands on the clave.

    The anchors never move; only the ghost notes between them are dealt out
    fresh each bar - reversed, pitched down, borrowed from another bar of the
    break. The count is nailed and the surface never repeats, which is the
    whole difference between a roller and a loop."""
    r = np.random.default_rng(seed * 7919 + b * 131)
    if side(b) == 0:                       # three side: 0, 6, 12
        anch = [(0, K, 1.00 * kicks), (4, SN, 0.92 * snare),
                (6, K2, 0.86 * kicks), (10, K2, 0.62 * kicks),
                (12, SN, 1.00 * snare)]
        taken = {0, 4, 6, 10, 12}
    else:                                  # two side: 4, 8
        anch = [(0, K, 0.95 * kicks), (4, SN, 0.94 * snare),
                (8, K2, 0.90 * kicks), (12, SN, 1.00 * snare)]
        taken = {0, 4, 8, 12}
    for st, seg, g in anch:
        s.place(s.pos(b, st), seg, g * gain, bus)
    s.hit(s.pos(b, 0))
    for st in range(16):
        if st in taken or r.random() > heat:
            continue
        pick = r.random()
        if pick < 0.12:
            g = GH_REV[r.integers(len(GH_REV))]
        elif pick < 0.22:
            g = GH_LO[r.integers(len(GH_LO))]
        else:
            g = GHOSTS[r.integers(len(GHOSTS))]
        v = ghost * (0.55 + 0.55 * r.random()) * (1.25 if st % 2 == 0 else 0.85)
        s.place(s.pos(b, st) + int(r.normal(0, 0.012) * STEP), g,
                v * gain * top, bus)


def cracked(b, gain=1.0, seed=0):
    """One bar where the break is chopped hard instead of rolled - a stutter
    on the two side, which is where the clave has the most room."""
    r = np.random.default_rng(seed * 313 + b)
    s.place(s.pos(b, 0), K, gain)
    s.hit(s.pos(b, 0))
    for st in (2, 3, 4, 5, 6, 7):
        s.place(s.pos(b, st), SN1 if st in (4, 6) else GHOSTS[r.integers(len(GHOSTS))],
                gain * (0.9 if st in (4, 6) else 0.5))
    s.place(s.pos(b, 8), K2, gain * 0.9)
    for i in range(4):                     # a ratchet into beat 4
        s.place(s.pos(b, 10 + i * 0.5), pitched(SN1, 1.0 + i * 0.06),
                gain * (0.45 + 0.12 * i))
    s.place(s.pos(b, 12), SN, gain)


# ====================================================== the rhythm box =====
# Where each player is standing, seen from the audience. Width by LEVEL, not
# by a micro-delay: a one-third-of-a-millisecond channel offset on every drum
# is a Haas widener, and a bus full of them combs into a hole in mono - which
# is where half of this record will be heard.
PAN = {'clave': 0.00, 'cascara': -0.36, 'campana': 0.28, 'maraca': 0.56,
       'guiro': -0.60, 'bongo': 0.46, 'tumba': -0.16, 'conga': -0.34,
       'quinto': -0.52, 'paila': -0.40}


def pp(b, st, seg, gain, who, nudge=0.0):
    s.place(s.pos(b, st) + int(nudge * STEP), panned(seg, PAN[who]), gain, 'perc')


def latin(b, gain=1.0, bell=1.0, cas=1.0, mar=1.0, gui=1.0, bong=0.0,
          clv=1.0, seed=0):
    """Clave, timbale shell, mambo bell, maracas, gourd, bongo.

    The bell is hit on every eighth with the mouth on the beats and the neck
    between them. That is not decoration: at 174 the break's own pulse is a
    two-step, felt at 87, and the bell is what keeps the body counting at 174.
    Density is how this music carries a pulse - not a kick on every beat."""
    sd = side(b)
    for st in (CLAVE3 if sd == 0 else CLAVE2):
        pp(b, st, clave(seed=(b * 3 + st) % 17), 0.85 * clv * gain, 'clave')
    if cas:
        for st in (CASCARA_A if sd == 0 else CASCARA_B):
            v = 1.0 if st in (0, 8) else 0.70
            pp(b, st, cascara(seed=(b * 17 + st) % 23, vel=v),
               0.40 * cas * gain, 'cascara')
    if bell:
        for st in range(0, 16, 2):
            m = (st % 4 == 0)
            pp(b, st, campana(mouth=m, seed=(b * 11 + st) % 19,
                              vel=1.0 if m else 0.58),
               0.40 * bell * gain, 'campana', nudge=0.02)
    if mar:
        for st in range(16):
            v = 1.0 if st % 4 == 0 else (0.55 if st % 2 else 0.75)
            pp(b, st, maraca(seed=(b * 7 + st) % 29, vel=v),
               0.46 * mar * gain, 'maraca', nudge=0.03)
    if gui:
        # a long down-stroke on the beat, two short scrapes answering it
        pp(b, 0, guiro(4.0, teeth=15, seed=(b * 5) % 13), 0.62 * gui * gain, 'guiro')
        pp(b, 6, guiro(1.6, teeth=5, seed=(b * 5 + 1) % 13), 0.46 * gui * gain, 'guiro')
        pp(b, 8, guiro(4.0, teeth=15, seed=(b * 5 + 2) % 13), 0.62 * gui * gain, 'guiro')
        pp(b, 14, guiro(1.6, teeth=5, seed=(b * 5 + 3) % 13), 0.46 * gui * gain, 'guiro')
    if bong:
        # the martillo: continuous eighths, the accent on beat 3
        for st in range(0, 16, 2):
            hi = st in (4, 12)
            pp(b, st, bongo(MACHO if hi else HEMBRA,
                            'open' if st == 8 else 'tip',
                            seed=(b * 13 + st) % 19,
                            vel=1.0 if st == 8 else 0.6),
               0.34 * bong * gain, 'bongo')


def congas(b, gain=1.0, seed=0, quinto=0.0, heavy=0.0):
    """The marcha. heel, toe, slap, toe | heel, toe, OPEN OPEN - and those two
    open tones on beat 4 and its and are the reason anyone dances to this.
    They also land on the clave's third stroke, which is not a coincidence:
    the pattern was built on it."""
    sd = side(b)
    if sd == 0:
        pat = [(0, TUMBA, 'heel', 0.62), (2, TUMBA, 'toe', 0.45),
               (4, CONGA, 'slap', 0.95), (6, CONGA, 'toe', 0.42),
               (8, TUMBA, 'heel', 0.60), (10, TUMBA, 'toe', 0.45),
               (12, CONGA, 'open', 1.00), (14, CONGA, 'open', 0.88)]
    else:
        pat = [(0, TUMBA, 'heel', 0.60), (2, TUMBA, 'toe', 0.45),
               (4, CONGA, 'slap', 0.92), (6, CONGA, 'open', 0.80),
               (8, TUMBA, 'toe', 0.48), (10, CONGA, 'slap', 0.55),
               (12, TUMBA, 'open', 0.95), (14, CONGA, 'open', 0.90)]
    for st, note, stroke, v in pat:
        pp(b, st, conga(note, stroke, seed=(b * 5 + st) % 11, vel=v,
                        size=1.35 if note == TUMBA else 1.0),
           0.62 * gain * (1.15 if heavy and stroke == 'open' else 1.0),
           'tumba' if note == TUMBA else 'conga', nudge=rng.normal(0, 0.015))
    if quinto:
        # the quinto is the solo drum: it does not keep time, it comments
        r = np.random.default_rng(seed * 977 + b)
        for st in sorted(r.choice([1, 3, 5, 7, 9, 11, 13, 15],
                                  size=int(r.integers(2, 5)), replace=False)):
            pp(b, int(st), conga(QUINTO, r.choice(['slap', 'open', 'tip']),
                                 seed=int(st) % 11, vel=0.9, size=0.75),
               0.5 * quinto * gain, 'quinto')


def abanico(b, st=12, gain=1.0, n=6, seed=0):
    """The fan: the timbale fill that announces a section in this music, and
    which does the job an EDM riser does everywhere else. A rimshot, then an
    accelerating roll, then the downbeat."""
    r = np.random.default_rng(seed + b)
    pp(b, st, paila(67, rim=1.0, vel=1.1, seed=1), 0.85 * gain, 'paila')
    for i in range(n):
        u = i / max(n - 1, 1)
        p = st + 0.5 + u * 3.2
        pp(b, p, paila(64 + int(r.integers(0, 3)), vel=0.5 + 0.6 * u,
                       seed=int(i) % 7), (0.30 + 0.45 * u) * gain, 'paila')
    pp(b, 15.5, paila(64, rim=0.8, vel=1.0, seed=3), 0.6 * gain, 'paila')


# ============================================================== the bass ===
def bassline(b, gain=1.0, sub=0.75, extra=0.0, decay=0.42):
    """The tumbao. Beat 1 empty; the fifth on the and-of-2; the root of the
    NEXT bar on beat 4."""
    c, nx = ci(b), ci(b + 1)
    ev = [(6, FIFTH[c], 0.88), (12, ROOT[nx], 1.0)]
    if extra:
        ev.append((14.5, ROOT[nx] + 12, 0.5))       # the octave answering itself
    if side(b) == 0 and extra:
        ev.append((3, ROOT[c], 0.55))
    s.place(s.pos(b), tumbao(tuple(sorted(ev)), 16, sub=sub, decay=decay,
                             seed=b % 7), gain, 'bass')


# ============================================================= the piano ===
def piano(b, gain=1.0, oct_=0, vel=0.85, left=1.0, seed=0):
    """The montuno, in octaves, both hands."""
    c = ci(b)
    fa, fb = FIGS[(b // 16) % len(FIGS)]
    rhy, fig = (RHY_A, fa) if side(b) == 0 else (RHY_B, fb)
    acc = (0, 6) if side(b) == 0 else (4, 8)
    ev = []
    for st, i in zip(rhy, fig):
        n = POOL[c][i] + 12 * oct_
        notes = (n, n - 12) if left else (n,)
        ev.append((st, notes, 1.0 if st in acc else 0.72))
    s.place(s.pos(b), montuno(tuple(ev), 16, vel=vel, seed=b % 5), gain, 'music')



# ---------------------------------------------------- the piano solo -------
# A descarga is an improvisation, so the piano cannot go on playing the guajeo
# through it - a montuno under a montuno is just the montuno. Sixteen bars of
# written line instead: one phrase stated, the same phrase sequenced a step
# down and cut short, then broken into sixteenths, then a climb out of the
# section. Every strong beat is a chord tone; the notes between them are
# passing and chromatic approach, and the only two notes from outside A minor
# in the whole record - the G# and the F above it - land on the E7, which is
# the one bar that asks for them.
#                  bar, step, midi
SOLO = [(0, 0, 76), (0, 2, 79), (0, 4, 81), (0, 6, 79), (0, 8, 76), (0, 11, 72),
        (1, 0, 74), (1, 2, 77), (1, 4, 81), (1, 8, 77), (1, 10, 76), (1, 12, 74),
        (2, 0, 76), (2, 3, 77), (2, 6, 80), (2, 8, 83), (2, 11, 80), (2, 14, 77),
        (3, 0, 76), (3, 4, 81), (3, 8, 84), (3, 12, 81),
        # the same phrase, a step lower and cut off before it finishes
        (4, 0, 74), (4, 2, 77), (4, 4, 79), (4, 6, 77), (4, 8, 74), (4, 11, 72),
        (5, 0, 72), (5, 2, 74), (5, 4, 77), (5, 8, 74), (5, 10, 72), (5, 12, 71),
        (6, 0, 71), (6, 3, 74), (6, 6, 77), (6, 8, 80), (6, 12, 77),
        (7, 0, 76), (7, 6, 72), (7, 10, 69),
        # broken into sixteenths: the same notes, four times the traffic
        (8, 0, 69), (8, 1, 72), (8, 2, 76), (8, 3, 79), (8, 4, 81), (8, 5, 79),
        (8, 6, 76), (8, 8, 72), (8, 9, 71), (8, 10, 72), (8, 12, 76), (8, 14, 79),
        (9, 0, 81), (9, 1, 79), (9, 2, 77), (9, 3, 74), (9, 4, 72), (9, 6, 74),
        (9, 8, 77), (9, 10, 81), (9, 12, 77), (9, 14, 74),
        (10, 0, 71), (10, 1, 72), (10, 2, 74), (10, 3, 76), (10, 4, 77),
        (10, 6, 80), (10, 8, 83), (10, 10, 80), (10, 12, 77), (10, 14, 74),
        (11, 0, 76), (11, 2, 72), (11, 4, 69), (11, 8, 72), (11, 12, 76),
        # and the climb out
        (12, 0, 69), (12, 4, 72), (12, 8, 76), (12, 12, 79),
        (13, 0, 81), (13, 4, 77), (13, 8, 74), (13, 12, 77),
        (14, 0, 80), (14, 4, 83), (14, 8, 86), (14, 12, 83),
        (15, 0, 84), (15, 3, 81), (15, 6, 76), (15, 8, 81), (15, 11, 84),
        (15, 14, 88)]


def solo(b, b0, gain=1.0, vel=0.95):
    """One bar of the written solo, right hand only."""
    db = (b - b0) % 16
    ev = [(st, (n,), 1.0 if st % 4 == 0 else 0.78)
          for bb, st, n in SOLO if bb == db]
    if not ev:
        return
    s.place(s.pos(b), montuno(tuple(ev), 16, vel=vel, seed=db % 5,
                              hold=1.6, decay=1.5), gain, 'music')

# ============================================================== the horns ==
# The mona: four bars, three parts. Trumpets on top in close harmony, the
# trombone on the roots underneath. The riff waits through the Am7 and lands
# on the Dm7, which is how a section actually enters - on the change, not on
# the downbeat of a phrase.
MONA_T1 = [(0, 8, 76, '>'), (0, 11, 79, 'n'), (0, 14, 76, '.'),
           (1, 0, 77, '>'), (1, 4, 74, 'n'), (1, 6, 72, '.'),
           (2, 0, 71, '>'), (2, 3, 74, 'n'), (2, 6, 77, '>f'),
           (3, 0, 76, '>'), (3, 8, 72, 'n'), (3, 12, 69, '.')]
MONA_T2 = [(0, 8, 72, '>'), (0, 11, 76, 'n'), (0, 14, 72, '.'),
           (1, 0, 74, '>'), (1, 4, 69, 'n'), (1, 6, 69, '.'),
           (2, 0, 68, '>'), (2, 3, 71, 'n'), (2, 6, 74, '>f'),
           (3, 0, 72, '>'), (3, 8, 69, 'n'), (3, 12, 64, '.')]
MONA_TB = [(0, 8, 57, '>'), (0, 11, 60, 'n'), (0, 14, 57, '.'),
           (1, 0, 62, '>'), (1, 4, 57, 'n'), (1, 6, 57, '.'),
           (2, 0, 56, '>'), (2, 3, 59, 'n'), (2, 6, 62, '>f'),
           (3, 0, 57, '>'), (3, 8, 60, 'n'), (3, 12, 52, '.')]


def horns(b0, gain=1.0, vel=1.0, bright=1.0, parts=('t1', 't2', 'tb'), oct_=0):
    """Four bars of the section. Each line is rendered as one continuous
    phrase per bar so the players' vibrato and their slurs survive."""
    for name, line, bore, g, w in (('t1', MONA_T1, 'trumpet', 1.00, 0.55),
                                   ('t2', MONA_T2, 'trumpet', 0.80, -0.55),
                                   ('tb', MONA_TB, 'bone', 0.85, 0.0)):
        if name not in parts:
            continue
        for db in range(4):
            ph = tuple((st, n + 12 * oct_, art) for bb, st, n, art in line if bb == db)
            if not ph:
                continue
            first = ph[0][0]
            ph = tuple((st - first, n, art) for st, n, art in ph)
            seg = mona(ph, 16 - first, bore=bore, vel=vel, seed=db * 7 + len(name),
                       bright=bright, players=2 if name == 'tb' else 3,
                       width=0.5)
            s.place(s.pos(b0 + db, first), panned(seg, w * 0.5), gain * g, 'horns')


def stab(b, st, notes, gain=1.0, dur=2.0, vel=1.1):
    """A single section hit - the punctuation between phrases."""
    for i, (n, bore) in enumerate(notes):
        s.place(s.pos(b, st), mona(((0, n, '>.'),), dur, bore=bore, vel=vel,
                                   seed=i * 5, players=2, width=0.6),
                gain * (1.0 if bore == 'trumpet' else 0.85), 'horns')


# ============================================================= the pregon ==
# The call, and who answers it. In son the singer improvises a line and the
# chorus answers with a fixed one; here the trumpets take the call and the
# piano and the timbales answer, because a synthesised chorus singing
# non-words is worse than no chorus at all. The line is long, high and mostly
# held - the opposite of the montuno underneath it, which is short and busy.
PREGON = [(0, 0, 81, '>'), (0, 6, 79, 'n'), (0, 12, 76, 'nf'),
          (1, 4, 77, '^>'), (1, 10, 74, 'n'),
          (2, 0, 80, '>'), (2, 6, 83, 'n'), (2, 12, 80, 'nf'),
          (3, 2, 76, '^>'), (3, 8, 72, 'n'), (3, 12, 69, 'n')]
PREGON2 = [(0, 0, 76, '>'), (0, 6, 72, 'n'), (0, 12, 69, 'nf'),
           (1, 4, 74, '^>'), (1, 10, 69, 'n'),
           (2, 0, 74, '>'), (2, 6, 77, 'n'), (2, 12, 74, 'nf'),
           (3, 2, 72, '^>'), (3, 8, 68, 'n'), (3, 12, 64, 'n')]


def pregon(b0, gain=1.0, vel=1.0, bright=1.0, oct_=0):
    """Four bars of the call, two trumpets in thirds."""
    for line, g, w in ((PREGON, 1.00, 0.35), (PREGON2, 0.78, -0.35)):
        for db in range(4):
            ph = tuple((st, n + 12 * oct_, art) for bb, st, n, art in line if bb == db)
            if not ph:
                continue
            first = ph[0][0]
            ph = tuple((st - first, n, art) for st, n, art in ph)
            seg = mona(ph, 16 - first, bore='trumpet', vel=vel, seed=db * 11 + int(g * 7),
                       bright=bright, players=3, width=0.45)
            s.place(s.pos(b0 + db, first), panned(seg, w), gain * g, 'horns')


# ================================================================ the bombo ==
# There is no bass drum in a salsa band. There is one here, and only in the
# last drop, because a breakbeat on its own halves the felt pulse: at 174 the
# two-step is counted at 87 in the body however fast the hats run. The bell
# holds the eighths up for four minutes; for the final thirty-two bars
# something has to hit the floor on every beat, and the Amen's own kick is a
# 1969 drum recorded in a room - too soft and too short to do it.
BOMBO = fade_edges(kick(4, tune=55.0, top=250.0, punch=1.1, drive=3.2,
                        decay=0.115), 1.2)


def bombo(b, gain=1.0, half=False):
    for st in (0, 8) if half else (0, 4, 8, 12):
        s.place(s.pos(b, st), BOMBO, gain)
        s.hit(s.pos(b, st))


# ============================================================================
#                              THE ARRANGEMENT
# ============================================================================

# ---------------------------------------------- b0-7: a room, and a clave --
s.place(s.pos(0), crackle(128, 0.5), 0.30, 'fx')
s.place(s.pos(0), reverb(crowd(128, 0.30, roar=0.15, seed=3), 2.2, 0.5, 3000), 0.16, 'fx')
for b in range(0, 8):
    u = b / 7.0                             # one instrument every two bars
    latin(b, gain=0.70 + 0.45 * u, bell=0.0, cas=1.15 if b >= 6 else 0.0,
          mar=1.0 if b >= 2 else 0.0, gui=1.1 if b >= 4 else 0.0,
          clv=1.05 + 0.30 * u)
    if b >= 6:
        congas(b, 0.85)
abanico(7, 12, 0.7)

# ------------------------------------- b8-15: the rhythm section, complete --
for b in range(8, 16):
    latin(b, gain=1.15, bell=0.95 if b >= 10 else 0.0, bong=1.0 if b >= 12 else 0.0)
    congas(b, 1.05)
s.place(s.pos(12), reverse_crash(8), 0.20, 'fx')
abanico(15, 10, 0.85, n=8)

# --------------------------------------- b16-31: the bass, and the piano ---
for b in range(16, 32):
    latin(b, gain=1.0, bong=0.9)
    congas(b, 0.92, quinto=0.5 if b % 8 == 6 else 0.0, seed=b)
    bassline(b, 0.62, sub=0.55, extra=(b % 4 == 3))
    if b >= 20:
        piano(b, 0.50 if b < 24 else 0.62, vel=0.72 if b < 24 else 0.85)
s.place(s.pos(24), reverse_crash(8), 0.22, 'fx')
abanico(31, 8, 1.0, n=10)
s.place(s.pos(31, 12), subdrop(6, 78, 33), 0.30, 'bass')
s.place(s.pos(32), impact(20), 0.34, 'fx')
s.place(s.pos(32), CR, 0.55)

# ============================== b32-63: DROP 1 - the break arrives ==========
for b in range(32, 64):
    heat = 0.42 + 0.22 * ((b - 32) / 31)
    if b % 16 == 15:
        cracked(b, 0.95, seed=b)
    else:
        clavebreak(b, 0.95, ghost=0.55, heat=heat, seed=1, snare=1.0)
    latin(b, gain=1.0, bong=0.85, gui=0.8, mar=0.9)
    congas(b, 0.95, quinto=0.55 if b % 8 == 6 else 0.0, seed=b, heavy=1.0)
    bassline(b, 0.90, sub=0.82, extra=(b % 4 == 3))
    piano(b, 0.66, vel=0.90)
    if b % 8 == 7:
        abanico(b, 13, 0.8, n=5)
s.place(s.pos(48), CR, 0.45)
stab(47, 12, ((79, 'trumpet'), (76, 'trumpet'), (60, 'bone')), 0.55, dur=3.0)

# =================================== b64-79: the mona ======================
for b in range(64, 80):
    clavebreak(b, 0.90, ghost=0.42, heat=0.42, seed=2, top=0.75)
    latin(b, gain=0.95, bell=0.9, bong=0.7, gui=0.7)
    congas(b, 0.92, heavy=1.0)
    bassline(b, 0.90, sub=0.82, extra=(b % 4 == 3))
    piano(b, 0.52, vel=0.82)
for b0 in (64, 68, 72, 76):
    horns(b0, 0.60, vel=1.0, bright=1.0)
abanico(79, 10, 0.9, n=8)
s.place(s.pos(79, 14), downlifter(4, 0.5), 0.22, 'fx')

# =============================== b80-95: the descarga ======================
# The drums stop. This is the jam the section is named after: the piano takes
# the montuno up an octave and stretches it, the quinto answers, and the clave
# never once stops - it is the only thing in the room that is not improvising.
for b in range(80, 96):
    u = (b - 80) / 15.0                     # the room fills back up over 16 bars
    latin(b, gain=0.55 + 0.45 * u,
          bell=0.0 if b < 86 else (b - 86) / 9.0,
          cas=0.0 if b < 84 else 0.85,
          mar=0.35 + 0.65 * u, gui=0.4 + 0.5 * u, bong=0.0 if b < 88 else 0.9)
    congas(b, 0.62 + 0.38 * u, quinto=0.9 if b % 4 in (1, 3) else 0.45,
           seed=b * 3, heavy=1.0)
    bassline(b, 0.55 + 0.35 * u, sub=0.55 + 0.2 * u, extra=True, decay=0.55)
    solo(b, 80, 0.62 + 0.24 * u, vel=0.80 + 0.15 * u)
    if b >= 88:                             # the break walks back in, filtered
        clavebreak(b, 0.70 + 0.28 * u, ghost=0.40, heat=0.45, seed=5, bus='brk')
    if b == 84:
        stab(b, 8, ((77, 'trumpet'), (74, 'trumpet'), (62, 'bone')), 0.42, dur=4.0)
    if b == 86:
        stab(b, 4, ((76, 'trumpet'), (72, 'trumpet'), (57, 'bone')), 0.42, dur=4.0)
s.place(s.pos(80), reverse_crash(12), 0.24, 'fx')

# ============================== b96-103: the build =========================
for b in range(96, 104):
    u = (b - 96) / 7.0
    clavebreak(b, 0.80 + 0.22 * u, ghost=0.30 + 0.45 * u, heat=0.35 + 0.40 * u,
               seed=7, snare=0.9)
    latin(b, gain=0.85 + 0.20 * u, bell=1.0, mar=1.0, gui=0.8, bong=1.0)
    congas(b, 0.90 + 0.28 * u, heavy=1.0)
    bassline(b, 0.80, sub=0.75 - 0.5 * u, extra=True)
    piano(b, 0.55 + 0.14 * u, oct_=1, vel=0.9)
    # the cascara doubles: the shell goes to sixteenths and climbs
    if b >= 100:
        for st in range(16):
            pp(b, st, cascara(seed=(b * 3 + st) % 23,
                              vel=0.5 + 0.5 * ((b - 100) * 16 + st) / 63),
               0.30 + 0.30 * u, 'cascara')
s.place(s.pos(100), riser(64, 0.42, 200, 1400), 1.0, 'fx')
s.place(s.pos(100), crowd(64, 0.30, roar=0.5, seed=11), 0.18, 'fx')
abanico(103, 8, 1.1, n=12)
for b0, st in ((102, 0), (103, 0)):
    stab(b0, st, ((79, 'trumpet'), (76, 'trumpet'), (64, 'bone')), 0.5, dur=6.0, vel=1.2)
# the last beat is empty. Everything above is written so that it can be.
s.place(s.pos(103, 12), downlifter(4, 0.6, 1400, 70), 0.26, 'fx')
s.place(s.pos(103, 12), subdrop(8, 82, 30), 0.34, 'bass')
s.place(s.pos(104), impact(24), 0.40, 'fx')
s.place(s.pos(104), CR, 0.70)

# ============================ b104-151: DROP 2, 48 bars ====================
for b in range(104, 152):
    u = (b - 104) / 47.0
    if b % 16 == 15:
        cracked(b, 1.0, seed=b + 3)
    else:
        clavebreak(b, 1.0, ghost=0.60, heat=0.50 + 0.18 * u, seed=13)
    latin(b, gain=1.0, bell=1.0, bong=0.85, gui=0.75, mar=0.95)
    congas(b, 1.0, quinto=0.7 if b % 8 in (5, 6) else 0.0, seed=b * 7, heavy=1.0)
    bassline(b, 0.95, sub=0.88, extra=(b % 4 == 3))
    piano(b, 0.66, oct_=1 if b >= 120 else 0, vel=0.92)
    if b % 8 == 7:
        abanico(b, 13, 0.75, n=5)
for b0 in (104, 108, 120, 124, 136, 140, 144, 148):
    horns(b0, 0.58 if b0 < 136 else 0.68, vel=1.0 if b0 < 136 else 1.15,
          bright=1.0 if b0 < 136 else 1.15, oct_=0)
for b0 in (112, 116, 128, 132):
    stab(b0, 8, ((79, 'trumpet'), (76, 'trumpet'), (60, 'bone')), 0.5, dur=3.0)
    stab(b0 + 2, 4, ((77, 'trumpet'), (74, 'trumpet'), (62, 'bone')), 0.45, dur=3.0)
s.place(s.pos(120), CR, 0.45)
s.place(s.pos(136), CR, 0.50)
for pb in (119, 135):
    for bus in ('main', 'perc', 'music', 'bass', 'horns'):
        if bus in s.bus:
            a0, e0 = s.pos(pb, 8), s.pos(pb + 1)
            s.bus[bus][a0:e0] *= np.linspace(1.0, 0.0, e0 - a0)[:, None] ** 2.5
    stab(pb, 8, ((81, 'trumpet'), (76, 'trumpet'), (64, 'bone')), 0.62, dur=2.0, vel=1.3)
    pp(pb, 8, conga(TUMBA, 'open', vel=1.1, size=1.35, seed=2), 0.9, 'tumba')
    s.place(s.pos(pb, 8), K, 0.9)
pregon(148, 0.42, vel=0.85, bright=0.9)

# ============================== b152-167: the mambo ========================
# The section every salsa arrangement has and no jungle record does: the horns
# stop punctuating and take the tune, the piano drops to answering them in the
# gaps, and the drums thin out under both. Call and response, which is the
# oldest structure this music has.
for b in range(152, 168):
    if b % 4 in (0, 1):
        clavebreak(b, 0.75, ghost=0.30, heat=0.30, seed=17, top=0.5)
    else:
        s.place(s.pos(b, 0), K, 0.75)
        s.place(s.pos(b, 12), SN, 0.75)
        s.hit(s.pos(b, 0))
    latin(b, gain=1.0, bell=0.95, bong=0.9, gui=0.85, mar=1.0)
    congas(b, 1.0, quinto=0.6 if b % 4 == 3 else 0.0, seed=b * 11, heavy=1.0)
    bassline(b, 0.88, sub=0.78, extra=True)
    piano(b, 0.40 if b % 4 in (0, 2) else 0.62, vel=0.85)   # answering, not leading
for b0 in (152, 160):
    pregon(b0, 0.66, vel=1.05, bright=1.05)
for b0 in (156, 164):
    pregon(b0, 0.66, vel=1.15, bright=1.15, oct_=0)
    stab(b0 + 3, 12, ((81, 'trumpet'), (76, 'trumpet'), (64, 'bone')), 0.5, dur=3.0)
for b0 in (155, 159, 163, 167):
    abanico(b0, 12, 0.75, n=5)
s.place(s.pos(164), riser(64, 0.30, 240, 1500), 0.85, 'fx')
abanico(167, 8, 1.1, n=12)
s.place(s.pos(167, 14), subdrop(6, 80, 30), 0.32, 'bass')
s.place(s.pos(168), impact(24), 0.42, 'fx')
s.place(s.pos(168), CR, 0.70)

# ====================== b168-199: DROP 3 - the floor ========================
for b in range(168, 200):
    u = (b - 168) / 31.0
    if b % 16 == 15:
        cracked(b, 1.0, seed=b + 5)
    else:
        clavebreak(b, 0.95, ghost=0.55, heat=0.55, seed=19)
    bombo(b, 0.72, half=(b < 172))
    latin(b, gain=1.0, bell=1.0, bong=0.9, gui=0.8, mar=1.0)
    congas(b, 1.0, quinto=0.75 if b % 8 in (5, 6) else 0.0, seed=b * 13, heavy=1.0)
    bassline(b, 0.95, sub=0.92, extra=(b % 4 == 3))
    piano(b, 0.68, oct_=1 if b >= 184 else 0, vel=0.95)
    if b % 8 == 7:
        abanico(b, 13, 0.8, n=6)
for b0 in (168, 172, 180, 184, 192, 196):
    horns(b0, 0.70, vel=1.15, bright=1.2)
for b0 in (176, 178, 188, 190):
    stab(b0, 8, ((81, 'trumpet'), (77, 'trumpet'), (62, 'bone')), 0.55, dur=3.0)
for b0 in (172, 188):
    pregon(b0, 0.62, vel=1.1, bright=1.15)
s.place(s.pos(184), CR, 0.50)

# ============================== b200-215: the outro ========================
for b in range(200, 216):
    u = (b - 200) / 15.0
    if b < 206:
        clavebreak(b, 0.85 - 0.35 * u, ghost=0.35, heat=0.35, seed=23, top=0.6)
        bombo(b, 0.55 * (1 - u))
    elif b < 210:
        s.place(s.pos(b, 0), K, 0.55)
        s.place(s.pos(b, 12), SN, 0.5)
        s.hit(s.pos(b, 0))
    latin(b, gain=1.0 - 0.5 * u,
          bell=1.0 if b < 210 else 0.0,
          cas=1.0 if b < 208 else 0.0,
          bong=0.8 if b < 206 else 0.0,
          gui=0.8 if b < 210 else 0.0,
          mar=1.0 if b < 212 else 0.0,
          clv=1.0)
    if b < 212:
        congas(b, 0.95 - 0.5 * u, heavy=1.0)
    if b < 208:
        bassline(b, 0.85 - 0.5 * u, sub=0.8, extra=False)
        piano(b, 0.60 - 0.35 * u, vel=0.85)
pregon(200, 0.50, vel=0.9, bright=0.95)
stab(204, 8, ((76, 'trumpet'), (72, 'trumpet'), (57, 'bone')), 0.45, dur=6.0)
s.place(s.pos(207), reverse_crash(8), 0.20, 'fx')
# the clave stops last, because it started first
pp(215, 12, clave(4.0, seed=1), 0.85, 'clave')

# ================================================================== mix =====
# The break walks back in through a filter that opens over eight bars: the
# only place on the record where an EDM gesture is the right one, because the
# descarga has to hand back to a drop and a timbale fill alone will not do it.
if 'brk' in s.bus:
    a, e = s.pos(88), s.pos(96)
    seg = s.bus['brk'][a:e]
    s.bus['brk'][a:e] = morph_lp(seg, 320.0, 14000.0,
                                 np.linspace(0, 1, len(seg)) ** 0.7)
    s.bus['main'] += s.bus['brk'] * 0.85
    del s.bus['brk']

s.bus['perc'] = hp(s.bus['perc'], 120, order=2)
s.bus['perc'] = bus_reverb(s.bus['perc'], decay=0.85, wet=0.16, tone=5200)
s.bus['horns'] = bus_reverb(s.bus['horns'], decay=1.1, wet=0.24, tone=4800)
s.bus['music'] = bus_reverb(s.bus['music'], decay=0.9, wet=0.14, tone=5000)
s.bus['music'] = mono_below(s.bus['music'], 220)
s.bus['horns'] = mono_below(s.bus['horns'], 300)
s.bus['perc'] = mono_below(s.bus['perc'], 200)
s.bus['bass'] = mono_below(s.bus['bass'], 120)
# The break is the loudest thing on a jungle record and it is also the only
# source of anything above 5 kHz here - a Cuban rhythm section is a mid-range
# instrument almost all the way up. Shelve it, then carve the percussion where
# the snare lives so the two are not both shouting at 2 kHz.
s.bus['main'] = shelf(shelf(s.bus['main'], 5200, 3.4), 10000, 5.5)
s.bus['perc'] = peak_eq(peak_eq(s.bus['perc'], 1700, -1.8, 0.8), 700, -1.6, 0.7)
s.bus['perc'] = shelf(s.bus['perc'], 8500, 4.2)
s.bus['music'] = shelf(peak_eq(s.bus['music'], 300, -2.2, 0.8), 9000, 2.0)
s.bus['bass'] = peak_eq(s.bus['bass'], 90, -1.5, 1.0)

GAINS = {'main': 0.88, 'perc': 0.50, 'bass': 0.40, 'music': 0.44,
         'horns': 0.54, 'fx': 0.38}
s.report(GAINS)
# 0.83 rather than the usual 0.94: the inter-sample peaks of this mix run
# 0.66 dB above its sample peaks, and a lossy encoder and a D/A converter both
# see the higher number. -1 dBTP is the ceiling that costs nothing, because
# every platform normalises the loudness back anyway.
s.render('amen_descarga_174.wav', drive=1.0, duck=0.16, limit=0.94,
         clip=1.0, gains=GAINS, fade=2.0, peak=0.83)
