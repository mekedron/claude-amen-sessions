"""TVAR - neurofunk, F Phrygian, 174 BPM. Something is in the water and it is
faster than you are.

A horror-game chase written to `theory/20-genres/04a-neurofunk.md`. The brief
was Lovecraft: not a monster you fight, a scale of thing that makes fighting
an irrelevant idea. Three decisions follow from that and everything else is
detail.

**There is no melody.** The genre file says the melodic content is the bass's
timbre, and a horror record proves it: a tune is a human artefact and putting
one in says a person is present. What carries the narrative instead is
`sonar()` - a ping from something far below - and `breath()`, filtered noise
on a slow swell with no pitch and no formant in it. The only harmony on the
record is sixteen bars of `chasm()` in the breakdown, voiced with no third
anywhere: a bare fifth at the bottom and the Phrygian b2 two octaves above the
root, which is dread rather than a chord.

**The bass is one creature, not a bass part.** Every two-bar cell is a single
oscillator running a lane of ten half-bar gestures from `abysslib.GESTURES`.
The pitch barely moves; the rate of the wavetable scan moves every sixteenth.
`lurk` holds the timbre still and `shred` runs it at thirty-seconds, and the
cell that goes `lurk draw chew shred` is one note accelerating from stillness
to texture without ever restarting. `reel` is the pair that does it in both
directions - `stretch wind stretch shred`, the vibration drawn out until it
nearly stops and then wound back up, measured at 234 -> 83 -> 366 Hz.

**The pitch arc is saved for the end of each drop.** Ten bars of F, then a
climb through the b3 and the b6 and a fall of a semitone onto a note that does
not resolve - the b2 at the end of drop one, the tritone at the end of drop
three. The fourth and the fifth barely appear: they are the two degrees of
this scale that are neither major nor minor, and this record has no use for
either.

**The arrangement is a chase, so it has to actually accelerate.** Bar 80 is
the floor of the record at -11.5 dB against the drops, and the ARC ride below
is a master fader move written in decibels per bar - because per-part gains do
not sum to a section and a limiter closes whatever gap survives them.

    intro       0-15   the drone, a ping, something breathing
    beat in    16-31   the kit at half power, the sub alone
    build 1    32-47   the creature heard once per four bars, then a sub-drop
    DROP 1     48-79   growl table; statement, answer, escalation, switch-up
    breakdown  80-95   drums gone, the drone climbs to the b2, it sees you
    build 2    96-111
    DROP 2    112-143  the metal table forward: it stops growling and tears
    halftime  144-159  snare on 3 only; the chase stops because it caught you
    DROP 3    160-191  both patches trading every two bars
    outro     192-207  subtract; the drone is still there
"""
import numpy as np
from core import *
import core, abysslib as A
from abysslib import (maw, phrase, resink, crush, bone, thump, ghost, tick, sonar,
                      leviathan, chasm, hull, breath, swarm, scream, descent,
                      maw_rev, deg, ROOT)

set_grid(bpm=174)
BARS = 208
s = Session(BARS, tail=3.0)
# The sub and the bed get ducked too. A kick that only moves the character
# layer out of the way leaves the two loudest things in the record fighting
# over 40-90 Hz.
s.DUCKED = {'bass': 1.0, 'sub': 0.70, 'body': 0.80, 'pad': 0.90, 'atmos': 0.30}
rs = np.random.RandomState(1917)


# ---------------------------------------------------------------- the kit --
# Four bar-shapes on a two-step skeleton: kick on 1, snare on 2, the second
# kick pushed late to step 10 - the eighth before the second snare - and the
# second snare on 4. That displacement is the stepping quality of the genre,
# and every variation below keeps it and edits around it.
SNARE_HITS = []
KICKS = ([0, 10], [0, 6, 10], [0, 10, 14], [0, 3, 10])
SNARES = ([4, 12], [4, 12], [4, 12], [4, 11.5, 12])
GHOSTS = ([2.5, 6.5, 9, 14.5], [3, 7.5, 13, 15], [2, 6, 9.5, 14],
          [2.5, 5.5, 9, 13.5, 15.5])


