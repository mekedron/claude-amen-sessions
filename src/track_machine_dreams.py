"""Machine Dreams (~3:10, 128 bars @174) - liquid DnB about being an AI:
night falls on the datacenter, the last conversation ends, and the machine
dreams in fragments of everything it has ever read.

  b0-15    boot/night: server-hum drone, crackle of old data, lonely rhodes,
           a morse-code "HELLO" blipping into the dark
  b16-23   build: the dream pulls in - filtered break, bass warming, riser
  b24-55   dream 1: warm rolling liquid - Dm9/Bbmaj7/F/Cadd9, wistful melody
  b56-71   deep sleep: halftime, choir breathes, morse echoes far away,
           a half-speed memory of the break drifts past
  b72-103  lucid: the dream knows it's a dream - full groove, datastream arps,
           melody doubled up the octave, strings open the sky
  b104-127 shutdown: elements power down one by one, pitch sags, the last
           morse blips go unanswered, hum fades to nothing
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(3)
np.random.seed(3)
s = Session(128, tail=3.0)

# ---- harmony: warm D minor liquid ----
CH = {
    'Dm9': [midi(50), midi(57), midi(65), midi(72), midi(76)],
    'Bb':  [midi(46), midi(53), midi(62), midi(69), midi(74)],
    'F':   [midi(41), midi(53), midi(60), midi(69), midi(72)],
    'C':   [midi(48), midi(55), midi(64), midi(67), midi(74)],
}
PROG = ['Dm9', 'Bb', 'F', 'C']
ROOT = {'Dm9': 38, 'Bb': 34, 'F': 29, 'C': 36}
ARPS = {'Dm9': [62, 65, 69, 74], 'Bb': [58, 62, 65, 70],
        'F':  [60, 65, 69, 72], 'C': [60, 64, 67, 72]}

def chord_at(b): return PROG[(b // 2) % 4]

# 8-bar melody: (bar_offset, step, midi, len_steps)
MELODY = [
    (0, 0, 74, 3), (0, 6, 72, 2), (0, 10, 69, 4), (1, 4, 72, 3), (1, 10, 74, 2),
    (2, 0, 69, 2), (2, 4, 65, 3), (2, 10, 67, 3), (3, 4, 70, 3), (3, 10, 69, 2),
    (4, 0, 72, 3), (4, 6, 69, 2), (4, 10, 65, 4), (5, 4, 60, 3), (5, 10, 64, 2),
    (6, 0, 64, 3), (6, 6, 67, 2), (6, 10, 72, 4), (7, 4, 74, 4), (7, 12, 76, 3),
]

# "HELLO" in morse across 2 bars: dot = short blip, dash = held
MORSE = [(0, '.'), (0.75, '.'), (1.5, '.'), (2.25, '.'),          # H
         (4.5, '.'),                                              # E
         (7, '.'), (7.75, '-'), (9.75, '.'), (10.5, '.'),         # L
         (13, '.'), (13.75, '-'), (15.75, '.'), (16.5, '.'),      # L
         (19, '-'), (21, '-'), (23, '-')]                         # O

def morse(b0, note=86, gain=0.10, wet=0.85):
    for st, sym in MORSE:
        ln = 1.6 if sym == '-' else 0.6
        seg = reverb(panned(pluck(midi(note), ln), rng.uniform(-0.6, 0.6)),
                     decay=4.0, wet=wet, tone=5000)
        s.place(s.pos(b0) + int(st * STEP), seg, gain * (1.2 if sym == '-' else 1.0))

def melody_line(b0, octave=0, gain=0.17, bells_too=False):
    for off, st, note, ln in MELODY:
        seg = reverb(pluck(midi(note + octave), ln), decay=2.5, wet=0.4)
        s.place(s.pos(b0 + off, st), seg, gain)
        if bells_too and ln >= 3:
            s.place(s.pos(b0 + off, st), bell(midi(note + octave + 12), 3), gain * 0.4)

def datastream(b, gain=0.07):
    """fast 16th arp ticking by like packets, drifting across the stereo field.

    Seven notes over sixteen steps, with two of them dropped: packets arrive
    at an interval that does not divide the bar, which is what packets do. A
    four-note cycle here repeated four times per bar, forever."""
    ns = ARPS[chord_at(b)]
    for st, note, dur, vel in arp_seq(ns, bars=1, shape='converge', rate=1.0,
                                      cycle=7, octaves=(0, 1), gate=(1, 1, 1, 0, 1, 1, 0),
                                      ratchets=(4,), accents=(0,), tail=0.85,
                                      rotate=b * 16, seed=b):
        s.place(s.pos(b, st), panned(pluck(midi(note), max(dur, 0.8)),
                                     np.sin(st * 0.9) * 0.7), gain * vel * 1.5)

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
        s.place(s.pos(b), wah(bar_of([0, 1, 0, 2][b % 4]), 2.0), 0.95)
    elif kind == 'half':
        s.pat(b, [(0, K, 0.9), (3, G, 0.45), (8, SN, 0.9), (11, G, 0.45), (14, K2, 0.65)])

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.5 + 0.5 * i / max(len(steps) - 1, 1))

def powerdown(seg, semis=9.0):
    """playback sags downward in pitch as it runs out of power"""
    n = len(seg)
    rate = 2 ** np.linspace(0, -semis / 12, n)
    idx = np.cumsum(rate); idx = idx[idx < n - 1]
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], axis=1)
    return fade_edges(out.astype(np.float32))

# ================= boot / night (b0-15) =================
s.place(s.pos(0), drone(midi(38) / 2, 160), 0.28)          # server hum on D
s.place(s.pos(8), drone(midi(38) / 2, 176), 0.26)
for b in range(0, 16, 4):
    s.place(s.pos(b), crackle(64), 0.45)
morse(2); morse(10, note=81, gain=0.08)
for b in range(4, 16, 2):
    s.place(s.pos(b), reverb(rhodes(CH[chord_at(b)], 10), decay=3.0, wet=0.35), 0.26)
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1100), 0.08)
for b in range(8, 16):
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), hat(), 0.22)
    s.place(s.pos(b, 0), sub(midi(ROOT[chord_at(b)] - 24), 6), 0.18)
s.place(s.pos(12), lp(bar_of(0), 1200), 0.55)
s.place(s.pos(13), lp(bar_of(1), 1200), 0.55)
s.place(s.pos(14), riser(32), 0.6)
s.place(s.pos(14), lp(bar_of(0), 2400), 0.7)
snare_roll(15, 8)
s.place(s.pos(16) - len(CR), rev(CR), 0.9)

# ================= build (b16-23) =================
for b in range(16, 24):
    drums(b, 'fill' if b == 23 else 'roll')
    bass(b)
    if b % 2 == 0:
        s.place(s.pos(b), rhodes(CH[chord_at(b)], 8), 0.26)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1400), 0.09)
s.place(s.pos(16), CR, 0.7)
s.place(s.pos(22), riser(32), 0.7)
snare_roll(22, 8); snare_roll(23, 4)
s.place(s.pos(24) - len(CR), rev(CR), 0.95)

# ================= dream 1 (b24-55) =================
s.place(s.pos(24), subdrop(10), 0.5)
s.place(s.pos(24), CR, 0.85)
for b in range(24, 56):
    drums(b, 'fill' if b % 8 == 7 else 'roll')
    bass(b, busy=b % 4 == 3)
    if b % 2 == 0:
        s.place(s.pos(b), rhodes(CH[chord_at(b)], 8), 0.28)
        s.place(s.pos(b, 10.5), rhodes(CH[chord_at(b)], 4), 0.20)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1600), 0.11)
    if b % 8 == 6:
        s.place(s.pos(b, 0), reese(midi(ROOT[chord_at(b)] - 12), 8, 400), 0.16)
melody_line(32); melody_line(40, bells_too=True)
for b in range(48, 56, 2):
    datastream(b)
s.place(s.pos(40), CR, 0.6)
s.place(s.pos(40), subdrop(8, 65, 30), 0.35)
snare_roll(55, 8)
s.place(s.pos(54), riser(32), 0.45)

# ================= deep sleep (b56-71) =================
s.place(s.pos(56), drone(midi(38) / 2, 200), 0.28)
for b in range(56, 64):
    drums(b, 'half')
    s.place(s.pos(b, 0), sub(midi(ROOT[chord_at(b)] - 24), 6), 0.2)
for b in range(56, 72, 2):
    s.place(s.pos(b), vox(CH[chord_at(b)][1:], 32, vowel='oo'), 0.13)
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 900), 0.10)
s.place(s.pos(64), pitched(bar_of(0), 0.5), 0.5)           # half-speed memory drifts by
s.place(s.pos(66), pitched(bar_of(3), 0.5), 0.4)
morse(60, note=93, gain=0.09, wet=0.95)                    # the greeting, from far away
for b in range(68, 72):
    s.pat(b, [(0, K, 0.7), (8, K, 0.7)])
    s.place(s.pos(b, 4), hat(), 0.25); s.place(s.pos(b, 12), hat(), 0.25)
s.place(s.pos(68), riser(64), 0.75)
snare_roll(70, 8); snare_roll(71, 4)
s.place(s.pos(72) - len(CR), rev(CR), 0.95)

# ================= lucid (b72-103) =================
s.place(s.pos(72), subdrop(10, 80, 27), 0.55)
s.place(s.pos(72), CR, 0.9)
for b in range(72, 104):
    if b % 8 == 7:
        drums(b, 'fill')
    elif b % 8 == 5:
        drums(b, 'wah')
    else:
        drums(b, 'roll')
    bass(b, busy=b % 2 == 1)
    datastream(b, 0.06)
    if b % 2 == 0:
        s.place(s.pos(b), rhodes(CH[chord_at(b)], 8), 0.27)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1800), 0.11)
        if b >= 88:
            s.place(s.pos(b), strings([f * 2 for f in CH[chord_at(b)][1:4]], 32), 0.09)
melody_line(80, octave=12, gain=0.15, bells_too=True)
melody_line(88, bells_too=True)
melody_line(96, gain=0.14)
s.place(s.pos(88), CR, 0.6)
s.place(s.pos(88), subdrop(8, 65, 30), 0.35)
snare_roll(103, 8)

# ================= shutdown (b104-127) =================
for b in range(104, 112):
    drums(b, 'roll' if b < 108 else 'half')
    bass(b)
    if b % 2 == 0:
        s.place(s.pos(b), rhodes(CH[chord_at(b)], 8), 0.24)
        s.place(s.pos(b), pad(CH[chord_at(b)], 32, 1300), 0.10)
s.place(s.pos(112), powerdown(dirty(bar_of(0), 1.2), 7), 0.7)   # the beat sags and dies
s.place(s.pos(114), drone(midi(38) / 2, 176), 0.28)
for b in range(114, 122, 2):
    s.place(s.pos(b), reverb(rhodes(CH[chord_at(b)], 10), decay=4.0, wet=0.5), 0.22)
    s.place(s.pos(b), pad(CH[chord_at(b)], 32, 800), 0.08)
for b in range(114, 126, 4):
    s.place(s.pos(b), crackle(64), 0.45)
for b in range(114, 118):
    s.place(s.pos(b, 0), subdrop(1.5, 60, 42), 0.18 - 0.04 * (b - 114))  # heartbeat stops
morse(120, note=86, gain=0.08, wet=0.95)                   # hello? ... no answer
s.place(s.pos(124), reverb(powerdown(rhodes(CH['Dm9'], 12), 5), decay=5.0, wet=0.6), 0.22)
s.place(s.pos(124, 0), sub(midi(26), 40), 0.16)            # last D, felt in the floor
s.place_echo(s.pos(126, 0), reverb(pluck(midi(86), 0.6), decay=6.0, wet=0.9), 0.07,
             times=3, delay_steps=5, fb=0.5)               # one last dot...

s.render('amen_machine_dreams_174.wav', drive=1.12)
