"""MOLOTILKA - big beat at 153 BPM in E minor. Brighton, 1998, the fast end
of it: a surf guitar loop, a spoken hook repeated until it stops being words,
and a chop that winds up until the ear cannot count it any more.

The name is a threshing machine - the thing that beats.

Three parts carry it and none of them is a chord progression. The guitar is a
stiff steel string on a bridge single-coil into a spring, playing one
descending pentatonic run for four minutes. The hook is SYNTHESISED speech,
not a sample: `speak` renders the whole sentence as one utterance with a
falling pitch and a formant track that never stops travelling, because a
sentence built out of separately-sung syllables is a robot chanting. And the
structural device is `accel` - the same slice retriggered at a spacing that
shrinks geometrically, which is the one gesture this genre invented.

E minor because that is where a surf guitar lives: the open low E is the
drone every one of those records is built on, and the riff is the top four
notes of the pentatonic falling onto it.

    intro | beat | groove | THE WIND-UP | DROP | break | DROP 2 | wind | FINAL | out
    0       8      24       40            56     88      104      136    144     168
"""
import numpy as np
from skanklib import *

set_tempo(153)
np.random.seed(153)

# ---- the material ----
# Near-static harmony: three bars of E minor and one of A, the Dorian IV, so
# the natural 6th is audible once per cycle and the mode is not just "minor".
ORGAN = [(59, 62, 64, 67), (59, 62, 64, 67),          # B D E G
         (59, 62, 64, 67), (59, 61, 64, 67)]          # B C# E G - one voice moves
HORN = [(64, 67, 71), (64, 67, 71), (64, 67, 71), (64, 68, 71)]
KICK_TUNE = 52.0

# The riff: a descending pentatonic run that lands on the open low E, slid
# into at the top and tremolo-picked at the bottom. Two bars, and it does not
# change once in the record - the filter and the arrangement do the moving.
RIFF = [
    ((0, 64, 2.0, {'bend': 2.0}), (2, 62, 1.0), (3, 59, 2.0), (6, 57, 2.0),
     (8, 55, 3.0), (11, 52, 2.0), (14, 55, 2.0)),
    ((0, 59, 2.0), (2, 57, 1.0), (3, 55, 2.0), (6, 52, 6.0, {'trem': 12.0}),
     (12, 55, 2.0), (14, 57, 2.0, {'bend': 1.0})),
]

# The bass. The low E1 anchors every downbeat and the line works upward from
# it; the last hit of each bar approaches the next root.
BASS = [
    ((0, 28), (3, 40), (6, 43), (8, 40), (11, 47), (14, 46)),
    ((0, 28), (3, 40), (6, 43), (8, 45), (10, 47), (13, 50), (15, 47)),
]

# The hook. (step, length, vowel in, vowel out, consonant, semitone accent).
# It is not English that a machine can pronounce - it is the SHAPE of the
# sentence, and at this tempo under this much distortion that is all any
# sampled vocal in this genre ever was.
SAY_A = ((0, 2.0, 'ah', 'ee', 'r', +2), (2, 1.0, 'uh', 'uh', '', 0),
         (3, 2.0, 'uh', 'oo', 'b', +1), (5, 3.0, 'ah', 'oo', 'n', +3),
         (9, 1.0, 'uh', 'uh', 'th', -1), (10, 2.0, 'uh', 'uh', 'f', +2),
         (12, 2.0, 'oh', 'oo', 's', +1), (14, 2.0, 'oh', 'oh', 'b', 0),
         (16, 3.0, 'uh', 'uh', 'th', -3))
SAY_B = ((0, 2.0, 'eh', 'eh', 'ch', +2), (2, 1.0, 'ih', 'ih', 't', 0),
         (3, 2.0, 'ah', 'oo', '', +1), (5, 3.0, 'ah', 'oo', 'n', +3),
         (9, 1.0, 'uh', 'uh', 'th', -1), (10, 2.0, 'uh', 'uh', 'f', +2),
         (12, 2.0, 'oh', 'oo', 's', +1), (14, 2.0, 'oh', 'oh', 'b', 0),
         (16, 3.0, 'uh', 'uh', 'th', -3))
