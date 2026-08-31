"""ASCENSION - industrial hardstyle at 170 BPM, A minor. Four on the floor
with a kick that has been through the whole distortion chain, the bass
swelling in every gap it leaves, and a breakdown that has to earn the drop it
walks into.

    intro | build | DROP 1 | breakdown | DROP 2 | bridge | FINAL DROP | outro
"""
import numpy as np
from hardlib import *

np.random.seed(2077)

# ---- the hook: Am - F - C - G ----
HOOK = [
    [(0, 69), (3, 72), (6, 76), (8, 74), (11, 72), (14, 69)],
    [(0, 72), (3, 74), (6, 77), (8, 74), (11, 72), (14, 69)],
    [(0, 76), (3, 79), (6, 76), (8, 72), (11, 74), (14, 76)],
    [(0, 74), (3, 71), (6, 74), (8, 79), (11, 76), (14, 74)],
]
CHORDS = [[57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62]]
ROOTS = [33, 29, 36, 31]                       # A1 F1 C2 G1
KICKTUNE = [55.0, 55.0, 55.0, 55.0]            # the kick stays on A: it is the floor

s = Session(108, tail=3.0)

def hook(b):
    """the bar's notes as (step, note, gap)"""
    bar = HOOK[b % 4]
    return [(st, n, (bar[i + 1][0] if i + 1 < len(bar) else 16) - st)
            for i, (st, n) in enumerate(bar)]

def four(b, gain=1.0, tune=None, roll=None, decay=0.28, drive=9.0, mid=2.8,
         lpf=None, raw=0.5, scream=0.35):
    """four on the floor; roll = the list of steps to hit instead"""
    hits = list(roll) if roll else [0, 4, 8, 12]
    for st in hits:
        t = s.pos(b, st)
        s.hit(t)
        k = hardkick(tune=tune or KICKTUNE[b % 4], decay=decay, drive=drive, mid=mid,
                     raw=raw, scream=scream)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')

def offbeat(b, gain=1.0, cutoff=850, drive=2.2, steps_=(2, 6, 10, 14), dur=2.0):
    for st in steps_:
        s.place(s.pos(b, st), revbass(ROOTS[b % 4], dur, cutoff=cutoff, drive=drive), gain, 'bass')

def tops(b, gain=1.0, claps=(4, 12), closed=True, open_=(2, 6, 10, 14)):
    for st in claps:
        s.place(s.pos(b, st), clap(3.5), gain * 0.85, 'drums')
    if closed:
        for i in range(16):
            if i % 2:
                s.place(s.pos(b, i), hat(0.7), gain * 0.5, 'drums')
    for st in open_:
        s.place(s.pos(b, st), hat(2.2, open_=True), gain * 0.55, 'drums')

def lead(b, gain=1.0, drive=6.0, octave=0, f0=3200, f1=700, bus='music'):
    for st, note, gap in hook(b):
        s.place(s.pos(b, st), screech(note + octave, min(gap * 0.95, 4), drive=drive,
                                      f0=f0, f1=f1), gain, bus)

# ================= intro: 0-7 =================
s.place(s.pos(0), supersaw([midi(n) for n in CHORDS[0]], 32, gain=0.35, cutoff=2600,
                           attack=0.9, release=0.6), 1.0, 'pad')
s.place(s.pos(2), supersaw([midi(n) for n in CHORDS[3]], 32, gain=0.35, cutoff=2600,
                           attack=0.9, release=0.6), 1.0, 'pad')
s.place(s.pos(0), crash808(24, gain=0.5), 1.0, 'fx')
for b in range(4, 8):
    four(b, gain=0.55, lpf=200 + 260 * (b - 4), raw=0.2, scream=0.0)
    tops(b, gain=0.3, claps=(), closed=False, open_=(2, 6, 10, 14))
s.place(s.pos(4), supersaw([midi(n) for n in CHORDS[0]], 64, gain=0.4, cutoff=3200,
                           attack=0.6, release=0.5), 1.0, 'pad')
s.place(s.pos(6, 8), shout(4, note=57, gain=0.7), 1.0, 'fx')
s.place(s.pos(7), riser(16, gain=0.75, f0=200, f1=1100), 1.0, 'fx')

# ================= build: 8-15 =================
for b in range(8, 16):
    four(b, gain=0.9, raw=0.35, scream=0.2)
    offbeat(b, gain=0.75 if b < 12 else 0.9, cutoff=650 if b < 12 else 850)
    tops(b, gain=0.55 if b < 12 else 0.75, claps=(4, 12) if b >= 12 else ())
    if b >= 12:
        lead(b, gain=0.45, drive=4.5, f0=2400, f1=900)