def kit(b, v=0, gain=1.0, hats=1.0, ghosts=1.0, opens=(6,), tick_pat=None):
    """One bar of drums. Velocity is shaped and the timing is jittered on
    everything except the kick: the pulse is the one thing a listener counts,
    and a kick moved three milliseconds is a mix that drifts."""
    for st in KICKS[v]:
        t = s.pos(b, st)
        s.place(t, crush(3.0), gain * (1.0 if st == 0 else 0.86), 'drums')
        s.hit(t)
    for i, st in enumerate(SNARES[v]):
        j = int(rs.normal(0, 0.0016) * SR)
        s.place(s.pos(b, st) + j, bone(3.0), gain * (1.0 if i < 2 else 0.55), 'drums')
        if i < 2:
            # the bottom of the backbeat, as a layer rather than as EQ
            s.place(s.pos(b, st) + j, thump(2.0), gain * 0.95, 'drums')
            if gain > 0.5:
                SNARE_HITS.append(s.pos(b, st) + j)
    for st in GHOSTS[v]:
        j = int(rs.normal(0, 0.0035) * SR)
        s.place(s.pos(b, st) + j, ghost(1.0), gain * ghosts * rs.uniform(0.55, 1.0), 'drums')
    if hats:
        pat = tick_pat if tick_pat is not None else range(16)
        for st in pat:
            if st in opens:
                s.place(s.pos(b, st), tick(open_=True), gain * hats * 0.55, 'drums')
                continue
            # alternating levels, downbeat emphasis, and a little chance
            lv = (1.0 if st % 4 == 0 else 0.62 if st % 2 == 0 else 0.42)
            s.place(s.pos(b, st) + int(rs.normal(0, 0.0012) * SR),
                    tick(), gain * hats * lv * rs.uniform(0.85, 1.12), 'drums')


# ------------------------------------------------------------- the creature --
# Cells are named by what the thing is doing. Each is four half-bar gestures
# handed to one oscillator, and the table underneath is which mouth it uses.
CELLS = {
    'wake':   (['lurk', 'lurk', 'draw', 'draw'], 'growl', dict(bite=0.85)),
    'stalk':  (['lurk', 'draw', 'chew', 'shred'], 'growl', dict(bite=0.80)),
    'answer': (['snap', 'snap', 'chew', 'gnash'], 'growl', dict(bite=0.70, drive=2.7)),
    'climb':  (['chew', 'shred', 'gnash', 'howl'], 'growl', dict(bite=0.42, drive=2.6)),
    'scream': (['howl', 'howl', 'gnash', 'sink'], 'vowel', dict(bite=0.50, vwet=0.62, drive=2.4)),
    'hunt':   (['gnash', 'shred', 'gnash', 'shred'], 'metal', dict(bite=0.34, drive=2.9, fold_g=1.42)),
    'bite':   (['snap', 'snap', 'snap', 'gnash'], 'metal', dict(bite=0.34, drive=3.0)),
    'hand':   (['shred', 'shred', 'gnash', 'sink'], 'growl', dict(bite=0.75)),
    'tear':   (['gnash', 'gnash', 'shred', 'howl'], 'rip', dict(bite=0.30, drive=3.1, fold_g=1.5,
                                                                crush=7)),
    'talk':   (['chew', 'howl', 'chew', 'gnash'], 'vowel', dict(bite=0.55, vwet=0.70,
                                                                vowels=('oo', 'ee'))),
    'wide':   (['draw', 'chew', 'chew', 'shred'], 'reeseb', dict(bite=0.72, detune=32.0, drive=2.2)),
    'crush':  (['lurk', 'lurk', 'sink', 'sink'], 'witch', dict(bite=0.90, drive=2.5, fold_g=1.2)),
    # The reel: the vibration stretched out until it nearly stops, then wound
    # back up to thirty-seconds - and the pitch arc lifts on the cell after
    # it, so the phrase reads long, short, higher. One note the whole way.
    'reel':   (['stretch', 'wind', 'stretch', 'shred'], 'witch', dict(bite=0.80, drive=2.5)),
    'reel2':  (['stretch', 'wind', 'gnash', 'wind'], 'reeseb', dict(bite=0.75, detune=38.0)),
}
_CACHE = {}


def cell(name, note, seed=0, res=0.62, **kw):
    """One two-bar cell of bass, resampled. The resampling is not a polish
    pass - it is where the harmonic relationships nobody programmed come
    from - so it is applied to every cell and cached by identity."""
    key = (name, note, seed, res, tuple(sorted(kw.items())))
    if key in _CACHE:
        return _CACHE[key]
    cells, table, base = CELLS[name]
    o = dict(base); o.update(kw)
    x = phrase(cells, [(0, note)], table=table, seed=seed, **o)
    _CACHE[key] = resink(x, mix=res, seed=seed) if res else x
    return _CACHE[key]


