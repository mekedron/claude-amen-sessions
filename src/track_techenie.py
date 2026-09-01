"""TECHENIE - neurofunk, C minor, 174 BPM.

Written against two records: Magnetude's "Exile" and Magnetude & Receptor's
"Goodbye". Neither could be listened to, so both were measured, and what came
back changed the instrument, not the arrangement.

What the measurements said, and what each one changed here:

- **The mid bass makes four to six attacks a bar.** A written-out riff of
  short notes makes twelve or more. So the bass is not notes at all: it is
  `phrase()`, a whole bar rendered as ONE oscillator that never restarts,
  with the filter, the sync ratio, the FM index and the vowel sequenced
  across it per sixteenth. The timbre carries through the note changes.
- **The low end sounds 81-85% of the time** and dips 30 dB on the kick. So
  the sub is legato and the sidechain is deep and short, rather than the sub
  being retriggered.
- **The sub holds two or three notes across sixteen bars** - one of them for
  43% of the time. So the harmony is a pedal on C with two departures, not a
  bassline.
- **The spectrum is flat within 3 dB from 300 Hz to 11 kHz**, over a shelf
  that rises 9 dB below 130. So: a big low shelf, a scooped 170-220, and a
  broad flat plateau made of distortion rather than of separate parts.
- **400-1200 Hz measures 95-138% side energy** while under 120 Hz measures 5%.
  So the mid bass is rendered twice with different oscillator phases and put
  one per channel, which is width a mono sum averages instead of cancelling.
- **-4.8 and -5.5 LUFS at 6.7 dB crest.** Density is part of the genre here,
  so this master is clipped and limited far harder than the other two in this
  repo, and the arrangement carries a 10 dB range to survive it.
- **The drops are 48 bars long** and the breakdown before them is 10 dB down.

    intro     0-15     one note and the room
    approach  16-31
    DROP 1    32-79    48 bars
    breakdown 80-95    10 dB down
    build     96-103
    DROP 2    104-151  48 bars
    breakdown 152-167
    DROP 3    168-199  32 bars
    outro     200-215
"""
import numpy as np
from neurolib import *

s = Session(216, tail=3.0)
rs = np.random.RandomState(2611)

# C minor, with the natural 6 (A) available - both references use it
C1, D1, Eb1, F1, G1, Ab1, A1, Bb1 = 24, 26, 27, 29, 31, 32, 33, 34
C2, Eb2, F2, G2, Ab2, Bb2 = 36, 39, 41, 43, 44, 46
C3, Eb3, G3, Ab3, Bb3 = 48, 51, 55, 56, 58
C4, Eb4, F4, G4, Ab4, Bb4, C5, Eb5 = 60, 63, 65, 67, 68, 70, 72, 75

CHORDS = [[48, 51, 55, 58, 62],      # Cm9
          [44, 48, 51, 55, 58],      # Abmaj9
          [46, 50, 53, 58, 60],      # Bbsus/Bb9
          [41, 44, 48, 51, 56]]      # Fm11

# ---- the phrases: a bar is one gesture, not sixteen ----
# (step, note, dur, {cut, sync, fm, vow, amp, slide, legato})
L = dict(legato=True)

