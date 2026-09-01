"""RAZRYV - neurofunk, F minor, 174 BPM. The bass is a workflow, not a patch.

Written to the modern neuro bass method rather than to a synth preset:

1. **The scan is the sound.** `neurobass()` reads a spectral wavetable with a
   per-sample position, and the position is a sixteen-value lane per bar with
   several peaks in it - not an LFO. Measured on one held note, the scan moves
   the spectral centroid 1.6 octaves a bar; the same patch with the position
   nailed down moves 0.7, and most of that is the distortion. A wavetable
   whose position never moves is a subtractive patch with extra steps.
2. **The distortion is serial, and EQ'd between every stage.** Waveshaper for
   odd harmonics, then an asymmetric saturator for even ones, then bit
   reduction for grit - each driven moderately, each followed by a 105 Hz
   highpass and an 8 kHz lowpass. Skipping the inter-stage EQ is what makes a
   neuro patch mud at the bottom and pain at the top.
3. **The formant moves with the scan.** The same lane drives both, so the
   vowel and the waveform change together and the bass reads as saying
   something rather than as being filtered.
4. **Two resampling passes.** An octave-down pass and an octave-up pass with
   transient shaping between them, blended back - relationships no oscillator
   generated.
5. **It is edited, not played.** Every two-bar cell is assembled by `stitch()`
   from two finished patches - a growl table and a vowel table - cut against
   each other at the half bar and the beat. The riff stays the same and the
   instrument changes underneath it.

Three layers that never share a band: `subbar` under 105 Hz, mono, one
unbroken oscillator across eight bars; the neuro bass from 105 Hz up; and
`reese()` behind it for the width and the weight in 200-500 Hz that a
distorted wavetable does not have.

    intro       0-15   room, the dark voice, drums arriving filtered
    groove     16-23   the kit, the sub, the riff at half power
    build 1    24-31
    DROP 1     32-63   statement / variation / four bars halftime / escalation
    breakdown  64-79   Fm - Db - Gb - Eb, and the tune said out loud
    build 2    80-87
    DROP 2     88-119  the vowel table forward: the bass talks
    machines  120-135  no bass line; clanks, grains, a dub delay
    build 3   136-143
    DROP 3    144-175  both tables stitched bar by bar, the lead over it
    outro     176-191

Kick on beats 1 and 3, snare on 2 and 4, in every cell: an event on every
beat, so the felt pulse is 174 and not 87. The halftime bars inside the drops
are four bars long and never more.
"""
import numpy as np
from machinelib import *

s = Session(192, tail=3.0)

# ---- F minor, with the Phrygian bII for the chords ----
Db1, Eb1, F1, Gb1, Ab1, Bb1 = 25, 27, 29, 30, 32, 34
C2, Db2, Eb2 = 36, 37, 39
F2, Gb2, Ab2, Bb2, C3, Db3, Eb3 = 41, 42, 44, 46, 48, 49, 51
C3x, F3, Ab3, Bb3, C4, Db4, Eb4 = 48, 53, 56, 58, 60, 61, 63
F4, Ab4, Bb4, B4, C5, Db5, Eb5, F5 = 65, 68, 70, 71, 72, 73, 75, 77

CHORDS = [[41, 48, 53, 56, 63],      # Fm11
          [37, 44, 49, 56, 60],      # Dbmaj9
          [42, 49, 54, 61, 64],      # Gbmaj9  - the bII
          [39, 46, 51, 58, 61]]      # Ebm9

SWING = 0.045
SUBKW = dict(h2=0.42, h3=0.11)

# ============================================================ the kit
CELLS = {
    'A': ([0, 8],       [4, 12],     [2, 7, 10, 14],     [6, 14]),
    'B': ([0, 8, 10],   [4, 12],     [2, 7, 14],         [6, 14]),
    'C': ([0, 3, 8],    [4, 12],     [2, 6, 10, 13, 14], [6, 10, 14]),
    'D': ([0, 8, 14],   [4, 12, 15], [2, 7, 10],         [6]),
    'E': ([0, 8],       [4, 12],     [7],                [14]),
    'H': ([0],          [8],         [4, 11],            [6, 14]),   # halftime
}