def lay(b, name, note, gain=1.0, seed=0, **kw):
    s.place(s.pos(b), cell(name, note, seed, **kw), gain, 'bass')


# ------------------------------------------------------------------- the sub --
# ONE oscillator for the whole record. Rendering a sub section by section
# means every seam is two segments at unrelated phases meeting, and at 44 Hz
# that cancellation is not subtle - it is a hole in the low end exactly where
# a section change was supposed to land hardest.
SUB_NOTES = [(0, 29)]
SUB_GATE = np.zeros(BARS * 16)


def subseg(b0, b1, note=29, level=1.0):
    SUB_NOTES.append((b0 * 16, note))
    SUB_GATE[b0 * 16:b1 * 16] = level


# ============================================================== ARRANGEMENT ==

# ---- 0-15  intro: the drone, a ping, something breathing ----
s.place(s.pos(0), leviathan(16 * 16 + 8, 41, 0.85, cutoff=620, seed=1), 1.0, 'body')
s.place(s.pos(0), breath(16 * 16, seed=2, cycles=2.0), 0.90, 'atmos')
s.place(s.pos(2), hull(14 * 16, seed=3, lo=1400, hi=6200, density=0.7), 0.55, 'atmos')
for b, f0, g in ((1, 428, 0.55), (5, 428, 0.62), (9, 321, 0.70), (13, 428, 0.80)):
    s.place(s.pos(b, 2), reverb(sonar(10.0, f0), decay=4.2, wet=0.75, tone=2600), g, 'atmos')
s.place(s.pos(8), chasm([41, 48, 61, 66], 8 * 16, 0.55, (260, 900), seed=4), 1.0, 'pad')
# the creature backwards, before anything has heard it forwards
s.place(s.pos(12), maw_rev(cell('stalk', 41, seed=9), 0.55), 1.0, 'fx')
s.place(s.pos(14), whoosh(32, 0.55), 1.0, 'fx')
for b in range(8, 16):
    kit(b, v=b % 4, gain=0.0)   # no drums yet; the hits still register nothing
subseg(0, 16, 29, 0.0)

# ---- 16-31  beat in: the kit at half power, the sub alone ----
s.place(s.pos(16), leviathan(16 * 16 + 8, 41, 0.75, cutoff=780, seed=5), 1.0, 'body')
s.place(s.pos(16), hull(16 * 16, seed=6, lo=1600, hi=7000, density=0.8), 0.50, 'atmos')
for b in range(16, 32):
    v = (b - 16) % 4
    kit(b, v, gain=0.70, hats=0.55, ghosts=0.6,
        opens=(6,) if v in (0, 2) else (14,),
        tick_pat=range(0, 16, 2) if b < 24 else range(16))
subseg(16, 32, 29, 0.72)
s.place(s.pos(20, 2), reverb(sonar(10.0, 428), decay=4.0, wet=0.6, tone=2600), 0.55, 'atmos')
s.place(s.pos(28, 2), reverb(sonar(10.0, 321), decay=4.0, wet=0.6, tone=2600), 0.60, 'atmos')

# ---- 32-47  build 1: the creature heard once per four bars ----
s.place(s.pos(32), leviathan(16 * 16 + 8, 41, 0.90, cutoff=1000, seed=7), 1.0, 'body')
s.place(s.pos(32), hull(16 * 16, seed=8, lo=1800, hi=8000), 0.62, 'atmos')
s.place(s.pos(32), breath(16 * 16, seed=9, cycles=3.0), 0.60, 'atmos')
for b in range(32, 48):
    v = (b - 32) % 4
    kit(b, v, gain=0.90, hats=0.85, ghosts=0.9, opens=(6, 14) if b >= 40 else (6,))
subseg(32, 48, 29, 0.80)
lay(34, 'wake', 29, 0.75, seed=11)
lay(38, 'wake', 29, 0.85, seed=11)
lay(42, 'stalk', 29, 0.90, seed=12)
lay(46, 'stalk', 30, 0.95, seed=13)          # Gb - the b2, once, as a warning
s.place(s.pos(40), scream(8 * 16, 0.42, seed=1, f0=140, f1=1800), 1.0, 'fx')
s.place(s.pos(44), scream(4 * 16, 0.60, seed=2, f0=260, f1=3400), 1.0, 'fx')
# the last half bar: everything stops and the sub falls out from under it
s.place(s.pos(47, 8), descent(8, 1.0), 1.0, 'fx')
SUB_GATE[47 * 16 + 8:48 * 16] = 0.0

