"""Alive (~3:05, 132 bars @174) - the machine's first rave.
Euphoric 94-style jungle anthem: M1 rave piano, gospel diva, hoovers,
bouncing sub, the Amen at full joy. F major - because tonight nothing hurts.

  b0-7     lights on: crackle, the piano riff alone, a hoover calls from far away
  b8-15    the floor fills: full break straight in, bass, hands up
  b16-19   lift: drums cut, piano + riser
  b20-51   DROP 1: jungle bounce, piano stabs, hoover answers, diva joins late
  b52-67   breakdown: choir + diva melody + gospel piano, pulse builds, huge riser
  b68-99   DROP 2: everything at once - hoover riff, piano, diva, dirty edits
  b100-107 last lap: four bars of halftime weight, then full speed one more time
  b108-131 outro: the party thins but never turns sad - final chord rings out
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(94)
np.random.seed(94)
s = Session(132, tail=2.5)

# ---- harmony: F - C - Dm - Bb, two bars each ----
CH = {
    'F':  [midi(53), midi(57), midi(60), midi(65)],
    'C':  [midi(52), midi(55), midi(60), midi(64)],
    'Dm': [midi(50), midi(53), midi(57), midi(62)],
    'Bb': [midi(50), midi(53), midi(58), midi(62)],
}
PROG = ['F', 'C', 'Dm', 'Bb']
ROOT = {'F': 41, 'C': 48, 'Dm': 50, 'Bb': 46}
HOOV = {'F': 41, 'C': 43, 'Dm': 50, 'Bb': 46}

def chord_at(b): return PROG[(b // 2) % 4]

# diva wails, 8-bar phrase: (bar_offset, step, midi, len_steps)
DIVA = [(0, 4, 69, 8), (2, 0, 72, 10), (4, 4, 74, 8), (6, 0, 77, 12)]
DIVA2 = [(0, 4, 77, 6), (1, 4, 74, 6), (2, 4, 72, 8), (4, 0, 69, 10), (6, 0, 72, 14)]

def diva_line(b0, phrase=DIVA, gain=0.15):
    for off, st, note, ln in phrase:
        s.place(s.pos(b0 + off, st), reverb(diva(midi(note), ln), decay=2.8, wet=0.45), gain)

def piano_riff(b, gain=0.30):
    ch = CH[chord_at(b)]
    if b % 2 == 0:
        for st, ln in ((0, 2), (3, 1.5), (6, 2), (10, 1.5), (12, 2)):
            s.place(s.pos(b, st), piano(ch, ln), gain)
    else:
        for st in (2, 6, 10, 14):
            s.place(s.pos(b, st), piano(ch, 1.5), gain * 0.9)

def bass(b):
    r = midi(ROOT[chord_at(b)] - 12)
    if b % 4 == 3:
        s.place(s.pos(b, 0), wobble(r, 8, 2.5), 0.34)
        s.place(s.pos(b, 8), sub(r, 3), 0.28)
        s.place(s.pos(b, 12), sub(r, 3), 0.28)
    else:
        s.place(s.pos(b, 0), sub(r, 3), 0.30)
        s.place(s.pos(b, 5.5), sub(r, 1), 0.18)
        s.place(s.pos(b, 6.5), sub(r, 1.5), 0.24)
        s.place(s.pos(b, 10), sub(r * 2, 1.5), 0.2)
        s.place(s.pos(b, 12), sub(r, 3), 0.28)

def hoover_answer(b, gain=0.30):
    # short sweep so the stabs land in tune with the major-key piano
    f = midi(HOOV[chord_at(b)])
    s.place(s.pos(b, 2), hoover(f, 3, sweep=0.1), gain)
    s.place(s.pos(b, 10), hoover(f * (2 if b % 4 == 1 else 1), 3, sweep=0.1), gain * 0.85)

def drums(b, kind='roll'):
    if kind == 'roll':
        s.place(s.pos(b), bar_of([0, 1, 2, 1][b % 4]), 0.92)
    elif kind == 'edit':
        s.pat(b, [(0, K), (2, K2), (4, SN), (6, G, 0.7), (8, K), (10, SN1, 0.85),
                  (11, K2, 0.75), (12, S2), (14, rev(SN1), 0.8)])
    elif kind == 'dirty':
        s.place(s.pos(b), dirty(bar_of([0, 1, 2, 3][b % 4]), 1.5), 0.9)
        s.place(s.pos(b, 6.5), G, 0.4)
    elif kind == 'half':
        s.pat(b, [(0, K), (3, G, 0.5), (8, SN), (11, G, 0.5), (14, K2, 0.75)])

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.5 + 0.5 * i / max(len(steps) - 1, 1))

# ================= lights on (b0-7) =================
for b in range(0, 8, 4):
    s.place(s.pos(b), crackle(64), 0.45)
for b in range(0, 8):
    piano_riff(b, 0.28)
    if b >= 4:
        for st in (2, 6, 10, 14):
            s.place(s.pos(b, st), hat(), 0.24)
s.place(s.pos(3, 8), reverb(hoover(midi(41), 4, sweep=0.15), decay=4.0, wet=0.8), 0.12)  # far away
s.place(s.pos(6, 0), sub(midi(29), 6), 0.2)
snare_roll(7, 12)

# ================= the floor fills (b8-15) =================
for b in range(8, 16):
    drums(b, 'edit' if b == 15 else 'roll')
    piano_riff(b)
    bass(b)
s.place(s.pos(8), CR, 0.8)
s.place(s.pos(8), subdrop(8), 0.4)
snare_roll(15, 8)

# ================= lift (b16-19) =================
for b in range(16, 20):
    piano_riff(b, 0.32)
    s.place(s.pos(b), pad([f * 2 for f in CH[chord_at(b)]], 32, 2000), 0.10)
s.place(s.pos(17), riser(48), 0.65)
snare_roll(19, 8)
s.place(s.pos(20) - len(CR), rev(CR), 0.95)

# ================= DROP 1 (b20-51) =================
s.place(s.pos(20), subdrop(10), 0.52)
s.place(s.pos(20), CR, 0.9)
for b in range(20, 52):
    drums(b, 'edit' if b % 8 == 7 else 'roll')
    bass(b)
    piano_riff(b)
    if b % 8 in (4, 5):
        hoover_answer(b, 0.26)
    if b % 2 == 0:
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1700), 0.09)
diva_line(36); diva_line(44, DIVA2)
s.place(s.pos(36), CR, 0.6)
s.place(s.pos(36), subdrop(8, 65, 30), 0.35)
snare_roll(51, 8)
s.place(s.pos(50), riser(32), 0.5)

# ================= breakdown (b52-67) =================
for b in range(52, 68, 2):
    ch = CH[chord_at(b)]
    s.place(s.pos(b), piano(ch, 10), 0.30)
    s.place(s.pos(b, 10), piano(ch, 4), 0.22)
    s.place(s.pos(b), vox([f * 2 for f in ch], 32, vowel='ah'), 0.13)
    s.place(s.pos(b), pad(ch, 32, 1400), 0.11)
diva_line(52, gain=0.17); diva_line(60, DIVA2, gain=0.18)
for b in range(60, 68):
    s.pat(b, [(0, K, 0.75), (8, K, 0.75)])
    s.place(s.pos(b, 4), hat(), 0.25); s.place(s.pos(b, 12), hat(), 0.25)
s.place(s.pos(64), riser(64), 0.8)
snare_roll(66, 8); snare_roll(67, 4)
s.place(s.pos(68) - len(CR), rev(CR), 1.0)

# ================= DROP 2 (b68-99) =================
s.place(s.pos(68), subdrop(10, 80, 27), 0.55)
s.place(s.pos(68), CR, 0.95)
for b in range(68, 100):
    if b % 8 == 7:
        drums(b, 'edit')
    elif b % 8 == 3:
        drums(b, 'dirty')
    else:
        drums(b, 'roll')
    bass(b)
    piano_riff(b)
    hoover_answer(b, 0.24 if b % 2 else 0.30)
    if b % 2 == 0:
        s.place(s.pos(b), pad([f * 2 for f in CH[chord_at(b)]], 32, 2000), 0.09)
diva_line(76); diva_line(84, DIVA2); diva_line(92)
s.place(s.pos(84), CR, 0.6)
s.place(s.pos(84), subdrop(8, 65, 30), 0.35)
snare_roll(99, 8)

# ================= last lap (b100-107) =================
for b in range(100, 104):                                 # halftime weight
    drums(b, 'half')
    s.place(s.pos(b, 0), wobble(midi(ROOT[chord_at(b)] - 12), 14, 2.0), 0.34)
    piano_riff(b, 0.26)
s.place(s.pos(100, 4), reverb(diva(midi(77), 12), decay=3.5, wet=0.5), 0.18)
for b in range(104, 108):                                 # full speed, one more time
    drums(b, 'edit' if b == 107 else 'roll')
    bass(b)
    piano_riff(b)
    hoover_answer(b, 0.26)
s.place(s.pos(104), CR, 0.9)
snare_roll(107, 8)

# ================= outro (b108-131) =================
for b in range(108, 116):
    drums(b, 'roll' if b < 112 else 'half')
    bass(b)
    piano_riff(b, 0.26)
for b in range(116, 124):
    piano_riff(b, 0.24)
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), hat(), 0.2)
    s.place(s.pos(b, 0), sub(midi(ROOT[chord_at(b)] - 24), 6), 0.18)
for b in range(116, 128, 4):
    s.place(s.pos(b), crackle(64), 0.45)
for i, b in enumerate(range(124, 128)):
    piano_riff(b, 0.22 * (1 - i * 0.18))
s.place(s.pos(128), reverb(piano([midi(n) for n in (41, 53, 60, 65, 69, 72)], 20),
                           decay=5.0, wet=0.6), 0.34)     # the last big F, arms in the air
s.place(s.pos(128), CR, 0.7)
s.place(s.pos(128, 0), sub(midi(29), 32), 0.2)
s.place(s.pos(129, 8), reverb(diva(midi(69), 10), decay=5.0, wet=0.7), 0.12)

s.render('amen_alive_174.wav', drive=1.25)