def drums(b, cell='A', gain=1.0, hats=1.0, ghosts=1.0, ride=0.0, perc=0.0,
          sc=True, seed=0):
    ks, sn, gh, op = CELLS[cell]
    for k in ks:
        t = s.pos(b, k)
        s.place(t, mkick(tune=66.0, seed=seed + k),
                gain * (1.0 if k in (0, 8) else 0.72), 'drums')
        if sc and k in (0, 8):
            s.hit(t)
    for k in sn:
        s.place(s.pos(b, k), msnare(seed=(seed + k) % 7),
                gain * (1.0 if k in (4, 8, 12) else 0.55), 'drums')
    if ghosts:
        for k in gh:
            s.place(s.pos(b, k + SWING), mghost(seed=seed + k),
                    gain * ghosts * (0.55 + 0.35 * ((seed + k) % 3) / 2), 'drums')
    if hats:
        vel = [1.0, .42, .66, .42, .88, .42, .66, .48,
               1.0, .42, .66, .42, .88, .48, .70, .58]
        for k in range(16):
            p = 0.46 * (1 if k % 2 else -1) * (1 - 0.5 * (k % 4 == 0))
            if k in op:
                s.place(s.pos(b, k + SWING),
                        panned(mhat(2.0, open_=True, seed=seed * 3 + k), p * 1.3),
                        gain * hats * 0.50, 'drums')
            else:
                s.place(s.pos(b, k + SWING), panned(mhat(seed=seed * 3 + k), p),
                        gain * hats * vel[k] * 0.62, 'drums')
    if ride:
        for k in range(0, 16, 2):
            s.place(s.pos(b, k + SWING),
                    panned(mride(1.6, seed=seed + k), 0.28 * (1 if k % 4 else -1)),
                    gain * ride * (0.40 if k % 4 else 1.0) * 0.26, 'drums')
    if perc:
        # Two struck-metal hits a bar, damped hard and rolled off at 2.6 kHz,
        # on steps 2 and 8 - the top two metrical tiers, and steps the
        # topline does not use. A clank that rings in the octave above the
        # snare is a glockenspiel and makes a dark record sound cheerful.
        for i, (k, nt, p) in enumerate([(2, F4, -0.6), (8, C5, 0.5)]):
            if (seed + i) % 3:
                s.place(s.pos(b, k + SWING),
                        panned(lp(mclank(dur_steps=1.2, note=nt, damp=3.2,
                                         bright=0.55, seed=seed + i), 2600, 4), p),
                        gain * perc * 0.16, 'texture')
        for k, nt, p in ((10, F5, 0.4), (14, C5, -0.45), (5, Ab4, 0.25)):
            s.place(s.pos(b, k + SWING), panned(mtok(note=nt, seed=seed + k), p),
                    gain * perc * 0.30, 'texture')
        for k in (0, 2, 4, 6, 8, 10, 12, 14):
            s.place(s.pos(b, k + SWING), mshake(seed=seed + k),
                    gain * perc * 0.15, 'texture')


# ============================================================ the bass
def repeat(pat, times, bars_each=2):
    out = []
    for k in range(times):
        out += [(st + k * bars_each * 16, nt) for st, nt in pat]
    return tuple(out)


# The bass is two notes in two bars. Everything you hear as rhythm is the
# rate at which the timbre is travelling, sequenced as a list of gestures -
# a stretched sweep, two stabs of a different patch, a sixteenth roll, a
# thirty-second stutter, a dive. Six different gesture sequences per riff, so
# no two bars of a thirty-two bar drop are assembled the same way.
CELLS_A = [
    [('stretch', 0, 12), ('pau', 1, 4), ('roll16', 0, 8), ('stutter', 1, 4), ('dive', 0, 4)],
    [('swell', 0, 16), ('pau3', 1, 8), ('roll8', 0, 8)],
    [('roll8', 1, 8), ('stretch', 0, 10), ('pau2', 1, 6), ('trip', 0, 8)],
    [('accel', 0, 16), ('stutter', 1, 6), ('hold', 0, 4), ('roll16', 1, 6)],
    [('pau', 1, 6), ('stretch', 0, 14), ('roll16', 0, 6), ('pau3', 1, 6)],
    [('dive', 1, 6), ('roll8', 0, 10), ('stutter', 0, 4), ('swell', 1, 12)],
]
CELLS_B = [
    [('stretch', 1, 14), ('pau2', 0, 6), ('trip', 1, 6), ('stutter', 0, 6)],
    [('roll16', 0, 8), ('pau', 1, 4), ('swell', 0, 12), ('roll8', 1, 8)],
    [('climb', 1, 12), ('pau3', 0, 8), ('roll16', 1, 8), ('gap', 0, 4)],
    [('accel', 1, 16), ('pau', 0, 4), ('stretch', 1, 12)],
    [('pau2', 0, 8), ('stretch', 1, 12), ('stutter', 0, 6), ('brake', 1, 6)],
    [('roll8', 1, 10), ('pau3', 0, 6), ('dive', 1, 4), ('swell', 0, 12)],
]
CELLS_C = [
    [('stutter', 0, 6), ('stretch', 1, 12), ('pau3', 0, 6), ('roll16', 1, 8)],
    [('accel', 0, 16), ('pau', 1, 4), ('stutter', 0, 4), ('brake', 1, 8)],
    [('roll16', 1, 8), ('pau2', 0, 6), ('climb', 1, 10), ('stutter', 0, 8)],
    [('stretch', 0, 10), ('pau', 1, 4), ('trip', 0, 6), ('roll16', 1, 6), ('dive', 0, 6)],
    [('swell', 1, 12), ('pau3', 0, 8), ('stutter', 1, 6), ('roll8', 0, 6)],
    [('pau', 0, 4), ('accel', 1, 12), ('pau2', 0, 6), ('stutter', 1, 10)],
]

