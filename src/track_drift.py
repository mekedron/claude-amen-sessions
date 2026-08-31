"""DRIFT PROTOCOL - drift phonk at 160 BPM, F# minor. No break, no samples:
the cowbell is two squares driven into tanh, the 808 is a gliding sine, and
the car is a saw stack whose firing rate climbs.

    intro | verse | DROP 1 | break | DROP 2 | the drift | DROP 3 | outro
"""
import numpy as np
from phonklib import *

np.random.seed(1969)

# ---- the riff: F#m - F#m - D - C#m, four bars of (step, note) ----
RIFF = [
    [(0, 66), (3, 66), (6, 69), (8, 66), (10, 73), (11, 71), (14, 69)],
    [(0, 66), (3, 66), (6, 69), (8, 73), (10, 76), (12, 73), (14, 71)],
    [(0, 69), (3, 69), (6, 74), (8, 69), (10, 66), (12, 69), (14, 71)],
    [(0, 73), (3, 73), (6, 76), (8, 73), (10, 71), (12, 69), (14, 68)],
]
ROOTS = [30, 30, 38, 37]                       # F#1 F#1 D2 C#2
CHORDS = [[42, 45, 49], [42, 45, 49], [38, 42, 45], [37, 41, 44]]

def riff(b):
    """the bar's notes as (step, note, gap): gap = steps until the next note"""
    bar = RIFF[b % 4]
    return [(st, note, (bar[i + 1][0] if i + 1 < len(bar) else 16) - st)
            for i, (st, note) in enumerate(bar)]

s = Session(96, tail=3.0)

def cowbells(b, gain=1.0, drive=6.0, decay=0.16, bright=1.0, folded=0.0,
             octave=0, double=False, pan=0.0, bus='music'):
    """one bar of the riff; double=True fills the gaps with 32nds"""
    bar = RIFF[b % 4]
    for i, (st, note) in enumerate(bar):
        seg = cowbell(note + octave, 2.4, drive=drive, decay=decay,
                      bright=bright, folded=folded)
        if pan:
            seg = panned(seg, pan)
        s.place(s.pos(b, st), seg, gain, bus)
        if double:
            seg2 = cowbell(note + octave + 12, 1.2, drive=drive * 0.8,
                           decay=decay * 0.5, bright=bright * 0.8)
            s.place(s.pos(b, st + 1.5), panned(seg2, 0.7 if i % 2 else -0.7),
                    gain * 0.32, bus)

def bassline(b, gain=1.0, drive=2.4, style='roll'):
    """808 under the bar: root, a mid hit, and a slide back to the root"""
    root = ROOTS[b % 4]
    if style == 'walk':
        for st, note in ((0, root), (4, root + 12), (8, root + 7), (12, root + 3)):
            s.place(s.pos(b, st), eight08(note, 3.6, drive=drive, decay=0.32), gain, 'bass')
        return
    s.place(s.pos(b, 0), eight08(root, 5.5, slide_from=root - 7, drive=drive, decay=0.5), gain, 'bass')
    s.place(s.pos(b, 6), eight08(root, 3.2, drive=drive, decay=0.3), gain * 0.85, 'bass')
    s.place(s.pos(b, 10), eight08(root, 5.0, slide_from=root - 5, drive=drive, decay=0.45), gain * 0.95, 'bass')

def drums(b, kicks=(0, 6, 10), snares=(8,), gain=1.0, hats=True, hat_gain=0.55,
          roll=None, ohat=(14,), rims=()):
    for st in kicks:
        t = s.pos(b, st)
        s.place(t, kick(4.5, punch=1.0), gain, 'drums')
        s.hit(t)
    for st in snares:
        s.place(s.pos(b, st), snare(3.5, gain=1.0), gain * 0.95, 'drums')
    for st in rims:
        s.place(s.pos(b, st), rim(), gain * 0.5, 'drums')
    if hats:
        for i in range(16):
            if roll and i >= roll:
                for k in (0, 0.5):
                    s.place(s.pos(b, i + k), lp(hat808(), 11000), hat_gain * 0.45, 'drums')
                continue
            accent = 1.0 if i % 4 == 0 else (0.75 if i % 2 == 0 else 0.55)
            jitter = int(np.random.uniform(-90, 90))
            s.place(s.pos(b, i) + jitter, hat808(), hat_gain * accent, 'drums')
        for st in ohat:
            s.place(s.pos(b, st), hat808(1, open_=True), hat_gain * 1.1, 'drums')