s.place(s.pos(14), riser(32, gain=0.9, f0=180, f1=1600), 1.0, 'fx')
s.place(s.pos(15, 8), reverse_crash(8, gain=0.9), 1.0, 'fx')
s.place(s.pos(15, 12), shout(4, note=60, gain=0.8), 1.0, 'fx')

# ================= DROP 1: 16-31 =================
for b in range(16, 32):
    ph = b - 16
    roll = None
    if ph % 8 == 7:
        roll = [0, 4, 8, 10, 12, 13, 14, 15]
    four(b, gain=1.0, roll=roll, drive=11.0, raw=0.8, scream=0.5)
    offbeat(b, gain=1.0)
    tops(b, gain=0.9)
    lead(b, gain=0.7, drive=6.0)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.75), 1.0, 'drums')
    if ph >= 8:
        s.place(s.pos(b), supersaw([midi(n) for n in CHORDS[b % 4]], 16, gain=0.28,
                                   cutoff=5000, attack=0.02, release=0.1), 1.0, 'pad')
s.place(s.pos(23, 12), shout(4, note=64, gain=0.6), 1.0, 'fx')
s.place(s.pos(31, 8), whoosh(8, gain=0.85), 1.0, 'fx')

# ================= breakdown: 32-47 =================
s.place(s.pos(32), downlifter(16, gain=0.9), 1.0, 'fx')
for i, b in enumerate(range(32, 40, 2)):
    ch = [midi(n) for n in CHORDS[i % 4]]
    s.place(s.pos(b), supersaw(ch, 32, gain=0.5, cutoff=4200, attack=0.35, release=0.6,
                               sub=0.25), 1.0, 'pad')
for b in range(32, 40):                                  # the hook, sung wide and slow
    for st, note, gap in hook(b)[::2]:
        seg = supersaw([midi(note)], min(gap * 1.7, 8), gain=0.42, cutoff=6000,
                       attack=0.03, release=0.25, detune=0.016)
        s.place(s.pos(b, st), reverb(seg, decay=3.0, wet=0.4, tone=5200), 1.0, 'music')
for b in range(36, 40):
    tops(b, gain=0.45, claps=(4, 12), closed=False, open_=())
s.place(s.pos(38), shout(4, note=57, gain=0.6), 1.0, 'fx')

for b in range(40, 44):                                  # gated, the floor coming back
    ch = [midi(n) for n in CHORDS[b % 4]]
    s.place(s.pos(b), gate(supersaw(ch, 16, gain=0.55, cutoff=5200, attack=0.02,
                                    release=0.05), 1.0, duty=0.5), 1.0, 'pad')
    tops(b, gain=0.6, claps=(4, 12), closed=True, open_=(6, 14))
    offbeat(b, gain=0.5, cutoff=520)
for b in range(44, 48):                                  # the last four bars of nerves
    ph = b - 44
    ch = [midi(n) for n in CHORDS[b % 4]]
    s.place(s.pos(b), gate(supersaw(ch, 16, gain=0.6, cutoff=5600, attack=0.02,
                                    release=0.05), (1.0, 1.0, 0.5, 0.5)[ph], duty=0.5), 1.0, 'pad')
    div = (2, 1, 1, 0.5)[ph]
    st = 0.0
    while st < 16:
        s.place(s.pos(b, st), lp(clap(2.5, spread=0.4), 6000),
                0.3 + 0.35 * (st / 16) + 0.05 * ph, 'drums')
        st += div
    four(b, gain=0.85, raw=0.5 + 0.15 * ph, scream=0.3,
         roll=[0, 4, 8, 12] if ph < 3 else [0, 2, 4, 6, 8, 10, 12, 14])
s.place(s.pos(44), riser(64, gain=1.0, f0=160, f1=1900), 1.0, 'fx')
s.place(s.pos(47, 8), reverse_crash(8, gain=1.0), 1.0, 'fx')
s.place(s.pos(47, 12), shout(4, note=69, gain=0.9), 1.0, 'fx')

# ================= DROP 2: 48-63 =================
for b in range(48, 64):
    ph = b - 48
    roll = [0, 4, 8, 10, 12, 13, 14, 15] if ph % 8 == 7 else None
    four(b, gain=1.0, roll=roll, drive=12.0, raw=0.9, scream=0.55)
    offbeat(b, gain=1.0, cutoff=950)
    tops(b, gain=0.95)
    lead(b, gain=0.72, drive=6.5)
    lead(b, gain=0.3, octave=-12, drive=5.0, f0=1800, f1=500)
    s.place(s.pos(b), supersaw([midi(n) for n in CHORDS[b % 4]], 16, gain=0.3,
                               cutoff=5200, attack=0.02, release=0.1), 1.0, 'pad')
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.8), 1.0, 'drums')
s.place(s.pos(55, 12), shout(4, note=72, gain=0.7), 1.0, 'fx')
s.place(s.pos(63, 8), whoosh(8, gain=0.9), 1.0, 'fx')

