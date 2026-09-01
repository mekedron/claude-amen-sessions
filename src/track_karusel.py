"""KARUSEL - funky neurofunk, G Dorian, 174 BPM.

The same sound design as `track_bezdna.py` and the opposite mood. Three
decisions do all of it:

- **Dorian, not Aeolian.** The natural 6 (E in G minor) is the one note that
  stops a minor key sounding sad, and the bass and the topline both land on
  it on purpose. The chords go i - IV - bIII - ii, and that IV is major.
- **The bass bounces instead of holding.** `funkmid` closes its filter in
  70 ms, so every note has a bright front, a dark back and a gap after it.
  A growl fills its note; this one leaves three quarters of it empty.
- **Swing on the top layer only.** The kick and the snare stay dead on the
  grid at 174 BPM; the hats, the chank and the arp are pushed 6% of a step
  late. Straight underneath, shuffled on top - which is a garage trick, and
  the reason this moves sideways rather than forward.

The hook is a two-bar riff, not an arpeggio. Sixteen sixteenths of a rising
pool is a plugin playing a scale: in key, no shape, nothing to remember.
This is eight events a bar with holes in it, a repeated note carrying a
ratchet, an arch to G5 and one surprise - and every note is a `neurolead`,
which is the bass an octave and a half up: hard sync tearing upward inside
the note while the pitch stays put, stepped so the timbre has its own rhythm.
A smooth sweep moves the centre of a note's spectrum about 1.4 octaves; a
stepped one moves it 2.6 and puts ten times as much energy above 2.5 kHz.

Underneath it the carousel turns: seven notes on a sixteen-step bar, so it
starts somewhere new every bar and does not come back round for seven of
them. It is texture, and in the intro it is alone.

    intro     0-15    the hook alone, and the room it turns in
    approach  16-31
    build 1   32-39
    DROP 1    40-71   the bounce
    breakdown 72-87   chords, and the topline says the tune out loud
    build 2   88-95
    DROP 2    96-127  the bass learns to talk back
    bridge    128-139 halftime funk: clav, shuffle, no neuro at all
    build 3   140-147
    DROP 3    148-179 hook, bass and chank at once
    outro     180-195
"""
import numpy as np
from neurolib import *

s = Session(196, tail=3.0)
rs = np.random.RandomState(1974)

# ---- G Dorian: G A Bb C D E F, and the E is the whole point ----
G1, A1, Bb1, C2, D2, E1, F1 = 31, 33, 34, 36, 38, 28, 29
G2, A2, Bb2, C3, D3, E3, F2 = 43, 45, 46, 48, 50, 52, 41
G3, Bb3, C4, D4, E4, F4 = 55, 58, 60, 62, 64, 65
G4, A4, Bb4, C5, D5, E5, F5, G5 = 67, 69, 70, 72, 74, 76, 77, 79

CHORDS = [[55, 58, 62, 65, 69],      # Gm9
          [48, 52, 58, 62, 69],      # C13   - the major IV, with the E in it
          [58, 62, 65, 69, 72],      # Bbmaj9
          [57, 60, 64, 67, 74]]      # Am11
CHANK = [(58, 62, 65), (60, 64, 70), (58, 62, 69), (57, 60, 64)]

SWING = 0.06                          # of a step, on the offbeat 16ths only

HAT_V = [1.00, 0.44, 0.74, 0.40, 0.94, 0.44, 0.80, 0.46,
         0.98, 0.42, 0.74, 0.40, 0.92, 0.46, 0.82, 0.58]

CELLS_A = [dict(k=(0, 10), s=(4, 12), g=(2, 6, 9, 14), o=(6,), r=(2, 6, 10, 14)),
           dict(k=(0, 6.5, 10), s=(4, 12), g=(2, 9, 13, 15), o=(14,), r=(2, 10)),
           dict(k=(0, 10, 11), s=(4, 12), g=(2, 6.5, 9, 14.5), o=(6,), r=(2, 6, 14)),
           dict(k=(0, 10, 15), s=(4, 12, 14), g=(2, 6, 9), o=(), r=(6, 10))]

CELLS_B = [dict(k=(0, 8.5, 10), s=(4, 12), g=(2.5, 6, 9, 13, 15), o=(6,), r=(2, 10, 14)),
           dict(k=(0, 10), s=(4, 12, 15), g=(2, 5.5, 9, 13), o=(14,), r=(2, 6, 10)),
           dict(k=(0, 3.5, 10), s=(4, 12), g=(2, 7, 9, 14), o=(6,), r=(6, 14)),
           dict(k=(0, 10, 12.5), s=(4, 12, 14.5), g=(2.5, 6, 9), o=(), r=(2, 10))]