SAY_SHORT = SAY_A[:4]                                  # just "right about now"

# ---- the grooves ----
BREAK = {
    'kick':  ('x---x---x---x---', 'x---x---x---x---'),
    'snare': ('----x-------x---', '----x-------x-+-'),
    'ghost': ('..-...-..-.-..-.', '..-...-.-..-..-.'),
    'hat':   ('x-+-x-+-x-+-x-+-', 'x-+-x-+-x-+-x-++'),
    'ohat':  ('--------o-------', '----------------'),
    'tamb':  ('--+---+---+---+-', '--+---+---+---+-'),
}
STRIPPED = {'kick': 'x---x---x---x---', 'snare': '----x-------x---',
            'hat': 'x---x---x---x---'}
LOOSE = {'snare': ('----x-------x---', '----x---x---x-+-'),
         'ghost': ('..-...-..-.-..-.', '..-...-.-..-..-.'),
         'hat': 'x-+-x-+-x-+-x-+-', 'tamb': '--+---+---+---+-'}
HANDS = {'hat': 'x-+-x-+-x-+-x-+-', 'tamb': '--+---+---+---+-',
         'clap': '----x-------x---'}
BIG = {
    'kick':  ('x---x---x---x---', 'x---x---x--xx---'),
    'snare': ('----x-------x---', '----x---.---x-+-'),
    'ghost': ('..-...-..-.-..-.', '..-.-.-.-..-..-.'),
    'hat':   ('x-+-x-+-x-+-x-+-', 'x-+-x-+-x-+-x-++'),
    'ride':  ('+-+-+-+-+-+-+-+-', '+-+-+-+-+-+-+-+-'),
    'ohat':  ('--------o-------', '------------o---'),
    'tamb':  ('--+---+---+---+-', '--+---+---+---+-'),
    'clap':  ('----x-------x---', '----x-------x---'),
}

s = Session(176, tail=3.0)

# ---- the parts ----
_ORG = {}
STABS = [(2, 1.5), (6, 1.0), (7, 0.5), (10, 1.5), (14, 1.0), (15, 0.5)]
STABS_B = [(2, 1.5), (6, 1.0), (9, 0.5), (10, 1.0), (14, 2.0)]


def organ(b, gain=1.0, hits=None, cutoff=None, rate=6.4, click=1.0):
    key = (b % 4, round(rate, 2), click)
    if key not in _ORG:
        raw = organbar(tuple(midi(n) for n in ORGAN[b % 4]), 16, click=click,
                       seed=b % 4)
        _ORG[key] = leslie(raw, rate=rate, drum_rate=rate * 0.84)
    seg = _ORG[key]
    if hits:
        seg = chop(seg, hits)
    if cutoff:
        seg = lp(seg, cutoff)
    s.place(s.pos(b), seg, gain, 'keys')


def gtr(b, gain=1.0, bright=1.0, dirt=0.30, decay=1.4, octave=0, bus='gtr'):
    twangbar(s, b, [(e[0], e[1] + octave, e[2]) + tuple(e[3:]) for e in RIFF[b % 2]],
             gain=gain, bus=bus, seed=b, bright=bright, dirt=dirt, decay=decay)


def bass(b, gain=1.0, fuzz=5.5, cut=2400, sub=1.0, grind=1.0, **kw):
    s.place(s.pos(b), fuzzbar(BASS[b % 2], gain=gain, fuzz=fuzz, cut=cut,
                              sub=sub, grind=grind, take=b % 2, **kw), 1.0, 'bass')


_SAY = {}


