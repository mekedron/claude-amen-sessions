"""Curbside (~2:20, 104 bars @178) - hardcore punk in D minor, drop D.

The opposite corner of the genre from Grip Tape. That one was bright, major,
186, and carried by a sung lead line. This one is faster, tuned down a whole
tone, Phrygian where it wants to be nasty, and has no melody instrument at
all - the hook is eight people shouting the same three notes. Two minutes,
because a hardcore song that outstays two minutes is a rock song.

The low string is dropped to D (73 Hz), which is under the highpass the amp
chain is built around, so the whole front of the amp moves down with it.

  b0-3     feedback off a standing amp, one chord, four on the hats
  b4-11    the riff: i - i - bII - i - bVI - bVII - i - i, d-beat under it
  b12-27   verse 1: palm-muted eighths, the bII stabbing every fourth bar
  b28-35   chorus: chords open, two octaves of gang shouts, F - G - A
  b36-51   verse 2, kick doubling up
  b52-59   chorus 2
  b60-67   the fast part: snare on every offbeat, one tremolo-picked line
  b68-75   chorus 3
  b76-83   the breakdown: half-time snare over a kick that never stops
  b84-91   the riff again, climbing, everything returning
  b92-99   last chorus: gangs doubled, guitars harmonised in fifths
  b100-103 one chord, and the amp still humming after it
"""
import numpy as np
from punklib import *

BAR, STEP = set_tempo(178)                       # rebind: `import *` copied 186
rng = np.random.default_rng(19)
np.random.seed(19)
s = Session(104, tail=3.0)

# ---- the harmony -------------------------------------------------------
# D natural minor for anything sung, D Phrygian for the guitars: the bII is
# borrowed as a chord only, which is the oldest trick in heavy music - the
# menace lives in the riff and the tune stays singable.
D, Eb, F, G, A, Bb, C = 38, 39, 41, 43, 45, 46, 48
RIFF   = [D, D, Eb, D, Bb, C, D, D]              # i i bII i bVI bVII i i
HOOK   = [Bb, C, D, D, Bb, C, A, A]              # ends on the v, screaming for i
BREAK  = [D, D, Eb, Eb, D, D, C, A]

def ch(prog, b, b0):  return prog[(b - b0) % len(prog)]

HEAVY = 0.85
SPREAD = 0.9
SLIP = int(0.0032 * SR)
EIGHTHS = [0, 2, 4, 6, 8, 10, 12, 14]

# ---- guitars -----------------------------------------------------------
def wall(b, root, dur=16, gain=1.0, st=0.0, level=1.0):
    t = s.pos(b, st)
    s.place(t, panned(gtr(root, dur, take=b % 3, gain=19.0, heavy=HEAVY), -SPREAD),
            gain, 'gtr')
    s.place(t + SLIP, panned(gtr(root, dur, take=10 + (b + 1) % 3, gain=19.0,
                                 heavy=HEAVY), SPREAD), gain * 0.98, 'gtr')

def chug(b, root, pattern, gain=1.0, dur=2):
    for i, st in enumerate(pattern):
        t = s.pos(b, st)
        v = gain * (1.0 if st % 4 == 0 else 0.85 + 0.07 * rng.random())
        s.place(t, panned(mute(root, dur, take=(i + b) % 3, gain=17.0, heavy=HEAVY),
                          -SPREAD), v, 'gtr')
        s.place(t + SLIP, panned(mute(root, dur, take=10 + (i + b + 2) % 3,
                                      gain=17.0, heavy=HEAVY), SPREAD), v * 0.98, 'gtr')

def stab(b, root, st, dur=4, gain=1.0):
    """one open chord thrown into a gap"""
    wall(b, root, dur, gain, st=st)