def sw(st):
    """push the offbeat 16ths late; leave the downbeats where they are"""
    return st + (SWING if int(round(st)) % 2 else 0.0)


# ---- the kit ----
def drums(b, cell, gain=1.0, hats=1.0, ghosts=1.0, ride=1.0, sidechain=True,
          seed=0, bus='drums'):
    for st in cell['k']:
        t = s.pos(b, st)
        s.place(t, nkick(), gain * 1.08, bus)
        if sidechain:
            s.hit(t)
    for i, st in enumerate(cell['s']):
        v = 1.0 if st in (4, 12) else 0.55
        s.place(s.pos(b, st + rs.randn() * 0.012),
                nsnare(seed=(seed + i) % 3), gain * v * 1.05, bus)
    if ghosts:
        for i, st in enumerate(cell['g']):
            s.place(s.pos(b, sw(st) + rs.randn() * 0.02), nghost(seed=(seed + i) % 4),
                    gain * ghosts * rs.uniform(0.22, 0.40), bus)
    if ride:
        for i, st in enumerate(cell.get('r', ())):
            s.place(s.pos(b, sw(st) + rs.randn() * 0.015),
                    nride(2.0, tone=0.96 + 0.05 * (i % 3), seed=i % 3),
                    gain * ride * 0.34, bus)
    if hats:
        loud = set(cell['k']) | set(cell['s'])
        for i in range(16):
            if i in loud:
                continue
            op = i in cell['o']
            shade = 0.45 if any(0 < i - k <= 1 for k in loud) else 1.0
            s.place(s.pos(b, sw(i) + rs.randn() * 0.018),
                    nhat(open_=op, tone=1.0 + 0.04 * (i % 3), seed=i % 4),
                    gain * hats * HAT_V[i] * (0.75 if op else 1.0) * shade * 0.52, bus)


def subline(b, notes, gain=1.0, bus='sub'):
    for i, (st, note, dur) in enumerate(notes):
        end = notes[i + 1][0] if i + 1 < len(notes) else st + dur
        s.place(s.pos(b, st), nsub(note, min(dur, end - st + 0.4), decay=0.5), gain, bus)


def bassline(b, notes, gain=1.0, bus='bass'):
    for st, voice, note, dur, g, kw in notes:
        s.place(s.pos(b, st), voice(note, dur, **kw), gain * g, bus)


def chanks(b, steps_, chord, gain=1.0, seed=0):
    for i, st in enumerate(steps_):
        s.place(s.pos(b, sw(st) + rs.randn() * 0.015),
                chank(tuple(midi(n) for n in chord), 1.2, seed=(seed + i) % 4),
                gain * (0.9 if int(round(st)) % 4 == 2 else 0.62), 'music')


# ---- the riff ----
def F_(note, dur, **kw):  return (funkmid, note, dur, 1.0, kw)
def T_(note, dur, **kw):  return (talkline, note, dur, 0.9, kw)
def R_(note, dur, **kw):  return (reesemid, note, dur, 0.9, kw)
def S_(note, dur, **kw):  return (screech, note, dur, 0.8, kw)


def riff_a(bar_even):
    """Drop 1. Octave pops on the offbeats, the sub anchored on G, and every
    second bar answered by something that talks."""
    if bar_even:
        sub = [(0, G1, 6), (6.5, G1, 3.5), (10, G1, 6)]
        mid = [(0, *F_(G2, 1.6)),
               (2, *F_(G3, 1.1, decay=0.05)),
               (3.5, *F_(G2, 1.2)),
               (5, *F_(Bb2, 1.4)),
               (6.5, *T_(G2, 2.2, vowels=('oo', 'ah', 'ee'))),
               (9, *F_(G3, 1.0, decay=0.05)),
               (11, *F_(F2, 1.5)),
               (13, *T_(C3, 2.6, vowels=('ah', 'ee', 'oh')))]
    else:
        sub = [(0, G1, 5), (5, Bb1, 3), (8, C2, 3), (11, E1, 5)]
        mid = [(0, *F_(G2, 1.6)),
               (2, *T_(Bb2, 1.6, vowels=('ee', 'ah'))),
               (3.5, *F_(C3, 1.1, decay=0.05)),
               (5, *F_(D3, 1.4)),
               (6.5, *R_(G2, 2.2, rate=1.4, tilt=5.0)),
               (8.5, *F_(E3, 1.1, decay=0.045)),      # the Dorian 6, up high
               (10, *F_(D3, 1.2)),
               (11.5, *T_(C3, 2.0, vowels=('oo', 'ee'))),
               (13.5, *F_(Bb2, 1.4)),
               (15, *S_(G3, 1.3, r0=1.5, r1=6.0))]
    return sub, mid


