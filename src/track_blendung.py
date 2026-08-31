"""BLENDUNG - industrial techno at 154 BPM, A minor / A Phrygian.

Blendung is German for the dazzle - being blinded by light - and it is also
the word for a delusion. Both are correct at six in the morning in a room
where everyone is in black and wearing sunglasses indoors.

This project already has two industrial techno records and they are both
grim from the first bar to the last. Morgengrauen says so in its own
docstring: not a peak-time banger, the one after it. Measured, they agree
with each other about everything, including their faults - 1.7% and 1.0% of
their energy above 3 kHz, which on a big rig is a blanket over the whole
thing, and 13% of their sub in the side channel, which a club system that
sums the bass throws away.

So this one is built from the opposite decision in the one dimension that
matters. The machine is the same machine. What is different is that at bar
120, three minutes in, something enormous and consonant lands ON TOP of it
and the kick does not stop. Not a breakdown - an overlay. `glare()` is that
voice: a section of detuned saws that enter in pitch order thirty
milliseconds apart, wander in intonation and never come home, through the
same drive-EQ-drive-fold chain as the acid, so it is made of the record's
own distortion rather than dropped in from a trance track. It is ducked hard
by the kick, and that pumping is the emotion, not an effect on it.

One note carries the argument. The whole dark half is A Phrygian and leans on
the Bb - the b2, the knife. BLENDUNG is A Aeolian: the Bb becomes B, and the
chords are the plainest euphoric loop there is, i-bVI-bIII-bVII. Then in
VERNICHTUNG the Bb comes back, over those same chords, so the loudest and
happiest thing on the record is also the only place the two scales are
sounding at once.

    EINSTIEG | MASCHINE | DRUCK | LEERE | AUFBAU
             | BLENDUNG (48) | SCHWARZ | VERNICHTUNG (56) | AUSGANG

256 bars, 6:39. The kick is there from the first sample. The lowest point of
the record is bar 168 and the highest starts at bar 184, which is 72% of the
way through, which is where a peak belongs.
"""
import numpy as np
from industriallib import *

set_tempo(154)
np.random.seed(1541)

# ---- the material ----
ROOT   = 55.00                                  # A1 - the kick, the sub, the floor
Session.DUCKED = {'bass': 1.0, 'rumble': 0.92, 'sub': 0.45, 'acid': 0.35,
                  'glare': 0.85, 'music': 0.55, 'air': 0.45, 'pad': 0.8}

# The euphoric loop: i - bVI - bIII - bVII in A minor, two bars each.
# Voiced wide at the bottom and close at the top, and voice-led so the
# overlapping tails at each change are consonant: the top line runs
# E5 - F5 - G5 - G5, an arch, and the only semitone in the whole cycle is
# the F5 over C, which is a 4-3 suspension and wants to be there.
WALL = [tuple(midi(n) for n in ch) for ch in (
    (57, 64, 69, 72, 76),      # Am   A3 E4 A4 C5 E5
    (53, 60, 69, 72, 77),      # F    F3 C4 A4 C5 F5
    (60, 67, 72, 76, 79),      # C    C4 G4 C5 E5 G5
    (55, 62, 67, 74, 79),      # G    G3 D4 G4 D5 G5  - no third, so it is a
)]                             #      power chord, which is what techno wants

Am = [midi(n) for n in (57, 60, 64)]
Bb = [midi(n) for n in (58, 62, 65)]           # the Phrygian bII
F_ = [midi(n) for n in (57, 60, 65)]

# 303 lines, A Phrygian from A3 = 57: A Bb C D E F G.
# (step, note, dur_steps, accent, slide)
ACID_A = [(0, 57, 2, 1, 0), (2, 57, 1, 0, 0), (3, 69, 1.5, 0, 1), (5, 57, 1, 0, 0),
          (6, 60, 2, 0, 0), (8, 57, 2, 1, 0), (10, 64, 1, 0, 0), (11, 57, 1, 0, 0),
          (13, 58, 1.5, 0, 1), (15, 57, 1, 0, 0)]
ACID_B = [(0, 57, 1.5, 1, 0), (2, 64, 1, 0, 0), (3, 57, 1, 0, 0), (4, 60, 1, 0, 0),
          (5, 69, 1.5, 1, 1), (7, 57, 1, 0, 0), (8, 58, 1.5, 0, 0), (10, 65, 1, 0, 1),
          (11, 64, 1, 0, 0), (12, 60, 1, 0, 0), (13, 57, 1, 0, 0), (14, 62, 2, 1, 0)]
ACID_C = [(0, 57, 1, 1, 0), (1, 57, 1, 0, 0), (2, 58, 1, 0, 1), (3, 57, 1, 0, 0),
          (4, 69, 1.5, 1, 0), (6, 65, 1, 0, 0), (7, 64, 1, 0, 0), (8, 57, 1, 1, 0),
          (9, 60, 1, 0, 0), (10, 67, 1.5, 0, 1), (12, 64, 1, 0, 0), (13, 62, 1, 0, 0),
          (14, 57, 2, 1, 0)]
# Thirteen steps against a sixteen-step bar: it starts three steps earlier
# every bar and only comes home on the thirteenth, so thirteen bars of it are
# thirteen different bars and nothing about the notes had to change.
ACID_P = [(0, 57, 2, 1, 0), (2, 58, 1, 0, 1), (3, 57, 1, 0, 0), (4, 64, 1.5, 0, 0),
          (6, 57, 1, 0, 0), (7, 60, 2, 1, 0), (9, 57, 1, 0, 0), (10, 65, 1.5, 0, 1),
          (12, 57, 1, 0, 0)]