def squeal(b, st, note=86, ln=30, gain=0.30, swell=2.2):
    """A guitar left in front of its own speaker. The note is whatever the
    room decides; here it is the fifth, high enough to sit over everything."""
    seg = solo(note, ln, gain=26.0, decay=9.0, vib=5.2, vib_depth=0.022, take=1)
    e = np.linspace(0, 1, len(seg)) ** swell
    k = int(0.3 * SR); e[-k:] *= np.linspace(1, 0.15, k)
    s.place(s.pos(b, st), reverb(seg * e[:, None], decay=2.0, wet=0.28), gain, 'lead')

# ---- bass --------------------------------------------------------------
def bassline(b, root, busy=True, walk_to=None, gain=0.95):
    note = root - 12
    pat = EIGHTHS if busy else [0, 4, 8, 12]
    evs = [(st, note) for st in pat]
    if walk_to is not None:
        tgt = walk_to - 12
        d = 1 if tgt > note else -1
        evs = [e for e in evs if e[0] < 12] + [(12, tgt - 2 * d), (14, tgt - d)]
    s.place(s.pos(b), bassbar(tuple(evs), take=b % 3, drive=2.4), gain, 'bass')

# ---- drums -------------------------------------------------------------
def hats(b, open_at=(), gain=0.9, rate=2):
    for st in range(0, 16, rate):
        o = st in open_at
        v = gain * (1.0 if st % 4 == 0 else 0.60 + 0.09 * rng.random())
        s.place(s.pos(b, st) + int(rng.integers(-70, 70)),
                phat(1.5 if o else 1, open_=o, seed=(st + b) % 5),
                v * (1.15 if o else 1), 'drums')

def kicks(b, pat, gain=1.0):
    for st in pat:
        s.place(s.pos(b, st) + int(rng.integers(-22, 22)),
                pkick(seed=(int(st) + b) % 4, tune=62.0),
                gain * (1.0 if st % 4 == 0 else 0.92), 'drums')

def snares(b, pat=(4, 12), gain=1.0, ghost=()):
    for st in pat:
        s.place(s.pos(b, st) + int(0.002 * SR) + int(rng.integers(-55, 55)),
                psnare(seed=(int(st) + b) % 5, tune=198.0),
                gain * (0.97 + 0.06 * rng.random()), 'drums')
    for st in ghost:
        s.place(s.pos(b, st), psnare(2, seed=2), gain * 0.22, 'drums')

def beat(b, kind, crash=False, gain=1.0):
    """Every pattern kicks on all four beats. The extras go between them.
    A hardcore beat that only kicks on 1 and 3 halves the felt tempo, and
    198 BPM played that way feels like 99."""
    if kind == 'dbeat':
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b); hats(b, gain=0.85 * gain)
    elif kind == 'drive':
        kicks(b, (0, 3, 4, 7, 8, 11, 12, 15)); snares(b)
        hats(b, open_at=(6, 14), gain=0.8 * gain)
    elif kind == 'skank':                                # the fast part
        kicks(b, (0, 4, 8, 12)); snares(b, (2, 6, 10, 14), gain=0.78)
        hats(b, gain=0.78 * gain)
    elif kind == 'charge':                               # the chorus
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b, ghost=(7,) if b % 2 else ())
        hats(b, open_at=(2, 6, 10, 14), gain=0.72 * gain)
    elif kind == 'mosh':                                 # the breakdown
        kicks(b, (0, 4, 8, 12), gain=1.05)
        snares(b, (8,), gain=1.05)
        for st in range(0, 16, 4):
            s.place(s.pos(b, st) + int(rng.integers(-60, 60)),
                    pride(3, seed=(st + b) % 4), 0.85 * gain, 'drums')
    if crash:
        s.place(s.pos(b), pcrash(20, seed=b % 3), 0.55 * gain, 'drums')

