"""Sound System (~2:50, 124 bars @174) - ragga jungle: dub foundation, sirens,
DJ rewinds, a two-note riddim bass, and an Amen you can count to all the way.
G minor. Kick on the one, snares on two and four - the count is law.

  b0-7     dub intro: one-drop drums, offbeat skanks in echo, siren calls
  b8-15    the bass arrives, dub style - heavy and slow over the one-drop
  b16-19   rewind! + roll ->
  b20-51   JUNGLE DROP 1: full break + wobble riddim, skanks, sirens answer
  b52-59   dub break: one-drop again, echoes flying everywhere
  b60-63   rewind + build
  b64-95   DROP 2: riddim doubles up, edits get rowdier (anchored, countable)
  b96-123  cool-down: back to the dub, siren dissolves into its own echo
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(76)
np.random.seed(76)
s = Session(124, tail=2.5)

# riddim: G / G / Bb / F, one bar each
RIDDIM = [43, 43, 46, 41]                                  # G2 G2 Bb2 F2 (midi)
SKANK = {43: [58, 62, 67], 46: [58, 65, 70], 41: [57, 60, 65]}  # Gm / Bb / F

def root_at(b): return RIDDIM[b % 4]

def skank(b, steps=(2, 6, 10, 14), gain=0.24, echo=False):
    ch = [midi(n) for n in SKANK[root_at(b)]]
    for st in steps:
        seg = clav(ch, 1.2)
        if echo:
            s.place_echo(s.pos(b, st), seg, gain, times=2, delay_steps=3, fb=0.45)
        else:
            s.place(s.pos(b, st), seg, gain)

def onedrop(b, hats=True):
    """reggae one-drop: kick+snare together on beat 3, nothing on the one"""
    s.place(s.pos(b, 8), K, 0.9)
    s.place(s.pos(b, 8), SN, 0.75)
    if hats:
        for st in (2, 6, 10, 14):
            s.place(s.pos(b, st), hat(), 0.22)
    if rng.random() < 0.4:
        s.place(s.pos(b, 15), G, 0.4)

def riddim_bass(b, style='dub'):
    r = midi(root_at(b) - 24)                              # down where it hurts
    if style == 'dub':
        s.place(s.pos(b, 0), sub(r, 5), 0.34)
        s.place(s.pos(b, 8), sub(r, 3), 0.28)
        s.place(s.pos(b, 12), sub(r * 1.5, 2), 0.22)
    elif style == 'wobble':
        s.place(s.pos(b, 0), wobble(r, 8, 2.2), 0.36)
        s.place(s.pos(b, 8), sub(r, 3), 0.28)
        s.place(s.pos(b, 12), sub(r, 3), 0.28)
    elif style == 'double':
        for st in (0, 3, 6, 8, 11, 14):
            s.place(s.pos(b, st), sub(r * (2 if st in (3, 11) else 1), 2), 0.26)

def drums(b, kind='roll'):
    if kind == 'roll':
        s.place(s.pos(b), bar_of([0, 1, 0, 2][b % 4]), 0.92)
    elif kind == 'edit':                                   # anchored: count survives
        s.pat(b, [(0, K), (2, K2, 0.6), (4, SN), (6, G, 0.5), (8, K, 0.85),
                  (10, SN1, 0.6), (12, S2), (14, rev(SN1), 0.55)])
    elif kind == 'dirty':
        s.place(s.pos(b), dirty(bar_of([0, 1, 2, 1][b % 4]), 1.5), 0.9)

def siren(b, st, f0=650, lfo=3.0, shape='tri', gain=0.14):
    s.place_echo(s.pos(b, st), dubsiren(4, f0, lfo, shape=shape), gain,
                 times=3, delay_steps=3, fb=0.5)

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.5 + 0.5 * i / max(len(steps) - 1, 1))

def do_rewind(b, src_bar=0):
    s.place(s.pos(b), rewind(bar_of(src_bar), 3.5), 0.75)

# ================= dub intro (b0-7) =================
s.place(s.pos(0), crackle(128), 0.45)
for b in range(0, 8):
    onedrop(b)
    skank(b, echo=b % 2 == 1)
siren(1, 8); siren(5, 0, 780, 2.0, 'square', 0.11)
s.place(s.pos(6, 0), sub(midi(19), 8), 0.18)               # low G stirring

# ================= bass arrives (b8-15) =================
for b in range(8, 16):
    onedrop(b)
    skank(b, echo=b % 4 == 3)
    riddim_bass(b, 'dub')
s.place(s.pos(8), CR, 0.6)
siren(11, 8, 650, 3.0)
siren(14, 4, 520, 4.5, 'square', 0.12)

# ================= rewind + build (b16-19) =================
do_rewind(16)
for b in (17, 18):
    drums(b, 'roll')
    riddim_bass(b, 'dub')
    skank(b)
s.place(s.pos(18), riser(32), 0.6)
snare_roll(19, 8)
s.place(s.pos(20) - len(CR), rev(CR), 0.95)

# ================= JUNGLE DROP 1 (b20-51) =================
s.place(s.pos(20), subdrop(10), 0.5)
s.place(s.pos(20), CR, 0.9)
for b in range(20, 52):
    drums(b, 'edit' if b % 8 == 7 else 'roll')
    riddim_bass(b, 'wobble')
    skank(b, steps=(2, 10) if b % 2 == 0 else (2, 6, 10, 14))
    if b % 8 == 4:
        siren(b, 2, float(rng.choice([520, 650, 780])), float(rng.uniform(2, 4)))
s.place(s.pos(36), CR, 0.6)
s.place(s.pos(36), subdrop(8, 65, 30), 0.35)
snare_roll(51, 8)

# ================= dub break (b52-59) =================
for b in range(52, 60):
    onedrop(b)
    skank(b, echo=True)
    riddim_bass(b, 'dub')
siren(53, 8, 780, 2.5); siren(57, 0, 650, 5.0, 'square', 0.12)
s.place(s.pos(56), pad([midi(n) for n in (55, 58, 62, 67)], 64, 1100), 0.10)

# ================= rewind + build (b60-63) =================
do_rewind(60, 3)
for b in (61, 62):
    drums(b, 'roll')
    riddim_bass(b, 'wobble')
s.place(s.pos(62), riser(32), 0.75)
snare_roll(62, 8); snare_roll(63, 4)
s.place(s.pos(64) - len(CR), rev(CR), 0.95)

# ================= DROP 2 (b64-95) =================
s.place(s.pos(64), subdrop(10, 80, 27), 0.55)
s.place(s.pos(64), CR, 0.95)
for b in range(64, 96):
    if b % 8 == 7:
        drums(b, 'edit')
    elif b % 8 == 3:
        drums(b, 'dirty')
    else:
        drums(b, 'roll')
    riddim_bass(b, 'double' if b % 4 == 3 else 'wobble')
    skank(b, steps=(2, 6, 10, 14), gain=0.22)
    if b % 8 == 4:
        siren(b, 2, float(rng.choice([650, 780, 980])), float(rng.uniform(3, 6)),
              'square' if rng.random() < 0.4 else 'tri')
s.place(s.pos(80), CR, 0.6)
s.place(s.pos(80), subdrop(8, 65, 30), 0.35)
snare_roll(95, 8)

# ================= cool-down (b96-123) =================
for b in range(96, 104):
    drums(b, 'roll')
    riddim_bass(b, 'dub')
    skank(b, steps=(2, 10))
for b in range(104, 116):
    onedrop(b)
    skank(b, echo=b % 2 == 1)
    riddim_bass(b, 'dub') if b < 112 else s.place(s.pos(b, 0), sub(midi(19), 6), 0.2)
siren(106, 8, 650, 3.0)
s.place(s.pos(110), crackle(96), 0.45)
for b in range(116, 122):
    onedrop(b, hats=False)
    if b % 2 == 0:
        skank(b, steps=(2, 10), gain=0.18, echo=True)
s.place_echo(s.pos(120, 8), dubsiren(6, 520, 1.5), 0.12, times=5, delay_steps=4, fb=0.6)
s.place(s.pos(122, 8), K, 0.6); s.place(s.pos(122, 8), SN, 0.5)   # last one-drop
s.place(s.pos(122, 8), sub(midi(19), 16), 0.2)

s.render('amen_soundsystem_174.wav', drive=1.25)
