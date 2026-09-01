"""KARTRIDZH - 138 BPM in D minor. A Mega Drive, an NES and a Game Boy playing
a synthwave record.

Nothing here is a sample and nothing here is an emulation: the chips are
rebuilt from what they actually were. The bass is four-operator FM with the
modulator's envelope falling three times faster than the carrier's, so the
note is bright for sixty milliseconds and then it is not - which is a filter
sweep on a machine that has no filter. The chords are one voice changing pitch
sixty times a second, because the chip has three voices and two of them are
already spent. The drums come out of a fifteen-bit shift register. And every
parameter in the record - pitch, volume, duty, vibrato - is a staircase at
60 Hz, because that is how often the CPU got to write to the sound chip.

D minor with the seventh raised to C# on every fourth bar. The harmonic minor
V is the cadence of this entire era of game music: it is what makes a loop
sound like it is about to start again rather than like it has stopped.

    boot | A | B | break | A' | C | build | FINAL | out
    0      8   24  40      48   64  80      88      112
"""
import numpy as np
from chiplib import *

np.random.seed(138)

# ---- the material ----
# i - bVI - bIII - V, and the V is major: C# is the raised seventh and the
# only note in the record from outside the natural minor.
ROOT = [38, 34, 41, 33]                       # D2 Bb1 F2 A1 - the bass
ARPR = [62, 58, 65, 57]                       # D4 Bb3 F4 A3 - the arpeggio
CHORD = [(0, 3, 7), (0, 4, 7), (0, 4, 7), (0, 4, 7)]
BELLR = [74, 70, 77, 69]

# The bass: root, root, octave, root - the shape every driving chip bassline
# on the machine has, because octave jumps are free and chords are not.
BASS = [((0, r), (2, r), (4, r + 12), (6, r), (8, r), (10, r + 7),
         (12, r + 12), (14, r + 7)) for r in ROOT]

# The theme. Eight bars, an arch that climbs a fourth higher the second time
# round and lands on the raised seventh before it turns over.
THEME = [
    ((0, 74, 2), (2, 77, 2), (4, 81, 4), (8, 79, 2), (10, 77, 2), (12, 74, 4)),
    ((0, 77, 2), (2, 79, 2), (4, 82, 4), (8, 81, 2), (10, 79, 4), (14, 77, 2)),
    ((0, 72, 2), (2, 74, 2), (4, 77, 4), (8, 81, 2), (10, 79, 2), (12, 77, 4)),
    ((0, 76, 2), (2, 74, 2), (4, 73, 4), (8, 69, 2), (10, 73, 2), (12, 74, 4)),
    ((0, 74, 2), (2, 77, 2), (4, 81, 4), (8, 79, 2), (10, 77, 2), (12, 74, 4)),
    ((0, 77, 2), (2, 79, 2), (4, 82, 2), (6, 84, 2), (8, 86, 4), (12, 84, 4)),
    ((0, 84, 2), (2, 81, 2), (4, 79, 4), (8, 77, 2), (10, 74, 2), (12, 72, 4)),
    ((0, 73, 2), (2, 76, 2), (4, 73, 4), (8, 69, 4), (12, 74, 4)),
]

# The counter-line, on the Game Boy's wave channel. It moves where the theme
# rests, which is the only rule a counter-melody has.
COUNTER = [
    ((4, 62, 2), (6, 65, 2), (12, 69, 4)),
    ((0, 65, 2), (6, 62, 2), (12, 70, 4)),
    ((2, 60, 2), (6, 65, 2), (12, 72, 2), (14, 69, 2)),
    ((4, 61, 2), (8, 64, 2), (12, 57, 4)),
]

# A shout through the DAC. It is not a word - it is the SHAPE of one, which
# is all the eight-bit voice channel on any of these machines ever managed.
SHOUT = ((0, 2.0, 'eh', 'ee', 's', +4), (2.5, 4.0, 'ah', 'uh', 'k', -2))

# A per-frame vibrato, written the way the CPU wrote it: eight numbers on a
# loop, in steps, starting only after the note has been held a moment.
VIB = (0, 0, 0, 0, 0, 0, 0, 0) + tuple(
    round(0.35 * v, 2) for v in (0, 1, 2, 1, 0, -1, -2, -1)) * 6

# Two bars inside an eight-bar phrase repeats four times exactly. Three bars
# is coprime with the phrase, so the drums - the loudest thing in the record -
# do not come back to the same place for twenty-four bars.
KIT = {'kick':  ('x-------x-------', 'x-------x-----x-', 'x-----x-x-------'),
       'snare': ('----x-------x---', '----x-------x---', '----x-------x-+-'),
       'hat':   ('x-x-x-x-x-x-x-x-', 'x-x-x-x-x-x-x-xx', 'x-x-x-xxx-x-x-x-'),
       'ohat':  ('------------o---', '----------------', '--------o-------')}
