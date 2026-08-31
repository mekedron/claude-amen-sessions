"""UNTERTAGE - industrial techno at 136 BPM, G minor / G harmonic minor.

Untertage is the German word for working underground - the word on a miner's
contract, not a metaphor. This is the shift: a machine that never stops, a
hall big enough to answer it, and a choir of men who have been in it for nine
hours.

The choir is the instrument. `labourchoir` divides the formants by `size`, and
a vocal tract scaled up does not read as a lower voice - it reads as a bigger
body, at the same pitch. That one number turns four saw stacks into something
the size of the room it is standing in, which is where the grotesque comes
from. They sag flat across every phrase because nobody is holding the pitch up
any more, and they answer the press rather than the beat.

Harmonically it is G minor with a harmonic-minor V, so the choir keeps walking
into the augmented second between Eb and F#: the interval that makes a church
chord sound wrong. A work song sung in a cathedral built for machines.

    DESCENT | SHIFT | MACHINE | CHANT | DEEPER | THE HOLLOW | PRESSURE
            | THE GREAT WORK | THE GROAN | COLLAPSE | SILT

192 bars, 5:38. Slower than Morgengrauen on purpose: at 136 the press has
room to ring, and everything sounds heavier than it is.
"""
import numpy as np
from industriallib import *

# 152 is this module's tempo; a heavier piece wants the same machine shop
# slower. set_tempo re-grids core and the module together - and `import *`
# copied the old BAR/STEP into this script, so take the new ones back.
BAR, STEP = set_tempo(136)
BPM = 136.0
np.random.seed(1936)

ROOT = 49.0                                    # G1 - the kick and the floor
Gm  = [midi(n) for n in (55, 58, 62)]          # i
Eb  = [midi(n) for n in (51, 55, 58)]          # bVI
Dma = [midi(n) for n in (50, 54, 57)]          # V of the harmonic minor - F# against Eb
Cm  = [midi(n) for n in (48, 51, 55)]          # iv
CHOIR = [Gm, Gm, Eb, Eb, Dma, Dma, Gm, Cm]     # two bars each: a 16-bar breath

# the machine's own line, low and monotonous
ACID_G = [(0, 55, 2, 1, 0), (2, 55, 1, 0, 0), (3, 62, 1.5, 0, 1), (5, 55, 1, 0, 0),
          (6, 58, 2, 0, 0), (8, 55, 2, 1, 0), (10, 63, 1, 0, 0), (11, 55, 1, 0, 0),
          (13, 66, 1.5, 0, 1), (15, 56, 1, 0, 0)]
METAL = [
    [(3, 67, 0.5), (7, 62, 0.38), (11, 70, 0.46), (14, 62, 0.32)],
    [(2, 70, 0.42), (6, 67, 0.46), (10, 62, 0.36), (13, 74, 0.42), (15, 67, 0.28)],
    [(1, 62, 0.32), (3, 67, 0.46), (6, 74, 0.36), (9, 67, 0.42), (12, 70, 0.46)],
    [(3, 74, 0.46), (5, 67, 0.32), (8, 70, 0.42), (11, 62, 0.36), (15, 70, 0.46)],
]

s = Session(192, tail=5.0)

def floor(b, gain=1.0, steps_=(0, 4, 8, 12), lpf=None, rum=1.0, drive=6.0,
          decay=0.24, grit=0.3, rdecay=1.1, rdrive=2.4):
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = techkick(dur_steps=2.6, tune=ROOT, drive=drive, decay=decay, grit=grit)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if rum:
            r = rumble(dur_steps=8, tune=ROOT, decay=rdecay, drive=rdrive)
            if lpf:
                r = lp(r, min(lpf * 1.6, 900))
            s.place(t, r, rum, 'rumble')

def tops(b, gain=1.0, sixteenths=True, opens=(), claps=(4, 12), clapg=0.62):
    for st in claps:
        s.place(s.pos(b, st), distclap(3.0), gain * clapg, 'drums')
    if sixteenths:
        for i in range(16):
            if i % 4 == 0:
                continue
            s.place(s.pos(b, i), metalhat(0.7), gain * (0.58 if i % 2 else 0.34), 'drums')
    for st in opens:
        s.place(s.pos(b, st), metalhat(3.2, open_=True), gain * 0.38, 'drums')

def metal(b, idx=0, gain=1.0):
    for st, note, g in METAL[idx % len(METAL)]:
        s.place(s.pos(b, st), anvil(note, 2.6, seed=note), gain * g, 'music')