def chords(b, gain=1.0, dur=16, cut=3800):
    for st in (0,):
        s.place(s.pos(b, st), guitar(CHORDS[b % 4][0] - 12, 3.5, drive=8.0, cutoff=cut), gain, 'music')
        s.place(s.pos(b, 10), guitar(CHORDS[b % 4][0] - 12, 2.5, drive=8.0, cutoff=cut), gain * 0.7, 'music')

# ================= intro: 0-7 =================
s.place(s.pos(0), crackle(16 * 8, gain=0.9), 1.0, 'fx')
s.place(s.pos(0), engine(16 * 4, rpm0=34, rpm1=44, gain=0.5, grit=2.2), 1.0, 'fx')
s.place(s.pos(2), siren(16 * 2, f0=620, lfo=0.9, gain=0.22), 1.0, 'fx')
for b in range(4, 8):                                   # riff arrives through a filter
    for st, note in RIFF[b % 4]:
        seg = cowbell(note, 2.4, drive=4.0, decay=0.2)
        seg = lp(seg, 700 + 500 * (b - 4))
        s.place(s.pos(b, st), reverb(seg, decay=1.6, wet=0.5, tone=4200), 0.55, 'music')
s.place(s.pos(6, 8), whisper(6, gain=0.5, syllables=3), 1.0, 'fx')
s.place(s.pos(6), pad([midi(n) for n in CHORDS[2]], 32, cutoff=1200, gain=0.35, wide=0.9), 1.0, 'pad')
s.place(s.pos(7), riser(16, gain=0.7, f0=140, f1=900), 1.0, 'fx')
s.place(s.pos(7, 8), engine(8, rpm0=44, rpm1=105, gain=0.55, shape=1.6), 1.0, 'fx')

# ================= verse: 8-15 =================
for b in range(8, 16):
    cowbells(b, gain=0.72, drive=5.0, decay=0.15, bright=0.85)
    bassline(b, gain=0.8, drive=2.1)
    drums(b, kicks=(0, 6, 10), snares=(8,) if b >= 12 else (),
          gain=0.85, hat_gain=0.4 if b < 12 else 0.5,
          roll=14 if b == 15 else None)
s.place(s.pos(14), riser(32, gain=0.75, f0=180, f1=1400), 1.0, 'fx')
s.place(s.pos(15, 8), screech(8, gain=0.8), 1.0, 'fx')
s.place(s.pos(15, 12), reverse_crash(4, gain=0.9), 1.0, 'fx')

# ================= DROP 1: 16-31 =================
s.place(s.pos(16), bass_drop(14, note=30, gain=0.95), 1.0, 'bass')
for b in range(16, 32):
    ph = b - 16
    cowbells(b, gain=1.0, drive=6.5, decay=0.17, folded=0.15)
    bassline(b, gain=1.0, drive=2.5, style='walk' if ph % 8 == 7 else 'roll')
    drums(b, kicks=(0, 3, 6, 10) if ph % 4 == 3 else (0, 6, 10),
          snares=(8,), rims=(12,) if ph % 2 else (),
          roll=14 if ph % 8 == 7 else None)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(16, gain=0.8), 1.0, 'drums')
    if ph >= 8:
        chords(b, gain=0.5)
s.place(s.pos(23, 12), screech(6, gain=0.5), 1.0, 'fx')
s.place(s.pos(31, 8), whoosh(8, gain=0.8), 1.0, 'fx')
s.place(s.pos(31, 8), pitch_echo(cowbell(66, 2.4, drive=6.0), 1.5, 5, semis=(5, 12, 17, 24)), 0.5, 'fx')

# ================= break: 32-39 =================
s.place(s.pos(32), downlifter(12, gain=0.9), 1.0, 'fx')
s.place(s.pos(32), pad([midi(n) for n in CHORDS[0]], 32, cutoff=1100, gain=0.5, wide=0.9), 1.0, 'pad')
s.place(s.pos(34), pad([midi(n) for n in CHORDS[3]], 32, cutoff=1100, gain=0.5, wide=0.9), 1.0, 'pad')
s.place(s.pos(32), crackle(16 * 8, gain=0.7), 1.0, 'fx')
for i, b in enumerate((32, 33, 34, 35)):
    for st, note, gap in riff(b)[::3]:
        s.place(s.pos(b, st), reverb(chop(note - 12, min(gap * 1.4, 7), vowels=('ah', 'oo'),
                                          gain=0.5, grit=0.25), decay=2.4, wet=0.45, tone=3800),
                1.0, 'music')
