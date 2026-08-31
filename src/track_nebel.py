"""NEBEL - dub techno with acid in it, 130 BPM, Bb minor.

Nebel is fog. This is the fourth four-to-the-floor record with a 303 in it,
and the way it avoids being the third one is not tempo or key - it is space.

Spirale and Saeure are dense: everything is close, dry and in your face, and
the 303 is the only voice. Here the chord is on the offbeat, filtered dark
and thrown into a delay that filters and saturates inside its own feedback
path, so the tenth repeat is a different sound from the first. The acid
arrives from somewhere behind that, and the arrangement mostly consists of
deciding how much of it you are allowed to hear. Half the notes in this track
were played once.

    NEBEL | PULS | SAEURE IM NEBEL | SOG | STROM | ENTZUG | AUFLOESUNG

208 bars, 6:24. There is one drum fill in the whole thing.
"""
import numpy as np
from industriallib import *

BAR, STEP = set_tempo(130)
BPM = 130.0
np.random.seed(130)

ROOT = 58.27                                   # Bb1
Bbm = [midi(n) for n in (58, 61, 65)]          # i
Gb  = [midi(n) for n in (54, 58, 61)]          # bVI
Ab  = [midi(n) for n in (56, 60, 63)]          # bVII
Ebm = [midi(n) for n in (51, 54, 58)]          # iv
CHORDS = [Bbm, Bbm, Gb, Ab, Bbm, Ebm, Gb, Ab]  # one per two bars: a 16-bar breath

# the 303, low and mostly hidden
LINE = [(0, 46, 2, 1, 0), (2, 46, 1, 0, 0), (3, 58, 1.5, 0, 1), (6, 49, 2, 0, 0),
        (8, 46, 2, 1, 0), (10, 53, 1, 0, 0), (13, 56, 1.5, 0, 1), (15, 47, 1, 0, 0)]
LINE2 = [(0, 46, 1.5, 1, 0), (3, 53, 1, 0, 1), (5, 46, 1, 0, 0), (6, 51, 2, 0, 0),
         (8, 58, 1.5, 1, 0), (11, 49, 1, 0, 1), (13, 46, 1, 0, 0), (14, 54, 2, 0, 0)]

s = Session(208, tail=6.0)

