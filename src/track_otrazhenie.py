"""OTRAZHENIE - hypnotic minimal techno at 131 BPM, A minor / A Phrygian.

Otrazhenie is Russian for reflection, and for an echo. The chord in this
record is played about forty times in eight minutes; what the listener
follows is not the chord but the six copies of it that come back, each one
darker, quieter and a little further out of tune than the last. The stab is
written to be thrown away - 55 ms of decay, high-passed at 230 Hz, no
sustain - because a stab with a tail turns a delay into mud inside two
repeats. `dubecho` supplies the tape: a geometric darkening per pass,
saturation in the loop, and a transport that never quite held speed.

The companion piece to `maskarad`, and deliberately built from the opposite
choices in every dimension that matters. There the bass rolled in sixteenths
and the sub was felt in gaps; here `holdbass` sustains through the whole bar
and the sidechain puts it down four times a beat, so the pump is the bass
part rather than an effect on it. There the hook was a plucked melody with a
filter closing on every note; here it is a chord and its reflections, and
the melodic line is `syncarp` - a hard sync whose *waveform* tears while the
pitch stays put, which is the one timbre a filter cannot make. There the
grid was dead straight; here the hats and shakers swing 55% and the kick
does not, which is the whole difference between a machine and a groove.

The harmony is one chord. Six bars of i, then two of bII - the Phrygian flat
second, the only note in the record from outside the key, and the reason a
loop this long does not settle.

    INTRO (32) | FLOOR (32) | THE ROOM (32) | THE ARP (32)
    | DISSOLVE - breakdown (24) + build (8) | THE LOCK (48) | OUTRO (32)

240 bars, 7:20. The lowest point is bar 128 and the highest starts at 160 -
67% of the way in. Change arrives every sixteen bars and never every eight:
patience is this genre's aesthetic, not a shortage of ideas.
"""
import numpy as np
import minimallib as M

M.set_tempo(131)                       # re-grid before a single voice renders
from minimallib import *

np.random.seed(1310)

# ---- the material ----
TUNE = 55.0                                        # A1 - the kick and the floor
SWING = 0.10                                       # 55%: hats and shakers only

def sw(i, amt=SWING):
    """delay every second sixteenth, and nothing else"""
    return i + (amt if i % 2 else 0.0)

# The chord, rootless, and its one departure. Six bars of i, two of bII.
STAB_i  = tuple(midi(n) for n in (60, 64, 67, 71))     # C E G B  = Am9
STAB_II = tuple(midi(n) for n in (62, 65, 69, 72))     # D F A C  = Bbmaj9, the bII
STAB_VI = tuple(midi(n) for n in (60, 65, 69, 72))     # C F A C  = F6/9, the breakdown

def stab_of(b):
    return STAB_II if b % 8 >= 6 else STAB_i

# The sub holds; the pattern is one note a bar and the sidechain does the rest.
SUB = [(0, 33, 16.0, 0, 0)] + [(16, 33, 16.0, 0, 0)] + \
      [(32, 33, 16.0, 0, 0)] + [(48, 34, 16.0, 0, 0)]        # bar 4 goes to the bII
# The mid bass answers on the offbeat eighths, where the kick is not.
# No accents: an accent on an offbeat eighth is an accent against the kick,
# and the body loses the beat long before it notices the bass got louder.
MID = [(st + 16 * bar, n, 1.8, 0, 0, v * w)
       for bar, (n, v) in enumerate(((33, 0.90), (33, 0.84), (33, 0.90), (34, 0.82)))
       for st, w in ((2, 1.0), (6, 0.86), (10, 0.96), (14, 0.84))]

# A minor pentatonic, seven notes to a sixteen-step bar, so the figure starts
# somewhere new every bar and does not come back around until bar seven.
ARP = arp_seq([64, 69, 72, 76], bars=4, shape='updown', rate=1.0, cycle=7,
              octaves=(0, 1), gate=(1, 1, 0, 1, 1, 0, 1), accents=(0, 4),
              jitter=0.015, seed=3)
