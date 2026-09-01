"""ZUBY - BEZDNA with teeth. Dark neurofunk, F minor, 174 BPM.

Same key, same drums, same arrangement, same structure, note for note. The
only thing rebuilt is the bass, because that is the only thing that was
wrong: measured side by side against the voice it replaces, `growlmid` had

    +4.5 dB of attack over its own body      a hit needs +10 to +18
    -8.8 dB of energy above 1 kHz vs below   all weight, no teeth
     5.9 dB of filter swing                  modulated often, never far
    -3.0 dB odd-versus-even harmonics        warm, when it should be hollow

`snarl()` fixes those four numbers and nothing else. It keeps the integer FM
ratio that makes a note a note, and its pitch definition still measures above
what the reference records manage in their own bass band - loud and filthy is
not the same as vague.

    intro     0-15    the room, before anything is in it
    approach  16-31   drums arrive filtered, the sub starts breathing
    build 1   32-39
    DROP 1    40-71   32 bars
    breakdown 72-87
    build 2   88-95
    DROP 2    96-127
    bridge    128-139 halftime
    build 3   140-147
    DROP 3    148-175
    outro     176-191
"""
import numpy as np
from neurolib import *

s = Session(192, tail=3.0)
rs = np.random.RandomState(2026)

# ---- the material ----
F1, Gb1, Ab1, Bb1, Db1, Eb1, C1 = 29, 30, 32, 34, 25, 27, 24
F2, Gb2, Ab2, Bb2, C2, Db2, Eb2 = 41, 42, 44, 46, 36, 37, 39
F3, Gb3, Ab3, C3 = 53, 54, 56, 48
F4, Gb4, Ab4, Bb4, C5, Db5, Eb5, F5 = 65, 66, 68, 70, 72, 73, 75, 77

# i - bVI - bIII - bII: the last chord is the Phrygian one, and it is the
# reason the loop restarts instead of resolving.
CHORDS = [[53, 56, 60, 63, 67],      # Fm9
          [49, 53, 56, 60, 63],      # Dbmaj9
          [56, 60, 63, 67, 70],      # Abmaj9
          [54, 58, 61, 65, 72]]      # Gbmaj7#11

HAT_V = [1.00, 0.40, 0.70, 0.38, 0.92, 0.40, 0.76, 0.42,
         0.98, 0.40, 0.70, 0.38, 0.90, 0.42, 0.78, 0.52]

# (kicks, snares, ghosts, open hats). Four cells make a phrase: the ear needs
# bar 2 to differ from bar 1 and bar 4 to announce the next four.
CELLS_A = [dict(k=(0, 10), s=(4, 12), g=(6, 9, 14), o=(6,)),
           dict(k=(0, 6.5, 10), s=(4, 12), g=(2, 9, 13, 15), o=(14,)),
           dict(k=(0, 11), s=(4, 12), g=(2, 6.5, 9, 14.5), o=(6,)),
           dict(k=(0, 10, 15), s=(4, 12, 14), g=(2, 6, 9), o=())]

CELLS_B = [dict(k=(0, 8.5, 10), s=(4, 12), g=(2.5, 6, 9, 13, 15), o=(6,)),
           dict(k=(0, 10), s=(4, 12, 15), g=(2, 5.5, 9, 13), o=(14,)),
           dict(k=(0, 6, 10.5), s=(4, 12), g=(2, 7, 9, 14), o=(6,)),
           dict(k=(0, 10, 12.5), s=(4, 12, 14.5), g=(2.5, 6, 9), o=())]

CELLS_C = [dict(k=(0, 10), s=(4, 12), g=(2, 6, 7, 9, 14), o=(6,)),
           dict(k=(0, 3.5, 10), s=(4, 12, 14), g=(2, 6.5, 9, 13), o=(14,)),
           dict(k=(0, 10, 11), s=(4, 12), g=(2, 5, 6.5, 9, 15), o=(6,)),
           dict(k=(0, 8, 10), s=(4, 12, 13.5, 15), g=(2, 6, 9), o=())]


# ---- the kit, played ----
SNARES = []