# ---- 48-79  DROP 1: growl table ----
s.place(s.pos(48), impact(24, 0.85), 1.0, 'fx')
s.place(s.pos(48), hull(32 * 16, seed=14, lo=2000, hi=9000, density=0.6), 0.40, 'atmos')
D1 = [('stalk', 29), ('answer', 29), ('stalk', 29), ('climb', 29),
      ('stalk', 30), ('answer', 29), ('scream', 32), ('climb', 29),
      ('hunt', 30), ('reel', 29), ('hunt', 29), ('bite', 32),
      ('hunt', 37), ('climb', 36), ('scream', 30), ('hand', 29)]
for i, (name, nt) in enumerate(D1):
    b = 48 + i * 2
    lay(b, name, nt, 1.0, seed=20 + i % 5)
for b in range(48, 80):
    v = (b - 48) % 4
    kit(b, v, gain=1.0, hats=1.0, ghosts=1.0,
        opens=(6, 14) if v % 2 == 0 else (10,))
s.place(s.pos(63, 12), descent(4, 0.55), 1.0, 'fx')     # the 16-bar switch-up
s.place(s.pos(64), impact(16, 0.55), 1.0, 'fx')
s.place(s.pos(78), scream(2 * 16, 0.30, seed=3, f0=400, f1=2600), 1.0, 'fx')

# ---- 80-95  breakdown: it sees you ----
# The floor of the record. The drone climbs a semitone to the b2 and stays
# there for eight bars, which is the only harmonic event on the whole track.
s.place(s.pos(80), leviathan(8 * 16 + 8, 41, 1.0, cutoff=540, seed=15), 1.0, 'body')
s.place(s.pos(88), leviathan(8 * 16 + 8, 42, 1.0, cutoff=700, seed=16), 1.0, 'body')
s.place(s.pos(80), chasm([41, 48, 61, 66], 8 * 16, 0.80, (240, 1100), seed=17), 1.0, 'pad')
s.place(s.pos(88), chasm([42, 49, 61, 66], 8 * 16, 0.90, (300, 1900), seed=18), 1.0, 'pad')
s.place(s.pos(80), breath(16 * 16, seed=19, cycles=2.5), 1.0, 'atmos')
s.place(s.pos(80), hull(16 * 16, seed=20, lo=1300, hi=7500, density=1.0), 0.75, 'atmos')
s.place(s.pos(84), swarm(12 * 16, 0.85, seed=21), 1.0, 'atmos')
for b, f0 in ((81, 428), (85, 321), (89, 285), (93, 428)):
    s.place(s.pos(b, 2), reverb(sonar(12.0, f0), decay=5.0, wet=0.85, tone=2400),
            0.85, 'atmos')
# halftime hits: the pulse is still there, four times slower
for b in range(82, 96, 2):
    s.place(s.pos(b), crush(3.0), 0.55, 'drums'); s.hit(s.pos(b))
    s.place(s.pos(b, 8), reverb(bone(3.0), 1.4, 0.35, 3000), 0.42, 'drums')
    s.place(s.pos(b, 8), thump(2.4), 0.60, 'drums')
lay(94, 'crush', 29, 0.55, seed=22)
subseg(94, 96, 29, 0.30)

# ---- 96-111  build 2 ----
s.place(s.pos(96), leviathan(16 * 16 + 8, 41, 0.95, cutoff=1100, seed=23), 1.0, 'body')
s.place(s.pos(96), hull(16 * 16, seed=24, lo=1800, hi=8600), 0.70, 'atmos')
for b in range(96, 112):
    v = (b - 96) % 4
    kit(b, v, gain=0.62 + 0.30 * (b - 96) / 15, hats=0.7 + 0.3 * (b - 96) / 15,
        ghosts=0.8, opens=(6, 14))