KIT_HARD = {'kick':  ('x---x---x---x---', 'x---x--xx---x---', 'x---x---x-x-x---'),
            'snare': ('----x-------x---', '----x-------x-x-', '----x---+---x---'),
            'hat':   ('xxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxx', 'xxxxxxxx.xxxxxxx'),
            'ohat':  ('--------o-------', '----------------', '------------o---')}

FILLS = ('toms', 'roll', 'noise', 'kicks', 'roll', 'toms', 'kicks', 'noise')

s = Session(128, tail=2.5)

# ---- the parts ----
def bassbar(b, gain=1.0, fm=True, triangle=True, patch='bass', index=1.0):
    """Two chips playing one line: the Mega Drive's FM for the slap, the NES
    triangle for the weight. The triangle has no volume control, so it is the
    one part of this record whose dynamics are note length and nothing else."""
    for st, nt in BASS[b % 4]:
        t = s.pos(b, st)
        if fm:
            s.place(t, fm4(nt, 1.9, patch=patch, index=index), gain, 'bass')
        if triangle:
            s.place(t, tri(nt - 12, 1.9), gain * 0.55, 'bass')


def arpbar(b, gain=1.0, duty=0.5, rate=1, octaves=(0,), voice='pulse',
           dur=16, vol=None, vary=True):
    """`vary` walks the duty cycle on an eight-bar cycle. A chip composer had
    no filter and no reverb to vary a repeat with; the duty register was the
    tone control, and moving it is how the second half of a phrase stops being
    a copy of the first."""
    if vary:
        # a THREE-bar cycle. The phrase is eight bars long, so any variation
        # on a cycle of four or eight lines up with it and changes nothing;
        # three is coprime with eight and the pair does not come round for
        # twenty-four bars.
        duty = (0.5, 0.25, 0.125)[b % 3] if duty >= 0.5 else duty
    s.place(s.pos(b), arp(CHORD[b % 4], ARPR[b % 4], dur, duty=duty, rate=rate,
                          octaves=octaves, voice=voice, vol=vol), gain, 'arp')


