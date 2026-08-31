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
LINE_A2 = [(0, 45, 2, 1, 0), (2, 48, 1, 0, 0), (3, 45, 1, 0, 0), (5, 57, 1.5, 1, 1),
           (7, 45, 1, 0, 0), (8, 46, 1.5, 0, 0), (10, 45, 1, 0, 0), (11, 52, 1, 0, 1),
           (13, 45, 1, 0, 0), (14, 55, 2, 1, 0)]
LINE_A3 = [(0, 45, 1, 1, 0), (1, 45, 1, 0, 0), (2, 52, 1, 0, 1), (3, 45, 1, 0, 0),
           (4, 57, 1.5, 1, 0), (6, 48, 1, 0, 0), (7, 45, 1, 0, 0), (8, 45, 1, 1, 0),
           (9, 55, 1, 0, 1), (10, 45, 1, 0, 0), (12, 46, 1.5, 0, 0), (14, 52, 2, 1, 1)]
LINE_C = [(0, 57, 1, 1, 0), (1, 57, 1, 0, 0), (2, 60, 1, 0, 1), (4, 64, 1.5, 1, 0),
          (6, 57, 1, 0, 0), (7, 62, 1, 0, 0), (8, 57, 1, 1, 0), (10, 69, 1.5, 0, 1),
          (12, 60, 1, 0, 0), (14, 57, 2, 1, 0)]

POLY = poly_pattern(LINE_B, 15, 15)            # one 15-bar block of the drifting line

s = Session(256, tail=4.0)

def q(v, step=50):
    """quantise a swept parameter so the cache still works"""
    return round(v / step) * step

def hat909(dur_steps=0.6, open_=False, gain=1.0, tone=1.0, seed=0):
    """A 909-ish hat: noise band-limited, not merely highpassed.

    core's hat() keeps only what is above 8 kHz. One of those is a tick; a
    line of them on sixteenths is a continuous crackle at the top of the
    spectrum, because there is no body underneath for the ear to hear as an
    instrument. Give it 3.8-12 kHz and it becomes a hi-hat again."""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 2.6))
    rs = np.random.RandomState(seed + 77)
    x = bandpass(stereo(rs.randn(n)), 3800 * tone, 12000 * tone)
    dec = 0.20 if open_ else 0.028
    return x * (np.exp(-t / dec) * adsr(n, a=0.0006, r=0.008))[:, None] * gain * 0.55

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
            s.place(s.pos(b, i), panned(hat909(0.6), p), gain * (0.55 if i % 2 else 0.3), 'drums')
    for st in opens:                                      # the offbeat open hat
        s.place(s.pos(b, st), panned(hat909(2.4, open_=True), 0.22 if st % 8 else -0.22),
                gain * 0.38, 'drums')
    if ride:
        for i in range(0, 16, 2):
            s.place(s.pos(b, i), panned(metalhat(0.8, tone=1.3), -0.55 if i % 4 else 0.55),
                    gain * 0.22, 'drums')

def phrase(b0, bars, pat=None, knob=(0.5, 1.0), res=4.4, dec=0.16, drive=4.2,
           wave='saw', gain=1.0, f_hi=5200, f_lo=200, low=88, cycle=16, bus='acid'):
    """One pass of the 303, rendered in a single call so the oscillator phase
    never restarts, with the cutoff knob swept across the whole phrase.

    Every argument here is a knob on the front panel, and the point of the
    track is that no two phrases have them in the same place: waveform, cutoff
    sweep shape, resonance, envelope decay and drive all move."""
    p = poly_pattern(pat or LINE_A, cycle, bars)
    s.place(s.pos(b0), acid(p, dur_bars=bars, f_lo=f_lo, f_hi=f_hi, res=res,
                            drive=drive, low=low, decay=dec, wave=wave, knob=knob),
            gain, bus)

def acid_lead(b, gain=1.0, f_hi=6000, res=4.6, octave=0):
    pat = LINE_C if not octave else [(st, n + octave, d, a, sl) for st, n, d, a, sl in LINE_C]
    s.place(s.pos(b), acid(pat, f_lo=500, f_hi=q(f_hi), res=round(res, 1), drive=4.2,
                           low=420, decay=0.11), gain, 'lead')

