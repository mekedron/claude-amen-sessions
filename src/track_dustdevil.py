"""Dust Devil (~2:55, 96 bars @132) - desert blues-rock western, drop D.

Two things that do not obviously belong together: a swaggering drop-D blues
riff played in unison by guitar and bass, and a spaghetti western - tremolo
twang in a spring tank, a whistled theme, a harmon-muted trumpet, and the
Andalusian cadence, which is the four chords every western score has used
since 1964 because they descend and never resolve until you let them.

The riff is D blues (D F G Ab A C - the Ab is the flat five and it is a
passing note, never a landing). The choruses leave the blues and drop onto
i - bVII - bVI - V, and over that V the whistle plays C# instead of C: one
note, and the desert turns Spanish. That is the whole trick.

  b0-7     the desert: wind, one tremolo chord in a spring tank, the theme
  b8-15    the riff arrives, guitar and bass in unison, tambourine
  b16-31   verse 1: full band, the swagger
  b32-39   the lift: chords open out, handclaps, twang answering
  b40-55   chorus: Dm - C - Bb - A, whistle and trumpet on the theme
  b56-71   verse 2, the twang taking the gaps between riff phrases
  b72-79   the standoff: everything gone but wind, whistle and one held note
  b80-95   last chorus: the gallop underneath it, everything on top

Reused deliberately, from the punk module and re-tuned for this piece rather
than taken as-is: the Karplus-Strong string and the amp (`gtr`, `mute`) at
`heavy=0.55` - half the drop-D compensation the hardcore track needs, because
this guitar has to stay bright enough to sound like a blues riff and not a
wall; `bassbar`, whose whole-bar continuous oscillator is what lets the riff's
bass slide instead of restarting; and the acoustic kit re-tuned softer and
lower (kick 66, snare 186 against the hardcore track's 62/198) because a lope
needs a drum that decays, not one that cracks. Everything else - the twang,
the spring tank, the whistle, the open trumpet, the tambourine, the claps, the
woodblock gallop and the wind - is new, in `westernlib.py`.
"""
import numpy as np
from westernlib import *

rng = np.random.default_rng(41)
np.random.seed(41)
s = Session(96, tail=4.0)

# ---- harmony -----------------------------------------------------------
D, Eb, F, G, Ab, A, Bb, C = 38, 39, 41, 43, 44, 45, 46, 48
CHORD_G = [D, C, Bb, A]                     # i bVII bVI V - the Andalusian
CHORD_B = [38, 36, 34, 33]                  # and the bass walking down under it
HEAVY = 0.55
SPREAD = 0.82
SLIP = int(0.004 * SR)
SWING = 0.545                               # a lope, not a shuffle

def swing(st):
    """delay the offbeat sixteenths only - the kick and snare stay put"""
    return st + ((SWING - 0.5) * 2 if int(st) % 2 else 0.0)

# The riff. Two bars, D blues, and the rhythm is the half of it you could
# clap: hits on 0, 3, 6, 8, 12, 14 - never on beat 2, which is the hole the
# whole thing swaggers around.
RIFF_A = ((0, D, 3), (3, D, 1), (6, F, 2), (8, G, 3), (12, F, 2), (14, D, 2))
RIFF_B = ((0, D, 3), (3, D, 1), (6, F, 2), (8, G, 2), (10, Ab, 1), (11, A, 1),
          (12, C, 4))

def ch(prog, b, b0):  return prog[(b - b0) % len(prog)]

# ---- guitars -----------------------------------------------------------
def riff(b, gain=1.0, open_last=False):
    """guitar and bass playing the same notes - the blues-rock wall"""
    fig = RIFF_A if (b % 2 == 0) else RIFF_B
    for i, (st, note, ln) in enumerate(fig):
        t = s.pos(b, swing(st))
        v = gain * (1.0 if st % 4 == 0 else 0.88)
        s.place(t, panned(mute(note, ln, take=(i + b) % 3, gain=15.0, heavy=HEAVY),
                          -SPREAD), v, 'gtr')
        s.place(t + SLIP, panned(mute(note, ln, take=10 + (i + b + 1) % 3,
                                      gain=15.0, heavy=HEAVY), SPREAD), v * 0.98, 'gtr')
    s.place(s.pos(b), bassbar(tuple((swing(st), note) for st, note, _ in fig),
                              take=b % 3, drive=2.2, decay=0.30), 0.95, 'bass')
    if open_last:
        s.place(s.pos(b, 12), panned(gtr(C, 8, take=b % 3, gain=16.0,
                                         heavy=HEAVY), 0.0), 0.55, 'gtr')