def fillbar(b, gain=1.0):
    """one fill on the last bar of every eight, and never the same one twice
    in a row"""
    if b % 8 == 7:
        psgfill(s, b, FILLS[(b // 8) % 8], gain=gain)


def polytick(b, gain=0.26, period=7, bus='drums'):
    """A tick every SEVEN steps, counted from the top of the record and
    running straight through the bar lines.

    Seven and sixteen are coprime, so the pattern does not come back to the
    same place in the bar for seven bars - which means no two bars inside a
    phrase are identical however deterministic everything else is. It is the
    cheapest way there is to make a machine-exact loop stop sounding like
    one, and it costs a single quiet noise hit."""
    base = b * 16
    for i in range(16):
        if (base + i) % period == 0:
            s.place(s.pos(b, i), psghat(1, rate=17000.0, decay=0.009), gain, bus)


def theme(b, cell, gain=1.0, patch='lead', octave=0, index=1.0, vib=True,
          beat=0.0, edge=0.0, body=0.0, swell=0.0, echo=0.0, spread=0.0,
          harm=0.0, harm_step=-2, wave='organ'):
    """The tune, as a stack of chip channels rather than one.

    It grows across the record: two layers in the first chorus, four in the
    second, the full six and a harmony line in the last. That is an
    arrangement, not a mix decision - the melody has to have somewhere to go,
    and on a machine with six channels the only thing you can spend on it is
    more channels.

    The harmony is built with `scale_step`, so it is a diatonic third (or a
    sixth) and not a fixed transposition. On the V bar the seventh is C#, and
    a parallel-transposed harmony would put a C against it."""
    sc = DMIN_V if cell % 4 == 3 else DMIN
    for st, nt, ln in THEME[cell % 8]:
        p = VIB[:nframes(ln)] if vib else None
        leadnote(s, s.pos(b, st), nt, ln * 0.95, gain=gain, patch=patch,
                 index=index, pitch=p, beat=beat, edge=edge, body=body,
                 swell=swell, echo=echo, spread=spread, octave=octave,
                 wave=wave)
        if harm:
            hn = scale_step(nt + octave, harm_step, sc)
            s.place(s.pos(b, st), fm4(hn, ln * 0.95, patch=patch,
                                      index=index * 0.85, pitch=p),
                    gain * harm, 'harm')


def counter(b, gain=1.0, wave='organ', octave=0):
    for st, nt, ln in COUNTER[b % 4]:
        s.place(s.pos(b, st), wavech(nt + octave, ln * 0.95,
                                     table=tuple(WAVES[wave])), gain, 'wave')


def bells(b, gain=1.0, steps_=(0, 6, 10), octave=0):
    for st in steps_:
        s.place(s.pos(b, st), fm4(BELLR[b % 4] + octave, 6, patch='bell'),
                gain, 'bell')


_SHOUT = None


def shout(b, st=0.0, gain=1.0, note=50):
    global _SHOUT
    if _SHOUT is None:
        _SHOUT = dac(speak(SHOUT, 12, note=note, seed=5), bits=8, sr_div=4)
    s.place(s.pos(b, st), _SHOUT, gain, 'vox')


# ================= boot: 0-7 =================
# The chime a cartridge played before the game started: one FM bell, one
# arpeggio, and the machine's noise floor.
s.place(s.pos(0), fm4(74, 12, patch='bell', gain=1.1), 0.9, 'bell')
s.place(s.pos(0, 6), fm4(81, 14, patch='bell', gain=1.0), 0.8, 'bell')
s.place(s.pos(2), fm4(86, 16, patch='bell', gain=0.9), 0.7, 'bell')
for b in range(4, 8):
    arpbar(b, gain=0.42 + 0.10 * (b - 4), duty=0.25,
           vol=tuple(framecurve(nframes(16), 0.55, 0.85)))
    if b >= 6:
        psgline(s, b, KIT, gain=0.55 + 0.15 * (b - 6))
        bassbar(b, gain=0.55, index=0.7)
s.place(s.pos(7, 8), zap(8, gain=0.6, rate0=26000, rate1=1200), 1.0, 'fx')

# ================= A: 8-23 =================
for b in range(8, 24):
    ph = b - 8
    psgline(s, b, KIT, gain=0.95)
    fillbar(b, 0.85)
    polytick(b)
    bassbar(b, gain=1.0, index=0.9 + 0.02 * ph)
    arpbar(b, gain=0.60, duty=(0.25, 0.125, 0.25, 0.5, 0.125)[b % 5])
    if ph >= 4:
        theme(b, ph - 4, gain=0.72, index=1.0, edge=0.30 + 0.02 * ph)
    if ph >= 8:
        counter(b, gain=0.42)
shout(8, gain=0.70)
shout(16, gain=0.62)
s.place(s.pos(23, 12), zap(4, gain=0.55, rate0=22000, rate1=3000), 1.0, 'fx')

# ================= B: 24-39 - the machine opens up =================
for b in range(24, 40):
    ph = b - 24
    psgline(s, b, KIT_HARD, gain=1.0)
    fillbar(b, 0.90)
    polytick(b)
    s.place(s.pos(b), dackick(3), 0.5, 'drums')
    s.place(s.pos(b, 8), dackick(3), 0.42, 'drums')
    bassbar(b, gain=1.05, index=1.15)
    arpbar(b, gain=0.66, duty=0.5, rate=1,
           octaves=((0, 1) if b % 5 else (0, 1, 0, 2)) if ph >= 8 else (0,))
    theme(b, ph, gain=0.74, index=1.25, patch='lead', beat=0.55,
          edge=0.42, body=0.30, spread=0.25)
    counter(b, gain=0.50, wave='reed' if ph >= 8 else 'organ')
    if ph % 4 == 3:
        bells(b, gain=0.34, steps_=(12,))
shout(24, gain=0.70)
shout(32, st=8.0, gain=0.66)
s.place(s.pos(31, 12), zap(4, gain=0.6, rate0=20000, rate1=2500), 1.0, 'fx')

# ================= break: 40-47 - the DAC talks =================
for b in range(40, 48):
    ph = b - 40
    arpbar(b, gain=0.52 + 0.04 * ph, duty=0.125,
           vol=tuple(framecurve(nframes(16), 0.5, 0.9)))
    bells(b, gain=0.40, steps_=(0, 8), octave=12 if ph % 2 else 0)
    if ph >= 2:
        counter(b, gain=0.46, wave='vox')
    if ph >= 4:
        psgline(s, b, KIT, gain=0.55 + 0.12 * (ph - 4))
        bassbar(b, gain=0.70 + 0.08 * (ph - 4), fm=ph >= 5, index=0.8)
for b, st, g in ((40, 0.0, 0.80), (42, 4.0, 0.72), (44, 0.0, 0.78), (46, 6.0, 0.85)):
    shout(b, st=st, gain=g)
s.place(s.pos(47), zap(12, gain=0.7, rate0=3000, rate1=24000, frames=24), 1.0, 'fx')
s.place(s.pos(47, 12), psgsnare(2, gain=0.9), 1.0, 'drums')
s.place(s.pos(47, 13), psgsnare(2, gain=0.95), 1.0, 'drums')
s.place(s.pos(47, 14), psgsnare(2, gain=1.0), 1.0, 'drums')
s.place(s.pos(47, 15), psgsnare(2, gain=1.05), 1.0, 'drums')

# ================= A': 48-63 - the theme an octave up =================
for b in range(48, 64):
    ph = b - 48
    psgline(s, b, KIT_HARD, gain=1.02)
    fillbar(b, 0.92)
    polytick(b)
    s.place(s.pos(b), dackick(3), 0.52, 'drums')
    bassbar(b, gain=1.06, index=1.2)
    arpbar(b, gain=0.68, duty=0.5,
           octaves=(0, 1) if b % 5 else (0, 1, 0, 2))
    theme(b, ph, gain=0.74, octave=12 if ph < 8 else 0, index=1.35,
          patch='lead' if ph < 8 else 'brass', beat=0.55, edge=0.40,
          body=0.32, echo=0.38, spread=0.45)
    counter(b, gain=0.52, wave='reed')
    if ph % 2 == 1:
        bells(b, gain=0.30, steps_=(4, 12))
shout(56, gain=0.70)

# ================= C: 64-79 - the bridge, and the mode shows itself ========
# Same four chords, but the arpeggio moves to the wave channel and the theme
# gives way to a bell line, so the raised seventh is exposed on its own.
for b in range(64, 80):
    ph = b - 64
    psgline(s, b, KIT if ph < 8 else KIT_HARD, gain=0.88 + 0.02 * ph)
    fillbar(b, 0.88)
    polytick(b)
    bassbar(b, gain=0.95, triangle=ph >= 4, index=0.85, patch='pluck')
    arpbar(b, gain=0.58, voice='wave' if ph < 8 else 'pulse', duty=0.25,
           rate=2 if ph < 8 else 1)
    bells(b, gain=0.52, steps_=(0, 4, 8, 12) if ph >= 8 else (0, 8),
          octave=12 if ph >= 12 else 0)
    if ph >= 4:
        counter(b, gain=0.55, wave='vox', octave=12)
    if ph >= 8:
        theme(b, ph, gain=0.56, patch='organ', index=1.0, vib=False,
              swell=0.55, body=0.40, wave='vox', spread=0.35)
s.place(s.pos(71, 12), zap(4, gain=0.55, rate0=18000, rate1=2200), 1.0, 'fx')

# ================= build: 80-87 =================
for b in range(80, 88):
    ph = b - 80
    psgline(s, b, KIT_HARD, gain=0.95 + 0.01 * ph)
    bassbar(b, gain=1.0, index=1.0 + 0.08 * ph)
    arpbar(b, gain=0.62 + 0.03 * ph, duty=0.125 if ph % 2 else 0.25,
           octaves=(0, 1, 2) if ph >= 4 else (0, 1))
    theme(b, ph, gain=0.62 + 0.025 * ph, index=1.2 + 0.1 * ph,
          beat=0.5, edge=0.30 + 0.05 * ph, body=0.28, spread=0.30)
    counter(b, gain=0.50)
    if ph >= 4:
        for st in (0, 4, 8, 12):
            s.place(s.pos(b, st), dackick(3), 0.5, 'drums')
shout(80, gain=0.72)
shout(84, gain=0.76)
s.place(s.pos(86), zap(16, gain=0.75, rate0=2500, rate1=26000, frames=30),
        1.0, 'fx')
for i, st in enumerate((8, 10, 12, 13, 14, 15)):
    s.place(s.pos(87, st), psgsnare(2, gain=0.75 + 0.06 * i), 1.0, 'drums')

# ================= FINAL: 88-111 =================
for b in range(88, 112):
    ph = b - 88
    psgline(s, b, KIT_HARD, gain=1.06)
    fillbar(b, 0.95)
    polytick(b)
    s.place(s.pos(b), dackick(3), 0.55, 'drums')
    s.place(s.pos(b, 8), dackick(3), 0.46, 'drums')
    bassbar(b, gain=1.10, index=1.35)
    arpbar(b, gain=0.72, duty=0.5,
           octaves=(0, 1) if b % 5 else (0, 1, 2, 1))
    theme(b, ph, gain=0.78, index=1.45, octave=12 if 8 <= ph < 16 else 0,
          patch='brass' if 16 <= ph < 20 else 'lead', beat=0.60, edge=0.44,
          body=0.34, swell=0.26, echo=0.40, spread=0.55,
          harm=0.62 if ph >= 4 else 0.0, harm_step=-5 if ph >= 16 else -2)
    counter(b, gain=0.56, wave='reed', octave=12 if ph >= 16 else 0)
    bells(b, gain=0.34, steps_=(0, 8) if ph % 2 == 0 else (4,))
for b in (88, 96, 104):
    shout(b, gain=0.76)
s.place(s.pos(103, 12), zap(4, gain=0.6, rate0=22000, rate1=2600), 1.0, 'fx')

# ================= outro: 112-127 =================
for b in range(112, 128):
    ph = b - 112
    if ph < 8:
        psgline(s, b, KIT_HARD if ph < 4 else KIT, gain=1.0 - 0.09 * ph)
        bassbar(b, gain=1.0 - 0.10 * ph, index=1.2 - 0.08 * ph)
        theme(b, ph, gain=0.72 - 0.08 * ph, index=1.3 - 0.10 * ph,
              beat=max(0.55 - 0.09 * ph, 0), edge=max(0.40 - 0.07 * ph, 0),
              body=max(0.32 - 0.05 * ph, 0), echo=max(0.36 - 0.06 * ph, 0),
              spread=0.45)
        counter(b, gain=0.50 - 0.05 * ph)
    arpbar(b, gain=max(0.62 - 0.055 * ph, 0.0), duty=0.25,
           vol=tuple(framecurve(nframes(16), max(0.9 - 0.07 * ph, 0.0),
                                max(0.85 - 0.07 * ph, 0.0))))
    if ph >= 8:
        bells(b, gain=max(0.42 - 0.05 * (ph - 8), 0.0), steps_=(0, 8))
shout(120, gain=0.55)
s.place(s.pos(124), fm4(74, 32, patch='bell', gain=1.0), 0.7, 'bell')
s.place(s.pos(124), fm4(62, 32, patch='bell', gain=0.9), 0.6, 'bell')

# ---- the machine's output stage ----
# One filter for the whole chip, because the C64 had exactly one and all
# three voices went through it. It opens across the intro and closes across
# the outro, and it is the only continuous automation in the record - the
# machine had a knob on it, and everything else was written in frames.
for bus in ('arp', 'lead', 'wave', 'bell'):
    sweep_bars(s.bus[bus], 0, 8, 700, 16000, curve=0.7)
    sweep_bars(s.bus[bus], 120, 128, 16000, 900, curve=1.0)

s.bus['drums'] = squash(s.bus['drums'], thresh=0.30, ratio=5.0, attack=0.012,
                        release=0.109, mix=0.7, report='drums')
s.bus['bass'] = mono_below(s.bus['bass'], 130)
s.bus['arp'] = widen(s.bus['arp'], 1.1)
s.bus['wave'] = panned(s.bus['wave'], 0.35)
s.bus['bell'] = s.bus['bell'] + reverb(s.bus['bell'], decay=2.0, wet=0.30,
                                       tone=6000)[:s.total]
s.bus['lead'] = s.bus['lead'] + reverb(s.bus['lead'], decay=1.3, wet=0.16,
                                       tone=5600)[:s.total]
s.bus['harm'] = panned(s.bus['harm'], 0.42)
s.bus['harm'] = s.bus['harm'] + reverb(s.bus['harm'], decay=1.3, wet=0.16,
                                       tone=5400)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=1.6, wet=0.24, tone=5200)[:s.total]
s.bus['vox'] = s.bus['vox'] + reverb(s.bus['vox'], decay=1.1, wet=0.18,
                                     tone=4800)[:s.total]
for name in s.bus:
    s.bus[name] = console(s.bus[name], ladder_=0.005, tone=15000, drive=1.10)

# The shout and the lasers are the two things anyone remembers about a
# cartridge; at -46 LUFS they were furniture.
GAINS = {'drums': 0.78, 'bass': 0.66, 'arp': 0.44, 'lead': 0.40,
         'harm': 0.30, 'wave': 0.36, 'bell': 0.36, 'vox': 0.74, 'fx': 0.62}
s.report(GAINS)
s.render('chip_kartridzh_138.wav', drive=0.55, duck=0.14, clip=1.35,
         limit=0.90, peak=0.86, fade=1.4, gains=GAINS)