def fill(b, kind='toms'):
    if kind == 'toms':
        kicks(b, (0, 4, 8)); snares(b, (4,))
        for i, (st, tune) in enumerate(((8, 210), (9, 210), (10, 168), (11, 168),
                                        (12, 132), (13, 132), (14, 104), (15, 104))):
            s.place(s.pos(b, st), ptom(2, tune=tune), 0.68 + 0.04 * i, 'drums')
    elif kind == 'roll':
        kicks(b, (0, 4))
        for i in range(16):
            s.place(s.pos(b, 8 + i * 0.5), psnare(1.5, seed=i % 3),
                    0.45 + 0.035 * i, 'drums')
        snares(b, (4,))
    elif kind == 'stop':                                 # one hit, then air
        kicks(b, (0,)); snares(b, (0,), gain=1.05)
        s.place(s.pos(b), pcrash(26, seed=1), 0.62, 'drums')

# ---- gang vocals -------------------------------------------------------
# Two octaves at once. One is a crowd; two is a room that cannot fit them.
def shout(b, note, ln=15, gain=1.0, low=True):
    s.place(s.pos(b, 0.3), gang(note, ln, seed=b % 4, rasp=0.55, drop=0.045),
            0.34 * gain, 'gang')
    if low:
        s.place(s.pos(b, 0.3) + 300,
                gang(note - 12, ln, seed=(b + 2) % 4, rasp=0.35, drop=0.03),
                0.26 * gain, 'gang')

GANG = [65, 67, 69, 69, 65, 67, 69, 72]              # F G A A  F G A C

# ================= intro (b0-3) =================
_n, _t = steps(52)
hum = stereo(np.sin(2 * np.pi * 50 * _t) + 0.4 * np.sin(2 * np.pi * 150 * _t))
hum = hum * (0.06 * np.minimum(_t / 0.5, 1.0))[:, None]
hum += hp(stereo(np.random.randn(_n)), 3000) * 0.012
s.place(s.pos(0), hum, 1.0, 'gtr')
squeal(0, 2, note=86, ln=34, gain=0.34)
wall(1, D, 24, 0.85, st=8)                            # one chord, then nothing
s.place(s.pos(1, 8), pcrash(28, seed=0), 0.55, 'drums')
s.place(s.pos(1, 8), bassbar(((0, D - 12),), dur_steps=24), 0.8, 'bass')
for i in range(4):                                    # "one-two-three-four"
    s.place(s.pos(3, i * 4), phat(2, seed=i), 0.65 if i else 0.95, 'drums')
    s.place(s.pos(3, i * 4), psnare(1.2, seed=i, rim=1.5), 0.40, 'drums')

# ================= the riff (b4-11) =================
for b in range(4, 12):
    root = ch(RIFF, b, 4)
    nxt = ch(RIFF, b + 1, 4)
    if root == Eb or b % 8 in (6, 7):
        wall(b, root, 16, 0.95)                       # the bII rings
    else:
        chug(b, root, EIGHTHS, gain=0.95)
        wall(b, root, 6, 0.55, st=12)
    bassline(b, root, walk_to=nxt if b % 4 == 3 else None)
    beat(b, 'dbeat' if b < 8 else 'drive', crash=(b in (4, 8)))
fill(11, 'toms')

# ================= verse 1 (b12-27) =================
for b in range(12, 28):
    root = ch(RIFF, b, 12)
    nxt = ch(RIFF, b + 1, 12)
    chug(b, root, EIGHTHS, gain=0.95)
    if root == Eb:
        stab(b, Eb, 8, 8, 0.7)                        # the Phrygian stab
    bassline(b, root, walk_to=nxt if (b - 12) % 8 == 7 else None)
    beat(b, 'dbeat' if b < 20 else 'drive', crash=(b in (12, 20)))
    if b == 19:
        fill(19, 'toms')
    if b == 27:
        fill(27, 'roll')

# ================= chorus 1 (b28-35) =================
def chorus(b0, gang_gain=1.0, fifths=False, kind='charge'):
    for b in range(b0, b0 + 8):
        root = ch(HOOK, b, b0)
        nxt = ch(HOOK, b + 1, b0)
        wall(b, root, 16, 1.0)
        if fifths:                                    # a second guitar a fifth up
            s.place(s.pos(b) + 200,
                    panned(gtr(root + 7, 16, take=(b + 2) % 3, gain=19.0,
                               heavy=HEAVY * 0.5), 0.25), 0.42, 'gtr')
        bassline(b, root, walk_to=nxt if (b - b0) % 4 == 3 else None)
        beat(b, kind, crash=((b - b0) % 4 == 0))
        shout(b, GANG[(b - b0) % 8], gain=gang_gain)
    fill(b0 + 7, 'roll') if False else None