def wall(b, root, dur=16, gain=1.0, st=0.0):
    t = s.pos(b, st)
    s.place(t, panned(gtr(root, dur, take=b % 3, gain=16.0, heavy=HEAVY), -SPREAD),
            gain, 'gtr')
    s.place(t + SLIP, panned(gtr(root, dur, take=10 + (b + 1) % 3, gain=16.0,
                                 heavy=HEAVY), SPREAD), gain * 0.98, 'gtr')

# ---- drums -------------------------------------------------------------
def kicks(b, pat, gain=1.0):
    for st in pat:
        s.place(s.pos(b, st) + int(rng.integers(-25, 25)),
                pkick(seed=(int(st) + b) % 4, tune=60.0, decay=0.19),
                gain * (1.0 if st % 4 == 0 else 0.90), 'drums')

def snares(b, pat=(4, 12), gain=1.0, ghost=()):
    for st in pat:
        s.place(s.pos(b, st) + int(0.003 * SR) + int(rng.integers(-70, 70)),
                psnare(seed=(int(st) + b) % 5, tune=186.0, decay=0.13),
                gain * (0.96 + 0.07 * rng.random()), 'drums')
    for st in ghost:
        s.place(s.pos(b, swing(st)), psnare(2, seed=3), gain * 0.20, 'drums')

def tambs(b, gain=0.55, rate=2):
    for st in range(0, 16, rate):
        s.place(s.pos(b, swing(st)) + int(rng.integers(-90, 90)),
                tamb(1.4, open_=(st % 8 == 6), seed=(st + b) % 4),
                gain * (1.0 if st % 4 == 0 else 0.62 + 0.1 * rng.random()), 'perc')

def beat(b, kind, crash=False, gain=1.0):
    """A kick on every beat throughout. This is a lope, and a lope still has
    four beats in it - take two of them away and 132 BPM becomes 66."""
    if kind == 'swagger':
        kicks(b, (0, 4, 8, 11, 12)); snares(b, ghost=(7, 15))
        tambs(b, gain=0.5 * gain)
    elif kind == 'drive':
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b, ghost=(7,))
        tambs(b, gain=0.6 * gain)
        for st in range(0, 16, 2):
            s.place(s.pos(b, swing(st)) + int(rng.integers(-70, 70)),
                    phat(1.2, open_=(st == 14), seed=(st + b) % 4),
                    (0.55 if st % 4 == 0 else 0.36) * gain, 'drums')
    elif kind == 'chorus':
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b)
        for st in range(0, 16, 2):
            s.place(s.pos(b, swing(st)) + int(rng.integers(-70, 70)),
                    pride(3, seed=(st + b) % 4),
                    (0.9 if st % 4 == 0 else 0.58) * gain, 'drums')
        tambs(b, gain=0.7 * gain)
    elif kind == 'gallop':
        kicks(b, (0, 4, 8, 12)); snares(b)
        hooves(s, b, gain=0.42 * gain, seed=b)
        tambs(b, gain=0.5 * gain, rate=4)
    elif kind == 'sparse':
        kicks(b, (0, 8)); snares(b, (12,), gain=0.8)
        tambs(b, gain=0.35 * gain, rate=4)
    if crash:
        s.place(s.pos(b), pcrash(24, seed=b % 3), 0.5 * gain, 'drums')

def claps(b, steps_=(4, 12), gain=0.7):
    for st in steps_:
        s.place(s.pos(b, st) + int(rng.integers(-120, 120)),
                handclap(3, seed=(int(st) + b) % 4), gain, 'perc')