PH_A = [(0.0,  C1, 4.0, dict(lfo=14.0, cut=(0.95, 0.45, 0.8, 0.5), sync=(1.0, 2.4, 1.3),
                             fm=1.2, **L)),
        (4.0,  C1, 2.5, dict(lfo=27.0, cut=(0.5, 0.95), sync=(1.8, 3.6), fm=2.0,
                             vow=(0.0, 0.8), **L)),
        (6.5,  C1, 3.5, dict(lfo=19.0, cut=(0.85, 0.4, 0.7, 0.35), sync=(2.6, 1.4, 3.2),
                             fm=1.6, amp=(1.0, 1.0, 0.55, 1.0), **L)),
        (10.0, Eb1, 3.0, dict(lfo=44.0, cut=(0.45, 1.0, 0.6), sync=(2.0, 4.4), fm=2.6,
                              vow=(0.6, 0.0), slide=True, **L)),
        (13.0, C1, 3.0, dict(lfo=23.0, cut=(0.9, 0.5, 0.85), sync=(1.6, 3.0, 2.0),
                             fm=1.8, slide=True, **L)),
        (16.0, C1, 5.0, dict(lfo=11.0, cut=(0.8, 0.4, 0.9, 0.45, 0.75),
                             sync=(1.2, 2.8, 1.6, 3.4), fm=1.4, **L)),
        (21.0, Ab1, 3.0, dict(lfo=33.0, cut=(0.55, 1.0), sync=(2.2, 4.8), fm=2.8,
                              vow=(0.0, 1.0), slide=True, **L)),
        (24.0, Bb1, 2.0, dict(lfo=17.0, cut=(0.9, 0.45), sync=(1.8, 3.2), fm=2.0,
                              slide=True, **L)),
        (26.0, C1, 6.0, dict(lfo=52.0, cut=(0.5, 0.95, 0.4, 0.85, 0.55, 1.0),
                             sync=(2.4, 1.3, 3.6, 2.0), fm=2.2,
                             amp=(1.0, 0.6, 1.0, 1.0), slide=True, **L))]

PH_B = [(0.0,  C1, 6.5, dict(lfo=21.0, cut=(0.9, 0.35, 0.75, 0.4, 0.95, 0.5),
                             sync=(1.0, 3.0, 1.5, 2.2), fm=1.6, **L)),
        (6.5,  G1, 3.5, dict(lfo=38.0, cut=(0.45, 1.0, 0.55), sync=(2.6, 5.2), fm=3.0,
                             vow=(0.0, 1.0), slide=True, **L)),
        (10.0, C1, 6.0, dict(lfo=15.0, cut=(0.85, 0.4, 0.9, 0.45), sync=(1.4, 3.4, 1.8),
                             fm=1.8, amp=(1.0, 1.0, 0.5, 1.0), slide=True, **L)),
        (16.0, C1, 4.0, dict(lfo=29.0, cut=(0.55, 0.95, 0.45, 0.85), sync=(2.0, 1.2, 3.8),
                             fm=2.4, **L)),
        (20.0, Eb1, 2.0, dict(lfo=24.0, cut=(0.95, 0.5), sync=(1.6, 3.0), fm=2.0,
                              slide=True, **L)),
        (22.0, F1, 2.0, dict(lfo=47.0, cut=(0.5, 1.0), sync=(2.4, 4.6), fm=2.8,
                             vow=(0.3, 1.0), slide=True, **L)),
        (24.0, Ab1, 3.0, dict(lfo=18.0, cut=(0.9, 0.4, 0.8), sync=(1.8, 3.6, 2.2),
                              fm=2.0, slide=True, **L)),
        (27.0, C1, 5.0, dict(lfo=35.0, cut=(0.45, 0.9, 0.5, 1.0), sync=(2.8, 1.5, 4.0),
                             fm=2.6, amp=(1.0, 0.55, 1.0), slide=True, **L))]

PH_C = [(0.0,  C1, 3.0, dict(lfo=12.0, cut=(1.0, 0.4, 0.85), sync=(1.2, 3.2), fm=1.8, **L)),
        (3.0,  C1, 3.5, dict(lfo=26.0, cut=(0.5, 0.95, 0.45), sync=(2.4, 4.8, 2.0),
                             fm=2.8, vow=(0.0, 1.0), **L)),
        (6.5,  Bb1, 3.5, dict(lfo=41.0, cut=(0.9, 0.45, 0.8), sync=(1.6, 3.4), fm=2.0,
                              slide=True, **L)),
        (10.0, C1, 6.0, dict(lfo=20.0, cut=(0.55, 1.0, 0.4, 0.9), sync=(2.0, 1.3, 3.8, 2.4),
                             fm=2.2, amp=(1.0, 1.0, 0.6, 1.0), slide=True, **L)),
        (16.0, Ab1, 4.0, dict(lfo=31.0, cut=(0.85, 0.4, 0.95, 0.5), sync=(1.4, 3.0, 1.8),
                              fm=1.6, slide=True, **L)),
        (20.0, G1, 3.0, dict(lfo=16.0, cut=(0.5, 1.0, 0.55), sync=(2.6, 5.0), fm=3.2,
                             vow=(0.5, 0.0), slide=True, **L)),
        (23.0, F1, 3.0, dict(lfo=55.0, cut=(0.9, 0.45, 0.85), sync=(1.8, 3.4, 2.2),
                             fm=2.0, slide=True, **L)),
        (26.0, C1, 6.0, dict(lfo=22.0, cut=(0.45, 0.9, 0.5, 1.0, 0.55),
                             sync=(3.0, 1.6, 4.2, 2.2), fm=2.6,
                             amp=(1.0, 0.55, 1.0, 1.0), slide=True, **L))]

