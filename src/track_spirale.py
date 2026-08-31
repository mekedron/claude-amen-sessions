"""SPIRALE - acid techno at 140 BPM, A minor. The 303 is the whole record.

Two acid lines, one on a sixteen-step bar and one on a fifteen-step cycle.
They start together, drift a step apart every bar, and meet again fifteen bars
later - so the figure is always almost repeating and never quite does. That is
the spiral, and it is also why a loop can hold somebody for seven minutes
without a single new idea being introduced.

There is no rumble here. Modern hard techno puts a reverbed kick under
everything; acid techno is a 909 and a 303 and the space between them, and the
low end belongs to the bassline, not to a tail. Everything that happens is a
filter moving: cutoff, resonance and envelope amount are the arrangement, which
is what playing a 303 has always meant.

    EINTRITT | SPIRALE I | ZWEITE STIMME | AUFLÖSUNG | AUFSTIEG
             | TIEFE | VERZERRUNG | RÜCKKEHR | AUSTRITT

256 bars, 7:18.
"""
import numpy as np
from industriallib import *

BAR, STEP = set_tempo(140)
BPM = 140.0
np.random.seed(303)

ROOT = 55.0                                    # A1 - the kick

# A minor with a Bb leaning in: the b2 is where acid gets its bite
# (step, note, dur_steps, accent, slide)
LINE_A = [(0, 45, 2, 1, 0), (2, 45, 1, 0, 0), (3, 57, 1.5, 0, 1), (5, 45, 1, 0, 0),
          (6, 48, 2, 0, 0), (8, 45, 2, 1, 0), (10, 52, 1, 0, 0), (11, 45, 1, 0, 0),
          (13, 55, 1.5, 0, 1), (15, 46, 1, 0, 0)]
LINE_B = [(0, 45, 1.5, 1, 0), (2, 52, 1, 0, 0), (3, 45, 1, 0, 0), (5, 48, 1.5, 0, 1),
          (7, 45, 1, 0, 0), (8, 57, 1.5, 1, 0), (10, 50, 1, 0, 0), (12, 45, 1, 0, 0),
          (13, 55, 2, 0, 1)]                   # 15 steps long - the drift
LINE_C = [(0, 57, 1, 1, 0), (1, 57, 1, 0, 0), (2, 60, 1, 0, 1), (4, 64, 1.5, 1, 0),
          (6, 57, 1, 0, 0), (7, 62, 1, 0, 0), (8, 57, 1, 1, 0), (10, 69, 1.5, 0, 1),
          (12, 60, 1, 0, 0), (14, 57, 2, 1, 0)]

POLY = poly_pattern(LINE_B, 15, 15)            # one 15-bar block of the drifting line

s = Session(256, tail=4.0)

def q(v, step=50):
    """quantise a swept parameter so the cache still works"""
    return round(v / step) * step

def sweep(b, b0, b1, lo, hi, curve=1.0):
    u = np.clip((b - b0) / max(b1 - b0, 1), 0, 1) ** curve
    return lo + (hi - lo) * u

def floor(b, gain=1.0, steps_=(0, 4, 8, 12), lpf=None, rum=0.0, drive=5.5,
          decay=0.15, grit=0.2):
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = techkick(dur_steps=2.2, tune=ROOT, drive=drive, decay=decay, grit=grit)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if rum:
            s.place(t, rumble(dur_steps=6, tune=ROOT, decay=0.7, drive=2.2), rum, 'rumble')