def riff_b(bar_even):
    """Drop 2. The bass answers itself: a bouncing phrase, then the same
    phrase saying a word instead of playing a note."""
    if bar_even:
        sub = [(0, G1, 8), (8, G1, 8)]
        mid = [(0, *F_(G2, 1.5)),
               (1.5, *F_(G2, 1.0, decay=0.05)),
               (3, *F_(Bb2, 1.3)),
               (5, *T_(G2, 2.4, vowels=('oo', 'ah', 'ee', 'oh'))),
               (8, *F_(G3, 1.2, decay=0.05)),
               (9.5, *F_(F2, 1.3)),
               (11, *F_(G2, 1.5)),
               (13, *T_(D3, 2.6, vowels=('ee', 'ah', 'oo')))]
    else:
        sub = [(0, G1, 6), (6, F1, 2), (8, Bb1, 4), (12, C2, 4)]
        mid = [(0, *R_(G2, 2.4, rate=1.2, tilt=5.0)),
               (2.5, *F_(D3, 1.2, decay=0.05)),
               (4.5, *F_(C3, 1.3)),
               (6, *T_(Bb2, 2.2, vowels=('ah', 'ee'))),
               (8.5, *F_(Bb2, 1.2)),
               (10, *F_(D3, 1.2, decay=0.05)),
               (11.5, *F_(E3, 1.2, decay=0.045)),
               (13, *T_(C3, 2.4, vowels=('oo', 'ee', 'ah'))),
               (15.5, *S_(G3, 1.2, r0=2.0, r1=7.5))]
    return sub, mid


def riff_c(bar_even):
    """Drop 3. Both, plus the octave pops doubled a fifth up."""
    if bar_even:
        sub = [(0, G1, 6), (6.5, G1, 3.5), (10, G1, 6)]
        mid = [(0, *F_(G2, 1.6, f_hi=8000)),
               (2, *F_(G3, 1.0, decay=0.045)),
               (3.5, *F_(D3, 1.1, decay=0.05)),
               (5, *F_(Bb2, 1.4, f_hi=8000)),
               (6.5, *T_(G2, 2.2, vowels=('oo', 'ah', 'ee'))),
               (9, *F_(G3, 1.0, decay=0.045)),
               (10.5, *S_(D4, 1.2, r0=1.8, r1=6.5)),
               (13, *T_(C3, 2.6, vowels=('ah', 'ee', 'oh')))]
    else:
        sub = [(0, G1, 5), (5, Bb1, 3), (8, C2, 3), (11, E1, 5)]
        mid = [(0, *R_(G2, 2.2, rate=1.3, tilt=5.5)),
               (2, *T_(Bb2, 1.6, vowels=('ee', 'ah'))),
               (3.5, *F_(C3, 1.1, decay=0.045)),
               (5, *F_(D3, 1.4, f_hi=8000)),
               (6.5, *F_(G3, 1.6, decay=0.05)),
               (8.5, *F_(E3, 1.1, decay=0.045)),
               (10, *F_(D3, 1.2)),
               (11.5, *T_(C3, 2.0, vowels=('oo', 'ee'))),
               (13.5, *F_(Bb2, 1.4)),
               (15, *S_(G4, 1.3, r0=2.4, r1=9.0))]
    return sub, mid


HOLES = {63, 119}


def play_riff(b, riff, gain=1.0, sub_gain=1.0):
    sub, mid = riff(b % 2 == 0)
    if b in HOLES:
        sub = [e for e in sub if e[0] < 11]
        mid = [e for e in mid if e[0] < 11]
    subline(b, sub, sub_gain)
    bassline(b, mid, gain)


HOLE_CELL = dict(k=(0, 10), s=(4,), g=(2, 6, 9), o=(6,), r=(2, 6))


def section_bar(b, cell, chank_steps, chord, seed):
    """one bar of a drop, or the hole that makes the next one land"""
    if b in HOLES:
        drums(b, HOLE_CELL, seed=seed)
        chanks(b, tuple(st for st in chank_steps if st < 11), chord, 0.30, seed=b)
        s.place(s.pos(b, 12), reverse_crash(4, gain=0.55), bus='fx')
        s.place(s.pos(b, 14), blip(midi(G5), 2.0, bend=0.6), 0.34, bus='music')
        return True
    drums(b, cell, seed=seed)
    chanks(b, chank_steps, chord, 0.30 if b < 96 else 0.32, seed=b)
    return False