# Aeolian: the same hand, one note moved. Bb (58) becomes B (59).
ACID_E = [(0, 57, 2, 1, 0), (2, 64, 1, 0, 0), (3, 69, 1.5, 0, 1), (5, 64, 1, 0, 0),
          (6, 60, 2, 0, 0), (8, 57, 2, 1, 0), (10, 67, 1, 0, 0), (11, 64, 1, 0, 0),
          (13, 59, 1.5, 0, 1), (15, 57, 1, 0, 0)]

# The machine shop. Struck, not rung: low register, short decay, dark - a
# bright ringing pitched thing above C5 reads as a glockenspiel and makes a
# dark record cheerful. Two to four hits a bar, never more.
METAL = [
    [(3, 57, 0.55), (7, 53, 0.4), (11, 60, 0.5), (14, 53, 0.3)],
    [(2, 60, 0.45), (6, 57, 0.5), (10, 53, 0.4), (13, 65, 0.42), (15, 57, 0.28)],
    [(3, 53, 0.45), (6, 65, 0.4), (9, 57, 0.45), (11, 60, 0.5), (14, 53, 0.32)],
    [(3, 65, 0.5), (5, 57, 0.35), (7, 60, 0.42), (10, 53, 0.4), (15, 60, 0.45)],
]

@cached
def subhit(tune=ROOT, dec=0.10, dur_steps=2.6):
    """The third layer of the kick: a clean sine at the root, mono, short.
    Not a bass note - the weight the punch and the growl are standing on."""
    n, t = steps(dur_steps)
    return (sub(tune, dur_steps) * np.exp(-t / dec)[:, None]).astype(np.float32)

s = Session(256, tail=4.0)

# ---- the parts ----
def floor(b, gain=1.0, steps_=(0, 4, 8, 12), rum=1.0, subg=0.85, lpf=None,
          tune=ROOT, drive=7.0, decay=0.185, grit=0.4, rtone=150, rdecay=0.95,
          rdrive=2.8, sdec=0.10, sub_steps=None):
    """Three layers, one instrument.

    The kick is the punch (its fundamental dives onto A1 and most of its
    energy is 20-120 Hz), the rumble is the room it is standing in - the same
    hit thrown into a dark reverb and driven until it is continuous, which is
    what fills the 390 ms between two kicks at this tempo - and the sub is a
    clean sine at 55 Hz underneath both, which is the weight. The two
    industrial records before this one had no third layer, and measured 32%
    and 36% of their energy under 120 Hz against 38% and 33% in the 120-300
    band: all growl, not enough floor.

    Every hit is registered, because the rumble and the sub both have to duck
    to the kick that made them or the three sum into one long smear.
    """
    subs = steps_ if sub_steps is None else sub_steps
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = techkick(tune=tune, drive=drive, decay=decay, grit=grit)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if rum:
            r = rumble(dur_steps=6, tune=tune, decay=rdecay, tone=rtone, drive=rdrive)
            if lpf:
                r = lp(r, min(lpf * 1.5, 600))
            s.place(t, r, rum, 'rumble')
        # When the kick goes to eighths the sub does NOT follow it. Eight sine
        # hits a bar at 55 Hz is not eight times the weight, it is one long
        # smear - so the weight stays on the four beats and the offbeats are
        # pure punch. That is how a double-time gear is built, and it is why
        # the last third of this record measured 13% in the 20-60 band on the
        # first pass against 28% in the section before it.
        if subg and st in subs:
            s.place(t, subhit(tune, sdec), subg, 'sub')

def tops(b, gain=1.0, sixteenths=True, opens=(), claps=(4, 12), clapg=0.72,
         shuffle=0.0, hatg=1.0):
    for st in claps:
        s.place(s.pos(b, st), distclap(3.0), gain * clapg, 'drums')
    if sixteenths:
        for i in range(16):
            if i % 4 == 0:
                continue                                  # the kick owns the beat
            v = 0.62 if i % 2 else 0.36                   # loud/soft: the cheapest groove
            off = shuffle * STEP if i % 2 else 0.0
            s.place(int(s.pos(b, i) + off), metalhat(0.7), gain * v * 0.9 * hatg, 'drums')
    for st in opens:
        s.place(s.pos(b, st), metalhat(3.0, open_=True), gain * 0.40 * hatg, 'drums')

# Swept-up filings on the floor of the machine hall: eight inharmonic clinks
# of four to sixteen milliseconds each, never on the grid. This is where the
# top of this record comes from - `chains` is a transient source, and two
# events a bar are heard as events, where a sustained band of noise at 6-9 kHz
# is a bed that hurts after ninety seconds.
def clink(b, gain=1.0, steps_=(6, 14), seed=0):
    for st in steps_:
        s.place(s.pos(b, st), chains(2.4, density=7, seed=seed + b * 3 + st),
                gain, 'music')

def metal(b, idx=0, gain=1.0):
    for st, note, g in METAL[idx % len(METAL)]:
        s.place(s.pos(b, st), anvil(note, 2.2, decay=0.105, bright=0.8, ring=0.5,
                                    seed=note), gain * g, 'music')

def offbeat(b, gain=1.0, cutoff=420, note=45, steps_=(2, 6, 10, 14), dur=2.0):
    for st in steps_:
        s.place(s.pos(b, st), distbass(note, dur, cutoff=cutoff), gain, 'bass')

def stabs(b, chord, gain=1.0, steps_=(2, 6, 10, 14), dur=1.6, drive=7.0):
    for st in steps_:
        s.place(s.pos(b, st), stab(tuple(chord), dur, drive=drive), gain, 'music')

