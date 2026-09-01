"""KACHAY - big beat at 131 BPM in A Dorian. Fatboy Slim's corner of the
genre: a funk break played by a real kit, a fuzz bass riff, a 303, an organ
through a Leslie, and every one of them crushed to 12 bits and squashed until
the room breathes between the hits.

Not techno, and one thing borrowed from it: the kick is on all four quarters,
underneath the break rather than instead of it. That is the "Right Here Right
Now" trick - the break carries the swagger, the quarters carry the room, and
at 131 BPM a break left on its own halves the felt pulse and the record goes
slack. Everything else here is 1998: harmony is one Dorian vamp, the riff is
the song, and the arrangement is a filter opening.

    intro | beat | groove | breakdown | build | DROP | break | build | FINAL | outro
    0       8      16       32          40      48     80      88      96      128

A Dorian: Am7 for two bars, D9 for two. The D is the whole point of the mode -
it is the major IV, the natural 6th made audible, and it is what stops this
sounding like a minor-key rave record.
"""
import numpy as np
from skanklib import *

np.random.seed(131)

# ---- the material ----
# One four-bar cycle for the whole record: Am7 Am7 D9 D9.
ORGAN = [(64, 67, 69, 72), (64, 67, 69, 72),       # E G A C
         (64, 66, 69, 72), (64, 66, 69, 72)]       # E F# A C - one voice moves
HORN  = [(64, 67, 72), (64, 67, 72), (66, 69, 72), (66, 69, 72)]
KICK_TUNE = 54.6                                   # near A1; the floor, not a bass note

# The riff. Steps 0/3/6 is the tresillo, and the last hit of every bar is an
# approach note into the next root - which is the entire difference between a
# bass part and a bass line.
RIFF = [
    ((0, 33), (3, 33), (6, 36), (8, 33), (11, 40), (14, 39)),   # A A C A E Eb
    ((0, 33), (3, 33), (6, 36), (8, 38), (10, 40), (13, 43), (15, 40)),
    ((0, 38), (3, 38), (6, 42), (8, 38), (11, 45), (14, 37)),   # D D F# D A C#
    ((0, 38), (3, 38), (6, 42), (8, 45), (11, 42), (14, 40)),   # ...E back to A
]

# The 303. (step, midi, accent, slide). Root-heavy with three reaches per bar:
# a line that moves all the time is a solo, and a 303 is a hook. It sits an
# octave above the bass riff on purpose - acid house puts its 303 in the sub,
# but there is already a fuzz bass down there, and two square-ish sources in
# one octave make mud, not weight.
ACID = [
    ((0, 57, 1, 0), (2, 57, 0, 0), (3, 64, 0, 1), (4, 57, 0, 0), (6, 60, 1, 0),
     (7, 57, 0, 0), (8, 57, 0, 0), (10, 67, 1, 0), (11, 64, 0, 1), (12, 57, 0, 0),
     (14, 55, 0, 0), (15, 57, 0, 0)),
    ((0, 57, 1, 0), (2, 69, 0, 0), (3, 57, 0, 1), (6, 60, 0, 0), (8, 57, 1, 0),
     (10, 64, 0, 0), (11, 57, 0, 1), (13, 62, 0, 0), (14, 60, 0, 0), (15, 57, 0, 0)),
    ((0, 62, 1, 0), (2, 62, 0, 0), (3, 69, 0, 1), (4, 62, 0, 0), (6, 66, 1, 0),
     (7, 62, 0, 0), (8, 62, 0, 0), (10, 57, 1, 0), (12, 62, 0, 0), (14, 60, 0, 0)),
    ((0, 62, 1, 0), (2, 74, 0, 0), (3, 62, 0, 1), (6, 66, 0, 0), (8, 62, 1, 0),
     (10, 69, 0, 0), (11, 62, 0, 1), (14, 64, 0, 0), (15, 57, 0, 0)),
]

