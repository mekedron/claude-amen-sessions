"""HEIMWEG - ambient dub techno at 118 BPM, A minor moving to A Dorian.

Heimweg is the way home. This is the third record from the same night as
`blendung` and `finsternis` and it is the one that happens after them: seven
in the morning, you are outside, the light is wrong, your body is still at
142 and the city has started without you.

118 BPM because a walking pace is about 118 steps a minute, so the beat is a
footstep and not a machine. The kick is `mkick` - clean, 138 ms, no distortion
anywhere near it - and for a third of the record there is no kick at all.

The whole harmonic argument is one note, twice.

The chords are i - bVII - bVI - bVII, four bars each, and above them the lead
does not move: it holds E5 for the entire record. Over Am that E is the fifth,
over G the sixth, over F the major seventh, over D the ninth - one note that
is four different feelings depending on what walks underneath it, which is
worth more than a melody here and costs nothing.

Then at bar 96 the F becomes D. That is the natural sixth, Aeolian becomes
Dorian, and it is the difference between being tired and being alright. It is
the only note that changes in six minutes.

`shimmer()` is new and it is what makes this a morning rather than a night:
a reverb with an octave transposition inside its feedback path, so a held
chord grows a choir of its own harmonics that nobody played - late, in tune,
and further away every pass. Measured on one chord it moves the energy from
78% in 200-800 Hz to 73% in 800-3000 and takes the ring from 2.0 seconds to
6.3.

No bells. The concept is daylight and a struck bright object would read as a
music box, which is the one thing this must not be; the top comes from the
shimmer and from dust.

    ANKUNFT | GEHEN | LICHT | MUEDIGKEIT | DORISCH | ZUHAUSE | SCHLAF

176 bars, 5:58.
"""
import numpy as np
from minimallib import *

set_tempo(118)
np.random.seed(1180)

ROOT = 55.00                                     # A1 - the pedal
Session.DUCKED = {'sub': 0.55, 'pad': 0.45, 'shine': 0.30, 'chord': 0.55,
                  'lead': 0.35, 'air': 0.25}

Am = tuple(midi(n) for n in (57, 64, 69, 72))    # i     A  E  A  C
G_ = tuple(midi(n) for n in (55, 62, 67, 71))    # bVII  G  D  G  B
F_ = tuple(midi(n) for n in (53, 60, 65, 69))    # bVI   F  C  F  A
D_ = tuple(midi(n) for n in (50, 57, 62, 66))    # IV    D  A  D  F#  - the Dorian
AEOL = (Am, G_, F_, G_)
DOR  = (Am, G_, D_, G_)
HELD = midi(76)                                  # E5, and it never moves

s = Session(176, tail=8.0)

# ---- the parts ----
@cached
def chordpad(notes, dur_steps=64, cutoff=2200, attack=0.9, gain=1.0, seed=0):
    """The harmony. `ens` and not `pad`: four players per note who enter
    10-70 ms apart and each drift on their own slow walk, so the beating is
    aperiodic. A block chord here would be a preset lying under a record
    about being awake too long."""
    return ens(list(notes), dur_steps, gain=gain, voices=4, cutoff=cutoff,
               attack=attack, bow=0.55, drift=1.25, seed=seed)

@cached
def shine(notes, dur_steps=64, decay=6.0, wet=0.55, tone=2800, passes=3,
          fb=0.55, seed=0):
    """The same chord sent round the octave loop. Rendered from a quieter,
    darker copy than the pad hears, because what comes back is three passes
    of room on top of a transposition and it does not need the transient."""
    dry = ens(list(notes), dur_steps, gain=0.55, voices=3, cutoff=1500,
              attack=1.4, bow=0.2, drift=1.0, seed=seed + 11)
    return shimmer(dry, decay=decay, wet=wet, tone=tone, passes=passes,
                   fb=fb, damp=4000)

