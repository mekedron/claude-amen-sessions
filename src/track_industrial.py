"""MORGENGRAUEN - industrial techno at 152 BPM, F minor / F Phrygian.

Morgengrauen is German for daybreak. It also literally reads as "morning
horror", which is the correct name for the eighth hour of a night out: the
sun is up outside and nobody in the room has agreed to that yet. This is the
record that plays then - not a peak-time banger, the one after it, when the
job is no longer to lift the floor but to finish it.

The kick is tuned to F1 (43.65 Hz) and never leaves. Under it sits the same
kick thrown into a dark room and driven into a continuous growl - the rumble
is the bass part; there is no bassline. Over it, a 303 in F Phrygian, a metal
shop for percussion, and a siren.

    COLD OPEN | THE FLOOR | LOCK | ACID RISE | VOID | BUILD
              | PEAK (48) | TUNNEL | ANNIHILATION (48) | OUTRO

228 bars, 6:00. The lowest point is bar 72 and bar 152; the last 48 bars are
the highest, and they start at 74% of the way through, which is where a peak
belongs.
"""
import numpy as np
from industriallib import *

np.random.seed(1952)

# ---- the material ----
ROOT = 43.65                                   # F1 - the kick, and the floor
Fm   = [midi(n) for n in (53, 56, 60)]         # i
Gb   = [midi(n) for n in (54, 58, 61)]         # bII - the Phrygian knife
Ab   = [midi(n) for n in (56, 60, 63)]         # bIII

# 303 lines: (step, note, dur_steps, accent, slide). F Phrygian from F3=53.
ACID_A = [(0, 53, 2, 1, 0), (2, 53, 1, 0, 0), (3, 65, 1.5, 0, 1), (5, 53, 1, 0, 0),
          (6, 56, 2, 0, 0), (8, 53, 2, 1, 0), (10, 60, 1, 0, 0), (11, 53, 1, 0, 0),
          (13, 61, 1.5, 0, 1), (15, 54, 1, 0, 0)]
ACID_B = [(0, 53, 1.5, 1, 0), (2, 60, 1, 0, 0), (3, 53, 1, 0, 0), (4, 56, 1, 0, 0),
          (5, 65, 1.5, 1, 1), (7, 53, 1, 0, 0), (8, 53, 1.5, 0, 0), (10, 61, 1, 0, 1),
          (11, 60, 1, 0, 0), (12, 56, 1, 0, 0), (13, 53, 1, 0, 0), (14, 58, 2, 1, 0)]
ACID_C = [(0, 53, 1, 1, 0), (1, 53, 1, 0, 0), (2, 54, 1, 0, 1), (3, 53, 1, 0, 0),
          (4, 65, 1.5, 1, 0), (6, 60, 1, 0, 0), (7, 56, 1, 0, 0), (8, 53, 1, 1, 0),
          (9, 53, 1, 0, 0), (10, 61, 1.5, 0, 1), (12, 58, 1, 0, 0), (13, 56, 1, 0, 0),
          (14, 53, 2, 1, 0)]

# metal-shop patterns: (step, note, gain) - rotated every 8 bars so the loop
# never sits still for longer than the ear will allow
METAL = [
    [(3, 72, 0.55), (7, 67, 0.4), (11, 75, 0.5), (14, 67, 0.35)],
    [(2, 75, 0.45), (6, 72, 0.5), (10, 67, 0.4), (13, 79, 0.45), (15, 72, 0.3)],
    [(1, 67, 0.35), (3, 72, 0.5), (6, 79, 0.4), (9, 72, 0.45), (11, 75, 0.5), (14, 67, 0.35)],
    [(3, 79, 0.5), (5, 72, 0.35), (7, 75, 0.45), (10, 67, 0.4), (12, 72, 0.3), (15, 75, 0.5)],
]

s = Session(228, tail=4.0)

# ---- the parts ----
def floor(b, gain=1.0, steps_=(0, 4, 8, 12), lpf=None, rum=1.0, tune=ROOT,
          drive=6.5, decay=0.19, grit=0.35, rdecay=1.1, rdrive=2.6):
    """kick and its room. Register every hit: the rumble has to duck to it."""
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = techkick(tune=tune, drive=drive, decay=decay, grit=grit)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if rum:
            r = rumble(tune=tune, decay=rdecay, drive=rdrive)
            if lpf:
                r = lp(r, min(lpf * 1.6, 900))
            s.place(t, r, rum, 'rumble')