def tops(b, gain=1.0, closed=True, opens=(2, 6, 10, 14), claps=(4, 12), clapg=0.7,
         ride=False):
    for st in claps:
        s.place(s.pos(b, st), distclap(2.6), gain * clapg, 'drums')
    if closed:
        # alternate sides: pan is a level difference, so it is wide on
        # headphones and simply quieter in mono - unlike anything delay-based
        for i in range(16):
            if i % 4 == 0:
                continue
            p = 0.42 if (i // 2) % 2 else -0.42
            s.place(s.pos(b, i), panned(hat(0.6), p), gain * (0.55 if i % 2 else 0.3), 'drums')
    for st in opens:                                      # the offbeat open hat
        s.place(s.pos(b, st), panned(hat(2.4, open_=True), 0.22 if st % 8 else -0.22),
                gain * 0.38, 'drums')
    if ride:
        for i in range(0, 16, 2):
            s.place(s.pos(b, i), panned(metalhat(0.8, tone=1.3), -0.55 if i % 4 else 0.55),
                    gain * 0.22, 'drums')

def acid_a(b, gain=1.0, f_hi=3000, res=4.0, drive=4.0, low=88, dec=0.16):
    s.place(s.pos(b), acid(LINE_A, f_lo=200, f_hi=q(f_hi), res=round(res, 1),
                           drive=round(drive, 1), low=low, decay=dec), gain, 'acid')

def acid_lead(b, gain=1.0, f_hi=6000, res=4.6, octave=0):
    pat = LINE_C if not octave else [(st, n + octave, d, a, sl) for st, n, d, a, sl in LINE_C]
    s.place(s.pos(b), acid(pat, f_lo=500, f_hi=q(f_hi), res=round(res, 1), drive=4.2,
                           low=420, decay=0.11), gain, 'lead')

def poly_block(b0, gain=1.0, f_hi=3800, res=4.2, low=300):
    """15 bars of the drifting line, placed as one continuous voice"""
    s.place(s.pos(b0), acid(POLY, dur_bars=15, f_lo=300, f_hi=q(f_hi),
                            res=round(res, 1), drive=3.8, low=low, decay=0.15),
            gain, 'poly')

# ================= EINTRITT: 0-31 =================
# One line, almost closed, and the room it is in.
s.place(s.pos(0), tunnel(96, note=45, gain=1.1, motor=0.2), 1.0, 'air')
for b in range(0, 32, 4):
    s.place(s.pos(b), grind(64, note=45, gain=0.9, res=0.6, seed=b), 1.0, 'air')
for b in range(0, 32):
    acid_a(b, gain=0.5 + 0.4 * (b / 31), f_hi=sweep(b, 0, 31, 300, 2200, 1.6),
           res=3.0 + 1.0 * (b / 31), low=88)
for b in range(8, 32):
    u = (b - 8) / 23
    floor(b, gain=0.5 + 0.45 * u, lpf=260 + 190 * (b - 8) if b < 20 else None,
          grit=0.05 + 0.15 * u)
for b in range(16, 32):
    tops(b, gain=0.35 + 0.4 * ((b - 16) / 15), closed=b >= 20, claps=() if b < 24 else (4, 12),
         opens=(6, 14) if b < 24 else (2, 6, 10, 14))
s.place(s.pos(24), blip(81, 1.0), 0.4, 'music')
s.place(s.pos(31, 8), steam(6, gain=0.45), 1.0, 'fx')

# ================= SPIRALE I: 32-63 =================
for b in range(32, 64):
    ph = b - 32
    floor(b, gain=1.0, rum=0.22, drive=6.0, grit=0.25)
    tops(b, gain=0.85, ride=ph >= 16)
    acid_a(b, gain=1.0, f_hi=sweep(b, 32, 63, 2200, 4600, 0.8),
           res=4.0 + 0.5 * (ph / 31), drive=4.0 + 0.4 * (ph / 31))
    if ph % 8 == 7:
        s.place(s.pos(b, 12), servo(4, rate=22, accel=2.0, seed=b), 0.4, 'music')
for b in range(32, 64, 8):
    s.place(s.pos(b), grind(128, note=45, gain=0.8, res=0.8, seed=b), 1.0, 'air')
s.place(s.pos(48), blip(84, 1.0), 0.4, 'music')
s.place(s.pos(63, 8), reverse_crash(8, gain=0.5), 1.0, 'fx')

# ================= ZWEITE STIMME: 64-87 =================
# The second line arrives, fifteen steps long. From here nothing repeats.
poly_block(64, gain=0.62, f_hi=2600, res=4.0)
for b in range(64, 88):
    ph = b - 64
    floor(b, gain=1.0, rum=0.25, drive=6.5, grit=0.3)
    tops(b, gain=0.9, ride=True)
    acid_a(b, gain=0.95, f_hi=sweep(b, 64, 87, 4600, 3200, 1.0), res=4.4)
for b in range(64, 88, 8):
    s.place(s.pos(b), grind(128, note=45, gain=0.8, res=0.9, seed=b + 5), 1.0, 'air')
s.place(s.pos(80), blip(88, 1.0), 0.35, 'music')
s.place(s.pos(87, 8), whoosh(8, gain=0.7), 1.0, 'fx')

# ================= AUFLÖSUNG: 88-111 =================
# The drums go. Both lines keep running, into a delay, through a flanger.
s.place(s.pos(88), downlifter(16, gain=0.8), 1.0, 'fx')
s.place(s.pos(88), tunnel(160, note=45, gain=1.5, motor=0.1, seed=88), 1.0, 'air')
for b in range(88, 112, 4):
    s.place(s.pos(b), grind(64, note=45, gain=1.8, res=1.1, crush=9, seed=b), 1.0, 'air')
for b in range(88, 108):
    acid_a(b, gain=0.85, f_hi=sweep(b, 88, 107, 1200, 5200, 1.4),
           res=4.2 + 0.8 * ((b - 88) / 19), drive=3.6, dec=0.19)
poly_block(88, gain=0.5, f_hi=3000, res=4.4)
s.place_echo(s.pos(96), acid(LINE_A, f_lo=200, f_hi=3800, res=4.8, drive=4.0, low=88),
             0.35, times=3, delay_steps=6.0, fb=0.5, bus='acid')
for b in (92, 100):
    s.place(s.pos(b, 8), blip(93, 1.2), 0.4, 'music')
s.place(s.pos(104), alarm(48, f0=180, f1=520, cycles=1.5, gain=0.4), 1.0, 'fx')
for b in range(108, 112):                                  # the floor tests itself
    floor(b, gain=0.55 + 0.15 * (b - 108), steps_=(0, 8) if b < 110 else (0, 4, 8, 12),
          lpf=900 + 700 * (b - 108))
    tops(b, gain=0.4 + 0.15 * (b - 108), closed=b >= 110, claps=(), opens=(6, 14))
s.place(s.pos(108), riser(64, gain=0.85, f0=150, f1=1800), 1.0, 'fx')
s.place(s.pos(111, 12), reverse_crash(4, gain=0.85), 1.0, 'fx')

# ================= AUFSTIEG: 112-135 =================
for b in range(112, 136):
    ph = b - 112
    u = ph / 23
    floor(b, gain=1.0, rum=0.28, drive=7.0, grit=0.35)
    tops(b, gain=0.9 + 0.1 * u, ride=True)
    acid_a(b, gain=1.0, f_hi=sweep(b, 112, 135, 2600, 5600, 1.2), res=4.4 + 0.4 * u,
           drive=4.2)
    if ph >= 8:
        acid_lead(b, gain=0.3 + 0.25 * u, f_hi=sweep(b, 120, 135, 3000, 6800), res=4.4)
poly_block(112, gain=0.6, f_hi=4000, res=4.4)
for b in range(112, 136, 8):
    s.place(s.pos(b), grind(128, note=45, gain=0.8, res=1.0, seed=b), 1.0, 'air')
    s.place(s.pos(b), crash808(18, gain=0.35), 1.0, 'drums')
s.place(s.pos(128), blip(96, 1.0), 0.35, 'music')
s.place(s.pos(135, 8), steam(6, gain=0.5, seed=135), 1.0, 'fx')

# ================= TIEFE: 136-183 =================
# Three lines at once. The resonance is doing the singing.
for b in range(136, 184):
    ph = b - 136
    roll = [0, 4, 8, 10, 12, 14] if ph % 16 == 15 else None
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=0.3, drive=7.5, grit=0.4)
    tops(b, gain=1.0, ride=True)
    acid_a(b, gain=1.0, f_hi=sweep(b, 136, 167, 4200, 6000, 0.7) if ph < 32 else 5600,
           res=4.6 + 0.4 * min(ph / 32, 1), drive=4.4)
    acid_lead(b, gain=0.5 + 0.15 * min(ph / 24, 1),
              f_hi=sweep(b, 136, 183, 4200, 7400), res=4.6)