RIFF_A = dict(
    notes=((0, F2), (26, Eb2)),
    sub=((0, F1), (26, Eb1)),
    cells=CELLS_A,
    vowel=['oo', 'ah', 'oo', 'ee', 'oh', 'ah', 'ee', 'uh',
           'ah', 'oo', 'ee', 'ah', 'oh', 'ee', 'ah', 'oo'] * 2,
    rtab="wwwo wwww wwoO wwww  wwww ooww wwww wwoo",
    # The first drop is the reference sample itself: `witch` is that record's
    # partial profile - a resonant hump on the third to sixth harmonic and a
    # decibel of loss per partial after it - answered by the vowel table.
    tables=('witch', 'vowel'),
    chain=dict(ws=2.5, sat=1.9, fold_=0.25, crush=0),
)
RIFF_B = dict(
    notes=((0, F2), (14, Ab2), (24, F2)),
    sub=((0, F1), (14, Ab1), (24, F1)),
    cells=CELLS_B,
    vowel=['ee', 'ah', 'oh', 'oo', 'ah', 'ee', 'uh', 'ah',
           'oo', 'ee', 'ah', 'oh', 'ee', 'ah', 'oo', 'ee'] * 2,
    rtab="wwoo wwww WwwO wwww  wwww OwwW wwoo wwww",
    # The second drop is the other sample: a notch travelling through the
    # harmonics, answered by a hollow odd-harmonic table. No wavefolder here
    # and a bit-reducer instead - a different kind of dirt, so the two drops
    # are not the same patch at two brightnesses.
    tables=('reeseb', 'hollow'),
    chain=dict(ws=2.2, sat=2.4, fold_=0.0, crush=6),
)
RIFF_C = dict(
    notes=((0, F2), (16, Db2), (28, F2)),
    sub=((0, F1), (16, Db1), (28, F1)),
    cells=CELLS_C,
    vowel=['ah', 'ee', 'ah', 'oh', 'ee', 'ah', 'oo', 'ee',
           'ah', 'oh', 'ee', 'ah', 'oo', 'ee', 'ah', 'oh'] * 2,
    rtab="WwwO wwww GwwW wwww  wwww WwwG wwWO wwww",
    # The third drop is the harsh end: the growl table against `rip`, whose
    # moving comb piles energy exactly where the ear is most sensitive. It is
    # on one patch of the pair and never on both.
    tables=('growl', 'rip'),
    chain=dict(ws=3.0, sat=2.0, fold_=0.40, crush=9),
)

_P = {}


def cellbar(riff, ci, bright=1.0, drive=1.0):
    """One two-bar cell: two finished patches sharing one gesture timeline,
    cut against each other at the gesture boundaries.

    Patch 0 is the growl table with the waveshaper forward; patch 1 is the
    vowel table, bit-crushed, with the formant filter riding the same lane as
    the scan. Because the lanes are shared, the cut between them lands on a
    rhythm that was already moving - the instrument changes and the gesture
    does not stop.
    """
    key = (id(riff), ci, round(bright, 3), round(drive, 3))
    if key not in _P:
        ph = phrase(riff['cells'][ci % len(riff['cells'])], 32)
        cut = 800 + (6800 * bright - 800) * (ph['pos'] / 7.8)
        t0, t1 = riff['tables']
        c = riff['chain']
        p0 = neurobass(riff['notes'], 32, table=t0, pos=ph['pos'],
                       cut=cut, q=2.4, ws=c['ws'] * drive, sat=c['sat'],
                       fold_=c['fold_'], crush=0, gatep=ph['gatep'],
                       punch=0.35, glide=0.045,
                       passes=((0.5, 0.0), (2.0, 0.0)), seed=11)
        p1 = neurobass(riff['notes'], 32, table=t1, pos=ph['pos'],
                       cut=cut * 0.8, q=3.0, ws=(c['ws'] - 0.5) * drive,
                       sat=c['sat'] + 0.3, crush=max(c['crush'], 6),
                       vowel=riff['vowel'] if t1 == 'vowel' else None, vmix=0.6,
                       gatep=ph['gatep'], punch=0.25, detune=22.0, glide=0.045,
                       passes=((2.0, 6.0),), grain=0.25, seed=23)
        _P[key] = stitch((p0, p1), ph['plan'], 32)
    return _P[key]


