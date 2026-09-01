"""FINSTERNIS - dark acid techno at 142 BPM, D# minor / D# Phrygian.

Finsternis is darkness, and it is also the word for an eclipse - the light
being taken away rather than merely absent. That is the opposite of
`blendung`, which is the dazzle, and the two records are built from opposite
decisions in the same room.

There are four records with a 303 in them here already, and the way this one
avoids being the fifth is not tempo or key. It is register, twice over. Every
acid line in this project so far high-passes itself at 165-240 Hz on the
principle that the sub belongs to the kick - correct when the 303 is a hook
riding over a bassline. Here there is no bassline. The 303 IS the bass: it
sits at D#2 with the filter resting below 150 Hz, and what the room feels is
a resonant peak crawling around in the low harmonics. `deepacid()` is that
instrument, and it measures 15% in 60-120 Hz and 62% in 120-300 where the old
one measures 0% and 8%. And the whole record sits at Eb1 - 38.89 Hz, three
semitones under the previous draft and the lowest root in the catalogue,
which puts 43% of the kick's energy in 20-40 Hz where a body feels it rather
than hears it.

The mode is the other half, and it is the half that actually carries the
dark. In equal temperament a key name is not a colour - every key is a
transposition of every other, and "the character of Eb minor" is a myth left
over from unequal temperaments. What is not a myth is WHICH DEGREES SOUND.
The first draft of this line was root, fifth and octave with the b2 passing
through on a slide, which is a powerful shape, not a dark one - the perfect
fifth is the most stable interval there is and the octave is confirmation.
So the fifth is nearly gone from these patterns. What is left is the b2, the
b3 and the b6, the b2 lands ON beats instead of sliding past them, and in the
umbra and the last section the fifth flattens to the b5 - one note, and D#
Phrygian becomes D# Locrian, which is a tritone standing on the kick and is
as dark as tonal music gets. The two chords are i and the Neapolitan bII:
the Phrygian cadence, and the only harmony in the record.

Nothing from the machine hall is in it. No anvils, no drop forge, no steam,
no stepper motors, no chains, no siren - the industrial palette is the other
half of this module and none of it is here. What is here is a 909, a 303, a
drone and the space between them.

The shape is an eclipse, and it is written in the spectrum rather than in the
level. The band from 2.5 to 6 kHz - presence, definition, the band an ear
reads as "bright" - is EMPTY for the first hundred and forty-four bars. Not
quiet: empty. The hats are dark, the acid never opens past a third, and in
KERNSCHATTEN even the hats go. That is what makes the last quarter possible:
you cannot open a band that was never closed.

    DAEMMERUNG | ERSTE | ZWEITE | VERDUNKLUNG | KERNSCHATTEN | RING
               | RUECKKEHR | ZWEITER SCHATTEN | FINSTERNIS (48) | AUSTRITT

256 bars, 7:13. The darkest spectrum is bar 96; the quietest bar is 187; the
peak starts at bar 192, which is 75% of the way through.
"""
import numpy as np
from industriallib import *

set_tempo(142)
np.random.seed(1420)

ROOT = 38.89                                    # Eb1 - the kick and the floor
Session.DUCKED = {'acid': 0.55, 'ghost': 0.62, 'rumble': 0.92, 'sub': 0.45,
                  'room': 0.75, 'music': 0.60, 'air': 0.45, 'bass': 1.0}

# D# Phrygian from D#2 = MIDI 39 (77.78 Hz): D# E F# G# A# B C#.
# Degrees, and how much each is used here:
#   39 D#  the root                     - everywhere
#   40 E   the b2, the Phrygian knife   - on beats, not sliding past them
#   42 F#  the b3                       - the mode's floor
#   44 G#  the 4                        - passing
#   45 A   the b5, the TRITONE          - the Locrian inflection, dark sections only
#   46 A#  the 5                        - almost never: it is the stabiliser
#   47 B   the b6, dark-sweet           - the second most used note here
#   49 C#  the b7                       - falling
#   51 D#  the octave
A_ = [(0, 39, 2, 1, 0), (2, 39, 1, 0, 0), (3, 40, 1.5, 0, 1), (5, 39, 1, 0, 0),
      (6, 42, 2, 0, 0), (8, 39, 2, 1, 0), (10, 47, 1, 0, 0), (11, 39, 1, 0, 0),
      (13, 40, 1.5, 0, 1), (15, 39, 1, 0, 0)]
B_ = [(0, 39, 1.5, 1, 0), (2, 42, 1, 0, 0), (3, 39, 1, 0, 0), (4, 40, 1, 0, 0),
      (5, 51, 1.5, 1, 1), (7, 39, 1, 0, 0), (8, 40, 1.5, 0, 0), (10, 47, 1, 0, 1),
      (11, 42, 1, 0, 0), (12, 44, 1, 0, 0), (13, 39, 1, 0, 0), (14, 42, 2, 1, 0)]
