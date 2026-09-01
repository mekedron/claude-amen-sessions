"""RAZLOM - machine funk, F minor, 174 BPM.

Noisia's end of drum & bass, written against measurement rather than against
memory. Two Magnetude records were analysed first, and they say three things
that the repo's earlier neurofunk did not do:

- **52-55% of the energy lives under 120 Hz**, split almost evenly between
  20-60 and 60-120. The low end is not a sub plus a kick, it is a sub WITH
  AN OCTAVE - `subbar` carries a deliberate second harmonic, so an F1 root at
  43.7 Hz puts weight at 87 Hz too, and the kick is tuned to 57 so its own
  fundamental lands in the same band.
- **The low band never gaps.** Their per-16th peak grid runs 0.6-1.0 across
  the whole bar; the old tracks here fall to 0.30. So the sub is one
  continuous oscillator across eight bars - not one call per note - and the
  sidechain release is 90 ms, short enough to have recovered before the next
  sixteenth.
- **Crest 7.2-7.6 dB at -10 LUFS.** That is not a limiter setting, it is
  density: the low band's own crest is 11 dB, which only happens if the sub
  is playing all the time.

The rest is the point of the exercise - every voice on this record is new.
The kit is modal (a snare's five membrane modes, wires that start 2.2 ms late
because the head drags them in), the bass is one oscillator per two-bar riff
with a sixteen-character timbre tablature driving a real resonant filter, and
the atmosphere is granulated from the record's own drums.

    intro       0-15    room, grains, the bell motif, drums arriving filtered
    approach   16-31    the kit, the sub, the riff implied and dark
    build 1    32-39    the drop's own bar, reversed
    DROP 1     40-71    riff A: sixteen timbres, one note
    breakdown  72-87    Fm - Db - Gb - Eb, and the tune said out loud
    build 2    88-95
    DROP 2     96-127   riff B: the bass talks - moving formants, per step
    machines  128-143   no bass line at all; clanks, grains, a dub delay
    build 3   144-151
    DROP 3    152-183   riff C, the lead over it, screeches answering
    outro     184-191

The felt pulse is 174, not 87: the kick is on beats 1 and 3 and the snare on
2 and 4 in every cell, so there is an event on every beat. The two-step
displacement onto the "and" of 3 happens as a variation, over the top of a
kick that is still there, rather than instead of it.
"""
import numpy as np
from machinelib import *

s = Session(192, tail=3.0)
rs = np.random.RandomState(1741)

# ---- F minor, with the Phrygian bII kept for the chords ----
Db1, Eb1, F1, Gb1, Ab1, Bb1 = 25, 27, 29, 30, 32, 34
C2, Db2, Eb2 = 36, 37, 39
F2, Ab2, Bb2, C3, Db3, Eb3, Gb2 = 41, 44, 46, 48, 49, 51, 42
C3x, F3, Ab3, Bb3, C4, Db4, Eb4 = 48, 53, 56, 58, 60, 61, 63
F4, Ab4, Bb4, B4, C5, Db5, Eb5, F5, Ab5 = 65, 68, 70, 71, 72, 73, 75, 77, 80
Bb5, C6, Db6, Eb6, F6, Ab6 = 82, 84, 85, 87, 89, 92

CHORDS = [[41, 48, 53, 56, 63],      # Fm11
          [37, 44, 49, 56, 60],      # Dbmaj9
          [42, 49, 54, 61, 64],      # Gbmaj9   - the bII, the menace
          [39, 46, 51, 58, 61]]      # Ebm9

SWING = 0.045                        # of a step, on the top layer only

# The sub's own octave. With an F1 root at 43.7 Hz the second harmonic lands
# at 87 - and 60-120 Hz is a band the kick already owns, so the sub carries
# just enough of it to be audible on a phone and no more.
SUBKW = dict(h2=0.42, h3=0.11)


# ============================================================ the kit
CELLS = {
    #        kicks        snares       ghosts               opens
    'A': ([0, 8],        [4, 12],     [2, 7, 10, 14],      [6, 14]),
    'B': ([0, 8, 10],    [4, 12],     [2, 7, 14],          [6, 14]),
    'C': ([0, 3, 8],     [4, 12],     [2, 6, 10, 13, 14],  [6, 10, 14]),
    'D': ([0, 8, 14],    [4, 12, 15], [2, 7, 10],          [6]),
    'E': ([0, 8],        [4, 12],     [7],                 [14]),
}