chorus(28)
fill(35, 'toms')

# ================= verse 2 (b36-51) =================
for b in range(36, 52):
    root = ch(RIFF, b, 36)
    nxt = ch(RIFF, b + 1, 36)
    chug(b, root, EIGHTHS, gain=0.95)
    if root == Eb:
        stab(b, Eb, 8, 8, 0.75)
    bassline(b, root, walk_to=nxt if (b - 36) % 8 == 7 else None)
    beat(b, 'drive', crash=(b in (36, 44)))
    if b == 43:
        fill(43, 'toms')
    if b == 51:
        fill(51, 'roll')
squeal(46, 8, note=84, ln=26, gain=0.20)

# ================= chorus 2 (b52-59) =================
chorus(52)

# ================= the fast part (b60-67) =================
# Snare on every offbeat eighth. The kick keeps all four beats underneath it,
# so the tempo does not double - only the top of the kit does.
TREM = [69, 69, 70, 69, 74, 76, 77, 81]              # A A Bb A  D E F A
for b in range(60, 68):
    root = ch(RIFF, b, 60)
    chug(b, root, EIGHTHS, gain=0.9)
    bassline(b, root)
    beat(b, 'skank', crash=(b == 60))
    for i in range(16):                               # tremolo picking
        s.place(s.pos(b, i) + int(rng.integers(-45, 45)),
                panned(solo(TREM[b - 60], 1.6, take=i % 3), 0.1 if i % 2 else -0.1),
                0.40 * (1.0 if i % 4 == 0 else 0.78), 'lead')
fill(67, 'roll')

# ================= chorus 3 (b68-75) =================
chorus(68, gang_gain=1.1)

# ================= the breakdown (b76-83) =================
# Everything halves except the kick. The snare moves to beat 3 and the
# guitars stop playing eighths and start playing gaps - the gaps are the part.
s.place(s.pos(76), pcrash(40, seed=1, size=1.4), 0.7, 'drums')
MOSH = [(0, 'open', 6), (6, 'mute', 2), (8, 'mute', 2), (10, 'open', 6)]
for b in range(76, 84):
    root = ch(BREAK, b, 76)
    for st, how, ln in MOSH:
        if how == 'open':
            wall(b, root, ln + 2, 1.0, st=st)
        else:
            chug(b, root, [st], gain=1.0)
    s.place(s.pos(b), bassbar(tuple((st, root - 12) for st, _, _ in MOSH),
                              take=b % 3, drive=2.6, decay=0.45), 1.0, 'bass')
    beat(b, 'mosh', gain=1.0)
    if b >= 80:
        shout(b, [57, 57, 60, 62][b - 80], ln=13, gain=0.85, low=False)
squeal(82, 0, note=81, ln=28, gain=0.26)
fill(83, 'roll')

# ================= the riff returns (b84-91) =================
for b in range(84, 92):
    root = ch(RIFF, b, 84)
    nxt = ch(RIFF, b + 1, 84)
    chug(b, root, EIGHTHS, gain=1.0)
    if root == Eb:
        stab(b, Eb, 8, 8, 0.8)
    bassline(b, root, walk_to=nxt if (b - 84) % 4 == 3 else None)
    beat(b, 'dbeat' if b < 88 else 'drive', crash=(b in (84, 88)))
fill(91, 'toms')

# ================= last chorus (b92-99) =================
chorus(92, gang_gain=1.25, fifths=True, kind='drive')

# ================= outro (b100-103) =================
for b in (100, 101):
    chug(b, D, EIGHTHS, gain=1.0)
    bassline(b, D)
    beat(b, 'drive')