# C_ carries the tritone: the fifth is gone and an A natural stands in its
# place. It is the last figure to arrive and it does not leave.
C_ = [(0, 39, 1, 1, 0), (1, 39, 1, 0, 0), (2, 40, 1, 0, 1), (3, 39, 1, 0, 0),
      (4, 51, 1.5, 1, 0), (6, 47, 1, 0, 0), (7, 45, 1, 0, 0), (8, 39, 1, 1, 0),
      (9, 42, 1, 0, 0), (10, 49, 1.5, 0, 1), (12, 47, 1, 0, 0), (13, 44, 1, 0, 0),
      (14, 39, 2, 1, 0)]
D_ = [(0, 39, 1, 1, 0), (2, 47, 1.5, 0, 1), (4, 39, 1, 0, 0), (5, 40, 1, 0, 0),
      (6, 39, 1.5, 1, 0), (8, 45, 1, 0, 1), (9, 44, 1, 0, 0), (10, 39, 2, 0, 0),
      (13, 40, 1, 0, 1), (14, 42, 2, 1, 0)]
E_ = [(0, 39, 3, 1, 0), (4, 51, 2, 1, 1), (7, 39, 1, 0, 0), (8, 40, 3, 0, 0),
      (12, 47, 2, 1, 1), (15, 39, 1, 0, 0)]
F_ = [(0, 39, 1, 1, 0), (1, 51, 1, 0, 1), (2, 40, 1, 0, 1), (4, 39, 1, 1, 0),
      (5, 42, 1.5, 0, 0), (7, 39, 1, 0, 0), (8, 40, 1, 1, 1), (9, 39, 1, 0, 1),
      (10, 47, 1.5, 0, 0), (12, 39, 1, 1, 0), (13, 49, 1, 0, 1), (14, 42, 2, 0, 0)]
# Eleven steps against a sixteen-step bar: five steps earlier every bar, home
# on the eleventh. It is the only figure in the umbra, and it has the tritone
# in it, which is the whole reason those twenty-four bars are the darkest
# thing here.
P_ = [(0, 39, 2, 1, 0), (2, 40, 1, 0, 1), (3, 39, 1, 0, 0), (4, 45, 1.5, 0, 0),
      (6, 39, 1, 0, 0), (7, 42, 2, 1, 0), (9, 39, 1.5, 0, 0)]
FIG = (A_, B_, D_, A_, C_, E_, B_, F_, D_, C_, F_, E_)

# The kick is a part, not a constant. `задавать тему не только тарелками, а
# еще и киками` - so the pattern moves: the extra hits sit on 3, 7, 11 and 15,
# which are the steps the hats are already accenting, and the sub stays on the
# four beats so the felt pulse does not go with them.
K4  = (0, 4, 8, 12)
K4b = (0, 4, 8, 12, 15)
K4c = (0, 4, 7, 8, 12)
K5  = (0, 3, 4, 8, 12)
K6  = (0, 3, 4, 8, 11, 12)
K7  = (0, 4, 7, 8, 11, 12, 15)
K8  = (0, 2, 4, 6, 8, 10, 12, 14)

TONIC = [midi(n) for n in (39, 42, 46)]         # i   - D# minor
NEAP  = [midi(n) for n in (40, 44, 47)]         # bII - E major over a D# pedal:
                                                #       the Phrygian cadence, and the
                                                #       darkest move in the language

s = Session(256, tail=4.0)

# ---- the parts ----
@cached
def subhit(tune=ROOT, dec=0.105, dur_steps=2.6):
    n, t = steps(dur_steps)
    return (sub(tune, dur_steps) * np.exp(-t / dec)[:, None]).astype(np.float32)

def floor(b, gain=1.0, steps_=(0, 4, 8, 12), rum=1.0, subg=0.85, lpf=None,
          tune=ROOT, drive=5.8, decay=0.20, grit=0.18, rtone=128, rdecay=1.05,
          rdrive=2.5, sdec=0.105, sub_steps=None, mid=1.6, click=1.0,
          tone=7000, accent=()):
    """A 909 rather than a wall: drive 5.8 and grit 0.18 where the industrial
    records run 8-9 and 0.5. The darkness here is not distortion, it is the
    rumble - the same hit in a dark room, band-limited to the growl, ducked by
    the kick that made it."""
    subs = steps_ if sub_steps is None else sub_steps
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        acc = st in accent
        # A different seed on every hit. The click layer is a noise burst, and
        # `techkick` used to draw it from RandomState(7) every time - so all
        # four thousand kicks in a record carried bit-identical noise, which
        # the ear stops hearing as a drum and starts hearing as a tick.
        k = techkick(tune=tune, drive=drive * (1.15 if acc else 1.0),
                     decay=decay * (1.35 if acc else 1.0), grit=grit,
                     mid=mid, click=click, tone=tone, ctrack=1.0, cdecay=0.0018,
                     cseed=(b * 16 + int(st)) % 89)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain * (1.0 if not acc else 1.08), 'drums')
        if rum:
            r = rumble(dur_steps=6, tune=tune, decay=rdecay, tone=rtone, drive=rdrive)
            if lpf:
                r = lp(r, min(lpf * 1.5, 500))
            s.place(t, r, rum, 'rumble')
        if subg and st in subs:
            s.place(t, subhit(tune, sdec), subg, 'sub')