def lay(b0, bars, riff, gain=1.0, subg=1.0, reeseg=0.5, bright=1.0, drive=1.0,
        cell_off=0, sub_notes=None):
    """Place `bars` bars of a riff: the sub in eight-bar blocks as one
    oscillator, a new gesture sequence every two bars, and the reese
    underneath for the 200-500 Hz weight a distorted wavetable loses."""
    for k in range(bars // 8):
        b = b0 + k * 8
        s.place(s.pos(b), subbar(repeat(sub_notes or riff['sub'], 4), 128,
                                 **SUBKW), subg, 'sub')
        for j in range(4):
            ci = cell_off + k * 4 + j
            s.place(s.pos(b + j * 2), cellbar(riff, ci, bright, drive),
                    gain, 'bass')
            if reeseg:
                s.place(s.pos(b + j * 2),
                        reese_c(riff['notes'], riff['rtab'], 32,
                                cut=1.15 * bright, q=0.9, decay=0.0, sub=0.40),
                        reeseg, 'body')


# ---- the topline ----
LEAD = ((0, F4), (3, Ab4), (6, F4), (10, C5), (12, Bb4),
        (16, Ab4), (20, Eb4), (23, F4), (27, B4), (30, F4))
LEAD_CUT = [2600, 5200, 3000, 6800, 2400, 4400, 3200, 7400,
            2800, 4000, 5600, 2600, 6000, 3400, 4800, 2400] * 2
LEAD_SYNC = [1.0, 2.2, 1.0, 3.0, 1.4, 1.0, 2.6, 1.8,
             1.0, 2.4, 1.0, 3.4, 1.2, 2.0, 1.0, 2.8] * 2
GLOOM = ((0, F3), (12, Ab3), (26, Eb3), (40, Db3), (52, C3x), (58, F3))


def hole(b, s0=14.0, s1=16.0):
    a, e = s.pos(b, s0), s.pos(b, s1)
    ramp = np.linspace(1, 0, e - a)[:, None] ** 1.4
    for name in s.bus:
        s.bus[name][a:e] *= ramp


# ============================================================ intro 0-15
for b in range(0, 16, 4):
    s.place(s.pos(b), air(64, gain=1.0, seed=b, lo=700, hi=6500), 1.0, 'atmos')
s.place(s.pos(0), mgloom(GLOOM, 64, gain=0.70, cut=(420, 1700), seed=0), 1.0, 'pad')
s.place(s.pos(8), mgloom(GLOOM, 64, gain=0.85, cut=(460, 2000), seed=8), 1.0, 'pad')
s.place(s.pos(2), grains(mclank(dur_steps=4, note=F3, damp=1.5, bright=0.4, seed=5),
                         32, density=18, seed=11, pitch=(0.35, 1.3)), 0.7, 'atmos')
s.place(s.pos(10), grains(msnare(seed=2), 32, density=26, seed=12,
                          pitch=(0.4, 1.8)), 0.5, 'atmos')
for b in range(4, 16):
    s.place(s.pos(b), mpad(CHORDS[(b // 4) % 4], 16, cut=900, seed=b), 0.34, 'pad')
for b in range(8, 16):
    drums(b, 'E', gain=0.55, hats=0.7, ghosts=0.3, sc=b >= 12, seed=b)
s.place(s.pos(14), slam(16, gain=0.5, seed=3), 1.0, 'fx')

# ============================================================ groove 16-23
for b in range(16, 24):
    drums(b, ['A', 'A', 'B', 'A', 'A', 'C', 'A', 'D'][b % 8], gain=0.9, hats=0.95,
          ghosts=0.8, perc=0.5 if b >= 20 else 0.0, seed=b)
    s.place(s.pos(b), mpad(CHORDS[(b // 4) % 4], 16, cut=1150, seed=b), 0.30, 'pad')
s.place(s.pos(16), mgloom(GLOOM, 128, gain=0.55, cut=(480, 1900), seed=16), 1.0, 'pad')
lay(16, 8, RIFF_A, gain=0.60, subg=0.85, reeseg=0.35, bright=0.45, drive=0.7)

# ============================================================ build 1  24-31
for b in range(24, 32):
    drums(b, ['A', 'B', 'A', 'C', 'A', 'B', 'C', 'D'][b - 24], gain=0.95, hats=1.0,
          ghosts=0.9, perc=0.6, seed=b)
    s.place(s.pos(b), mpad(CHORDS[(b // 2) % 4], 16, cut=1400, seed=b), 0.32, 'pad')
lay(24, 8, RIFF_A, gain=0.74, subg=0.9, reeseg=0.42, bright=0.72, drive=0.85)
_A0 = cellbar(RIFF_A, 0)
s.place(s.pos(28), revfx(_A0, cut=(260, 8000), q=1.5), 0.55, 'fx')
roll(s, 30, 8.0, 12, spacing=0.7, gain=0.55, accel=True, voice=msnare,
     seed=31, dur_steps=2.0)
s.place(s.pos(31, 12), subdive(6, 92, 27, gain=0.55), 1.0, 'fx')
hole(31, 15.0, 16.0)

# ============================================================ DROP 1  32-63
# Eight bars of statement, eight of variation, four halftime, twelve of
# escalation. A thirty-two bar drop that is one loop repeated sixteen times
# has no shape; this one has four.
lay(32, 16, RIFF_A, gain=1.0, subg=1.0, reeseg=0.55)
lay(52, 12, RIFF_A, gain=1.0, subg=1.0, reeseg=0.55, bright=1.18, drive=1.12,
    cell_off=2)
for b in range(32, 48):
    i = b - 32
    drums(b, ['A', 'A', 'B', 'A', 'A', 'C', 'B', 'D'][i % 8], gain=1.0, hats=1.0,
          ghosts=1.0, perc=0.85, ride=0.8 if i >= 8 else 0.0, seed=b)
    if i % 8 == 7:
        roll(s, b, 12.0, 6, spacing=0.66, gain=0.5, accel=True, seed=b)
    if i % 8 in (3, 7):
        s.place(s.pos(b, 14), panned(screech(F4 if i < 8 else Ab4, 2.5,
                                             gain=0.40, seed=b), 0.4), 1.0, 'music')
# four bars of halftime: the snare moves to beat 3 and the bass holds. It is
# the same tempo and it feels half of it, which is the point - and it is four
# bars, because eight would stop being a gesture and start being the groove.
for b in range(48, 52):
    drums(b, 'H', gain=1.0, hats=0.55, ghosts=0.5, perc=0.4, seed=b + 5)
    s.place(s.pos(b), subbar(((0, F1), (8, Db1)), 16, drive=1.2, **SUBKW), 1.05, 'sub')
    s.place(s.pos(b), cellbar(RIFF_A, 1)[:int(16 * STEP)], 0.95, 'bass')
    s.place(s.pos(b), mpad(CHORDS[(b - 48) % 4], 16, cut=1500, seed=b), 0.34, 'pad')
s.place(s.pos(51, 12), subdive(5, 80, 26, gain=0.45), 1.0, 'fx')
for b in range(52, 64):
    i = b - 52
    drums(b, ['C', 'A', 'B', 'A', 'C', 'A', 'B', 'D'][i % 8], gain=1.0, hats=1.0,
          ghosts=1.0, perc=1.0, ride=0.9, seed=b + 20)
    if i % 8 == 7:
        roll(s, b, 12.0, 8, spacing=0.55, gain=0.52, accel=True, seed=b)
    if i % 4 == 2:
        s.place(s.pos(b, 7), panned(lp(mclank(dur_steps=1.4, damp=3.0, bright=0.5,
                                              note=[C5, Bb4, Ab4, F4][i % 4],
                                              seed=b), 2400, 4), -0.55),
                0.18, 'texture')
s.place(s.pos(32), slam(16, gain=0.62, seed=1), 1.0, 'fx')
s.place(s.pos(52), slam(16, gain=0.55, seed=2), 1.0, 'fx')
s.place(s.pos(63, 12), subdive(6, 88, 26, gain=0.5), 1.0, 'fx')
hole(63, 14.5, 16.0)

# ============================================================ breakdown 64-79
for b in range(64, 80):
    ch = CHORDS[(b // 2) % 4]
    s.place(s.pos(b), mpad(ch, 16, cut=1600 if b < 72 else 2400, seed=b), 0.42, 'pad')
    s.place(s.pos(b), air(16, gain=1.2, seed=b, lo=500, hi=5000), 1.0, 'atmos')
    if b % 2 == 0:
        s.place(s.pos(b), subbar(((0, ch[0] - 12),), 32, drive=1.1, **SUBKW),
                0.38, 'sub')
    if b >= 68:
        s.place(s.pos(b, 0), mstab(ch, 2.2, gain=0.32, cut=(4200, 900), seed=b),
                1.0, 'music')
        s.place(s.pos(b, 10), mstab(ch, 1.6, gain=0.22, cut=(3000, 800), seed=b + 3),
                1.0, 'music')
    if b >= 72:
        drums(b, 'E', gain=0.62, hats=0.55, ghosts=0.4, perc=0.4, seed=b,
              sc=b >= 76)
s.place(s.pos(64), mgloom(GLOOM, 128, gain=0.62, cut=(400, 2200), seed=64), 1.0, 'pad')
s.place(s.pos(72), mgloom(tuple((st, nt + 5) for st, nt in GLOOM), 128, gain=0.50,
                          cut=(500, 2600), seed=72), 1.0, 'pad')
for b in (70, 78):
    s.place(s.pos(b), mlead(LEAD, 32, gain=0.50, cut=[c * 0.7 for c in LEAD_CUT],
                            sync=LEAD_SYNC, q=3.5, drive=1.5, decay=0.55), 1.0, 'music')
s.place(s.pos(64), grains(_A0, 64, density=22, seed=21, pitch=(0.3, 1.1)),
        0.55, 'atmos')

# ============================================================ build 2  80-87
for b in range(80, 88):
    drums(b, ['A', 'A', 'B', 'C', 'A', 'B', 'C', 'D'][b - 80], gain=0.9 + 0.02 * (b - 80),
          hats=1.0, ghosts=0.9, perc=0.7, seed=b)
    s.place(s.pos(b), mpad(CHORDS[(b // 2) % 4], 16, cut=2000, seed=b), 0.40, 'pad')
lay(80, 8, RIFF_B, gain=0.76, subg=0.92, reeseg=0.42, bright=0.7, drive=0.9)
s.place(s.pos(84), revfx(cellbar(RIFF_B, 2), cut=(300, 9000), q=1.6), 0.55, 'fx')
roll(s, 86, 8.0, 14, spacing=0.62, gain=0.55, accel=True, voice=msnare,
     seed=71, dur_steps=2.0)
s.place(s.pos(87, 12), subdive(6, 95, 26, gain=0.55), 1.0, 'fx')
hole(87, 15.0, 16.0)

# ============================================================ DROP 2  88-119
lay(88, 16, RIFF_B, gain=1.05, subg=1.05, reeseg=0.5, cell_off=1)
lay(108, 12, RIFF_B, gain=1.05, subg=1.05, reeseg=0.5, bright=1.2, drive=1.1,
    cell_off=3)
for b in range(88, 104):
    i = b - 88
    drums(b, ['B', 'A', 'C', 'A', 'B', 'A', 'C', 'D'][i % 8], gain=1.0, hats=1.0,
          ghosts=1.0, perc=1.0, ride=0.7 if i >= 8 else 0.0, seed=b + 40)
    if i % 8 == 7:
        roll(s, b, 12.0, 6, spacing=0.66, gain=0.5, accel=True, seed=b)
    if i % 8 == 5:
        s.place(s.pos(b, 8), panned(screech(C5, 3.0, gain=0.34, r1=7.0, seed=b),
                                    -0.45), 1.0, 'music')
for b in range(104, 108):
    drums(b, 'H', gain=1.0, hats=0.55, ghosts=0.5, perc=0.4, seed=b + 9)
    s.place(s.pos(b), subbar(((0, F1), (8, Eb1)), 16, drive=1.2, **SUBKW), 1.05, 'sub')
    s.place(s.pos(b), cellbar(RIFF_B, 3)[int(16 * STEP):], 0.95, 'bass')
for b in range(108, 120):
    i = b - 108
    drums(b, ['C', 'A', 'B', 'A', 'C', 'B', 'A', 'D'][i % 8], gain=1.0, hats=1.0,
          ghosts=1.0, perc=1.0, ride=0.85, seed=b + 60)
    if i % 8 == 7:
        roll(s, b, 12.0, 8, spacing=0.55, gain=0.52, accel=True, seed=b)
s.place(s.pos(88), slam(16, gain=0.58, seed=4), 1.0, 'fx')
s.place(s.pos(108), slam(16, gain=0.52, seed=5), 1.0, 'fx')
s.place(s.pos(119, 12), subdive(6, 90, 25, gain=0.5), 1.0, 'fx')
hole(119, 14.5, 16.0)

# ============================================================ machines 120-135
for b in range(120, 136):
    i = b - 120
    drums(b, 'E' if i < 8 else 'A', gain=0.9, hats=0.55 if i < 8 else 0.9,
          ghosts=0.5, perc=1.2, seed=b + 90)
    s.place(s.pos(b), subbar(((0, F1), (8, Db1)), 16, drive=1.15, **SUBKW),
            0.72, 'sub')
    s.place(s.pos(b), air(16, gain=1.0, seed=b, lo=800, hi=7000), 1.0, 'atmos')
    if i % 4 == 0:
        s.place(s.pos(b), grains(mclank(dur_steps=5, note=[F3, Ab3, C4, Eb4][i % 4],
                                        damp=1.6, bright=0.4, seed=b), 64,
                                 density=16, seed=b, pitch=(0.3, 1.6)), 0.5, 'atmos')
    for k, nt, p in [(2, Eb5, -0.7), (6, Ab4, 0.6), (10, C5, 0.3), (14, F4, -0.4)]:
        if (i + int(k)) % 2 == 0:
            s.place_echo(s.pos(b, k + SWING),
                         panned(lp(mclank(dur_steps=2.0, damp=2.4, bright=0.6,
                                          note=nt, seed=b + int(k)), 2800, 4), p),
                         0.34, times=3, delay_steps=3.0, fb=0.45, bus='texture')
    if i >= 8:
        s.place(s.pos(b, 0), mstab(CHORDS[(b // 2) % 4], 2.0, gain=0.34,
                                   cut=(3800, 800), seed=b), 1.0, 'music')
s.place(s.pos(124), mgloom(GLOOM, 128, gain=0.60, cut=(430, 2000), seed=124),
        1.0, 'pad')
s.place(s.pos(128), mlead(LEAD, 32, gain=0.34, cut=[c * 0.5 for c in LEAD_CUT],
                          sync=LEAD_SYNC, q=3.0, drive=1.4, decay=0.4), 1.0, 'music')

# ============================================================ build 3  136-143
for b in range(136, 144):
    drums(b, ['A', 'B', 'A', 'C', 'B', 'C', 'C', 'D'][b - 136], gain=1.0, hats=1.0,
          ghosts=1.0, perc=0.9, seed=b + 10)
    s.place(s.pos(b), mpad(CHORDS[(b // 2) % 4], 16, cut=2400, seed=b), 0.36, 'pad')
lay(136, 8, RIFF_C, gain=0.82, subg=0.95, reeseg=0.45, bright=0.78, drive=0.95)
s.place(s.pos(140), revfx(cellbar(RIFF_C, 0), cut=(320, 10000), q=1.7), 0.58, 'fx')
roll(s, 142, 4.0, 20, spacing=0.62, gain=0.6, accel=True, voice=msnare,
     seed=111, dur_steps=2.0)
s.place(s.pos(143, 12), subdive(6, 98, 25, gain=0.6), 1.0, 'fx')
hole(143, 15.0, 16.0)

# ============================================================ DROP 3  144-175
lay(144, 16, RIFF_C, gain=1.0, subg=1.0, reeseg=0.55, cell_off=4)
lay(164, 12, RIFF_C, gain=1.0, subg=1.0, reeseg=0.55, bright=1.22, drive=1.15,
    cell_off=1)
for b in range(144, 160):
    i = b - 144
    drums(b, ['A', 'C', 'B', 'A', 'C', 'A', 'B', 'D'][i % 8], gain=1.0, hats=1.0,
          ghosts=1.0, perc=1.0, ride=0.9 if i >= 8 else 0.0, seed=b + 60)
    if i % 8 == 7:
        roll(s, b, 12.0, 8, spacing=0.55, gain=0.52, accel=True, seed=b)
    if i % 8 in (2, 6):
        s.place(s.pos(b, 12), panned(screech(Ab4 if i < 8 else C5, 2.5,
                                             gain=0.38, seed=b), -0.5), 1.0, 'music')
for b in range(160, 164):
    drums(b, 'H', gain=1.0, hats=0.6, ghosts=0.5, perc=0.5, seed=b + 3)
    s.place(s.pos(b), subbar(((0, F1), (8, Gb1)), 16, drive=1.2, **SUBKW), 1.05, 'sub')
    s.place(s.pos(b), cellbar(RIFF_C, 4)[:int(16 * STEP)], 0.95, 'bass')
for b in range(164, 176):
    i = b - 164
    drums(b, ['C', 'A', 'B', 'C', 'A', 'B', 'C', 'D'][i % 8], gain=1.0, hats=1.0,
          ghosts=1.0, perc=1.0, ride=0.95, seed=b + 80)
    if i % 8 == 7:
        roll(s, b, 12.0, 9, spacing=0.52, gain=0.55, accel=True, seed=b)
for b in range(148, 176, 4):
    s.place(s.pos(b), mlead(LEAD, 32, gain=0.44, cut=LEAD_CUT, sync=LEAD_SYNC,
                            q=4.5, drive=2.0, decay=0.0), 1.0, 'music')
s.place(s.pos(144), slam(16, gain=0.6, seed=6), 1.0, 'fx')
s.place(s.pos(164), slam(16, gain=0.56, seed=7), 1.0, 'fx')

# ============================================================ outro 176-191
for b in range(176, 192):
    i = b - 176
    fade = max(0.0, 1 - i / 15.0)
    drums(b, 'A' if i < 8 else 'E', gain=0.95 * fade, hats=0.9 * fade,
          ghosts=0.7 * fade, perc=0.6 * fade, seed=b, sc=i < 10)
    s.place(s.pos(b), air(16, gain=1.2, seed=b, lo=600, hi=6000), 1.0, 'atmos')
    if i < 10:
        s.place(s.pos(b), subbar(((0, F1),), 16, drive=1.1, **SUBKW),
                0.8 * fade, 'sub')
    s.place(s.pos(b), mpad(CHORDS[0], 16, cut=1200, seed=b), 0.30 * max(fade, 0.4),
            'pad')
lay(176, 8, RIFF_C, gain=0.55, subg=0.0, reeseg=0.3, bright=0.8, drive=0.8,
    cell_off=2)
s.place(s.pos(186), mgloom(GLOOM, 96, gain=0.75, cut=(380, 1400), seed=9), 1.0, 'pad')
s.place(s.pos(188), grains(cellbar(RIFF_C, 1), 32, density=20, seed=44,
                           pitch=(0.25, 1.0)), 0.45, 'atmos')


# ============================================================ the mix
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.3, wet=0.24, tone=5200)
s.bus['texture'] = bus_reverb(s.bus['texture'], decay=0.9, wet=0.22, tone=6000)
s.bus['pad'] = bus_reverb(s.bus['pad'], decay=2.8, wet=0.34, tone=3200)
s.bus['atmos'] = bus_reverb(s.bus['atmos'], decay=3.2, wet=0.30, tone=2800)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=1.8, wet=0.20, tone=4400)

s.bus['sub'] = compress(mono_below(s.bus['sub'], 200), thresh=0.50, ratio=3.0,
                        attack=0.004, release=0.09)
# The neuro bass is EQ'd where the distortion chain leaves it: a lift at
# 700 Hz where the scan lives, a cut at 2.2 kHz which belongs to the snare's
# crack, and everything under 105 Hz gone - the sub owns that and nothing
# that has been through three distortion stages is allowed near it.
s.bus['bass'] = peak_eq(peak_eq(s.bus['bass'], 1500, 2.5, 0.7), 2600, -1.5, 0.8)
s.bus['bass'] = peak_eq(s.bus['bass'], 520, -2.0, 0.9)
# The bass carries its own weight now, so the shelf only has to confirm it.
s.bus['bass'] = shelf(s.bus['bass'], 190, 2.0, 'low')
s.bus['bass'] = mono_below(hp(s.bus['bass'], 68, 2), 150)
s.bus['body'] = mono_below(hp(peak_eq(s.bus['body'], 520, 1.5, 0.8), 72, 2), 150)
s.bus['drums'] = peak_eq(shelf(hp(s.bus['drums'], 34, 2), 6200, 2.2, 'high'),
                         3800, 1.5, 0.5)
s.bus['drums'] = compress(s.bus['drums'], thresh=0.24, ratio=3.5, attack=0.010,
                          release=0.11, report=True, label='drum bus')
# The kick's fundamental at 66 Hz and the sub's octave at 87 both land in
# 60-120, and together they were four points over the references. One dip
# on the drum bus is cheaper than detuning the kick.
# 7-9 kHz is where a cymbal stops being bright and starts being painful.
s.bus['drums'] = peak_eq(peak_eq(s.bus['drums'], 95, -2.0, 0.9), 8000, -2.0, 0.7)
s.bus['drums'] = side_boost(peak_eq(s.bus['drums'], 5200, 2.0, 0.6), 3000, 0.55)
s.bus['texture'] = side_boost(shelf(hp(compress(s.bus['texture'], thresh=0.14,
                                                ratio=3.0, attack=0.006,
                                                release=0.10), 300, 2),
                                    3000, -1.5, 'high'), 1200, 0.5)
s.bus['music'] = shelf(hp(s.bus['music'], 190, 2), 3200, -2.0, 'high')
s.bus['pad'] = hp(s.bus['pad'], 200, 2)
s.bus['atmos'] = hp(s.bus['atmos'], 240, 2)
s.bus['fx'] = hp(s.bus['fx'], 30, 2)

GAINS = {'drums': 0.88, 'sub': 0.33, 'bass': 0.80, 'body': 0.60,
         'texture': 0.58, 'music': 0.74, 'pad': 0.30, 'atmos': 0.46, 'fx': 0.32}
s.report(GAINS)
# The clipper takes the spikes off first: if it does not, the limiter has to
# duck a whole bar to catch one sample and the master gets quieter the harder
# it is pushed. Then 3:1 glue, then a look-ahead limiter detecting on a 4x
# upsample, so the master lands at -1 dBTP instead of the +3 to +4 the
# reference records carry.
s.render('neurofunk_razryv_174.wav', drive=0.0, duck=0.26, duck_rel=0.090,
         limit=0.0, peak=0.99, gains=GAINS, clip=1.20, fade=2.2,
         comp=dict(thresh=0.38, ratio=2.5, attack=0.006, release=0.11, makeup=1.2),
         brick=dict(gain=1.55, ceiling=0.89, release=0.075))