def say(b, which='A', st=0.0, gain=1.0, bus='vox', note=52, bars=2):
    key = (which, note, bars)
    if key not in _SAY:
        src = {'A': SAY_A, 'B': SAY_B, 'S': SAY_SHORT}[which]
        _SAY[key] = crush(speak(src, 16 * bars, note=note, seed=hash(which) % 97),
                          bits=11, sr_div=2, pre=11000)
    s.place(s.pos(b, st), _SAY[key], gain, bus)


def hornhit(b, steps_=(6, 14), gain=1.0, dur=3.0, bright=1.0):
    for x in steps_:
        s.place(s.pos(b, x), horns(tuple(midi(n) for n in HORN[b % 4]), dur,
                                   bright=bright, seed=b % 4), gain, 'horn')


# ================= intro: 0-7 - the deck comes up to speed =================
s.place(s.pos(0), crackle(8 * 16, gain=0.9), 1.0, 'fx')
_loop = np.zeros((int(2 * BAR), 2), dtype=np.float32)
for i, ev in enumerate(RIFF[0] + tuple((e[0] + 16,) + e[1:] for e in RIFF[1])):
    seg = twang(ev[1], ev[2], take=i % 5, **(ev[3] if len(ev) > 3 else {}))
    a = int(ev[0] * STEP)
    e = min(a + len(seg), len(_loop))
    _loop[a:e] += seg[:e - a]
s.place(s.pos(0), spin(_loop, r0=0.42, r1=1.0, curve=1.5), 0.60, 'gtr')
s.place(s.pos(4), spin(_loop, r0=0.72, r1=1.0, curve=1.2), 0.68, 'gtr')
for b in range(4, 8):
    kitbar(s, b, LOOSE if b < 6 else STRIPPED, gain=0.40 + 0.10 * (b - 4),
           swing=0.56, seed=b, hats=0.8, register=b >= 6)
s.place(s.pos(6), say(6, 'S', gain=0.0) or 0, 0.0, 'vox') if False else None
say(6, 'S', st=8.0, gain=0.55)
s.place(s.pos(7), stab_riser(16, gain=0.65, f0=260, f1=3400), 1.0, 'fx')
fill(s, 7, 'roll', gain=0.7, seed=7)

