"""CHETYRE UTRA - party hardstyle at 154 BPM in A minor. Four in the morning,
the room is finished, and the only thing that will get it back up is a kick on
every single beat with something screaming in the gaps.

The floor is hardstyle: a tuned, distorted kick on 0/4/8/12, never once
syncopated, never once halved. The answer on the offbeat is two instruments at
the same time - a reverse saw stack swelling up into the next kick, and a
jump-up bass that tears and talks. The lead is a stack, not an oscillator, and
it is drowned: chorus in the voice, a dotted-eighth ping-pong and a bright hall
on the bus, and a sidechain deep enough that the whole top half of the mix
breathes on every beat. In this genre the effects are not a finish, they are
the instrument.

    intro | build | DROP 1 | breakdown | DROP 2 | bridge | FINAL DROP | outro
    0       8       16       48          64       96       104          144
"""
import numpy as np
from ravelib import *

np.random.seed(154)

# Everything above the bass breathes on the kick. At this depth the pump is
# not a mixing trick that hides a collision, it is an audible part.
Session.DUCKED = {'bass': 1.0, 'music': 0.9, 'pad': 1.0, 'keys': 0.55}

# ---- the material ----
# i - bIII - bVI - bVII in A minor. Rootless voicings up in the fourth octave:
# the bass owns everything below, and two common tones survive every change.
CHORDS = [[60, 64, 71], [60, 64, 67], [60, 64, 69], [59, 62, 67]]
KEYS   = [[64, 69, 72], [64, 67, 72], [65, 69, 72], [67, 71, 74]]   # piano, voice-led
KICKTUNE = [55.00, 65.41, 55.00, 49.00]                             # A1 C2 A1 G1
KICKGAIN = [1.00, 0.96, 1.00, 1.02]

# The hook, on straight eighths. Motif, sequence up a third, peak and fall,
# cadence that lands on the fifth so the loop has to come round again.
# (step, note, duration, velocity)
HOOK = [
    [(0, 69, 2, 1.00), (2, 72, 2, 0.68), (4, 76, 2, 0.88), (6, 72, 2, 0.66),
     (8, 69, 2, 0.95), (10, 72, 2, 0.70), (12, 76, 2, 0.86), (14, 81, 2, 0.80)],
    [(0, 72, 2, 1.00), (2, 76, 2, 0.68), (4, 79, 2, 0.90), (6, 76, 2, 0.66),
     (8, 72, 2, 0.95), (10, 76, 2, 0.70), (12, 79, 2, 0.88), (14, 84, 2, 0.86)],
    [(0, 81, 2, 1.00), (2, 79, 2, 0.72), (4, 76, 2, 0.86), (6, 72, 2, 0.64),
     (8, 76, 2, 0.92), (10, 79, 2, 0.72), (12, 81, 2, 1.00), (14, 79, 2, 0.74)],
    [(0, 76, 2, 0.94), (2, 74, 2, 0.66), (4, 71, 2, 0.84), (6, 74, 2, 0.64),
     (8, 76, 2, 0.92), (10, 79, 2, 0.74), (12, 76, 4, 1.00)],
]

# The bass answers on the offbeat quarters and spells the chord out while it
# does: in this half of the fusion the bass is the riff, not a rhythm part.
BASS = [
    [(2, 45, 2), (6, 45, 2), (10, 48, 2), (14, 52, 2)],   # A  A  C  E
    [(2, 48, 2), (6, 52, 2), (10, 48, 2), (14, 45, 2)],   # C  E  C  A
    [(2, 41, 2), (6, 41, 2), (10, 45, 2), (14, 48, 2)],   # F  F  A  C
    [(2, 43, 2), (6, 47, 2), (10, 45, 2), (14, 43, 2)],   # G  B  A  G
]
VOWELS = [('oo', 'ee'), ('ah', 'ee'), ('oo', 'ah'), ('ee', 'oo')]
RATIOS = [(1.4, 3.2), (1.6, 4.4), (1.3, 3.0), (1.8, 5.2)]

s = Session(152, tail=3.5)