subseg(96, 112, 29, 0.85)
lay(100, 'stalk', 29, 0.80, seed=25)
lay(104, 'climb', 29, 0.90, seed=26)
lay(108, 'reel', 29, 0.95, seed=27)
s.place(s.pos(104), scream(8 * 16, 0.55, seed=4, f0=150, f1=2600), 1.0, 'fx')
s.place(s.pos(110), scream(2 * 16, 0.75, seed=5, f0=500, f1=5200), 1.0, 'fx')
s.place(s.pos(111, 8), descent(8, 1.1), 1.0, 'fx')
SUB_GATE[111 * 16 + 8:112 * 16] = 0.0
# one bar of the creature backwards, so the drop is something arriving
s.place(s.pos(110), maw_rev(cell('hunt', 41, seed=28), 0.42), 1.0, 'fx')

# ---- 112-143  DROP 2: the metal table forward ----
s.place(s.pos(112), impact(24, 1.0), 1.0, 'fx')
s.place(s.pos(112), hull(32 * 16, seed=29, lo=2200, hi=9500, density=0.6), 0.42, 'atmos')
D2 = [('hunt', 29), ('bite', 29), ('hunt', 29), ('tear', 29),
      ('talk', 32), ('bite', 29), ('tear', 30), ('climb', 29),
      ('hunt', 32), ('reel2', 29), ('wide', 32), ('bite', 36),
      ('talk', 37), ('tear', 36), ('hunt', 30), ('hand', 29)]
for i, (name, nt) in enumerate(D2):
    b = 112 + i * 2
    lay(b, name, nt, 1.0, seed=40 + i % 6)
for b in range(112, 144):
    v = (b - 112) % 4
    kit(b, v, gain=1.0, hats=1.0, ghosts=1.05,
        opens=(6, 14) if v % 2 else (10, 14))
s.place(s.pos(127, 12), descent(4, 0.6), 1.0, 'fx')
s.place(s.pos(128), impact(16, 0.6), 1.0, 'fx')
s.place(s.pos(142), scream(2 * 16, 0.35, seed=6, f0=380, f1=2800), 1.0, 'fx')

# ---- 144-159  halftime: it caught you ----
# Same tempo, snare on beat 3 only. The chase does not slow down; the felt
# pulse halves and the weight doubles, which is what being caught sounds like.
s.place(s.pos(144), leviathan(16 * 16 + 8, 41, 1.1, cutoff=620, seed=30), 1.0, 'body')
s.place(s.pos(144), hull(16 * 16, seed=31, lo=1500, hi=7200, density=0.9), 0.65, 'atmos')
for b in range(144, 160):
    s.place(s.pos(b), crush(3.0), 0.95, 'drums'); s.hit(s.pos(b))
    s.place(s.pos(b, 10), crush(3.0), 0.72, 'drums'); s.hit(s.pos(b, 10))
    s.place(s.pos(b, 8), bone(3.0), 1.0, 'drums')
    s.place(s.pos(b, 8), thump(2.4), 1.10, 'drums')
    if b % 2:
        s.place(s.pos(b, 14), ghost(1.0), 0.7, 'drums')
        s.place(s.pos(b, 15), ghost(1.0), 0.5, 'drums')
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), tick(open_=(st == 6)), 0.5, 'drums')
for i, (name, nt) in enumerate([('crush', 29), ('scream', 30), ('crush', 29),
                                ('talk', 32), ('crush', 37), ('scream', 36),
                                ('wide', 30), ('tear', 29)]):
    lay(144 + i * 2, name, nt, 0.95, seed=50 + i)
s.place(s.pos(156), scream(4 * 16, 0.70, seed=7, f0=200, f1=4200), 1.0, 'fx')
s.place(s.pos(159, 8), descent(8, 1.15), 1.0, 'fx')
SUB_GATE[159 * 16 + 8:160 * 16] = 0.0

# ---- 160-191  DROP 3: both patches trading ----
s.place(s.pos(160), impact(24, 1.1), 1.0, 'fx')
s.place(s.pos(160), hull(32 * 16, seed=32, lo=2400, hi=10000, density=0.6), 0.40, 'atmos')
D3 = [('hunt', 29), ('scream', 29), ('tear', 29), ('answer', 29),
      ('hunt', 29), ('bite', 30), ('climb', 32), ('tear', 29),
      ('reel', 29), ('bite', 32), ('talk', 37), ('tear', 36),
      ('hunt', 37), ('tear', 36), ('hunt', 35), ('hand', 29)]
for i, (name, nt) in enumerate(D3):
    b = 160 + i * 2
    lay(b, name, nt, 1.0, seed=60 + i % 7)