def fill(b, kind='toms'):
    if kind == 'toms':
        kicks(b, (0, 4, 8)); snares(b, (4,))
        for i, (st, tune) in enumerate(((8, 200), (10, 160), (11, 160),
                                        (12, 126), (13, 126), (14, 98), (15, 98))):
            s.place(s.pos(b, st), ptom(2, tune=tune), 0.66 + 0.045 * i, 'drums')
    elif kind == 'roll':
        kicks(b, (0, 4))
        for i in range(12):
            s.place(s.pos(b, 10 + i * 0.5), psnare(1.5, seed=i % 3),
                    0.42 + 0.04 * i, 'drums')
        snares(b, (4,))

# ---- the theme ---------------------------------------------------------
# Over Dm C Bb A. Every phrase falls, because the cadence falls; the one
# note that rises is the C# over the A, and that is the whole West.
THEME = [(0, 74, 6), (6, 72, 2), (8, 70, 4), (12, 69, 4),
         (16, 72, 8), (24, 69, 8),
         (32, 70, 4), (36, 69, 4), (40, 67, 8),
         (48, 69, 6), (54, 73, 6), (60, 69, 4)]
THEME_B = [(0, 77, 6), (6, 74, 2), (8, 72, 4), (12, 70, 4),
           (16, 72, 8), (24, 74, 8),
           (32, 74, 4), (36, 72, 4), (40, 70, 8),
           (48, 73, 8), (56, 69, 8)]