# ---- the parts ----
def kicks(b, gain=1.0, hits=(0, 4, 8, 12), lpf=None, **kw):
    i = b % 4
    floor(s, b, tune=KICKTUNE[i], gain=gain * KICKGAIN[i], hits=hits, lpf=lpf, **kw)

def bassbar(b, gain=1.0, filth=0.0, swell=0.7, drive=4.5, sub_gain=0.18,
            saw=0.0, extra=()):
    """The offbeat answer. `saw` layers the reverse saw stack under the talking
    bass - the hardstyle half and the jump-up half of the same note.

    sub_gain is deliberately low. This swells into the kick, so a moment before
    every beat it is the loudest thing under 110 Hz unless it is kept out of
    there, and then the floor stops being the floor. The kick tail owns the
    sub; this bass owns the midrange it talks in."""
    for i, (st, note, dur) in enumerate(BASS[b % 4]):
        v0, v1 = VOWELS[i]
        r0, r1 = RATIOS[i]
        bassbite(s, b, st, note, dur, gain=gain, sub_gain=sub_gain, bus='bass',
                 v0=v0, v1=v1, r0=r0, r1=r1 * (1 + 0.35 * filth),
                 drive=drive + 2.5 * filth, swell=swell, fold_=0.3 + 0.25 * filth)
        if saw:
            s.place(s.pos(b, st), hp(revsaw(note - 12, dur, gain=saw,
                                            f_hi=1200 + 700 * filth), 150), 1.0, 'bass')
    for st, note, dur in extra:
        bassbite(s, b, st, note, dur, gain=gain * 0.85, sub_gain=sub_gain * 0.7,
                 bus='bass', v0='ah', v1='ee', r0=2.0, r1=6.0, drive=6.0, swell=0.0)

def lead(b, gain=1.0, octave=0, drive=6.5, f0=3400, f1=800, res=2.6, tear=3.2,
         sparse=False, half=False, bend=0.0, vowel='ee', chor=0.5, sub=0.30,
         bus='music'):
    """the hook on straight eighths. Each note is shorter than its step on
    purpose: butted end to end they read as one held drone, and the thing a
    room claps to is the gap."""
    notes = HOOK[b % 4]
    if sparse:
        notes = [n for n in notes if n[0] % 4 == 0]
    if half:                                   # front half only: the bass answers alone
        notes = [n for n in notes if n[0] < 8]
    for st, note, dur, vel in notes:
        hard = vel > 0.8
        # an accent is not just louder: it is longer, brighter and driven
        # harder, and it bends into pitch. That is the whole difference
        # between a line that was played and one that was entered.
        ln = min(dur, 2) * (0.84 if hard else 0.58)
        s.place(s.pos(b, st), hardlead(note + octave, ln,
                                       drive=drive * (1.0 if hard else 0.8),
                                       f0=f0 * (1.0 if hard else 0.78), f1=f1,
                                       res=res * (1.0 if hard else 0.82),
                                       tear=tear * (1.0 if hard else 0.6),
                                       bend=bend if hard else 0.0,
                                       vowel=vowel, chor=chor, sub=sub),
                gain * vel, bus)

def shimmer(b, gain=0.5, octaves=(1, 2), cycle=7, rate=1.0):
    """The top layer. A seven-step cycle over a sixteen-step bar walks: it
    starts on a different note every bar and does not come back round for
    seven, so sixteenth notes for thirty-two bars never repeat themselves."""
    seq = arp_seq(CHORDS[b % 4], bars=1, shape='updown', rate=rate, cycle=cycle,
                  octaves=octaves, ratchets=(3,), accents=(0, 4), tail=0.8,
                  rotate=b, jitter=0.012, seed=b)
    for st, note, dur, vel in seq:
        s.place(s.pos(b, st), arpvoice(midi(note), dur, wave='saw', detune=0.012,
                                       f_lo=900, f_hi=9000, res=2.2, decay=0.07),
                gain * vel, 'music')

def keys(b, gain=1.0, steps_=(2, 6, 10, 14), dur=1.9, bright=1.0):
    ch = [midi(n) for n in KEYS[b % 4]]
    for st in steps_:
        s.place(s.pos(b, st), ravepiano(ch, dur, bright=bright), gain, 'keys')