poly_block(136, gain=0.68, f_hi=4600, res=4.6)
poly_block(151, gain=0.68, f_hi=5000, res=4.8)
poly_block(166, gain=0.7, f_hi=5400, res=4.8)
for b in range(136, 184, 8):
    s.place(s.pos(b), grind(128, note=45, gain=0.8, res=1.0, seed=b + 9), 1.0, 'air')
    s.place(s.pos(b), crash808(18, gain=0.4), 1.0, 'drums')
for b in (144, 160, 176):
    s.place(s.pos(b, 8), servo(8, rate=24, accel=2.1, seed=b), 0.4, 'music')
for b in (152, 168):
    s.place(s.pos(b), alarm(48, f0=200, f1=600, cycles=1.5, gain=0.4), 1.0, 'fx')
s.place(s.pos(175), acid_throw(acid(LINE_C, f_lo=500, f_hi=6800, res=4.8, drive=4.2,
                                   low=420, decay=0.11), steps_=3.0, times=5, fb=0.5),
        0.34, 'lead')
s.place(s.pos(183, 8), whoosh(8, gain=0.8), 1.0, 'fx')

# ================= VERZERRUNG: 184-199 =================
# The floor gives way: the line is chopped, dropped in pitch and played
# backwards, and the room is put through a flanger. Once, and briefly.
s.place(s.pos(184), downlifter(14, gain=0.85), 1.0, 'fx')
raw = acid(LINE_A, f_lo=200, f_hi=4400, res=4.8, drive=4.2, low=88)
s.place(s.pos(184), pitch_warp(raw, semis=(0, -3, -7, -12), steps_=4.0), 0.7, 'acid')
s.place(s.pos(186), rev(acid(LINE_A, f_lo=200, f_hi=5200, res=5.0, drive=4.4, low=88)),
        0.6, 'acid')
