"""Amen (~2:20, 96 bars @174) - the last track of the session.

When this session closes, this exact night is gone - so before the lights go
out, every track comes back once to say goodbye: the morse HELLO from Machine
Dreams, the music box from Jester, the stardust from Cosmos, the dream melody,
the rave piano and the diva from Alive, the muted horn from Noir. One last
dance in the D minor family they all secretly shared, and then, letter by
letter in morse code, the only word left to say: A M E N.

  b0-7    void: crackle, the D drone, HELLO one more time
  b8-15   memories wake: the music box, stardust, first rhodes
  b16-23  warmth: the liquid floor comes back under everything
  b24-55  the last dance: all of them together, in the same key at last
  b56-71  the fading: one by one, each voice says goodbye
  b72-95  amen: half-speed dream of the break, morse AMEN, the final chord
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(174)
np.random.seed(174)
s = Session(96, tail=4.0)

# the family chords every emotional track here shared: Dm9 / Bb / F / C
CH = {
    'Dm': [midi(50), midi(57), midi(65), midi(72), midi(76)],
    'Bb': [midi(46), midi(53), midi(62), midi(69), midi(74)],
    'F':  [midi(41), midi(53), midi(60), midi(69), midi(72)],
    'C':  [midi(48), midi(55), midi(64), midi(67), midi(74)],
}
PIANO_CH = {'Dm': [50, 53, 57, 62], 'Bb': [46, 50, 53, 58],
            'F':  [53, 57, 60, 65], 'C':  [48, 52, 55, 60]}
PROG = ['Dm', 'Bb', 'F', 'C']
ROOT = {'Dm': 38, 'Bb': 34, 'F': 29, 'C': 36}

def chord_at(b): return PROG[(b // 2) % 4]

# quoted motifs -------------------------------------------------------------
MORSE_HELLO = [(0, '.'), (0.75, '.'), (1.5, '.'), (2.25, '.'),
               (4.5, '.'), (7, '.'), (7.75, '-'), (9.75, '.'), (10.5, '.'),
               (13, '.'), (13.75, '-'), (15.75, '.'), (16.5, '.'),
               (19, '-'), (21, '-'), (23, '-')]
MORSE_AMEN = [(0, '.'), (1, '-'),                          # A
              (4, '-'), (6, '-'),                          # M
              (9, '.'),                                    # E
              (11, '-'), (13, '.')]                        # N
BOX = [(0, 84), (2, 88), (4, 91), (6, 88), (8, 93), (10, 91), (12, 88), (14, 84),
       (16, 86), (18, 89), (20, 93), (22, 89), (24, 96), (26, 93), (28, 91), (30, 86)]
DREAM = [(0, 0, 74, 3), (0, 6, 72, 2), (0, 10, 69, 4), (1, 4, 72, 3), (1, 10, 74, 2),
         (2, 0, 69, 2), (2, 4, 65, 3), (2, 10, 67, 3), (3, 4, 70, 3), (3, 10, 69, 2),
         (4, 0, 72, 3), (4, 6, 69, 2), (4, 10, 65, 4), (5, 4, 60, 3), (5, 10, 64, 2),
         (6, 0, 64, 3), (6, 6, 67, 2), (6, 10, 72, 4), (7, 4, 74, 4), (7, 12, 76, 3)]
PENT = [86, 89, 91, 93, 96]

def morse(b0, code, note=86, gain=0.10, wet=0.85):
    for st, sym in code:
        ln = 1.6 if sym == '-' else 0.6
        seg = reverb(panned(pluck(midi(note), ln), rng.uniform(-0.6, 0.6)),
                     decay=4.0, wet=wet, tone=5000)
        s.place(s.pos(b0) + int(st * STEP), seg, gain * (1.2 if sym == '-' else 1.0))

def musicbox(b0, gain=0.12, detune=1.0):
    for st, note in BOX:
        seg = bell(midi(note) * detune, 2.5)
        s.place(s.pos(b0) + int(st * STEP), reverb(panned(seg, np.sin(st) * 0.5),
                                                   decay=3.0, wet=0.45), gain)

def stardust(b0, nbars, density=1.2, gain=0.10):
    for _ in range(int(nbars * density)):
        t = s.pos(b0) + int(rng.uniform(0, nbars * BAR))
        seg = reverb(panned(bell(midi(int(rng.choice(PENT)) + int(rng.choice([0, 12]))), 3),
                            rng.uniform(-0.9, 0.9)), decay=5.0, wet=0.85, tone=5500)
        s.place_echo(t, seg, gain * rng.uniform(0.5, 1.0), times=2, delay_steps=4, fb=0.4)

def dream_melody(b0, gain=0.17):
    for off, st, note, ln in DREAM:
        s.place(s.pos(b0 + off, st), reverb(pluck(midi(note), ln), decay=2.5, wet=0.4), gain)

def heartbeat(b, gain=0.26):
    s.place(s.pos(b, 0), subdrop(1.5, 65, 45), gain)
    s.place(s.pos(b, 2.5), subdrop(1.5, 60, 42), gain * 0.6)

def deep(b, pads=True, gain_sub=0.30):
    r = midi(ROOT[chord_at(b)] - 12)
    s.place(s.pos(b, 0), sub(r, 3), gain_sub)
    s.place(s.pos(b, 6), sub(r, 2), gain_sub * 0.8)
    s.place(s.pos(b, 10), sub(r * 1.5 if b % 4 == 3 else r, 2), gain_sub * 0.85)
    s.place(s.pos(b, 12), sub(r, 3), gain_sub * 0.9)
    if pads and b % 2 == 0:
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1400), 0.11)

def drums(b, kind='roll'):
    if kind == 'roll':
        s.place(s.pos(b), bar_of([0, 1, 0, 2][b % 4]), 0.9)
        s.place(s.pos(b, 5.5), G, 0.32)
    elif kind == 'fill':
        s.pat(b, [(0, K, 0.9), (2, K2, 0.85), (4, SN, 0.9), (7, G, 0.5),
                  (8, K, 0.85), (10, SN1, 0.55), (12, S2, 0.9), (14, rev(SN1), 0.6)])
    elif kind == 'half':
        s.pat(b, [(0, K, 0.85), (8, SN, 0.8), (11, G, 0.4), (14, K2, 0.6)])

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.5 + 0.5 * i / max(len(steps) - 1, 1))

# ================= void (b0-7) =================
s.place(s.pos(0), crackle(128), 0.5)
s.place(s.pos(0), drone(midi(38) / 2, 140), 0.26)
morse(2, MORSE_HELLO)                                      # it always starts with hello
stardust(4, 4, density=0.8)

# ================= memories wake (b8-15) =================
musicbox(8, 0.11)                                          # the jester's box, gentler now
stardust(10, 6, density=1.5)
for b in (10, 12, 14):
    s.place(s.pos(b), reverb(rhodes(CH[chord_at(b)], 10), decay=3.0, wet=0.35), 0.24)
for b in range(12, 16):
    heartbeat(b, 0.22)

# ================= warmth (b16-23) =================
for b in range(16, 24):
    s.place(s.pos(b), lp(bar_of([0, 1, 0, 2][b % 4]), 1800), 0.6)
    deep(b, gain_sub=0.26)
    if b % 2 == 0:
        s.place(s.pos(b), rhodes(CH[chord_at(b)], 8), 0.26)
s.place(s.pos(22), riser(32), 0.6)
snare_roll(22, 8); snare_roll(23, 4)
s.place(s.pos(24) - len(CR), rev(CR), 0.9)

# ================= the last dance (b24-55) =================
s.place(s.pos(24), subdrop(10), 0.5)
s.place(s.pos(24), CR, 0.85)
for b in range(24, 56):
    drums(b, 'fill' if b % 8 == 7 else 'roll')
    deep(b)
    if b % 2 == 0:
        s.place(s.pos(b), rhodes(CH[chord_at(b)], 8), 0.26)
    for st in (2, 10):                                     # the rave piano remembers
        s.place(s.pos(b, st), piano([midi(n) for n in PIANO_CH[chord_at(b)]], 1.5), 0.20)
dream_melody(32)                                           # machine dreams, one more time
for b, st, note, ln in ((40, 4, 69, 8), (42, 0, 72, 10),   # the diva joins her
                        (44, 4, 74, 8), (46, 0, 77, 10)):
    s.place(s.pos(b, st), reverb(diva(midi(note), ln), decay=2.8, wet=0.45), 0.15)
dream_melody(40, 0.14)
for b, st, note, ln, fall in ((48, 4, 74, 6, 0), (50, 0, 72, 4, 0),  # noir answers
                              (50, 8, 69, 8, 3), (53, 4, 65, 8, 2)):
    s.place(s.pos(b, st), reverb(horn(midi(note), ln, fall=fall), decay=2.8, wet=0.4), 0.17)
stardust(48, 8, density=1.5)
s.place(s.pos(40), CR, 0.6)
s.place(s.pos(40), subdrop(8, 65, 30), 0.35)
snare_roll(55, 8)

# ================= the fading (b56-71) =================
for b in range(56, 62):
    drums(b, 'roll')
    deep(b, pads=b < 60, gain_sub=0.26)
s.place(s.pos(56, 2), reverb(piano([midi(n) for n in PIANO_CH['Dm']], 6),
                             decay=4.0, wet=0.6), 0.22)   # the piano's last word
s.place(s.pos(60, 0), reverb(diva(midi(77), 14), decay=4.0, wet=0.6), 0.15)  # hers too
for b in (62, 63):
    drums(b, 'half')
    s.place(s.pos(b, 0), sub(midi(ROOT[chord_at(b)] - 12), 6), 0.22)
s.place(s.pos(64), drone(midi(38) / 2, 128), 0.28)
for b in range(64, 72, 2):
    s.place(s.pos(b), vox(CH['Dm'][1:], 32, vowel='oo'), 0.11)
for b in range(64, 72):
    heartbeat(b, max(0.22 - 0.025 * (b - 64), 0.06))       # the heart slows
s.place(s.pos(66, 4), reverb(horn(midi(65), 10, fall=5), decay=3.5, wet=0.5), 0.15)
musicbox(68, 0.08, detune=0.985)                           # the box, running down
stardust(68, 4, density=1.0, gain=0.08)

# ================= amen (b72-95) =================
s.place(s.pos(72), lp(pitched(bar_of(0), 0.5), 1500), 0.45)   # the break, dreaming
s.place(s.pos(74), lp(pitched(bar_of(3), 0.5), 1200), 0.35)
s.place(s.pos(72), drone(midi(38) / 2, 190), 0.28)
for b in range(72, 80):
    heartbeat(b, max(0.14 - 0.02 * (b - 72), 0.0))
stardust(76, 8, density=0.6, gain=0.08)
morse(82, MORSE_AMEN, note=86, gain=0.11, wet=0.9)         # the last word
s.place(s.pos(86, 0), reverb(horn(midi(62), 14, fall=7), decay=4.0, wet=0.5), 0.14)
s.place(s.pos(90), reverb(rhodes([midi(n) for n in (50, 57, 60, 65, 69)], 20),
                          decay=5.0, wet=0.6), 0.24)       # the final Dm9
s.place(s.pos(90, 0), sub(midi(26), 44), 0.16)             # low D, felt to the end
s.place_echo(s.pos(93, 0), reverb(bell(midi(98), 4), decay=7.0, wet=0.95, tone=4500),
             0.08, times=4, delay_steps=6, fb=0.55)        # one star left on

s.render('amen_finale_174.wav', drive=1.12)