def chord(b, bars=1, gain=0.5, cutoff=4200, attack=0.3, release=0.5, sub=0.2):
    s.place(s.pos(b), supersaw([midi(n) for n in CHORDS[b % 4]], 16 * bars, gain=gain,
                               cutoff=cutoff, attack=attack, release=release, sub=sub),
            1.0, 'pad')

def reverse_in(b, note=74):
    """a reversed lead whose tail lands exactly on the downbeat of bar b"""
    seg = rev(hardlead(note, 5, drive=5.0, f0=4200, f1=1400, chor=0.6))
    s.place(s.pos(b) - len(seg), seg, 0.55, 'fx')

# ================= intro: 0-7 - the room, at four in the morning =================
for b in (0, 2, 4, 6):
    s.place(s.pos(b), crowd(32, gain=0.9, roar=0.12 * b / 6, seed=b), 1.0, 'fx')
s.place_echo(s.pos(0, 4), dubsiren(6, f0=520, lfo=2.2, gain=0.5), 1.0,
             times=3, delay_steps=3.0, fb=0.45, bus='fx')
s.place(s.pos(0), supersaw([midi(n) for n in CHORDS[0]], 64, gain=0.30, cutoff=1500,
                           attack=1.4, release=1.0), 1.0, 'pad')
for b in range(4, 8):                                   # the floor arrives filtered
    kicks(b, gain=0.5 + 0.14 * (b - 4), lpf=260 + 420 * (b - 4), bite=0.25,
          drive=4.5, tail=0.65)
    tops(s, b, gain=0.26 + 0.08 * (b - 4), claps=(), closed=False,
         open_=(2, 6, 10, 14) if b >= 5 else ())
s.place(s.pos(6), airhorn(8, note=69, gain=0.55), 1.0, 'fx')
s.place(s.pos(6), supersaw([midi(n) for n in CHORDS[2]], 32, gain=0.34, cutoff=2600,
                           attack=0.7, release=0.6), 1.0, 'pad')
s.place(s.pos(7), riser(16, gain=0.7, f0=190, f1=1200), 1.0, 'fx')

# ================= build: 8-15 =================
for b in range(8, 16):
    ph = b - 8
    kicks(b, gain=0.86 + 0.02 * ph, bite=0.6, drive=6.0, tail=0.9)
    tops(s, b, gain=0.5 + 0.05 * ph, claps=(4, 12) if b >= 12 else ())
    if b >= 10:
        for st, note, dur in BASS[b % 4]:               # the swell alone first
            s.place(s.pos(b, st), hp(revsaw(note - 12, dur, gain=0.85,
                                            f_hi=600 + 260 * (b - 10)), 150), 1.0, 'bass')
    if b >= 12:
        lead(b, gain=0.55, drive=5.0, f0=2400, f1=950, res=2.0, sparse=True, chor=0.6)
    chord(b, gain=0.30, cutoff=2600 + 260 * ph, attack=0.05, release=0.2)
s.place(s.pos(12), airhorn(10, note=76, gain=0.6), 1.0, 'fx')
s.place(s.pos(14), riser(32, gain=0.95, f0=170, f1=1800), 1.0, 'fx')
s.place(s.pos(15), crowd(16, gain=1.0, roar=0.85, seed=9), 1.0, 'fx')
s.place(s.pos(15, 8), reverse_crash(8, gain=0.95), 1.0, 'fx')
s.place(s.pos(15, 12), shout(4, note=62, gain=0.85), 1.0, 'fx')
reverse_in(16, 81)
s.place(s.pos(16), impact(20, gain=0.55), 1.0, 'fx')
s.place(s.pos(16), subdrop(10, f0=150, f1=32, gain=0.5, decay=0.55), 1.0, 'bass')