def tops(b, gain=1.0, sixteenths=True, opens=(2, 6, 10, 14), claps=(4, 12),
         clapg=0.55, tone=0.72, hatg=1.0):
    """The closed hat is `hat909` - band-passed noise, 28 ms - and for a
    closed hat that is the right instrument, because a short noise tick is
    what one is. The open hat is NOT that instrument opened out: a 200 ms
    burst of noise centred at 3-6 kHz is a rattle, and 3-6 kHz is the band a
    short bright sound hurts in. `openhat` is metal instead, it rings for
    400 ms, it sheds its top first, and it lives above 6 kHz.

    Both take a seed that changes with the bar and the step. There are
    sixteen closed hats in a bar and four thousand in the record, and until
    now every one of them was the same noise, sample for sample."""
    for st in claps:
        s.place(s.pos(b, st), lp(distclap(2.6, drive=1.5, room=0.3), 5200),
                gain * clapg, 'drums')
    if sixteenths:
        for i in range(16):
            if i % 4 == 0:
                continue
            v = 0.66 if i % 2 else 0.34
            s.place(s.pos(b, i), hat909(0.55, tone=tone, seed=(b * 16 + i) % 83),
                    gain * v * hatg, 'drums')
    for st in opens:
        s.place(s.pos(b, st),
                openhat(3.4, tone=0.85 + 0.35 * tone, hpf=4200 + 1100 * tone,
                        air=0.30 + 0.55 * tone, decay=0.22 + 0.24 * tone,
                        seed=(b * 4 + int(st)) % 71),
                gain * 0.52 * hatg, 'drums')

def rims(b, gain=1.0, steps_=(7, 15)):
    for st in steps_:
        s.place(s.pos(b, st), rim(1.0), gain * 0.5, 'drums')

def low(b0, bars, pat, gain=1.0, knob=None, cutoff=0.16, res=5.6, envmod=0.60,
        drive=4.2, f_hi=2400.0, split=105.0, sine=0.34, sub_oct=0.32, cycle=16):
    """The bass. A phrase per call, so the oscillator never restarts and the
    slides really slide, with the knob swept across the whole phrase."""
    s.place(s.pos(b0), deepacid(poly_pattern(pat, cycle, bars), dur_bars=bars,
                                knob=knob, cutoff=cutoff, res=res, envmod=envmod,
                                drive=drive, f_hi=f_hi, split=split, sine=sine,
                                sub_oct=sub_oct),
            gain, 'acid')

def ghost(b0, bars, pat, gain=1.0, knob=None, cutoff=0.28, res=6.2, envmod=0.55,
          drive=5.2, f_lo=210.0, f_hi=5400.0, oct_=12, cycle=16):
    """The same machine an octave up with no split and no sine layer, so it
    owns 800-3000 Hz and nothing below 200 - and it is fed to the room rather
    than to the mix, which is why it arrives from behind the kick instead of
    in front of it."""
    p = [(st, n + oct_, d, a, sl) for st, n, d, a, sl in poly_pattern(pat, cycle, bars)]
    s.place(s.pos(b0), deepacid(p, dur_bars=bars, knob=knob, cutoff=cutoff, res=res,
                                envmod=envmod, drive=drive, f_lo=f_lo, f_hi=f_hi,
                                split=0.0, sine=0.0, low=200.0, tame=7000.0),
            gain, 'ghost')

def stab(b, chord, gain=1.0, st=6, dur=2.0, cutoff=1200, fb=0.58, times=6):
    """The Basic Channel move: a dark detuned triad, struck short, thrown
    into a delay that filters and saturates inside its own feedback. The
    instrument is the chord plus the echo; on its own it is a dull stab."""
    seg = dubchord(tuple(chord), dur, cutoff=cutoff, drift=8.0, drive=1.5)
    s.place(s.pos(b, st), dubdelay(seg, steps_=3.0, times=times, fb=fb,
                                   damp=950, sat=1.3, spread=0.7), gain, 'room')