def drums(b, cell='A', gain=1.0, hats=1.0, ghosts=1.0, ride=0.0, perc=0.0,
          sc=True, seed=0, kick_g=1.0, snare_g=1.0):
    """One bar of kit. Beat 1 and beat 3 always get a kick and beats 2 and 4
    always get a snare, whatever the cell adds on top - a broken grid is a
    variation here, never the foundation."""
    ks, sn, gh, op = CELLS[cell]
    t0 = s.pos(b)
    for k in ks:
        t = s.pos(b, k)
        s.place(t, mkick(tune=66.0, seed=seed + k), gain * kick_g * (1.0 if k in (0, 8) else 0.72),
                'drums')
        if sc and k in (0, 8):
            s.hit(t)
    for k in sn:
        s.place(s.pos(b, k), msnare(seed=(seed + k) % 7),
                gain * snare_g * (1.0 if k in (4, 12) else 0.55), 'drums')
    if ghosts:
        for k in gh:
            s.place(s.pos(b, k + SWING), mghost(seed=seed + k),
                    gain * ghosts * (0.55 + 0.35 * ((seed + k) % 3) / 2), 'drums')
    if hats:
        vel = [1.0, .42, .66, .42, .88, .42, .66, .48,
               1.0, .42, .66, .42, .88, .48, .70, .58]
        for k in range(16):
            # Alternating pan on the hats. Two hits a bar in the centre and
            # fourteen spread across the field is where the width above 3 kHz
            # comes from; the references measure 110-140% side up there and
            # a mono hat line cannot get anywhere near it.
            p = 0.46 * (1 if k % 2 else -1) * (1 - 0.5 * (k % 4 == 0))
            if k in op:
                s.place(s.pos(b, k + SWING),
                        panned(mhat(2.4, open_=True, seed=seed * 3 + k), p * 1.3),
                        gain * hats * 0.60, 'drums')
            else:
                s.place(s.pos(b, k + SWING),
                        panned(mhat(seed=seed * 3 + k), p),
                        gain * hats * vel[k] * 0.62, 'drums')
    if ride:
        for k in range(0, 16, 2):
            s.place(s.pos(b, k + SWING),
                    panned(mride(2.0, seed=seed + k), 0.28 * (1 if k % 4 else -1)),
                    gain * ride * (0.6 if k % 4 else 0.95) * 0.42, 'drums')
    if perc:
        # Struck metal is inharmonic above its fundamental, but the
        # fundamental still has a pitch. These are C6, Eb6, F5 and Ab6 - in
        # the key - because a clank at 980 Hz over F minor is a wrong note
        # that happens to be made of metal.
        # Three of the four hits are on beats or offbeat 8ths. A figure whose
        # every hit is on a weak sixteenth has no meter to be syncopated
        # against, and the ear files it as a second machine running alongside
        # the track rather than as part of it. The spine is 2, 8 and 14 -
        # steps the topline does not use, so this answers instead of doubling.
        # Struck metal, damped hard and rolled off at 2.6 kHz. A clank that
        # rings for 400 ms in the octave above the snare is a glockenspiel,
        # and a glockenspiel makes a dark record sound cheerful whatever the
        # notes are. Two hits a bar, not four, both on the top two metrical
        # tiers, both short enough to read as an object being struck in a
        # room rather than as a tuned instrument playing along.
        pat = [(2, F4, -0.6), (8, C5, 0.5)]
        for i, (k, nt, p) in enumerate(pat):
            if (seed + i) % 3:
                s.place(s.pos(b, k + SWING),
                        panned(lp(mclank(dur_steps=1.2, note=nt, damp=3.2,
                                         bright=0.55, seed=seed + i), 2600, 4), p),
                        gain * perc * 0.16, 'texture')
        for k, nt, p in ((10, F5, 0.4), (14, C5, -0.45), (5, Ab4, 0.25)):
            s.place(s.pos(b, k + SWING), panned(mtok(note=nt, seed=seed + k), p),
                    gain * perc * 0.30, 'texture')
        for k in (0, 2, 4, 6, 8, 10, 12, 14):
            s.place(s.pos(b, k + SWING), mshake(seed=seed + int(k)),
                    gain * perc * 0.22, 'texture')


# ============================================================ the bass
def repeat(pat, times, bars_each=2):
    """A short pattern laid end to end, with the step numbers offset - so an
    eight-bar sub block is one oscillator playing a two-bar figure four times
    rather than four segments butted together."""
    out = []
    for k in range(times):
        out += [(st + k * bars_each * 16, nt) for st, nt in pat]
    return tuple(out)


# Riff A - the drop. Five notes in two bars; the line is in the tablature.
RIFF_A = (((0, F2), (4, F2), (6, Ab2), (10, F2), (12, Eb2),
           (16, F2), (19, Bb2), (22, F2), (24, Db2), (28, F2)),
          "Gwo. GwWo .oGw gWo.  GwoG woGw Gwo. Gwo.")