# The struck metal, as a melody on the grid.
#
# This was a five-step cycle against a sixteen-step bar - the coprime trick
# that keeps a loop alive. It does not work for a voice with a pitch and a
# ring: every gap comes out at five sixteenths, which at 131 BPM is 572 ms
# against a 458 ms beat, and a pulse that close to the beat without being it
# is heard as a mistake rather than as a device. Short dry ticks may drift;
# anything that rings reads as a part, and a part has to be in time.
#
# So: a fixed spine on steps 4, 10 and 14 - beat two and the two offbeat
# eighths of the second half - which answers the kick instead of arguing
# with it. Eight bars, matching the harmony: six of i and two of the
# Phrygian bII, with the top note in bar 4, halfway.
CLANG = [
    [(4, 81, 0.80), (10, 79, 0.62), (14, 76, 0.70)],
    [(4, 79, 0.78), (10, 76, 0.60), (14, 72, 0.68)],
    [(4, 76, 0.78), (8, 74, 0.66), (14, 76, 0.70)],
    [(4, 79, 0.80), (10, 81, 0.64), (14, 83, 0.72)],
    [(4, 84, 0.86), (10, 81, 0.66), (14, 79, 0.72)],          # the top
    [(4, 81, 0.80), (10, 79, 0.62), (14, 76, 0.68)],
    [(4, 82, 0.82), (8, 79, 0.66), (14, 77, 0.70)],           # Bb - the bII
    [(4, 79, 0.76), (10, 77, 0.60), (13, 76, 0.42), (14, 74, 0.68)],
]
CLPAN = {4: -0.30, 8: 0.34, 10: 0.26, 13: -0.44, 14: 0.18}
# the tresillo, on toms - the one figure in the record that is not on the grid
TOMS = ((0, 45, 0.30), (3, 40, 0.42), (6, 45, 0.26), (11, 38, 0.40), (14, 45, 0.24))

# Where each thing stands. Fixed, so the image is the same every bar.
SHKPAN   = (-0.16, 0.28, 0.11, -0.32)

# The sustained sub and the offbeat mid both sit between kicks, so both have
# to be put down hard; the pump is this record's bass part.
Session.DUCKED = dict(Session.DUCKED, mid=0.90, bass=1.0)

s = Session(240, tail=6.0)

# ---- the parts ----
def floor(b, gain=1.0, lpf=None, tail=1.0, steps_=(0, 4, 8, 12)):
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = mkick(tune=TUNE, decay=0.162, punch=1.35, knock=0.78, top=215.0)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if tail:
            s.place(t, ktail(tune=TUNE, decay=0.24), tail * gain, 'sub')

def tops(b, gain=1.0, ride=True, hats=True, shakers=True, claps=(4, 12),
         opens=(), clapg=0.8):
    if ride:
        for i in range(0, 16, 2):
            s.place(s.pos(b, i), panned(mride(seed=i), -0.26 if i % 4 else -0.10),
                    gain * (0.72 if i % 4 == 0 else 0.46), 'drums')
    for st in claps:
        s.place(s.pos(b, st), mclap(seed=b % 3, room=0.30, spread=0.8),
                gain * clapg, 'drums')
    for st in opens:
        s.place(s.pos(b, sw(st)), mhat(open_=True, seed=st), gain * 0.42, 'drums')
    if hats:
        for i in (1, 3, 5, 7, 9, 11, 13, 15):
            v = 0.50 if i in (3, 11) else 0.30
            s.place(s.pos(b, sw(i)), panned(mhat(seed=i), 0.24 if i % 4 == 1 else -0.20),
                    gain * v, 'drums')
    if shakers:
        for i in range(16):
            v = 0.58 if i % 4 == 2 else (0.40 if i % 2 == 0 else 0.24)
            s.place(s.pos(b, sw(i)), panned(shaker(seed=i), SHKPAN[i % 4]),
                    gain * v * 0.62, 'drums')