# ================= DROP 1: 16-47 =================
for b in range(16, 48):
    ph = b - 16
    big = ph >= 16                                       # second half: piano and octaves
    hits = (0, 4, 8, 12)
    if ph % 8 == 7:
        hits = (0, 4, 8, 12, 14, 15)                     # the bar-end run, quarters intact
    kicks(b, gain=1.0, hits=hits, drive=7.5, bite=1.0 + 0.25 * big)
    bassbar(b, gain=1.0, filth=0.55 if big else 0.15, saw=0.55 if big else 0.42,
            extra=((15, 45, 1),) if ph % 8 == 7 else ())
    tops(s, b, gain=0.9, ride=(0, 4, 8, 12) if big else ())
    lead(b, gain=0.85, drive=6.5, bend=0.05 if ph % 4 == 0 else 0.0)
    if big:
        lead(b, gain=0.30, octave=12, drive=4.8, f0=6000, f1=2600, res=2.0,
             vowel='ih', sub=0.0)
        keys(b, gain=0.62 if ph % 2 == 0 else 0.42)
        shimmer(b, gain=0.28)
    chord(b, gain=0.26, cutoff=5200, attack=0.02, release=0.1)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.8), 1.0, 'drums')
        s.place(s.pos(b), crowd(16, gain=0.5, roar=0.5, seed=b), 1.0, 'fx')
    if ph % 8 == 6:
        s.place(s.pos(b, 14), zap(3, f0=3200, f1=180, gain=0.4), 1.0, 'fx')
s.place(s.pos(24), airhorn(10, note=76, gain=0.6), 1.0, 'fx')
s.place(s.pos(31, 12), shout(4, note=69, gain=0.7), 1.0, 'fx')
reverse_in(32, 84)
s.place(s.pos(40), airhorn(10, note=81, gain=0.6), 1.0, 'fx')
s.place(s.pos(47, 8), whoosh(8, gain=0.9), 1.0, 'fx')
s.place(s.pos(47, 12), shout(4, note=74, gain=0.8), 1.0, 'fx')

# ================= breakdown: 48-63 =================
# The kick goes, so the clap takes the quarters over: the pulse never actually
# stops, only the weight does, and that is what makes the drop land.
s.place(s.pos(48), downlifter(16, gain=0.9), 1.0, 'fx')
s.place(s.pos(48), crowd(64, gain=0.8, roar=0.3, seed=48), 1.0, 'fx')
for b in range(48, 56):
    chord(b, gain=0.55, cutoff=4400, attack=0.25, release=0.5, sub=0.28)
    for st, note, dur, vel in HOOK[b % 4]:               # the hook, sung wide
        s.place(s.pos(b, st), supersaw([midi(note), midi(note - 12)], dur * 1.5,
                                       gain=0.30 * vel, cutoff=6200, attack=0.02,
                                       release=0.2, detune=0.017), 1.0, 'music')
    if b >= 50:
        for st in (0, 4, 8, 12):
            s.place(s.pos(b, st), clap(3.0), 0.5 + 0.06 * (b - 50), 'drums')
    if b >= 52:
        keys(b, gain=0.5, steps_=(2, 6, 10, 14))
        tops(s, b, gain=0.35, claps=(), closed=True, open_=())
for b in range(56, 64):                                  # and the floor walks back in
    ph = b - 56
    kicks(b, gain=0.62 + 0.055 * ph, lpf=None if ph >= 4 else 700 + 500 * ph,
          bite=0.35 + 0.11 * ph, drive=5.5 + 0.3 * ph, tail=0.75 + 0.03 * ph)
    tops(s, b, gain=0.55 + 0.06 * ph, claps=(4, 12))
    s.place(s.pos(b), gate(supersaw([midi(n) for n in CHORDS[b % 4]], 16, gain=0.58,
                                    cutoff=4600 + 200 * ph, attack=0.02, release=0.05),
                           1.0, duty=0.5), 1.0, 'pad')
    keys(b, gain=0.5)
    if ph >= 4:
        bassbar(b, gain=0.7 + 0.1 * (ph - 4), filth=0.2, sub_gain=0.16, saw=0.4)
        lead(b, gain=0.55 + 0.09 * (ph - 4), drive=5.5, f0=2800, f1=900, res=2.2)