def air(b0, bars, drone=1.0, note=39, motor=0.2, seed=0):
    if drone:
        s.place(s.pos(b0), tunnel(bars * 16, note=note, gain=drone, motor=motor,
                                  seed=seed), 1.0, 'air')


# ================= DAEMMERUNG: 0-15 =================
# The kick is there on the first sample, and it is deliberately dull - mid at
# 1.2, no click to speak of, lowpassed. It has eight minutes to get bright,
# and it cannot do that if it starts there.
air(0, 16, drone=1.5, motor=0.22, seed=1)
# Nothing above 3 kHz exists at all for the first ten seconds, so whatever
# arrives there first arrives against absolute silence - and on the first
# pass the kick's lowpass came off and the open hat walked in on the same
# bar, which reads as a rattle starting rather than a record opening. Both
# now ramp: the filter climbs 1.4 -> 12 kHz across twelve bars and comes off
# at thirteen, and the hat fades up from a twentieth of its level.
for b in range(0, 16):
    u = b / 15
    floor(b, gain=0.90 + 0.10 * u, steps_=K4,
          lpf=1400 * (1.20 ** b) if b < 13 else None,
          rum=0.0 if b < 2 else 0.60 + 0.40 * u, subg=0.80 + 0.20 * u,
          rtone=112 + 16 * u, drive=5.2 + 0.6 * u, grit=0.05 + 0.09 * u,
          mid=1.20 + 0.25 * u, click=0.45 + 0.30 * u, tone=4400 + 220 * b)
    if b >= 6:
        s.place(s.pos(b, 14), openhat(3.0, tone=0.9, hpf=4300, air=0.34,
                                      decay=0.24 + 0.02 * (b - 6), seed=b),
                0.06 + 0.034 * (b - 6), 'drums')
for i, b0 in enumerate((4, 8, 12)):
    low(b0, 4, A_, gain=0.55 + 0.12 * i, knob=(0.06 + 0.02 * i, 0.09 + 0.02 * i),
        f_hi=1500, envmod=0.42, drive=3.4, sub_oct=0.28)

# ================= ERSTE: 16-47 =================
# Thirty-two bars in which nothing is introduced and one knob moves.
for b in range(16, 48):
    ph = b - 16
    u = ph / 31
    floor(b, gain=1.0, steps_=K4b if ph % 8 == 7 else K4, accent=(0, 8),
          rum=1.0, rtone=126 + 8 * u, drive=5.8, grit=0.18,
          mid=1.45 + 0.25 * u, click=0.80 + 0.25 * u, tone=5700 + 900 * u)
    tops(b, gain=0.62 + 0.30 * u, sixteenths=ph >= 8, tone=0.55,
         claps=(4, 12) if ph >= 8 else (), clapg=0.5,
         opens=(2, 6, 10, 14) if ph >= 16 else (6, 14))
    if ph >= 12 and ph % 2:
        rims(b, gain=0.5)
air(16, 32, drone=1.2, motor=0.18, seed=2)
for i, b0 in enumerate(range(16, 48, 8)):
    a = 0.10 + 0.05 * i
    low(b0, 8, FIG[i], gain=0.86 + 0.04 * i, knob=(a, a + 0.05),
        f_hi=1900 + 180 * i, envmod=0.48 + 0.03 * i, drive=3.6 + 0.2 * i)

# ================= ZWEITE: 48-79 =================
# The ghost - the same machine an octave up, no split and no sine, so it owns
# 800-3000 Hz and nothing under 200. Its phrases start four bars off the bass
# line's and its knob runs the other way, so the two are never doing the same
# thing. And the kick starts moving: an extra hit on the "and" of 2 every
# other bar, which is the first thing in the record that is not on a beat.
for b in range(48, 80):
    ph = b - 48
    u = ph / 31
    floor(b, gain=1.0, steps_=(K4c if ph % 4 == 2 else (K4b if ph % 8 == 7 else K4)),
          accent=(0, 8), rum=1.0, rtone=134, drive=6.0, grit=0.20,
          mid=1.70, click=0.88, tone=6600 + 600 * u)
    tops(b, gain=0.92, tone=0.55, clapg=0.55)
    if ph % 2:
        rims(b, gain=0.55)
air(48, 32, drone=1.1, motor=0.16, seed=3)
for i, b0 in enumerate(range(48, 80, 8)):
    a = 0.24 + 0.04 * i
    low(b0, 8, FIG[(4 + i) % len(FIG)], gain=0.95, knob=(a, a + 0.04),
        f_hi=2300, envmod=0.56, drive=4.0)