# ---- the riff ----
# Sixteen sixteenths of a rising pool is an arpeggiator, not a hook: in key,
# no shape, nothing to remember. This is a two-bar motif instead - a rhythm
# you could clap, holes in it, one repeated note carrying a ratchet, an arch
# to G5 and one surprise (the Dorian E, late). Eight events a bar, not
# sixteen.
#
# The fourth column is the sync ratio each note tears up to and the fifth is
# the stepped pattern it tears in, locked per note the way a 303 pattern locks
# accent and slide. No two events in the bar reach the same ratio or step the
# same way, so no two are the same instrument - which is what makes a line
# read as sound design rather than as a preset playing a scale.
RIFF = [
    (0.0,  D5,  1.5,  4.5, dict(pattern=(1.0, 0.25, 0.8, 0.35, 0.95, 0.3))),
    (2.0,  D5,  0.45, 6.0, dict(pattern=(0.2, 1.0))),
    (2.5,  D5,  0.45, 7.5, dict(pattern=(1.0, 0.25))),                # ratchet
    (3.0,  F5,  1.0,  3.4, dict(pattern=(0.3, 0.95, 0.5))),
    (6.0,  G5,  2.0,  5.5, dict(pattern=(0.15, 1.0, 0.4, 0.85, 0.25, 1.0, 0.5, 0.9),
                                vowels=('ah', 'ee'))),                # the peak
    (10.0, F5,  1.0,  4.0, dict(pattern=(0.9, 0.3, 1.0))),
    (11.0, D5,  1.0,  3.0, dict(pattern=(0.25, 0.8, 0.4))),
    (14.0, C5,  1.5,  6.5, dict(pattern=(0.2, 1.0, 0.4, 0.9, 0.3, 1.0))),
    (16.0, D5,  1.5,  4.5, dict(pattern=(1.0, 0.25, 0.8, 0.35, 0.95, 0.3))),
    (18.0, D5,  0.45, 6.0, dict(pattern=(0.2, 1.0))),
    (18.5, D5,  0.45, 8.0, dict(pattern=(1.0, 0.3))),
    (19.0, C5,  1.0,  3.4, dict(pattern=(0.3, 0.95, 0.5))),
    (22.0, Bb4, 2.0,  5.0, dict(pattern=(0.2, 0.9, 0.35, 1.0, 0.3, 0.85, 0.45, 1.0),
                                vowels=('oo', 'ah'))),
    (26.0, C5,  1.0,  4.0, dict(pattern=(0.9, 0.3, 1.0))),
    (28.0, E5,  1.5,  7.0, dict(pattern=(0.15, 1.0, 0.5, 0.85, 0.3, 1.0))),
    (31.0, D5,  1.0,  5.0, dict(pattern=(1.0, 0.35, 0.9))),
]

# The carousel: seven notes on a sixteen-step bar, so it starts somewhere new
# every bar and does not come back round for seven of them. It is texture,
# not the hook - it turns underneath the riff and alone in the intro.
CAROUSEL = arp_seq([67, 70, 72, 74, 77], bars=1, shape='updown', rate=1.0,
                   cycle=7, octaves=(0, 1), accents=(0, 4), ratchets=(5,),
                   tail=0.8, jitter=0.02, swing=SWING, seed=11)