def play(events, b0, fn, bus, gain=1.0, pan=0.0, oct_=0, **kw):
    for st, note, ln in events:
        seg = fn(note + oct_, ln, **kw)
        s.place(s.pos(b0 + st // 16, st % 16), panned(seg, pan), gain, bus)

# ================= the desert (b0-7) =================
# Two pitched voices alone in a reverb is not "sparse", it is a games
# console: no noise floor, no low end, nothing with a body. So the wind is a
# real bed, a bass holds the tonic under the whole thing, and a floor tom
# marks the phrase - the room has a size before the tune arrives in it.
#
# And the guitar plays a LINE. A single note held for two bars, rendered once
# and placed twice, is a sample being triggered; a phrase whose every note is
# a separate take, with a hand's vibrato inside it and the squeak of that
# hand moving between them, is a person.
s.place(s.pos(0), wind_bed(16 * 16 + 40, seed=1), 1.45, 'air')
for b in (0, 4):
    # A drone is bowed, not picked: no pick grind, or it fills 250-500 Hz and
    # the whole intro comes out as one octave with a tune on top of it.
    s.place(s.pos(b), bassbar(((0, 26),), dur_steps=68, drive=1.2, decay=3.0,
                              bright=0.15), 0.80, 'bass')
    s.place(s.pos(b), ptom(6, tune=86.0, seed=b), 0.42, 'drums')
    s.place(s.pos(b, 8), ptom(4, tune=104.0, seed=b + 1), 0.20, 'drums')

# The line sits an octave up and the baritone doubles it an octave down, so
# the pair spans two octaves instead of both crowding the bass drone. That
# spread IS the classic western guitar sound, and it is also the only reason
# an intro built on one instrument does not come out as one narrow band.
TW_A = [(0, D + 12, 8), (8, F + 12, 4), (12, G + 12, 4),
        (16, A + 12, 8), (24, G + 12, 4), (28, F + 12, 4)]
TW_B = [(0, A + 12, 8), (8, C + 12, 4), (12, 62, 4),
        (16, C + 12, 8), (24, A + 12, 8)]
phrase(s, TW_A, 0, twang, 'twang', 0.34, pan=-0.10, trem=1.0, rate=1.0, decay=1.4)
phrase(s, TW_A, 0, twang, 'twang', 0.15, pan=0.18, oct_=-12, trem=1.0, rate=1.0,
       decay=1.8, bright=0.7)                          # the baritone underneath
play(THEME[:6], 2, whistle, 'whistle', 0.62, pan=0.1)
phrase(s, TW_B, 4, twang, 'twang', 0.32, pan=-0.16, trem=1.0, rate=1.0, decay=1.3)
phrase(s, TW_B, 4, twang, 'twang', 0.14, pan=0.20, oct_=-12, trem=1.0, rate=1.0,
       decay=1.7, bright=0.7)

# the bottleneck answers: the one articulation a picked guitar cannot make
s.place(s.pos(6), panned(slide(A + 12, 62, 14, take=0), 0.30), 0.40, 'twang')
s.place(s.pos(7, 6), panned(slide(C + 12, 65, 10, take=1, glide=0.55), -0.24),
        0.34, 'twang')

for b, st in ((1, 14), (3, 14), (5, 14), (7, 12)):     # the hand moving
    s.place(s.pos(b, st), fretnoise(2, seed=b, up=(b % 4 == 3)), 0.70, 'perc')
for b in range(2, 8):                                  # a rattle in the heat
    for st in (0, 4, 6, 10, 12, 14):
        s.place(s.pos(b, st) + int(rng.integers(-200, 200)),
                tamb(1.6, open_=(st in (6, 14)), seed=(st + b) % 4),
                (0.30 if st % 4 == 0 else 0.17) * (0.5 + 0.09 * (b - 2)), 'perc')

for b in (4, 5, 6, 7):                                 # a pulse, quietly
    kicks(b, (0, 8), gain=0.34 + 0.06 * (b - 4))
    if b >= 6:
        hooves(s, b, gain=0.20 + 0.10 * (b - 6), seed=b)
s.place(s.pos(7, 12), pcrash(16, seed=2, size=0.8), 0.30, 'drums')

# ================= the riff arrives (b8-15) =================
for b in range(8, 16):
    riff(b, gain=0.9)
    beat(b, 'sparse' if b < 12 else 'swagger', crash=(b in (8, 12)))
    if b >= 12:
        claps(b, (4, 12), 0.5)
    if b % 2 == 1:                                     # into every change
        s.place(s.pos(b, 14.5), fretnoise(1.5, seed=b), 0.30, 'perc')
s.place(s.pos(9, 8), panned(slide(50, A, 10, take=2, glide=0.5), 0.34), 0.26, 'twang')
s.place(s.pos(13, 8), panned(slide(A, 53, 12, take=0), -0.30), 0.30, 'twang')
fill(15, 'toms')

# ================= verse 1 (b16-31) =================
for b in range(16, 32):
    riff(b, gain=1.0, open_last=(b % 8 == 7))
    beat(b, 'swagger' if b < 24 else 'drive', crash=(b in (16, 24)))
    if b % 8 in (3, 7):
        claps(b, (4, 12), 0.55)
    if b == 23:
        fill(23, 'toms')
    if b == 31:
        fill(31, 'roll')
play([(0, 74, 4), (4, 72, 4), (8, 69, 8)], 20, twang, 'twang', 0.26, pan=0.4,
     trem=0.0, decay=1.6)
play([(0, 70, 4), (4, 69, 4), (8, 67, 6), (14, 69, 2)], 28, twang, 'twang',
     0.26, pan=-0.4, trem=0.0, decay=1.6)

# ================= the lift (b32-39) =================
for b in range(32, 40):
    root = [D, D, F, F, G, G, A, A][b - 32]
    wall(b, root, 16, 0.9)
    s.place(s.pos(b), bassbar(tuple((st, root - 12 if root > 40 else root)
                                    for st in (0, 4, 8, 12)),
                              take=b % 3, drive=2.2), 0.9, 'bass')
    beat(b, 'drive', crash=(b % 4 == 0))
    claps(b, (4, 12), 0.6)
play([(0, 69, 4), (4, 70, 4), (8, 72, 8), (16, 73, 12)], 36, twang, 'twang',
     0.30, pan=0.3, trem=1.0, rate=1.0)
fill(39, 'roll')

# ================= chorus 1 (b40-55) =================
def chorus(b0, bars=16, kind='chorus', horn_=False, gallop=False, mel=0.5):
    for b in range(b0, b0 + bars):
        i = (b - b0) % 4
        wall(b, CHORD_G[i], 16, 1.0)
        s.place(s.pos(b), bassbar(tuple((st, CHORD_B[i]) for st in (0, 3, 6, 8, 11, 14)),
                                  take=b % 3, drive=2.2), 0.95, 'bass')
        beat(b, 'gallop' if (gallop and (b - b0) % 8 >= 4) else kind,
             crash=((b - b0) % 4 == 0))
        if (b - b0) % 8 == 7 and b - b0 < bars - 1:
            fill(b, 'toms')
    for k in range(bars // 8):
        th = THEME if k % 2 == 0 else THEME_B
        play(th, b0 + k * 4 if False else b0 + k * 8, whistle, 'whistle', mel, pan=0.05)
        if horn_:
            play(th, b0 + k * 8, trumpet, 'horn', 0.34, pan=-0.15, oct_=-12,
                 rip=1.2, seed=k)

chorus(40, 16)
play([(0, 69, 4), (4, 73, 4), (8, 74, 8)], 54, twang, 'twang', 0.28, pan=-0.35,
     trem=1.0, rate=1.0)

# ================= verse 2 (b56-71) =================
for b in range(56, 72):
    riff(b, gain=1.0, open_last=(b % 8 == 7))
    beat(b, 'drive', crash=(b in (56, 64)))
    if b % 8 in (3, 7):
        claps(b, (4, 12), 0.55)
    if b == 63:
        fill(63, 'toms')
    if b == 71:
        fill(71, 'roll')
play([(0, 74, 4), (4, 73, 4), (8, 69, 8), (16, 67, 6), (22, 69, 10)], 58,
     twang, 'twang', 0.30, pan=0.4, trem=1.0, rate=1.0)
play([(0, 77, 4), (4, 74, 4), (8, 72, 4), (12, 70, 4), (16, 69, 12)], 66,
     twang, 'twang', 0.30, pan=-0.4, trem=1.0, rate=1.0)

# ================= the standoff (b72-79) =================
# Everything goes. The oldest device in the genre: the longer nothing
# happens, the bigger the thing that happens next.
s.place(s.pos(72), wind_bed(8 * 16 + 20, seed=5), 0.65, 'air')
s.place(s.pos(72), panned(twang(D, 46, trem=1.0, rate=1.0, decay=1.6), -0.15),
        0.30, 'twang')
play(THEME[:4], 73, whistle, 'whistle', 0.55, pan=0.1)
play(THEME[6:9], 76, whistle, 'whistle', 0.50, pan=-0.1)
s.place(s.pos(78), panned(twang(A, 28, trem=1.0, rate=1.0, decay=1.6), 0.2),
        0.32, 'twang')
for st in (8, 10, 12, 13, 14, 15):                     # the gallop, approaching
    s.place(s.pos(79, st), woodblock(1, tune=1050 - 30 * st, seed=st % 3),
            0.25 + 0.06 * (st - 8), 'perc')
s.place(s.pos(79, 12), pcrash(20, seed=1), 0.35, 'drums')
fill(79, 'roll')

# ================= last chorus (b80-95) =================
s.place(s.pos(80), pcrash(40, seed=0, size=1.5), 0.65, 'drums')
chorus(80, 16, horn_=True, gallop=True, mel=0.58)
for i, note in enumerate((62, 60, 58, 57)):            # gang shouts on the cadence
    for k in range(4):
        b = 80 + k * 4 + i
        if b >= 88:
            s.place(s.pos(b, 0.4), gang(note, 15, seed=i, rasp=0.4, drop=0.03),
                    0.26, 'gang')
play([(0, 81, 8), (8, 79, 8), (16, 77, 6), (22, 74, 10)], 92, twang, 'twang',
     0.32, pan=0.3, trem=1.0, rate=1.0)
# the last chord, and the wind again
s.place(s.pos(95), panned(gtr(D, 40, take=0, gain=16.0, heavy=HEAVY), -SPREAD), 1.0, 'gtr')
s.place(s.pos(95) + SLIP, panned(gtr(D, 40, take=11, gain=16.0, heavy=HEAVY),
                                 SPREAD), 0.98, 'gtr')
s.place(s.pos(95), bassbar(((0, 38),), dur_steps=32), 0.95, 'bass')
s.place(s.pos(95), pkick(tune=60.0), 1.0, 'drums')
s.place(s.pos(95), psnare(tune=186.0), 1.0, 'drums')
s.place(s.pos(95), pcrash(48, seed=0, size=1.8), 0.8, 'drums')
s.place(s.pos(95), wind_bed(70, seed=9), 0.55, 'air')
s.place(s.pos(95, 8), panned(twang(D + 12, 40, trem=1.0, rate=1.0, decay=2.2), 0.1),
        0.22, 'twang')

# ---- space -------------------------------------------------------------
# The twang and the whistle live in a spring tank; the band lives in a room.
# Two spaces, not five - the tank is a place the guitar is, not an effect on it.
s.bus['twang'] += bus_spring(s.bus['twang'], decay=1.7, wet=0.75, boing=0.7)
s.bus['whistle'] += bus_spring(s.bus['whistle'], decay=2.4, wet=0.55, boing=0.25)
s.bus['horn'] += room(s.bus['horn'], decay=2.2, wet=0.5, tone=3600)
s.bus['drums'] += room(s.bus['drums'], decay=0.62, wet=0.28, tone=5200)
s.bus['gtr'] += room(s.bus['gtr'], decay=0.32, wet=0.12, tone=4200)
s.bus['perc'] += room(s.bus['perc'], decay=0.9, wet=0.30, tone=6000)
s.bus['gang'] += room(s.bus['gang'], decay=1.4, wet=0.40, tone=3800)
s.bus['air'] = lp(s.bus['air'], 2200)

def duck_band(target, trigger, lo=500, hi=3200, depth=0.34, sens=3.0):
    env = uniform_filter1d(np.abs(trigger).max(axis=1), int(0.03 * SR))
    env = np.clip(env / max(env.max(), 1e-9) * sens, 0, 1)
    g = uniform_filter1d(1 - depth * env, int(0.05 * SR)).astype(np.float32)
    return target - bandpass(target, lo, hi) * (1 - g)[:, None]

s.bus['gtr'] = duck_band(s.bus['gtr'], s.bus['whistle'], lo=450, hi=2400, depth=0.30)

# ---- bus tone ----
s.bus['bass'] = hp(s.bus['bass'], 52, order=2)
s.bus['drums'] = shelf(hp(s.bus['drums'], 44, order=2), 8500, 2.5, 'high')
s.bus['drums'] -= 0.20 * bandpass(s.bus['drums'], 70, 130)
s.bus['gtr'] = hp(s.bus['gtr'], 74, order=2)
s.bus['gtr'] = shelf(s.bus['gtr'], 2300, 3.0, 'high')
s.bus['gtr'] -= 0.16 * bandpass(s.bus['gtr'], 260, 480)

# ---- the fader ---------------------------------------------------------
SECTIONS = [(0, 0.46), (8, 0.72), (12, 0.82),
            (16, 0.88), (24, 0.94),                     # verse 1
            (32, 0.96),                                 # the lift
            (40, 1.00),                                 # CHORUS
            (56, 0.90), (64, 0.96),                     # verse 2
            (72, 0.44),                                 # the standoff
            (80, 1.06),                                 # LAST CHORUS
            (96, 1.06)]

def fader():
    g = np.ones(s.total, dtype=np.float32)
    ramp = int(0.12 * SR)
    for (b0, v0), (b1, _) in zip(SECTIONS, SECTIONS[1:] + [(999, 0)]):
        a = s.pos(b0); e = min(s.pos(b1), s.total) if b1 < 999 else s.total
        if a >= s.total:
            break
        g[a:e] = v0
    for b, _ in SECTIONS[1:]:
        a = s.pos(b)
        if ramp < a < s.total - ramp:
            g[a - ramp:a + ramp] = np.linspace(g[a - ramp], g[a + ramp], 2 * ramp)
    return g[:, None]

AUTO = fader()
for _b in s.bus:
    s.bus[_b] *= AUTO

GAINS = {'drums': 0.30, 'gtr': 0.40, 'bass': 0.28, 'twang': 0.62,
         'whistle': 0.32, 'horn': 0.80, 'perc': 0.72, 'gang': 0.60, 'air': 0.70}
s.report(GAINS)
s.render('western_dustdevil_132.wav', drive=1.15, duck=0.0, limit=0.94,
         gains=GAINS, clip=1.18, fade=1.6)
