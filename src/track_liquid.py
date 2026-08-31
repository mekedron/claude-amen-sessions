"""Full-length liquid DnB track (~3 min, 128 bars @174).

Arrangement:
  b0-15    intro: vinyl crackle, rhodes, pad; filtered break sneaks in at b8
  b16-23   build 1: dry break, bass teases, riser + snare roll
  b24-55   drop 1: sub-drop boom, full groove; arp sparkle joins at b40
  b56-71   breakdown: drums out, chords drift (Dm9/Em7), pluck melody w/ echo
  b72-103  drop 2: bigger - wah'd break bars, busier bass, arp on
  b104-127 outro: elements peel away back to crackle + last chord
"""
import numpy as np
from amenlib import *

np.random.seed(11)
s = Session(128, tail=2.5)

# ---- harmony ----
CH = {
    'Am9':   [midi(45), midi(55), midi(60), midi(64), midi(71)],
    'Fmaj9': [midi(41), midi(52), midi(57), midi(60), midi(67)],
    'Cadd9': [midi(48), midi(55), midi(62), midi(64)],
    'G7':    [midi(43), midi(53), midi(59), midi(62)],
    'Dm9':   [midi(50), midi(60), midi(64), midi(65), midi(69)],
    'Em7':   [midi(52), midi(62), midi(67), midi(71)],
}
PROG  = ['Am9', 'Fmaj9', 'Cadd9', 'G7']          # 2 bars each -> 8-bar loop
ROOTS = {'Am9': 33, 'Fmaj9': 29, 'Cadd9': 36, 'G7': 31, 'Dm9': 26, 'Em7': 28}
ARPN  = {'Am9': [69, 72, 76, 79], 'Fmaj9': [69, 72, 77, 81],
         'Cadd9': [67, 72, 74, 79], 'G7': [67, 71, 74, 77]}

def chord_at(b): return PROG[(b // 2) % 4]

# ---- part writers ----
def keys(b, full=True):
    ch = CH[chord_at(b)]
    s.place(s.pos(b, 0), rhodes(ch, 8), 0.30)
    if full:
        s.place(s.pos(b, 10.5), rhodes(ch, 4), 0.22)

def bass(b, busy=False):
    r = midi(ROOTS[chord_at(b)] - 12)
    s.place(s.pos(b, 0), sub(r, 3), 0.30)
    s.place(s.pos(b, 6), sub(r, 2), 0.24)
    s.place(s.pos(b, 10), sub(r * 1.5 if b % 4 == 3 else r, 2), 0.26)
    s.place(s.pos(b, 12), sub(r, 3), 0.28)
    if busy:
        s.place(s.pos(b, 3.5), sub(r, 1), 0.18)
        s.place(s.pos(b, 14.5), sub(r * 2, 1), 0.16)

def arp(b):
    """Five notes over eight 8th-note slots, so the figure starts somewhere
    new every bar and only comes home on bar 5. Same pluck, same chord tones -
    a four-note cycle just divided the bar exactly and landed identically
    every time."""
    notes = ARPN[chord_at(b)]
    for st, note, dur, vel in arp_seq(notes, bars=1, shape='updown', rate=2.0,
                                      cycle=5, octaves=(0, 1), gate=(1, 1, 1, 0, 1),
                                      accents=(0,), tail=0.8, rotate=b * 8, seed=b):
        s.place(s.pos(b, st), pluck(midi(note), max(dur, 1.2)), 0.13 * vel)

def drums(b, kind='roll'):
    if kind == 'roll':
        s.place(s.pos(b), bar_of([0, 1, 0, 2][b % 4]), 0.9)
        s.place(s.pos(b, 5.5), G, 0.35)
    elif kind == 'fill':
        s.pat(b, [(0, K, 0.9), (2, K2, 0.85), (4, SN, 0.9), (7, G, 0.5),
                  (8, K, 0.85), (10, SN1, 0.55), (12, S2, 0.9), (14, rev(SN1), 0.6)])
    elif kind == 'wah':
        s.place(s.pos(b), wah(bar_of([0, 1, 0, 2][b % 4]), 2.0), 0.95)
    elif kind == 'thin':
        s.pat(b, [(0, K, 0.85), (4, SN, 0.8), (8, K2, 0.7), (12, S2, 0.8)])

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.5 + 0.5 * i / max(len(steps) - 1, 1))

# ================= intro (b0-15) =================
for b in range(0, 16, 4):
    s.place(s.pos(b), crackle(64), 0.5)
for b in range(0, 16, 2):
    keys(b, full=b >= 8)
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1300), 0.10)
for b in range(4, 16):
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), hat(), 0.3)
    if b >= 6:
        s.place(s.pos(b, 8), hat(1.2, open_=True), 0.18)