s.place(s.pos(60), riser(64, gain=1.0, f0=160, f1=2100), 1.0, 'fx')
s.place(s.pos(62), crowd(32, gain=1.0, roar=1.0, seed=62), 1.0, 'fx')
kickroll(s, 63, (8, 10, 12, 13, 14), tune=55.0, climb=0.10, gain=0.95,
         bite=1.1, dur_steps=2.0, hold=0.62)
s.place(s.pos(63, 8), reverse_crash(8, gain=1.0), 1.0, 'fx')
s.place(s.pos(63, 14), shout(3, note=76, gain=0.95), 1.0, 'fx')
reverse_in(64, 81)
s.place(s.pos(64), impact(22, gain=0.62), 1.0, 'fx')
s.place(s.pos(64), subdrop(10, f0=160, f1=30, gain=0.55, decay=0.6), 1.0, 'bass')

# ================= DROP 2: 64-95 =================
for b in range(64, 96):
    ph = b - 64
    hits = (0, 4, 8, 12)
    if ph % 8 == 7:
        hits = (0, 4, 8, 12, 14, 15)
    elif ph % 4 == 3:
        hits = (0, 4, 8, 12, 15)
    kicks(b, gain=1.0, hits=hits, drive=8.5, bite=1.25)
    bassbar(b, gain=1.05, filth=0.8, saw=0.6, extra=((15, 45, 1),) if ph % 8 == 7 else ())
    tops(s, b, gain=0.95, ride=(0, 4, 8, 12))
    call = 16 <= ph < 24                                 # the lead takes the front half
    lead(b, gain=0.90, drive=7.0, half=call, bend=0.05 if ph % 4 == 0 else 0.0)
    lead(b, gain=0.32, octave=12, drive=4.8, f0=6200, f1=2800, res=2.0,
         vowel='ih', sub=0.0, half=call)
    lead(b, gain=0.22, octave=-12, drive=5.5, f0=1800, f1=620, res=1.8,
         vowel='oh', chor=0.3, half=call)
    keys(b, gain=0.6 if ph % 2 == 0 else 0.44)
    shimmer(b, gain=0.30 + 0.12 * call)
    chord(b, gain=0.30, cutoff=5600, attack=0.02, release=0.1)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.85), 1.0, 'drums')
        s.place(s.pos(b), crowd(16, gain=0.55, roar=0.6, seed=b), 1.0, 'fx')
    if ph % 8 == 6:
        s.place(s.pos(b, 14), zap(3, f0=3600, f1=200, gain=0.45), 1.0, 'fx')
s.place(s.pos(72), airhorn(10, note=81, gain=0.65), 1.0, 'fx')
s.place(s.pos(79, 12), shout(4, note=78, gain=0.8), 1.0, 'fx')
reverse_in(80, 76)
s.place(s.pos(88), airhorn(12, note=76, gain=0.65), 1.0, 'fx')
s.place(s.pos(95, 8), whoosh(8, gain=0.9), 1.0, 'fx')

# ================= bridge: 96-103 - four bars of air, four of runway =========
s.place(s.pos(96), downlifter(14, gain=0.9), 1.0, 'fx')
s.place(s.pos(96), crowd(64, gain=0.9, roar=0.45, seed=96), 1.0, 'fx')
for b in range(96, 100):
    chord(b, gain=0.6, cutoff=5000, attack=0.03, release=0.4, sub=0.3)
    for st in (0, 4, 8, 12):                             # the pulse survives as a clap
        s.place(s.pos(b, st), clap(3.0), 0.72, 'drums')
    keys(b, gain=0.6)
    for st, note, dur, vel in HOOK[b % 4][::2]:
        s.place(s.pos(b, st), supersaw([midi(note), midi(note - 12)], dur * 1.7,
                                       gain=0.30 * vel, cutoff=6400, attack=0.02,
                                       release=0.22, detune=0.017), 1.0, 'music')