def choir(b0, bars=2, chord=None, gain=1.0, vowel='oh', size=1.25, spread=20.0,
          rasp=0.16, attack=0.5, seed=0):
    ch = chord or CHOIR[(b0 // 2) % len(CHOIR)]
    s.place(s.pos(b0), labourchoir(tuple(ch), 16 * bars, vowel=vowel, size=size,
                                   spread=spread, rasp=rasp, attack=attack, seed=seed),
            gain, 'choir')

def workcall(b, gain=1.0, low=55, high=62, size=1.2, rasp=0.26, pattern='call'):
    """Call and response: the crew answers the machine, not the beat. Two
    syllables low on the first half of the bar, two higher on the second - the
    oldest structure there is, and the reason a work song is a work song."""
    if pattern in ('call', 'both'):
        for st in (0, 3):
            s.place(s.pos(b, st), chant(low, 2.2, size=size, rasp=rasp, seed=st),
                    gain * (1.0 if st == 0 else 0.72), 'choir')
    if pattern in ('answer', 'both'):
        for st in (8, 11):
            s.place(s.pos(b, st), chant(high, 2.2, size=size, rasp=rasp, seed=st + 7),
                    gain * (0.9 if st == 8 else 0.65), 'choir')

# ================= DESCENT: 0-15 =================
s.place(s.pos(0), bellow(128, gain=1.5, rate=0.5), 1.0, 'air')
s.place(s.pos(0), tunnel(96, note=43, gain=1.4, motor=0.18), 1.0, 'air')
for b in range(0, 16, 4):
    s.place(s.pos(b), grind(64, note=43, gain=1.6, res=0.7, seed=b), 1.0, 'air')
for b in (1, 5, 9, 13):
    s.place(s.pos(b, 6), chains(6, seed=b), 0.5, 'fx')
s.place(s.pos(3), reverb(groan(48, 14, fall=2.8, seed=1), decay=5.5, wet=0.8, tone=2200),
        0.55, 'fx')
s.place(s.pos(9), reverb(groan(51, 12, fall=2.2, seed=2), decay=5.0, wet=0.75, tone=2000),
        0.45, 'fx')
s.place(s.pos(6), press(16, gain=0.7, seed=1), 1.0, 'fx')
for b in range(10, 16):                                   # the floor arrives from far off
    u = (b - 10) / 5
    floor(b, gain=0.0, rum=0.3 + 0.3 * u, lpf=150 + 200 * (b - 10), rdecay=1.6)
s.place(s.pos(14), press(16, gain=0.85, seed=2), 1.0, 'fx')
s.place(s.pos(15), steam(8, gain=0.6), 1.0, 'fx')

# ================= SHIFT: 16-31 =================
for b in range(16, 32):
    ph = b - 16
    u = min(ph / 8, 1.0)
    floor(b, gain=0.55 + 0.4 * u, rum=0.7 + 0.3 * u,
          lpf=900 + 500 * ph if ph < 8 else None, grit=0.12 + 0.18 * u)
    tops(b, gain=0.3 + 0.3 * u, sixteenths=ph >= 4, claps=() if ph < 8 else (12,),
         opens=(14,))
    if ph >= 8:
        metal(b, idx=0, gain=0.45)
for b in range(16, 32, 8):
    s.place(s.pos(b), press(16, gain=0.85, seed=b), 1.0, 'fx')
for b in range(16, 32, 4):
    s.place(s.pos(b), grind(64, note=43, gain=1.3, res=0.9, seed=b + 3), 1.0, 'air')
s.place(s.pos(22, 8), chains(6, seed=22), 0.45, 'fx')
s.place(s.pos(28), reverb(groan(46, 14, fall=3.0, seed=3), decay=4.5, wet=0.6), 0.4, 'fx')

# ================= MACHINE: 32-47 =================
for b in range(32, 48):
    ph = b - 32
    floor(b, gain=1.0, rum=1.0, drive=6.5, grit=0.35)
    tops(b, gain=0.75, opens=(14,), claps=(4, 12))
    metal(b, idx=ph // 8, gain=0.7)
    offbeat = distbass(31, 2.0, cutoff=420)
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), offbeat, 0.55, 'bass')
for b in range(32, 48, 8):
    s.place(s.pos(b), press(16, gain=0.9, seed=b), 1.0, 'fx')
for b in range(32, 48, 4):
    s.place(s.pos(b), grind(64, note=43, gain=1.2, res=1.0, seed=b + 7), 1.0, 'air')
s.place(s.pos(40, 8), servo(8, rate=18, accel=2.0, seed=40), 0.5, 'music')
s.place(s.pos(47, 8), steam(6, gain=0.55, seed=47), 1.0, 'fx')

# ================= CHANT: 48-63 =================
# The crew comes in on the machine's beat. Nothing else changes - the arrival
# of a human sound is the event.
for b in range(48, 64):
    ph = b - 48
    floor(b, gain=1.0, rum=1.0, drive=7.0, grit=0.4)
    tops(b, gain=0.85, opens=(14,))
    metal(b, idx=ph // 8, gain=0.72)
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), distbass(43, 2.0, cutoff=720), 0.55, 'bass')
    workcall(b, gain=1.75 + 0.35 * (ph / 15), pattern='call' if ph % 2 == 0 else 'answer')
    if ph >= 8 and ph % 2 == 0:                           # the held voices start gathering
        choir(b, 2, gain=0.24 + 0.05 * (ph - 8), attack=0.8, seed=b)