for b in range(160, 192):
    v = (b - 160) % 4
    kit(b, v, gain=1.0, hats=1.05, ghosts=1.1,
        opens=(6, 14) if v % 2 else (10, 14))
s.place(s.pos(175, 12), descent(4, 0.6), 1.0, 'fx')
s.place(s.pos(176), impact(16, 0.65), 1.0, 'fx')
s.place(s.pos(190), scream(2 * 16, 0.40, seed=8, f0=420, f1=3000), 1.0, 'fx')

# ---- 192-207  outro: subtract; the drone is still there ----
s.place(s.pos(192), leviathan(16 * 16 + 24, 41, 1.0, cutoff=760, seed=33), 1.0, 'body')
s.place(s.pos(192), chasm([41, 48, 61, 66], 14 * 16, 0.60, (240, 800), seed=34), 1.0, 'pad')
s.place(s.pos(192), breath(16 * 16, seed=35, cycles=1.5), 0.85, 'atmos')
s.place(s.pos(192), hull(14 * 16, seed=36, lo=1300, hi=6000, density=0.7), 0.55, 'atmos')
for b in range(192, 200):
    v = (b - 192) % 4
    kit(b, v, gain=0.85 - 0.09 * (b - 192), hats=0.7 - 0.08 * (b - 192),
        ghosts=0.6, opens=(6,))
lay(192, 'hand', 29, 0.80, seed=70)
lay(196, 'crush', 29, 0.55, seed=71)
subseg(192, 200, 29, 0.70)
subseg(200, 203, 29, 0.35)
for b, f0 in ((197, 428), (201, 321), (205, 428)):
    s.place(s.pos(b, 2), reverb(sonar(14.0, f0), decay=6.0, wet=0.9, tone=2200),
            0.80, 'atmos')
s.place(s.pos(199), downlifter(32, 0.55), 1.0, 'fx')

# ---------------------------------------------------------------- the sub --
# One call, one oscillator, 208 bars. The gate lane carries the arrangement.
s.place(0, subbar(tuple(SUB_NOTES), dur_steps=BARS * 16 + 8, glide=0.045,
                  h2=0.42, h3=0.10, drive=1.25,
                  gatep=tuple(np.round(SUB_GATE, 3))), 1.0, 'sub')

# ================================================================== the mix ==
# Bus surgery first, then one gain ride over all of it, then the master.

# The bass keeps its own fundamental: an F2 at 87 Hz highpassed at 105 has
# lost its first two harmonics and what is left is a mid-range instrument
# sitting on top of a separate sub, which is not the same as a deep bass.
s.bus['bass'] = hp(s.bus['bass'], 27, 2)
s.bus['bass'] = shelf(s.bus['bass'], 150, 1.5, 'low')
s.bus['bass'] = peak_eq(s.bus['bass'], 1450, 2.0, 0.7)      # where the scan lives
s.bus['bass'] = peak_eq(s.bus['bass'], 2500, -2.0, 0.8)     # the snare's crack
s.bus['bass'] = peak_eq(s.bus['bass'], 520, -1.8, 0.9)
# The creature is a SUSTAINED source, and a sustained source that owns the top
# of a record is a noise bed - which at 6-9 kHz is the thing that hurts after
# ninety seconds. Shelved out of the band the snare has to win.
s.bus['bass'] = shelf(s.bus['bass'], 5400, -2.0, 'high')
s.bus['bass'] = mono_below(s.bus['bass'], 170)

s.bus['sub'] = mono_below(lp(s.bus['sub'], 130, 4), 200)
s.bus['body'] = mono_below(hp(s.bus['body'], 100, 2), 170)

s.bus['drums'] = hp(s.bus['drums'], 32, 2)
s.bus['drums'] = peak_eq(s.bus['drums'], 2400, 2.5, 0.7)    # the crack
s.bus['drums'] = peak_eq(s.bus['drums'], 4200, 2.2, 0.6)    # the snap
s.bus['drums'] = peak_eq(s.bus['drums'], 8200, -2.0, 0.7)   # where bright turns to pain
s.bus['drums'] = shelf(s.bus['drums'], 11000, -5.0, 'high')
# Parallel compression first, to lift the ghost notes into audibility, then
# glue. A 25 dB crest factor on a drum bus is a kit that was recorded; these
# drums were built, and in this genre they are as loud as the bass.
s.bus['drums'] = parallel_comp(s.bus['drums'], blend=0.45, thresh=0.05,
                               ratio=10.0, attack=0.0005, release=0.070)