def acid_sub(b0, bars, pat=None, gain=1.0, cycle=16):
    """A clean octave under the 303: weight, no character. The character is
    already happening upstairs, and two distorted things in the same octave
    is how a low end turns to mud."""
    p = poly_pattern(pat or LINE_A, cycle, bars)
    seg = acid(p, dur_bars=bars, f_lo=70, f_hi=190, res=0.5, drive=2.2, low=28,
               decay=0.22, sub=0.95, knob=(1.0,))
    s.place(s.pos(b0), lp(seg, 150), gain, 'sub')

def acid_grit(b0, bars, pat=None, gain=1.0, cycle=16, drive=6.5, f_hi=2400,
              fold_=1.15):
    """The same line driven until it tears, then band-limited to the mids.
    This is where 'harder' actually lives - not in the sub, which only has
    room for one clean thing, but in the 200-1800 Hz an ear reads as force."""
    p = poly_pattern(pat or LINE_A, cycle, bars)
    seg = acid(p, dur_bars=bars, f_lo=260, f_hi=f_hi, res=3.0, drive=drive,
               low=150, decay=0.15, knob=(0.9, 1.0))
    s.place(s.pos(b0), bandpass(fold(seg, fold_), 190, 1900), gain, 'grit')

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
phrase(0,  8, knob=(0.10, 0.30), res=3.0, dec=0.22, drive=3.4, f_hi=3200, gain=0.60)
phrase(8,  8, knob=(0.26, 0.48), res=3.4, dec=0.20, drive=3.6, f_hi=3800, gain=0.75)
phrase(16, 8, pat=LINE_A2, knob=(0.42, 0.66), res=3.8, dec=0.18, drive=3.8,
       f_hi=4400, gain=0.88)
phrase(24, 8, knob=(0.58, 0.86, 0.70), res=4.0, dec=0.16, drive=4.0, f_hi=4800, gain=1.0)
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
    floor(b, gain=1.0, rum=0.0, drive=6.0, grit=0.25)
    tops(b, gain=0.85, ride=ph >= 16)
    if ph % 8 == 7:
        s.place(s.pos(b, 12), servo(4, rate=22, accel=2.0, seed=b), 0.4, 'music')
phrase(32, 8, knob=(0.72, 1.0, 0.84), res=4.2, dec=0.16, drive=4.2, f_hi=5000)
phrase(40, 8, wave='square', knob=(0.80, 0.58, 0.96), res=4.4, dec=0.15, drive=4.0,
       f_hi=4600)                                    # the other switch on the 303
phrase(48, 8, pat=LINE_A3, knob=(0.70, 1.0), res=4.6, dec=0.13, drive=4.4, f_hi=5400)
phrase(56, 8, knob=(0.92, 0.66, 1.0), res=4.4, dec=0.17, drive=4.2, f_hi=5200)
for b in range(32, 64, 8):
    s.place(s.pos(b), grind(128, note=45, gain=0.8, res=0.8, seed=b), 1.0, 'air')
s.place(s.pos(48), blip(84, 1.0), 0.4, 'music')
s.place(s.pos(63, 8), reverse_crash(8, gain=0.5), 1.0, 'fx')

# ================= ZWEITE STIMME: 64-87 =================
# The second line arrives, fifteen steps long. From here nothing repeats.
poly_block(64, gain=0.62, f_hi=2600, res=4.0)
phrase(64, 8, pat=LINE_A2, knob=(0.88, 0.52), res=4.4, dec=0.18, drive=4.2,
       f_hi=5000, gain=0.95)
phrase(72, 8, knob=(0.55, 1.0), res=4.8, dec=0.14, drive=4.4, f_hi=5600, gain=0.95)
phrase(80, 8, wave='square', pat=LINE_A3, knob=(0.90, 0.62, 0.98), res=4.6, dec=0.16,
       drive=4.0, f_hi=4800, gain=0.95)
for b in range(64, 88):
    ph = b - 64
    floor(b, gain=1.0, rum=0.0, drive=6.5, grit=0.3)
    tops(b, gain=0.9, ride=True)
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
# a twelve-bar hand on the knob: right down, then all the way open
phrase(88,  12, knob=(0.18, 0.55, 1.0), res=4.6, dec=0.21, drive=3.6, f_hi=5800,
       gain=0.88)