PHRASES = (PH_A, PH_B, PH_C, PH_B)

# Three layers, one phrase, and they never share a frequency. The references
# put a quarter of all their energy in 60-120 Hz - that is neither the 33 Hz
# root nor the character layer, it is a body an octave up that neither covers.
MID = dict(vowels=('oo', 'ah'), spread=0.85, f_lo=210, f_hi=8200, res=2.6,
           drive=3.4, low=115, smooth=0.008, octave=24, lfo_depth=0.9)
# The body layer stays smooth: the references put only 2-3% of the sub's
# movement between 20 and 40 Hz, and a growl down there is a rattle.
BODY = dict(spread=0.0, f_lo=70, f_hi=340, res=1.0, drive=2.4, low=52,
            smooth=0.040, octave=12, sync_mul=0.0, fm_mul=0.0, lfo_depth=0.0)


def bass(b, pat, gain=1.0, sub_gain=1.0):
    s.place(s.pos(b), phrase(pat, 2, **MID), gain, bus='bass')
    s.place(s.pos(b), phrase(pat, 2, **BODY), gain * 0.95, bus='body')
    s.place(s.pos(b), subph(pat, 2), sub_gain, bus='sub')


# ---- the kit ----
# kick on 1 and 3, snare on 2 and 4 - what "Goodbye" measures as. Every
# fourth bar goes halftime, which is what "Exile" measures as.
CELLS = [dict(k=(0, 8), s=(4, 12), g=(2, 6, 10, 14), o=(6,), r=(2, 6, 10, 14)),
         dict(k=(0, 8, 10.5), s=(4, 12), g=(2, 6, 9, 14, 15), o=(14,), r=(2, 10)),
         dict(k=(0, 8, 13), s=(4, 12), g=(2, 6.5, 10, 14.5), o=(6,), r=(2, 6, 14)),
         dict(k=(0, 10), s=(8,), g=(2, 4, 6, 12, 14), o=(6,), r=(4, 12))]

HAT_V = [1.00, 0.42, 0.72, 0.40, 0.94, 0.42, 0.78, 0.44,
         0.98, 0.42, 0.72, 0.40, 0.92, 0.44, 0.80, 0.55]


def drums(b, cell, gain=1.0, hats=1.0, ghosts=1.0, ride=1.0, sidechain=True,
          seed=0, bus='drums'):
    for st in cell['k']:
        t = s.pos(b, st)
        s.place(t, nkick(), gain * 1.08, bus)
        if sidechain:
            s.hit(t)
    for i, st in enumerate(cell['s']):
        s.place(s.pos(b, st + rs.randn() * 0.012), nsnare(seed=(seed + i) % 3),
                gain * 1.05, bus)
    if ghosts:
        for i, st in enumerate(cell['g']):
            s.place(s.pos(b, st + rs.randn() * 0.02), nghost(seed=(seed + i) % 4),
                    gain * ghosts * rs.uniform(0.22, 0.40), bus)
    if ride:
        for i, st in enumerate(cell.get('r', ())):
            s.place(s.pos(b, st + rs.randn() * 0.015),
                    nride(2.0, tone=0.96 + 0.05 * (i % 3), seed=i % 3),
                    gain * ride * 0.30, bus)
    if hats:
        loud = set(cell['k']) | set(cell['s'])
        for i in range(16):
            if i in loud:
                continue
            op = i in cell['o']
            shade = 0.45 if any(0 < i - k <= 1 for k in loud) else 1.0
            s.place(s.pos(b, i + rs.randn() * 0.018),
                    nhat(open_=op, tone=1.0 + 0.04 * (i % 3), seed=i % 4),
                    gain * hats * HAT_V[i] * (0.75 if op else 1.0) * shade * 0.52,
                    bus)


