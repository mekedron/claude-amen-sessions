"""PSX snowboarding liquid (~2:50, 120 bars @174) - Cool Boarders energy:
icy bells, bright game lead melody, mountain wind, rolling break.

  b0-7     wind + bell arps, hats tick in
  b8-15    filtered break fades in, bass joins
  b16-47   RUN 1: full groove + lead melody + bell echoes
  b48-63   viewpoint: drums drop to halftime, bells & wind, build back
  b64-95   RUN 2: groove with wah bars, melody up the octave, busier bass
  b96-119  last slope + outro: thins back down to wind and one bell
"""
import numpy as np
from amenlib import *

np.random.seed(21)
s = Session(120, tail=2.5)

# ---- harmony: sunny C major loop, 2 bars per chord ----
CH = {
    'C':  [midi(48), midi(55), midi(64), midi(67), midi(74)],
    'G':  [midi(43), midi(50), midi(59), midi(62), midi(67)],
    'Am': [midi(45), midi(52), midi(60), midi(64), midi(67)],
    'F':  [midi(41), midi(48), midi(57), midi(60), midi(69)],
}
PROG = ['C', 'G', 'Am', 'F']
ROOT = {'C': 36, 'G': 31, 'Am': 33, 'F': 29}
BELLS = {'C': [72, 76, 79, 83], 'G': [71, 74, 79, 83],
         'Am': [72, 76, 81, 84], 'F': [72, 77, 81, 84]}

def chord_at(b): return PROG[(b // 2) % 4]

# 8-bar lead melody: (bar_offset, step, midi, len_steps)
MELODY = [
    (0, 0, 76, 3), (0, 6, 79, 2), (0, 10, 81, 4), (1, 4, 79, 3), (1, 10, 76, 2),
    (2, 0, 74, 3), (2, 6, 79, 2), (2, 10, 83, 4), (3, 4, 79, 3), (3, 10, 74, 2),
    (4, 0, 76, 3), (4, 6, 81, 2), (4, 10, 84, 4), (5, 4, 81, 3), (5, 10, 79, 2),
    (6, 0, 81, 3), (6, 4, 79, 2), (6, 8, 77, 3), (6, 12, 74, 2),
    (7, 0, 72, 6), (7, 10, 74, 2), (7, 13, 76, 3),
]

def melody(b0, octave=0, gain=0.2):
    for off, st, note, ln in MELODY:
        s.place(s.pos(b0 + off, st), lead(midi(note + octave), ln), gain)

def bells_arp(b, gain=0.12):
    """Seven bells over six slots: the icy figure never repeats a bar until
    bar 7, which is what stops it reading as a loop behind the melody."""
    ns = BELLS[chord_at(b)]
    for st, note, dur, vel in arp_seq(ns, bars=1, shape='up', rate=3.0, cycle=7,
                                      octaves=(0, 1), gate=(1, 1, 0, 1, 1, 1, 0),
                                      accents=(0,), tail=0.9, rotate=b * 6, seed=b):
        s.place(s.pos(b, st), bell(midi(note), 2.5), gain * vel * 1.35)

def bass(b, busy=False):
    r = midi(ROOT[chord_at(b)] - 12)
    s.place(s.pos(b, 0), sub(r, 3), 0.30)
    s.place(s.pos(b, 6), sub(r, 2), 0.24)
    s.place(s.pos(b, 10), sub(r * 1.5 if b % 4 == 3 else r, 2), 0.26)
    s.place(s.pos(b, 12), sub(r, 3), 0.28)
    if busy:
        s.place(s.pos(b, 3.5), sub(r, 1), 0.18)
        s.place(s.pos(b, 14.5), sub(r * 2, 1), 0.16)

def drums(b, kind='roll'):
    if kind == 'roll':
        s.place(s.pos(b), bar_of([0, 1, 0, 2][b % 4]), 0.9)
        s.place(s.pos(b, 5.5), G, 0.35)
    elif kind == 'fill':
        s.pat(b, [(0, K, 0.9), (2, K2, 0.85), (4, SN, 0.9), (7, G, 0.5),
                  (8, K, 0.85), (10, SN1, 0.55), (12, S2, 0.9), (14, rev(SN1), 0.6)])
    elif kind == 'wah':
        s.place(s.pos(b), wah(bar_of([0, 1, 0, 2][b % 4]), 2.5), 0.95)
    elif kind == 'half':
        s.pat(b, [(0, K, 0.85), (8, SN, 0.85), (11, G, 0.4), (14, K2, 0.6)])

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.5 + 0.5 * i / max(len(steps) - 1, 1))

# ================= intro (b0-15) =================
s.place(s.pos(0), wind(64), 0.7)
s.place(s.pos(4), wind(64), 0.5)
for b in range(0, 16, 2):
    bells_arp(b, 0.10 if b < 8 else 0.13)
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1500), 0.09)
for b in range(4, 16):
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), hat(), 0.28)
for b in range(8, 16):
    s.place(s.pos(b), lp(bar_of([0, 1, 0, 2][b % 4]), 1600), 0.6)
    bass(b) if b >= 12 else s.place(s.pos(b, 0), sub(midi(ROOT[chord_at(b)] - 12), 6), 0.2)