for b in range(100, 104):
    ph = b - 100
    kicks(b, gain=0.8 + 0.06 * ph, bite=0.8 + 0.12 * ph, drive=7.0)
    tops(s, b, gain=0.7 + 0.07 * ph, claps=(4, 12))
    bassbar(b, gain=0.85 + 0.05 * ph, filth=0.5, saw=0.5)
    lead(b, gain=0.68 + 0.08 * ph, drive=6.5)
    keys(b, gain=0.55)
    shimmer(b, gain=0.28)
    s.place(s.pos(b), gate(supersaw([midi(n) for n in CHORDS[b % 4]], 16, gain=0.55,
                                    cutoff=5000, attack=0.02, release=0.05),
                           0.5 if ph >= 2 else 1.0, duty=0.5), 1.0, 'pad')
s.place(s.pos(100), riser(64, gain=1.0, f0=165, f1=2300), 1.0, 'fx')
s.place(s.pos(102), crowd(32, gain=1.0, roar=1.0, seed=102), 1.0, 'fx')
kickroll(s, 103, (8, 10, 11, 12, 13, 14, 15), tune=55.0, climb=0.14, gain=0.95,
         bite=1.15, dur_steps=1.6, hold=0.60)
s.place(s.pos(103, 8), reverse_crash(8, gain=1.0), 1.0, 'fx')
s.place(s.pos(103, 14), shout(3, note=81, gain=1.0), 1.0, 'fx')
reverse_in(104, 84)
s.place(s.pos(104), impact(24, gain=0.7), 1.0, 'fx')
s.place(s.pos(104), subdrop(12, f0=170, f1=28, gain=0.6, decay=0.7), 1.0, 'bass')

# ================= FINAL DROP: 104-143 =================
for b in range(104, 144):
    ph = b - 104
    hands = 16 <= ph < 24                                # eight bars for the hands
    hits = (0, 4, 8, 12)
    if ph % 8 == 7:
        hits = (0, 4, 8, 12, 13, 14, 15)
    elif ph % 4 == 3 and not hands:
        hits = (0, 4, 8, 12, 15)
    kicks(b, gain=1.0, hits=hits, drive=9.0, bite=1.4)
    tops(s, b, gain=1.0, ride=(0, 4, 8, 12))
    chord(b, gain=0.34, cutoff=6000, attack=0.02, release=0.1)
    shimmer(b, gain=0.34 if not hands else 0.45)
    if hands:                                            # kick stays, everything else lifts
        bassbar(b, gain=0.8, filth=0.3, sub_gain=0.22, saw=0.45)
        keys(b, gain=0.75, steps_=(0, 2, 4, 6, 8, 10, 12, 14), dur=1.7, bright=1.2)
        for st, note, dur, vel in HOOK[b % 4]:
            s.place(s.pos(b, st), supersaw([midi(note), midi(note + 12)], dur * 0.95,
                                           gain=0.19 * vel, cutoff=7500, attack=0.006,
                                           release=0.05, detune=0.02), 1.0, 'music')
    else:
        bassbar(b, gain=1.1, filth=1.0, saw=0.65,
                extra=((15, 45, 1),) if ph % 8 == 7 else ())
        lead(b, gain=0.95, drive=7.5, bend=0.06 if ph % 4 == 0 else 0.0)
        lead(b, gain=0.34, octave=12, drive=5.0, f0=6400, f1=3000, res=2.0,
             vowel='ih', sub=0.0)
        lead(b, gain=0.24, octave=-12, drive=5.5, f0=1800, f1=620, res=1.8,
             vowel='oh', chor=0.3)
        keys(b, gain=0.62 if ph % 2 == 0 else 0.46)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.9), 1.0, 'drums')
        s.place(s.pos(b), crowd(16, gain=0.6, roar=0.7, seed=b), 1.0, 'fx')
    if ph % 8 == 6:
        s.place(s.pos(b, 14), zap(3, f0=4000, f1=220, gain=0.5), 1.0, 'fx')