def drums(b, cell, gain=1.0, hats=1.0, ghosts=1.0, sidechain=True, seed=0,
          bus='drums'):
    """One bar. Timing jitter goes on everything except the kick - move the
    kick and the whole track slides."""
    for st in cell['k']:
        t = s.pos(b, st)
        s.place(t, nkick(), gain * 1.08, bus)
        if sidechain:
            s.hit(t)
    for i, st in enumerate(cell['s']):
        v = 1.0 if st in (4, 12) else 0.55
        t = s.pos(b, st + rs.randn() * 0.012)
        s.place(t, nsnare(seed=(seed + i) % 3), gain * v * 1.05, bus)
        if sidechain and v == 1.0:
            SNARES.append(t)
    if ghosts:
        for i, st in enumerate(cell['g']):
            s.place(s.pos(b, st + rs.randn() * 0.02),
                    nghost(seed=(seed + i) % 4),
                    gain * ghosts * rs.uniform(0.22, 0.40), bus)
    if hats:
        loud = set(cell['k']) | set(cell['s'])
        for i in range(16):
            if i in loud:
                continue                # the kick and the snare own their step
            op = i in cell['o']
            # A hat one 16th after a kick lands inside that kick's forward
            # masking window, so it costs the kick its click and buys nothing.
            shade = 0.45 if any(0 < i - k <= 1 for k in loud) else 1.0
            s.place(s.pos(b, i + rs.randn() * 0.018),
                    nhat(open_=op, tone=1.0 + 0.04 * (i % 3), seed=i % 4),
                    gain * hats * HAT_V[i] * (0.75 if op else 1.0) * shade * 0.52,
                    bus)


def subline(b, notes, gain=1.0, bus='sub'):
    """Strictly monophonic: each note is trimmed to end where the next one
    starts. Two overlapping sines at 43 Hz do not sound like two notes, they
    sound like a level jump and a phase cancellation."""
    for i, (st, note, dur) in enumerate(notes):
        end = notes[i + 1][0] if i + 1 < len(notes) else st + dur
        s.place(s.pos(b, st), nsub(note, min(dur, end - st + 0.4),
                                   decay=0.55), gain, bus)


def bassline(b, notes, gain=1.0, bus='bass'):
    """(step, voice, note, dur, gain, kwargs) - the mid layer, above 110 Hz"""
    for st, voice, note, dur, g, kw in notes:
        s.place(s.pos(b, st), voice(note, dur, **kw), gain * g, bus)



# ---- the bassline: long notes whose growl rate changes inside them ----
# The old version of this track played six to eight short notes a bar, each
# with its own fixed modulation. However varied the notes, that is an
# arpeggiator with a filter on it - the ear hears a sequence of events, not a
# bass. What a bassline in this genre does is stretch: one note holds while
# the rate of its own modulation ramps from a slow sweep up into a scream and
# back down, unevenly, across four or eight beats.
#
# The `lfo` column is a tuple per note, and the modulator's phase is
# integrated from it rather than restarted per step, so the growl accelerates
# continuously instead of stepping between speeds. Measured across one bar of
# the first phrase the rate runs 5 -> 22 -> 65 -> 32 -> 11 Hz, without the
# note ever retriggering.
L = dict(legato=True)

PH_1 = [(0.0,  F1,  10.0, dict(lfo=(3, 5, 9, 16, 28, 20, 11, 6),
                               cut=(0.35, 1.0, 0.5, 0.95, 0.4, 1.0),
                               sync=(1.3, 2.0, 3.0, 2.2), fm=2.0, **L)),
        (10.0, F1,  6.0,  dict(lfo=(24, 38, 20, 10),
                               cut=(1.0, 0.35, 0.85, 0.45),
                               sync=(2.6, 3.8, 2.0), fm=2.8, slide=True, **L)),
        (16.0, F1,  5.0,  dict(lfo=(5, 11, 22, 36),
                               cut=(0.4, 1.0, 0.55), sync=(1.5, 2.8), fm=2.2, **L)),
        (21.0, Db1, 3.0,  dict(lfo=(30, 16, 8), cut=(1.0, 0.4, 0.8),
                               sync=(3.2, 1.8), fm=2.6, slide=True, **L)),
        (24.0, Eb1, 3.0,  dict(lfo=(9, 20, 34), cut=(0.45, 0.95, 0.5),
                               sync=(1.8, 3.0), fm=2.4, slide=True, **L)),
        (27.0, Gb1, 5.0,  dict(lfo=(40, 22, 12, 6), cut=(1.0, 0.35, 0.9, 0.4),
                               sync=(3.6, 2.0, 2.8), fm=3.0, slide=True, **L))]