for b in range(8, 16):
    s.place(s.pos(b), lp(bar_of([0, 1, 0, 2][b % 4]), 1400), 0.6)
    bass(b) if b >= 12 else s.place(s.pos(b, 0), sub(midi(ROOTS[chord_at(b)] - 12), 6), 0.2)
s.place(s.pos(14), riser(32), 0.5)
snare_roll(15, 12)

# ================= build 1 (b16-23) =================
for b in range(16, 24):
    drums(b, 'fill' if b == 23 else 'roll')
    keys(b) if b % 2 == 0 else None
    bass(b)
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1500), 0.10) if b % 2 == 0 else None
s.place(s.pos(16), CR, 0.6)
s.place(s.pos(22), riser(32), 0.7)
snare_roll(22, 8); snare_roll(23, 8)
s.place(s.pos(24) - len(CR), rev(CR), 0.9)

# ================= drop 1 (b24-55) =================
s.place(s.pos(24), subdrop(10), 0.5)                     # bass drop!
s.place(s.pos(24), CR, 0.8)
for b in range(24, 56):
    drums(b, 'fill' if b % 8 == 7 else 'roll')
    if b % 2 == 0:
        keys(b)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1600), 0.12)
    bass(b, busy=b % 4 == 3)
    if b >= 40:
        arp(b)
s.place(s.pos(40), CR, 0.6)
s.place(s.pos(40), subdrop(8, 65, 30), 0.35)             # second dip mid-drop
snare_roll(55, 8)
s.place(s.pos(54), riser(32), 0.45)

# ================= breakdown (b56-71) =================
BPROG = ['Dm9', 'Em7', 'Fmaj9', 'G7']
for i, b in enumerate(range(56, 72, 2)):
    ch = BPROG[i % 4]
    s.place(s.pos(b), rhodes(CH[ch], 12), 0.32)
    s.place(s.pos(b), pad(CH[ch], 32, 2000), 0.16)
for b in range(56, 72, 4):
    s.place(s.pos(b), crackle(64), 0.4)
MEL = [69, 76, 74, 72, 71, 74, 72, 67]                  # little answer melody
for i, b in enumerate(range(56, 72, 2)):
    s.place_echo(s.pos(b, 4), pluck(midi(MEL[i]), 2), 0.16, times=3, delay_steps=3, fb=0.5)
for b in range(64, 72):                                  # heartbeat kick returns
    s.pat(b, [(0, K, 0.7), (8, K, 0.55 if b < 68 else 0.7)])
    if b >= 68:
        s.place(s.pos(b, 4), hat(), 0.25); s.place(s.pos(b, 12), hat(), 0.25)
s.place(s.pos(68), riser(64), 0.7)                       # long 4-bar riser
snare_roll(70, 8); snare_roll(71, 4)
s.place(s.pos(72) - len(CR), rev(CR), 0.95)

# ================= drop 2 (b72-103) =================
s.place(s.pos(72), subdrop(10, 80, 27), 0.55)            # the big one
s.place(s.pos(72), CR, 0.9)
for b in range(72, 104):
    if b % 8 == 7:
        drums(b, 'fill')
    elif b % 8 == 5:
        drums(b, 'wah')
    else:
        drums(b, 'roll')
    if b % 2 == 0:
        keys(b)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1700), 0.13)
    bass(b, busy=b % 2 == 1)
    arp(b)
s.place(s.pos(88), CR, 0.6)
s.place(s.pos(88), subdrop(8, 65, 30), 0.35)
s.pat(103, [(8, SN1, 0.6), (10, SN1, 0.7), (12, SN1, 0.85), (13, SN1, 0.9),
            (14, SN1), (15, rev(SN1), 0.8)])

# ================= outro (b104-127) =================
for b in range(104, 112):                                # drums thin out
    drums(b, 'roll' if b < 108 else 'thin')
    bass(b)
    if b % 2 == 0:
        keys(b)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1400), 0.11)
for b in range(112, 120):                                # break gone, hats + keys
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), hat(), 0.22)
    if b % 2 == 0:
        keys(b, full=False)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1200), 0.10)
    s.place(s.pos(b, 0), sub(midi(ROOTS[chord_at(b)] - 12), 6), 0.18)
for b in range(112, 128, 4):
    s.place(s.pos(b), crackle(64), 0.5)
for i, b in enumerate(range(120, 128, 2)):               # fading rhodes echoes
    s.place(s.pos(b), rhodes(CH[chord_at(b)], 10), 0.26 * (1 - i * 0.22))
s.place_echo(s.pos(124, 4), pluck(midi(81), 2), 0.14, times=4, delay_steps=3, fb=0.55)
s.place(s.pos(126), rhodes(CH['Am9'], 24), 0.3)          # final chord rings out
s.place(s.pos(126, 0), sub(midi(21), 20), 0.2)

s.render('amen_liquid_track_174.wav', drive=1.12)