def acidphrase(b0, bars, pat, cycle=16, gain=1.0, knob=None, f_hi=4800,
               f_lo=330, res=4.0, drive=4.0, low=240, octave=0, hard=False,
               bus='acid'):
    """A phrase per call, never a bar. The oscillator phase is continuous
    inside one call, so the slides really slide and there is no waveform
    discontinuity on the bar line - and `knob` is the hand on the cutoff,
    swept across the whole phrase rather than reset every sixteen steps."""
    p = poly_pattern(pat, cycle, bars)
    if octave:
        p = [(st, n + octave, d, a, sl) for st, n, d, a, sl in p]
    fn = acid_hard if hard else acid
    seg = fn(p, dur_bars=bars, knob=knob, f_lo=f_lo, f_hi=f_hi, res=res,
             drive=drive, low=low)
    s.place(s.pos(b0), seg, gain, bus)

def wall(b0, bars, gain=1.0, o0=(0.06, 0.55), o1=(0.35, 0.95), drive=2.6,
         fold_amt=0.22, detune=17.0, air=0.5, seed=0, start=0, top=0.0):
    """The chord loop, two bars a chord, rendered 2.4 bars long and placed
    every 2 - so the tails overlap the change and the wall is voice-led
    across it instead of switched. The filter's start and end points are
    ramped across the whole section by the caller, so it grows over thirty
    bars rather than pulsing every two.

    `top` adds the bottom three voices again an octave up and high-passed off
    their own fundamentals. A saw stack whose roots are around 200 Hz has
    almost nothing above 3 kHz - its 20th partial is 26 dB down - so a wall
    that is meant to read as glare has to be layered by band the way a lead
    is, not turned up."""
    n = bars // 2
    for i in range(n):
        u = i / max(n - 1, 1)
        ch = WALL[(start + i) % 4]
        a = o0[0] + (o0[1] - o0[0]) * u
        b = o1[0] + (o1[1] - o1[0]) * u
        s.place(s.pos(b0 + i * 2),
                glare(ch, 38, open0=a, open1=b, drive=drive, fold_amt=fold_amt,
                      detune=detune, air=air, seed=seed + i * 13),
                gain, 'glare')
        if top:
            s.place(s.pos(b0 + i * 2),
                    glare(tuple(f * 2 for f in ch[:3]), 38,
                          open0=min(a * 1.3, 1.0), open1=min(b * 1.15, 1.0),
                          f_lo=700.0, f_hi=11000.0, hpf=620.0, drive=drive * 0.85,
                          fold_amt=fold_amt * 0.7, detune=detune * 1.25,
                          air=air * 1.4, width=1.8, seed=seed + i * 13 + 5),
                    gain * top, 'glare')

def air_bed(b0, bars, grindg=1.4, sheetg=1.0, res=1.0, crush=0, gated=False,
            seed=0):
    """The room: the grind is its tone, tuned to the root; the sheet is its
    top, tuned to nothing. Both are needed and they are not the same job.

    `sheetg` is deliberately small wherever the drums are playing. A first
    pass had this bus owning 49% of everything above 3 kHz - two and a half
    times the level at which a sustained source stops being a texture and
    becomes the thing the ear is standing under. The top of a driving section
    belongs to hats, claps and short metal, all of which are events; the
    sheet's job is to be audible in the gaps they leave, and to take the band
    over completely in the two sections that have no drums at all."""
    for b in range(b0, b0 + bars, 4):
        s.place(s.pos(b), grind(64, note=45, gain=grindg, res=res, crush=crush,
                                seed=b + seed), 1.0, 'air')
    if sheetg:
        for b in range(b0, b0 + bars, 8):
            sh = sheet(128, seed=b + seed)
            if gated:
                sh = gate(sh, rate_steps=1.0, duty=0.55, depth=0.7)
            s.place(s.pos(b), sh, sheetg, 'air')

# ================= DER EINSTIEG: 0-15 =================
# No intro. The kick is there on the first sample, because a record that has
# to be explained for twenty-five seconds is not the one that plays at six in
# the morning. What builds is the room around it, not the pulse.
s.place(s.pos(0), tunnel(256, note=33, gain=1.6, motor=0.28), 1.0, 'air')
for b in range(0, 16):
    u = b / 15
    lpf = None if b >= 5 else 900 + 900 * b
    floor(b, gain=0.90 + 0.10 * u, lpf=lpf, rum=0.0 if b < 2 else 0.62 + 0.38 * u,
          subg=0.82 + 0.18 * u, rtone=120 + 20 * u, drive=6.2 + 1.0 * u,
          grit=0.14 + 0.24 * u)
    tops(b, gain=0.28 + 0.52 * u, sixteenths=b >= 4,
         claps=(4, 12) if b >= 8 else (), clapg=0.62,
         opens=(14,) if b >= 6 else ())
air_bed(0, 16, grindg=1.5, sheetg=0.0, res=0.8, seed=3)
air_bed(8, 8, grindg=1.7, sheetg=0.85, res=0.9, seed=11)
s.place(s.pos(4), hammer(8, tune=55, gain=0.8), 1.0, 'fx')
s.place(s.pos(12), press(24, tune=41.2, gain=0.55), 1.0, 'fx')
s.place(s.pos(15, 8), steam(8, gain=0.7), 1.0, 'fx')
kickroll(s, 15, [12, 13, 14, 15], gain=0.85, tune=ROOT, drive=8.0, decay=0.16,
         grit=0.5)