def harmony(b0, bars, prog, gain=1.0, shineg=0.0, cutoff=2200, attack=0.9,
            decay=6.0, seed=0):
    """Four bars a chord, rendered five bars long and placed on the change so
    the tails overlap it - the progression is voice-led across the seam
    instead of switched."""
    for i in range(bars // 4):
        ch = prog[i % len(prog)]
        s.place(s.pos(b0 + i * 4), chordpad(ch, 80, cutoff=cutoff,
                                            attack=attack, seed=seed + i * 7),
                gain, 'pad')
        if shineg:
            s.place(s.pos(b0 + i * 4), shine(ch, 72, decay=decay,
                                             seed=seed + i * 7), shineg, 'shine')

def held(b0, bars, gain=1.0, cutoff=2600, seed=0):
    """E5, for as long as the section lasts. It is the same note over four
    different chords and it means something different under each one."""
    s.place(s.pos(b0), ens([HELD], bars * 16 + 8, gain=gain, voices=3,
                           cutoff=cutoff, attack=2.2, bow=0.5, drift=1.4,
                           seed=seed), 1.0, 'lead')

def floor(b, gain=1.0, steps_=(0, 4, 8, 12), tailg=0.9, tune=ROOT, decay=0.135,
          drive=2.0, click=0.55, tick=0.5, knock=0.6, lpf=None):
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)
        k = mkick(tune=tune, decay=decay, drive=drive, click=click, tick=tick,
                  knock=knock)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')
        if tailg:
            s.place(t, ktail(tune=tune, decay=0.24, tone=180), tailg, 'sub')

def perc(b, gain=1.0, sh=(2, 6, 10, 14), rim=(), clap=(), seed=0):
    for st in sh:
        s.place(s.pos(b, st), shaker(0.8, bright=0.72, seed=(b * 16 + st) % 61),
                gain * 0.30, 'drums')
    for st in rim:
        s.place(s.pos(b, st), rimtick(0.6, f=1480.0, seed=(b * 4 + st) % 47),
                gain * 0.34, 'drums')
    for st in clap:
        s.place(s.pos(b, st), mclap(3.0, room=0.7, seed=(b + st) % 29),
                gain * 0.22, 'drums')

def offchord(b, ch, gain=1.0, st=6, cutoff=3200, times=7, fb=0.58):
    """The offbeat chord thrown into a tape echo. The instrument is the stab
    plus the echo; on its own it is a click with a chord attached."""
    seg = dubstab(list(ch), 1.6, f_hi=cutoff, res=2.0, decay=0.075, drive=1.6)
    s.place(s.pos(b, st), dubecho(seg, steps_=3.0, times=times, fb=fb,
                                  damp0=4200.0, darken=0.60, drive=1.5,
                                  seed=b), gain, 'chord')

def bed(b0, bars, humg=1.0, dustg=0.0, note=33, seed=0):
    s.place(s.pos(b0), hum(note=note, dur_steps=bars * 16, gain=humg,
                           cutoff=460, motor=0.16, seed=seed), 1.0, 'air')
    if dustg:
        for b in range(b0, b0 + bars, 4):
            s.place(s.pos(b), dust(64, gain=dustg, density=14, lo=2600,
                                   hi=9000, seed=b), 1.0, 'air')

# ================= ANKUNFT: 0-15 =================
# Outside. No kick for thirty-three seconds, and the first thing that happens
# is the shimmer arriving before the chord that caused it, because three
# passes of a six-second room put the octaves a long way behind the note.
bed(0, 16, humg=1.3, seed=1)
harmony(0, 16, AEOL, gain=0.62, shineg=0.34, cutoff=1500, attack=1.8, seed=0)
held(4, 12, gain=0.30, cutoff=1800, seed=3)
s.place(s.pos(8), sweepnoise(64, gain=0.28, f0=400, f1=5200, q=0.5, curve=2.0,
                             seed=2), 1.0, 'air')
for b in range(12, 16):
    perc(b, gain=0.34 + 0.12 * (b - 12), sh=(6, 14))

# ================= GEHEN: 16-47 =================
# The walk. A kick that is 138 ms long and has nothing done to it, a sub tail
# under it, and an offbeat chord in a tape echo. Three elements and the room.
for b in range(16, 48):
    ph = b - 16
    u = ph / 31
    floor(b, gain=0.52 + 0.28 * u, tailg=0.55 + 0.35 * u,
          lpf=2600 + 260 * ph if ph < 8 else None, click=0.40 + 0.20 * u,
          tick=0.30 + 0.25 * u)
    perc(b, gain=0.5 + 0.3 * u, sh=(2, 6, 10, 14),
         rim=(7, 15) if ph >= 8 else (), clap=(12,) if ph >= 16 else ())
bed(16, 32, humg=1.1, dustg=0.5, seed=4)
harmony(16, 32, AEOL, gain=0.78, shineg=0.40, cutoff=1900, attack=1.3, seed=10)
held(16, 32, gain=0.34, cutoff=2100, seed=5)
for i, b in enumerate(range(19, 48, 4)):
    offchord(b, AEOL[(i + 1) % 4], gain=0.34 + 0.03 * i, cutoff=2600 + 120 * i)