def perc(b, gain=1.0, clangs=True, toms=True, rims=True, dusty=True):
    if clangs:
        for st, note, v in CLANG[b % 8]:
            s.place(s.pos(b, st), panned(clang(note=note, decay=0.075, seed=st),
                                         CLPAN[st]),
                    gain * v * 0.62, 'perc')
    if toms:
        for st, note, v in TOMS:
            s.place(s.pos(b, st), panned(tom(note=note, decay=0.085, seed=st),
                                         0.22 if st % 3 else -0.26),
                    gain * v, 'perc')
    if rims:
        for st in (7, 13):
            s.place(s.pos(b, sw(st)), panned(rimtick(f=1490 + 120 * (st % 3), seed=st),
                                             0.52 if st == 7 else -0.46),
                    gain * 0.38, 'perc')
    if dusty and b % 4 == 0:
        s.place(s.pos(b), dust(64, gain=0.85, seed=b, lo=2600, hi=12000), 1.0, 'air')

def stabbar(b, gain=1.0, fb=0.55, times=6, step=6.0, dark=0.60, notes=None,
            drive=1.9, dur=1.4):
    """the chord, and the six reflections that are the actual part"""
    seg = dubstab(notes or stab_of(b), dur)
    s.place(s.pos(b, step),
            dubecho(seg, steps_=3.0, times=times, fb=fb, damp0=5200,
                    darken=dark, hp_hz=280, drive=drive, drift=1.1,
                    spread=0.44, seed=b),
            gain, 'music')

def bass(b, gain=1.0, mid=1.0):
    s.place(s.pos(b), holdbass(SUB, 4), gain, 'bass')
    if mid:
        s.place(s.pos(b), midbass(MID, 4, decay=0.10, cut_decay=0.055,
                                  f_hi=2100.0, res=2.8), gain * mid, 'mid')

def arp(b, gain=1.0, r0=3.4, decay=0.075, f_hi=7000.0):
    for (st, note, dur, v) in ARP:
        if int(st) // 16 != b % 4:
            continue
        s.place(s.pos(b, st - (b % 4) * 16),
                syncarp(midi(int(note)), max(dur, 0.8), r0=r0, decay=decay,
                        f_hi=f_hi),
                gain * v * 0.9, 'arp')

# ================= INTRO  bars 0-31 =================
# Thirty-two bars of kick and a ride. Techno introduces one element at a time
# and the unit of change is sixteen bars, not eight.
for b in range(0, 32):
    u = b / 31
    floor(b, gain=0.42 + 0.50 * u, lpf=620 + 330 * b,
          tail=0.0 if b < 8 else 0.55 * (b - 8) / 24)
    tops(b, gain=0.30 + 0.45 * u, ride=b >= 4, hats=b >= 16, shakers=b >= 12,
         claps=() if b < 24 else (4, 12), clapg=0.6)
    if b >= 20:
        perc(b, gain=0.34 + 0.3 * u, clangs=b >= 24, toms=False, rims=True)
s.place(s.pos(0), hum(33, 64, gain=0.55, seed=1, cutoff=380), 1.0, 'air')
s.place(s.pos(16), hum(33, 64, gain=0.6, seed=2, cutoff=520), 1.0, 'air')
s.place(s.pos(0), sweepnoise(128, gain=0.5, f0=240, f1=6000, seed=1), 1.0, 'air')
s.place(s.pos(24), sweepnoise(64, gain=0.55, f0=500, f1=9000, seed=2), 1.0, 'air')

# ================= THE FLOOR  bars 32-63 =================
for b in range(32, 64):
    u = (b - 32) / 31
    floor(b, tail=0.9)
    tops(b, gain=0.85 + 0.15 * u, opens=(2, 10) if b >= 48 else ())
    perc(b, gain=0.7 + 0.3 * u, toms=b >= 40)
for b in range(32, 64, 4):
    bass(b, gain=0.75 if b < 40 else 1.0, mid=0.0 if b < 48 else 0.85)
s.place(s.pos(32), hum(33, 64, gain=0.45, seed=3, cutoff=620), 1.0, 'air')
s.place(s.pos(56), sweepnoise(64, gain=0.6, f0=400, f1=10000, seed=3), 1.0, 'air')