SUB_A = ((0, F1), (6, Ab1), (10, F1), (12, Eb1),
         (16, F1), (19, Bb1), (22, F1), (24, Db1), (28, F1))

# Riff B - the same skeleton, said instead of played. The vowels move per
# step; the tablature keeps the holes so the words have consonants.
RIFF_B = (((0, F2), (3, F2), (6, Gb2), (10, F2), (13, C3),
           (16, F2), (18, Ab2), (22, Eb2), (26, F2), (29, Db3)),
          "OwoO woOw o.Ow Owo.  GwOw o.Gw OwO. gwo.")
VOWELS_B = ['oo', 'ah', 'oo', 'ee', 'oh', 'ah', 'ee', 'uh',
            'ah', 'oo', 'ee', 'ah', 'oh', 'ee', 'ah', 'oo',
            'ee', 'ah', 'oh', 'oo', 'ah', 'ee', 'uh', 'ah',
            'oo', 'ee', 'ah', 'oh', 'ee', 'ah', 'oo', 'ee']
SUB_B = ((0, F1), (6, Gb1), (10, F1), (13, C2),
         (16, F1), (18, Ab1), (22, Eb1), (26, F1), (29, Db2))

# Riff C - the third drop. Same notes as A an octave apart in places, the
# tablature pushed up: where A growled, C screeches.
RIFF_C = (((0, F2), (4, F2), (6, Ab2), (8, F2), (10, C3), (12, Eb2), (14, F2),
           (16, F2), (18, Db3), (20, F2), (23, Bb2), (26, Ab2), (28, F2), (30, Gb2)),
          "SwoG mwSo Gwmo SwGo  Swmo Gwom woGw SxGo")
SUB_C = ((0, F1), (6, Ab1), (10, C2), (12, Eb1), (14, F1),
         (16, F1), (18, Db2), (23, Bb1), (26, Ab1), (28, F1), (30, Gb1))


# Four different saws across a thirty-two bar drop. The riff does not change;
# the oscillator under it does - narrow and hard, then wide and chorused, then
# driven, then notched. Eight bars is the longest a single timbre survives at
# 174 BPM, and changing the SOUND is a better answer than changing the notes,
# which would cost the drop its hook.
DROPMOD = [dict(wide=0.55, cut=0.92),
           dict(wide=1.35, nk=1.30),
           dict(wide=0.85, cut=1.14, drive=1.10),
           dict(wide=1.60, nk=0.78, q=1.25)]


ACCENT = set('mSxG')


def accents(tab):
    """The accent layer only speaks where the tablature asks for teeth. Left
    open it doubles the reese an octave up and the two fight for 600 Hz."""
    return [1.0 if c in ACCENT else 0.05 for c in tab if c in CHARS]


def lay(b0, blocks, riff, subpat, gain=1.0, subg=1.0, acc=0.0, sub_kw=None,
        mods=None, acc_kw=None, **kw):
    """Place `blocks` x 8 bars of one riff, in three layers that never share a
    band: `subbar` under 145 Hz, mono, one continuous oscillator across eight
    bars; `reese` from 62 Hz to about 4 kHz carrying the note; and `bassbar`
    highpassed at 680 Hz, gated so it only sounds on the accent characters,
    for the sync tear the reese deliberately does not have."""
    notes, tab = riff
    for k in range(blocks):
        b = b0 + k * 8
        kk = dict(kw)
        if mods:
            for key, v in mods[k % len(mods)].items():
                kk[key] = kk.get(key, 1.0) * v
        s.place(s.pos(b), subbar(repeat(subpat, 4), 128, **(sub_kw or SUBKW)),
                subg, 'sub')
        for j in range(4):
            s.place(s.pos(b + j * 2), reese_c(notes, tab, 32, **kk), gain, 'bass')
            if acc:
                s.place(s.pos(b + j * 2),
                        bassbar_c(notes, tab, 32, cut=2.4, q=0.8, hpf=680,
                                  detune=22.0, top=0.45, spr=0.6, rs=1.0,
                                  drives=(0.0, 0.0, 3.0, 2.2),
                                  gatep=accents(tab), **(acc_kw or {})),
                        acc, 'body')


# ============================================================ the topline
# Two bars, F minor pentatonic with one note from outside it: the B natural
# in bar 2 is the b5, and it is the only surprise the tune gets.
LEAD = ((0, F4), (3, Ab4), (6, F4), (10, C5), (12, Bb4),
        (16, Ab4), (20, Eb4), (23, F4), (27, B4), (30, F4))