def chord_of(b): return CHORDS[(b // 2) % len(CHORDS)]

def floor(b, gain=1.0, steps_=(0, 4, 8, 12), lpf=None, rum=0.55, drive=4.5,
          decay=0.22, grit=0.12):
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = techkick(dur_steps=2.6, tune=ROOT, drive=drive, decay=decay, grit=grit)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if rum:
            s.place(t, rumble(dur_steps=8, tune=ROOT, decay=1.3, drive=2.0), rum, 'rumble')

def tops(b, gain=1.0, closed=True, opens=(2, 6, 10, 14), claps=()):
    for st in claps:
        s.place(s.pos(b, st), distclap(3.0), gain * 0.5, 'drums')
    if closed:
        for i in range(1, 16, 2):
            s.place(s.pos(b, i), panned(hat909(0.55), 0.3 if (i // 2) % 2 else -0.3),
                    gain * 0.3, 'drums')
    for st in opens:
        s.place(s.pos(b, st), panned(hat909(2.2, open_=True), 0.18 if st % 8 else -0.18),
                gain * 0.26, 'drums')

def chords(b, gain=1.0, steps_=(2, 6, 10, 14), dur=2.0, cutoff=1500, echo=3.0,
           times=7, fb=0.60):
    """The offbeat stab, and its weather. Only the first of each bar is thrown
    into the long delay - four of them would be fog with no shape."""
    ch = tuple(chord_of(b))
    for i, st in enumerate(steps_):
        seg = dubchord(ch, dur, cutoff=cutoff, seed=b + i)
        if i == 0:
            s.place(s.pos(b, st), dubdelay(seg, steps_=echo, times=times, fb=fb),
                    gain, 'chord')
        else:
            s.place(s.pos(b, st), seg, gain * 0.55, 'chord')

def line(b0, bars, pat=None, knob=(0.4, 0.8), res=4.0, dec=0.18, drive=3.6,
         gain=1.0, f_hi=3600, low=100, hard=0.0, bus='acid'):
    p = poly_pattern(pat or LINE, 16, bars)
    kw = dict(f_lo=180, f_hi=f_hi, res=res, drive=drive, low=low, decay=dec, knob=knob)
    seg = acid_hard(p, bars, fold_amt=hard, bite=0.7, **kw) if hard else acid(p, dur_bars=bars, **kw)
    s.place(s.pos(b0), seg, gain, bus)

# ================= NEBEL: 0-31 =================
# No kick for sixteen bars. The chord and its echo are the whole record.
s.place(s.pos(0), tunnel(160, note=46, gain=1.3, motor=0.12), 1.0, 'air')
for b in range(0, 32, 8):
    s.place(s.pos(b), grind(128, note=46, gain=0.9, res=0.6, seed=b), 1.0, 'air')
s.place(s.pos(0), crackle(128, gain=0.7), 1.0, 'air')
for b in range(2, 32, 4):
    chords(b, gain=0.85 if b < 16 else 1.0, steps_=(2,) if b < 12 else (2, 10),
           cutoff=900 + 60 * b, echo=3.0, times=8, fb=0.64)
for b in range(16, 32):
    u = (b - 16) / 15
    floor(b, gain=0.35 + 0.45 * u, lpf=200 + 300 * (b - 16) if b < 26 else None,
          rum=0.3 + 0.3 * u, grit=0.02)
    if b >= 22:
        tops(b, gain=0.4 + 0.4 * u, closed=b >= 26, opens=(6, 14))
s.place(s.pos(24), steam(8, gain=0.35), 1.0, 'fx')

# ================= PULS: 32-63 =================
for b in range(32, 64):
    floor(b, gain=0.95, rum=0.75)
    tops(b, gain=0.85, claps=(4, 12) if b >= 40 else ())
    chords(b, gain=1.0, steps_=(2, 6, 10, 14) if b % 2 == 0 else (2, 10),
           cutoff=1500, echo=3.0, times=7)
for b in range(32, 64, 8):
    s.place(s.pos(b), grind(128, note=46, gain=0.8, res=0.7, seed=b + 3), 1.0, 'air')
s.place(s.pos(56), ravesiren(16, f0=380, lfo=1.4, gain=0.3) if False else
        alarm(32, f0=150, f1=330, cycles=1.0, gain=0.25), 1.0, 'fx')

# ================= SAEURE IM NEBEL: 64-95 =================
# The acid arrives from behind the chords, filter almost shut, and opens over
# thirty-two bars. It is never louder than the chord.
for b in range(64, 96):
    floor(b, gain=1.0, rum=0.8)
    tops(b, gain=0.9, claps=(4, 12))
    chords(b, gain=1.0, steps_=(2, 6, 10, 14) if b % 2 == 0 else (2, 10), cutoff=1700)
line(64, 16, knob=(0.14, 0.40, 0.26), res=3.6, dec=0.20, drive=3.4, f_hi=2800, gain=0.55)
line(80, 16, knob=(0.34, 0.64, 0.48), res=4.0, dec=0.19, drive=3.6, f_hi=3400, gain=0.72)
for b in range(64, 96, 8):
    s.place(s.pos(b), grind(128, note=46, gain=0.8, res=0.8, seed=b + 7), 1.0, 'air')
s.place(s.pos(88), blip(82, 1.2), 0.3, 'music')

# ================= SOG: 96-119 =================
s.place(s.pos(96), downlifter(16, gain=0.6), 1.0, 'fx')
s.place(s.pos(96), tunnel(192, note=46, gain=1.6, motor=0.08, seed=96), 1.0, 'air')
for b in range(96, 120, 4):
    ch = tuple(chord_of(b))
    seg = dubchord(ch, 3.0, cutoff=1100, seed=b)
    s.place(s.pos(b, 2), dubdelay(seg, steps_=3.0, times=10, fb=0.70, damp=700),
            1.15, 'chord')
line(96, 16, pat=LINE2, knob=(0.50, 0.86, 0.34), res=4.4, dec=0.21, drive=3.4,
     f_hi=4000, gain=0.85)
for b in range(96, 120, 8):
    s.place(s.pos(b), grind(128, note=46, gain=1.8, res=1.0, crush=9, seed=b), 1.0, 'air')
for b in (108, 114):                                    # two kicks, a promise
    floor(b, gain=0.6, steps_=(0,), rum=0.6, lpf=1200)
for b in range(116, 120):
    floor(b, gain=0.6 + 0.12 * (b - 116), steps_=(0, 8) if b < 118 else (0, 4, 8, 12),
          lpf=800 + 800 * (b - 116), rum=0.6)
    tops(b, gain=0.4 + 0.12 * (b - 116), closed=b >= 118, opens=(6, 14))
s.place(s.pos(116), riser(48, gain=0.7, f0=140, f1=1400), 1.0, 'fx')

# ================= STROM: 120-159 =================
for b in range(120, 160):
    ph = b - 120
    floor(b, gain=1.0, rum=0.9, drive=5.0, grit=0.18)
    tops(b, gain=1.0, claps=(4, 12))
    chords(b, gain=1.05, steps_=(2, 6, 10, 14), cutoff=1900, echo=3.0, times=8, fb=0.62)
    if ph == 31:                                        # the one fill
        for st in (12, 13, 14, 15):
            s.place(s.pos(b, st), distclap(1.6), 0.45, 'drums')
line(120, 16, knob=(0.62, 0.94, 0.74, 1.0), res=4.4, dec=0.17, drive=3.8, f_hi=4400,
     gain=0.88, hard=0.20)
line(136, 16, pat=LINE2, knob=(0.86, 0.66, 1.0, 0.80), res=4.6, dec=0.16, drive=4.0,
     f_hi=4800, gain=0.92, hard=0.26)
line(152, 8,  knob=(0.90, 1.0), res=4.6, dec=0.16, drive=4.0, f_hi=5000, gain=0.92,
     hard=0.28)
for b in range(120, 160, 8):
    s.place(s.pos(b), grind(128, note=46, gain=0.8, res=0.9, seed=b + 11), 1.0, 'air')
    s.place(s.pos(b), crash808(20, gain=0.25), 1.0, 'drums')
for b in (128, 144):
    s.place(s.pos(b), alarm(48, f0=170, f1=420, cycles=1.0, gain=0.28), 1.0, 'fx')

# ================= ENTZUG: 160-183 =================
for b in range(160, 184):
    ph = b - 160
    u = ph / 23
    floor(b, gain=1.0 - 0.25 * u, rum=0.9 - 0.2 * u, drive=4.8)
    tops(b, gain=0.9 - 0.4 * u, claps=(4, 12) if ph < 12 else (12,),
         closed=ph < 16, opens=(6, 14))
    chords(b, gain=1.0, steps_=(2, 6, 10, 14) if ph < 12 else (2, 10),
           cutoff=1900 - 40 * ph, echo=3.0, times=9, fb=0.66)
line(160, 16, knob=(0.86, 0.50, 0.70, 0.34), res=4.4, dec=0.18, drive=3.8, f_hi=4400,
     gain=0.80, hard=0.18)
line(176, 8,  knob=(0.40, 0.16), res=4.0, dec=0.20, drive=3.4, f_hi=3400, gain=0.60)
for b in range(160, 184, 8):
    s.place(s.pos(b), grind(128, note=46, gain=0.9, res=0.8, seed=b), 1.0, 'air')

# ================= AUFLOESUNG: 184-207 =================
s.place(s.pos(184), tunnel(160, note=46, gain=1.5, motor=0.06, seed=184), 1.0, 'air')
s.place(s.pos(184), crackle(160, gain=0.8), 1.0, 'air')
for b in range(184, 208):
    ph = b - 184
    u = ph / 23
    if ph < 14:
        floor(b, gain=0.75 - 0.6 * u, steps_=(0, 4, 8, 12) if ph < 8 else (0, 8),
              lpf=3000 - 180 * ph, rum=0.7 - 0.5 * u, grit=0.0)
    if ph < 10:
        tops(b, gain=0.5 - 0.4 * u, closed=ph < 5, opens=(6, 14) if ph < 8 else ())
for b in range(184, 206, 4):
    ch = tuple(chord_of(b))
    seg = dubchord(ch, 3.0, cutoff=1300 - 40 * (b - 184), seed=b)
    s.place(s.pos(b, 2), dubdelay(seg, steps_=3.0, times=11, fb=0.72, damp=650),
            1.0 - 0.5 * ((b - 184) / 22), 'chord')
s.place(s.pos(206), downlifter(20, gain=0.4), 1.0, 'fx')

# ---- bus space, then the master ----
Session.DUCKED = dict(Session.DUCKED, acid=0.45, chord=0.72)
s.bus['chord'] = bus_reverb(s.bus['chord'], decay=4.0, wet=0.30, tone=2800)
s.bus['acid'] = bus_reverb(s.bus['acid'], decay=2.0, wet=0.20, tone=3600)
s.bus['air'] = bus_reverb(s.bus['air'], decay=3.4, wet=0.26, tone=2600)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=3.6, wet=0.32, tone=3400)
s.bus['acid'] = autopan(s.bus['acid'], cycle_bars=17.0, depth=0.34, phase=0.9)
s.bus['chord'] = hp(s.bus['chord'], 170)
s.bus['air'] = hp(s.bus['air'], 70)
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.85)
for b in ('drums', 'air', 'fx'):
    s.bus[b] = shelf(s.bus[b], 9000, -2.5)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)

GAINS = {'drums': 0.98, 'rumble': 0.54, 'acid': 0.72, 'chord': 1.15,
         'music': 0.50, 'air': 0.60, 'fx': 0.50}
s.report(GAINS)
s.render('acid_nebel_130.wav', drive=1.0, duck=0.20, clip=1.10, limit=0.94,
         peak=0.95, fade=4.0, gains=GAINS)