# ================= THE ROOM  bars 64-95 =================
# the chord arrives, and the feedback opens over thirty-two bars
for b in range(64, 96):
    u = (b - 64) / 31
    floor(b)
    tops(b, opens=(2, 10))
    perc(b)
    if b % 2 == 0:
        stabbar(b, gain=0.55 + 0.35 * u, fb=0.36 + 0.24 * u,
                times=4 + int(3 * u), dark=0.52 + 0.10 * u)
for b in range(64, 96, 4):
    bass(b)
s.place(s.pos(64), mcrash(24, gain=0.5), 1.0, 'fx')
s.place(s.pos(80), sweepnoise(96, gain=0.55, f0=350, f1=11000, seed=4), 1.0, 'air')
s.place(s.pos(88), hum(33, 32, gain=0.35, seed=4, cutoff=760), 1.0, 'air')

# ================= THE ARP  bars 96-127 =================
for b in range(96, 128):
    u = (b - 96) / 31
    floor(b)
    tops(b, opens=(2, 10, 14))
    perc(b)
    arp(b, gain=0.55 + 0.40 * u, r0=2.6 + 1.4 * u, f_hi=4800 + 2600 * u)
    if b % 2 == 0:
        stabbar(b, gain=0.92, fb=0.58, times=7, dark=0.62)
for b in range(96, 128, 4):
    bass(b)
for b in range(112, 128, 4):
    s.place(s.pos(b), acid(ARP_ACID := [(0, 45, 1.5, 1, 0), (3, 45, 1.0, 0, 0),
                                        (5, 57, 1.5, 0, 1), (8, 45, 1.5, 1, 0),
                                        (11, 52, 1.0, 0, 0), (13, 45, 1.0, 0, 1),
                                        (16, 45, 1.0, 1, 0), (18, 57, 1.5, 0, 1),
                                        (21, 48, 1.0, 0, 0), (24, 45, 1.5, 1, 1),
                                        (27, 52, 1.0, 0, 0), (29, 45, 2.0, 0, 0)], 2,
                          cutoff=0.06 + 0.05 * ((b - 112) / 12), res=4.0,
                          envmod=0.78, drive=4.2, gain=0.5), 1.0, 'acid')
s.place(s.pos(96), mcrash(28, gain=0.6), 1.0, 'fx')
s.place(s.pos(104), sweepnoise(128, gain=0.6, f0=300, f1=12000, seed=5), 1.0, 'air')
s.place(s.pos(127, 12), mdown(6, gain=0.6, f0=3000, f1=220), 1.0, 'fx')

# ================= DISSOLVE - breakdown  bars 128-151 =================
# The kick leaves for twenty-four bars. What is left is the room, and one
# chord going round the tape until it is unrecognisable.
for b in range(128, 152):
    ph = b - 128
    u = ph / 23
    if b % 2 == 0:
        stabbar(b, gain=1.0 - 0.2 * u, fb=0.70 + 0.06 * u, times=9,
                dark=0.70, drive=2.3,
                notes=STAB_VI if 8 <= ph < 16 else stab_of(b))
    if ph >= 12:
        for st in (2, 10):
            s.place(s.pos(b, sw(st)), mhat(open_=True, seed=st),
                    0.16 * (ph - 12) / 12, 'drums')
    if ph >= 16:
        perc(b, gain=0.28 * (ph - 16) / 8, clangs=True, toms=False, rims=True,
             dusty=False)
        arp(b, gain=0.30 * (ph - 16) / 8, r0=2.0, f_hi=3200)
s.place(s.pos(128), rev(mcrash(16, gain=0.85)), 1.0, 'fx')
s.place(s.pos(128), mimpact(28, tune=TUNE, gain=0.8, decay=0.9), 1.0, 'fx')
s.place(s.pos(128), hum(33, 96, gain=0.85, seed=5, cutoff=460, motor=0.42), 1.0, 'air')
s.place(s.pos(136), whisper(48, gain=0.55, v0='oo', v1='ah', note=69, seed=6), 1.0, 'air')
s.place(s.pos(144), hum(34, 64, gain=0.6, seed=7, cutoff=700, motor=0.25), 1.0, 'air')
s.place(s.pos(140), sweepnoise(160, gain=0.7, f0=260, f1=11000, seed=6, curve=2.2),
        1.0, 'air')