for i, b0 in enumerate(range(52, 80, 8)):
    ghost(b0, 8, FIG[(4 + i) % len(FIG)], gain=0.34 + 0.10 * i,
          knob=(0.40 - 0.05 * i, 0.35 - 0.05 * i), f_hi=5000 - 300 * i, drive=5.0)
stab(63, NEAP, gain=1.43, st=6, cutoff=1100)
stab(71, TONIC + [midi(51)], gain=1.29, st=14, cutoff=980)

# ================= VERDUNKLUNG: 80-95 =================
# The darkening, done to the spectrum rather than to the level: the hats lose
# their tone, the ghost's ceiling falls from 4.4 kHz to 1.6, the kick goes
# dull again, and the clap leaves.
for b in range(80, 96):
    ph = b - 80
    u = ph / 15
    floor(b, gain=1.0, steps_=K4, rum=1.0 + 0.05 * u, rtone=134 - 18 * u,
          drive=6.0, grit=0.20 - 0.10 * u, rdecay=1.05 + 0.15 * u,
          mid=1.70 - 0.40 * u, click=0.88 - 0.45 * u, tone=7200 - 2200 * u)
    tops(b, gain=0.92 - 0.55 * u, sixteenths=ph < 10, tone=0.55 - 0.20 * u,
         claps=(4, 12) if ph < 6 else (), clapg=0.5,
         opens=(6, 14) if ph < 12 else ())
air(80, 16, drone=1.4, motor=0.12, seed=4)
low(80, 8, B_, gain=0.98, knob=(0.28, 0.20), f_hi=2200, envmod=0.55, drive=4.0)
low(88, 8, D_, gain=1.0, knob=(0.20, 0.13), f_hi=1800, envmod=0.48, drive=3.8)
ghost(80, 8, B_, gain=0.49, knob=(0.30, 0.20), f_hi=4400, drive=4.8)
ghost(88, 8, D_, gain=0.35, knob=(0.20, 0.10), f_hi=2400, drive=4.4)
stab(87, NEAP, gain=1.36, st=12, cutoff=820, times=7)

# ================= KERNSCHATTEN: 96-119 =================
# The umbra. Four elements and no hats at all for twenty-four bars - this is
# what the whole first half has been closing down towards, and the reason the
# second half has anywhere to go. The line runs on an eleven-step cycle here,
# five steps earlier every bar, home on the eleventh.
for b in range(96, 120):
    ph = b - 96
    floor(b, gain=1.0, steps_=K4, rum=1.12, rtone=116, drive=5.6, grit=0.06,
          rdecay=1.25, rdrive=2.4, decay=0.215, mid=1.15, click=0.42, tone=4200)
    if ph % 4 == 3:
        s.place(s.pos(b, 14), openhat(2.6, tone=0.8, hpf=4200, air=0.22,
                                      decay=0.20, seed=b), 0.12, 'drums')
    if ph % 8 == 7:
        rims(b, gain=0.34, steps_=(15,))
air(96, 24, drone=1.7, motor=0.10, seed=5)
for i, b0 in enumerate(range(96, 120, 8)):
    a = (0.09, 0.12, 0.10)[i]
    low(b0, 8, P_, cycle=11, gain=1.0, knob=(a, a + 0.03), f_hi=1500,
        envmod=0.40, drive=3.4, res=6.0, sine=0.40, sub_oct=0.34)
stab(111, TONIC, gain=1.16, st=6, cutoff=700, times=7, fb=0.62)
stab(117, NEAP, gain=1.09, st=10, cutoff=640, times=7, fb=0.64)

# ================= RING: 120-127 =================
# Totality. Eight bars with no kick in them - the only place in the record
# where the floor stops.
s.place(s.pos(120), downlifter(16, gain=0.75), 1.0, 'fx')
air(120, 8, drone=2.0, motor=0.05, seed=6)
low(120, 8, P_, cycle=11, gain=0.92, knob=(0.16, 0.30), f_hi=2100, envmod=0.52,
    drive=3.8, sine=0.30, sub_oct=0.28)
ghost(121, 7, A_, gain=0.72, knob=(0.22, 0.42), f_hi=4400, drive=5.0)
for b, ch in ((121, TONIC), (123, NEAP), (125, TONIC), (126, NEAP)):
    stab(b, ch, gain=1.70, st=2 if b % 2 else 6, cutoff=900 + 120 * (b - 121), times=7)
for b in (124, 126):                                      # two kicks: a promise
    floor(b, gain=0.78, steps_=(0,), rum=0.85, subg=0.7, lpf=1400, rtone=118,
          mid=1.4, click=0.7)
s.place(s.pos(126), riser(32, gain=0.8, f0=140, f1=1400), 1.0, 'fx')
s.place(s.pos(127, 12), reverse_crash(6, gain=0.6), 1.0, 'fx')