# The hook: two bars of syllables. It is not a word in any language - it is
# the shape of one, which is all a chopped vocal ever is once the third slice
# has been moved. Consonants carry the rhythm, vowels carry the pitch.
HOOK = [
    [(0, 69, 2.0, ('uh', 'ah'), 'k'), (2, 69, 1.0, ('ah', 'ah'), ''),
     (3, 72, 2.0, ('oh', 'ah'), 'n'), (6, 69, 2.0, ('ah', 'ee'), ''),
     (8, 67, 2.0, ('eh', 'ah'), 'h'), (11, 69, 2.0, ('ah', 'oh'), 'n'),
     (14, 64, 3.0, ('ah', 'uh'), 'ch')],
    [(0, 72, 2.0, ('ah', 'ee'), 'k'), (3, 74, 2.0, ('ee', 'ah'), 't'),
     (6, 72, 1.5, ('ah', 'ah'), ''), (8, 69, 2.0, ('oh', 'ah'), 'h'),
     (10, 67, 2.0, ('ah', 'eh'), 'r'), (13, 69, 3.0, ('eh', 'ah'), 'sh')],
]

# ---- the grooves ----
BREAK = {                                    # the main break, two bars
    'kick':  ('x---x---x---x---', 'x---x---x---x---'),
    'snare': ('----x-------x---', '----x-------x-+-'),
    'ghost': ('..-...-..-.-..-.', '..-...-.-..-..-.'),
    'hat':   ('x-+-x-+-x-+-x-+-', 'x-+-x-+-x-+-x-++'),
    'ohat':  ('--------o-------', '----------------'),
    'tamb':  ('--+---+---+---+-', '--+---+---+---+-'),
}
STRIPPED = {                                 # the same floor, half the hands
    'kick':  'x---x---x---x---',
    'snare': '----x-------x---',
    'hat':   'x---x---x---x---',
}
LOOSE = {                                    # the break with the quarters gone
    'snare': ('----x-------x---', '----x---x---x-+-'),
    'ghost': ('..-...-..-.-..-.', '..-...-.-..-..-.'),
    'hat':   'x-+-x-+-x-+-x-+-',
    'tamb':  '--+---+---+---+-',
}
BIG = {                                      # the drop: ride instead of hats,
    'kick':  ('x---x---x---x---', 'x---x---x--xx---'),   # and the room opens
    'snare': ('----x-------x---', '----x---.---x-+-'),
    'ghost': ('..-...-..-.-..-.', '..-.-.-.-..-..-.'),
    'hat':   ('x-+-x-+-x-+-x-+-', 'x-+-x-+-x-+-x-++'),
    'ride':  ('+-+-+-+-+-+-+-+-', '+-+-+-+-+-+-+-+-'),
    'ohat':  ('--------o-------', '------------o---'),
    'tamb':  ('--+---+---+---+-', '--+---+---+---+-'),
    'clap':  ('----x-------x---', '----x-------x---'),
}

s = Session(144, tail=3.0)

# ---- the parts ----
_ORGAN = {}


def organ(b, bars=1, gain=1.0, hits=None, cutoff=None, rate=6.4, click=1.0):
    """The tonewheels never stop; only the gate moves. One render per chord
    is reused for the whole record, which is not a shortcut - it is what
    makes consecutive stabs phase-continuous instead of flickering."""
    key = (b % 4, bars, round(rate, 2), click)
    if key not in _ORGAN:
        raw = organbar(tuple(midi(n) for n in ORGAN[b % 4]), 16 * bars,
                       click=click, seed=b % 4)
        _ORGAN[key] = leslie(raw, rate=rate, drum_rate=rate * 0.84)
    seg = _ORGAN[key]
    if hits:
        seg = chop(seg, hits)
    if cutoff:
        seg = lp(seg, cutoff)
    s.place(s.pos(b), seg, gain, 'keys')


STABS = [(2, 1.5), (6, 1.0), (7, 0.5), (10, 1.5), (14, 1.0), (15, 0.5)]
STABS_B = [(2, 1.5), (6, 1.0), (9, 0.5), (10, 1.0), (14, 2.0)]