# ================= LICHT: 48-79 =================
# The light. Nothing new arrives - the shimmer's send goes up, the pad's
# filter opens from 1.9 to 3.4 kHz, and the held note comes forward. The
# section is one long crossfade and it has no event in it anywhere.
for b in range(48, 80):
    ph = b - 48
    u = ph / 31
    floor(b, gain=0.80 + 0.10 * u, tailg=0.92, click=0.60, tick=0.55,
          knock=0.66)
    perc(b, gain=0.85, sh=(2, 6, 10, 14), rim=(7, 15),
         clap=(12,) if ph % 4 == 3 else ())
bed(48, 32, humg=0.9, dustg=0.85, seed=6)
harmony(48, 32, AEOL, gain=0.92, shineg=0.62, cutoff=2600, attack=1.0, seed=20)
held(48, 32, gain=0.50, cutoff=3000, seed=7)
for i, b in enumerate(range(51, 80, 4)):
    offchord(b, AEOL[(i + 1) % 4], gain=0.46, cutoff=3400, fb=0.62)
s.place(s.pos(64), sweepnoise(96, gain=0.34, f0=600, f1=7000, q=0.45, seed=8),
        1.0, 'air')

# ================= MUEDIGKEIT: 80-95 =================
# Tiredness. The kick stops mid-phrase and does not come back for sixteen
# bars; the echo's feedback goes up and its damping down, so the chord that
# was a stab turns into weather.
s.place(s.pos(80), mdown(12, gain=0.4, f0=2600, f1=200), 1.0, 'air')
bed(80, 16, humg=1.5, dustg=0.6, seed=9)
harmony(80, 16, AEOL, gain=0.86, shineg=0.78, cutoff=1600, attack=2.2,
        decay=8.0, seed=30)
held(80, 16, gain=0.44, cutoff=2200, seed=11)
for i, b in enumerate(range(81, 96, 4)):
    offchord(b, AEOL[i % 4], gain=0.52, cutoff=1900, times=9, fb=0.70)
for b in (88, 92):                                # two footsteps, then nothing
    floor(b, gain=0.44, steps_=(0,), tailg=0.6, lpf=1400)
for b in range(92, 96):
    perc(b, gain=0.2 + 0.12 * (b - 92), sh=(6, 14))

# ================= DORISCH: 96-135 =================
# The F becomes D. One note in six minutes, and it is the natural sixth -
# the difference between a minor key that is sad and a minor key that is
# only early.
bed(96, 40, humg=0.85, dustg=1.0, seed=12)
harmony(96, 40, DOR, gain=1.0, shineg=0.72, cutoff=3000, attack=0.9, seed=40)
held(96, 40, gain=0.58, cutoff=3400, seed=13)
for b in range(96, 136):
    ph = b - 96
    u = ph / 39
    floor(b, gain=0.60 + 0.32 * u, tailg=0.7 + 0.28 * u,
          lpf=1800 + 420 * ph if ph < 8 else None,
          click=0.45 + 0.25 * u, tick=0.40 + 0.30 * u, knock=0.70)
    perc(b, gain=0.55 + 0.40 * u, sh=(2, 6, 10, 14),
         rim=(7, 15) if ph >= 4 else (), clap=(12,) if ph >= 12 else ())
for i, b in enumerate(range(99, 136, 4)):
    offchord(b, DOR[(i + 1) % 4], gain=0.42 + 0.02 * i, cutoff=3000 + 100 * i,
             fb=0.60)
s.place(s.pos(112), sweepnoise(128, gain=0.30, f0=500, f1=8000, q=0.4, seed=14),
        1.0, 'air')

# ================= ZUHAUSE: 136-159 =================
# Home. Everything leaves in the order it arrived.
bed(136, 24, humg=1.0, dustg=0.6, seed=15)
harmony(136, 24, DOR, gain=0.90, shineg=0.60, cutoff=2200, attack=1.4, seed=50)
held(136, 24, gain=0.46, cutoff=2600, seed=16)
for b in range(136, 160):
    ph = b - 136
    u = ph / 23
    floor(b, gain=0.90 - 0.70 * u, tailg=0.95 - 0.55 * u,
          lpf=9000 - 320 * ph, click=0.60 - 0.45 * u, tick=0.55 - 0.45 * u)
    perc(b, gain=0.90 - 0.75 * u, sh=(2, 6, 10, 14) if ph < 12 else (6, 14),
         rim=(7, 15) if ph < 8 else ())