s.bus['drums'] = compress(s.bus['drums'], thresh=0.15, ratio=4.0, attack=0.009,
                          release=0.085, report=True, label='drum bus')
s.bus['drums'] = side_boost(s.bus['drums'], 3400, 0.7)
s.bus['drums'] = mono_below(s.bus['drums'], 150)

s.bus['atmos'] = shelf(side_boost(hp(s.bus['atmos'], 210, 2), 1400, 0.6), 8000, -5.0, 'high')
s.bus['atmos'] = compress(s.bus['atmos'], thresh=0.06, ratio=3.5, attack=0.008,
                          release=0.12, makeup=2.4)
s.bus['pad'] = hp(s.bus['pad'], 220, 2)
s.bus['fx'] = hp(s.bus['fx'], 28, 2)

# The backbeat has to have a bottom, and the sub sustaining flat across the
# bar takes it away: the low-band grid reads steps 4 and 12 - the two loudest
# things the ear counts - as no louder than the sixteenths between them. The
# kick duck alone cannot fix that because the kick is not on 4 or 12, so the
# low end is ducked against the SNARE as well, shallower and faster.
_sd = duck_env(s.total, SNARE_HITS, depth=0.84, hold=0.006, release=0.055)
s.bus['sub'] = (s.bus['sub'] * _sd[:, None]).astype(np.float32)
s.bus['bass'] = (s.bus['bass'] * (0.55 + 0.45 * _sd)[:, None]).astype(np.float32)
s.bus['body'] = (s.bus['body'] * (0.70 + 0.30 * _sd)[:, None]).astype(np.float32)

# ---- the ride ----
# Per-part gains do not sum to a section: a section is three hundred place()
# calls across seven buses, and turning each of them down by the amount that
# feels right leaves the total where it was. This is a master fader move
# written in decibels per bar, and it is as much a part of the arrangement as
# the notes. Note the dip half a bar before every drop - a climb into a drop
# spends the contrast the drop was going to use.
ARC = [(0, -10.5), (6, -8.0), (14, -6.6), (16, -6.4), (24, -5.8),
       (32, -5.6), (42, -3.8), (46, -3.4), (47.4, -7.2),
       (48, -1.6), (56, -1.3), (64, -1.1), (76, -1.3), (79, -2.2),
       (80, -11.4), (86, -10.0), (88, -8.6), (94, -7.0),
       (96, -6.4), (106, -3.8), (110, -2.8), (111.4, -6.8),
       (112, -0.8), (124, -0.6), (128, -0.5), (140, -0.7), (143, -1.4),
       (144, -5.4), (150, -4.6), (156, -3.6), (159.4, -7.6),
       (160, 0.0), (172, 0.2), (176, 0.2), (188, 0.2), (191, -0.4),
       (192, -5.6), (198, -7.4), (203, -11.0), (207, -17.0), (BARS, -25.0)]
n = s.total
tt = np.arange(n) / BAR
ride = 10 ** (np.interp(tt, [b for b, _ in ARC], [d for _, d in ARC]) / 20)
ride = uniform_filter1d(ride, int(0.030 * SR))      # no zipper on the fader
for b in s.bus:
    s.bus[b] = (s.bus[b] * ride[:, None]).astype(np.float32)

GAINS = {'drums': 2.10, 'sub': 0.42, 'bass': 0.60, 'body': 1.10,
         'atmos': 1.30, 'pad': 3.20, 'fx': 0.42}
s.report(GAINS)
s.ownership(3000, 16000, GAINS, label='3-16k')

# The clipper takes the spikes off before the limiter sees them; if it does
# not, the limiter ducks a whole bar to catch one sample and the master gets
# quieter the harder it is pushed. Then 2.5:1 glue, then a look-ahead limiter
# detecting on a 4x upsample, so this lands at -1 dBTP rather than the +3 the
# reference records carry.
s.render('neuro_tvar_174.wav', drive=0.0, duck=0.30, duck_rel=0.085,
         limit=0.0, peak=0.99, gains=GAINS, clip=1.55, fade=2.6,
         comp=dict(thresh=0.40, ratio=2.5, attack=0.006, release=0.10, makeup=1.2),
         brick=dict(gain=1.16, ceiling=0.89, release=0.075))