for b in range(48, 64, 8):
    s.place(s.pos(b), press(16, gain=0.9, seed=b), 1.0, 'fx')
for b in range(48, 64, 4):
    s.place(s.pos(b), grind(64, note=43, gain=1.1, res=1.0, seed=b), 1.0, 'air')
s.place(s.pos(56, 4), chains(8, seed=56), 0.4, 'fx')

# ================= DEEPER: 64-79 =================
for b in range(64, 80):
    ph = b - 64
    floor(b, gain=1.0, rum=1.0, drive=7.5, grit=0.45)
    tops(b, gain=0.9, opens=(6, 14) if ph % 2 else (14,))
    metal(b, idx=(ph // 8) + 1, gain=0.78)
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), distbass(43, 2.0, cutoff=760), 0.58, 'bass')
    workcall(b, gain=1.5, pattern='both' if ph % 4 == 3 else
             ('call' if ph % 2 == 0 else 'answer'))
for b in range(64, 80, 2):                                # the choir starts holding notes
    choir(b, 2, gain=0.5 + 0.12 * ((b - 64) // 4), seed=b)
for b in range(64, 80, 8):
    s.place(s.pos(b), press(16, gain=0.95, seed=b), 1.0, 'fx')
s.place(s.pos(79, 8), whoosh(8, gain=0.8), 1.0, 'fx')

# ================= THE HOLLOW: 80-95 =================
# The machine stops. The room it was in does not, and neither do they.
s.place(s.pos(80), downlifter(16, gain=0.85), 1.0, 'fx')
s.place(s.pos(80), bellow(128, gain=2.0, rate=0.4, seed=80), 1.0, 'air')
s.place(s.pos(80), tunnel(160, note=43, gain=1.7, motor=0.1, seed=80), 1.0, 'air')
for b in range(80, 96, 4):
    s.place(s.pos(b), grind(64, note=43, gain=2.4, res=1.2, crush=8, seed=b), 1.0, 'air')
for b in range(80, 94, 2):
    ch = CHOIR[(b // 2) % len(CHOIR)]
    s.place(s.pos(b), reverb(labourchoir(tuple(ch), 32, vowel='oh', size=1.35,
                                         spread=30.0, rasp=0.25, attack=0.9, seed=b),
                             decay=5.0, wet=0.55, tone=2600), 0.58, 'choir')
for b, note, fall in ((82, 46, 3.2), (86, 43, 2.6), (90, 48, 3.6), (92, 41, 2.2)):
    s.place(s.pos(b, 4), reverb(groan(note, 16, fall=fall, size=1.4, seed=b),
                                decay=6.0, wet=0.7, tone=2000), 0.45, 'fx')
for b in (84, 90):
    s.place(s.pos(b), press(16, gain=0.5, seed=b), 1.0, 'fx')
s.place(s.pos(88, 8), chains(8, seed=88), 0.4, 'fx')
for b in (92, 94):                                        # two hits: the machine testing
    floor(b, gain=0.7, steps_=(0,), rum=0.75, lpf=1500)

# ================= PRESSURE: 96-111 =================
for b in range(96, 112):
    ph = b - 96
    u = ph / 15
    floor(b, gain=0.7 + 0.3 * u, rum=0.8 + 0.2 * u,
          lpf=1100 + 700 * ph if ph < 8 else None, drive=6.5 + 1.5 * u, grit=0.2 + 0.3 * u)
    tops(b, gain=0.5 + 0.4 * u, sixteenths=ph >= 3, claps=(4, 12) if ph >= 4 else ())
    if ph >= 4:
        metal(b, idx=ph // 4, gain=0.6 + 0.02 * ph)
    if ph >= 6:
        s.place(s.pos(b), acid(ACID_G, f_lo=330, f_hi=1400 + 3000 * u, res=4.0,
                               drive=3.6, low=340), 0.5 + 0.4 * u, 'acid')
    if ph >= 8:
        workcall(b, gain=1.35, pattern='both' if ph % 2 else 'call')
    if ph >= 12:
        s.place(s.pos(b), servo(16, rate=14 + 9 * (ph - 12), accel=2.3, seed=b), 0.55, 'music')
for b in range(96, 112, 2):
    choir(b, 2, gain=0.45, seed=b)
s.place(s.pos(104), press(16, gain=0.95, seed=104), 1.0, 'fx')
s.place(s.pos(108), riser(64, gain=0.95, f0=140, f1=1900), 1.0, 'fx')
s.place(s.pos(111, 8), reverse_crash(8, gain=0.9), 1.0, 'fx')
s.place(s.pos(111, 12), chant(67, 4, size=1.1, rasp=0.36, seed=111), 1.1, 'choir')

# ================= THE GREAT WORK: 112-135 =================
for b in range(112, 136):
    ph = b - 112
    roll = [0, 4, 8, 10, 12, 14] if ph % 8 == 7 else None
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=1.0, drive=8.0,
          decay=0.23, grit=0.5, rdrive=2.9)
    tops(b, gain=0.95, opens=(6, 14) if ph % 2 else (14,))
    metal(b, idx=ph // 6, gain=0.85)
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), distbass(43, 2.0, cutoff=800), 0.6, 'bass')
    s.place(s.pos(b), acid(ACID_G, f_lo=420, f_hi=5200, res=4.2, drive=4.0, low=340),
            0.72, 'acid')
    workcall(b, gain=1.55, pattern='both' if ph % 4 == 3 else
             ('call' if ph % 2 == 0 else 'answer'))
for b in range(112, 136, 2):
    choir(b, 2, gain=0.62, rasp=0.2, seed=b)
for b in range(112, 136, 8):
    s.place(s.pos(b), press(16, gain=1.0, seed=b), 1.0, 'fx')
    s.place(s.pos(b), crash808(20, gain=0.45), 1.0, 'drums')
for b in (118, 128):
    s.place(s.pos(b, 8), chains(8, seed=b), 0.42, 'fx')
s.place(s.pos(124), alarm(48, f0=150, f1=430, cycles=1.5, gain=0.5), 1.0, 'fx')

# ================= THE GROAN: 136-143 =================
# The machine is switched off mid-bar and takes four seconds to stop. The
# crew keeps going, because the shift has not ended.
s.place(s.pos(136), tape_stop(s.bus['drums'][s.pos(135):s.pos(136)].copy(), stop_s=1.1),
        0.9, 'fx')
s.place(s.pos(136), downlifter(20, gain=0.9, f0=1400, f1=45), 1.0, 'fx')
s.place(s.pos(136), bellow(128, gain=1.5, rate=0.35, seed=136), 1.0, 'air')
for b in range(136, 144, 2):
    ch = CHOIR[(b // 2) % len(CHOIR)]
    s.place(s.pos(b), reverb(labourchoir(tuple(ch), 32, vowel='uh', size=1.45,
                                         spread=38.0, rasp=0.3, sag=70.0, attack=0.7,
                                         seed=b), decay=5.5, wet=0.6, tone=2400),
            0.95, 'choir')
for b, note, fall in ((137, 43, 4.0), (139, 46, 3.4), (141, 40, 4.5), (142, 48, 3.0)):
    s.place(s.pos(b, 6), reverb(groan(note, 18, fall=fall, size=1.5, rasp=0.6, seed=b),
                                decay=6.5, wet=0.75, tone=1900), 0.33, 'fx')
s.place(s.pos(140), press(16, gain=0.42, seed=140), 1.0, 'fx')
s.place(s.pos(142), riser(32, gain=0.85, f0=120, f1=2100), 1.0, 'fx')
s.place(s.pos(143, 8), reverse_crash(8, gain=1.0), 1.0, 'fx')
s.place(s.pos(143, 12), chant(67, 4, size=1.05, rasp=0.38, seed=143), 1.2, 'choir')

# ================= COLLAPSE: 144-183 =================
for b in range(144, 184):
    ph = b - 144
    roll = None
    if ph % 16 == 15:
        roll = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15]
    elif ph % 8 == 7:
        roll = [0, 4, 8, 10, 12, 14]
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=1.0, drive=9.0,
          decay=0.22, grit=0.6, rdrive=3.1)
    tops(b, gain=1.0, opens=(6, 14))
    metal(b, idx=ph // 4, gain=0.9)
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), distbass(43, 2.0, cutoff=850), 0.65, 'bass')
    s.place(s.pos(b), acid(ACID_G, f_lo=420, f_hi=6000, res=4.5, drive=4.5, low=340),
            0.8, 'acid')
    workcall(b, gain=1.65, rasp=0.34, pattern='both')
    if ph >= 16:                                          # the crew doubles its own call
        s.place(s.pos(b, 5), chant(62, 2.0, size=1.15, rasp=0.32, seed=b), 0.7, 'choir')
        s.place(s.pos(b, 13), chant(67, 2.0, size=1.15, rasp=0.32, seed=b + 1), 0.62, 'choir')
for b in range(144, 184, 2):                              # the choir, now through the machine
    ch = CHOIR[(b // 2) % len(CHOIR)]
    seg = labourchoir(tuple(ch), 32, vowel='oh', size=1.2, spread=24.0, rasp=0.3,
                      attack=0.25, seed=b)
    s.place(s.pos(b), seg, 0.72, 'choir')
for b in range(144, 184, 8):
    s.place(s.pos(b), press(16, gain=1.0, seed=b), 1.0, 'fx')
    s.place(s.pos(b), crash808(20, gain=0.5), 1.0, 'drums')
for b in (152, 168, 180):
    s.place(s.pos(b, 8), chains(8, seed=b), 0.45, 'fx')
for b in (160, 176):
    s.place(s.pos(b), alarm(64, f0=160, f1=520, cycles=2.0, gain=0.55), 1.0, 'fx')
s.place(s.pos(183, 8), whoosh(8, gain=0.9), 1.0, 'fx')

# ================= SILT: 184-191 =================
s.place(s.pos(184), bellow(96, gain=1.8, rate=0.3, seed=184), 1.0, 'air')
s.place(s.pos(184), tunnel(96, note=43, gain=1.5, motor=0.12, seed=184), 1.0, 'air')
for b in range(184, 192):
    ph = b - 184
    u = ph / 7
    floor(b, gain=0.9 - 0.7 * u, lpf=5000 - 560 * ph, rum=0.9 - 0.5 * u,
          drive=6.0, rdecay=1.5)
    tops(b, gain=0.6 - 0.5 * u, sixteenths=ph < 4, claps=() , opens=(14,) if ph < 5 else ())
    if ph < 4:
        metal(b, idx=ph, gain=0.5 - 0.1 * ph)
for b in (184, 188):
    ch = CHOIR[(b // 2) % len(CHOIR)]
    s.place(s.pos(b), reverb(labourchoir(tuple(ch), 32, vowel='oh', size=1.35,
                                         spread=32.0, rasp=0.2, attack=1.0, seed=b),
                             decay=6.0, wet=0.6, tone=2200), 0.6, 'choir')
s.place(s.pos(186), reverb(groan(43, 18, fall=3.5, size=1.45, seed=186),
                           decay=7.0, wet=0.8, tone=1800), 0.5, 'fx')
s.place(s.pos(190), press(16, gain=0.55, seed=190), 1.0, 'fx')
s.place(s.pos(191), downlifter(16, gain=0.6), 1.0, 'fx')

# ---- bus space, then the master ----
Session.DUCKED = dict(Session.DUCKED, choir=0.5)
s.bus['choir'] = bus_reverb(s.bus['choir'], decay=3.4, wet=0.34, tone=3000)
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.8, wet=0.22, tone=5000)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.6, wet=0.34, tone=3800)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=3.0, wet=0.24, tone=3000)
s.bus['acid']  = bus_reverb(s.bus['acid'],  decay=1.0, wet=0.12, tone=4400)
s.bus['air'] = hp(s.bus['air'], 55)
s.bus['choir'] = hp(s.bus['choir'], 150)                  # the kick owns the bottom
s.bus['choir'] = shelf(s.bus['choir'], 1900, 4.0)         # presence: a voice needs 1-4 kHz
s.bus['choir'] = softclip(s.bus['choir'], 0.85, knee=0.7) # even out the shouts
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.85)
s.bus['rumble'] = softclip(s.bus['rumble'], 1.05, knee=0.85)
for b in ('drums', 'music', 'fx', 'air'):
    s.bus[b] = shelf(s.bus[b], 9500, -1.5)
s.bus['acid'] = shelf(s.bus['acid'], 340, -3.5, kind='low')   # the choir owns 200-800
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)

GAINS = {'drums': 0.86, 'rumble': 0.50, 'bass': 0.30, 'acid': 0.40,
         'choir': 0.76, 'music': 0.86, 'air': 0.32, 'fx': 0.40}
s.report(GAINS)
s.render('industrial_untertage_136.wav', drive=1.0, duck=0.16, clip=1.10,
         limit=0.94, peak=0.95, fade=2.5, gains=GAINS)