s.place(s.pos(33), engine(16 * 2, rpm0=38, rpm1=96, gain=0.5, shape=1.8), 1.0, 'fx')
s.place(s.pos(34, 12), screech(10, gain=0.75), 1.0, 'fx')
for b in (34, 35):                                       # cowbell drifting away
    for st, note in RIFF[b % 4]:
        s.place(s.pos(b, st), lp(cowbell(note, 2.4, drive=4.5), 1600), 0.4, 'music')
s.place(s.pos(35, 8), tape_stop(np.concatenate(
    [cowbell(n, 2.4, drive=5.0) for n in (73, 71, 69, 66)]), 0.75), 0.6, 'music')

for b in range(36, 40):                                  # build back up
    ph = b - 36
    cowbells(b, gain=0.6 + 0.12 * ph, drive=5.0 + ph, decay=0.15, bright=0.8 + 0.1 * ph)
    bassline(b, gain=0.85, drive=2.2)
    drums(b, kicks=(0, 6, 10) if ph < 3 else (0, 4, 8, 12), snares=(8,),
          hat_gain=0.4 + 0.06 * ph, roll=12 if ph == 3 else None)
s.place(s.pos(38), riser(32, gain=0.85, f0=200, f1=1600), 1.0, 'fx')
s.place(s.pos(39, 8), reverse_crash(8, gain=1.0), 1.0, 'fx')

# ================= DROP 2: 40-55 =================
s.place(s.pos(40), bass_drop(14, note=30, gain=1.0), 1.0, 'bass')
for b in range(40, 56):
    ph = b - 40
    dbl = 48 <= b < 52                                   # four bars of 32nd cowbells
    cowbells(b, gain=1.0, drive=7.0, decay=0.17, folded=0.3, double=dbl)
    cowbells(b, gain=0.35, drive=5.0, decay=0.2, octave=-12, bright=0.7, pan=-0.35)
    bassline(b, gain=1.0, drive=2.7, style='walk' if ph % 8 == 7 else 'roll')
    drums(b, kicks=(0, 3, 6, 10, 14) if ph % 4 == 3 else (0, 6, 10),
          snares=(8,), rims=(4, 12) if ph % 2 else (),
          hat_gain=0.6, roll=12 if ph % 8 == 7 else None)
    chords(b, gain=0.6 if ph < 8 else 0.75)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(16, gain=0.85), 1.0, 'drums')
s.place(s.pos(47, 8), siren(16, f0=820, lfo=2.2, gain=0.3), 1.0, 'fx')
s.place(s.pos(47, 12), pitch_echo(cowbell(73, 2.4, drive=6.5), 1.0, 6, semis=(-5, 7, 12, 19)), 0.45, 'fx')
s.place(s.pos(55, 8), whoosh(8, gain=0.9), 1.0, 'fx')

# ================= the drift: 56-63 =================
s.place(s.pos(56), downlifter(14, gain=1.0), 1.0, 'fx')
s.place(s.pos(56), engine(16 * 3, rpm0=50, rpm1=135, gain=0.65, shape=1.3, grit=3.6), 1.0, 'fx')
s.place(s.pos(56), pad([midi(n) for n in CHORDS[0]], 48, cutoff=900, gain=0.55, wide=1.0), 1.0, 'pad')
s.place(s.pos(57), screech(20, gain=0.9, f0=980), 1.0, 'fx')
s.place(s.pos(58, 8), screech(12, gain=0.7, f0=1320), 1.0, 'fx')
for i in range(4):                                       # the riff, sung, half speed
    b = 56 + i
    for st, note, gap in riff(b)[::2]:
        s.place(s.pos(b, st), reverb(chop(note - 12, min(gap * 1.6, 6), vowels=('oh', 'ah'),
                                          gain=0.55, grit=0.2), decay=2.2, wet=0.4), 1.0, 'music')
s.place(s.pos(58), pitch_echo(chop(54, 4, vowels=('ah', 'ih'), gain=0.5), 2.0, 5,
                             semis=(12, 7, 19, 24), spread=0.95), 0.55, 'fx')
s.place(s.pos(59), tape_stop(np.concatenate(
    [cowbell(n, 2.4, drive=6.0) for n in (66, 69, 73, 76, 78)]), 0.9), 0.75, 'music')