# ================= the beat: 8-23 =================
for b in range(8, 24):
    ph = b - 8
    kitbar(s, b, BREAK, gain=0.88, swing=0.56, seed=b, tune=KICK_TUNE)
    gtr(b, gain=0.62, bright=0.9, dirt=0.24)
    if ph >= 4:
        bass(b, gain=0.92, fuzz=4.8, cut=1700 + 40 * ph)
    if ph >= 8:
        organ(b, gain=0.30, hits=STABS)
    if ph % 4 == 0:
        say(b, 'A' if (ph // 4) % 2 == 0 else 'B', gain=0.58 + 0.04 * ph)
s.place(s.pos(8), bcrash(20, gain=0.7), 1.0, 'drums')
s.place(s.pos(16), bcrash(18, gain=0.6), 1.0, 'drums')
fill(s, 15, 'stutter', gain=0.85, seed=15)
fill(s, 23, 'roll', gain=0.9, seed=23)

# ================= groove: 24-39 - the record proper =================
for b in range(24, 40):
    ph = b - 24
    kitbar(s, b, BREAK, gain=0.98, swing=0.56, seed=b, tune=KICK_TUNE,
           fat=1.0 + 0.15 * (ph >= 8))
    gtr(b, gain=0.78, dirt=0.30)
    bass(b, gain=1.0, fuzz=5.5, cut=2100 + 40 * ph)
    organ(b, gain=0.38, hits=STABS if ph % 4 != 3 else STABS_B)
    if ph % 4 == 0:
        say(b, 'A' if (ph // 4) % 2 == 0 else 'B', gain=0.66)
    if ph >= 8:
        hornhit(b, steps_=(14,), gain=0.42)
s.place(s.pos(24), bcrash(24, gain=0.8), 1.0, 'drums')
s.place(s.pos(32), bcrash(20, gain=0.7), 1.0, 'drums')
fill(s, 31, 'toms', gain=0.85, seed=31)
s.place(s.pos(35, 12), scratch(twang(64, 4, take=2), cycles=3.0, depth=2.0),
        0.70, 'fx')
fill(s, 39, 'roll', gain=0.9, seed=39)

# ============ THE WIND-UP: 40-55 - the device the genre is named for =======
# Sixteen bars in which nothing new arrives and everything speeds up. The
# guitar figure and the hook are both retriggered at a spacing that halves
# roughly every four bars, the filter opens across the whole run, and the
# drums are pulled out from under it at bar 52 so the last four bars are the
# chop on its own.
_hook = _SAY[('S', 52, 2)] if ('S', 52, 2) in _SAY else None
say(40, 'S', gain=0.0)                                  # make sure it is cached
_hook = _SAY[('S', 52, 2)]
_stab = twang(64, 3.0, take=1, bend=2.0)
for b in range(40, 56):
    ph = b - 40
    if ph >= 14:                       # the kit comes back for the last two
        kitbar(s, b, BIG, gain=1.04, swing=0.56, seed=b, tune=KICK_TUNE, fat=1.2)
        bass(b, gain=1.06, fuzz=6.4, cut=2700)
        hornhit(b, steps_=(6, 14), gain=0.60)
    elif ph < 12:
        kitbar(s, b, BREAK if ph < 8 else STRIPPED, gain=0.98 + 0.01 * ph,
               swing=0.56, seed=b, tune=KICK_TUNE, hats=0.9 + 0.06 * ph)
        bass(b, gain=1.00, fuzz=5.0 + 0.15 * ph, cut=1500 + 130 * ph)
    if ph < 8:
        gtr(b, gain=0.62, dirt=0.30)
        hornhit(b, steps_=(14,), gain=0.44)
    organ(b, gain=0.34, hits=STABS)
n_hits = accel(s, s.pos(40), _stab, total_steps=256.0, step0=4.0, step1=0.25,
               gain=0.44, gain1=0.80, bus='gtr', curve=1.0)
for i, b in enumerate((40, 44, 48, 50, 52, 53, 54, 55)):
    say(b, 'S', gain=0.44 + 0.04 * i, bars=1)
s.place(s.pos(44), stab_riser(96, gain=0.60, f0=240, f1=4200), 1.0, 'fx')
s.place(s.pos(52), stab_riser(64, gain=0.95, f0=260, f1=7000), 1.0, 'fx')
s.place(s.pos(54), bcrash(16, gain=0.5), 1.0, 'drums')
fill(s, 55, 'roll', gain=1.0, seed=55)
s.place(s.pos(55, 10), reverse_crash(12, gain=0.9), 1.0, 'fx')
s.place(s.pos(55, 12), subdrop(8, f0=190, f1=30, gain=0.85, drive=1.7), 1.0, 'fx')

# ================= DROP 1: 56-87 =================
for b in range(56, 88):
    ph = b - 56
    kitbar(s, b, BIG if ph >= 8 else BREAK, gain=1.0, swing=0.56, seed=b,
           tune=KICK_TUNE, fat=1.15)
    gtr(b, gain=0.84, dirt=0.34 + 0.06 * (ph >= 16))
    bass(b, gain=1.02, fuzz=6.0, cut=2500,
         wah=1.0 if 16 <= ph < 24 else 0.0, wah_lo=340, wah_hi=2600)
    thin = 24 <= ph < 28
    if ph % 8 != 7 and not thin:
        organ(b, gain=0.42, hits=STABS if ph % 4 != 3 else STABS_B)
    if ph % 4 == 0:
        say(b, 'A' if (ph // 4) % 2 == 0 else 'B', gain=0.70)
    if ph >= 8 and not thin:
        hornhit(b, steps_=(6, 14) if ph % 4 != 3 else (6, 12, 14),
                gain=0.52 if ph < 16 else 0.60)
for b in (56, 64, 72, 80, 84):
    s.place(s.pos(b), bcrash(24, gain=0.75), 1.0, 'drums')
for b, kind in ((59, 'stutter'), (63, 'roll'), (67, 'toms'), (71, 'roll'),
                (75, 'stutter'), (79, 'kicks'), (83, 'toms'), (87, 'roll')):
    fill(s, b, kind, gain=0.9, seed=b)
s.place(s.pos(78, 12), scratch(_hook[:int(3 * STEP)], cycles=3.0, depth=2.2),
        0.72, 'fx')

# ================= the break: 88-103 =================
for b in range(88, 104):
    ph = b - 88
    if ph < 4:
        kitbar(s, b, HANDS, gain=0.72, swing=0.56, seed=b)
        organ(b, gain=0.48, rate=1.1, click=0.3, cutoff=3400)
        gtr(b, gain=0.70, bright=1.1, dirt=0.18, decay=2.0)
    elif ph < 10:
        kitbar(s, b, LOOSE, gain=0.58 + 0.06 * (ph - 4), swing=0.56, seed=b)
        organ(b, gain=0.44, hits=STABS)
        gtr(b, gain=0.76, dirt=0.26)
        bass(b, gain=0.68 + 0.06 * (ph - 4), fuzz=4.2, cut=1300, grind=0.5)
    else:
        kitbar(s, b, BREAK, gain=0.90 + 0.02 * (ph - 10), swing=0.56, seed=b,
               tune=KICK_TUNE)
        gtr(b, gain=0.80, dirt=0.32)
        bass(b, gain=0.95, fuzz=5.6, cut=2100)
        organ(b, gain=0.42, hits=STABS)
    if ph % 4 == 0:
        say(b, 'B' if ph % 8 == 0 else 'A', gain=0.62 + 0.02 * ph)
accel(s, s.pos(100), _stab, total_steps=64.0, step0=2.0, step1=0.25,
      gain=0.60, bus='gtr')
for b in (100, 101, 102, 103):
    say(b, 'S', gain=0.50 + 0.05 * (b - 100), bars=1)
s.place(s.pos(100), stab_riser(64, gain=0.95, f0=230, f1=7200), 1.0, 'fx')
fill(s, 103, 'roll', gain=1.0, seed=103)
s.place(s.pos(103, 10), reverse_crash(12, gain=0.95), 1.0, 'fx')
s.place(s.pos(103, 12), subdrop(8, f0=200, f1=30, gain=0.9, drive=1.8), 1.0, 'fx')

# ================= DROP 2: 104-135 =================
for b in range(104, 136):
    ph = b - 104
    kitbar(s, b, BIG, gain=1.04, swing=0.56, seed=b, tune=KICK_TUNE, fat=1.2)
    gtr(b, gain=0.88, dirt=0.40, octave=12 if 16 <= ph < 24 else 0)
    bass(b, gain=1.06, fuzz=6.4, cut=2800,
         wah=2.0 if 8 <= ph < 16 else 0.0, wah_lo=320, wah_hi=2800)
    thin = 24 <= ph < 28
    if ph % 8 != 7 and not thin:
        organ(b, gain=0.44, hits=STABS if ph % 4 != 3 else STABS_B)
    if ph % 4 == 0:
        say(b, 'A' if (ph // 4) % 2 == 0 else 'B', gain=0.74)
    if not thin:
        hornhit(b, steps_=(6, 14) if ph % 4 != 3 else (2, 6, 12, 14),
                gain=0.64, bright=1.15)
for b in (104, 112, 120, 128, 132):
    s.place(s.pos(b), bcrash(26, gain=0.78), 1.0, 'drums')
for b, kind in ((107, 'stutter'), (111, 'roll'), (115, 'toms'), (119, 'kicks'),
                (123, 'roll'), (127, 'stutter'), (131, 'toms'), (135, 'roll')):
    fill(s, b, kind, gain=0.95, seed=b)

# ================= the second wind-up: 136-143 =================
for b in range(136, 144):
    ph = b - 136
    kitbar(s, b, BIG if ph < 4 else STRIPPED, gain=1.0, swing=0.56, seed=b,
           tune=KICK_TUNE, hats=1.0 + 0.05 * ph)
    bass(b, gain=1.0, fuzz=6.4, cut=2600)
    organ(b, gain=0.40, hits=STABS)
accel(s, s.pos(136), _stab, total_steps=64.0, step0=2.0, step1=0.5,
      gain=0.58, bus='gtr')
accel(s, s.pos(140), _stab, total_steps=64.0, step0=1.0, step1=0.25,
      gain=0.66, bus='gtr', rise=2.0)
for i, b in enumerate((136, 138, 140, 141, 142, 143)):
    say(b, 'S', gain=0.48 + 0.04 * i, bars=1)
s.place(s.pos(140), stab_riser(64, gain=1.0, f0=250, f1=7600), 1.0, 'fx')
fill(s, 143, 'roll', gain=1.0, seed=143)
s.place(s.pos(143, 12), subdrop(8, f0=200, f1=28, gain=0.9, drive=1.8), 1.0, 'fx')

# ================= FINAL: 144-167 =================
for b in range(144, 168):
    ph = b - 144
    kitbar(s, b, BIG, gain=1.06, swing=0.56, seed=b, tune=KICK_TUNE, fat=1.2)
    gtr(b, gain=0.92, dirt=0.44, bright=1.1)
    bass(b, gain=1.08, fuzz=6.8, cut=3000)
    if ph % 8 != 7:
        organ(b, gain=0.46, hits=STABS if ph % 4 != 3 else STABS_B)
    if ph % 4 == 0:
        say(b, 'A' if (ph // 4) % 2 == 0 else 'B', gain=0.78)
    hornhit(b, steps_=(6, 14) if ph % 4 != 3 else (2, 6, 12, 14),
            gain=0.68, bright=1.2)
for b in (144, 152, 160):
    s.place(s.pos(b), bcrash(28, gain=0.8), 1.0, 'drums')
for b, kind in ((147, 'stutter'), (151, 'roll'), (155, 'toms'), (159, 'kicks'),
                (163, 'roll'), (167, 'roll')):
    fill(s, b, kind, gain=0.95, seed=b)
s.place(s.pos(158, 12), scratch(twang(67, 4, take=3), cycles=3.5, depth=2.2),
        0.78, 'fx')

# ================= outro: 168-175 =================
for b in range(168, 176):
    ph = b - 168
    kitbar(s, b, BREAK if ph < 4 else STRIPPED, gain=1.0 - 0.09 * ph,
           swing=0.56, seed=b, tune=KICK_TUNE, hats=1.0 - 0.09 * ph)
    if ph < 6:
        gtr(b, gain=0.85 - 0.10 * ph, dirt=0.34 - 0.04 * ph)
        bass(b, gain=1.0 - 0.13 * ph, fuzz=6.0 - 0.4 * ph, cut=2600 - 260 * ph)
        organ(b, gain=0.42 - 0.06 * ph, hits=STABS)
    if ph == 0:
        say(b, 'A', gain=0.70)
    if ph == 4:
        say(b, 'S', gain=0.46, bars=1)
s.place(s.pos(168), bcrash(26, gain=0.7), 1.0, 'drums')
s.place(s.pos(168), crackle(8 * 16, gain=0.8), 1.0, 'fx')
s.place(s.pos(173), spin(_loop, r0=1.0, r1=0.2, curve=0.8), 0.45, 'gtr')

# ---- the two holes ----
gap(s, 55, st=13.0, length=3.0)
gap(s, 103, st=12.5, length=3.5)

# ---- the room, the spring, the sampler and the compressor ----
# Crush first, because the sampler saw a clean loop and the 12-bit error has
# to be made of the drums; then the room, because the room was there before
# the sampler; then squash, because the pump has to breathe around the whole
# thing including its tail. Release is a sixteenth at 153.
s.bus['drums'] = crush(s.bus['drums'], bits=11, sr_div=2, pre=13500)
s.bus['drums'] = s.bus['drums'] + room(s.bus['drums'], decay=0.58, wet=0.22,
                                       tone=5400, hp_hz=260)
s.bus['drums'] = squash(s.bus['drums'], thresh=0.33, ratio=6.0, attack=0.014,
                        release=0.098, mix=0.62, report='drums')
s.bus['drums'] = shelf(sat(s.bus['drums'], 1.30), 8000, -1.5)
s.bus['drums'] = peak_eq(s.bus['drums'], 235, -2.2, width=0.45)
s.bus['drums'] = mono_below(s.bus['drums'], 110)

s.bus['bass'] = squash(s.bus['bass'], thresh=0.38, ratio=3.5, attack=0.020,
                       release=0.098, mix=0.5, report='bass')
s.bus['bass'] = peak_eq(s.bus['bass'], 215, -2.8, width=0.55)
s.bus['bass'] = mono_below(s.bus['bass'], 130)

# The guitar gets the spring and nothing else. It is the only voice on the
# record with a reverb of its own, which is what puts it in a different room
# from the drums - and that separation is most of why a surf loop over a
# breakbeat sounds like two records rather than one arrangement.
s.bus['gtr'] = crush(s.bus['gtr'], bits=12)
s.bus['gtr'] = s.bus['gtr'] + spring(s.bus['gtr'], decay=1.6, wet=0.42,
                                     tone=4300, boing=1.0)
s.bus['gtr'] = squash(s.bus['gtr'], thresh=0.30, ratio=4.0, attack=0.012,
                      release=0.098, mix=0.7)

s.bus['keys'] = crush(s.bus['keys'], bits=11)
s.bus['keys'] = peak_eq(s.bus['keys'], 620, 2.2, width=0.6)
s.bus['keys'] = reverb(s.bus['keys'], decay=1.2, wet=0.15, tone=5600)[:s.total]
s.bus['horn'] = reverb(s.bus['horn'], decay=1.3, wet=0.20, tone=5000)[:s.total]
s.bus['vox'] = peak_eq(hp(s.bus['vox'], 170, order=2), 1600, 2.6, width=0.6)
s.bus['vox'] = squash(s.bus['vox'], thresh=0.34, ratio=4.0, attack=0.008,
                      release=0.098, mix=0.8)
s.bus['vox'] = s.bus['vox'] + reverb(s.bus['vox'], decay=1.0, wet=0.14,
                                     tone=5200)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=2.0, wet=0.26, tone=4800)[:s.total]

for bus in ('drums', 'bass', 'keys', 'gtr'):
    sweep_bars(s.bus[bus], 0, 8, 320, 16000, curve=0.55)
    sweep_bars(s.bus[bus], 48, 54, 900, 16000, curve=1.5)
    sweep_bars(s.bus[bus], 136, 144, 900, 16000, curve=1.6)
sweep_bars(s.bus['drums'], 175.4, 176.0, 12000, 400, curve=1.0)

GAINS = {'drums': 0.68, 'bass': 0.44, 'gtr': 0.46, 'keys': 0.40,
         'horn': 0.46, 'vox': 0.46, 'fx': 0.38}
s.report(GAINS)
s.render('bigbeat_molotilka_153.wav', drive=0.60, duck=0.16, clip=1.45,
         limit=0.90, peak=0.86, fade=1.6, gains=GAINS)