phrase(100, 8,  pat=LINE_A2, knob=(0.95, 0.40, 1.0), res=5.0, dec=0.17, drive=3.8,
       f_hi=6200, gain=0.88)
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
    floor(b, gain=1.0, rum=0.12, drive=7.0, grit=0.35)
    tops(b, gain=0.9 + 0.1 * u, ride=True)
    if ph >= 8:
        acid_lead(b, gain=0.3 + 0.25 * u, f_hi=sweep(b, 120, 135, 3000, 6800), res=4.4)
phrase(112, 8, knob=(0.48, 0.80), res=4.4, dec=0.18, drive=4.2, f_hi=5000)
phrase(120, 8, pat=LINE_A3, knob=(0.74, 0.96), res=4.6, dec=0.14, drive=4.4, f_hi=5600)
phrase(128, 8, wave='square', knob=(0.86, 1.0, 0.90), res=4.8, dec=0.15, drive=4.2,
       f_hi=5400)
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
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=0.26, drive=7.5, grit=0.4)
    tops(b, gain=1.0, ride=True)
    acid_lead(b, gain=0.5 + 0.15 * min(ph / 24, 1),
              f_hi=sweep(b, 136, 183, 4200, 7400), res=4.6)
phrase(136, 8, knob=(0.82, 1.0), res=4.6, dec=0.16, drive=4.4, f_hi=5800)
for _b in range(136, 184, 8):                        # weight underneath, from here on
    acid_sub(_b, 8, gain=0.42 + 0.10 * ((_b - 136) / 40))
acid_grit(152, 8, pat=LINE_A3, gain=0.26, drive=6.0)
acid_grit(168, 8, pat=LINE_A2, gain=0.32, drive=6.4)
acid_grit(176, 8, gain=0.38, drive=6.8)
phrase(144, 8, pat=LINE_A2, knob=(1.0, 0.62, 0.92), res=5.0, dec=0.13, drive=4.6,
       f_hi=6200)
phrase(152, 8, wave='square', pat=LINE_A3, knob=(0.70, 1.0), res=4.8, dec=0.15,
       drive=4.4, f_hi=5600)
phrase(160, 8, knob=(0.95, 0.55, 1.0), res=5.2, dec=0.12, drive=4.8, f_hi=6600)
phrase(168, 8, pat=LINE_A2, knob=(0.66, 0.98), res=4.8, dec=0.18, drive=4.4, f_hi=6000)
phrase(176, 8, wave='square', knob=(1.0, 0.74), res=5.0, dec=0.14, drive=4.6, f_hi=6400)
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
phrase(188, 8, pat=LINE_A3, knob=(0.12, 0.45, 1.0), res=4.8, dec=0.20, drive=4.0,
       f_hi=6000, gain=0.80)
for b in range(188, 196):
    if b >= 190:
        floor(b, gain=0.5 + 0.12 * (b - 190), steps_=(0, 8), lpf=700 + 500 * (b - 190))
s.place(s.pos(184), tunnel(96, note=45, gain=1.4, motor=0.25, seed=184), 1.0, 'air')
s.place(s.pos(190), tape_stop(acid(LINE_A, f_lo=200, f_hi=3600, res=4.6, drive=4.0,
                                   low=88), stop_s=0.9), 0.55, 'acid')
phrase(196, 4, knob=(0.62, 1.0), res=4.8, dec=0.15, drive=4.4, f_hi=6000, gain=0.9)
for b in range(196, 200):
    ph = b - 196
    floor(b, gain=0.75 + 0.08 * ph, lpf=2200 + 1200 * ph)
    tops(b, gain=0.5 + 0.15 * ph, closed=ph >= 2, claps=(4, 12), opens=(6, 14))
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
    floor(b, gain=1.0, steps_=roll or (0, 4, 8, 12), rum=0.44, drive=8.0, grit=0.5)
    tops(b, gain=1.0, ride=True)
    acid_lead(b, gain=0.62, f_hi=sweep(b, 200, 247, 5600, 7800), res=4.8)