s.place(s.pos(112), airhorn(10, note=81, gain=0.68), 1.0, 'fx')
s.place(s.pos(119, 12), shout(4, note=81, gain=0.85), 1.0, 'fx')
reverse_in(128, 81)
s.place(s.pos(128), airhorn(12, note=76, gain=0.7), 1.0, 'fx')
s.place(s.pos(135, 12), shout(4, note=74, gain=0.85), 1.0, 'fx')
s.place(s.pos(136), airhorn(10, note=81, gain=0.65), 1.0, 'fx')

# ================= outro: 144-151 =================
s.place(s.pos(144), crash808(28, gain=0.75), 1.0, 'fx')
s.place(s.pos(144), crowd(96, gain=0.9, roar=0.5, seed=144), 1.0, 'fx')
for b in range(144, 152):
    ph = b - 144
    kicks(b, gain=0.95 - 0.11 * ph, lpf=6000 - 650 * ph, bite=0.8 - 0.09 * ph,
          drive=6.5, tail=1.0 - 0.07 * ph)
    tops(s, b, gain=0.75 - 0.09 * ph, claps=(4, 12) if ph < 4 else ())
    chord(b, gain=0.34, cutoff=4200 - 380 * ph, attack=0.04, release=0.3)
    if ph < 4:
        bassbar(b, gain=0.85 - 0.15 * ph, filth=0.3, saw=0.4)
        lead(b, gain=0.7 - 0.16 * ph, drive=5.5, f0=2800, f1=900, sparse=ph >= 2)
        keys(b, gain=0.5 - 0.1 * ph)
s.place(s.pos(151), downlifter(16, gain=0.8), 1.0, 'fx')

# ---- the space. In this genre it is not a finish, it is the instrument ----
# The lead is dry out of the voice on purpose: one dotted-eighth ping-pong and
# one bright hall, shared, put every note in the same room. Per-note reverb
# would give each stab its own room and fog the lot.
s.bus['music'] = delay(s.bus['music'], steps_=3.0, times=3, fb=0.34, ping=True,
                       damp=3200)[:s.total]
s.bus['music'] = reverb(s.bus['music'], decay=1.9, wet=0.30, tone=6800)[:s.total]
s.bus['keys'] = delay(s.bus['keys'], steps_=3.0, times=2, fb=0.26, ping=True,
                      damp=2600)[:s.total]
s.bus['keys'] = reverb(s.bus['keys'], decay=1.7, wet=0.30, tone=5800)[:s.total]
s.bus['pad'] = reverb(s.bus['pad'], decay=3.0, wet=0.34, tone=5600)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=2.6, wet=0.32, tone=5000)[:s.total]
# a room on the kit above 400 Hz only: size for the claps and hats, and none of
# it anywhere near the low end, where reverb is only ever mud
s.bus['drums'] = s.bus['drums'] + 0.16 * reverb(hp(s.bus['drums'], 400),
                                                decay=0.5, wet=1.0, tone=6000)[:s.total]
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.7)
s.bus['bass'] = peak_eq(mono_below(s.bus['bass'], 130), 420, -2.0, width=0.8)
# The reference is 71-87% side from 120 Hz up and near-mono below it. A quiet
# midrange that wide reads as bigger than a loud narrow one, and it leaves the
# centre free for the thing the track is actually built on.
for b in ('music', 'keys', 'pad', 'fx'):
    s.bus[b] = side_boost(s.bus[b], 230, 0.95)
s.bus['drums'] = side_boost(s.bus['drums'], 2500, 0.8)   # the kit's top only
s.bus['music'] = shelf(peak_eq(peak_eq(s.bus['music'], 480, -2.5, width=0.8),
                                      3000, 1.8, width=0.9), 10500, -1.5)
s.bus['drums'] = shelf(shelf(s.bus['drums'], 7000, 2.5), 14000, -2.0)
s.bus['keys'] = shelf(s.bus['keys'], 7000, 1.0)

GAINS = {'drums': 0.78, 'bass': 0.82, 'music': 0.76, 'pad': 0.40, 'keys': 0.50, 'fx': 0.52}
s.report(GAINS)
s.render('rave_chetyre_utra_154.wav', drive=1.0, duck=0.24, duck_rel=0.11,
         clip=1.20, limit=0.90, peak=0.89, fade=1.8, gains=GAINS)