def bass(b, gain=1.0, fuzz=5.5, cut=2400, sub=1.0, grind=1.0, **kw):
    s.place(s.pos(b), fuzzbar(RIFF[b % 4], gain=gain, fuzz=fuzz, cut=cut,
                              sub=sub, grind=grind, take=b % 4, **kw),
            1.0, 'bass')


# The 303 is played by turning knobs, not by writing notes: the sixteen steps
# never change for the whole record and the cutoff, resonance, envelope decay
# and overdrive walk continuously underneath them. Every call is one bar's
# worth of a section-long move, sampled at both ends of the bar so the render
# joins at the bar line instead of stepping there.
def acid(b, b0, b1, cut, pk, res, dec, drv, lvl, curve=1.0):
    c0, c1 = ramp(b, b0, b1, *cut, curve=curve, geom=True)
    p0, p1 = ramp(b, b0, b1, *pk, curve=curve, geom=True)
    g0, g1 = ramp(b, b0, b1, *lvl, curve=curve)
    s.place(s.pos(b), acidbar(ACID[b % 4], cutoff=c0, cut1=c1, peak=p0, peak1=p1,
                              res=round(ramp(b, b0, b1, *res, curve=curve)[0], 2),
                              decay=round(ramp(b, b0, b1, *dec, curve=curve)[0], 4),
                              drive=round(ramp(b, b0, b1, *drv, curve=curve)[0], 2),
                              gain=g0, gain1=g1), 1.0, 'music')