for b in (60, 61, 62, 63):                               # the build
    ph = b - 60
    drums(b, kicks=(0, 8) if ph < 2 else (0, 4, 8, 12), snares=(), hats=False, gain=0.9)
    div = (4, 2, 1, 0.5)[ph]                             # snare roll doubling up
    st = 0.0
    while st < 16:
        roll = lp(snare(2.2, bright=0.5, body=1.25), 5200)
        s.place(s.pos(b, st), roll, (0.16 + 0.16 * (st / 16) + 0.05 * ph) * (0.7 if div < 1 else 1.0), 'drums')
        st += div
    cowbells(b, gain=0.5 + 0.15 * ph, drive=5.5, decay=0.14, bright=0.9)
s.place(s.pos(60), riser(64, gain=1.0, f0=160, f1=1800), 1.0, 'fx')
s.place(s.pos(62), whisper(16, gain=0.6, syllables=5), 1.0, 'fx')
s.place(s.pos(63, 12), reverse_crash(4, gain=1.0), 1.0, 'fx')

# ================= DROP 3, the big one: 64-87 =================
s.place(s.pos(64), bass_drop(16, note=30, gain=1.0), 1.0, 'bass')
for b in range(64, 88):
    ph = b - 64
    last = b >= 80                                       # the last eight go double time
    cowbells(b, gain=1.0, drive=7.5, decay=0.18, folded=0.4, double=last or ph % 8 >= 6)
    cowbells(b, gain=0.4, drive=5.5, decay=0.21, octave=-12, bright=0.7, pan=-0.4)
    cowbells(b, gain=0.22, drive=6.0, decay=0.13, octave=12, bright=1.1, pan=0.5)
    bassline(b, gain=1.0, drive=3.0, style='walk' if ph % 8 == 7 else 'roll')
    drums(b, kicks=(0, 3, 6, 10, 14) if last else ((0, 3, 6, 10) if ph % 2 else (0, 6, 10)),
          snares=(8,), rims=(4, 12) if ph % 2 else (), hat_gain=0.65,
          roll=12 if ph % 8 == 7 else None, ohat=(6, 14))
    chords(b, gain=0.85, cut=4600)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(16, gain=0.9), 1.0, 'drums')
    if ph >= 8:                                          # the lead sings the riff, in step
        for st, note, gap in riff(b):
            s.place(s.pos(b, st), lp(screamlead(note - 12, min(gap * 0.92, 3.0), drive=4.5), 5200),
                    0.28, 'music')
s.place(s.pos(72), siren(32, f0=880, lfo=2.6, gain=0.28), 1.0, 'fx')
s.place(s.pos(79, 8), screech(8, gain=0.85), 1.0, 'fx')
s.place(s.pos(79, 12), pitch_echo(cowbell(78, 2.4, drive=7.0), 0.75, 6, semis=(7, 12, 19, 24)), 0.4, 'fx')
s.place(s.pos(80), bass_drop(12, note=30, gain=0.8), 1.0, 'bass')

# ================= outro: 88-95 =================
s.place(s.pos(88), crackle(16 * 8, gain=1.0), 1.0, 'fx')
s.place(s.pos(88), downlifter(16, gain=0.9), 1.0, 'fx')
for b in range(88, 92):
    cowbells(b, gain=0.75 - 0.15 * (b - 88), drive=5.0, decay=0.16, bright=0.8 - 0.1 * (b - 88))
    bassline(b, gain=0.7, drive=2.0)
    drums(b, kicks=(0, 6, 10), snares=(8,), hat_gain=0.35, gain=0.8)
s.place(s.pos(92), tape_stop(np.concatenate(
    [cowbell(n, 2.4, drive=5.5) for n in (66, 69, 73, 71, 69, 66)]), 1.3), 0.7, 'music')
s.place(s.pos(92), engine(16 * 3, rpm0=110, rpm1=36, gain=0.5, shape=0.7), 1.0, 'fx')
s.place(s.pos(93), siren(16 * 2, f0=560, lfo=0.8, gain=0.16), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['music'] = reverb(s.bus['music'], decay=1.2, wet=0.14, tone=6500)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=2.4, wet=0.3, tone=5000)[:s.total]
for b in ('drums', 'music', 'fx'):
    s.bus[b] = shelf(s.bus[b], 8500, -3.0)
s.bus['drums'] = softclip(wow(s.bus['drums'], depth_ms=0.35, rate=0.4), 1.35)
s.bus['music'] = dirty(s.bus['music'], 1.15)
s.bus['bass'] = dirty(s.bus['bass'], 1.35)

GAINS = {'drums': 1.15, 'bass': 0.6, 'music': 0.92, 'pad': 0.8, 'fx': 0.75}
s.report(GAINS)
s.render('phonk_drift_160.wav', drive=1.0, duck=0.22, limit=0.93, peak=0.95, fade=1.5,
         gains=GAINS)