phrase(200, 8, knob=(0.86, 1.0), res=5.0, dec=0.15, drive=4.6, f_hi=6200)
for _b in range(200, 248, 8):
    acid_sub(_b, 8, gain=0.72 + 0.22 * ((_b - 200) / 40))
    acid_grit(_b, 8, pat=(LINE_A3 if (_b // 8) % 2 else LINE_A2),
              gain=0.44 + 0.16 * ((_b - 200) / 40),
              drive=7.0 + 1.4 * ((_b - 200) / 40),
              fold_=1.15 + 0.25 * ((_b - 200) / 40))
phrase(208, 8, pat=LINE_A3, knob=(1.0, 0.70, 1.0), res=5.2, dec=0.12, drive=4.8,
       f_hi=6800)
phrase(216, 8, wave='square', pat=LINE_A2, knob=(0.78, 1.0), res=5.0, dec=0.16,
       drive=4.6, f_hi=6400)
phrase(224, 8, knob=(1.0, 0.60, 1.0), res=5.4, dec=0.13, drive=5.0, f_hi=7000)
phrase(232, 8, pat=LINE_A3, knob=(0.90, 1.0), res=5.2, dec=0.14, drive=4.8, f_hi=6800)
phrase(240, 8, wave='square', knob=(1.0, 0.82), res=5.0, dec=0.15, drive=4.6, f_hi=6600)
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
phrase(248, 8, knob=(0.80, 0.12), res=4.4, dec=0.18, drive=4.0, f_hi=5200, gain=0.85)
for b in range(248, 256):
    ph = b - 248
    u = ph / 7
    floor(b, gain=0.9 - 0.7 * u, lpf=5000 - 560 * ph, grit=0.1)
    tops(b, gain=0.7 - 0.6 * u, closed=ph < 4, claps=(4, 12) if ph < 3 else (),
         opens=(6, 14) if ph < 5 else ())
s.place(s.pos(248), grind(128, note=45, gain=1.0, res=0.8, seed=248), 1.0, 'air')
s.place(s.pos(255), downlifter(16, gain=0.6), 1.0, 'fx')

# ---- bus space, then the master ----
Session.DUCKED = dict(Session.DUCKED, acid=0.62, sub=0.95, grit=0.5,
                      poly=0.35, lead=0.3)
s.bus['acid'] = swirl(s.bus['acid'], rate=0.035, depth_ms=3.0, mix=0.4, stages=2)
# The 303 itself drifts too, slowly and on a cycle that shares no factor with
# the other two. mono_below() further down pins its bottom to the centre, so
# only the part of it above 150 Hz actually travels.
s.bus['acid'] = autopan(s.bus['acid'], cycle_bars=13.0, depth=0.30, phase=1.1)
s.bus['poly'] = autopan(s.bus['poly'], cycle_bars=11.0, depth=0.72)
s.bus['poly'] = bus_reverb(s.bus['poly'], decay=1.4, wet=0.18, tone=4600)
s.bus['lead'] = autopan(s.bus['lead'], cycle_bars=5.0, depth=0.78, phase=2.1)
s.bus['lead'] = bus_reverb(s.bus['lead'], decay=1.1, wet=0.20, tone=5200)
s.bus['music'] = bus_reverb(s.bus['music'], decay=2.0, wet=0.28, tone=5000)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.0, wet=0.32, tone=4000)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.6, wet=0.22, tone=3200)
s.bus['air'] = hp(s.bus['air'], 60)
s.bus['lead'] = hp(s.bus['lead'], 380)
s.bus['poly'] = hp(s.bus['poly'], 260)
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.85)
for b in ('drums', 'music', 'fx', 'air'):
    s.bus[b] = shelf(s.bus[b], 9500, -2.5)
s.bus['drums'] = lp(s.bus['drums'], 15000)     # noise above this is hiss, not hat
s.bus['acid'] = lp(s.bus['acid'], 12000)       # nor does a 303 have anything up there
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)

GAINS = {'drums': 0.94, 'rumble': 0.32, 'acid': 0.78, 'sub': 0.60, 'grit': 0.38,
         'poly': 0.74, 'lead': 0.62, 'music': 0.58, 'air': 0.48, 'fx': 0.48}
s.report(GAINS)
s.render('acid_spirale_140.wav', drive=1.0, duck=0.18, clip=1.10, limit=0.94,
         peak=0.95, fade=2.5, gains=GAINS)