PH_2 = [(0.0,  F1,  16.0, dict(lfo=(3, 4, 7, 12, 20, 32, 46, 28, 15, 8, 4, 9),
                               cut=(0.3, 0.9, 0.4, 1.0, 0.35, 0.85, 0.45, 1.0,
                                    0.4, 0.9),
                               sync=(1.2, 1.8, 2.6, 3.4, 2.2, 3.0),
                               fm=(1.6, 2.4, 3.2, 2.0), **L)),
        (16.0, F1,  7.0,  dict(lfo=(6, 14, 26, 42, 24),
                               cut=(0.4, 1.0, 0.35, 0.95),
                               sync=(1.6, 2.4, 3.6), fm=2.6, **L)),
        (23.0, Bb1, 4.0,  dict(lfo=(18, 30, 14, 7), cut=(0.95, 0.4, 0.85),
                               sync=(3.0, 1.8), fm=2.2, slide=True, **L)),
        (27.0, F1,  5.0,  dict(lfo=(8, 18, 34, 20, 10),
                               cut=(0.45, 1.0, 0.4, 0.9),
                               sync=(2.0, 3.4, 2.2), fm=2.8, slide=True, **L))]

PH_3 = [(0.0,  F1,  6.5,  dict(lfo=(4, 8, 15, 26, 40, 22),
                               cut=(0.35, 0.95, 0.45, 1.0),
                               sync=(1.4, 2.2, 3.4), fm=2.2, **L)),
        (6.5,  Ab1, 3.5,  dict(lfo=(28, 44, 20), cut=(1.0, 0.4, 0.9),
                               sync=(3.2, 1.9), fm=3.0, slide=True, **L)),
        (10.0, F1,  6.0,  dict(lfo=(7, 16, 30, 18, 9), cut=(0.5, 1.0, 0.4, 0.95),
                               sync=(1.8, 2.8, 2.0), fm=2.4, slide=True, **L)),
        (16.0, C2,  4.0,  dict(lfo=(5, 12, 24, 38), cut=(0.4, 0.95, 0.5),
                               sync=(1.5, 2.6), fm=2.0, slide=True, **L)),
        (20.0, Bb1, 4.0,  dict(lfo=(34, 18, 9, 20), cut=(1.0, 0.45, 0.85),
                               sync=(3.4, 2.0), fm=2.8, slide=True, **L)),
        (24.0, Ab1, 3.0,  dict(lfo=(10, 22, 36), cut=(0.45, 1.0, 0.4),
                               sync=(1.9, 3.0), fm=2.4, slide=True, **L)),
        (27.0, F1,  5.0,  dict(lfo=(42, 24, 12, 6), cut=(1.0, 0.35, 0.9, 0.45),
                               sync=(3.8, 2.2, 2.6), fm=3.2, slide=True, **L))]

PH_4 = [(0.0,  F1,  8.0,  dict(lfo=(2, 3, 5, 9, 16, 27, 44, 26),
                               cut=(0.3, 0.85, 0.4, 1.0, 0.35, 0.9),
                               sync=(1.2, 1.7, 2.5, 3.3), fm=(1.4, 2.2, 3.0), **L)),
        (8.0,  Gb1, 8.0,  dict(lfo=(30, 16, 8, 14, 26, 40),
                               cut=(1.0, 0.4, 0.9, 0.45, 1.0),
                               sync=(3.4, 1.9, 2.8), fm=2.8, slide=True, **L)),
        (16.0, F1,  11.0, dict(lfo=(4, 7, 13, 22, 36, 24, 13, 7, 12),
                               cut=(0.35, 0.95, 0.45, 1.0, 0.4, 0.9, 0.5),
                               sync=(1.3, 2.1, 3.1, 2.3, 3.5), fm=2.4,
                               slide=True, **L)),
        (27.0, Eb1, 5.0,  dict(lfo=(38, 20, 10, 18), cut=(1.0, 0.4, 0.85),
                               sync=(3.6, 2.0), fm=3.0, slide=True, **L))]