def tops(b, gain=1.0, sixteenths=True, opens=(), claps=(4, 12), clapg=0.70):
    for st in claps:
        s.place(s.pos(b, st), distclap(3.0), gain * clapg, 'drums')
    if sixteenths:
        for i in range(16):
            if i % 4 == 0:
                continue                                  # the kick owns the beat
            v = 0.62 if i % 2 else 0.38                   # loud/soft: the cheapest groove
            s.place(s.pos(b, i), metalhat(0.7), gain * v * 0.9, 'drums')
    for st in opens:
        s.place(s.pos(b, st), metalhat(3.2, open_=True), gain * 0.42, 'drums')

def metal(b, idx=0, gain=1.0):
    for st, note, g in METAL[idx % len(METAL)]:
        s.place(s.pos(b, st), anvil(note, 2.6, seed=note), gain * g, 'music')

def offbeat(b, gain=1.0, cutoff=430, note=41, steps_=(2, 6, 10, 14), dur=2.0):
    for st in steps_:
        s.place(s.pos(b, st), distbass(note, dur, cutoff=cutoff), gain, 'bass')

def acidbar(b, pat, gain=1.0, f_hi=5000, f_lo=330, res=4.0, drive=4.0, low=230,
            octave=0):
    p = pat if not octave else [(st, n + octave, d, a, sl) for st, n, d, a, sl in pat]
    s.place(s.pos(b), acid(p, f_lo=f_lo, f_hi=f_hi, res=res, drive=drive, low=low),
            gain, 'acid')

def stabs(b, chord, gain=1.0, steps_=(2, 6, 10, 14), dur=1.6, drive=7.0):
    for st in steps_:
        s.place(s.pos(b, st), stab(tuple(chord), dur, drive=drive), gain, 'music')

ARPN = [53, 56, 60, 63]                        # Fm7 - the pool the arp walks

def arpline(b0, bars, gain=1.0, cycle=7, shape='updown', rate=1.0, octaves=(1,),
            gate=(1, 1, 0, 1, 1, 1, 0), ratchets=(3,), f_hi=6800, f_lo=360,
            decay=0.10, res=1.7, seed=0, bus='music'):
    """The machine sequence. cycle=7 over a sixteen-step bar is the whole
    point: the pattern starts on a different note every bar and only comes
    home on bar 7, so eight bars of it are eight different bars. Generated a
    phrase at a time so the walk actually carries across the bar line."""
    for st, note, dur, vel in arp_seq(ARPN, bars=bars, shape=shape, rate=rate,
                                      cycle=cycle, octaves=octaves, gate=gate,
                                      ratchets=ratchets, accents=(0, 4), tail=0.9,
                                      jitter=0.012, seed=seed):
        s_ = arpvoice(midi(note), round(dur, 3), f_lo=f_lo, f_hi=f_hi, res=res,
                      decay=decay)
        s.place(s.pos(b0, st), s_, gain * vel, bus)

def chord_of(b):
    """i for three bars, bII on the fourth - Phrygian, and one chord change is
    already a lot for this genre"""
    return Gb if b % 8 == 7 else (Ab if b % 8 == 3 else Fm)

# ================= COLD OPEN: 0-15 =================
s.place(s.pos(0), tunnel(64, note=41, gain=1.5, motor=0.3), 1.0, 'air')
for b in range(0, 16, 4):
    s.place(s.pos(b), grind(64, note=41, gain=2.2, res=0.8, seed=b), 1.0, 'air')
s.place(s.pos(2), alarm(48, f0=150, f1=380, cycles=1.5, gain=0.5), 1.0, 'fx')
for b in range(4, 8):                                     # the room before the machine
    floor(b, gain=0.0, rum=0.42, lpf=170, rdecay=1.4)
for b in range(8, 16):
    u = (b - 8) / 7
    floor(b, gain=0.35 + 0.35 * u, lpf=200 + 420 * (b - 8), rum=0.55 + 0.3 * u,
          grit=0.1, drive=5.0)
    tops(b, gain=0.22 + 0.2 * u, sixteenths=b >= 12, claps=(), opens=(6, 14))
s.place(s.pos(12), hammer(8, gain=0.8), 1.0, 'fx')
s.place(s.pos(15), steam(8, gain=0.7), 1.0, 'fx')
s.place(s.pos(15, 8), reverse_crash(8, gain=0.5), 1.0, 'fx')

