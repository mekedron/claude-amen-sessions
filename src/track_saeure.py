"""SAEURE - hard acid at 146 BPM, E minor with a Phrygian second.

Saeure is German for acid, and this is the version of it that lives at the
bottom. The kick is tuned to E1 - 41.2 Hz, a third under Spirale and at the
lower edge of what a club system will actually move air with - and the 303
starts an octave above where it ends up.

The shape of the record is a descent. The line begins at E3, drops to E2
halfway, and by the last forty bars a saturated copy of it is running an
octave below that while the original is being folded. Nothing is transposed
for variety: every drop in register comes with more distortion, so the track
gets lower and harder at the same time, which is the only way "deep" and
"hard" are the same direction.

    ANSATZ | ERSTE SAEURE | TIEFER I | LEERE | TIEFER II | DRUCK
           | HAMMERWERK | BODEN | AUSKLANG

240 bars, 6:34. HAMMERWERK is sixteen bars of nothing but industrial kicks -
hard-clipped, half of each one made of air.
"""
import numpy as np
from industriallib import *

BAR, STEP = set_tempo(146)
BPM = 146.0
np.random.seed(146)

ROOT = 41.20                                   # E1 - deep, and still reproducible

# E minor leaning Phrygian: the F is the b2 and it is the whole flavour
HIGH = [(0, 52, 2, 1, 0), (2, 52, 1, 0, 0), (3, 64, 1.5, 0, 1), (5, 52, 1, 0, 0),
        (6, 55, 2, 0, 0), (8, 52, 2, 1, 0), (10, 59, 1, 0, 0), (11, 52, 1, 0, 0),
        (13, 62, 1.5, 0, 1), (15, 53, 1, 0, 0)]
HIGH2 = [(0, 52, 2, 1, 0), (2, 55, 1, 0, 0), (3, 52, 1, 0, 0), (5, 64, 1.5, 1, 1),
         (7, 52, 1, 0, 0), (8, 53, 1.5, 0, 0), (10, 52, 1, 0, 0), (11, 59, 1, 0, 1),
         (13, 52, 1, 0, 0), (14, 62, 2, 1, 0)]
DENSE = [(0, 52, 1, 1, 0), (1, 52, 1, 0, 0), (2, 59, 1, 0, 1), (3, 52, 1, 0, 0),
         (4, 64, 1.5, 1, 0), (6, 55, 1, 0, 0), (7, 52, 1, 0, 0), (8, 52, 1, 1, 0),
         (9, 62, 1, 0, 1), (10, 52, 1, 0, 0), (12, 53, 1.5, 0, 0), (14, 59, 2, 1, 1)]

def down(pat, semis=-12):
    return [(st, n + semis, d, a, sl) for st, n, d, a, sl in pat]

s = Session(240, tail=4.0)

def floor(b, gain=1.0, steps_=(0, 4, 8, 12), lpf=None, rum=0.0, drive=6.0,
          decay=0.17, grit=0.25):
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = techkick(dur_steps=2.4, tune=ROOT, drive=drive, decay=decay, grit=grit)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if rum:
            s.place(t, rumble(dur_steps=6, tune=ROOT, decay=0.8, drive=2.4), rum, 'rumble')