# ================= BUILD  bars 152-159 =================
for b in range(152, 160):
    ph = b - 152
    u = ph / 7
    floor(b, gain=0.45 + 0.55 * u, lpf=260 + 900 * ph if ph < 6 else None,
          tail=0.3 + 0.7 * u)
    tops(b, gain=0.45 + 0.5 * u, ride=ph >= 2, hats=ph >= 3, shakers=True,
         claps=(4, 12) if ph >= 4 else (), opens=(2, 10))
    perc(b, gain=0.5 + 0.5 * u, toms=ph >= 4)
    arp(b, gain=0.5 + 0.4 * u, r0=2.8 + 0.8 * u)
    if b % 2 == 0:
        stabbar(b, gain=0.95, fb=0.60, times=7, dark=0.62)
for b in (156,):
    bass(b, gain=0.8, mid=0.7)
s.place(s.pos(152), mriser(128, gain=0.55, f0=320, f1=9000, rate_steps=2.0, seed=1),
        1.0, 'fx')
s.place(s.pos(158), mriser(32, gain=0.65, f0=800, f1=13000, rate_steps=0.5, seed=2,
                           tone=0.45), 1.0, 'fx')
s.place(s.pos(159, 12), mdown(6, gain=0.5, f0=3400, f1=240), 1.0, 'fx')

# ================= THE LOCK  bars 160-207 =================
# Forty-eight bars. Nothing new arrives after 176; what changes is the sync
# ratio, the feedback and the filters.
for b in range(160, 208):
    ph = b - 160
    floor(b)
    tops(b, opens=(2, 10, 14))
    perc(b)
    arp(b, gain=1.0, r0=3.0 + 1.2 * min(ph / 32, 1.0),
        decay=0.075 - 0.02 * min(ph / 32, 1.0), f_hi=6200 + 1800 * min(ph / 32, 1.0))
    if b % 2 == 0:
        stabbar(b, gain=1.0, fb=0.56 + 0.10 * min(ph / 40, 1.0),
                times=7, dark=0.62,
                notes=STAB_II if (ph >= 16 and b % 8 >= 4) else stab_of(b))
for b in range(160, 208, 4):
    bass(b)
for b in range(176, 208, 4):
    u = (b - 176) / 28
    s.place(s.pos(b), acid(ARP_ACID, 2, cutoff=0.12 + 0.34 * u,
                           res=4.6 + 2.2 * u, envmod=0.84 + 0.12 * u,
                           drive=4.6 + 3.0 * u, gain=0.62), 1.0, 'acid')
s.place(s.pos(160), mcrash(28, gain=0.75), 1.0, 'fx')
s.place(s.pos(160), mimpact(24, tune=TUNE, gain=0.9), 1.0, 'fx')
s.place(s.pos(176), mcrash(24, gain=0.55), 1.0, 'fx')
s.place(s.pos(192), mcrash(24, gain=0.6), 1.0, 'fx')
for b in (168, 184, 200):
    s.place(s.pos(b), sweepnoise(128, gain=0.5, f0=380, f1=12000, seed=b), 1.0, 'air')

# ================= OUTRO  bars 208-239 =================
# Thirty-two bars of subtraction, mirroring the intro. The kick is last out.
for b in range(208, 240):
    ph = b - 208
    u = ph / 31
    floor(b, gain=1.0 - 0.45 * u,
          lpf=None if ph < 12 else 7000 - 300 * (ph - 12), tail=1.0 - 0.6 * u)
    tops(b, gain=0.95 - 0.75 * u, ride=ph < 20, hats=ph < 16, shakers=ph < 24,
         claps=(4, 12) if ph < 12 else (), opens=(2, 10) if ph < 18 else ())
    perc(b, gain=0.9 - 0.8 * u, clangs=ph < 22, toms=ph < 14, rims=ph < 26)
    if ph < 16:
        arp(b, gain=0.9 - 0.055 * ph, r0=3.4 - 0.08 * ph, f_hi=7000 - 300 * ph)
    if b % 2 == 0 and ph < 24:
        stabbar(b, gain=0.9 - 0.03 * ph, fb=0.58, times=7, dark=0.62)