PHRASES = (PH_1, PH_2, PH_3, PH_4)

MID = dict(octave=24, spread=0.55, square=0.7, fold_=0.45, punch=2.8,
           transient=1.6, tilt=6.0, f_lo=220, f_hi=11500, res=3.8,
           drive=3.2, low=95, lfo_depth=0.65, smooth=0.008)


def play_riff(b, riff, gain=1.0, sub_gain=1.0):
    """place one two-bar phrase; odd bars are the second half of it"""
    if b % 2:
        return
    pat = PHRASES[(b // 2) % len(PHRASES)] if riff is None else riff
    s.place(s.pos(b), phrase(pat, 2, **MID), gain, 'bass')
    s.place(s.pos(b), subph(pat, 2), sub_gain, 'sub')


def riff_a(_=None): return PH_1
def riff_b(_=None): return PH_3
def riff_c(_=None): return PH_4


# ---- 0-15  the room ----
s.place(s.pos(0), metaldrone(midi(F1), 16 * 16, gain=0.72, seed=1), bus='atmos')
s.place(s.pos(0), voidpad([midi(n) for n in (41, 48, 53)], 16 * 16,
                          cutoff=520, gain=0.30, seed=3), bus='pad')
for b, st in ((1, 4), (3, 10), (6, 2), (9, 12), (12, 6), (14, 0)):
    s.place_echo(s.pos(b, st), sonar(4, freq=700 + 140 * (b % 3)), 0.32,
                 times=3, delay_steps=6.0, fb=0.55, bus='atmos')
s.place(s.pos(2), chatter(24, seed=5), 0.55, bus='atmos')
s.place(s.pos(10), chatter(20, seed=9), 0.45, bus='atmos')
s.place(s.pos(5), scrape(16, seed=11), 0.5, bus='fx')
s.place(s.pos(11), scrape(12, seed=13, rev_=True), 0.45, bus='fx')

# a snare arriving alone, before there is a beat for it to belong to
for b, st in ((7, 12), (13, 4), (15, 8)):
    s.place(s.pos(b, st), reverb(nsnare(6, room=0.6), 2.4, 0.55, 3600), 0.5,
            bus='fx')

s.place(s.pos(14), riser(32, gain=0.45, f0=90, f1=520), bus='fx')
s.place(s.pos(15, 12), whoosh(8, gain=0.5, rev_=True), bus='fx')

# ---- 16-31  approach ----
s.place(s.pos(16), metaldrone(midi(F1), 16 * 16, gain=0.42, seed=2), bus='atmos')
s.place(s.pos(16), voidpad([midi(n) for n in (41, 48, 53, 60)], 16 * 16,
                           cutoff=680, gain=0.26, seed=7), bus='pad')
for b in range(16, 32):
    cell = CELLS_A[b % 4]
    filt = min(1.0, (b - 16) / 12.0)
    dry = 0.30 + 0.55 * filt
    drums(b, cell, gain=dry, hats=0.55 + 0.45 * filt, ghosts=0.5, seed=b)
    if b >= 20:
        subline(b, [(0, F1, 8), (8, F1, 8)], 0.55 + 0.35 * filt)
    if b >= 24:
        g = 0.35 + 0.4 * filt
        s.place(s.pos(b), phrase(PH_1[:2], 1, **{**MID, 'f_hi': 3800}), g * 1.3, 'bass')
    if b == 31:
        s.place(s.pos(b, 12), scrape(4, seed=17), 0.5, bus='fx')
s.place(s.pos(20), sonar(6, freq=560), 0.3, bus='atmos')
s.place(s.pos(28), chatter(16, seed=19), 0.4, bus='atmos')

# ---- 32-39  build 1 ----
for b in range(32, 40):
    cell = CELLS_A[b % 4]
    drums(b, cell, gain=0.85 - 0.1 * (b - 32) / 8, hats=1.0, ghosts=0.7, seed=b)
    subline(b, [(0, F1, 8), (8, F1, 8)], 0.8 * (1 - (b - 32) / 12))
s.place(s.pos(32), riser(8 * 16, gain=0.55, f0=140, f1=1900), bus='fx')
s.place(s.pos(36), voidpad([midi(n) for n in (53, 60, 65)], 4 * 16,
                           cutoff=2600, gain=0.22, seed=23), bus='pad')
roll(s, 38, 0, 8, spacing=2.0, gain=0.55, seed=1)
roll(s, 39, 0, 8, spacing=1.0, gain=0.7, accel=False, seed=2)
roll(s, 39, 8, 6, spacing=0.5, gain=0.85, accel=True, seed=3)
s.place(s.pos(39, 12), whoosh(4, gain=0.6), bus='fx')
# the last beat is empty on purpose; the drop lands on a rested ear
s.place(s.pos(40) - int(2.2 * STEP), subdrop(6, f0=110, f1=30, gain=0.7), bus='fx')

# ---- 40-71  DROP 1 ----
for b in range(40, 72):
    i = b - 40
    drums(b, CELLS_A[i % 4], seed=b)
    play_riff(b, None)
    if i % 8 == 7:
        s.place(s.pos(b, 14), scrape(2, seed=b), 0.4, bus='fx')
    if i % 16 == 15:
        roll(s, b, 12, 6, spacing=0.6, gain=0.7, accel=True, seed=b % 3)
s.place(s.pos(40), crash808(24, gain=0.5), bus='fx')
s.place(s.pos(40), impact(20, gain=0.5), bus='fx')
s.place(s.pos(56), crash808(16, gain=0.35), bus='fx')
for b in (44, 52, 60, 68):
    s.place(s.pos(b, 15), sonar(3, freq=880), 0.25, bus='atmos')
s.place(s.pos(48), voidpad([midi(n) for n in (53, 60, 65)], 16 * 8,
                           cutoff=900, gain=0.16, seed=29), bus='pad')

# ---- 72-87  breakdown: the only chords in the track ----
s.place(s.pos(71, 12), downlifter(12, gain=0.55), bus='fx')
s.place(s.pos(72), metaldrone(midi(F1), 16 * 16, gain=0.4, seed=31), bus='atmos')
for i, ch in enumerate(CHORDS):
    b = 72 + i * 4
    s.place(s.pos(b), voidpad([midi(n) for n in ch], 4 * 16, cutoff=1500,
                              gain=0.30, seed=37 + i), bus='pad')
    s.place(s.pos(b), pad([midi(n + 12) for n in ch], 4 * 16, cutoff=2600,
                          gain=0.10, wide=1.4), bus='pad')

MOTIF = [[(0, C5, 2.5), (3, Ab4, 1.5), (6, Db5, 2.5), (10, C5, 3.5), (14, Ab4, 2)],
         [(0, Bb4, 2.5), (3, F4, 1.5), (6, Ab4, 2.5), (10, Gb4, 5.0)],
         [(0, C5, 2.5), (3, Ab4, 1.5), (6, Eb5, 2.5), (10, Db5, 3.5), (14, C5, 2)],
         [(0, Ab4, 2.0), (4, Gb4, 2.0), (8, F4, 6.0)]]
for i in range(4):
    b = 72 + i * 4
    for j, (st, note, dur) in enumerate(MOTIF[i % 4]):
        s.place(s.pos(b + 2, st), glass(midi(note), dur, gain=0.55), bus='music')
        if j == 0:
            s.place_echo(s.pos(b + 2, st), glass(midi(note + 12), dur * 0.5, gain=0.18),
                         1.0, times=3, delay_steps=3.0, fb=0.5, bus='music')

for i, b in enumerate((72, 76, 80, 84)):
    root = (F1, Db1, Ab1, Gb1)[i]
    s.place(s.pos(b), nsub(root, 4 * 16, decay=3.2), 0.85, bus='sub')
for b in (73, 77, 81, 85):
    s.place(s.pos(b, 8), growlmid(F2, 8, lfo=2.0, fm=2.0, f_hi=1600), 0.28, bus='bass')
for b, st in ((74, 6), (79, 2), (83, 10), (86, 4)):
    s.place_echo(s.pos(b, st), sonar(4, freq=980), 0.22, times=3, delay_steps=4.5,
                 fb=0.5, bus='atmos')
s.place(s.pos(76), chatter(24, seed=41), 0.4, bus='atmos')
s.place(s.pos(84), nsnare(8, room=0.7), 0.35, bus='fx')

# ---- 88-95  build 2 ----
for b in range(88, 96):
    i = b - 88
    drums(b, CELLS_B[i % 4], gain=0.5 + 0.4 * i / 8, hats=0.8, ghosts=0.6, seed=b)
    subline(b, [(0, F1, 8), (8, F1, 8)], 0.5)
    s.place(s.pos(b), voidpad([midi(n) for n in CHORDS[i % 4]], 16,
                              cutoff=1400 + 260 * i, gain=0.18, seed=43 + i), bus='pad')
s.place(s.pos(88), riser(8 * 16, gain=0.6, f0=150, f1=2400), bus='fx')
roll(s, 94, 0, 8, spacing=2.0, gain=0.55, seed=4)
roll(s, 95, 0, 8, spacing=1.0, gain=0.72, seed=5)
roll(s, 95, 8, 7, spacing=0.5, gain=0.9, accel=True, seed=6)
s.place(s.pos(95, 12), whoosh(4, gain=0.65), bus='fx')
s.place(s.pos(96) - int(2.2 * STEP), subdrop(6, f0=120, f1=28, gain=0.75), bus='fx')

# ---- 96-127  DROP 2 ----
for b in range(96, 128):
    i = b - 96
    drums(b, CELLS_B[i % 4], seed=b)
    play_riff(b, PHRASES[((b // 2) + 1) % 4])
    if i % 8 == 3:
        s.place(s.pos(b, 15), screech(Gb3, 1.5, r0=2.4, r1=9.0), 0.3, bus='bass')
    if i % 16 == 15:
        roll(s, b, 13, 5, spacing=0.5, gain=0.75, accel=True, seed=b % 3)
s.place(s.pos(96), crash808(24, gain=0.5), bus='fx')
s.place(s.pos(96), impact(20, gain=0.55), bus='fx')
s.place(s.pos(112), crash808(16, gain=0.35), bus='fx')
for b in range(100, 128, 8):
    s.place(s.pos(b), stab(tuple(midi(n) for n in (65, 68, 72)), 2.0, gain=0.30), bus='music')
    s.place(s.pos(b, 6.5), stab(tuple(midi(n) for n in (66, 70, 73)), 1.6, gain=0.22), bus='music')
s.place(s.pos(104), voidpad([midi(n) for n in (53, 60, 66)], 16 * 8, cutoff=1100,
                            gain=0.14, seed=47), bus='pad')

# ---- 128-139  bridge: halftime, the machine idles ----
s.place(s.pos(127, 12), downlifter(10, gain=0.5), bus='fx')
s.place(s.pos(128), metaldrone(midi(F1), 12 * 16, gain=0.45, seed=53), bus='atmos')
s.place(s.pos(128), voidpad([midi(n) for n in (41, 48, 54)], 12 * 16, cutoff=760,
                            gain=0.24, seed=59), bus='pad')
for b in range(128, 140):
    i = b - 128
    for st in (0,):
        t = s.pos(b, st)
        s.place(t, nkick(), 0.95, 'drums'); s.hit(t)
    if i % 2 == 0:
        t = s.pos(b, 10)
        s.place(t, nkick(), 0.8, 'drums'); s.hit(t)
    s.place(s.pos(b, 8), nsnare(6, room=0.5), 0.95, 'drums')     # halftime backbeat
    for st, g in ((2, 0.4), (6, 0.5), (11, 0.35), (14, 0.45)):
        s.place(s.pos(b, st + rs.randn() * 0.02), nghost(seed=i % 4), g * 0.5, 'drums')
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), nhat(open_=(st == 6), seed=i % 4), 0.35, 'drums')
    s.place(s.pos(b), dust(16, seed=b), 0.5, 'texture')
    subline(b, [(0, F1, 8), (8, Gb1 if i % 4 == 3 else F1, 8)], 0.75)
    s.place(s.pos(b), phrase(PH_2[:1] if i % 4 != 3 else PH_4[1:2], 1,
                             **{**MID, 'f_hi': 6500}), 0.75, 'bass')
    if i % 4 == 3:
        s.place(s.pos(b, 12), screech(F3, 3.0, r0=1.2, r1=8.5), 0.28, bus='bass')
for b, st in ((130, 4), (134, 12), (137, 6)):
    s.place_echo(s.pos(b, st), sonar(4, freq=640), 0.26, times=4, delay_steps=6.0,
                 fb=0.55, bus='atmos')
s.place(s.pos(132), chatter(20, seed=61), 0.42, bus='atmos')

# ---- 140-147  build 3 ----
for b in range(140, 148):
    i = b - 140
    drums(b, CELLS_C[i % 4], gain=0.55 + 0.4 * i / 8, hats=0.9, ghosts=0.7, seed=b)
    subline(b, [(0, F1, 8), (8, F1, 8)], 0.55)
    s.place(s.pos(b), dust(16, seed=b + 7), 0.4, 'texture')
s.place(s.pos(140), riser(8 * 16, gain=0.65, f0=160, f1=3000), bus='fx')
s.place(s.pos(144), scrape(4 * 16, seed=67), 0.45, bus='fx')
roll(s, 146, 0, 8, spacing=2.0, gain=0.6, seed=7)
roll(s, 147, 0, 8, spacing=1.0, gain=0.78, seed=8)
roll(s, 147, 8, 8, spacing=0.5, gain=0.95, accel=True, seed=9)
s.place(s.pos(147, 12), whoosh(4, gain=0.7), bus='fx')
s.place(s.pos(148) - int(2.4 * STEP), subdrop(7, f0=130, f1=27, gain=0.8), bus='fx')

# ---- 148-175  DROP 3 ----
for b in range(148, 176):
    i = b - 148
    drums(b, CELLS_C[i % 4], seed=b)
    s.place(s.pos(b), dust(16, seed=b + 3), 0.45, 'texture')
    play_riff(b, PHRASES[((b // 2) + 2) % 4])
    if i % 4 == 3:
        s.place(s.pos(b, 15), screech(F4, 1.4, r0=2.6, r1=10.0), 0.22, bus='bass')
    if i % 16 == 15:
        roll(s, b, 12, 7, spacing=0.55, gain=0.85, accel=True, seed=b % 3)
s.place(s.pos(148), crash808(28, gain=0.55), bus='fx')
s.place(s.pos(148), impact(24, gain=0.6), bus='fx')
s.place(s.pos(164), crash808(16, gain=0.4), bus='fx')
for i in range(7):
    b = 148 + i * 4
    for st, note, dur in MOTIF[i % 4]:
        s.place(s.pos(b, st), glass(midi(note), dur, gain=0.26), bus='music')
for b in range(150, 176, 4):
    s.place(s.pos(b, 6.5), stab(tuple(midi(n) for n in (65, 68, 72)), 1.6, gain=0.24),
            bus='music')

# ---- 176-191  outro ----
s.place(s.pos(175, 12), downlifter(14, gain=0.55), bus='fx')
s.place(s.pos(176), metaldrone(midi(F1), 16 * 16, gain=0.7, seed=71), bus='atmos')
s.place(s.pos(176), voidpad([midi(n) for n in (41, 48, 53)], 16 * 16, cutoff=560,
                            gain=0.28, seed=73), bus='pad')
for b in range(176, 188):
    i = b - 176
    fade = max(0.0, 1 - i / 11.0)
    drums(b, CELLS_A[i % 4], gain=0.8 * fade, hats=0.8 * fade, ghosts=0.5 * fade,
          sidechain=i < 8, seed=b)
    if i < 8:
        subline(b, [(0, F1, 8), (8, F1, 8)], 0.7 * fade)
    if i < 6:
        s.place(s.pos(b), phrase(PH_1[:2], 1, **{**MID, 'f_hi': 4200}),
                0.9 * fade, 'bass')
for b, st in ((180, 8), (184, 2), (188, 6)):
    s.place_echo(s.pos(b, st), sonar(4, freq=700), 0.3, times=4, delay_steps=6.0,
                 fb=0.55, bus='atmos')
s.place(s.pos(186), chatter(24, seed=79), 0.45, bus='atmos')
s.place(s.pos(189), scrape(12, seed=83, rev_=True), 0.4, bus='fx')

# ---- mix ----
# Space goes on the buses, not on the voices: one room for the melodic layers,
# a bigger and darker one for the atmosphere, and nothing at all on the drums
# or the bass - at 174 BPM a tail longer than a bar is fog.
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.6, wet=0.30, tone=4800)
s.bus['pad'] = bus_reverb(s.bus['pad'], decay=3.4, wet=0.34, tone=2600)
s.bus['atmos'] = bus_reverb(s.bus['atmos'], decay=4.5, wet=0.40, tone=2000)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=2.2, wet=0.22, tone=3600)
# Around 1 kHz is where a bass line stops being weight and starts being a part
# you can follow, and it is the band a phone reproduces best. Above 2.5 kHz it
# is only the kick's click and the snare's crack that matter, and the bass is
# shelved out of both - the skeleton of a drum & bass track is two hits a bar
# and they have to be the loudest thing in their own band.
# BEZDNA shelved the whole bass off above 2.6 kHz to keep the snare's crack
# clear. That works, and it also removes exactly the teeth this version
# exists for. So the carve is narrow instead of broad: one notch where the
# snare actually peaks, and presence either side of it.
s.bus['bass'] = hi_spread(s.bus['bass'], hz=420, amount=0.35)
s.bus['bass'] = peak_eq(peak_eq(s.bus['bass'], 1000, 3.0, 0.5), 2300, 3.5, 0.45)
s.bus['bass'] = peak_eq(s.bus['bass'], 3600, -5.0, 0.28)
s.bus['bass'] = (0.72 * s.bus['bass'] + 0.28 * fold(s.bus['bass'] * 1.25, 1.45))
s.bus['bass'] = peak_eq(s.bus['bass'], 520, -4.0, 0.5)
# A bass loud enough to be aggressive will cover the backbeat, and the fix is
# time, not frequency: it steps out of the way for 60 ms on every snare the
# way it already does on every kick. Carving the crack band out of the bass
# instead would take back the teeth this version is for.
s.bus['bass'] = s.bus['bass'] * duck_env(s.total, SNARES, depth=0.46,
                                         hold=0.006, release=0.075)[:, None]
s.bus['sub'] = mono_below(s.bus['sub'], 200)
# The kick and the sub cannot both own 40-60 Hz. The kick keeps its punch band
# and the transient; the sine underneath it belongs to the bass.
s.bus['drums'] = peak_eq(shelf(hp(s.bus['drums'], 42, order=2), 5200, 1.0, 'high'),
                         1900, 2.5, 0.5)
s.bus['atmos'] = hp(s.bus['atmos'], 34, order=2)

GAINS = {'drums': 0.57, 'sub': 0.30, 'bass': 0.3, 'texture': 0.42,
         'music': 1.90, 'pad': 1.30, 'atmos': 0.46, 'fx': 0.24}
s.report(GAINS)
s.render('neuro_zuby_174.wav', drive=1.25, duck=0.30, limit=0.82, peak=0.90,
         gains=GAINS, clip=0.86, fade=2.0)
