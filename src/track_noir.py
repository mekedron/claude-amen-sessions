"""Noir (~2:50, 120 bars @174) - jazz club at three in the morning:
walking upright bass, rootless rhodes comps, a harmon-muted trumpet dropping
phrases with fall-offs, and the Amen playing brushes. D minor, ii-V colors.

  b0-7     the room: rain-crackle, walking bass alone with brushed hats
  b8-15    the break slips in under a lowpass, first horn phrase
  b16-19   lift + roll
  b20-51   set one: full break, walking bass, comps, horn call-and-response
  b52-67   3 a.m.: halftime, the horn talks longer, everything smoky
  b68-95   set two: busier walk, horn up the register, faint strings
  b96-119  closing time: the band packs up one by one, last fall-off, door
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(33)
np.random.seed(33)
s = Session(120, tail=3.0)

# 8-bar harmony: Dm9 / Gm9 / Bbmaj9 / A7b9, two bars each (rootless comp
# voicings chosen so each chord moves to the next by step)
COMP = {
    'Dm9': [53, 57, 60, 64], 'Gm9': [53, 58, 62, 65],
    'Bb':  [50, 53, 57, 60], 'A7':  [49, 53, 55, 58],
}
PROG = ['Dm9', 'Gm9', 'Bb', 'A7']
# walking lines: 8 quarters per chord (two bars) - singable arches, root on
# the downbeat, all diatonic (C# only on A7), each line steps into the next root
WALK = {
    'Dm9': [38, 41, 45, 48, 50, 48, 45, 41],   # D F A C D' C A F -> up to G
    'Gm9': [43, 46, 50, 53, 55, 53, 50, 46],   # G Bb D F G' F D Bb -> Bb root
    'Bb':  [46, 50, 53, 58, 55, 53, 50, 46],   # Bb D F Bb' G F D Bb -> semitone to A
    'A7':  [45, 49, 52, 55, 52, 49, 40, 37],   # A C# E G E C# E, C# leads home to D
}

def chord_at(b): return PROG[(b // 2) % 4]

WALKING_BASS = False                                       # the upright is on a break

def walk(b, busy=False, gain=0.34):
    if not WALKING_BASS:
        return
    line = WALK[chord_at(b)]
    quarter = line[(b % 2) * 4:(b % 2) * 4 + 4]
    for i, note in enumerate(quarter):
        s.place(s.pos(b, i * 4), upright(midi(note), 3.5), gain)
        if busy and rng.random() < 0.4:                    # swung ghost 8th
            s.place(s.pos(b, i * 4 + 2.6), upright(midi(note), 1.2), gain * 0.4)

def deep(b, pads=True, gain_sub=0.30):
    """the liquid warmth: rolling sub on the chord root + a pad carpet"""
    r = midi(WALK[chord_at(b)][0] - 12)
    s.place(s.pos(b, 0), sub(r, 3), gain_sub)
    s.place(s.pos(b, 6), sub(r, 2), gain_sub * 0.8)
    s.place(s.pos(b, 10), sub(r * 1.5 if b % 4 == 3 else r, 2), gain_sub * 0.85)
    s.place(s.pos(b, 12), sub(r, 3), gain_sub * 0.9)
    if pads and b % 2 == 0:
        s.place(s.pos(b), pad([midi(n) for n in COMP[chord_at(b)]] + [r * 2], 32, 1200), 0.12)

def comps(b, gain=0.22):
    ch = [midi(n) for n in COMP[chord_at(b)]]
    for st in ((3.5, 11) if b % 2 == 0 else (5.5, 12.5)):
        s.place(s.pos(b, st), reverb(rhodes(ch, 3), decay=2.0, wet=0.3), gain)

def brushes(b, kind='full'):
    if kind == 'full':
        s.place(s.pos(b), bar_of([0, 1, 0, 2][b % 4]), 0.85)
        s.place(s.pos(b, 5.6), G, 0.3); s.place(s.pos(b, 13.6), G, 0.28)
    elif kind == 'soft':
        s.place(s.pos(b), lp(bar_of([0, 1, 0, 2][b % 4]), 2500), 0.65)
        s.place(s.pos(b, 5.6), G, 0.25)
    elif kind == 'half':
        s.pat(b, [(0, K, 0.8), (8, SN, 0.75), (11, G, 0.4), (13.6, G, 0.3)])
    elif kind == 'ticks':
        for st in (2, 6, 10, 13.6):
            s.place(s.pos(b, st), hat(), 0.2)

def phrase(events, gain=0.20):
    """horn phrases: (bar, step, midi, len, fall_semitones)"""
    for b, st, note, ln, fall in events:
        s.place(s.pos(b, st), reverb(horn(midi(note), ln, fall=fall),
                                     decay=2.8, wet=0.4), gain)

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.45 + 0.5 * i / max(len(steps) - 1, 1))

# ================= the room (b0-7) =================
s.place(s.pos(0), crackle(128), 0.5)
for b in range(0, 8):
    walk(b)
    brushes(b, 'ticks')
    if b >= 4 or not WALKING_BASS:
        comps(b, 0.18)
if not WALKING_BASS:                                       # sub roots hold the floor
    for b in range(2, 8, 2):
        s.place(s.pos(b, 0), sub(midi(WALK[chord_at(b)][0] - 12), 6), 0.2)

# ================= the break slips in (b8-15) =================
for b in range(8, 16):
    brushes(b, 'soft')
    walk(b)
    comps(b)
    deep(b, gain_sub=0.24)
phrase([(9, 4, 69, 6, 2), (11, 0, 72, 4, 0), (11, 8, 69, 6, 3),
        (13, 4, 65, 8, 0), (14, 12, 62, 6, 2)])
snare_roll(15, 12)

# ================= lift (b16-19) =================
for b in (16, 17, 18):
    walk(b, busy=True)
    comps(b)
    brushes(b, 'ticks')
s.place(s.pos(18), riser(32), 0.4)
snare_roll(19, 8)
s.place(s.pos(20) - len(CR), rev(CR), 0.8)

# ================= set one (b20-51) =================
s.place(s.pos(20), subdrop(8), 0.4)
s.place(s.pos(20), CR, 0.7)
for b in range(20, 52):
    brushes(b, 'full')
    walk(b, busy=b % 4 == 3)
    comps(b)
    deep(b)
phrase([(24, 4, 69, 6, 2), (26, 0, 72, 4, 0), (26, 8, 74, 6, 3),
        (28, 4, 65, 6, 0), (30, 0, 67, 4, 0), (30, 8, 62, 8, 2)])
phrase([(36, 4, 72, 4, 0), (37, 4, 74, 4, 0), (38, 4, 77, 6, 0),
        (40, 0, 74, 4, 2), (42, 4, 69, 10, 3)])
for b, st in ((33, 8), (41, 8), (45, 4)):                  # pluck echoes answer
    s.place_echo(s.pos(b, st), pluck(midi(81), 2), 0.10, times=3, delay_steps=3, fb=0.5)
phrase([(46, 4, 65, 6, 0), (48, 0, 64, 4, 0), (48, 10, 62, 10, 4)])
s.place(s.pos(36), CR, 0.5)
snare_roll(51, 8)

# ================= 3 a.m. (b52-67) =================
s.place(s.pos(52), crackle(128), 0.5)
for b in range(52, 68):
    brushes(b, 'half')
    walk(b)
    deep(b, pads=False, gain_sub=0.26)
    if b % 2 == 0:
        comps(b, 0.19)
        s.place(s.pos(b), pad([midi(n) for n in COMP[chord_at(b)]], 32, 900), 0.11)
phrase([(53, 4, 62, 10, 0), (56, 0, 65, 8, 2), (58, 8, 67, 6, 0),
        (60, 0, 69, 12, 0), (63, 8, 65, 4, 0), (64, 4, 62, 12, 5)], gain=0.22)
for b in range(64, 68):
    s.place(s.pos(b, 4), hat(), 0.22); s.place(s.pos(b, 12), hat(), 0.22)
s.place(s.pos(66), riser(32), 0.45)
snare_roll(67, 8)
s.place(s.pos(68) - len(CR), rev(CR), 0.85)

# ================= set two (b68-95) =================
s.place(s.pos(68), subdrop(8, 70, 30), 0.42)
s.place(s.pos(68), CR, 0.75)
for b in range(68, 96):
    brushes(b, 'full')
    walk(b, busy=b % 2 == 1)
    comps(b)
    deep(b)
    if b % 2 == 0 and b >= 80:
        s.place(s.pos(b), strings([midi(n + 12) for n in COMP[chord_at(b)][:3]], 32), 0.07)
phrase([(72, 4, 74, 6, 0), (74, 0, 77, 4, 0), (74, 8, 76, 6, 2),
        (76, 4, 72, 8, 0), (79, 0, 74, 4, 0), (80, 4, 81, 10, 3)])
phrase([(84, 4, 77, 6, 0), (86, 0, 74, 6, 0), (88, 4, 72, 6, 2),
        (90, 0, 69, 4, 0), (91, 4, 67, 12, 4)])
s.place(s.pos(84), CR, 0.5)
snare_roll(95, 8)

# ================= closing time (b96-119) =================
for b in range(96, 104):
    brushes(b, 'soft' if b >= 100 else 'full')
    walk(b)
    comps(b, 0.19)
    deep(b, gain_sub=0.26)
for b in range(104, 112):
    brushes(b, 'ticks')
    walk(b)
    deep(b, pads=b < 108, gain_sub=0.20)
    if b % 2 == 0:
        comps(b, 0.16)
phrase([(105, 4, 69, 8, 0), (108, 0, 65, 6, 0), (109, 8, 62, 12, 5)], gain=0.19)
s.place(s.pos(110), crackle(96), 0.5)
for b in range(112, 118):
    walk(b, gain=0.30 - 0.03 * (b - 112))                  # the bass packs up last
if not WALKING_BASS:                                       # rhodes closes the room instead
    for i, b in enumerate(range(112, 118, 2)):
        s.place(s.pos(b), reverb(rhodes([midi(n) for n in COMP[chord_at(b)]], 10),
                                 decay=3.0, wet=0.4), 0.20 * (1 - i * 0.25))
        s.place(s.pos(b, 0), sub(midi(WALK[chord_at(b)][0] - 12), 8), 0.16 * (1 - i * 0.25))
s.place(s.pos(116), reverb(rhodes([midi(n) for n in (50, 57, 60, 65, 69)], 14),
                           decay=4.0, wet=0.5), 0.22)      # last Dm9 rings
phrase([(114, 4, 62, 10, 7)], gain=0.16)                   # the longest fall-off
s.place(s.pos(118, 4), K, 0.5)                             # the door
s.place(s.pos(118, 4), sub(midi(26), 12), 0.16)

s.render('amen_noir_174.wav', drive=1.15)