# ================= THE FLOOR: 16-31 =================
for b in range(16, 32):
    ph = b - 16
    floor(b, gain=0.95, rum=0.95)
    tops(b, gain=0.62, claps=(), opens=(6, 14) if ph % 2 else (14,))
    if ph >= 8:
        metal(b, idx=0, gain=0.5)
    if b % 8 == 7:
        s.place(s.pos(b, 12), steam(4, gain=0.45, seed=b), 1.0, 'fx')
for b in range(16, 32, 4):
    s.place(s.pos(b), grind(64, note=41, gain=1.6, res=0.9, seed=b), 1.0, 'air')
s.place(s.pos(16), impact(24, gain=0.55), 1.0, 'fx')
s.place(s.pos(24), hammer(8, gain=0.85, seed=1), 1.0, 'fx')
kickroll(s, 31, [12, 13, 14, 15], gain=0.8, tune=ROOT, drive=7.0, decay=0.15, grit=0.4)

# ================= LOCK: 32-47 =================
for b in range(32, 48):
    ph = b - 32
    floor(b, gain=1.0, rum=1.0, drive=7.0)
    tops(b, gain=0.8, opens=(14,), claps=(4, 12), clapg=0.7)
    metal(b, idx=ph // 8, gain=0.72)
    offbeat(b, gain=0.5 if ph < 8 else 0.62, cutoff=380 if ph < 8 else 470)
    if ph % 8 == 6:
        s.place(s.pos(b, 8), servo(8, rate=20, accel=2.0, seed=b), 0.55, 'music')
for b in range(32, 48, 4):
    s.place(s.pos(b), grind(64, note=41, gain=1.5, res=1.0, seed=b + 3), 1.0, 'air')
s.place(s.pos(40), hammer(8, gain=0.85, seed=2), 1.0, 'fx')
s.place(s.pos(47), steam(6, gain=0.6, seed=47), 1.0, 'fx')
kickroll(s, 47, [8, 10, 12, 13, 14, 15], gain=0.9, drive=8.0, decay=0.15, grit=0.5)

# ================= ACID RISE: 48-71 =================
for b in range(48, 72):
    ph = b - 48
    u = min(ph / 15, 1.0)
    floor(b, gain=1.0, rum=1.0, drive=7.5)
    tops(b, gain=0.85, opens=(14,))
    metal(b, idx=(ph // 8) + 1, gain=0.7)
    offbeat(b, gain=0.6, cutoff=480)
    acidbar(b, ACID_A, gain=0.45 + 0.5 * u, f_hi=1500 + 3800 * u, res=3.2 + 1.4 * u,
            drive=3.4 + 1.0 * u)
    if ph >= 16:
        stabs(b, chord_of(b), gain=0.5, steps_=(6, 14))
    if ph % 8 == 7:
        s.place(s.pos(b, 12), steam(4, gain=0.5, seed=b), 1.0, 'fx')
for b in range(48, 72, 4):
    s.place(s.pos(b), grind(64, note=41, gain=1.3, res=1.0, seed=b + 7), 1.0, 'air')
s.place(s.pos(56), hammer(8, gain=0.9, seed=3), 1.0, 'fx')
s.place(s.pos(64), screamer(10, note=53, gain=0.6, vowel='eh', crush=7), 1.0, 'fx')
s.place(s.pos(64), impact(24, gain=0.5), 1.0, 'fx')
s.place(s.pos(71, 8), whoosh(8, gain=0.85), 1.0, 'fx')

# ================= VOID: 72-87 =================
# the kick stops. Everything the kick was hiding is suddenly the whole record.
s.place(s.pos(72), downlifter(16, gain=0.9), 1.0, 'fx')
s.place(s.pos(72), tunnel(128, note=41, gain=1.8, motor=0.15), 1.0, 'air')
for b in range(72, 88, 4):
    s.place(s.pos(b), grind(64, note=41, gain=3.0, res=1.3, crush=8, seed=b), 1.0, 'air')
s.place(s.pos(73), alarm(64, f0=170, f1=560, cycles=2.0, gain=0.85), 1.0, 'fx')
for b in range(72, 84):                                   # the acid, alone, opening up
    u = (b - 72) / 11
    acidbar(b, ACID_A, gain=0.72 + 0.26 * u, f_hi=1500 + 3900 * u,
            res=4.0 + 0.9 * u, drive=3.4 + 0.9 * u)
    if b >= 76:
        metal(b, idx=b // 4, gain=0.45)
s.place_echo(s.pos(79), acid(ACID_A, f_lo=330, f_hi=4400, res=4.6, drive=4.0, low=230),
             0.30, times=2, delay_steps=6.0, fb=0.45, bus='acid')
s.place(s.pos(83), stutter(acid(ACID_A, f_lo=330, f_hi=5200, res=4.6, drive=4.4, low=230),
                           slice_steps=2.0, repeats=7, decay=0.93, accel=1.18),
        0.55, 'acid')
s.place(s.pos(78), screamer(12, note=48, gain=0.7, vowel='oh', fall=5, crush=6), 1.0, 'fx')
s.place(s.pos(80), hammer(8, gain=0.9, seed=4), 1.0, 'fx')
for b in (80, 82):                                        # two kicks: a promise
    floor(b, gain=0.75, steps_=(0,), rum=0.8, lpf=1400)
for b in range(84, 88):                                   # the build inside the void
    ph = b - 84
    floor(b, gain=0.55 + 0.15 * ph, steps_=(0, 4, 8, 12), lpf=700 + 900 * ph, rum=0.7)
    tops(b, gain=0.4 + 0.15 * ph, claps=(4, 12), clapg=0.6)
    acidbar(b, ACID_A, gain=0.85, f_hi=4600, res=4.6)
    s.place(s.pos(b), servo(16, rate=14 + 8 * ph, accel=2.2, seed=b), 0.5 + 0.1 * ph, 'music')
s.place(s.pos(84), riser(64, gain=0.95, f0=170, f1=1700), 1.0, 'fx')
s.place(s.pos(87, 8), reverse_crash(8, gain=0.9), 1.0, 'fx')
s.place(s.pos(87, 12), screamer(4, note=60, gain=0.8, vowel='ah', crush=7), 1.0, 'fx')

# ================= BUILD: 88-103 =================
for b in range(88, 104):
    ph = b - 88
    u = ph / 15
    floor(b, gain=0.9 + 0.1 * u, rum=0.95, drive=7.5 + 1.5 * u)
    tops(b, gain=0.8 + 0.15 * u, opens=(14,))
    metal(b, idx=ph // 4, gain=0.7)
    offbeat(b, gain=0.65, cutoff=500)
    acidbar(b, ACID_A if ph < 8 else ACID_B, gain=0.9, f_hi=4800 + 600 * u,
            res=4.2, drive=4.2)
    stabs(b, chord_of(b), gain=0.55 + 0.2 * u, steps_=(2, 6, 10, 14) if ph >= 8 else (6, 14))
    if ph >= 12:                                          # the last four bars of nerves
        div = (2, 1, 1, 0.5)[ph - 12]
        st = 0.0
        while st < 16:
            s.place(s.pos(b, st), distclap(2.2), 0.3 + 0.3 * (st / 16), 'drums')
            st += div
        s.place(s.pos(b), servo(16, rate=18 + 10 * (ph - 12), accel=2.4, seed=b), 0.6, 'music')
s.place(s.pos(96), hammer(8, gain=0.9, seed=5), 1.0, 'fx')
s.place(s.pos(100), riser(64, gain=1.0, f0=160, f1=2000), 1.0, 'fx')
kickroll(s, 103, [0, 4, 8, 10, 12, 13, 14], gain=0.95, drive=9.0, decay=0.14,
         grit=0.6, climb=0.02)
s.place(s.pos(103, 15), np.zeros((int(STEP), 2), dtype=np.float32), 1.0, 'fx')  # the gap

# ================= PEAK: 104-151 =================
for b in range(104, 152):
    ph = b - 104
    roll = None
    if ph % 16 == 15:
        roll = [0, 4, 8, 10, 12, 14]
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=1.0, drive=8.5,
          decay=0.185, grit=0.5, rdrive=3.0)
    tops(b, gain=0.95, opens=(14,) if ph % 2 else (6, 14))
    metal(b, idx=ph // 8, gain=0.85)
    offbeat(b, gain=0.7, cutoff=520)
    acidbar(b, ACID_B if ph < 32 else ACID_C, gain=1.0,
            f_hi=5200 if ph < 32 else 5800, res=4.4, drive=4.4)
    stabs(b, chord_of(b), gain=0.72, drive=7.5)
    if ph % 8 == 4:
        s.place(s.pos(b, 8), servo(8, rate=24, accel=2.0, seed=b), 0.5, 'music')
for b in range(104, 152, 8):
    s.place(s.pos(b), grind(128, note=41, gain=1.2, res=1.0, seed=b), 1.0, 'air')
    s.place(s.pos(b), crash808(20, gain=0.5), 1.0, 'drums')
for b in (108, 124, 140):
    s.place(s.pos(b), hammer(8, gain=0.85, seed=b), 1.0, 'fx')
for b, note, vow in ((112, 53, 'eh'), (128, 60, 'ah'), (144, 56, 'eh')):
    s.place(s.pos(b, 12), screamer(6, note=note, gain=0.7, vowel=vow, crush=7), 1.0, 'fx')
for b in range(136, 152, 4):                              # the hoover: rave, at 8 a.m.
    ch = chord_of(b)
    s.place(s.pos(b, 8), hoover(ch[0] / 2, 4, gain=0.5), 1.0, 'music')
    s.place(s.pos(b + 2, 8), hoover(ch[1] / 2, 4, gain=0.42), 1.0, 'music')
for b0 in range(128, 152, 8):                             # the arp arrives, high and quiet
    arpline(b0, 8, gain=0.30, octaves=(1,), f_hi=7200, decay=0.075, res=1.4, seed=b0)
s.place(s.pos(151, 8), whoosh(8, gain=0.9), 1.0, 'fx')

# ================= TUNNEL: 152-167 =================
# take away the acid, the stabs and the clap. What is left has to be enough,
# and in this genre it is.
s.place(s.pos(152), downlifter(12, gain=0.75), 1.0, 'fx')
s.place(s.pos(152), tunnel(128, note=41, gain=1.5, motor=0.35), 1.0, 'air')
# The trough. The kick loses half its hits and all of its grit, the rumble
# shortens, and the arp - which has been a decoration until now - is suddenly
# the only thing playing a note. This has to be quiet or the last 48 bars
# have nothing to be louder than.
for b in range(152, 168):
    ph = b - 152
    u = ph / 15
    floor(b, gain=0.62 + 0.3 * u, steps_=(0, 8) if ph < 4 else (0, 4, 8, 12),
          rum=0.55 + 0.35 * u, drive=5.5 + 2.0 * u, grit=0.1 + 0.4 * u,
          rdecay=0.85, lpf=2200 + 700 * ph if ph < 8 else None)
    tops(b, gain=0.3 + 0.35 * u, sixteenths=ph >= 6, claps=() if ph < 10 else (12,),
         opens=(14,) if ph >= 4 else ())
    if ph >= 6:
        metal(b, idx=ph // 4, gain=0.4 + 0.03 * ph)
    if ph >= 12:
        offbeat(b, gain=0.45, cutoff=520)
for b0 in (152, 160):                                     # the arp carries the section
    arpline(b0, 8, gain=0.55 if b0 == 152 else 0.8, octaves=(0, 1),
            f_hi=3200 if b0 == 152 else 6200, decay=0.09, seed=b0)
for b in range(152, 168, 4):
    s.place(s.pos(b), grind(64, note=41, gain=1.5, res=1.0, seed=b + 2), 1.0, 'air')
s.place(s.pos(160), hammer(8, gain=0.75, seed=7), 1.0, 'fx')
s.place(s.pos(164), riser(64, gain=1.0, f0=150, f1=2200), 1.0, 'fx')
s.place(s.pos(166), alarm(32, f0=200, f1=620, cycles=1.0, gain=0.6), 1.0, 'fx')
for b in (164, 165, 166, 167):                            # the acid crawls back in
    acidbar(b, ACID_C, gain=0.3 + 0.22 * (b - 164), f_hi=900 + 1300 * (b - 164), res=4.0)
s.place(s.pos(167, 8), reverse_crash(8, gain=1.0), 1.0, 'fx')
s.place(s.pos(167, 12), screamer(4, note=65, gain=0.85, vowel='ah', crush=6), 1.0, 'fx')

# ================= ANNIHILATION: 168-215 =================
for b in range(168, 216):
    ph = b - 168
    roll = None
    if ph % 16 == 15:
        roll = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15]
    elif ph % 8 == 7:
        roll = [0, 4, 8, 10, 12, 14]
    elif ph >= 32 and ph % 4 == 3:
        roll = [0, 4, 6, 8, 12, 14]
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=1.0, drive=9.5,
          decay=0.18, grit=0.65, rdrive=3.2)
    tops(b, gain=1.0, opens=(6, 14))
    metal(b, idx=ph // 4, gain=0.9)
    offbeat(b, gain=0.75, cutoff=560)
    acidbar(b, ACID_C, gain=1.0, f_hi=6200, res=4.6, drive=4.8)
    if ph >= 8:                                           # the line doubled an octave up
        acidbar(b, ACID_C, gain=0.3, f_hi=7000, res=3.4, drive=3.6, low=520, octave=12)
    stabs(b, chord_of(b), gain=0.8, drive=8.0)
    if ph % 8 in (2, 6):
        s.place(s.pos(b, 8), servo(8, rate=26, accel=2.1, seed=b), 0.55, 'music')
for b in range(168, 216, 8):
    s.place(s.pos(b), grind(128, note=41, gain=1.3, res=1.1, seed=b + 5), 1.0, 'air')
    s.place(s.pos(b), crash808(20, gain=0.55), 1.0, 'drums')
for b in range(168, 216, 4):                              # the hoover hook, all the way out
    ch = chord_of(b)
    s.place(s.pos(b, 8), hoover(ch[0] / 2, 4, gain=0.55), 1.0, 'music')
    s.place(s.pos(b + 1, 12), hoover(ch[2] / 2, 3, gain=0.4), 1.0, 'music')
for b in (172, 188, 204):
    s.place(s.pos(b), hammer(8, gain=0.9, seed=b), 1.0, 'fx')
for b, note in ((176, 65), (192, 60), (208, 68)):
    s.place(s.pos(b, 12), screamer(6, note=note, gain=0.8, vowel='ah', crush=6), 1.0, 'fx')
s.place(s.pos(184), alarm(64, f0=190, f1=600, cycles=2.0, gain=0.55), 1.0, 'fx')
s.place(s.pos(200), alarm(64, f0=210, f1=680, cycles=2.0, gain=0.6), 1.0, 'fx')
for b0 in range(168, 216, 8):                             # full: two octaves, ratcheted
    arpline(b0, 8, gain=0.52, octaves=(0, 1), f_hi=7000, decay=0.095, res=1.8,
            ratchets=(3, 5), seed=b0)
s.place(s.pos(215, 8), whoosh(8, gain=0.9), 1.0, 'fx')

# ================= OUTRO: 216-227 =================
s.place(s.pos(216), tunnel(96, note=41, gain=1.7, motor=0.2), 1.0, 'air')
for b in range(216, 228, 4):
    s.place(s.pos(b), grind(64, note=41, gain=1.8, res=0.9, seed=b), 1.0, 'air')
for b in range(216, 228):
    ph = b - 216
    u = ph / 11
    floor(b, gain=0.95 - 0.55 * u, lpf=6000 - 480 * ph, rum=0.95 - 0.35 * u,
          drive=7.0, rdecay=1.3)
    tops(b, gain=0.7 - 0.5 * u, sixteenths=ph < 6, claps=(4, 12) if ph < 4 else (),
         opens=(14,) if ph < 8 else ())
    if ph < 6:
        metal(b, idx=ph // 2, gain=0.6 - 0.08 * ph)
    if ph < 4:
        acidbar(b, ACID_A, gain=0.7 - 0.15 * ph, f_hi=4000 - 700 * ph, res=3.8)
s.place(s.pos(216), hammer(8, gain=0.8, seed=9), 1.0, 'fx')
s.place(s.pos(224), hammer(10, gain=0.7, seed=10), 1.0, 'fx')
s.place(s.pos(224), alarm(48, f0=160, f1=330, cycles=1.0, gain=0.45), 1.0, 'fx')
s.place(s.pos(227), downlifter(16, gain=0.7), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.5, wet=0.20, tone=5200)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.0, wet=0.32, tone=4200)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.6, wet=0.22, tone=3200)
s.bus['acid']  = bus_reverb(s.bus['acid'],  decay=0.9, wet=0.12, tone=4600)
s.bus['air'] = hp(s.bus['air'], 58)                              # the kick owns 20-60
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.85)
s.bus['rumble'] = softclip(s.bus['rumble'], 1.05, knee=0.85)
# Everything with weight goes mono under 110 Hz. Reverb tails and Haas
# delays had leaked 39% of the sub into the side channel, which a club
# system that sums the bass would have cancelled on the night.
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)
for b in ('drums', 'music', 'fx', 'air'):
    s.bus[b] = shelf(s.bus[b], 9500, -1.5)
s.bus['acid'] = shelf(s.bus['acid'], 220, -2.0, kind='low')      # stay off the rumble

GAINS = {'drums': 0.80, 'rumble': 0.55, 'bass': 0.26, 'acid': 0.44,
         'music': 0.40, 'air': 0.34, 'fx': 0.38}
s.report(GAINS)
s.render('industrial_morgengrauen_152.wav', drive=1.0, duck=0.14, clip=1.10,
         limit=0.94, peak=0.95, fade=2.0, gains=GAINS)