def riff(b, gain=1.0, bright=1.0, half=None, bus='music'):
    """the two-bar motif; `b` must be the first bar of the pair"""
    for st, note, dur, r1, kw in RIFF:
        if half == 0 and st >= 16:
            continue
        if half == 1 and st < 16:
            continue
        bar, step = b + int(st // 16), st % 16
        s.place(s.pos(bar, sw(step)),
                neurolead(note, dur, r1=r1, f_hi=9500 * bright,
                          decay=0.075 if dur < 1.0 else 0.095, **kw),
                gain * (1.0 if step in (0, 6, 22 % 16) else 0.82), bus)


def carousel(b, gain=1.0, bright=1.0, bus='music'):
    for st, note, dur, v in CAROUSEL:
        s.place(s.pos(b, st),
                neurolead(note, dur, r1=1.4 + 0.4 * ((note + int(st)) % 3),
                          f_hi=6200 * bright, f_lo=520, res=1.8, decay=0.055,
                          drive=2.0, low=340),
                gain * v * 0.7, bus)


# ---- 0-15  the room the carousel turns in ----
s.place(s.pos(0), voidpad([midi(n) for n in (55, 62, 67)], 16 * 16, cutoff=1200,
                          gain=0.30, seed=3), bus='pad')
s.place(s.pos(0), crackle(16 * 16, gain=0.5), bus='atmos')
for b in range(16):
    carousel(b, gain=0.24 + 0.030 * b, bright=0.45 + 0.045 * b)
for b in (10, 12, 14):
    riff(b, gain=0.30, bright=0.75, half=0)
for b in (4, 8, 12):
    chanks(b, (2, 6, 10, 14), CHANK[0], 0.26, seed=b)
s.place(s.pos(6), whoop(8, gain=0.5), bus='fx')
s.place(s.pos(12), whoop(12, f0=220, f1=1900, gain=0.55), bus='fx')
for b, st in ((5, 12), (9, 4), (13, 8)):
    s.place(s.pos(b, st), reverb(nsnare(6, room=0.6), 2.0, 0.5, 4200), 0.45, bus='fx')
s.place(s.pos(14), riser(32, gain=0.4, f0=140, f1=700), bus='fx')
s.place(s.pos(15, 12), whoosh(8, gain=0.5, rev_=True), bus='fx')

# ---- 16-31  approach ----
s.place(s.pos(16), voidpad([midi(n) for n in (55, 62, 67, 74)], 16 * 16,
                           cutoff=1600, gain=0.24, seed=7), bus='pad')
for b in range(16, 32):
    i = b - 16
    cell = CELLS_A[i % 4]
    up = min(1.0, i / 12.0)
    drums(b, cell, gain=0.32 + 0.55 * up, hats=0.6 + 0.4 * up, ghosts=0.5,
          ride=0.5 + 0.5 * up, seed=b)
    carousel(b, gain=0.26, bright=0.9)
    if i % 2 == 0 and i >= 4:
        riff(b, gain=0.34, bright=0.95)
    if i >= 4:
        subline(b, [(0, G1, 8), (8, G1, 8)], 0.55 + 0.35 * up)
    if i >= 8:
        chanks(b, (2, 6, 10, 14), CHANK[(i // 4) % 4], 0.28 * up, seed=b)
    if i >= 8:
        g = 0.4 + 0.35 * up
        bassline(b, [(2, funkmid, G2, 1.4, g, {}),
                     (6.5, funkmid, Bb2, 1.4, g, {}),
                     (11, funkmid, G2, 1.4, g, {}),
                     (13.5, talkline, C3, 2.0, g * 0.8, dict(vowels=('oo', 'ee')))])
s.place(s.pos(24), whoop(6, gain=0.4), bus='fx')

# ---- 32-39  build 1 ----
for b in range(32, 40):
    i = b - 32
    drums(b, CELLS_A[i % 4], gain=0.85 - 0.30 * (i / 8) ** 2, hats=1.0 - 0.4 * (i / 8) ** 2,
          ghosts=0.7, seed=b)
    subline(b, [(0, G1, 8), (8, G1, 8)], 0.8 * (1 - i / 12))
    carousel(b, gain=0.22, bright=1.0 + 0.06 * i)
    if i % 2 == 0:
        riff(b, gain=0.40 + 0.03 * i, bright=1.0 + 0.06 * i)
    chanks(b, (2, 6, 10, 14), CHANK[i % 4], 0.30, seed=b)
s.place(s.pos(32), riser(8 * 16, gain=0.5, f0=150, f1=2000), bus='fx')
roll(s, 38, 0, 8, spacing=2.0, gain=0.34, seed=1)
roll(s, 39, 0, 8, spacing=1.0, gain=0.44, seed=2)
roll(s, 39, 8, 6, spacing=0.5, gain=0.56, accel=True, seed=3)
s.place(s.pos(39, 12), whoop(4, f0=400, f1=2200, gain=0.6), bus='fx')
s.place(s.pos(40) - int(2.2 * STEP), subdrop(6, f0=115, f1=32, gain=0.65), bus='fx')

# ---- 40-71  DROP 1 ----
for b in range(40, 72):
    i = b - 40
    hole = section_bar(b, CELLS_A[i % 4],
                       (2, 6, 10, 14) if i % 4 != 3 else (2, 6, 9, 10, 14),
                       CHANK[(i // 4) % 4], b)
    play_riff(b, riff_a)
    if i % 8 >= 4 and i % 2 == 0:
        riff(b, gain=0.34, bright=1.05, half=None if i % 8 == 4 else 1)
    if i % 16 == 15:
        roll(s, b, 12, 6, spacing=0.6, gain=0.7, accel=True, seed=b % 3)
    if i % 8 == 7:
        s.place(s.pos(b, 14.5), blip(midi(G5), 1.5), 0.30, bus='music')
s.place(s.pos(40), crash808(24, gain=0.45), bus='fx')
s.place(s.pos(40), impact(20, gain=0.42), bus='fx')
s.place(s.pos(56), crash808(16, gain=0.32), bus='fx')
s.place(s.pos(64), whoop(8, gain=0.35), bus='fx')

# ---- 72-87  breakdown: the tune, said out loud ----
s.place(s.pos(71, 12), downlifter(12, gain=0.5), bus='fx')
for i, ch in enumerate(CHORDS):
    b = 72 + i * 4
    s.place(s.pos(b), voidpad([midi(n) for n in ch], 4 * 16, cutoff=2100,
                              gain=0.28, seed=37 + i), bus='pad')
    s.place(s.pos(b), pad([midi(n + 12) for n in ch], 4 * 16, cutoff=3400,
                          gain=0.11, wide=1.3), bus='pad')
    s.place(s.pos(b), nsub((G1, C2, Bb1, A1)[i], 4 * 16, decay=3.0), 0.8, bus='sub')

TUNE = [[(0, D5, 2.5), (3, Bb4, 1.5), (6, G4, 2.5), (10, A4, 3.5), (14, Bb4, 2)],
        [(0, C5, 2.5), (3, A4, 1.5), (6, E5, 2.5), (10, D5, 5.0)],
        [(0, G5, 2.0), (4, F5, 2.0), (8, D5, 2.0), (12, C5, 4.0)],
        [(0, Bb4, 2.0), (3, A4, 1.5), (6, G4, 6.0)]]
for i in range(4):
    b = 72 + i * 4
    for bar in range(4):
        if bar in (1, 3):
            carousel(b + bar, gain=0.20, bright=1.0)
    for j, (st, note, dur) in enumerate(TUNE[i]):
        s.place(s.pos(b + 2, st), lead(midi(note), dur, gain=0.34), bus='music')
        s.place(s.pos(b + 2, st), glass(midi(note + 12), dur * 0.6, gain=0.16), bus='music')
        if j == 0:
            s.place_echo(s.pos(b + 2, st), blip(midi(note + 12), 1.0), 0.16,
                         times=3, delay_steps=3.0, fb=0.5, bus='music')
for b in (73, 77, 81, 85):
    chanks(b, (2, 6, 10, 14), CHANK[(b // 4) % 4], 0.22, seed=b)
s.place(s.pos(80), whoop(10, gain=0.4), bus='fx')
s.place(s.pos(86), nsnare(8, room=0.7), 0.35, bus='fx')

# ---- 88-95  build 2 ----
for b in range(88, 96):
    i = b - 88
    drums(b, CELLS_B[i % 4], gain=0.5 + 0.4 * i / 8 - 0.28 * (i / 8) ** 3,
          hats=0.85, ghosts=0.6, seed=b)
    subline(b, [(0, G1, 8), (8, G1, 8)], 0.5)
    carousel(b, gain=0.22, bright=1.0 + 0.05 * i)
    if i % 2 == 0:
        riff(b, gain=0.36 + 0.03 * i, bright=1.05 + 0.05 * i)
    chanks(b, (2, 6, 10, 14), CHANK[i % 4], 0.30, seed=b)
    s.place(s.pos(b), voidpad([midi(n) for n in CHORDS[i % 4]], 16,
                              cutoff=1800 + 260 * i, gain=0.16, seed=43 + i), bus='pad')
s.place(s.pos(88), riser(8 * 16, gain=0.55, f0=160, f1=2600), bus='fx')
roll(s, 94, 0, 8, spacing=2.0, gain=0.34, seed=4)
roll(s, 95, 0, 8, spacing=1.0, gain=0.45, seed=5)
roll(s, 95, 8, 7, spacing=0.5, gain=0.58, accel=True, seed=6)
s.place(s.pos(95, 12), whoop(4, f0=450, f1=2400, gain=0.65), bus='fx')
s.place(s.pos(96) - int(2.2 * STEP), subdrop(6, f0=125, f1=30, gain=0.7), bus='fx')

# ---- 96-127  DROP 2 ----
for b in range(96, 128):
    i = b - 96
    hole = section_bar(b, CELLS_B[i % 4], (2, 5, 6, 10, 14), CHANK[(i // 4) % 4], b)
    play_riff(b, riff_b)
    if i % 8 >= 4 and i % 2 == 0:
        riff(b, gain=0.32, bright=1.12)
    if i % 8 == 3:
        s.place(s.pos(b, 15), blip(midi(D5), 1.5, bend=0.5), 0.28, bus='music')
    if i % 16 == 15:
        roll(s, b, 13, 5, spacing=0.5, gain=0.75, accel=True, seed=b % 3)
s.place(s.pos(96), crash808(24, gain=0.45), bus='fx')
s.place(s.pos(96), impact(20, gain=0.45), bus='fx')
s.place(s.pos(112), crash808(16, gain=0.32), bus='fx')
for b in range(100, 128, 8):
    s.place(s.pos(b), orchhit(55, 3, gain=0.26), bus='music')

# ---- 128-139  bridge: halftime funk, no neuro in it at all ----
s.place(s.pos(127, 12), downlifter(10, gain=0.45), bus='fx')
s.place(s.pos(128), voidpad([midi(n) for n in (55, 62, 65)], 12 * 16, cutoff=1500,
                            gain=0.22, seed=59), bus='pad')
for b in range(128, 140):
    i = b - 128
    t = s.pos(b, 0); s.place(t, nkick(), 1.0, 'drums'); s.hit(t)
    if i % 2 == 0:
        t = s.pos(b, 10.5); s.place(t, nkick(), 0.8, 'drums'); s.hit(t)
    s.place(s.pos(b, 8), nsnare(6, room=0.5), 0.95, 'drums')
    for st in (2, 6, 11, 14):
        s.place(s.pos(b, sw(st) + rs.randn() * 0.02), nghost(seed=i % 4), 0.22, 'drums')
    for st in (2, 4, 6, 10, 12, 14):
        s.place(s.pos(b, sw(st)), nhat(open_=(st == 6), seed=i % 4), 0.26, 'drums')
    for st in (1, 3, 5, 7, 9, 11, 13, 15):
        s.place(s.pos(b, sw(st)), nride(1.6, tone=0.98, seed=i % 3), 0.14, 'drums')
    s.place(s.pos(b), dust(16, seed=b), 0.45, 'texture')
    ch = CHANK[i % 4]
    chanks(b, (2, 3, 6, 7, 10, 11, 14, 15), ch, 0.34, seed=b)
    s.place(s.pos(b, 0), clav([midi(n) for n in ch], 3.0, gain=0.30), bus='music')
    s.place(s.pos(b, 8), clav([midi(n + 5) for n in ch], 2.5, gain=0.22), bus='music')
    subline(b, [(0, G1, 6), (6, (G1, G1, Bb1, C2)[i % 4], 10)], 0.7)
    bassline(b, [(0, funkmid, G2, 1.6, 0.55, {}),
                 (3, funkmid, G3, 1.1, 0.5, dict(decay=0.05)),
                 (6, funkmid, Bb2, 1.4, 0.5, {}),
                 (10.5, funkmid, C3, 1.2, 0.5, {}),
                 (13, talkline, (G2, D3, Bb2, C3)[i % 4], 2.4, 0.45,
                  dict(vowels=('oo', 'ah', 'ee')))])
    if i % 4 == 3:
        s.place(s.pos(b, 14), blip(midi(G5), 1.5, bend=0.45), 0.26, bus='music')
s.place(s.pos(136), whoop(12, gain=0.45), bus='fx')

# ---- 140-147  build 3 ----
for b in range(140, 148):
    i = b - 140
    drums(b, CELLS_A[i % 4], gain=0.58 + 0.38 * i / 8 - 0.30 * (i / 8) ** 3,
          hats=0.9, ghosts=0.7, seed=b)
    subline(b, [(0, G1, 8), (8, G1, 8)], 0.55)
    carousel(b, gain=0.22, bright=1.05 + 0.05 * i)
    if i % 2 == 0:
        riff(b, gain=0.40 + 0.03 * i, bright=1.1 + 0.05 * i)
    chanks(b, (2, 6, 10, 14), CHANK[i % 4], 0.32, seed=b)
    s.place(s.pos(b), dust(16, seed=b + 7), 0.4, 'texture')
s.place(s.pos(140), riser(8 * 16, gain=0.6, f0=170, f1=3200), bus='fx')
roll(s, 146, 0, 8, spacing=2.0, gain=0.36, seed=7)
roll(s, 147, 0, 8, spacing=1.0, gain=0.48, seed=8)
roll(s, 147, 8, 8, spacing=0.5, gain=0.60, accel=True, seed=9)
s.place(s.pos(147, 12), whoop(4, f0=500, f1=2600, gain=0.7), bus='fx')
s.place(s.pos(148) - int(2.4 * STEP), subdrop(7, f0=135, f1=29, gain=0.75), bus='fx')

# ---- 148-179  DROP 3 ----
for b in range(148, 180):
    i = b - 148
    drums(b, CELLS_A[i % 4] if i % 8 < 4 else CELLS_B[i % 4], seed=b)
    s.place(s.pos(b), dust(16, seed=b + 3), 0.42, 'texture')
    if b != 171:
        play_riff(b, riff_c)
    else:
        subline(b, [(0, G1, 16)], 0.8)      # only the sub keeps the floor
    chanks(b, (2, 5, 6, 10, 13, 14), CHANK[(i // 4) % 4], 0.32, seed=b)
    if i % 2 == 0:
        riff(b, gain=0.38, bright=1.18)
    else:
        carousel(b, gain=0.18, bright=1.15)
    if i % 8 == 7:
        s.place(s.pos(b, 14.5), blip(midi(G5), 1.5, bend=0.5), 0.30, bus='music')
    if i % 16 == 15:
        roll(s, b, 12, 7, spacing=0.55, gain=0.85, accel=True, seed=b % 3)
s.place(s.pos(148), crash808(28, gain=0.5), bus='fx')
s.place(s.pos(148), impact(24, gain=0.5), bus='fx')
s.place(s.pos(164), crash808(16, gain=0.35), bus='fx')
for i in range(4):
    b = 156 + i * 4
    for st, note, dur in TUNE[i]:
        s.place(s.pos(b, st), lead(midi(note), dur, gain=0.20), bus='music')

# ---- 180-195  outro ----
s.place(s.pos(179, 12), downlifter(14, gain=0.5), bus='fx')
s.place(s.pos(180), voidpad([midi(n) for n in (55, 62, 67)], 16 * 16, cutoff=1100,
                            gain=0.26, seed=73), bus='pad')
s.place(s.pos(180), crackle(16 * 16, gain=0.45), bus='atmos')
for b in range(180, 194):
    i = b - 180
    fade = max(0.0, 1 - i / 13.0)
    drums(b, CELLS_A[i % 4], gain=0.8 * fade, hats=0.8 * fade, ghosts=0.5 * fade,
          ride=0.6 * fade, sidechain=i < 8, seed=b)
    carousel(b, gain=0.24 * max(fade, 0.35), bright=1.0)
    if i % 2 == 0 and i < 8:
        riff(b, gain=0.30 * fade, bright=1.0)
    if i < 8:
        subline(b, [(0, G1, 8), (8, G1, 8)], 0.7 * fade)
        chanks(b, (2, 6, 10, 14), CHANK[i % 4], 0.28 * fade, seed=b)
    if i < 6:
        bassline(b, [(2, funkmid, G2, 1.4, 0.5 * fade, {}),
                     (6.5, funkmid, Bb2, 1.4, 0.5 * fade, {}),
                     (13, talkline, C3, 2.2, 0.4 * fade, dict(vowels=('oo', 'ee')))])
s.place(s.pos(190), whoop(14, f0=900, f1=200, gain=0.4, curve=1.0), bus='fx')

# ---- mix ----
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.4, wet=0.26, tone=5200)
s.bus['pad'] = bus_reverb(s.bus['pad'], decay=3.0, wet=0.32, tone=3200)
s.bus['atmos'] = bus_reverb(s.bus['atmos'], decay=3.6, wet=0.30, tone=2600)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=2.0, wet=0.22, tone=4200)
# The bass keeps its presence at 1 kHz, where a phone can hear it, and is
# shelved out of 2.6 kHz up, which belongs to the kick's click and the
# snare's crack. Two hits a bar are what the ear counts the bar by.
s.bus['bass'] = shelf(peak_eq(hi_spread(s.bus['bass'], hz=420, amount=0.35),
                              1000, 3.5, 0.5), 2600, -4.0, 'high')
s.bus['drums'] = peak_eq(shelf(hp(s.bus['drums'], 42, order=2), 5200, 1.0, 'high'),
                         1900, 2.5, 0.5)
# The lead is designed like the bass, so it generates like the bass: a lot of
# 3 kHz and up. That band belongs to the snare's crack, and a hook that buries
# the backbeat is not a hook - so the lead is shelved out of it and run louder
# in the band where it is actually the tune.
s.bus['music'] = shelf(s.bus['music'], 3500, -4.5, 'high')
s.bus['sub'] = mono_below(s.bus['sub'], 200)
s.bus['atmos'] = hp(s.bus['atmos'], 34, order=2)

GAINS = {'drums': 0.57, 'sub': 0.235, 'bass': 0.64, 'texture': 0.42,
         'music': 1.90, 'pad': 1.15, 'atmos': 0.55, 'fx': 0.24}
s.report(GAINS)
s.render('neuro_karusel_174.wav', drive=1.25, duck=0.34, limit=0.82, peak=0.90,
         gains=GAINS, clip=0.86, fade=2.0)