# ================= DIE MASCHINE: 16-47 =================
# Sixteen bars of the machine on its own, then the acid arrives on a
# thirteen-step cycle - it starts three steps earlier every bar and only
# comes home on the thirteenth, so thirteen bars of it are thirteen
# different bars and not one note had to change.
for b in range(16, 48):
    ph = b - 16
    floor(b, gain=1.0, rum=1.0, rtone=140, drive=7.0, grit=0.42)
    tops(b, gain=0.85, opens=(14,) if ph % 2 else (6, 14), clapg=0.92, hatg=1.30)
    if ph >= 4:
        metal(b, idx=ph // 8, gain=0.55 + 0.15 * min(ph / 16, 1))
    if ph >= 8:
        clink(b, 1.05, (6, 14) if ph % 2 else (2, 11), seed=1)
    if ph >= 8:
        offbeat(b, gain=0.42 + 0.14 * min((ph - 8) / 16, 1), cutoff=380 + 90 * min(ph / 24, 1))
    if ph % 8 == 7:
        s.place(s.pos(b, 12), steam(4, gain=0.45, seed=b), 1.0, 'fx')
for b0 in range(16, 48, 8):
    air_bed(b0, 8, grindg=1.35, sheetg=0.62, res=1.0, gated=b0 >= 32, seed=b0)
for b0, knob, g in ((32, (0.16, 0.34), 0.42), (40, (0.34, 0.62), 0.62)):
    acidphrase(b0, 8, ACID_P, cycle=13, gain=g, knob=knob, f_hi=3400, res=3.4,
               drive=3.6)
s.place(s.pos(24), hammer(8, tune=55, gain=0.85, seed=1), 1.0, 'fx')
s.place(s.pos(32), impact(24, gain=0.5), 1.0, 'fx')
s.place(s.pos(40), press(24, tune=41.2, gain=0.6, seed=2), 1.0, 'fx')
kickroll(s, 47, [8, 10, 12, 13, 14, 15], gain=0.9, tune=ROOT, drive=8.5,
         decay=0.155, grit=0.55)

# ================= DRUCK: 48-79 =================
# The acid comes onto the grid and the knob starts moving. The pattern stops
# changing here and does not change again for thirty-two bars; the cutoff,
# the resonance and the drive do all the work, which is the genre's oldest
# and best trick.
for b in range(48, 80):
    ph = b - 48
    u = ph / 31
    floor(b, gain=1.0, rum=1.0, rtone=145 + 25 * u, drive=7.4 + 0.8 * u,
          grit=0.45, rdrive=2.9)
    tops(b, gain=0.92, opens=(14,), clapg=0.95, hatg=1.35)
    metal(b, idx=ph // 8, gain=0.75)
    clink(b, 1.25, (2, 6, 14) if ph % 2 else (6, 11, 14), seed=2)
    offbeat(b, gain=0.58, cutoff=470)
    if ph >= 16:
        stabs(b, Bb if b % 8 == 7 else Am, gain=0.42 + 0.2 * u, steps_=(6, 14))
    if ph % 8 == 6:
        s.place(s.pos(b, 8), servo(8, rate=20, accel=2.0, seed=b), 0.5, 'music')
for b0 in range(48, 80, 8):
    air_bed(b0, 8, grindg=1.25, sheetg=0.55, res=1.0, gated=True, seed=b0 + 5)
acidphrase(48, 8, ACID_A, gain=0.78, knob=(0.5, 0.72), f_hi=4200, res=3.9, drive=3.9)
acidphrase(56, 8, ACID_A, gain=0.88, knob=(0.72, 0.88), f_hi=5000, res=4.2, drive=4.2)
acidphrase(64, 8, ACID_B, gain=0.92, knob=(0.62, 0.95), f_hi=5400, res=4.4,
           drive=4.4, hard=True)
acidphrase(72, 8, ACID_B, gain=0.98, knob=(0.8, 1.0, 0.7), f_hi=5800, res=4.6,
           drive=4.6, hard=True)
s.place(s.pos(56), hammer(8, tune=55, gain=0.85, seed=3), 1.0, 'fx')
s.place(s.pos(64), impact(24, gain=0.55), 1.0, 'fx')
s.place(s.pos(64), screamer(10, note=57, gain=0.55, vowel='eh', crush=7), 1.0, 'fx')
s.place(s.pos(72), press(24, tune=41.2, gain=0.65, seed=4), 1.0, 'fx')
s.place(s.pos(79, 8), whoosh(8, gain=0.9), 1.0, 'fx')

# ================= LEERE: 80-95 =================
# The kick stops dead. What is left is loud in the mids and has no bottom at
# all, so it measures as the quiet section it is while sounding like the
# opposite - and the acid, which has been a texture under a machine for
# sixty bars, is suddenly the only thing in the room.
s.place(s.pos(80), downlifter(16, gain=0.95), 1.0, 'fx')
s.place(s.pos(80), tunnel(256, note=33, gain=1.9, motor=0.12), 1.0, 'air')
s.place(s.pos(81), alarm(64, f0=180, f1=580, cycles=2.0, gain=0.8), 1.0, 'fx')
for b0 in range(80, 96, 8):
    air_bed(b0, 8, grindg=2.6, sheetg=1.5, res=1.3, crush=8, seed=b0 + 9)
acidphrase(80, 8, ACID_A, gain=1.05, knob=(0.55, 0.95), f_hi=5600, res=4.7,
           drive=4.3, hard=True)
acidphrase(88, 4, ACID_B, gain=1.05, knob=(0.9, 1.0), f_hi=6000, res=4.8,
           drive=4.5, hard=True)
for b in range(84, 96):
    metal(b, idx=b // 3, gain=0.42)
s.place(s.pos(83), screamer(12, note=45, gain=0.7, vowel='oh', fall=5, crush=6), 1.0, 'fx')
s.place(s.pos(86), chains(8, gain=0.7, seed=86), 1.0, 'music')
for b in (88, 90):                                        # two kicks: a promise
    floor(b, gain=0.8, steps_=(0,), rum=0.85, subg=0.7, lpf=1500, rtone=130)
s.place(s.pos(92), stutter(acid_hard(poly_pattern(ACID_B, 16, 1), 1, f_lo=330,
                                     f_hi=6200, res=4.8, drive=4.6, low=240),
                           slice_steps=2.0, repeats=8, decay=0.94, accel=1.16),
        0.6, 'acid')
for b in range(92, 96):                                   # the floor rebuilds
    ph = b - 92
    floor(b, gain=0.6 + 0.13 * ph, lpf=900 + 1100 * ph, rum=0.7 + 0.08 * ph,
          subg=0.6 + 0.1 * ph, rtone=130 + 8 * ph)
    tops(b, gain=0.45 + 0.15 * ph, claps=(4, 12), clapg=0.6)
s.place(s.pos(92), riser(64, gain=0.9, f0=170, f1=1800), 1.0, 'fx')
s.place(s.pos(95, 8), reverse_crash(8, gain=0.9), 1.0, 'fx')

# ================= AUFBAU: 96-119 =================
# Sixteen bars to re-establish, eight to build. The wall is already there
# from bar 104 with its filter almost shut - four bars of something enormous
# that cannot be identified yet, so the arrival at 120 is a door opening
# rather than a new instrument being introduced.
for b in range(96, 112):
    ph = b - 96
    u = ph / 15
    floor(b, gain=1.0, rum=1.0, rtone=155 + 20 * u, drive=7.8, grit=0.5)
    tops(b, gain=0.95, opens=(14,) if ph % 2 else (6, 14), hatg=1.35, clapg=0.92)
    metal(b, idx=ph // 4, gain=0.8)
    clink(b, 1.30, (2, 6, 14) if ph % 2 else (6, 11, 14), seed=3)
    offbeat(b, gain=0.62, cutoff=500)
    if ph % 8 == 6:
        s.place(s.pos(b, 8), servo(8, rate=22, accel=2.1, seed=b), 0.5, 'music')
for b0 in range(96, 120, 8):
    air_bed(b0, 8, grindg=1.2, sheetg=0.55, res=1.0, gated=True, seed=b0 + 13)
acidphrase(96, 8, ACID_C, gain=0.95, knob=(0.7, 0.92), f_hi=5600, res=4.4,
           drive=4.4, hard=True)
acidphrase(104, 8, ACID_C, gain=0.98, knob=(0.85, 1.0), f_hi=6000, res=4.6,
           drive=4.6, hard=True)
wall(104, 16, gain=0.30, o0=(0.02, 0.06), o1=(0.10, 0.22), drive=2.2,
     fold_amt=0.12, air=0.25, seed=200)
s.place(s.pos(104), impact(24, gain=0.5), 1.0, 'fx')
s.place(s.pos(112), press(28, tune=41.2, gain=0.7, seed=5), 1.0, 'fx')
# The last eight bars raise five things at once and take one away: the claps
# accelerate 1/4 - 1/8 - 1/16 - 1/32, the servo speeds up, the riser climbs,
# the wall's filter opens - and the sub and the rumble drain out over the
# last four bars, which is the high-pass every build does and the reason the
# bottom coming back at 120 lands like a door.
for b in range(112, 120):
    ph = b - 112
    drain = max(0.0, (ph - 3) / 5.0)                      # 0 until bar 115
    floor(b, gain=1.0 - 0.25 * drain, steps_=(0, 4, 8, 12) if ph < 7 else (0, 4, 8),
          rum=1.0 - 0.95 * drain, subg=0.9 - 0.9 * drain,
          rtone=175, drive=8.0, grit=0.55)
    tops(b, gain=0.95 + 0.2 * (ph / 7), opens=(6, 14))
    metal(b, idx=ph // 2, gain=0.8)
    offbeat(b, gain=0.62 * (1 - drain), cutoff=520)
    div = (4, 4, 2, 2, 1, 1, 0.5, 0.5)[ph]
    st = 0.0
    stop = 13.0 if ph == 7 else 16.0            # the last beat is the gap
    while st < stop:
        s.place(s.pos(b, st), distclap(2.0), 0.20 + 0.36 * (ph / 7) * (0.5 + st / 32),
                'drums')
        st += div
    s.place(s.pos(b), servo(16, rate=16 + 7 * ph, accel=2.3, seed=b), 0.45 + 0.05 * ph,
            'music')
s.place(s.pos(112), riser(128, gain=1.0, f0=150, f1=2400), 1.0, 'fx')
s.place(s.pos(116), alarm(64, f0=210, f1=700, cycles=2.0, gain=0.6), 1.0, 'fx')
kickroll(s, 119, [0, 4, 8, 10, 12], gain=0.85, tune=ROOT, drive=8.5, decay=0.15,
         grit=0.6, climb=0.03)
s.place(s.pos(119, 8), reverse_crash(8, gain=1.0), 1.0, 'fx')
s.place(s.pos(119, 12), screamer(4, note=69, gain=0.85, vowel='ah', crush=6), 1.0, 'fx')

# ================= BLENDUNG: 120-167 =================
# The arrival, and the whole argument of the record. Nothing stops. The kick,
# the rumble, the sub, the hats, the clap and the machine shop all keep doing
# exactly what they were doing at bar 119 - and on top of them a section of
# detuned saws walks in with its filter opening and does not leave for
# forty-eight bars. The Bb is gone: this is A Aeolian, and the chords are the
# plainest euphoric loop in the language, i - bVI - bIII - bVII.
def wall_chord(b, b0=120, lo=3):
    return WALL[((b - b0) // 2) % 4][:lo]

for b in range(120, 168):
    ph = b - 120
    u = ph / 47
    floor(b, gain=1.0, rum=1.0, rtone=170 + 15 * u, drive=8.2, grit=0.5,
          rdrive=3.0)
    tops(b, gain=1.0, opens=(14,) if ph % 2 else (6, 14), hatg=1.35, clapg=0.95)
    metal(b, idx=ph // 8, gain=0.85)
    clink(b, 1.35, (2, 6, 14) if ph % 2 else (6, 11, 14), seed=4)
    offbeat(b, gain=0.68, cutoff=530)
    if ph % 16 == 15:
        kickroll(s, b, [0, 4, 8, 10, 12, 14], gain=1.0, tune=ROOT, drive=8.5,
                 decay=0.17, grit=0.55)
    if ph >= 32:
        stabs(b, wall_chord(b), gain=0.45, steps_=(6, 14), drive=6.5)
for b0 in range(120, 168, 8):
    air_bed(b0, 8, grindg=1.1, sheetg=0.55, res=1.0, gated=True, seed=b0 + 17)
    s.place(s.pos(b0), crash808(20, gain=0.5), 1.0, 'drums')
# The filter starts a third open rather than shut. On the first pass it came
# in at 0.06 and the arrival measured 3.9% in the 800-3000 band against the
# build's 4.6% - a wall named after being dazzled that made the record darker
# for eight bars. It still grows 0.16 -> 0.50 across the section; it just does
# not have to be inaudible to do it.
wall(120, 32, gain=0.98, o0=(0.16, 0.50), o1=(0.46, 0.90), drive=2.5,
     fold_amt=0.20, air=0.45, seed=300, top=0.55)
wall(152, 16, gain=1.05, o0=(0.45, 0.60), o1=(0.88, 0.97), drive=2.8,
     fold_amt=0.26, air=0.55, seed=700, top=0.58)
# The acid stays out for sixteen bars so the wall has the room, then comes
# back in Aeolian - the same hand, one note moved.
acidphrase(132, 4, ACID_E, gain=0.42, knob=(0.35, 0.55), f_hi=4400, res=3.6, drive=3.8)
acidphrase(136, 8, ACID_E, gain=0.66, knob=(0.55, 0.82), f_hi=5200, res=3.8, drive=4.0)
acidphrase(144, 8, ACID_E, gain=0.72, knob=(0.8, 0.95), f_hi=5800, res=4.0, drive=4.2)
acidphrase(152, 16, ACID_E, gain=0.80, knob=(0.85, 1.0, 0.9, 1.0), f_hi=6200,
           res=4.2, drive=4.4, hard=True)
s.place(s.pos(120), impact(28, gain=0.75), 1.0, 'fx')
for b in (128, 144, 160):
    s.place(s.pos(b), press(24, tune=41.2, gain=0.6, seed=b), 1.0, 'fx')
for b, note in ((136, 69), (152, 64), (164, 72)):
    s.place(s.pos(b, 12), screamer(6, note=note, gain=0.65, vowel='ah', crush=6), 1.0, 'fx')
s.place(s.pos(167, 8), whoosh(8, gain=0.95), 1.0, 'fx')

# ================= SCHWARZ: 168-183 =================
# The floor of the record. Eight bars in which almost nothing happens - one
# kick a bar, lowpassed until it is a thud in the next room, and the wall
# reduced to a shut filter. This has to measure as the quietest thing here or
# the fifty-six bars after it have nothing to be louder than.
s.place(s.pos(168), downlifter(14, gain=0.8), 1.0, 'fx')
s.place(s.pos(168), tunnel(192, note=33, gain=1.5, motor=0.4), 1.0, 'air')
for b in range(168, 176):
    ph = b - 168
    floor(b, gain=0.55 + 0.05 * ph, steps_=(0, 8) if ph < 4 else (0, 4, 8, 12),
          lpf=460 + 140 * ph, rum=0.45, subg=0.5, rtone=115, rdecay=1.3,
          drive=5.4, grit=0.0)
    if ph >= 3:
        s.place(s.pos(b, 8), metalhat(3.0, open_=True), 0.16, 'drums')
    if ph >= 5:
        s.place(s.pos(b, 4), distclap(3.0), 0.20, 'drums')
wall(168, 8, gain=0.40, o0=(0.02, 0.05), o1=(0.09, 0.16), drive=2.0,
     fold_amt=0.06, air=0.15, seed=900)
s.place(s.pos(170), chains(8, gain=0.45, seed=170), 1.0, 'music')
s.place(s.pos(173), bellow(48, gain=0.5, rate=0.5, seed=3), 1.0, 'air')
# and then eight bars that put everything back at once
for b in range(176, 184):
    ph = b - 176
    u = ph / 7
    floor(b, gain=0.62 + 0.38 * u, rum=0.45 + 0.55 * u, subg=0.45 + 0.5 * u,
          lpf=1400 + 1800 * ph if ph < 5 else None, rtone=120 + 62 * u,
          drive=6.2 + 2.0 * u, grit=0.15 + 0.4 * u)
    tops(b, gain=0.35 + 0.65 * u, sixteenths=ph >= 2, claps=(4, 12) if ph >= 3 else (),
         clapg=0.55 + 0.2 * u, opens=(14,) if ph >= 4 else ())
    if ph >= 4:
        metal(b, idx=ph, gain=0.5 + 0.09 * ph)
    div = (4, 4, 2, 2, 1, 1, 0.5, 0.5)[ph]
    st = 0.0
    stop = 13.0 if ph == 7 else 16.0
    while st < stop:
        s.place(s.pos(b, st), distclap(2.0), 0.14 + 0.32 * u * (0.5 + st / 32), 'drums')
        st += div
    s.place(s.pos(b), servo(16, rate=14 + 8 * ph, accel=2.4, seed=b), 0.4 + 0.06 * ph,
            'music')
air_bed(176, 8, grindg=1.5, sheetg=0.85, res=1.1, gated=True, seed=176)
acidphrase(176, 8, ACID_C, gain=0.5, knob=(0.25, 1.0), f_hi=6200, res=4.6,
           drive=4.6, hard=True)
wall(176, 8, gain=0.85, o0=(0.06, 0.30), o1=(0.20, 0.70), drive=2.6,
     fold_amt=0.18, air=0.4, seed=950, top=0.40)
s.place(s.pos(176), riser(128, gain=1.05, f0=140, f1=2600), 1.0, 'fx')
s.place(s.pos(180), alarm(64, f0=220, f1=760, cycles=2.0, gain=0.7), 1.0, 'fx')
kickbarrage(s, 183, [0, 4, 8, 10, 12, 13], gain=1.0, tune=ROOT, climb=0.04)
s.place(s.pos(183, 8), reverse_crash(8, gain=1.1), 1.0, 'fx')
s.place(s.pos(183, 14), screamer(2, note=72, gain=0.9, vowel='ah', crush=6), 1.0, 'fx')

# ================= VERNICHTUNG: 184-239 =================
# Fifty-six bars in three gears, and the gear is the kick pattern. Four on
# the floor for twenty-four, then the rolling eight - 0 3 4 7 8 11 12 15, the
# hard-groove pattern that feels like a doubling without being one - and then
# straight eighths for the last sixteen, which is the point at which it
# simply does not let go. The Bb is back, in the acid, over the euphoric
# chords: the loudest and brightest passage on the record is also the only
# place where both scales are sounding at once.
GEAR = {0: (0, 4, 8, 12), 1: (0, 3, 4, 7, 8, 11, 12, 15),
        2: (0, 2, 4, 6, 8, 10, 12, 14)}

for b in range(184, 240):
    ph = b - 184
    g = 0 if ph < 24 else (1 if ph < 40 else 2)
    u = ph / 55
    st_ = GEAR[g]
    floor(b, gain=1.0 if g == 0 else 0.94, steps_=st_,
          sub_steps=(0, 4, 8, 12), rum=1.0 if g == 0 else 0.86,
          subg=0.9 if g == 0 else 0.86, rtone=185, drive=8.6 + 0.8 * u,
          decay=0.185 if g == 0 else 0.16, grit=0.55, rdrive=3.1,
          rdecay=0.95 if g == 0 else 0.78, sdec=0.10 if g == 0 else 0.085)
    tops(b, gain=1.0, sixteenths=g < 2, opens=(6, 14), hatg=1.45,
         claps=(4, 12) if g < 2 else (2, 6, 10, 14), clapg=0.98 if g < 2 else 0.62)
    metal(b, idx=ph // 4, gain=0.9)
    clink(b, 1.45, (2, 6, 14) if ph % 2 else (6, 11, 14), seed=5)
    if g == 0:
        offbeat(b, gain=0.72, cutoff=560)
    stabs(b, wall_chord(b, 184), gain=0.55 + 0.2 * u,
          steps_=(6, 14) if g == 0 else (2, 6, 10, 14), drive=7.5)
    if g == 0 and ph % 16 == 15:
        kickroll(s, b, [0, 4, 8, 10, 12, 14], gain=1.0, tune=ROOT, drive=9.0,
                 decay=0.16, grit=0.6)
for b0 in range(184, 240, 8):
    air_bed(b0, 8, grindg=1.15, sheetg=0.58, res=1.1, gated=True, seed=b0 + 23)
    s.place(s.pos(b0), crash808(20, gain=0.55), 1.0, 'drums')
wall(184, 24, gain=1.05, o0=(0.35, 0.55), o1=(0.80, 0.95), drive=2.8,
     fold_amt=0.26, air=0.5, seed=400, start=0, top=0.54)
wall(208, 16, gain=1.12, o0=(0.55, 0.62), o1=(0.95, 0.99), drive=3.0,
     fold_amt=0.30, detune=19.0, air=0.6, seed=500, top=0.62)
wall(224, 16, gain=1.18, o0=(0.62, 0.68), o1=(0.99, 1.0), drive=3.2,
     fold_amt=0.34, detune=21.0, air=0.65, seed=600, top=0.70)
acidphrase(184, 8, ACID_C, gain=0.85, knob=(0.7, 0.9), f_hi=5800, res=4.4,
           drive=4.5, hard=True)
acidphrase(192, 16, ACID_C, gain=0.92, knob=(0.9, 1.0, 0.85, 1.0), f_hi=6200,
           res=4.6, drive=4.7, hard=True)
acidphrase(208, 16, ACID_C, gain=0.98, knob=(0.95, 1.0), f_hi=6600, res=4.7,
           drive=4.9, hard=True)
acidphrase(208, 16, ACID_C, gain=0.30, knob=(0.9, 1.0), f_hi=7400, res=3.4,
           drive=3.8, low=560, octave=12)                 # the line an octave up
acidphrase(224, 16, ACID_C, gain=1.0, knob=(1.0, 0.9, 1.0), f_hi=7000, res=4.8,
           drive=5.0, hard=True)
acidphrase(224, 16, ACID_C, gain=0.38, knob=(1.0, 1.0), f_hi=7800, res=3.6,
           drive=4.0, low=560, octave=12)
for b in (192, 216, 232):
    s.place(s.pos(b), press(24, tune=41.2, gain=0.65, seed=b), 1.0, 'fx')
for b, note in ((200, 69), (208, 72), (224, 76), (236, 69)):
    s.place(s.pos(b, 12), screamer(6, note=note, gain=0.7, vowel='ah', crush=6), 1.0, 'fx')
# the two gear changes are marked, or nobody notices them
for b in (208, 224):
    s.place(s.pos(b), impact(28, gain=0.8), 1.0, 'fx')
    s.place(s.pos(b - 1, 12), whoosh(4, gain=0.9), 1.0, 'fx')
    s.place(s.pos(b), alarm(64, f0=230, f1=800, cycles=2.0, gain=0.55), 1.0, 'fx')

# ================= AUSGANG: 240-255 =================
s.place(s.pos(240), tunnel(160, note=33, gain=1.6, motor=0.22), 1.0, 'air')
s.place(s.pos(240), downlifter(16, gain=0.7), 1.0, 'fx')
for b in range(240, 256):
    ph = b - 240
    u = ph / 15
    floor(b, gain=1.0 - 0.6 * u, steps_=(0, 4, 8, 12), lpf=9000 - 520 * ph,
          rum=1.0 - 0.55 * u, subg=0.9 - 0.5 * u, rtone=180 - 60 * u,
          drive=7.6, grit=0.4 - 0.35 * u, rdecay=1.15)
    tops(b, gain=0.9 - 0.75 * u, sixteenths=ph < 8, claps=(4, 12) if ph < 5 else (),
         clapg=0.6, opens=(14,) if ph < 10 else ())
    if ph < 8:
        metal(b, idx=ph // 2, gain=0.7 - 0.07 * ph)
for b0 in (240, 248):
    air_bed(b0, 8, grindg=1.5 + 0.3 * (b0 == 248), sheetg=0.8 - 0.45 * (b0 == 248),
            res=0.9, seed=b0 + 31)
wall(240, 8, gain=0.9, o0=(0.55, 0.20), o1=(0.90, 0.35), drive=2.4,
     fold_amt=0.16, air=0.35, seed=800)
acidphrase(240, 8, ACID_C, gain=0.7, knob=(0.9, 0.25), f_hi=5600, res=4.2, drive=4.2)
s.place(s.pos(248), press(28, tune=41.2, gain=0.5, seed=9), 1.0, 'fx')
s.place(s.pos(252), alarm(48, f0=170, f1=340, cycles=1.0, gain=0.45), 1.0, 'fx')
s.place(s.pos(255), downlifter(16, gain=0.6), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['music'] = bus_reverb(s.bus['music'], decay=1.4, wet=0.20, tone=5600)
s.bus['glare'] = bus_reverb(s.bus['glare'], decay=2.6, wet=0.26, tone=5200)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.0, wet=0.32, tone=4600)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=2.4, wet=0.20, tone=4200)
s.bus['acid']  = bus_reverb(s.bus['acid'],  decay=0.9, wet=0.13, tone=5000)
s.bus['air']   = hp(s.bus['air'], 62)                            # the kick owns 20-60
s.bus['glare'] = hp(s.bus['glare'], 230)                         # and 20-230
s.bus['acid']  = shelf(s.bus['acid'], 230, -2.0, kind='low')
s.bus['drums'] = softclip(s.bus['drums'], 1.15, knee=0.85)
s.bus['rumble'] = softclip(s.bus['rumble'], 1.05, knee=0.85)
s.bus['sub']   = softclip(s.bus['sub'], 1.0, knee=0.9)
# Everything with weight goes mono under 140 Hz. Both industrial records
# before this one still measured 13-14% of their sub in the side channel
# after this move, because a 4th-order crossover at 150 Hz leaks - so the
# crossover goes higher and the buses that have no business being wide down
# there get narrowed as well as folded.
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 170)
s.bus['glare'] = side_boost(s.bus['glare'], 480, 0.55)           # wide, but only up top
# `sheet` is already two independent noise channels plus a 1.7 ms offset, so
# it measures 270% side on its own. Widening that further does not make it
# bigger, it makes it cancel - the fix for a quiet top end is level, not width.
s.bus['air']   = narrow(s.bus['air'], 0.82)

# ---- the arc ----
# The first pass of this record measured -5 to -6.5 LUFS from bar 8 to bar
# 167 without a single break in it: every section had been given different
# PARTS and none had been given a different LEVEL, so the void was as loud as
# the drop and the arrival at bar 120 read 0.9 dB quieter than the bars
# before it. Contrast is relative, and the ear judges a section against what
# it just heard - so this is the ride, in decibels, and it is as much a part
# of the arrangement as the notes.
ARC = [(0, -3.4), (8, -2.7), (16, -2.5), (32, -2.3), (48, -2.0), (64, -1.6),
       (76, -1.4), (79.9, -1.4), (80, -7.6), (88, -6.6), (92, -4.6),
       (96, -2.6), (112, -2.2), (116, -2.8), (119.5, -3.6), (119.99, -3.6),
       (120, -0.4), (136, -0.4),
       (152, -0.2), (167.9, -0.2), (168, -8.5), (173, -8.0), (176, -5.2),
       (181, -2.8), (183.5, -2.4), (183.75, -4.2), (183.99, -4.2), (184, 0.0),
       (208, 0.0), (224, 0.0),
       (239.9, 0.0), (240, -1.8), (248, -4.5), (256, -9.0)]
_bars = np.array([p[0] for p in ARC]) * BAR
_db   = np.array([p[1] for p in ARC])
_t    = np.arange(s.total, dtype=np.float64)
_ride = 10 ** (np.interp(_t, _bars, _db) / 20.0)
_ride = uniform_filter1d(_ride, int(0.030 * SR))                 # no zipper
for b in s.bus:
    s.bus[b] = (s.bus[b] * _ride[:, None]).astype(np.float32)

GAINS = {'drums': 0.78, 'rumble': 0.54, 'sub': 0.44, 'bass': 0.22, 'acid': 0.42,
         'glare': 0.58, 'music': 0.52, 'air': 0.36, 'fx': 0.34}
s.report(GAINS)
s.ownership(3000, 16000, GAINS, 'top  3-16k')
s.ownership(120, 300, GAINS, 'low-mid 120-300')
s.render('industrial_blendung_154.wav', drive=1.0, duck=0.46, duck_rel=0.17,
         clip=1.05, peak=0.95, fade=2.2, gains=GAINS,
         brick=dict(gain=1.24, ceiling=0.89))