def vox(b, gain=1.0, transpose=0, cell=None):
    voxline(s, b, HOOK[(b // 1 if cell is None else cell) % 2], gain=gain,
            transpose=transpose, seed=b * 13)


def hornhit(b, steps_=(6, 14), gain=1.0, dur=3.0, bright=1.0):
    for st in steps_:
        s.place(s.pos(b, st), horns(tuple(midi(n) for n in HORN[b % 4]), dur,
                                    bright=bright, seed=b % 4), gain, 'horn')


# ================= intro: 0-7 - the needle, then the loop =================
s.place(s.pos(0), crackle(8 * 16, gain=0.9), 1.0, 'fx')
for b in range(0, 8):
    ph = b - 0
    if b >= 2:
        kitbar(s, b, LOOSE if b < 4 else STRIPPED, gain=0.42 + 0.09 * ph,
               swing=0.56, seed=b, hats=0.8, register=b >= 4)
    if b >= 4:
        bass(b, gain=0.55 + 0.10 * (b - 4), fuzz=3.2, cut=900, grind=0.4)
    if b >= 6:
        organ(b, gain=0.30, hits=STABS, cutoff=1400)
s.place(s.pos(1, 8), scratch(syl(69, 4, ('ah', 'ee'), 'k', gain=1.1),
                             cycles=2.0, depth=2.1), 0.7, 'fx')
s.place(s.pos(3, 12), scratch(syl(72, 4, ('oh', 'ah'), 'ch', gain=1.1),
                              cycles=3.0, depth=1.7), 0.75, 'fx')
s.place(s.pos(7), bcrash(16, gain=0.5), 1.0, 'drums')
s.place(s.pos(7), stab_riser(16, gain=0.7, f0=260, f1=3400), 1.0, 'fx')
fill(s, 7, 'roll', gain=0.7, seed=7)

# ================= the beat: 8-15 =================
for b in range(8, 16):
    ph = b - 8
    kitbar(s, b, BREAK, gain=0.92, swing=0.56, seed=b, tune=KICK_TUNE)
    bass(b, gain=0.95, fuzz=5.0, cut=1900)
    organ(b, gain=0.34 + 0.03 * ph, hits=STABS)
    if b >= 12:
        vox(b, gain=0.42 + 0.08 * (b - 12), cell=b)
s.place(s.pos(8), bcrash(20, gain=0.7), 1.0, 'drums')
s.place(s.pos(11, 12), scratch(syl(74, 4, ('ee', 'ah'), 't', gain=1.1),
                               cycles=2.5, depth=1.9), 0.7, 'fx')
fill(s, 15, 'stutter', gain=0.85, seed=15)

# ================= groove: 16-31 - the record proper =================
for b in range(16, 32):
    ph = b - 16
    kitbar(s, b, BREAK, gain=0.86, swing=0.56, seed=b, tune=KICK_TUNE,
           fat=1.0 + 0.15 * (ph >= 8))
    bass(b, gain=0.88, fuzz=5.5, cut=2200 + 40 * ph)
    organ(b, gain=0.40, hits=STABS if ph % 4 != 3 else STABS_B)
    vox(b, gain=0.62, cell=b)
    if ph >= 8:
        acid(b, 24, 32, cut=(205, 520), pk=(950, 2400), res=(0.30, 1.35),
             dec=(0.050, 0.110), drv=(2.5, 3.2), lvl=(0.42, 0.60))
s.place(s.pos(16), bcrash(24, gain=0.8), 1.0, 'drums')
s.place(s.pos(24), bcrash(20, gain=0.7), 1.0, 'drums')
s.place_echo(s.pos(23, 12), syl(76, 3, ('ah', 'ee'), 'sh', gain=0.9), 0.6,
             times=3, delay_steps=3.0, fb=0.5, bus='fx')
fill(s, 23, 'toms', gain=0.85, seed=23)
fill(s, 31, 'roll', gain=0.9, seed=31)

# ================= breakdown: 32-39 - the drums leave, the organ stays =====
for b in range(32, 40):
    ph = b - 32
    organ(b, bars=1, gain=0.55, rate=1.1 if ph < 4 else 6.4, click=0.4)
    if ph >= 2:
        acid(b, 34, 48, cut=(520, 2800), pk=(2400, 7800), res=(1.35, 6.20),
             dec=(0.110, 0.230), drv=(3.2, 6.4), lvl=(0.60, 0.94), curve=1.25)
    if ph >= 4:
        kitbar(s, b, LOOSE, gain=0.40 + 0.08 * (ph - 4), swing=0.56, seed=b,
               hats=0.7, ghosts=0.8)
    if ph >= 6:
        bass(b, gain=0.60, fuzz=3.0, cut=760, grind=0.3)
for b, note in ((32, 69), (34, 72), (36, 76), (38, 74)):
    s.place_echo(s.pos(b, 4), syl(note, 4, ('oh', 'ah'), 'h', gain=1.0), 0.62,
                 times=4, delay_steps=3.0, fb=0.55, bus='fx')
s.place(s.pos(32), crackle(8 * 16, gain=0.7), 1.0, 'fx')

# ================= build: 40-47 =================
for b in range(40, 48):
    ph = b - 40
    kitbar(s, b, BREAK if ph < 6 else STRIPPED, gain=0.72 + 0.05 * ph,
           swing=0.56, seed=b, tune=KICK_TUNE, hats=0.9 + 0.1 * ph)
    bass(b, gain=0.80 + 0.03 * ph, fuzz=4.5 + 0.3 * ph, cut=1400 + 220 * ph)
    acid(b, 34, 48, cut=(520, 2800), pk=(2400, 7800), res=(1.35, 6.20),
         dec=(0.110, 0.230), drv=(3.2, 6.4), lvl=(0.60, 0.94), curve=1.25)
    organ(b, gain=0.40, hits=STABS)
    if ph >= 4:
        vox(b, gain=0.55, cell=b)
s.place(s.pos(44), stab_riser(64, gain=0.85, f0=240, f1=6200), 1.0, 'fx')
s.place(s.pos(46), bcrash(16, gain=0.5), 1.0, 'drums')
fill(s, 47, 'roll', gain=1.0, seed=47)
s.place(s.pos(47, 11), reverse_crash(10, gain=0.85), 1.0, 'fx')
s.place(s.pos(47, 13), subdrop(6, f0=180, f1=32, gain=0.75, drive=1.6), 1.0, 'fx')

# ================= DROP: 48-79 - thirty-two bars, and it moves every four ==
for b in range(48, 80):
    ph = b - 48
    kitbar(s, b, BIG if ph >= 8 else BREAK, gain=0.98, swing=0.56, seed=b,
           tune=KICK_TUNE, fat=1.15)
    bass(b, gain=1.00, fuzz=6.0, cut=2600,
         wah=1.0 if 16 <= ph < 24 else 0.0, wah_lo=340, wah_hi=2600)
    acid(b, 48, 80, cut=(620, 1750), pk=(2700, 5400), res=(1.40, 3.50),
         dec=(0.110, 0.180), drv=(3.0, 4.6), lvl=(0.56, 0.74))
    thin = 24 <= ph < 28                       # four bars with the lid back on
    if ph % 8 != 7 and not thin:
        organ(b, gain=0.44, hits=STABS if ph % 4 != 3 else STABS_B)
    vox(b, gain=0.66 if ph < 24 else 0.74, cell=b)
    if ph >= 8 and not thin:
        hornhit(b, steps_=(6, 14) if ph % 4 != 3 else (6, 12, 14),
                gain=0.55 if ph < 16 else 0.62)
for b in (48, 56, 64, 72):
    s.place(s.pos(b), bcrash(24, gain=0.75), 1.0, 'drums')
s.place(s.pos(76), bcrash(20, gain=0.7), 1.0, 'drums')
for b, kind in ((51, 'stutter'), (55, 'roll'), (59, 'toms'), (63, 'roll'),
                (67, 'stutter'), (71, 'kicks'), (75, 'toms'), (79, 'roll')):
    fill(s, b, kind, gain=0.9, seed=b)
s.place_echo(s.pos(62, 12), syl(76, 3, ('ah', 'ee'), 'sh', gain=0.95), 0.6,
             times=3, delay_steps=3.0, fb=0.5, bus='fx')
s.place(s.pos(70, 12), scratch(syl(72, 4, ('ah', 'oh'), 'k', gain=1.1),
                               cycles=3.0, depth=2.0), 0.75, 'fx')

# ================= the break: 80-87 - everything stops but the hands ======
for b in range(80, 88):
    ph = b - 80
    if ph < 4:
        kitbar(s, b, {'hat': 'x-+-x-+-x-+-x-+-', 'tamb': '--+---+---+---+-',
                      'clap': '----x-------x---'}, gain=0.75, swing=0.56, seed=b)
        organ(b, gain=0.50, rate=1.1, click=0.3, cutoff=3200)
    else:
        kitbar(s, b, LOOSE, gain=0.60 + 0.10 * (ph - 4), swing=0.56, seed=b,
               hats=0.9)
        organ(b, gain=0.45, hits=STABS)
        bass(b, gain=0.70 + 0.09 * (ph - 4), fuzz=4.0, cut=1300, grind=0.5)
for b, note in ((80, 72), (82, 69), (84, 76), (86, 74)):
    s.place_echo(s.pos(b, 2), syl(note, 4, ('ah', 'ee'), 'ch', gain=1.0), 0.60,
                 times=4, delay_steps=3.0, fb=0.55, bus='fx')
s.place(s.pos(83, 8), tape_stop(organbar(tuple(midi(n) for n in ORGAN[3]), 8,
                                         gain=0.9), stop_s=0.7), 0.55, 'fx')

# ================= build 2: 88-95 - bigger, and it high-passes itself =====
for b in range(88, 96):
    ph = b - 88
    kitbar(s, b, BREAK, gain=0.88 + 0.04 * ph, swing=0.56, seed=b,
           tune=KICK_TUNE, hats=1.0 + 0.08 * ph)
    bass(b, gain=0.92, fuzz=5.5 + 0.2 * ph, cut=1800 + 200 * ph)
    acid(b, 88, 96, cut=(1000, 2400), pk=(3600, 6600), res=(2.10, 4.60),
         dec=(0.130, 0.200), drv=(3.4, 5.4), lvl=(0.60, 0.84), curve=1.2)
    organ(b, gain=0.42, hits=STABS)
    vox(b, gain=0.62, cell=b)
    if ph >= 4:
        hornhit(b, steps_=(6, 14), gain=0.5 + 0.06 * (ph - 4))
s.place(s.pos(92), stab_riser(64, gain=0.95, f0=220, f1=7000), 1.0, 'fx')
fill(s, 95, 'roll', gain=1.0, seed=95)
s.place(s.pos(95, 10), reverse_crash(12, gain=0.95), 1.0, 'fx')
s.place(s.pos(95, 12), subdrop(8, f0=190, f1=30, gain=0.85, drive=1.7), 1.0, 'fx')

# ================= FINAL: 96-127 - the same drop with the lid off ========
for b in range(96, 128):
    ph = b - 96
    kitbar(s, b, BREAK if 24 <= ph < 28 else BIG, gain=1.05, swing=0.56,
           seed=b, tune=KICK_TUNE, fat=1.2)
    bass(b, gain=1.08, fuzz=6.5, cut=2800,
         wah=2.0 if 8 <= ph < 16 else 0.0, wah_lo=320, wah_hi=2800)
    acid(b, 96, 128, cut=(1050, 2500), pk=(3900, 7200), res=(2.30, 5.00),
         dec=(0.140, 0.210), drv=(3.6, 5.8), lvl=(0.64, 0.82))
    thin = 24 <= ph < 28
    if ph % 8 != 7 and not thin:
        organ(b, gain=0.46, hits=STABS if ph % 4 != 3 else STABS_B)
    vox(b, gain=0.74, transpose=12 if 16 <= ph < 24 else 0, cell=b)
    if not thin:
        hornhit(b, steps_=(6, 14) if ph % 4 != 3 else (2, 6, 12, 14),
                gain=0.66, bright=1.15)
for b in (96, 104, 112, 120):
    s.place(s.pos(b), bcrash(28, gain=0.8), 1.0, 'drums')
s.place(s.pos(124), bcrash(24, gain=0.75), 1.0, 'drums')
for b, kind in ((99, 'stutter'), (103, 'roll'), (107, 'toms'), (111, 'kicks'),
                (115, 'roll'), (119, 'stutter'), (123, 'toms'), (127, 'roll')):
    fill(s, b, kind, gain=0.95, seed=b)
s.place(s.pos(110, 12), scratch(syl(76, 4, ('ee', 'ah'), 't', gain=1.15),
                                cycles=3.5, depth=2.2), 0.8, 'fx')
s.place_echo(s.pos(118, 12), syl(79, 3, ('ah', 'ee'), 'sh', gain=1.0), 0.62,
             times=3, delay_steps=3.0, fb=0.5, bus='fx')

# ================= outro: 128-143 - subtract, then the needle lifts ======
for b in range(128, 144):
    ph = b - 128
    kitbar(s, b, BIG if ph < 4 else (BREAK if ph < 10 else STRIPPED),
           gain=1.0 - 0.05 * ph, swing=0.56, seed=b, tune=KICK_TUNE,
           hats=1.0 - 0.05 * ph)
    if ph < 12:
        bass(b, gain=1.0 - 0.07 * ph, fuzz=6.0 - 0.25 * ph, cut=2600 - 170 * ph)
    if ph < 8:
        acid(b, 128, 136, cut=(2500, 320), pk=(7200, 1500), res=(5.00, 0.90),
             dec=(0.210, 0.070), drv=(5.8, 2.6), lvl=(0.78, 0.16))
        organ(b, gain=0.44 - 0.04 * ph, hits=STABS)
        vox(b, gain=0.70 - 0.08 * ph, cell=b)
    elif ph < 12:
        organ(b, gain=0.28, hits=STABS_B, cutoff=2600 - 240 * (ph - 8))
s.place(s.pos(128), bcrash(28, gain=0.75), 1.0, 'drums')
s.place(s.pos(136), bcrash(20, gain=0.5), 1.0, 'drums')
s.place(s.pos(128), crackle(16 * 16, gain=0.8), 1.0, 'fx')
s.place(s.pos(139, 12), rewind(organbar(tuple(midi(n) for n in ORGAN[3]), 8,
                                        gain=0.9), accel=3.2), 0.5, 'fx')
s.place(s.pos(143), tape_stop(bkick(8, tune=KICK_TUNE, gain=1.0), stop_s=0.5),
        0.7, 'drums')

# ---- the two holes ----
# Everything but the fx bus stops for the last three sixteenths of the bar
# before each drop. The riser and the reverse crash ring on through the hole,
# so what the ear gets is not silence, it is the floor disappearing.
gap(s, 47, st=13.0, length=3.0)
gap(s, 95, st=12.5, length=3.5)

# ---- the room, the sampler, and the compressor that makes it a record ----
# The order matters. Crush first, because the sampler saw a clean loop and the
# 12-bit error has to be made of the drums; then the room, because the room
# was there before the sampler and a reverb on top of quantisation noise
# sounds like a plugin; then squash, because the pump has to breathe around
# the whole thing including its tail. Release is a sixteenth at 131.
s.bus['drums'] = crush(s.bus['drums'], bits=11, sr_div=2, pre=13500)
s.bus['drums'] = s.bus['drums'] + room(s.bus['drums'], decay=0.62, wet=0.22,
                                       tone=5400, hp_hz=260)
s.bus['drums'] = squash(s.bus['drums'], thresh=0.33, ratio=5.0, attack=0.016,
                        release=0.1145, mix=0.62, report='drums')
s.bus['drums'] = shelf(sat(s.bus['drums'], 1.30), 8000, -1.5)
s.bus['drums'] = peak_eq(s.bus['drums'], 235, -2.2, width=0.45)
s.bus['drums'] = mono_below(s.bus['drums'], 110)

s.bus['bass'] = squash(s.bus['bass'], thresh=0.38, ratio=3.5, attack=0.020,
                       release=0.1145, mix=0.5, report='bass')
s.bus['bass'] = peak_eq(s.bus['bass'], 215, -2.8, width=0.55)
s.bus['bass'] = mono_below(s.bus['bass'], 130)

s.bus['music'] = squash(s.bus['music'], thresh=0.26, ratio=5.0, attack=0.012,
                        release=0.086, mix=0.8)
s.bus['music'] = crush(s.bus['music'], bits=12)
s.bus['keys'] = crush(s.bus['keys'], bits=11)
s.bus['keys'] = peak_eq(s.bus['keys'], 620, 2.2, width=0.6)
s.bus['keys'] = reverb(s.bus['keys'], decay=1.3, wet=0.16, tone=5600)[:s.total]
s.bus['horn'] = reverb(s.bus['horn'], decay=1.5, wet=0.22, tone=5000)[:s.total]
s.bus['vox'] = crush(s.bus['vox'], bits=11, sr_div=2, pre=12000)
s.bus['vox'] = peak_eq(hp(s.bus['vox'], 170, order=2), 900, 2.4, width=0.6)
s.bus['vox'] = reverb(s.bus['vox'], decay=1.4, wet=0.20, tone=5400)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=2.2, wet=0.28, tone=4800)[:s.total]

# The sixteen-bar filter opening, done to the buses rather than to a synth.
# In this genre that automation is the arrangement: the intro and the build
# are the same parts under a cutoff that is somewhere else.
for bus in ('drums', 'bass', 'keys'):
    sweep_bars(s.bus[bus], 0, 8, 300, 16000, curve=0.55)
    sweep_bars(s.bus[bus], 40, 48, 700, 16000, curve=1.6)
    sweep_bars(s.bus[bus], 88, 96, 900, 16000, curve=1.8)
sweep_bars(s.bus['drums'], 143.4, 144.0, 12000, 400, curve=1.0)

# The 303 is a lead, not a second kick: it was measuring louder than both the
# drums and the bass, which is why the whole record read as a drone with
# percussion on it. Drums first, bass under them, everything else beneath.
GAINS = {'drums': 0.74, 'bass': 0.48, 'music': 0.32, 'keys': 0.60,
         'horn': 0.62, 'vox': 0.62, 'fx': 0.46}
s.report(GAINS)
s.render('bigbeat_kachay_131.wav', drive=0.75, duck=0.16, clip=1.20, limit=0.90,
         peak=0.86, fade=1.6, gains=GAINS)