LEAD_CUT = [2600, 5200, 3000, 6800, 2400, 4400, 3200, 7400,
            2800, 4000, 5600, 2600, 6000, 3400, 4800, 2400] * 2
LEAD_SYNC = [1.0, 2.2, 1.0, 3.0, 1.4, 1.0, 2.6, 1.8,
             1.0, 2.4, 1.0, 3.4, 1.2, 2.0, 1.0, 2.8] * 2

# The dark line. Four bars, one bowed voice, and it goes DOWN: F3 up to Ab3,
# then a slow fall through Eb3 and Db3 to C3. A rising figure in a high
# register over a track this heavy is a music box; the same intervals an
# octave and a half lower, bowed, with a fifth under them, is the same tune
# read as a threat. It states the topline before anything else does, so the
# lead in the third drop is a return rather than an arrival.
GLOOM = ((0, F3), (12, Ab3), (26, Eb3), (40, Db3), (52, C3x), (58, F3))


def hole(b, s0=14.0, s1=16.0):
    """Cut everything to silence over the last beat of a bar. The gap is what
    makes the downbeat after it land; it costs nothing and works twice a
    record, which is exactly how often it is used here."""
    a, e = s.pos(b, s0), s.pos(b, s1)
    ramp = np.linspace(1, 0, e - a)[:, None] ** 1.4
    for name in s.bus:
        s.bus[name][a:e] *= ramp


def bandcut(b0, b1, bus, f0, f1, kind='hp'):
    """Sweep a filter across a range of bars on one bus, after the fact. A
    build is a filter opening on material that is already there, not a
    different arrangement."""
    a, e = s.pos(b0), s.pos(b1)
    seg = s.bus[bus][a:e]
    n = len(seg)
    lane = np.geomspace(f0, f1, n)
    s.bus[bus][a:e] = svf(seg, lane, 1.1, kind, block=256)


# ============================================================ intro 0-15
for b in range(0, 16, 4):
    s.place(s.pos(b), air(64, gain=1.0, seed=b, lo=700, hi=6500), 1.0, 'atmos')
for b in (0, 8):
    s.place(s.pos(b), mgloom(GLOOM, 64, gain=0.85 if b else 0.7,
                             cut=(420, 1700), seed=b), 1.0, 'pad')
s.place(s.pos(2), grains(mclank(dur_steps=4, note=F3, damp=1.5, bright=0.4,
                                seed=5), 32, density=18, seed=11,
                         pitch=(0.35, 1.3)), 0.7, 'atmos')
s.place(s.pos(10), grains(msnare(seed=2), 32, density=26, seed=12,
                          pitch=(0.4, 1.8)), 0.5, 'atmos')