for b in range(208, 228, 4):
    bass(b, gain=1.0 - 0.3 * ((b - 208) / 20), mid=1.0 if b < 220 else 0.5)
s.place(s.pos(216), hum(33, 96, gain=0.5, seed=8, cutoff=520, motor=0.2), 1.0, 'air')
s.place(s.pos(228), sweepnoise(96, gain=0.5, f0=9000, f1=400, seed=9, rev_=True),
        1.0, 'air')
s.place(s.pos(239, 8), rev(mcrash(12, gain=0.3)), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['music'] = bus_reverb(s.bus['music'], decay=2.6, wet=0.18, tone=4400)
s.bus['arp']   = bus_reverb(s.bus['arp'],   decay=1.5, wet=0.16, tone=5600)
s.bus['perc']  = bus_reverb(s.bus['perc'],  decay=1.2, wet=0.17, tone=6600)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.0, wet=0.30, tone=4200)
s.bus['acid']  = bus_reverb(s.bus['acid'],  decay=1.0, wet=0.14, tone=5000)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.8, wet=0.15, tone=3400)

s.bus['air']   = hp(s.bus['air'], 150)
s.bus['perc']  = hp(s.bus['perc'], 165)
s.bus['arp']   = hp(s.bus['arp'], 280)
s.bus['music'] = hp(s.bus['music'], 235)                 # the echoes stay off the bass
s.bus['mid']   = hp(s.bus['mid'], 88, order=4)
s.bus['acid']  = shelf(s.bus['acid'], 250, -2.5, kind='low')

s.bus['perc'] = squash(s.bus['perc'], thresh=0.24, ratio=3.2, attack=0.004,
                       release=0.115, mix=0.85, makeup=1.25, report='perc')
s.bus['music'] = squash(s.bus['music'], thresh=0.13, ratio=3.6, attack=0.006,
                        release=0.115, mix=0.85, makeup=1.70, report='music')
s.bus['bass'] = squash(s.bus['bass'], thresh=0.60, ratio=3.0, attack=0.006,
                       release=0.115, report='bass')
s.bus['drums'] = squash(s.bus['drums'], thresh=0.40, ratio=2.6, attack=0.016,
                        release=0.115, mix=0.55, report='drums')
s.bus['drums'] = softclip(s.bus['drums'], 1.25, knee=0.85)
s.bus['fx'] = hp(s.bus['fx'], 42)

# Four decorrelated buses - noise, reverb and a ping-pong echo - sum to an
# image wider than any record has; trim each rather than un-reverb them all.
for b, w in (('air', 0.66), ('perc', 0.74), ('arp', 0.78), ('music', 0.80)):
    s.bus[b] = narrow(s.bus[b], w)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)
for b in ('drums', 'perc', 'air', 'fx', 'arp'):
    s.bus[b] = shelf(s.bus[b], 11000, -1.5)

GAINS = {'drums': 0.86, 'sub': 0.13, 'bass': 0.11, 'mid': 2.05, 'perc': 3.10,
         'arp': 2.20, 'acid': 2.10, 'music': 3.90, 'air': 1.45, 'fx': 1.30}
s.report(GAINS)
# The sub holds through the bar, so the duck is the bass part: 0.24 s is two
# sixteenths at 131 BPM - down hard on the kick, most of the way back before
# the next one.
s.render('minimal_otrazhenie_131.wav', drive=0.60, duck=0.11, clip=1.35,
         limit=0.90, peak=0.95, fade=3.0, gains=GAINS, duck_rel=0.22)