for i, b in enumerate(range(139, 156, 4)):
    offchord(b, DOR[(i + 1) % 4], gain=0.44 - 0.06 * i, cutoff=2400, times=8,
             fb=0.64)

# ================= SCHLAF: 160-175 =================
# One chord, and the room it is in. The shimmer has the last word, three
# passes behind the note that caused it.
bed(160, 16, humg=1.2, seed=17)
s.place(s.pos(160), chordpad(Am, 200, cutoff=1500, attack=3.0, seed=60),
        0.72, 'pad')
s.place(s.pos(160), shine(Am, 176, decay=9.0, wet=0.6, tone=2400, passes=3,
                          fb=0.6, seed=61), 0.66, 'shine')
s.place(s.pos(160), ens([HELD], 200, gain=0.34, voices=3, cutoff=2000,
                        attack=3.5, bow=0.45, drift=1.5, seed=18), 1.0, 'lead')
for b in (160, 164):
    floor(b, gain=0.30 - 0.10 * (b - 160) / 4, steps_=(0,), tailg=0.4, lpf=900)
s.place(s.pos(168), sweepnoise(96, gain=0.22, f0=300, f1=3000, q=0.5, rev_=True,
                               seed=19), 1.0, 'air')

# ---- bus space, then the master ----
s.bus['pad']   = bus_reverb(s.bus['pad'],   decay=3.2, wet=0.26, tone=3000)
s.bus['lead']  = bus_reverb(s.bus['lead'],  decay=4.0, wet=0.34, tone=3400)
s.bus['chord'] = bus_reverb(s.bus['chord'], decay=2.4, wet=0.20, tone=2800)
s.bus['air']   = bus_reverb(s.bus['air'],   decay=3.0, wet=0.18, tone=2400)
s.bus['drums'] = bus_reverb(s.bus['drums'], decay=1.1, wet=0.09, tone=3600)
s.bus['pad']   = hp(s.bus['pad'], 150)
s.bus['shine'] = hp(s.bus['shine'], 320)          # the octaves, never the bottom
s.bus['lead']  = hp(s.bus['lead'], 300)
s.bus['chord'] = hp(s.bus['chord'], 240)
s.bus['air']   = hp(s.bus['air'], 40)
# A touch of instability on something too perfect: everything harmonic goes
# through tape, because nothing about seven in the morning is in tune.
for b in ('pad', 'shine', 'lead', 'chord'):
    s.bus[b] = tapeflutter(s.bus[b], depth_ms=0.7, rate=4.2)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)
s.bus['shine'] = side_boost(s.bus['shine'], 700, 0.6)
s.bus['pad']   = side_boost(s.bus['pad'], 600, 0.35)

ARC = [(0, -7.0), (8, -5.4), (16, -3.6), (32, -2.6), (47.9, -2.2),
       (48, -1.6), (64, -1.0), (79.9, -0.8),
       (80, -5.2), (88, -4.6), (95.9, -3.8),
       (96, -1.8), (112, -0.6), (128, 0.0), (135.9, 0.0),
       (136, -0.9), (148, -3.0), (159.9, -5.5),
       (160, -7.5), (168, -10.0), (176, -15.0)]
_bars = np.array([p[0] for p in ARC]) * BAR
_db   = np.array([p[1] for p in ARC])
_ride = 10 ** (np.interp(np.arange(s.total, dtype=np.float64), _bars, _db) / 20.0)
_ride = uniform_filter1d(_ride, int(0.030 * SR))
for b in s.bus:
    s.bus[b] = (s.bus[b] * _ride[:, None]).astype(np.float32)

GAINS = {'drums': 0.70, 'sub': 0.62, 'pad': 0.50, 'shine': 0.34,
         'chord': 0.40, 'lead': 0.34, 'air': 0.30}
s.report(GAINS)
s.ownership(3000, 16000, GAINS, 'top  3-16k')
s.ownership(200, 800, GAINS, 'mid  200-800')
# Deliberately not a club master. This is -12 LUFS with the peaks left on it:
# a record about being tired that has been limited to -6 is a lie.
s.render('dub_heimweg_118.wav', drive=1.0, duck=0.30, duck_rel=0.24,
         clip=0.0, peak=0.94, fade=6.0, gains=GAINS,
         brick=dict(gain=1.02, ceiling=0.90))