fill(102, 'toms')
s.place(s.pos(103), panned(gtr(D, 36, take=0, gain=19.0, heavy=HEAVY), -SPREAD),
        1.0, 'gtr')
s.place(s.pos(103) + SLIP,
        panned(gtr(D, 36, take=11, gain=19.0, heavy=HEAVY), SPREAD), 0.98, 'gtr')
s.place(s.pos(103), bassbar(((0, D - 12),), dur_steps=30), 1.0, 'bass')
s.place(s.pos(103), pkick(tune=62.0), 1.0, 'drums')
s.place(s.pos(103), psnare(tune=198.0), 1.0, 'drums')
s.place(s.pos(103), pcrash(46, seed=0, size=1.7), 0.85, 'drums')
squeal(103, 4, note=86, ln=40, gain=0.24, swell=1.3)   # the amp, still on

# ---- the fader ---------------------------------------------------------
SECTIONS = [(0, 0.34), (1, 0.62), (3, 0.50), (4, 0.82),
            (12, 0.72), (20, 0.79),                    # verse 1
            (28, 1.00),                                # CHORUS
            (36, 0.75), (44, 0.82),                    # verse 2
            (52, 1.00),                                # CHORUS 2
            (60, 0.90),                                # the fast part
            (68, 1.00),                                # CHORUS 3
            (76, 1.04),                                # breakdown: its hits slam;
                                                       # the gaps keep it quiet
            (84, 0.88),                                # riff returns
            (92, 1.06),                                # LAST CHORUS
            (100, 1.00), (104, 1.00)]

def fader():
    g = np.ones(s.total, dtype=np.float32)
    ramp = int(0.09 * SR)
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

# ---- make room for the shouts ------------------------------------------
def duck_band(target, trigger, lo=500, hi=3000, depth=0.34, sens=3.0):
    env = np.abs(trigger).max(axis=1)
    env = uniform_filter1d(env, int(0.025 * SR))
    env = np.clip(env / max(env.max(), 1e-9) * sens, 0, 1)
    g = uniform_filter1d(1 - depth * env, int(0.04 * SR)).astype(np.float32)
    return target - bandpass(target, lo, hi) * (1 - g)[:, None]

s.bus['gtr'] = duck_band(s.bus['gtr'], s.bus['gang'])
_pk = float(np.abs(s.bus['lead']).max()) or 1.0
s.bus['lead'] = softclip(s.bus['lead'] / _pk * 2.2, 1.0, knee=0.35) * _pk * 0.5

# ---- bus tone and room -------------------------------------------------
s.bus['bass'] = hp(s.bus['bass'], 44, order=2)
s.bus['drums'] = shelf(hp(s.bus['drums'], 36, order=2), 8500, 2.0, 'high')
s.bus['gtr'] = hp(s.bus['gtr'], 66, order=2)           # drop D lives at 73 Hz
s.bus['gtr'] = shelf(s.bus['gtr'], 2300, 2.5, 'high')
s.bus['drums'] -= 0.30 * bandpass(s.bus['drums'], 70, 130)   # kick and bass both
s.bus['bass'] -= 0.16 * bandpass(s.bus['bass'], 70, 130)     # wanted the same band

s.bus['drums'] += room(s.bus['drums'], decay=0.50, wet=0.26, tone=5400)
s.bus['gtr'] += room(s.bus['gtr'], decay=0.28, wet=0.10, tone=4000)
s.bus['lead'] += room(s.bus['lead'], decay=1.0, wet=0.20, tone=4600)
s.bus['gang'] += room(s.bus['gang'], decay=1.2, wet=0.42, tone=3800)

AUTO = fader()
for _b in s.bus:
    s.bus[_b] *= AUTO

GAINS = {'drums': 0.30, 'gtr': 0.44, 'bass': 0.30, 'lead': 0.30, 'gang': 0.40}
s.report(GAINS)
s.render('punk_curbside_178.wav', drive=1.15, duck=0.0, limit=0.94,
         gains=GAINS, clip=1.18, fade=0.6)