def tops(b, gain=1.0, closed=True, opens=(2, 6, 10, 14), claps=(4, 12), clapg=0.66,
         ride=False):
    for st in claps:
        s.place(s.pos(b, st), distclap(2.6), gain * clapg, 'drums')
    if closed:
        for i in range(16):
            if i % 4 == 0:
                continue
            p = 0.4 if (i // 2) % 2 else -0.4
            s.place(s.pos(b, i), panned(hat909(0.6), p), gain * (0.52 if i % 2 else 0.28), 'drums')
    for st in opens:
        s.place(s.pos(b, st), panned(hat909(2.4, open_=True), 0.2 if st % 8 else -0.2),
                gain * 0.34, 'drums')
    if ride:
        for i in range(0, 16, 2):
            s.place(s.pos(b, i), panned(metalhat(0.8, tone=1.25), -0.5 if i % 4 else 0.5),
                    gain * 0.2, 'drums')

def line(b0, bars, pat=None, knob=(0.5, 1.0), res=4.4, dec=0.16, drive=4.2,
         wave='saw', gain=1.0, f_hi=5000, f_lo=200, low=72, hard=0.0, bite=0.8,
         stage2=2.4, bus='acid'):
    """One pass of the 303. hard>0 sends it through the full distortion chain
    instead of a single waveshaper."""
    p = poly_pattern(pat or HIGH, 16, bars)
    kw = dict(f_lo=f_lo, f_hi=f_hi, res=res, drive=drive, low=low, decay=dec,
              wave=wave, knob=knob)
    seg = (acid_hard(p, bars, fold_amt=hard, bite=bite, stage2=stage2, **kw)
           if hard else acid(p, dur_bars=bars, **kw))
    s.place(s.pos(b0), seg, gain, bus)

def top_line(b0, bars, pat=None, knob=(0.6, 1.0), res=5.0, dec=0.12, drive=4.6,
             gain=1.0, f_hi=7000, hard=0.7, wave='saw'):
    """The line an octave above the bassline, and this is where the dirt goes.

    Two distorted voices in the same octave is mud; split them by register and
    the low one keeps its definition while the high one does the screaming.
    High-passed at 300 Hz so it cannot argue with the bass at all."""
    p = poly_pattern(pat or HIGH, 16, bars)
    seg = acid_hard(p, bars, fold_amt=hard, bite=1.1, stage2=2.8, f_lo=420,
                    f_hi=f_hi, res=res, drive=drive, low=300, decay=dec,
                    wave=wave, knob=knob)
    s.place(s.pos(b0), seg, gain, 'top')

def sub_line(b0, bars, pat=None, gain=1.0, sat=2.6, top=170):
    s.place(s.pos(b0), subacid(poly_pattern(pat or HIGH, 16, bars), bars, sat=sat,
                               top=top, knob=(1.0,)), gain, 'sub')

# ================= ANSATZ: 0-23 =================
s.place(s.pos(0), tunnel(96, note=40, gain=1.2, motor=0.22), 1.0, 'air')
for b in range(0, 24, 4):
    s.place(s.pos(b), grind(64, note=40, gain=1.0, res=0.7, seed=b), 1.0, 'air')
line(0,  8, knob=(0.08, 0.26), res=3.0, dec=0.22, drive=3.4, f_hi=3000, gain=0.60)
line(8,  8, knob=(0.24, 0.44), res=3.4, dec=0.20, drive=3.6, f_hi=3600, gain=0.78)
line(16, 8, pat=HIGH2, knob=(0.40, 0.68, 0.56), res=3.8, dec=0.18, drive=3.8,
     f_hi=4200, gain=0.92)
for b in range(6, 24):
    u = (b - 6) / 17
    floor(b, gain=0.5 + 0.45 * u, lpf=240 + 200 * (b - 6) if b < 16 else None,
          grit=0.05 + 0.2 * u)
for b in range(12, 24):
    tops(b, gain=0.3 + 0.45 * ((b - 12) / 11), closed=b >= 16,
         claps=() if b < 18 else (4, 12), opens=(6, 14) if b < 18 else (2, 6, 10, 14))
s.place(s.pos(23, 8), steam(6, gain=0.45), 1.0, 'fx')

# ================= ERSTE SAEURE: 24-55 =================
for b in range(24, 56):
    ph = b - 24
    floor(b, gain=1.0, drive=6.5, grit=0.3)
    tops(b, gain=0.85, ride=ph >= 16)
line(24, 8, knob=(0.70, 1.0, 0.82), res=4.2, dec=0.16, drive=4.2, f_hi=4800)
line(32, 8, wave='square', knob=(0.78, 0.56, 0.94), res=4.4, dec=0.15, drive=4.0,
     f_hi=4400)
line(40, 8, pat=DENSE, knob=(0.68, 1.0), res=4.6, dec=0.13, drive=4.4, f_hi=5200)
line(48, 8, pat=HIGH2, knob=(0.90, 0.64, 1.0), res=4.4, dec=0.17, drive=4.2, f_hi=5000)
for b in range(24, 56, 8):
    s.place(s.pos(b), grind(128, note=40, gain=0.8, res=0.8, seed=b), 1.0, 'air')
s.place(s.pos(40), resoscream(76, 6, gain=1.5, seed=40), 1.0, 'lead')
s.place(s.pos(55, 8), reverse_crash(8, gain=0.5), 1.0, 'fx')

# ================= TIEFER I: 56-87 =================
# The line drops an octave and the chain starts working on it.
for b in range(56, 88):
    ph = b - 56
    floor(b, gain=1.0, rum=0.14, drive=7.0, grit=0.35)
    tops(b, gain=0.9, ride=True)
line(56, 8, pat=down(HIGH), knob=(0.62, 0.92), res=4.4, dec=0.18, drive=4.4,
     f_hi=4200, low=64, hard=0.22)
line(64, 8, pat=down(HIGH2), knob=(0.84, 0.58, 1.0), res=4.6, dec=0.16, drive=4.6,
     f_hi=4600, low=64, hard=0.30)
line(72, 8, pat=down(DENSE), wave='square', knob=(0.70, 1.0), res=4.8, dec=0.14,
     drive=4.4, f_hi=4400, low=64, hard=0.34)
line(80, 8, pat=down(HIGH), knob=(0.92, 0.66, 1.0), res=4.6, dec=0.17, drive=4.8,
     f_hi=5000, low=64, hard=0.38)
for b in range(56, 88, 8):
    s.place(s.pos(b), grind(128, note=40, gain=0.8, res=0.9, seed=b + 5), 1.0, 'air')
s.place(s.pos(72), resoscream(71, 6, gain=1.5, seed=72), 1.0, 'lead')
s.place(s.pos(87, 8), whoosh(8, gain=0.7), 1.0, 'fx')

# ================= LEERE: 88-111 =================
s.place(s.pos(88), downlifter(16, gain=0.8), 1.0, 'fx')
s.place(s.pos(88), tunnel(160, note=40, gain=1.6, motor=0.1, seed=88), 1.0, 'air')
for b in range(88, 112, 4):
    s.place(s.pos(b), grind(64, note=40, gain=1.9, res=1.1, crush=9, seed=b), 1.0, 'air')
line(88,  12, pat=down(HIGH), knob=(0.16, 0.52, 1.0), res=4.8, dec=0.21, drive=3.8,
     f_hi=5600, low=64, gain=0.9, hard=0.25)
line(100, 8, pat=down(HIGH2), knob=(0.96, 0.38, 1.0), res=5.0, dec=0.17, drive=4.0,
     f_hi=6000, low=64, gain=0.9, hard=0.3)
for b, note in ((92, 76), (98, 71), (104, 79)):
    s.place(s.pos(b, 8), resoscream(note, 8, gain=0.4, res=8.0, seed=b), 1.0, 'lead')
s.place(s.pos(96), alarm(48, f0=170, f1=500, cycles=1.5, gain=0.38), 1.0, 'fx')
for b in range(108, 112):
    floor(b, gain=0.55 + 0.15 * (b - 108), steps_=(0, 8) if b < 110 else (0, 4, 8, 12),
          lpf=900 + 700 * (b - 108))
    tops(b, gain=0.4 + 0.15 * (b - 108), closed=b >= 110, claps=(), opens=(6, 14))
s.place(s.pos(108), riser(64, gain=0.85, f0=140, f1=1700), 1.0, 'fx')
s.place(s.pos(111, 12), reverse_crash(4, gain=0.85), 1.0, 'fx')

# ================= TIEFER II: 112-143 =================
for b in range(112, 144):
    ph = b - 112
    floor(b, gain=1.0, rum=0.2, drive=7.5, grit=0.4)
    tops(b, gain=0.95, ride=True)
# sixteen bars in one call, the knob walking through five positions: the line
# flows through its own variations instead of being restarted every eight bars
line(112, 16, pat=down(HIGH), knob=(0.54, 0.86, 0.66, 1.0, 0.78), res=4.6, dec=0.17,
     drive=4.6, f_hi=5000, low=64, hard=0.26, bite=1.1)
line(128, 16, pat=down(HIGH2), knob=(0.72, 1.0, 0.58, 0.94, 1.0), res=5.0, dec=0.15,
     drive=4.8, f_hi=5400, low=64, hard=0.32, bite=1.2)
# and the second voice arrives on top, one octave up, fading in over eight bars
for _b in range(112, 144, 8):
    top_line(_b, 8, pat=(HIGH2 if (_b // 8) % 2 else HIGH),
             knob=(0.5 + 0.1 * ((_b - 112) / 24), 0.9),
             gain=0.30 + 0.30 * ((_b - 112) / 24), hard=0.62, f_hi=6600)
for b in range(120, 144, 8):
    sub_line(b, 8, pat=down(HIGH), gain=0.34 + 0.06 * ((b - 120) / 16))
for b in range(112, 144, 8):
    s.place(s.pos(b), grind(128, note=40, gain=0.8, res=1.0, seed=b), 1.0, 'air')
    s.place(s.pos(b), crash808(18, gain=0.32), 1.0, 'drums')
s.place(s.pos(132), resoscream(83, 6, gain=1.5, res=8.0, seed=132), 1.0, 'lead')

# ================= DRUCK: 144-175 =================
for b in range(144, 176):
    ph = b - 144
    roll = [0, 4, 8, 10, 12, 14] if ph % 16 == 15 else None
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=0.26, drive=8.0, grit=0.45)
    tops(b, gain=1.0, ride=True)
line(144, 16, pat=down(HIGH), knob=(0.86, 1.0, 0.68, 0.96, 1.0), res=4.8, dec=0.16,
     drive=4.8, f_hi=5800, low=64, hard=0.30, bite=1.2)
line(160, 16, pat=down(DENSE), knob=(0.74, 1.0, 0.60, 1.0), res=5.2, dec=0.13,
     drive=5.2, f_hi=6200, low=64, hard=0.36, bite=1.25)
for _b in range(144, 176, 8):
    top_line(_b, 8, pat=(DENSE if (_b // 8) % 2 else HIGH2),
             knob=(0.66, 1.0, 0.74), gain=0.58, hard=0.70, res=5.2, f_hi=7000,
             wave='square' if (_b // 8) % 2 else 'saw')
for b in range(144, 176, 8):
    sub_line(b, 8, pat=down(HIGH), gain=0.48 + 0.08 * ((b - 144) / 24))
    s.place(s.pos(b), grind(128, note=40, gain=0.8, res=1.0, seed=b + 9), 1.0, 'air')
    s.place(s.pos(b), crash808(18, gain=0.38), 1.0, 'drums')
for b in (150, 164):
    s.place(s.pos(b, 8), resoscream(79, 8, gain=1.5, res=8.5, seed=b), 1.0, 'lead')
s.place(s.pos(158), alarm(48, f0=190, f1=560, cycles=1.5, gain=0.4), 1.0, 'fx')

# ================= HAMMERWERK: 176-191 =================
# Sixteen bars of nothing but kicks. Hard-clipped, half air, and fired in
# rows that get tighter - the acid drops out entirely so there is nothing to
# hear but the hammering, which is what makes the last section land.
s.place(s.pos(176), downlifter(12, gain=0.7), 1.0, 'fx')
s.place(s.pos(176), tunnel(128, note=40, gain=1.3, motor=0.3, seed=176), 1.0, 'air')
for b in range(176, 192):
    ph = b - 176
    rows = ([0, 4, 8, 12] if ph < 4 else
            [0, 2, 4, 6, 8, 10, 12, 14] if ph < 10 else
            [0, 2, 4, 6, 8, 10, 12, 13, 14, 15] if ph < 14 else
            list(np.arange(0, 16, 1)))
    kickbarrage(s, b, rows, gain=0.78 + 0.16 * (ph / 15), tune=ROOT,
                climb=0.0 if ph < 12 else 0.03,
                hiss=0.7 + 0.4 * (ph / 15), air=0.5 + 0.3 * (ph / 15),
                decay=0.13 - 0.03 * (ph / 15), drive=12.0 + 3.0 * (ph / 15))
    tops(b, gain=0.3 + 0.3 * (ph / 15), closed=False, claps=(4, 12) if ph >= 8 else (),
         opens=(6, 14), clapg=0.5)
    if ph >= 10:
        s.place(s.pos(b, 8), servo(8, rate=20 + 10 * (ph - 10), accel=2.2, seed=b),
                0.4, 'music')
for b in range(176, 192, 4):
    s.place(s.pos(b), grind(64, note=40, gain=1.4, res=1.0, seed=b + 2), 1.0, 'air')
s.place(s.pos(184), alarm(48, f0=200, f1=620, cycles=1.5, gain=0.5), 1.0, 'fx')
s.place(s.pos(188), riser(48, gain=1.0, f0=130, f1=2100), 1.0, 'fx')
s.place(s.pos(191, 12), reverse_crash(4, gain=1.0), 1.0, 'fx')

# ================= BODEN: 192-231 =================
for b in range(192, 232):
    ph = b - 192
    roll = None
    if ph % 16 == 15:
        roll = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15]
    elif ph % 8 == 7:
        roll = [0, 4, 8, 10, 12, 14]
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=0.4, drive=8.5, grit=0.5)
    tops(b, gain=1.0, ride=True)
    if ph % 8 == 7:                                   # the hammer answers every phrase
        kickbarrage(s, b, [8, 10, 12, 14], gain=0.7, hiss=1.0, air=0.7, drive=14.0)
line(192, 16, pat=down(HIGH), knob=(0.90, 1.0, 0.72, 1.0, 0.88), res=5.0, dec=0.15,
     drive=5.0, f_hi=6000, low=64, hard=0.34, bite=1.3)
line(208, 16, pat=down(DENSE), knob=(0.80, 1.0, 0.64, 1.0, 1.0), res=5.4, dec=0.13,
     drive=5.4, f_hi=6600, low=64, hard=0.40, bite=1.3)
line(224, 8,  pat=down(HIGH), knob=(0.94, 1.0), res=5.2, dec=0.15, drive=5.2,
     f_hi=6400, low=64, hard=0.36, bite=1.25)
for _b in range(192, 232, 8):                        # three octaves at once
    top_line(_b, 8, pat=(DENSE if (_b // 8) % 2 else HIGH),
             knob=(0.72, 1.0, 0.80), gain=0.66 + 0.10 * ((_b - 192) / 32),
             hard=0.78, res=5.4, f_hi=7400,
             wave='square' if (_b // 8) % 2 else 'saw')
for b in range(192, 232, 8):
    sub_line(b, 8, pat=down(HIGH), gain=0.68 + 0.16 * ((b - 192) / 32), sat=3.0)
    s.place(s.pos(b), grind(128, note=40, gain=0.8, res=1.0, seed=b + 3), 1.0, 'air')
    s.place(s.pos(b), crash808(18, gain=0.4), 1.0, 'drums')
for b in (198, 212, 226):
    s.place(s.pos(b, 8), resoscream(83, 8, gain=1.5, res=9.0, seed=b), 1.0, 'lead')
for b in (204, 220):
    s.place(s.pos(b), alarm(64, f0=210, f1=660, cycles=2.0, gain=0.42), 1.0, 'fx')
s.place(s.pos(231, 8), whoosh(8, gain=0.8), 1.0, 'fx')

# ================= AUSKLANG: 232-239 =================
s.place(s.pos(232), tunnel(96, note=40, gain=1.3, motor=0.15, seed=232), 1.0, 'air')
s.place(s.pos(232), grind(128, note=40, gain=1.1, res=0.8, seed=232), 1.0, 'air')
line(232, 8, pat=down(HIGH), knob=(0.84, 0.10), res=4.6, dec=0.18, drive=4.4,
     f_hi=5200, low=64, gain=0.85, hard=0.4)
for b in range(232, 240):
    ph = b - 232
    u = ph / 7
    floor(b, gain=0.9 - 0.7 * u, lpf=5000 - 560 * ph, rum=0.35 - 0.3 * u, grit=0.15)
    tops(b, gain=0.7 - 0.6 * u, closed=ph < 4, claps=(4, 12) if ph < 3 else (),
         opens=(6, 14) if ph < 5 else ())
s.place(s.pos(239), downlifter(16, gain=0.6), 1.0, 'fx')

# ---- bus space, then the master ----
Session.DUCKED = dict(Session.DUCKED, acid=0.6, sub=0.95, top=0.35, lead=0.3)
s.bus['acid'] = autopan(s.bus['acid'], cycle_bars=13.0, depth=0.26, phase=1.1)
s.bus['lead'] = autopan(s.bus['lead'], cycle_bars=5.0, depth=0.72, phase=2.1)
s.bus['lead'] = bus_reverb(s.bus['lead'], decay=1.6, wet=0.26, tone=5000)
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.8, wet=0.24, tone=4800)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.0, wet=0.30, tone=3800)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.6, wet=0.22, tone=3000)
s.bus['air'] = hp(s.bus['air'], 95)
s.bus['lead'] = hp(s.bus['lead'], 400)
s.bus['top'] = hp(s.bus['top'], 300)                      # never argues with the bass
s.bus['top'] = autopan(s.bus['top'], cycle_bars=9.0, depth=0.5, phase=0.7)
s.bus['top'] = bus_reverb(s.bus['top'], decay=1.2, wet=0.16, tone=5400)
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.85)
s.bus['acid'] = lp(s.bus['acid'], 12000)
s.bus['drums'] = lp(s.bus['drums'], 15000)
for b in ('drums', 'music', 'fx', 'air'):
    s.bus[b] = shelf(s.bus[b], 9500, -2.5)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)

GAINS = {'drums': 1.00, 'rumble': 0.30, 'acid': 0.62, 'sub': 0.56, 'top': 0.44,
         'lead': 0.50, 'music': 0.50, 'air': 0.38, 'fx': 0.46}
s.report(GAINS)
s.render('acid_saeure_146.wav', drive=1.0, duck=0.17, clip=1.10, limit=0.94,
         peak=0.95, fade=2.5, gains=GAINS)
