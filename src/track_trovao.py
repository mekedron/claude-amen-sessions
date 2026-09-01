"""Trovao - Brazilian phonk at 140 BPM, in G minor.

The brief was energy and an even pulse: no breakbeat, no halftime, and a
cowbell that plays a tune rather than clanging on the one.

So the kick is on every beat for 100 of the 112 bars, and the 3+3+2 a
tamborzao normally puts on the kick is moved onto a mid tom - the Brazilian
syncopation stays audible while the bottom stays square. Everything the ear
follows sits above it: an eight-note cowbell riff with a real velocity
contour, a low cowbell answering in its holes, and a bass written as
note-then-silence so the sub is empty every time the kick lands.

    G minor. The riff never transposes; the bass moves i - i - bVI - bVII
    underneath it, so the same eight notes read as the root, then the third
    of Eb, then the ninth of F. One hook, three harmonic readings.

Two things the arrangement is built around:

    The energy curve is written as a number per bar, not assumed. A track
    with a kick on every beat has no rhythmic contrast to fall back on, so
    the resets and the bridge carry the contrast in level instead - about
    3 dB under the drops. Further than that and a reset stops reading as a
    reset and starts reading as the record dropping out.

    The hook is dead centre and everything around it is not. The cowbell
    and the bass take no width at all (a Haas delay combs a cowbell's clang
    away the moment anything sums to mono); the two shakers, the tic, the
    tom, the octave accents and the shouts are spread, and the loudest
    accent of every fourth bar is thrown into a ping-pong delay.

Sections, in bars:

     0-7    the call, then the pulse arrives
     8-15   the beat assembles
    16-31   drop A
    32-35   reset - bass out, riser
    36-51   drop B, with the low cowbell answering
    52-59   the bridge: the kick never stops, the sub does
    60-83   drop C, the fullest 24 bars
    84-87   reset
    88-107  drop D - the riff an octave up, then home
   108-111  outro
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from brphonklib import *

BARS = 112
ROOTS = [31, 31, 27, 29]                 # G1 G1 Eb1 F1 - i i bVI bVII

# ---- the hook: two bars of cowbell ----
# (bar in the 2-bar cell, step, note, how hard it was struck)
RIFF = [
    (0,  0, 74, 1.15), (0,  2, 74, 0.42), (0,  3, 72, 0.75), (0,  6, 70, 1.05),
    (0,  8, 67, 0.90), (0, 10, 70, 0.52), (0, 11, 72, 0.85), (0, 14, 74, 1.00),
    (1,  0, 74, 1.15), (1,  2, 74, 0.42), (1,  3, 72, 0.75), (1,  6, 70, 1.05),
    (1,  8, 72, 0.90), (1, 11, 74, 0.70), (1, 13, 77, 1.10), (1, 14, 75, 0.58),
    (1, 15, 74, 0.50),
]

# every eighth bar the second bar climbs instead of falling away
RIFF_FILL = [
    (1,  0, 74, 1.15), (1,  2, 74, 0.42), (1,  3, 72, 0.75), (1,  6, 70, 1.05),
    (1,  8, 72, 0.90), (1, 10, 74, 0.60), (1, 11, 75, 0.78), (1, 12, 77, 0.95),
    (1, 13, 79, 1.20), (1, 14, 77, 0.70), (1, 15, 74, 0.60),
]

# and every sixteenth it empties out - the release of the same eight bars
# handled by taking notes away rather than by adding them
RIFF_HOLE = [
    (1,  0, 74, 1.20), (1,  6, 70, 1.05), (1, 13, 77, 1.15), (1, 15, 74, 0.55),
]

# the bridge riff: the same rhythm reading the bVI, with the one note that is
# not in the key - Ab, the Phrygian second - as its last accent
RIFF_B = [
    (0,  0, 75, 1.10), (0,  2, 75, 0.42), (0,  3, 74, 0.75), (0,  6, 72, 1.05),
    (0,  8, 70, 0.90), (0, 10, 72, 0.52), (0, 11, 74, 0.85), (0, 14, 75, 1.00),
    (1,  0, 75, 1.10), (1,  2, 75, 0.42), (1,  3, 74, 0.75), (1,  6, 72, 1.05),
    (1,  8, 74, 0.90), (1, 11, 75, 0.70), (1, 13, 80, 1.15), (1, 14, 77, 0.58),
    (1, 15, 75, 0.50),
]

# the low cowbell answers in the holes the hook leaves
ANSWER = [(0, 4, 58, 0.45), (0, 9, 55, 0.35), (0, 12, 58, 0.45),
          (1, 4, 58, 0.45), (1, 9, 60, 0.35), (1, 12, 58, 0.40)]

TRESILLO = [(0, 0.50, 46), (3, 0.85, 46), (6, 1.00, 50),
            (8, 0.45, 46), (11, 0.80, 46), (14, 0.95, 50)]
CAIXA = [(2, 0.9), (5, 0.6), (7, 0.85), (10, 0.9), (13, 0.6), (15, 0.85)]
SHAKE = [1.0, 0.45, 0.75, 0.45, 0.9, 0.45, 0.72, 0.5,
         1.0, 0.45, 0.75, 0.45, 0.9, 0.5, 0.8, 0.6]
BASSP = [(0, 0, 3.4), (6, 0, 2.4), (10, 0, 1.8), (14, -2, 1.9)]


# ---- the energy curve, one number per bar ----
def lvl(b):
    if b < 4:   return 0.86
    if b < 8:   return 0.94
    if b < 16:  return 0.95
    if b < 32:  return 1.00
    if b < 36:  return 0.90
    if b < 52:  return 1.02
    if b < 56:  return 0.84
    if b < 60:  return 0.88 + 0.04 * (b - 56)        # the bridge climbing back
    if b < 84:  return 1.05
    if b < 88:  return 0.88
    if b < 108: return 1.08
    return 1.0 - 0.10 * (b - 108)


def cell_for(b):
    """the hook, its fill and its hollowed-out version, on an eight-bar cycle"""
    if b % 16 == 15:
        return RIFF[:8] + RIFF_HOLE
    if b % 8 == 7:
        return RIFF[:8] + RIFF_FILL
    return RIFF


def riff_events(cell, bar, octave=0, mute=0.0, gain=1.0, scale=1.0, human=1.0):
    """one bar of a two-bar riff as (step, segment, gain), each note trimmed
    to the gap before the next so nothing rings into its neighbour.

    `human` jitters velocity and placement per bar from a seeded generator.
    A bar of cowbell struck at exactly the written velocity on exactly the
    grid is what says machine, and at 107 ms a step, 3 ms reads as feel
    rather than as sloppiness. Downbeats are never moved."""
    half = [e for e in cell if e[0] == bar % 2]
    order = sorted(cell, key=lambda e: (e[0], e[1]))
    rng = np.random.RandomState(bar * 131 + 7)
    out = []
    for b, st, note, h in half:
        nxt = next((e[1] + 16 * (e[0] - b) for e in order
                    if (e[0], e[1]) > (b, st)), st + 2.0)
        dur = float(np.clip(nxt - st, 0.75, 2.2))
        hv = round(float(np.clip(h * scale + human * rng.uniform(-0.07, 0.07), 0.15, 1.4)), 2)
        off = 0.0 if st % 4 == 0 else human * round(rng.uniform(-0.025, 0.03), 3)
        out.append((st + off, agogo(note + 12 * octave, dur, hit=hv, mute=mute), gain))
    return out


def accents(b, octave=1, gain=0.34, mute=0.25):
    """the loud hits of the bar doubled an octave up, thrown left and right -
    the hook stays centred, its outline does not"""
    out, i = [], 0
    for bb, st, n, h in cell_for(b):
        if bb != b % 2 or h < 1.0:
            continue
        i += 1
        seg = panned(agogo(n + 12 * octave, 1.2, hit=0.95, mute=mute), 0.48 if i % 2 else -0.48)
        out.append((st, seg, gain))
    return out


def drums(s, b, g=1.0, kick=True, tom=1.0, tic=1.0, shake=1.0, kgain=1.0):
    """The kick stays on the grid at full velocity - it is the pulse the brief
    asked for, and jittering it would undo the point. Everything above it is
    jittered and panned."""
    rng = np.random.RandomState(b * 977 + 3)
    ev = []
    if kick:
        for st in (0, 4, 8, 12):
            ev.append((st, bumbo(4.0), g * kgain * (1.0 if st in (0, 8) else 0.95)))
            s.hit(s.pos(b, st))
    if tom:
        for st, v, note in TRESILLO:
            seg = panned(timbau(note, 2.0), 0.34 if note == 46 else 0.21)
            ev.append((st + rng.uniform(-0.02, 0.025), seg,
                       g * 0.60 * v * tom * rng.uniform(0.88, 1.10)))
    if tic:
        for st, v in CAIXA:
            seg = panned(caixa(1.0, bright=round(0.8 + 0.4 * v, 2)), -0.44)
            ev.append((st + rng.uniform(-0.02, 0.03), seg,
                       g * 0.55 * v * tic * rng.uniform(0.86, 1.12)))
    if shake:
        for st in range(16):                          # the driving 16ths, right
            seg = panned(chique(1.0, seed=(b * 5 + st) % 24,
                                decay=round(0.030 + 0.008 * ((b + st) % 3), 4)), 0.42)
            ev.append((st + rng.uniform(-0.015, 0.02), seg,
                       g * 0.48 * SHAKE[st] * shake * rng.uniform(0.88, 1.10)))
        for st in (2, 6, 10, 14):                     # a second, brighter one, left
            seg = panned(chique(1.0, seed=(b * 3 + st) % 24, decay=0.022, tone=1.35), -0.52)
            ev.append((st + rng.uniform(-0.02, 0.02), seg,
                       g * 0.30 * shake * rng.uniform(0.85, 1.12)))
    s.pat(b, ev, bus='drums')


def bassline(s, b, gain=1.0, mid=1.0, sparse=False):
    r = ROOTS[b % 4]
    ev = []
    for st, off, dur in (BASSP[:1] + BASSP[2:3] if sparse else BASSP):
        note = r + off
        sl = (note + 3) if off else None
        sub = 0.35 if r >= 31 else 0.0        # keep the bVI and bVII reaching down
        ev.append((st, grave(note, dur, slide_from=sl, mid=mid, suboct=sub), gain))
    s.pat(b, ev, bus='bass')


def shout(s, b, st, dur=3.0, gain=0.9, **kw):
    s.place(s.pos(b, st), panned(grito(dur, gain, **kw), 0.25 if b % 2 else -0.25), bus='vox')


def throw(s, b):
    """the last accent of the bar sent to a ping-pong delay - the dub move that
    puts air around a hook without widening the hook itself"""
    last = max((e for e in cell_for(b) if e[0] == b % 2), key=lambda e: e[1])
    seg = delay(agogo(last[2], 1.6, hit=0.9, mute=0.35), steps_=3.0, times=3, fb=0.42,
                ping=True, damp=900)
    s.place(s.pos(b, last[1]), seg, 0.30, bus='bellfx')


s = Session(BARS, tail=2.2)

# ---- 0-3  the call ----
s.place(s.pos(0, 0), apito(6.0, 0.9), bus='fx')
for b in range(0, 4):
    drums(s, b, lvl(b), kick=b >= 1, tom=0.0 if b < 2 else 0.7,
          tic=0.0 if b < 2 else 0.7, shake=0.9, kgain=0.9)
    if b >= 2:
        bassline(s, b, gain=lvl(b) * 0.8, mid=0.7, sparse=True)
    s.pat(b, riff_events(RIFF, b, mute=0.55, scale=0.72, gain=lvl(b)), bus='bell')
s.place(s.pos(2, 0), crackle(32, 0.5), bus='fx')
s.place(s.pos(3, 8), riser(8, 0.5, f0=200, f1=900), bus='fx')

# ---- 4-7  the pulse arrives ----
for b in range(4, 8):
    drums(s, b, lvl(b), tom=0.0, tic=0.7, shake=0.9, kgain=0.92)
    s.pat(b, riff_events(RIFF, b, mute=0.25, scale=0.85, gain=lvl(b)), bus='bell')
s.place(s.pos(4, 0), widen(crash808(16, 0.5), 1.2), bus='drums')

# ---- 8-15  the beat assembles ----
for b in range(8, 16):
    drums(s, b, lvl(b))
    bassline(s, b, gain=lvl(b) * 0.95)
    s.pat(b, riff_events(cell_for(b), b, mute=0.15, gain=lvl(b)), bus='bell')
    if b % 4 == 3:
        throw(s, b)
shout(s, 11, 14, 3.0, 0.8)
shout(s, 15, 12, 4.0, 0.95, f0=190, drop=6.0)
s.place(s.pos(15, 12), riser(4, 0.55), bus='fx')

# ---- 16-31  drop A ----
for b in range(16, 32):
    g = lvl(b)
    drums(s, b, g)
    bassline(s, b, gain=g)
    s.pat(b, riff_events(cell_for(b), b, gain=g), bus='bell')
    if b >= 24:
        s.pat(b, accents(b, gain=0.34 * g), bus='bell')
    if b % 4 == 3:
        throw(s, b)
for b in (16, 24):
    s.place(s.pos(b, 0), widen(crash808(16, 0.45), 1.2), bus='drums')
shout(s, 19, 14, 3.0, 0.75)
shout(s, 23, 12, 4.0, 0.9, vowel=('ah', 'aw'))
shout(s, 27, 14, 3.0, 0.75)
shout(s, 31, 8, 5.0, 1.0, f0=200, drop=7.0)

# ---- 32-35  reset: the bass thins out, the pulse does not ----
for b in range(32, 36):
    g = lvl(b)
    drums(s, b, g, tom=0.8, tic=0.9, shake=0.9)
    bassline(s, b, gain=g * 0.72, mid=0.55, sparse=True)
    s.pat(b, riff_events(cell_for(b), b, mute=0.55 - 0.15 * (b - 32),
                         scale=0.8, gain=g), bus='bell')
s.place(s.pos(34, 0), riser(32, 0.75, f0=180, f1=1400), bus='fx')
s.place(s.pos(35, 12), apito(4.0, 0.75), bus='fx')

# ---- 36-51  drop B: the low cowbell answers ----
for b in range(36, 52):
    g = lvl(b)
    drums(s, b, g)
    bassline(s, b, gain=g)
    s.pat(b, riff_events(cell_for(b), b, gain=g), bus='bell')
    s.pat(b, [(st, panned(seg, -0.36), gn * 0.5)
              for st, seg, gn in riff_events(ANSWER, b, mute=0.75, gain=g)], bus='bell')
    if b % 4 == 3:
        throw(s, b)
for b in (36, 44):
    s.place(s.pos(b, 0), widen(crash808(16, 0.45), 1.2), bus='drums')
s.place(s.pos(36, 0), impact(20, 0.6), bus='fx')
shout(s, 39, 14, 3.0, 0.75)
shout(s, 43, 12, 4.0, 0.9, vowel=('ae', 'aw'))
shout(s, 47, 14, 3.0, 0.8)
shout(s, 51, 8, 5.0, 1.0, f0=205, drop=7.0)

# ---- 52-59  the bridge: the kick never stops, the sub does ----
for b in range(52, 60):
    g, late = lvl(b), b >= 56
    drums(s, b, g, tom=0.45 if not late else 1.0, tic=0.7 if not late else 0.9,
          shake=0.8 if not late else 1.0, kgain=0.92 if not late else 1.0)
    s.pat(b, riff_events(RIFF_B, b, mute=0.35 if not late else 0.1,
                         scale=0.82 if not late else 1.0, gain=g), bus='bell')
    bassline(s, b, gain=g * (0.9 if late else 0.62),
             mid=0.85 if late else 0.45, sparse=not late)
for b in range(52, 60, 2):
    r = ROOTS[b % 4]
    s.place(s.pos(b, 0), pad([midi(r + 12), midi(r + 15), midi(r + 22)], 32,
                             cutoff=1500, gain=0.5, wide=1.4), bus='pad')
s.place(s.pos(52, 0), downlifter(12, 0.6), bus='fx')
s.place(s.pos(58, 0), riser(32, 0.9, f0=200, f1=1700), bus='fx')
s.place(s.pos(59, 14), apito(3.0, 0.8), bus='fx')

# ---- 60-83  drop C ----
for b in range(60, 84):
    g = lvl(b)
    drums(s, b, g)
    bassline(s, b, gain=g)
    s.pat(b, riff_events(cell_for(b), b, gain=g), bus='bell')
    s.pat(b, [(st, panned(seg, -0.36), gn * 0.5)
              for st, seg, gn in riff_events(ANSWER, b, mute=0.75, gain=g)], bus='bell')
    s.pat(b, accents(b, gain=0.34 * g), bus='bell')
    if b % 4 == 3:
        throw(s, b)
for b in (60, 68, 76):
    s.place(s.pos(b, 0), widen(crash808(16, 0.45), 1.2), bus='drums')
s.place(s.pos(60, 0), impact(20, 0.65), bus='fx')
for b in (63, 71, 79):
    shout(s, b, 14, 3.0, 0.8)
for b in (67, 75):
    shout(s, b, 12, 4.0, 0.95, vowel=('ah', 'aw'))
shout(s, 83, 8, 5.0, 1.0, f0=210, drop=8.0)

# ---- 84-87  reset ----
for b in range(84, 88):
    g = lvl(b)
    drums(s, b, g, tom=0.9, tic=0.9, shake=0.9)
    bassline(s, b, gain=g * 0.75, mid=0.55, sparse=True)
    s.pat(b, riff_events(cell_for(b), b, mute=0.5 - 0.16 * (b - 84),
                         scale=0.85, gain=g), bus='bell')
s.place(s.pos(86, 0), riser(32, 0.85, f0=190, f1=1900), bus='fx')

# ---- 88-107  drop D: the riff an octave up, then home ----
for b in range(88, 108):
    g, up = lvl(b), 1 if b < 96 else 0
    drums(s, b, g)
    bassline(s, b, gain=g)
    s.pat(b, riff_events(cell_for(b), b, octave=up, gain=g * (0.85 if up else 1.0)), bus='bell')
    s.pat(b, [(st, panned(seg, -0.36), gn * 0.55)
              for st, seg, gn in riff_events(ANSWER, b, mute=0.75, gain=g)], bus='bell')
    if up:                                    # the octave up plus its own root below it
        s.pat(b, riff_events(cell_for(b), b, mute=0.45, gain=g * 0.5), bus='bell')
    else:
        s.pat(b, accents(b, gain=0.36 * g, mute=0.2), bus='bell')
    if b % 4 == 3:
        throw(s, b)
for b in (88, 96, 104):
    s.place(s.pos(b, 0), widen(crash808(16, 0.45), 1.2), bus='drums')
s.place(s.pos(88, 0), impact(20, 0.65), bus='fx')
s.place(s.pos(96, 0), impact(16, 0.55), bus='fx')
for b in (91, 99, 103):
    shout(s, b, 14, 3.0, 0.8)
shout(s, 95, 12, 4.0, 1.0, f0=215, drop=7.0)
shout(s, 107, 8, 5.0, 1.0, f0=195, drop=6.0)

# ---- 108-111  outro ----
for b in range(108, 112):
    g = lvl(b)
    drums(s, b, g, kick=(b < 110), tom=0.6 if b < 110 else 0.0,
          tic=0.5 if b < 110 else 0.0, shake=1.0)
    s.pat(b, riff_events(cell_for(b), b, mute=0.3 + 0.2 * (b - 108),
                         scale=0.9 - 0.15 * (b - 108), gain=g), bus='bell')
    bassline(s, b, gain=g * 0.9, sparse=b >= 110)
s.place(s.pos(110, 0), apito(6.0, 0.7), bus='fx')

# ---- mix ----
# Nothing below 110 Hz keeps an image: a rig that sums the bass, or a single
# earbud, would throw that energy away and the low end would quietly go.
for nm in ('drums', 'bass'):
    s.bus[nm] = mono_below(s.bus[nm], 110)
s.bus['bell'] = side_boost(s.bus['bell'], 700, 1.1)

# Each bus is saturated where it belongs, so the master clipper only meets a
# coincidence between buses rather than the peak of any one of them. A wide
# tanh across the sum would lift every tail toward the peaks and flatten a
# grid that was written with gaps in it on purpose.
for nm, ceil in (('drums', 0.62), ('bass', 0.64), ('bell', 0.50),
                 ('bellfx', 0.30), ('vox', 0.44), ('pad', 0.30), ('fx', 0.34)):
    if nm in s.bus:
        s.bus[nm] = softclip(s.bus[nm], ceil, knee=0.7)
for nm in ('bell', 'drums'):
    s.bus[nm] = lp(s.bus[nm], 13500)

GAINS = {'drums': 1.56, 'bass': 1.36, 'bell': 0.99, 'bellfx': 0.76,
         'vox': 0.86, 'pad': 0.58, 'fx': 0.54}
s.report(GAINS)
s.render('brphonk_trovao_140.wav', drive=0, duck=0.30, duck_rel=0.13,
         clip=1.62, limit=0.78, peak=0.855, gains=GAINS, fade=1.2)