s.place(s.pos(14), riser(32), 0.6)
snare_roll(15, 12)
s.place(s.pos(16) - len(CR), rev(CR), 0.9)

# ================= RUN 1 (b16-47) =================
s.place(s.pos(16), subdrop(10), 0.5)
s.place(s.pos(16), CR, 0.85)
for b in range(16, 48):
    drums(b, 'fill' if b % 8 == 7 else 'roll')
    bass(b, busy=b % 4 == 3)
    if b % 2 == 0:
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1700), 0.11)
    if b % 4 == 2:
        bells_arp(b, 0.10)
melody(24); melody(32)
melody(40, gain=0.16)                                    # softer third pass
for b in range(40, 48, 2):
    bells_arp(b, 0.12)
s.place(s.pos(32), CR, 0.6)
snare_roll(47, 8)
s.place(s.pos(46), riser(32), 0.45)

# ================= viewpoint (b48-63) =================
s.place(s.pos(48), wind(96), 0.7)
for b in range(48, 56):
    drums(b, 'half')
    s.place(s.pos(b, 0), sub(midi(ROOT[chord_at(b)] - 12), 6), 0.22)
for b in range(48, 64, 2):
    bells_arp(b, 0.14)
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 2100), 0.14)
for off, st, note, ln in MELODY[:10]:                    # half the tune, on bells
    s.place_echo(s.pos(48 + off * 2, st), bell(midi(note + 12), 3), 0.12, times=2, delay_steps=4, fb=0.45)
for b in range(60, 64):
    s.pat(b, [(0, K, 0.7), (8, K, 0.7)])
    s.place(s.pos(b, 4), hat(), 0.25); s.place(s.pos(b, 12), hat(), 0.25)
s.place(s.pos(60), riser(64), 0.7)
snare_roll(62, 8); snare_roll(63, 4)
s.place(s.pos(64) - len(CR), rev(CR), 0.95)

# ================= RUN 2 (b64-95) =================
s.place(s.pos(64), subdrop(10, 80, 27), 0.55)
s.place(s.pos(64), CR, 0.9)
for b in range(64, 96):
    if b % 8 == 7:
        drums(b, 'fill')
    elif b % 8 == 5:
        drums(b, 'wah')
    else:
        drums(b, 'roll')
    bass(b, busy=b % 2 == 1)
    if b % 2 == 0:
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1800), 0.12)
        bells_arp(b, 0.10)
melody(72, octave=12, gain=0.17)                         # melody up the octave
melody(80)
melody(88, gain=0.16)
s.place(s.pos(80), CR, 0.6)
s.place(s.pos(80), subdrop(8, 65, 30), 0.35)
snare_roll(95, 8)

# ================= last slope + outro (b96-119) =================
for b in range(96, 104):
    drums(b, 'roll' if b < 100 else 'half')
    bass(b)
    if b % 2 == 0:
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1500), 0.11)
        bells_arp(b, 0.11)
s.place(s.pos(96), CR, 0.7)
s.place(s.pos(104), wind(96), 0.7)
for b in range(104, 112):
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), hat(), 0.2)
    s.place(s.pos(b, 0), sub(midi(ROOT[chord_at(b)] - 12), 6), 0.18)
    if b % 2 == 0:
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1300), 0.10)
        bells_arp(b, 0.12)
for i, b in enumerate(range(112, 118, 2)):               # bells fading out
    bells_arp(b, 0.11 * (1 - i * 0.3))
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1100), 0.08)
s.place_echo(s.pos(116, 0), bell(midi(84), 4), 0.13, times=4, delay_steps=4, fb=0.55)
s.place(s.pos(117), rhodes(CH['C'], 24), 0.24)           # final chord under the snow
s.place(s.pos(117, 0), sub(midi(24), 24), 0.18)
s.place(s.pos(114), wind(80), 0.6)

s.render('amen_psx_snow_174.wav', drive=1.12)