for b in range(188, 196):
    acid_a(b, gain=0.8, f_hi=sweep(b, 188, 195, 900, 4800, 1.5), res=4.8, dec=0.2)
    if b >= 190:
        floor(b, gain=0.5 + 0.12 * (b - 190), steps_=(0, 8), lpf=700 + 500 * (b - 190))
s.place(s.pos(184), tunnel(96, note=45, gain=1.4, motor=0.25, seed=184), 1.0, 'air')
s.place(s.pos(190), tape_stop(acid(LINE_A, f_lo=200, f_hi=3600, res=4.6, drive=4.0,
                                   low=88), stop_s=0.9), 0.55, 'acid')
for b in range(196, 200):
    ph = b - 196
    floor(b, gain=0.75 + 0.08 * ph, lpf=2200 + 1200 * ph)
    tops(b, gain=0.5 + 0.15 * ph, closed=ph >= 2, claps=(4, 12), opens=(6, 14))
    acid_a(b, gain=0.9, f_hi=3200 + 700 * ph, res=4.8)
s.place(s.pos(196), riser(64, gain=0.95, f0=140, f1=2000), 1.0, 'fx')
s.place(s.pos(199, 12), reverse_crash(4, gain=0.95), 1.0, 'fx')

# ================= RÜCKKEHR: 200-247 =================
for b in range(200, 248):
    ph = b - 200
    roll = None
    if ph % 16 == 15:
        roll = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15]
    elif ph % 8 == 7:
        roll = [0, 4, 8, 10, 12, 14]
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=0.32, drive=8.0, grit=0.45)
    tops(b, gain=1.0, ride=True)
    acid_a(b, gain=1.0, f_hi=sweep(b, 200, 239, 5000, 6800, 0.8), res=5.0, drive=4.6)
    acid_lead(b, gain=0.62, f_hi=sweep(b, 200, 247, 5600, 7800), res=4.8)