# ================= bridge: 64-71 =================
s.place(s.pos(64), downlifter(14, gain=0.9), 1.0, 'fx')
for b in range(64, 72):
    ch = [midi(n) for n in CHORDS[b % 4]]
    s.place(s.pos(b), gate(supersaw(ch, 16, gain=0.5, cutoff=4000 + 220 * (b - 64),
                                    attack=0.02, release=0.06), 1.0, duty=0.45), 1.0, 'pad')
    four(b, gain=0.5 + 0.07 * (b - 64), roll=[0, 8] if b < 68 else [0, 4, 8, 12],
         lpf=500 + 400 * (b - 64))
    tops(b, gain=0.4 + 0.07 * (b - 64), claps=(4, 12), closed=b >= 68, open_=(6, 14))
    if b >= 68:
        lead(b, gain=0.4 + 0.1 * (b - 68), drive=5.0, f0=2200, f1=800)
s.place(s.pos(68), riser(64, gain=1.0, f0=170, f1=2000), 1.0, 'fx')
s.place(s.pos(70), shout(4, note=64, gain=0.7), 1.0, 'fx')
s.place(s.pos(71, 12), reverse_crash(4, gain=1.0), 1.0, 'fx')

# ================= FINAL DROP: 72-95 =================
for b in range(72, 104):
    ph = b - 72
    roll = None
    if ph % 8 == 7:
        roll = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15]
    elif ph >= 16 and ph % 4 == 3:
        roll = [0, 4, 8, 10, 12, 14]
    four(b, gain=1.0, roll=roll, drive=13.0, mid=3.2, raw=1.0, scream=0.6, decay=0.26)
    offbeat(b, gain=1.0, cutoff=1000, drive=2.6)
    tops(b, gain=1.0)
    lead(b, gain=0.75, drive=7.0)
    lead(b, gain=0.32, octave=-12, drive=5.0, f0=1800, f1=500)
    s.place(s.pos(b), supersaw([midi(n) for n in CHORDS[b % 4]], 16, gain=0.34,
                               cutoff=5600, attack=0.02, release=0.1), 1.0, 'pad')
    if ph >= 8:                                          # the hook goes up top as well
        for st, note, gap in hook(b):
            s.place(s.pos(b, st), supersaw([midi(note + 12)], min(gap * 0.9, 3),
                                           gain=0.16, cutoff=7000, attack=0.006,
                                           release=0.06, detune=0.02), 1.0, 'music')
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.85), 1.0, 'drums')
s.place(s.pos(79, 12), shout(4, note=76, gain=0.8), 1.0, 'fx')
s.place(s.pos(87, 12), shout(4, note=69, gain=0.8), 1.0, 'fx')
s.place(s.pos(95, 12), shout(4, note=72, gain=0.85), 1.0, 'fx')

# ================= outro: 96-99 =================
s.place(s.pos(104), crash808(28, gain=0.7), 1.0, 'fx')
for b in range(104, 108):
    four(b, gain=0.8 - 0.18 * (b - 104), lpf=3000 - 700 * (b - 104), raw=0.3, scream=0.1)
    tops(b, gain=0.5 - 0.12 * (b - 104), claps=(4, 12), closed=False, open_=(6, 14))
    s.place(s.pos(b), supersaw([midi(n) for n in CHORDS[b % 4]], 16, gain=0.35,
                               cutoff=3000, attack=0.05, release=0.3), 1.0, 'pad')
s.place(s.pos(107), downlifter(16, gain=0.8), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['music'] = reverb(s.bus['music'], decay=1.6, wet=0.2, tone=6000)[:s.total]
s.bus['pad'] = reverb(s.bus['pad'], decay=2.6, wet=0.3, tone=5500)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=2.8, wet=0.35, tone=5000)[:s.total]
s.bus['drums'] = softclip(s.bus['drums'], 1.3)
for b in ('drums', 'music', 'fx'):
    s.bus[b] = shelf(s.bus[b], 9000, -1.5)

GAINS = {'drums': 1.4, 'bass': 0.66, 'music': 0.78, 'pad': 0.45, 'fx': 0.65}
s.report(GAINS)
s.render('hard_ascension_170.wav', drive=1.3, duck=0.08, limit=0.88, peak=0.95,
         fade=1.5, gains=GAINS)