# ================= AUFGANG: 128-159 =================
# Bar 128 is exactly halfway, and it is where the record stops being dark and
# starts being heavy. Everything that was closed opens at once: the kick goes
# from mid 1.15 and a 4.2 kHz ceiling to mid 2.0 and 8.5 kHz - the same
# synthesis, un-dulled - the hats go from 2.1-6.6 kHz to 3.8-12, the bass
# line's cutoff more than doubles, and the kick pattern starts moving.
for b in range(128, 160):
    ph = b - 128
    u = ph / 31
    pat = (K4, K4, K5, K4c)[(ph // 4) % 4] if ph >= 8 else K4
    floor(b, gain=1.0, steps_=pat, accent=(0, 8), rum=1.0 + 0.1 * u,
          rtone=136 + 24 * u, drive=6.2 + 0.8 * u, grit=0.12 + 0.05 * u,
          mid=1.70 + 0.35 * u, click=0.86 + 0.18 * u, tone=6400 + 900 * u,
          sdec=0.105 + 0.02 * u)
    tops(b, gain=0.70 + 0.30 * u, tone=0.62 + 0.34 * u, clapg=0.55 + 0.15 * u,
         hatg=0.85 + 0.35 * u, opens=(2, 6, 10, 14) if ph >= 8 else (6, 14))
    if ph % 2:
        rims(b, gain=0.55 + 0.12 * u)
    if ph % 16 == 15:
        kickroll(s, b, [8, 10, 12, 14], gain=0.95, tune=ROOT, drive=6.8,
                 decay=0.18, grit=0.3)
air(128, 32, drone=1.0, motor=0.2, seed=7)
for i, b0 in enumerate(range(128, 160, 8)):
    a = 0.22 + 0.09 * i
    low(b0, 8, FIG[(2 + i) % len(FIG)], gain=1.0, knob=(a, a + 0.09),
        f_hi=2400 + 320 * i, envmod=0.56 + 0.03 * i, drive=4.0 + 0.25 * i,
        res=5.6 + 0.15 * i)
for i, b0 in enumerate(range(132, 160, 8)):
    ghost(b0, 8, FIG[(2 + i) % len(FIG)], gain=0.44 + 0.07 * i,
          knob=(0.30 + 0.10 * i, 0.38 + 0.10 * i), f_hi=4600 + 500 * i,
          drive=5.0 + 0.2 * i)
s.place(s.pos(128), impact(24, gain=0.6), 1.0, 'fx')
stab(143, NEAP, gain=1.36, st=6, cutoff=1300, times=6)
stab(155, TONIC, gain=1.29, st=14, cutoff=1500, times=6)

# ================= DRUCK: 160-183 =================
# Fatter still, and now the kick is genuinely a part: K6 and K7 put hits on
# 3, 7, 11 and 15 - the steps the hats accent - while the sub stays on the
# four beats, so the pattern gets busy without the felt pulse going with it.
for b in range(160, 184):
    ph = b - 160
    u = ph / 23
    pat = (K5, K6, K4c, K7)[(ph // 2) % 4]
    floor(b, gain=1.0, steps_=pat, sub_steps=K4, accent=(0, 8), rum=1.08,
          rtone=158 + 10 * u, drive=6.8 + 0.6 * u, grit=0.15,
          mid=2.05, click=1.02, tone=7300 + 400 * u, decay=0.195)
    tops(b, gain=1.0, tone=1.0, clapg=0.70, hatg=1.15)
    rims(b, gain=0.66, steps_=(7, 15) if ph % 2 else (3, 11, 15))
    if ph % 12 == 11:
        kickroll(s, b, [0, 4, 8, 10, 12], gain=1.0, tune=ROOT, drive=7.2,
                 decay=0.18, grit=0.4)
air(160, 24, drone=0.95, motor=0.24, seed=8)
for i, b0 in enumerate(range(160, 184, 8)):
    a = 0.48 + 0.05 * i
    low(b0, 8, FIG[(6 + i) % len(FIG)], gain=1.0, knob=(a, a + 0.06, a + 0.03),
        f_hi=3000 + 300 * i, envmod=0.62, drive=4.7 + 0.2 * i, res=5.9,
        split=112.0, sine=0.30, sub_oct=0.30)
for i, b0 in enumerate(range(164, 184, 8)):
    ghost(b0, 8, FIG[(6 + i) % len(FIG)], gain=0.62 + 0.05 * i,
          knob=(0.50 + 0.06 * i, 0.58 + 0.06 * i), f_hi=5600 + 400 * i,
          drive=5.4 + 0.2 * i, res=6.4)
stab(175, NEAP, gain=1.22, st=6, cutoff=1700, times=5, fb=0.5)

# ================= SCHLAG: 184-191 =================
# Pam. Pam. Pam. Pam. Eight bars of nothing but the kick, and it is a
# different kick: the decay goes from 195 ms to 340 ms, the rumble's tail
# from 1.0 to 2.4, and every hit is accented, so each one rings into the next
# instead of stopping. Nothing else plays. The section measures six decibels
# down because there is nothing in it - which is what makes bar 192 land -
# and the kicks themselves are the loudest single events on the record.
#
# It is NOT a quiet section, and the ride does not try to make it one. A
# 340 ms kick with a 2.4 s tail four times a bar is a lot of energy, and
# pushing it down to make the loudness curve dip would be working against
# the only thing in the passage. The reset is spectral instead: everything
# above 3 kHz leaves - 0.95% here against 4.8% in the bars before it - and
# 49% of what is left sits under 60 Hz. The room does not get quieter. It
# gets narrower, and then the top comes back all at once.
s.place(s.pos(184), downlifter(8, gain=0.5), 1.0, 'fx')
air(184, 8, drone=1.3, motor=0.05, seed=9)
for b in range(184, 192):
    ph = b - 184
    u = ph / 7
    floor(b, gain=1.06, steps_=K4, accent=K4, sub_steps=K4,
          rum=1.30, subg=1.0, rtone=150, rdecay=2.4, rdrive=2.9,
          drive=8.4, decay=0.34, grit=0.14, mid=2.20, click=1.10, tone=7900,
          sdec=0.20)
    if ph >= 6:                                   # the door starts to open again
        s.place(s.pos(b, 14), openhat(3.4, tone=1.15, hpf=5200, air=0.75,
                                      decay=0.42, seed=b), 0.26 + 0.22 * u, 'drums')
for b in (184, 188):
    s.place(s.pos(b), impact(20, gain=0.55), 1.0, 'fx')
ghost(188, 4, F_, gain=0.38, knob=(0.16, 0.55), f_hi=5200, drive=5.2)
s.place(s.pos(189), riser(48, gain=0.95, f0=150, f1=2800), 1.0, 'fx')
kickroll(s, 191, [0, 4, 8, 10, 12], gain=1.0, tune=ROOT, drive=7.6, decay=0.20,
         grit=0.4, climb=0.03)
s.place(s.pos(191, 8), reverse_crash(8, gain=0.95), 1.0, 'fx')

# ================= FINSTERNIS: 192-239 =================
for b in range(192, 240):
    ph = b - 192
    u = ph / 47
    eighth = ph >= 32
    floor(b, gain=1.0 if not eighth else 1.06,
          steps_=K8 if eighth else (K6, K7, K6, K4b)[(ph // 4) % 4],
          sub_steps=K4, accent=(0, 8), rum=1.05 if not eighth else 1.02,
          subg=0.94, rtone=168, drive=7.2, grit=0.16,
          mid=2.15, click=1.08, tone=7600,
          decay=0.20 if not eighth else 0.185,
          rdecay=1.05 if not eighth else 0.95, sdec=0.11)
    tops(b, gain=1.0, tone=1.0,
         claps=(4, 12) if not eighth else (2, 6, 10, 14),
         clapg=0.74 if not eighth else 0.66, hatg=1.25 if not eighth else 1.45)
    rims(b, gain=0.7, steps_=(7, 15) if ph % 2 else (3, 11))
    if not eighth and ph % 16 == 15:
        kickroll(s, b, [0, 4, 8, 10, 12], gain=1.0, tune=ROOT, drive=7.4,
                 decay=0.18, grit=0.42)
air(192, 48, drone=0.9, motor=0.26, seed=10)
for i, b0 in enumerate(range(192, 240, 8)):
    a = 0.56 + 0.05 * i
    low(b0, 8, FIG[(9 + i) % len(FIG)], gain=1.0, knob=(a, a + 0.05, a + 0.02),
        f_hi=3200 + 260 * i, envmod=0.64, drive=4.9 + 0.18 * i, res=5.9,
        split=112.0, sine=0.30, sub_oct=0.28)
for i, b0 in enumerate(range(196, 240, 8)):
    ghost(b0, 8, FIG[(9 + i) % len(FIG)], gain=0.66 + 0.05 * i,
          knob=(0.56 + 0.06 * i, 0.62 + 0.06 * i), f_hi=6000 + 400 * i,
          drive=5.6 + 0.2 * i, res=6.4)
for b, ch in ((199, NEAP), (215, TONIC), (231, NEAP)):
    stab(b, ch, gain=1.22, st=6, cutoff=1700, times=5, fb=0.5)
s.place(s.pos(192), impact(28, gain=0.75), 1.0, 'fx')
s.place(s.pos(224), impact(24, gain=0.58), 1.0, 'fx')
s.place(s.pos(223, 12), mono_below(whoosh(4, gain=0.75), 200), 1.0, 'fx')

# ================= AUSTRITT: 240-255 =================
air(240, 16, drone=1.5, motor=0.14, seed=11)
s.place(s.pos(240), downlifter(16, gain=0.55), 1.0, 'fx')
for b in range(240, 256):
    ph = b - 240
    u = ph / 15
    floor(b, gain=1.0 - 0.62 * u, steps_=K4, lpf=9000 - 540 * ph,
          rum=1.0 - 0.5 * u, subg=0.9 - 0.55 * u, rtone=164 - 54 * u,
          drive=6.2, grit=0.14 - 0.12 * u, rdecay=1.2,
          mid=2.05 - 0.75 * u, click=1.02 - 0.85 * u, tone=7600 - 3000 * u)
    tops(b, gain=0.9 - 0.8 * u, sixteenths=ph < 8, tone=1.0 - 0.45 * u,
         claps=(4, 12) if ph < 5 else (), clapg=0.6,
         opens=(6, 14) if ph < 10 else ())
low(240, 8, B_, gain=0.9, knob=(0.5, 0.20), f_hi=2600, envmod=0.55, drive=4.2)
low(248, 4, A_, gain=0.6, knob=(0.20, 0.08), f_hi=1600, envmod=0.42, drive=3.4)
ghost(240, 6, B_, gain=0.58, knob=(0.45, 0.16), f_hi=4200, drive=4.8)
stab(247, TONIC, gain=1.50, st=6, cutoff=900, times=7, fb=0.64)
s.place(s.pos(255), downlifter(16, gain=0.5), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['ghost'] = bus_reverb(s.bus['ghost'], decay=2.8, wet=0.42, tone=3400)
s.bus['room']  = bus_reverb(s.bus['room'],  decay=3.4, wet=0.30, tone=2800)
s.bus['acid']  = bus_reverb(s.bus['acid'],  decay=0.7, wet=0.08, tone=3600)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=2.6, wet=0.30, tone=3400)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.4, wet=0.16, tone=2600)
s.bus['ghost'] = hp(s.bus['ghost'], 260)                  # the bottom is the line's
s.bus['room']  = hp(s.bus['room'], 220)
s.bus['air']   = hp(s.bus['air'], 62)                     # 20-60 is the kick's alone
s.bus['drums'] = softclip(s.bus['drums'], 1.12, knee=0.85)
s.bus['rumble'] = softclip(s.bus['rumble'], 1.05, knee=0.85)
s.bus['sub']   = softclip(s.bus['sub'], 1.0, knee=0.9)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 170)
s.bus['ghost'] = side_boost(s.bus['ghost'], 600, 0.8)
s.bus['room']  = side_boost(s.bus['room'], 500, 0.7)

ARC = [(0, -3.6), (8, -2.9), (16, -2.6), (32, -2.4), (48, -2.0), (64, -1.8),
       (79.9, -1.8), (80, -2.6), (95.9, -3.6),
       (96, -5.4), (104, -5.8), (112, -5.2), (119.9, -4.8),
       (120, -13.4), (124, -11.6), (127.9, -7.6),
       (128, -3.0), (144, -2.4), (159.9, -2.0),
       (160, -1.6), (176, -1.2), (183.9, -1.1),
       (184, -3.4), (188, -3.0), (191.4, -1.8), (191.99, -1.8),
       (192, -1.6), (208, -1.2), (223.9, -1.0), (224, 0.0), (239.9, 0.0),
       (240, -1.4), (248, -2.8), (255, -5.0), (256, -6.5)]
_bars = np.array([p[0] for p in ARC]) * BAR
_db   = np.array([p[1] for p in ARC])
_ride = 10 ** (np.interp(np.arange(s.total, dtype=np.float64), _bars, _db) / 20.0)
_ride = uniform_filter1d(_ride, int(0.030 * SR))
for b in s.bus:
    s.bus[b] = (s.bus[b] * _ride[:, None]).astype(np.float32)

GAINS = {'drums': 0.88, 'rumble': 0.46, 'sub': 0.42, 'acid': 0.56,
         'ghost': 0.62, 'room': 2.10, 'air': 0.24, 'fx': 0.30}
s.report(GAINS)
s.ownership(3000, 16000, GAINS, 'top  3-16k')
s.ownership(60, 300, GAINS, 'bass 60-300 ')
s.render('acid_finsternis_142.wav', drive=1.0, duck=0.44, duck_rel=0.18,
         clip=1.05, peak=0.95, fade=2.4, gains=GAINS,
         brick=dict(gain=1.30, ceiling=0.89))