def drop(a, n, phrases=PHRASES, lead_from=8):
    """one long drop: the bass phrase turns over every two bars, the kit
    every four, and the pair only line up again every eight"""
    for i in range(0, n, 2):
        b = a + i
        drums(b, CELLS[i % 4], seed=b)
        drums(b + 1, CELLS[(i + 1) % 4], seed=b + 1)
        s.place(s.pos(b), dust(32, seed=b), 0.42, bus='texture')
        bass(b, phrases[(i // 2) % len(phrases)])
        if i % 8 == 6:
            roll(s, b + 1, 12, 6, spacing=0.6, gain=0.62, accel=True, seed=b % 3)
        if i >= lead_from and (i // 2) % 2 == 0:
            for st, note, dur, r1, kw in LEAD:
                bar, step = b + int(st // 16), st % 16
                s.place(s.pos(bar, step),
                        neurolead(note, dur, r1=r1, f_hi=8800, **kw),
                        0.30, bus='music')
        if i % 16 == 0:
            s.place(s.pos(b), crash808(24, gain=0.40), bus='fx')


# a topline that answers the bass instead of running over it: it only speaks
# in the second half of each two-bar cell, where the phrase is holding
LEAD = [(4.0,  G4,  2.0, 3.4, dict(pattern=(1.0, 0.3, 0.8, 0.4))),
        (6.5,  Eb4, 1.5, 2.6, {}),
        (10.0, C5,  2.5, 4.2, dict(pattern=(0.2, 1.0, 0.5, 0.9), vowels=('ah', 'ee'))),
        (13.0, Bb4, 2.5, 3.0, {}),
        (20.0, G4,  2.0, 3.4, dict(pattern=(1.0, 0.3, 0.8, 0.4))),
        (22.5, Ab4, 1.5, 2.8, {}),
        (26.0, Eb5, 2.5, 5.0, dict(pattern=(0.15, 1.0, 0.4, 0.9, 0.3), vowels=('oo', 'ah'))),
        (29.0, C5,  3.0, 3.6, {})]

TUNE = [[(0, C5, 3.0), (4, Bb4, 2.0), (7, G4, 3.0), (11, Ab4, 4.0)],
        [(0, Bb4, 3.0), (4, G4, 2.0), (7, Eb4, 3.5), (12, F4, 3.0)],
        [(0, C5, 2.5), (3, Eb5, 3.0), (8, C5, 2.5), (12, Bb4, 4.0)],
        [(0, Ab4, 3.0), (4, G4, 3.0), (9, F4, 2.0), (12, Eb4, 4.0)]]


# ---- 0-15  one note and the room ----
s.place(s.pos(0), metaldrone(midi(C1), 16 * 16, gain=0.65, seed=1), bus='atmos')
s.place(s.pos(0), voidpad([midi(n) for n in (48, 55, 63)], 16 * 16, cutoff=900,
                          gain=0.30, seed=3), bus='pad')
s.place(s.pos(4), chatter(24, seed=5), 0.40, bus='atmos')
for b, st in ((2, 8), (6, 2), (10, 12), (14, 4)):
    s.place_echo(s.pos(b, st), sonar(4, freq=660 + 90 * (b % 4)), 0.30,
                 times=4, delay_steps=6.0, fb=0.55, bus='atmos')
for b in (7, 11, 15):
    s.place(s.pos(b, 12), reverb(nsnare(6, room=0.6), 2.4, 0.5, 3800), 0.42, bus='fx')
s.place(s.pos(8), scrape(24, seed=11), 0.40, bus='fx')
s.place(s.pos(12), phrase(PH_A, 2, **{**MID, 'f_hi': 2200}), 0.35, bus='bass')
s.place(s.pos(14), phrase(PH_A, 2, **{**MID, 'f_hi': 3400}), 0.45, bus='bass')
s.place(s.pos(14), phrase(PH_A, 2, **BODY), 0.4, bus='body')
s.place(s.pos(14), subph(PH_A, 2), 0.5, bus='sub')
s.place(s.pos(14), riser(32, gain=0.45, f0=110, f1=620), bus='fx')

# ---- 16-31  approach ----
s.place(s.pos(16), metaldrone(midi(C1), 16 * 16, gain=0.5, seed=2), bus='atmos')
s.place(s.pos(16), voidpad([midi(n) for n in (48, 55, 63, 67)], 16 * 16,
                           cutoff=1300, gain=0.24, seed=7), bus='pad')
for i in range(0, 16, 2):
    b = 16 + i
    up = min(1.0, i / 12.0)
    drums(b, CELLS[i % 4], gain=0.34 + 0.55 * up, hats=0.6 + 0.4 * up,
          ghosts=0.5, ride=0.5 + 0.5 * up, seed=b)
    drums(b + 1, CELLS[(i + 1) % 4], gain=0.34 + 0.55 * up,
          hats=0.6 + 0.4 * up, ghosts=0.5, ride=0.5 + 0.5 * up, seed=b + 1)
    bass(b, PHRASES[(i // 2) % 4], gain=0.45 + 0.45 * up, sub_gain=0.5 + 0.45 * up)
s.place(s.pos(24), chatter(16, seed=19), 0.35, bus='atmos')
roll(s, 30, 0, 8, spacing=2.0, gain=0.34, seed=1)
roll(s, 31, 0, 8, spacing=1.0, gain=0.46, seed=2)
roll(s, 31, 8, 6, spacing=0.5, gain=0.58, accel=True, seed=3)
s.place(s.pos(28), riser(4 * 16, gain=0.5, f0=150, f1=2200), bus='fx')
s.place(s.pos(31, 12), whoosh(4, gain=0.55), bus='fx')
s.place(s.pos(32) - int(2.2 * STEP), subdrop(6, f0=110, f1=30, gain=0.6), bus='fx')

# ---- 32-79  DROP 1 (48 bars) ----
drop(32, 48)
s.place(s.pos(32), impact(20, gain=0.45), bus='fx')
for b in range(40, 80, 16):
    s.place(s.pos(b), voidpad([midi(n) for n in CHORDS[(b // 16) % 4]], 16 * 8,
                              cutoff=1100, gain=0.13, seed=29 + b), bus='pad')

# ---- 80-95  breakdown, ten decibels down ----
s.place(s.pos(79, 12), downlifter(12, gain=0.5), bus='fx')
s.place(s.pos(80), metaldrone(midi(C1), 16 * 16, gain=0.55, seed=31), bus='atmos')
for i, ch in enumerate(CHORDS):
    b = 80 + i * 4
    s.place(s.pos(b), voidpad([midi(n) for n in ch], 4 * 16, cutoff=1700,
                              gain=0.30, seed=37 + i), bus='pad')
    s.place(s.pos(b), pad([midi(n + 12) for n in ch], 4 * 16, cutoff=3000,
                          gain=0.10, wide=1.4), bus='pad')
    s.place(s.pos(b), nsub((C1, Ab1, Bb1, F1)[i], 4 * 16, decay=3.4), 0.75, bus='sub')
    for st, note, dur in TUNE[i]:
        s.place(s.pos(b + 1, st), lead(midi(note), dur, gain=0.30), bus='music')
        s.place(s.pos(b + 1, st), glass(midi(note + 12), dur * 0.6, gain=0.14), bus='music')
for b, st in ((82, 6), (86, 10), (90, 2), (94, 8)):
    s.place_echo(s.pos(b, st), sonar(4, freq=920), 0.22, times=3,
                 delay_steps=4.5, fb=0.5, bus='atmos')
s.place(s.pos(88), chatter(20, seed=41), 0.35, bus='atmos')

# ---- 96-103  build ----
for i in range(0, 8, 2):
    b = 96 + i
    drums(b, CELLS[i % 4], gain=0.5 + 0.4 * i / 8 - 0.30 * (i / 8) ** 3,
          hats=0.85, ghosts=0.6, seed=b)
    drums(b + 1, CELLS[(i + 1) % 4], gain=0.5 + 0.4 * i / 8 - 0.30 * (i / 8) ** 3,
          hats=0.85, ghosts=0.6, seed=b + 1)
    bass(b, PHRASES[(i // 2) % 4], gain=0.55, sub_gain=0.6)
    s.place(s.pos(b), voidpad([midi(n) for n in CHORDS[i % 4]], 32,
                              cutoff=1500 + 300 * i, gain=0.16, seed=43 + i), bus='pad')
s.place(s.pos(96), riser(8 * 16, gain=0.6, f0=160, f1=2800), bus='fx')
roll(s, 102, 0, 8, spacing=2.0, gain=0.36, seed=4)
roll(s, 103, 0, 8, spacing=1.0, gain=0.48, seed=5)
roll(s, 103, 8, 7, spacing=0.5, gain=0.60, accel=True, seed=6)
s.place(s.pos(103, 12), whoosh(4, gain=0.6), bus='fx')
s.place(s.pos(104) - int(2.2 * STEP), subdrop(6, f0=120, f1=28, gain=0.7), bus='fx')

# ---- 104-151  DROP 2 (48 bars) ----
drop(104, 48, phrases=(PH_C, PH_A, PH_B, PH_C), lead_from=4)
s.place(s.pos(104), impact(20, gain=0.5), bus='fx')
for b in range(112, 152, 16):
    s.place(s.pos(b), voidpad([midi(n) for n in CHORDS[(b // 16) % 4]], 16 * 8,
                              cutoff=1300, gain=0.12, seed=47 + b), bus='pad')

# ---- 152-167  second breakdown ----
s.place(s.pos(151, 12), downlifter(12, gain=0.5), bus='fx')
s.place(s.pos(152), metaldrone(midi(C1), 16 * 16, gain=0.55, seed=53), bus='atmos')
for i, ch in enumerate(CHORDS):
    b = 152 + i * 4
    s.place(s.pos(b), voidpad([midi(n) for n in ch], 4 * 16, cutoff=2000,
                              gain=0.28, seed=59 + i), bus='pad')
    s.place(s.pos(b), nsub((C1, Ab1, Bb1, F1)[i], 4 * 16, decay=3.4), 0.75, bus='sub')
    for st, note, dur in TUNE[(i + 2) % 4]:
        s.place(s.pos(b + 2, st), lead(midi(note), dur, gain=0.28), bus='music')
for b in range(160, 168, 2):
    drums(b, CELLS[3], gain=0.45 + 0.10 * (b - 160), hats=0.5, ghosts=0.4, seed=b)
    bass(b, PH_A, gain=0.5, sub_gain=0.55)
s.place(s.pos(164), riser(4 * 16, gain=0.55, f0=170, f1=3000), bus='fx')
roll(s, 167, 0, 8, spacing=1.0, gain=0.5, seed=7)
roll(s, 167, 8, 8, spacing=0.5, gain=0.62, accel=True, seed=8)
s.place(s.pos(168) - int(2.4 * STEP), subdrop(7, f0=130, f1=27, gain=0.75), bus='fx')

# ---- 168-199  DROP 3 (32 bars) ----
drop(168, 32, phrases=(PH_B, PH_C, PH_A, PH_C), lead_from=0)
s.place(s.pos(168), impact(24, gain=0.55), bus='fx')
s.place(s.pos(168), crash808(28, gain=0.5), bus='fx')
for b in range(168, 200, 8):
    s.place(s.pos(b), voidpad([midi(n) for n in CHORDS[(b // 8) % 4]], 8 * 16,
                              cutoff=1500, gain=0.13, seed=67 + b), bus='pad')

# ---- 200-215  outro ----
s.place(s.pos(199, 12), downlifter(14, gain=0.5), bus='fx')
s.place(s.pos(200), metaldrone(midi(C1), 16 * 16, gain=0.6, seed=71), bus='atmos')
s.place(s.pos(200), voidpad([midi(n) for n in (48, 55, 63)], 16 * 16, cutoff=800,
                            gain=0.28, seed=73), bus='pad')
for i in range(0, 12, 2):
    b = 200 + i
    fade = max(0.0, 1 - i / 11.0)
    drums(b, CELLS[i % 4], gain=0.75 * fade, hats=0.7 * fade, ghosts=0.4 * fade,
          ride=0.5 * fade, sidechain=i < 6, seed=b)
    drums(b + 1, CELLS[(i + 1) % 4], gain=0.75 * fade, hats=0.7 * fade,
          ghosts=0.4 * fade, ride=0.5 * fade, sidechain=i < 6, seed=b + 1)
    if i < 8:
        bass(b, PH_A, gain=0.55 * fade, sub_gain=0.6 * fade)
for b, st in ((204, 8), (208, 2), (212, 6)):
    s.place_echo(s.pos(b, st), sonar(4, freq=700), 0.28, times=4,
                 delay_steps=6.0, fb=0.55, bus='atmos')
s.place(s.pos(210), chatter(24, seed=79), 0.40, bus='atmos')

# ---- mix ----
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.5, wet=0.28, tone=4800)
s.bus['pad'] = bus_reverb(s.bus['pad'], decay=3.4, wet=0.34, tone=2800)
s.bus['atmos'] = bus_reverb(s.bus['atmos'], decay=4.2, wet=0.38, tone=2200)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=2.2, wet=0.22, tone=3800)
# The references scoop 170-220 Hz by 5-7 dB under a shelf that rises 9 dB
# below 130. That dip is what lets a 33 Hz root be that loud without the mix
# turning to mud, and it is where the bass and the snare's body collide.
s.bus['bass'] = peak_eq(peak_eq(s.bus['bass'], 195, -4.0, 0.35), 560, -7.0, 0.6)
s.bus['bass'] = shelf(peak_eq(s.bus['bass'], 1600, 2.5, 0.5), 3200, 2.0, 'high')
# The flat plateau the references hold from 300 Hz to 11 kHz is not parts. It
# is what a bass this loud does to a saturator: continuous broadband harmonics
# that fill every gap between the drum hits. Density has to come from the
# source - a clipper on the master only takes the transients off.
s.bus['bass'] = dirty(s.bus['bass'], 1.8)
s.bus['body'] = dirty(s.bus['body'], 1.3)
s.bus['drums'] = peak_eq(shelf(hp(s.bus['drums'], 42, order=2), 5200, 1.0, 'high'),
                         1900, 2.5, 0.5)
s.bus['sub'] = mono_below(s.bus['sub'], 200)
s.bus['body'] = mono_below(s.bus['body'], 300)
s.bus['bass'] = mono_below(s.bus['bass'], 160)
s.bus['atmos'] = hp(s.bus['atmos'], 34, order=2)
s.bus['music'] = shelf(s.bus['music'], 3500, -2.0, 'high')
# The references hold a flat plateau to 11 kHz. Half of that is not a part at
# all - it is broadband dirt sitting under everything, and with the texture
# bus this quiet the mix simply stops at 3 kHz.
s.bus['texture'] = shelf(s.bus['texture'], 6000, 3.0, 'high')

GAINS = {'drums': 0.62, 'sub': 0.185, 'body': 0.52, 'bass': 0.78,
         'texture': 5.00, 'music': 1.30, 'pad': 1.10, 'atmos': 0.44, 'fx': 0.22}
s.report(GAINS)
# The clipper does the peak work and the glue only catches what it leaves.
# Pushed further than this the beat starts to go: at 20% of samples shaped the
# kick's click is 1 dB from disappearing, and the last 2 dB of loudness the
# references have comes from a denser source, not from a harder master.
s.render('neuro_techenie_174.wav', drive=1.15, duck=0.28, limit=0.95, peak=0.94,
         gains=GAINS, clip=0.80, fade=2.0,
         comp=dict(thresh=0.42, ratio=4.0, attack=0.0008, release=0.06))