for b in range(4, 16):
    s.place(s.pos(b), mpad(CHORDS[(b // 4) % 4], 16, cut=900, seed=b), 0.34, 'pad')
for b in range(8, 16):
    drums(b, 'E', gain=0.55, hats=0.7, ghosts=0.3, perc=0.0, sc=b >= 12, seed=b)
s.place(s.pos(14), slam(16, gain=0.5, seed=3), 1.0, 'fx')

# ============================================================ approach 16-31
for b in range(16, 32):
    cell = ['A', 'A', 'B', 'A', 'A', 'C', 'A', 'D'][b % 8]
    drums(b, cell, gain=0.9, hats=0.95, ghosts=0.8, perc=0.5 if b >= 24 else 0.0,
          seed=b)
    s.place(s.pos(b), mpad(CHORDS[(b // 4) % 4], 16, cut=1150, seed=b), 0.30, 'pad')
    if b % 8 == 0:
        s.place(s.pos(b), mgloom(GLOOM, 128, gain=0.55, cut=(480, 1900),
                                 seed=b, decay=0.0), 1.0, 'pad')
# The riff is here from bar 16, but with the tablature's cutoffs at 45% - the
# same line, heard through a closed filter, so the drop is a lid coming off
# rather than a new idea arriving.
lay(16, 2, RIFF_A, SUB_A, gain=0.62, subg=0.85, cut=0.8, q=0.7, wide=0.6)

# ============================================================ build 1  32-39
for b in range(32, 40):
    cell = ['A', 'B', 'A', 'C', 'A', 'B', 'C', 'D'][b - 32]
    drums(b, cell, gain=0.95, hats=1.0, ghosts=0.9, perc=0.6, seed=b)
    s.place(s.pos(b), mpad(CHORDS[(b // 2) % 4], 16, cut=1400, seed=b), 0.32, 'pad')
lay(32, 1, RIFF_A, SUB_A, gain=0.72, subg=0.9, acc=0.30, cut=1.05, q=0.85)
# The riser is the drop's own bar, reversed and opened. It predicts the sound
# it leads into instead of announcing that something is coming.
_dropbar = reese_c(RIFF_A[0], RIFF_A[1], 32)
s.place(s.pos(36), revfx(_dropbar, cut=(260, 8000), q=1.5), 0.55, 'fx')
roll(s, 38, 8.0, 12, spacing=0.7, gain=0.55, accel=True, voice=msnare,
     seed=31, dur_steps=2.0)
s.place(s.pos(39, 12), subdive(6, 92, 27, gain=0.55), 1.0, 'fx')
s.place(s.pos(39, 8), rev(mhat(8, open_=True, seed=9)), 0.5, 'fx')
hole(39, 15.0, 16.0)

# ============================================================ DROP 1  40-71
lay(40, 4, RIFF_A, SUB_A, gain=1.0, subg=1.0, acc=0.55, cut=2.0,
    mods=DROPMOD)
for b in range(40, 72):
    i = b - 40
    cell = ['A', 'A', 'B', 'A', 'A', 'C', 'B', 'D'][i % 8]
    drums(b, cell, gain=1.0, hats=1.0, ghosts=1.0, perc=0.85,
          ride=0.8 if i >= 16 else 0.0, seed=b)
    if i % 8 == 7:
        roll(s, b, 12.0, 6, spacing=0.66, gain=0.5, accel=True, seed=b)
    if i % 8 in (3, 7):
        s.place(s.pos(b, 14), panned(screech(F4 if i % 16 < 8 else Ab4, 2.5,
                                             gain=0.42, seed=b), 0.4), 1.0, 'music')
    if i in (0, 16):
        s.place(s.pos(b), slam(16, gain=0.62, seed=b), 1.0, 'fx')
    if i % 4 == 2:
        s.place(s.pos(b, 7), panned(lp(mclank(dur_steps=1.4, damp=3.0, bright=0.5,
                                      note=[C5, Bb4, Ab4, F4][i % 4],
                                      seed=b), 2400, 4), -0.55),
                0.18, 'texture')
s.place(s.pos(71, 12), subdive(6, 88, 26, gain=0.5), 1.0, 'fx')
hole(71, 14.5, 16.0)

# ============================================================ breakdown 72-87
for b in range(72, 88):
    ch = CHORDS[(b // 2) % 4]
    s.place(s.pos(b), mpad(ch, 16, cut=1600 if b < 80 else 2400, seed=b), 0.42, 'pad')
    s.place(s.pos(b), air(16, gain=1.2, seed=b, lo=500, hi=5000), 1.0, 'atmos')
    if b % 2 == 0:
        s.place(s.pos(b), subbar(((0, ch[0] - 12),), 32, drive=1.1, **SUBKW), 0.38, 'sub')
    if b >= 76:
        s.place(s.pos(b, 0), mstab(ch, 2.2, gain=0.32, cut=(4200, 900), seed=b),
                1.0, 'music')
        s.place(s.pos(b, 10), mstab(ch, 1.6, gain=0.22, cut=(3000, 800), seed=b + 3),
                1.0, 'music')
    if b >= 80:
        drums(b, 'E', gain=0.62, hats=0.55, ghosts=0.4, perc=0.4, seed=b, sc=b >= 84)
# The breakdown says the tune twice: bowed and dark first, then the lead.
s.place(s.pos(72), mgloom(GLOOM, 128, gain=0.62, cut=(400, 2200), seed=72), 1.0, 'pad')
s.place(s.pos(80), mgloom(tuple((st, nt + 5) for st, nt in GLOOM), 128, gain=0.50,
                          cut=(500, 2600), seed=80), 1.0, 'pad')
for b in (78, 86):
    s.place(s.pos(b), mlead(LEAD, 32, gain=0.50, cut=[c * 0.7 for c in LEAD_CUT],
                            sync=LEAD_SYNC, q=3.5, drive=1.5, decay=0.55), 1.0, 'music')
s.place(s.pos(72), grains(_dropbar, 64, density=22, seed=21, pitch=(0.3, 1.1)),
        0.55, 'atmos')
s.place(s.pos(80), grains(msnare(seed=1), 64, density=30, seed=22, pitch=(0.5, 2.2)),
        0.40, 'atmos')

# ============================================================ build 2  88-95
for b in range(88, 96):
    cell = ['A', 'A', 'B', 'C', 'A', 'B', 'C', 'D'][b - 88]
    drums(b, cell, gain=0.9 + 0.02 * (b - 88), hats=1.0, ghosts=0.9,
          perc=0.7, seed=b)
    s.place(s.pos(b), mpad(CHORDS[(b // 2) % 4], 16, cut=2000, seed=b), 0.40, 'pad')
lay(88, 1, RIFF_B, SUB_B, gain=0.75, subg=0.92, acc=0.35, cut=1.0, q=0.8)
_dropbarB = reese_c(RIFF_B[0], RIFF_B[1], 32)
s.place(s.pos(92), revfx(_dropbarB, cut=(300, 9000), q=1.6), 0.55, 'fx')
roll(s, 94, 8.0, 14, spacing=0.62, gain=0.55, accel=True, voice=msnare,
     seed=71, dur_steps=2.0)
s.place(s.pos(95, 12), subdive(6, 95, 26, gain=0.55), 1.0, 'fx')
hole(95, 15.0, 16.0)

# ============================================================ DROP 2  96-127
lay(96, 4, RIFF_B, SUB_B, gain=1.15, subg=1.05, acc=0.70, cut=2.0,
    acc_kw=dict(vowel=VOWELS_B), mods=DROPMOD)
for b in range(96, 128):
    i = b - 96
    cell = ['B', 'A', 'C', 'A', 'B', 'A', 'C', 'D'][i % 8]
    drums(b, cell, gain=1.0, hats=1.0, ghosts=1.0, perc=1.0,
          ride=0.85 if i >= 8 else 0.0, seed=b + 40)
    if i % 8 == 7:
        roll(s, b, 12.0, 6, spacing=0.66, gain=0.5, accel=True, seed=b)
    if i in (0, 16):
        s.place(s.pos(b), slam(16, gain=0.58, seed=b), 1.0, 'fx')
    if i % 4 == 1:
        s.place(s.pos(b, 4), panned(lp(mclank(dur_steps=1.4, damp=3.0, bright=0.5,
                                     note=[Ab4, C5, Eb5, F5, Bb4][i % 5],
                                     seed=b), 2400, 4), 0.6),
                0.18, 'texture')
    if i % 8 == 5:
        s.place(s.pos(b, 8), panned(screech(C5, 3.0, gain=0.34, r1=7.0, seed=b), -0.45),
                1.0, 'music')
s.place(s.pos(127, 12), subdive(6, 90, 25, gain=0.5), 1.0, 'fx')
hole(127, 14.5, 16.0)

# ============================================================ machines 128-143
# No bass line at all for sixteen bars. The kick and the snare hold the pulse
# and everything else is the sound design that has been decorating the drops -
# clanks, grains and a dub delay - promoted to being the arrangement.
for b in range(128, 144):
    i = b - 128
    drums(b, 'E' if i < 8 else 'A', gain=0.9, hats=0.55 if i < 8 else 0.9,
          ghosts=0.5, perc=1.2, seed=b + 90)
    s.place(s.pos(b), subbar(((0, F1), (8, Db1)), 16, drive=1.15, **SUBKW), 0.72, 'sub')
    s.place(s.pos(b), air(16, gain=1.0, seed=b, lo=800, hi=7000), 1.0, 'atmos')
    if i % 4 == 0:
        s.place(s.pos(b), grains(mclank(dur_steps=5, note=[F3, Ab3, C4, Eb4][i % 4],
                                damp=1.6, bright=0.4, seed=b), 64, density=16,
                                 seed=b, pitch=(0.3, 1.6)), 0.5, 'atmos')
    for k, nt, p in [(2, Eb5, -0.7), (6, Ab4, 0.6), (10, C5, 0.3), (14, F4, -0.4)]:
        if (i + int(k)) % 2 == 0:
            s.place_echo(s.pos(b, k + SWING),
                         panned(lp(mclank(dur_steps=2.0, damp=2.4, bright=0.6,
                                          note=nt, seed=b + int(k)), 2800, 4), p),
                         0.34, times=3, delay_steps=3.0, fb=0.45, bus='texture')
    if i >= 8:
        s.place(s.pos(b, 0), mstab(CHORDS[(b // 2) % 4], 2.0, gain=0.34,
                                   cut=(3800, 800), seed=b), 1.0, 'music')
s.place(s.pos(132), mgloom(GLOOM, 128, gain=0.60, cut=(430, 2000), seed=132),
        1.0, 'pad')
s.place(s.pos(136), mlead(LEAD, 32, gain=0.34, cut=[c * 0.5 for c in LEAD_CUT],
                          sync=LEAD_SYNC, q=3.0, drive=1.4, decay=0.4), 1.0, 'music')

# ============================================================ build 3  144-151
for b in range(144, 152):
    cell = ['A', 'B', 'A', 'C', 'B', 'C', 'C', 'D'][b - 144]
    drums(b, cell, gain=1.0, hats=1.0, ghosts=1.0, perc=0.9, seed=b + 10)
    s.place(s.pos(b), mpad(CHORDS[(b // 2) % 4], 16, cut=2400, seed=b), 0.36, 'pad')
lay(144, 1, RIFF_C, SUB_C, gain=0.80, subg=0.95, acc=0.45, cut=1.1, q=0.85)
_dropbarC = reese_c(RIFF_C[0], RIFF_C[1], 32)
s.place(s.pos(148), revfx(_dropbarC, cut=(320, 10000), q=1.7), 0.58, 'fx')
roll(s, 150, 4.0, 20, spacing=0.62, gain=0.6, accel=True, voice=msnare,
     seed=111, dur_steps=2.0)
s.place(s.pos(151, 12), subdive(6, 98, 25, gain=0.6), 1.0, 'fx')
s.place(s.pos(151, 8), rev(mride(8, seed=4)), 0.45, 'fx')
hole(151, 15.0, 16.0)

# ============================================================ DROP 3  152-183
lay(152, 4, RIFF_C, SUB_C, gain=1.0, subg=1.0, acc=0.85, cut=2.1,
    mods=[DROPMOD[i] for i in (1, 3, 0, 2)])
for b in range(152, 184):
    i = b - 152
    cell = ['A', 'C', 'B', 'A', 'C', 'A', 'B', 'D'][i % 8]
    drums(b, cell, gain=1.0, hats=1.0, ghosts=1.0, perc=1.0,
          ride=0.9 if i >= 8 else 0.0, seed=b + 60)
    if i % 8 == 7:
        roll(s, b, 12.0, 8, spacing=0.55, gain=0.52, accel=True, seed=b)
    if i in (0, 16):
        s.place(s.pos(b), slam(16, gain=0.6, seed=b), 1.0, 'fx')
    if i % 8 in (2, 6):
        s.place(s.pos(b, 12), panned(screech(Ab4 if i % 16 < 8 else C5, 2.5,
                                             gain=0.38, seed=b), -0.5), 1.0, 'music')
for b in range(152, 184, 4):
    if b >= 160:
        s.place(s.pos(b), mlead(LEAD, 32, gain=0.46, cut=LEAD_CUT, sync=LEAD_SYNC,
                                q=4.5, drive=2.0, decay=0.0), 1.0, 'music')

# ============================================================ outro 184-191
for b in range(184, 192):
    i = b - 184
    fade = max(0.0, 1 - i / 7.5)
    drums(b, 'A' if i < 4 else 'E', gain=0.95 * fade, hats=0.9 * fade,
          ghosts=0.7 * fade, perc=0.6 * fade, seed=b, sc=i < 5)
    s.place(s.pos(b), air(16, gain=1.2, seed=b, lo=600, hi=6000), 1.0, 'atmos')
    if i < 5:
        s.place(s.pos(b), subbar(((0, F1),), 16, drive=1.1, **SUBKW), 0.8 * fade, 'sub')
    s.place(s.pos(b), mpad(CHORDS[0], 16, cut=1200, seed=b), 0.30 * max(fade, 0.4), 'pad')
if True:
    s.place(s.pos(184), reese_c(RIFF_C[0], RIFF_C[1], 32), 0.6, 'bass')
    s.place(s.pos(186), reese_c(RIFF_A[0], RIFF_A[1], 32, cut=0.6, q=0.8),
            0.4, 'bass')
s.place(s.pos(190), grains(_dropbarC, 32, density=20, seed=44, pitch=(0.25, 1.0)),
        0.45, 'atmos')
s.place(s.pos(186), mgloom(GLOOM, 96, gain=0.75, cut=(380, 1400), seed=9),
        1.0, 'pad')


# ============================================================ the mix
# Space, and not much of it. At 174 BPM a bar is 1.38 s, so a 3-second tail
# covers two bars; every reverb here is shorter than a bar except the one on
# the pad, which is the only thing allowed to blur.
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.3, wet=0.24, tone=5200)
s.bus['texture'] = bus_reverb(s.bus['texture'], decay=0.9, wet=0.22, tone=6000)
s.bus['pad'] = bus_reverb(s.bus['pad'], decay=2.8, wet=0.34, tone=3200)
s.bus['atmos'] = bus_reverb(s.bus['atmos'], decay=3.2, wet=0.30, tone=2800)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=1.8, wet=0.20, tone=4400)

# The sub is mono below 200 Hz and nothing else touches it. The mid bass keeps
# a presence peak at 1.1 kHz - the band a phone can actually reproduce, where
# the ear reconstructs the fundamental it cannot hear - and is shelved out of
# 2.8 kHz up, which belongs to the snare's crack and the kick's click. Two
# hits a bar are what the ear counts the bar by; a bass that buries them
# turns the groove into a texture.
# The sub is the densest thing on the record already; this only stops the
# few bars where a kick lands in phase with it from setting the peak for
# the whole track.
s.bus['sub'] = compress(mono_below(s.bus['sub'], 200), thresh=0.50, ratio=3.0,
                        attack=0.004, release=0.09)
# The reese is EQ'd the way the samples are shaped, not the way a bright synth
# bass would be: one broad lift at 420 Hz, where the resonant hump lives, and
# nothing else. The cuts a saw-and-filter bass needs at 700 and 1800 Hz would
# take out exactly the band this instrument exists to occupy.
s.bus['bass'] = peak_eq(peak_eq(s.bus['bass'], 420, 2.0, 0.8), 200, -2.5, 0.8)
# The sub owns everything under 105 Hz. Left in, the reese's own
# fundamental doubles it and the whole record turns into 60-120 Hz;
# taken out, what is left is the resonant hump at 300-800, which is the
# part of a reese anyone actually recognises.
s.bus['bass'] = mono_below(hp(s.bus['bass'], 105, 2), 130)
# The accent layer lives entirely above the reese: highpassed at 700 and
# shelved off the snare's crack, it adds teeth without adding weight.
s.bus['body'] = shelf(hp(s.bus['body'], 700, 2), 3200, -3.0, 'high')
s.bus['body'] = side_boost(compress(s.bus['body'], thresh=0.22, ratio=3.2,
                                    attack=0.005, release=0.10), 900, 0.45)
s.bus['drums'] = peak_eq(shelf(hp(s.bus['drums'], 34, 2), 6200, 4.5, 'high'),
                         3800, 1.5, 0.5)
# Glue on the drum bus, and it is a loudness decision as much as a sound one.
# The bus arrives with a crest of 10.5 dB because kick, snare, hats and a
# clank occasionally land on the same sample; those coincidences set the
# peak the master clipper then has to shave off the whole record. Taking
# 2 dB off them here is worth more than 2 dB of clipping everywhere.
s.bus['drums'] = compress(s.bus['drums'], thresh=0.24, ratio=3.5, attack=0.010,
                          release=0.11, report=True, label='drum bus')
s.bus['drums'] = peak_eq(s.bus['drums'], 5200, 2.0, 0.6)
# Width above 3 kHz only. The references measure 107-140% side up there and
# 16-19% below 120 Hz - a wide top over a mono bottom, which is what a club
# system can actually reproduce.
s.bus['drums'] = side_boost(s.bus['drums'], 3000, 0.55)
s.bus['texture'] = side_boost(compress(s.bus['texture'], thresh=0.14, ratio=3.0,
                                       attack=0.006, release=0.10), 1200, 0.5)
s.bus['music'] = shelf(hp(s.bus['music'], 190, 2), 2600, -5.0, 'high')
s.bus['texture'] = shelf(hp(s.bus['texture'], 300, 2), 3000, -4.0, 'high')
s.bus['pad'] = hp(s.bus['pad'], 200, 2)
s.bus['atmos'] = hp(s.bus['atmos'], 240, 2)
s.bus['fx'] = hp(s.bus['fx'], 30, 2)

# Scaled so the bus sum peaks a little over 1.0: the clipper is then shaving
# the tips of two or three transients per bar, which is inaudible, instead of
# a fifth of the record, which is the "too distorted" complaint.
GAINS = {'drums': 0.88, 'sub': 0.34, 'bass': 1.00, 'body': 1.35,
         'texture': 0.56, 'music': 0.58, 'pad': 0.30, 'atmos': 0.46, 'fx': 0.32}
s.report(GAINS)
# The two reference records measure a crest factor of 4.2-4.5 dB inside a
# drop and spend 65% of their time within 6 dB of the ceiling. That is a
# brickwalled master, and no amount of clipping reaches it - a clipper only
# removes the tips, and the ten loudest moments here are spread over nine
# different bars, so there is no single event to turn down either. The chain
# is therefore: a clipper that takes the spikes off first - if it does not,
# the limiter has to duck a whole bar to catch one sample and the master
# gets QUIETER the harder it is pushed - then 3:1 glue for cohesion, then
# 6.4 dB of push into a look-ahead limiter. It lands a little short of the
# references on purpose: at a crest of 7 the kit still hits.
s.render('neurofunk_razlom_174.wav', drive=0.0, duck=0.26, duck_rel=0.090,
         limit=0.0, peak=0.99, gains=GAINS, clip=1.20, fade=2.2,
         comp=dict(thresh=0.38, ratio=2.5, attack=0.006, release=0.11,
                   makeup=1.2),
         brick=dict(gain=1.55, ceiling=0.89, release=0.075))