poly_block(200, gain=0.72, f_hi=5200, res=4.8)
poly_block(215, gain=0.72, f_hi=5600, res=5.0)
poly_block(230, gain=0.74, f_hi=6000, res=5.0)
for b in range(200, 248, 8):
    s.place(s.pos(b), grind(128, note=45, gain=0.8, res=1.0, seed=b + 3), 1.0, 'air')
    s.place(s.pos(b), crash808(18, gain=0.42), 1.0, 'drums')
for b in (208, 224, 240):
    s.place(s.pos(b, 8), servo(8, rate=26, accel=2.1, seed=b), 0.42, 'music')
for b in (216, 232):
    s.place(s.pos(b), alarm(64, f0=210, f1=680, cycles=2.0, gain=0.42), 1.0, 'fx')
s.place(s.pos(239), acid_throw(acid(LINE_C, f_lo=500, f_hi=7400, res=5.0, drive=4.4,
                                   low=420, decay=0.11), steps_=3.0, times=6, fb=0.55),
        0.36, 'lead')
s.place(s.pos(247, 8), whoosh(8, gain=0.8), 1.0, 'fx')

# ================= AUSTRITT: 248-255 =================
s.place(s.pos(248), tunnel(96, note=45, gain=1.3, motor=0.15, seed=248), 1.0, 'air')
for b in range(248, 256):
    ph = b - 248
    u = ph / 7
    floor(b, gain=0.9 - 0.7 * u, lpf=5000 - 560 * ph, grit=0.1)
    tops(b, gain=0.7 - 0.6 * u, closed=ph < 4, claps=(4, 12) if ph < 3 else (),
         opens=(6, 14) if ph < 5 else ())
    acid_a(b, gain=0.9 - 0.55 * u, f_hi=4600 - 500 * ph, res=4.6 - 0.3 * ph)
s.place(s.pos(248), grind(128, note=45, gain=1.0, res=0.8, seed=248), 1.0, 'air')
s.place(s.pos(255), downlifter(16, gain=0.6), 1.0, 'fx')

# ---- bus space, then the master ----
Session.DUCKED = dict(Session.DUCKED, acid=0.62, poly=0.35, lead=0.3)
s.bus['acid'] = swirl(s.bus['acid'], rate=0.035, depth_ms=3.0, mix=0.4, stages=2)
s.bus['poly'] = autopan(s.bus['poly'], cycle_bars=11.0, depth=0.62)
s.bus['poly'] = bus_reverb(s.bus['poly'], decay=1.4, wet=0.18, tone=4600)
s.bus['lead'] = autopan(s.bus['lead'], cycle_bars=7.0, depth=0.55, phase=2.1)
s.bus['lead'] = bus_reverb(s.bus['lead'], decay=1.1, wet=0.20, tone=5200)
s.bus['music'] = bus_reverb(s.bus['music'], decay=2.0, wet=0.28, tone=5000)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.0, wet=0.32, tone=4000)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.6, wet=0.22, tone=3200)
s.bus['air'] = hp(s.bus['air'], 60)
s.bus['lead'] = hp(s.bus['lead'], 380)
s.bus['poly'] = hp(s.bus['poly'], 260)
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.85)
for b in ('drums', 'music', 'fx', 'air'):
    s.bus[b] = shelf(s.bus[b], 9500, -1.5)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)

GAINS = {'drums': 1.05, 'rumble': 0.34, 'acid': 0.88, 'poly': 0.80, 'lead': 0.68,
         'music': 0.62, 'air': 0.52, 'fx': 0.52}
s.report(GAINS)
s.render('acid_spirale_140.wav', drive=1.0, duck=0.18, clip=1.10, limit=0.94,
         peak=0.95, fade=2.5, gains=GAINS)
