"""RUFFNECK - jungle, G minor, 166 BPM. Not drum & bass, and the difference
is the bass.

Everything below follows from one decision: **the bassline is a tune**. In
drum & bass the bass is one note with something happening inside it, and the
drums carry the composition. Here it is the other way round - a four-bar
reggae line at 49-78 Hz with rests in it, ending on a D that pulls back to
the G, and the break's job is to run over the top of it. Written at 166,
because 174 is where the genre stopped being jungle.

Six things make it 1994 rather than 2024:

1. **The break is played before it is cut.** Bar A is the Amen as Gregory
   Coleman played it. The variations move two or three hits, not sixteen -
   and there are only nine bars of tablature on the whole record, because a
   jungle bar that has been rebuilt from scratch stops swinging.
2. **Varispeed, never time-stretch.** `idmlib.set_tempo(166)` re-reads the
   sample at the new speed, so its pitch travels with it. The break is a
   140 BPM funk record playing 3 semitones sharp, which is the sound.
3. **The pulse is not in the break.** `thump` on beats 1 and 3, tuned to the
   root, and `crack` with its 95 Hz bottom on 2 and 4, in almost every bar.
   The chops can fall apart for two beats and the body still knows where it
   is.
4. **The bass is an instrument, not a synth.** A double bass, pizzicato:
   stiffness-stretched partials, a decay rate per mode, two polarisations, a
   wooden box with four resonances, and the finger and the fingerboard at
   every attack. One phase track across the bar, so the portamento is a
   fretless slide; then split at 130 Hz across two buses, so the low half can
   be mono'd and ducked while it is still one oscillator.
5. **There is no chord instrument.** The harmony is the bass line, and
   behind it a string section with its filter shut. An offbeat organ skank
   is the reggae signature and it is also the funk keyboard vamp, and at
   166 BPM over a break the ear picks the second one.
6. **Dub is the arrangement.** Parts are thrown into an echo and the send is
   closed again; the whole record is muted and unmuted rather than written.

    intro       0-15   vinyl, a siren, the break through a closed filter
    roll-in    16-31   the kit lands; the tune from 24
    DROP 1     32-63   the break and the bass line, and nothing else
    dub        64-79   drums out, the strings arrive, everything in echo
    build 1    80-87   ratchets and a riser, then a bar with a hole in it
    DROP 2     88-119  the second deck on top, the orchestra hit, the airhorn
    ragga     120-135  stripped: bass forward, four bars of halftime snare
    dark      136-139  no drums at all - the quietest bars on the record
    build 2   140-143  the rewind
    DROP 3    144-175  the peak, at 69% of the way through
    roll-out  176-191
    outro     192-207  DJ-friendly, the filter closing

The lowest section sits immediately before the highest, and the difference
between them is written as a gain ride in decibels per bar over the finished
buses - not as per-part gains, which do not sum to a section.
"""
import numpy as np
from junglelib import *

s = Session(208, tail=3.0)

# ================================================================ G minor
G1, A1, Bb1, C2, D2, Eb2, F2 = 31, 33, 34, 36, 38, 39, 41
G2, Bb2, C3, D3, Eb3, F3 = 43, 46, 48, 50, 51, 53
A3, G3, Bb3, C4, D4, Eb4, F4, G4, A4, Bb4, D5 = 57, 55, 58, 60, 62, 63, 65, 67, 69, 70, 74

SW = dict(swing=0.08, swing_steps=(6, 14))

# The line. One rhythmic cell - a long root, a shorter root, a lift, and a
# note across the bar line - repeated for four bars and moved to the bVI in
# bar 3 with its rhythm untouched. Three of the four hits in every bar are
# the root, and the spacings are 6, 3, 5, 2 rather than 4, 4, 4, 4: a bass
# that puts a different degree on every fourth sixteenth is not a riff, it
# is a scale being picked through, and the ear hears an arpeggiator.
#
# The gaps are as written as the notes. Steps 5, 11, 12 and 13 are silent in
# most bars, and that silence is what the kick lands in.
#            step  midi  length
RIFF = [
    figure([(0, G1, 5), (6, G1, 3), (9, Bb1, 2), (14, G1, 2)], **SW),
    figure([(0, G1, 5), (6, G1, 3), (9, Bb1, 2), (13, C2, 1), (14, D2, 2)], **SW),
    figure([(0, Eb2, 5), (6, Eb2, 3), (9, Eb2, 2), (14, D2, 2)], **SW),
    figure([(0, Bb1, 5), (6, Bb1, 3), (9, C2, 2), (13, D2, 3)], **SW),
]
# The same cell with its middle taken out, for the sections where the gap
# does more than the notes would.
RIFF_LOW = [
    figure([(0, G1, 6), (9, Bb1, 3)]),
    figure([(0, G1, 6), (9, Bb1, 3)]),
    figure([(0, Eb2, 6), (9, Eb2, 3)]),
    figure([(0, Bb1, 6), (13, D2, 3)]),
]

# There is no chord instrument on this record. Three passes put one there -
# an offbeat organ skank, then a quieter one, then a darker and sparser one -
# and it was rejected every time, correctly: a keyboard chopping chords at
# 166 BPM over a break is a funk arrangement, and the jungle records this is
# written after mostly have no chord instrument at all. The harmony is the
# bass line, and behind it a string section with the filter shut.
STRINGS = [(G3, Bb3, D4, G4, Bb4), (G3, Bb3, D4, G4, Bb4),
           (G3, Bb3, Eb4, G4, Bb4), (G3, Bb3, D4, F4, Bb4)]

TUNE = 49.0                      # the kick under the break, tuned to G1


# ============================================================== the break
# Nine bars of tablature for a five-minute record. Every one of them is bar A
# with two or three hits moved: the swing lives in the recording, and a bar
# rebuilt from scratch loses it.
#            beat 1  2    3    4
BARS = {
    'A': "K.kh Shhh hhqQ D.hh",     # the Amen, as played
    'B': "K.kh Shhh hhqQ D.sh",     # last ghost becomes a snare
    'C': "K.kh Shhi hKqQ D.sd",     # an extra kick pushed into beat 3
    'D': "KhkS .hhq KhqQ Ds.h",     # snare pulled onto step 3 - the shuffle
    'E': "K.kh Sh.G kKqQ Dshs",     # busier out of the bar
    'F': ".hkh Shhh hKqQ D.hX",     # the downbeat left empty
    'G': "K.kh SshS hhqQ DsdS",     # double snares - the ragga bar
    'H': "K..h S... ..q. D..h",     # stripped, for the dub
    'R': "K.kh Shhh hhqQ Dsss",     # rolls out of the bar
}
for _k, _v in BARS.items():
    assert len(_v.replace(' ', '')) == 16, (_k, len(_v.replace(' ', '')))

# The second turntable: the same bar at double speed, band-passed, so its
# ghost notes interleave with the ones underneath. Two copies fit one bar
# exactly, which is why the interval is an octave and not a fifth.
TOP = deck(amen.bar(0), 12.0, lo=1150.0, hi=7600.0, steps_=16)
TOP2 = deck(amen.bar(3), 12.0, lo=1150.0, hi=7600.0, steps_=16)

# The break through the sampler that made the genre. 12 bits, truncated, and
# a converter that stops at 11 kHz.
PLATE = dict(bits=12, down=1, hi=11200.0, drive=1.10)

cthump, ccrack = cached(thump), cached(crack)


def kit(b, tab='A', gain=1.0, hpf=168.0, locks=None, seed=0, ghost=1.0,
        width=1.0, top=0.0, sc=True, kicks=(0, 8), snares=(4, 12),
        thumpg=1.0, crackg=1.0, swing=0.0):
    """One bar: the chopped break, and the pulse underneath it.

    `humanise=0` is not an oversight. `edit()` defaults to nudging every hit
    by up to a hundredth of a bar, which is right in drill'n'bass, where the
    break is the only kit on the record and the scatter is the point. Here
    there is a clean kick sitting under the break's own kick and a clean
    snare under its snare, both exactly on the grid - so a jitter of fourteen
    milliseconds is not feel, it is a flam, and because it is redrawn every
    bar the two layers drift against each other for five minutes. The break
    is a recording of a man playing drums; it arrived with its feel already
    in it.
    """
    edit(s, b, BARS[tab], locks=locks, gain=gain, bus='break', hpf=hpf,
         seed=seed, ghost=ghost, width=width, swing=swing, humanise=0.0)
    for k in kicks:
        t = s.pos(b, k)
        s.place(t, cthump(3.4, tune=TUNE, decay=0.155, drive=1.7),
                gain * thumpg * (1.0 if k == 0 else 0.88), 'drums')
        if sc:
            s.hit(t)
    for k in snares:
        s.place(s.pos(b, k),
                ccrack(3.0, tune=196.0, bottom=0.66, room=0.30, bright=0.70,
                       seed=(seed + k) % 7),
                gain * crackg * (1.0 if k in (4, 8, 12) else 0.6), 'drums')
    if top:
        s.place(s.pos(b), TOP2 if b % 4 == 3 else TOP, gain * top, 'break')


_PARTS = {}


def bass(b, i, sub_g=1.0, wood=1.0, riff=None, dur=22):
    """The tune, on one instrument cut in half.

    It is a double bass, not a keyboard: a stiffness-stretched string with a
    decay rate per mode, two polarisations, a wooden box with four
    resonances, and the finger and the fingerboard at every attack. One phase
    track across the whole bar, so the portamento between notes is a fretless
    slide and an attack re-excites a string that never stopped.

    Then split at 130 Hz and sent to two buses, so the low half can be
    collapsed to mono and ducked against the kick while the wood keeps its
    width - but it is still ONE oscillator. A separate sine playing the same
    note is a second oscillator at the same frequency with an unrelated
    phase, and two of those cancel rather than add.

    22 steps rather than 16, so the last note of a bar is still ringing when
    the next one starts: the anticipation is the whole reason the line leans
    forward, and cutting it at the bar line kills it.
    """
    notes, g16 = (riff or RIFF)[i % 4]
    gp = tuple(g16) + (g16[-1],) * (dur - 16)
    key = (notes, gp, dur)
    if key not in _PARTS:
        _PARTS[key] = split(contrabass(notes, dur, gatep=gp, sub=0.22,
                                       glide=0.028, decay=2.2, seed=3), 130.0)
    lo, hi = _PARTS[key]
    s.place(s.pos(b), lo, sub_g, 'sub')
    if wood:
        s.place(s.pos(b), hi, wood, 'bass')



def scratches(b, st, seg=None, n=3, span=1.0, cycles=(2.0, 3.5, 5.0),
              depth=2.0, gain=0.60, pan=0.0, bus='fx'):
    """A scratch phrase: one slice dragged under the needle at three
    different rates. `core.scratch` reverses the read whenever the rate goes
    negative, so the pitch travels with the hand - which is the whole gesture,
    and the thing a reversed copy of the sample does not give you."""
    src = CHARS['S'] if seg is None else seg
    src = src[:max(int(span * STEP), 256)]
    for j in range(n):
        y = scratch(src, cycles=cycles[j % len(cycles)], depth=depth,
                    gain=gain * (1.0 if j % 2 == 0 else 0.78))
        s.place(s.pos(b, st + j * span), panned(y, pan * (1 if j % 2 else -1)),
                1.0, bus)


def atmos(b, n=1, g=1.0, seed=0):
    s.place(s.pos(b), crackle(16 * n, gain=0.9), 0.32 * g, 'atmos')
    s.place(s.pos(b), hush(16 * n, gain=1.0, seed=seed, lo=500, hi=5200),
            0.9 * g, 'atmos')


# ================================================================ 0-15 intro
# A DJ tool: sixteen bars of atmosphere and a break behind a closed filter,
# with nothing in the mid-range for the other record to fight.
for b in range(16):
    atmos(b, 1, g=1.0, seed=b)
for b in range(0, 16, 4):
    s.place(s.pos(b), drone(midi(G1), 64, gain=0.5), 0.30, 'atmos')
for b in range(8, 16):
    i = b - 8
    cut = 260 + 130 * i                              # the filter opening
    y = lp(hp(dubplate(amen.bar(b % 2), **PLATE), 190, 2), cut, 4)
    s.place(s.pos(b), y, 0.42 + 0.05 * i, 'break')
    if b >= 12:
        s.place(s.pos(b, 4), ccrack(3.0, bottom=0.5, seed=b % 7), 0.45, 'drums')
        s.place(s.pos(b, 12), ccrack(3.0, bottom=0.5, seed=(b + 3) % 7), 0.40, 'drums')
throw(s, s.pos(2, 4), dubsiren(5, f0=760.0, lfo=4.5, gain=0.55), 0.5,
      times=5, delay_steps=3.0, fb=0.55)
throw(s, s.pos(10, 12), dubsiren(4, f0=980.0, lfo=7.0, gain=0.5, shape='square'),
      0.42, times=4, delay_steps=3.0, fb=0.5)
s.place(s.pos(6), whoosh(16, gain=0.5), 0.5, 'fx')
# The deck brought up to speed by hand - the first thing on the record.
s.place(s.pos(4), spin(dubplate(amen.bar(0), **PLATE), r0=0.40, r1=1.0,
                       curve=1.5), 0.42, 'break')
scratches(11, 12, n=2, span=2.0, cycles=(2.0, 3.0), gain=0.55, pan=0.4)
s.place(s.pos(14), riser(32, gain=0.5, f0=200.0, f1=1400.0), 0.5, 'fx')
s.place(s.pos(16) - int(2 * STEP), subdrop(4, f0=80.0, f1=27.0, gain=0.9), 0.7, 'fx')


# ============================================================= 16-31 roll-in
# The kit arrives; the tune waits until 24. Sixteen bars is a long time to
# hold a groove back, and it is what makes bar 32 land.
for b in range(16, 32):
    i = b - 16
    atmos(b, 1, g=0.7, seed=b)
    kit(b, 'A' if i % 4 < 3 else 'B', gain=0.80 + 0.012 * i,
        hpf=280 - 7 * i, seed=b, ghost=0.85, thumpg=0.85 if i < 4 else 1.0)
    if i >= 8:
        bass(b, b, sub_g=0.72 + 0.03 * (i - 8), wood=0.45 if i >= 10 else 0.0,
             riff=RIFF_LOW)
throw(s, s.pos(20, 12), dubsiren(4, f0=840.0, lfo=5.5, gain=0.5), 0.45,
      times=4, delay_steps=3.0)
scratches(30, 8, n=4, span=1.0, gain=0.62, pan=0.35)
roll(s, 31, 12, 4, spacing=1.0, gain=0.75, p1=1.25, bus='break')
s.place(s.pos(32) - int(1.5 * STEP), subdrop(3, f0=85.0, f1=26.0, gain=1.0),
        0.85, 'fx')


# ============================================================== 32-63 DROP 1
# The break and the bass line, and nothing else, for thirty-two bars.
# That is what a jungle drop is.
DROP1 = ['A', 'A', 'A', 'B', 'A', 'C', 'A', 'E',
      'A', 'A', 'D', 'B', 'A', 'C', 'G', 'R']
s.place(s.pos(32), impact(20, gain=0.8), 0.55, 'fx')
s.place(s.pos(32), crash808(24, gain=0.55), 0.42, 'drums')
for b in range(32, 64):
    i = b - 32
    atmos(b, 1, g=0.45, seed=b)
    kit(b, DROP1[i % 16], gain=1.0, hpf=168, seed=b,
        ghost=0.92, top=0.0, width=1.0,
        locks={14: dict(rat=3, curve='accel', p1=1.35, g1=0.6)}
        if i % 16 == 15 else None)
    bass(b, b)
for b in (40, 56):
    throw(s, s.pos(b, 6), dubsiren(4, f0=880.0, lfo=6.0, gain=0.5), 0.40,
          times=4, delay_steps=3.0, fb=0.5)
s.place(s.pos(48), crash808(20, gain=0.5), 0.34, 'drums')
# Two bars of the break thrown to a long echo and left there, which is the
# cheapest way to make a thirty-two bar loop stop being a loop.
throw(s, s.pos(55, 12), shape(CHARS['S'], hpf=200, pan=0.3), 0.55, times=5,
      delay_steps=3.0, fb=0.58)
scratches(43, 12, n=2, span=2.0, cycles=(2.5, 4.0), gain=0.5, pan=-0.4)
scratches(59, 12, n=4, span=1.0, gain=0.55, pan=0.4, seg=CHARS['C'])
roll(s, 63, 8, 8, spacing=1.0, gain=0.8, p1=1.5, bus='break')


# ================================================================ 64-79 dub
# Drums out. What is left is the tune, a chord thrown into an echo, and a
# string section with its filter shut - the quietest sixteen bars until 136.
for b in range(64, 80):
    i = b - 64
    atmos(b, 1, g=1.0, seed=b)
    bass(b, b, sub_g=0.85, wood=0.42, riff=RIFF_LOW)
    if i % 4 == 0:
        s.place(s.pos(b), ens([midi(n) for n in STRINGS[b % 4]], 68,
                              gain=0.55, voices=3, cutoff=1250, attack=0.55,
                              bow=0.6, drift=0.7, seed=b), 0.62, 'pad')
    if i >= 6:
        # Dub mutes everything except the drum and the bass. The kick keeps
        # beats 1 and 3 through the whole breakdown: a section that drops the
        # pulse does not read as space, it reads as the record stopping.
        for k in (0, 8):
            tt = s.pos(b, k)
            s.place(tt, cthump(3.4, tune=TUNE, decay=0.165),
                    (0.52 if i < 10 else 0.72) * (1.0 if k == 0 else 0.86),
                    'drums')
            s.hit(tt)
        for k in (4, 12):
            s.place(s.pos(b, k),
                    ccrack(3.0, bottom=0.58, room=0.62, bright=0.62,
                           seed=(b + k) % 7),
                    (0.40 if i < 10 else 0.56) * (1.0 if k == 4 else 0.86),
                    'drums')
    if i >= 12:
        kit(b, 'H', gain=0.66, hpf=210, seed=b, ghost=0.6,
            kicks=(), snares=(), sc=False)
throw(s, s.pos(70, 6), dubsiren(6, f0=700.0, lfo=3.2, gain=0.6), 0.50,
      times=6, delay_steps=3.0, fb=0.60)
# A snare held four times its own length: the S950 stretch, artefacts left in.
s.place(s.pos(68, 8), smear(CHARS['S'], 4.0, gain=0.55), 0.34, 'atmos')
s.place(s.pos(74), smear(amen.get(0, 4, 4), 3.0, tone=5200, gain=0.5), 0.28, 'atmos')


# ============================================================= 80-87 build 1
for b in range(80, 88):
    i = b - 80
    atmos(b, 1, g=0.6, seed=b)
    kit(b, ['A', 'A', 'B', 'A', 'C', 'B', 'E', 'R'][i], gain=0.70 + 0.035 * i,
        hpf=200 - 4 * i, seed=b, ghost=0.9, sc=True)
    bass(b, b, sub_g=0.85, wood=0.65)
    s.place(s.pos(b), ens([midi(n) for n in STRINGS[b % 4]], 18, gain=0.40,
                          voices=3, cutoff=900 + 130 * i, attack=0.30,
                          bow=0.5, seed=b), 0.42, 'pad')
s.place(s.pos(84), riser(64, gain=0.55, f0=240.0, f1=2600.0), 0.55, 'fx')
scratches(85, 8, n=4, span=1.0, gain=0.62, pan=0.35)
roll(s, 86, 0, 12, spacing=1.2, gain=0.7, accel=True, p1=1.4, bus='break')
roll(s, 87, 0, 14, spacing=1.0, gain=0.85, accel=True, p1=1.8, bus='break')
# The last beat of the build is a hole. Nothing is placed in bar 87 beat 4,
# and the ride takes the whole mix down 4 dB through it.
s.place(s.pos(88) - int(2 * STEP), subdrop(4, f0=90.0, f1=25.0, gain=1.0),
        0.9, 'fx')
s.place(s.pos(88) - int(4 * STEP), rev(crash808(8, gain=0.8)), 0.45, 'fx')


# ============================================================== 88-119 DROP 2
# The second deck comes in over the top. No lead line: a rave hoover, whose
# whole identity is a stab sliding four semitones into pitch, is a rave
# signifier and not a jungle one, and it is the loudest thing on a record
# that is not in tune with anything else on it.
DROP2 = ['A', 'C', 'A', 'B', 'D', 'A', 'C', 'E',
      'A', 'C', 'G', 'B', 'A', 'D', 'E', 'R']
s.place(s.pos(88), impact(20, gain=0.95), 0.62, 'fx')
s.place(s.pos(88), crash808(24, gain=0.6), 0.45, 'drums')
s.place(s.pos(88), airhorn(7, note=67, gain=0.75), 0.30, 'lead')
s.place(s.pos(88), orchhit(G3, 3, gain=0.7), 0.26, 'lead')
for b in range(88, 120):
    i = b - 88
    atmos(b, 1, g=0.40, seed=b)
    kit(b, DROP2[i % 16], gain=1.0, hpf=170, seed=b + 40, top=0.17, ghost=0.92,
        locks={10: dict(rat=4, curve='accel', p1=1.4, g1=0.55)}
        if i % 16 == 11 else
        ({14: dict(rat=5, curve='accel', p1=1.6, g1=0.5)} if i % 16 == 15 else None))
    bass(b, b)
s.place(s.pos(104), crash808(20, gain=0.5), 0.34, 'drums')
for b in (96, 112):
    throw(s, s.pos(b, 14), dubsiren(4, f0=920.0, lfo=6.5, gain=0.5,
                                    shape='square'), 0.42, times=4,
          delay_steps=3.0, fb=0.5)
throw(s, s.pos(111, 12), shape(CHARS['D'], hpf=220, pan=-0.35), 0.5, times=5,
      delay_steps=3.0, fb=0.56)
scratches(99, 12, n=2, span=2.0, cycles=(3.0, 4.5), gain=0.52, pan=0.45)
scratches(115, 12, n=4, span=1.0, gain=0.58, pan=-0.4, seg=CHARS['C'])
roll(s, 119, 8, 8, spacing=1.0, gain=0.85, p1=1.5, bus='break')


# ============================================================= 120-135 ragga
# Stripped back: the break loses its ghosts, the bass comes forward, and four
# bars in the middle take the snare to beat 3 only. The kick stays on 1 and 3
# through all of it, because a halftime snare over a halftime kick is a slow
# record whatever the tempo says.
for b in range(120, 136):
    i = b - 120
    atmos(b, 1, g=0.6, seed=b)
    # The contrast here is density and level, NOT a halftime snare. Taking
    # the backbeat to beat 3 alone leaves two beats with nothing under them,
    # and that reads as beats being skipped rather than as space - so the
    # kick stays on 1 and 3 and the snare on 2 and 4 through all sixteen
    # bars, and what changes is how much of the break is playing.
    ragga = 8 <= i < 12
    kit(b, 'G' if ragga else ('A' if i % 4 < 2 else 'B'),
        gain=0.86, hpf=180, seed=b + 90, ghost=0.50 if not ragga else 0.62,
        crackg=1.05 if ragga else 1.0)
    bass(b, b, sub_g=1.0, wood=0.85, riff=RIFF if i % 8 < 4 else RIFF_LOW)
    if i % 8 == 0:
        s.place(s.pos(b), ens([midi(n) for n in STRINGS[b % 4]], 132, gain=0.42,
                              voices=3, cutoff=1050, attack=0.6, bow=0.5,
                              seed=b), 0.44, 'pad')
throw(s, s.pos(122, 6), dubsiren(6, f0=660.0, lfo=3.6, gain=0.6), 0.52,
      times=6, delay_steps=3.0, fb=0.60)
s.place(s.pos(134), smear(amen.get(3, 10, 4), 3.5, tone=5600, gain=0.5),
        0.30, 'atmos')


# ============================================================== 136-143 dark
# Four bars with no drums on them at all - the trough, and it is here rather
# than in the dub section because the thing it has to make big is bar 144.
for b in range(136, 140):
    atmos(b, 1, g=1.0, seed=b)
    bass(b, b, sub_g=0.80, wood=0.35, riff=RIFF_LOW)
    # No break at all for four bars, but the kick stays. This is the quietest
    # place on the record and it still has a beat you could walk to.
    for k in (0, 8):
        tt = s.pos(b, k)
        s.place(tt, cthump(3.4, tune=TUNE, decay=0.17), 0.62, 'drums')
        s.hit(tt)
    s.place(s.pos(b, 12), ccrack(3.0, bottom=0.55, room=0.7, bright=0.5,
                                 seed=b % 7), 0.30, 'drums')
    if b == 136:
        s.place(s.pos(b), ens([midi(n) for n in STRINGS[0]], 64, gain=0.62,
                              voices=4, cutoff=1000, attack=0.9, bow=0.7,
                              drift=0.7, seed=5), 0.70, 'pad')
        s.place(s.pos(b), ens([midi(n) for n in STRINGS[3]], 64, gain=0.30,
                              voices=3, cutoff=800, attack=1.4, bow=0.6,
                              seed=9), 0.34, 'pad')
throw(s, s.pos(136, 8), dubsiren(8, f0=560.0, lfo=2.4, gain=0.6), 0.48,
      times=6, delay_steps=3.0, fb=0.62)
s.place(s.pos(138), smear(amen.get(0, 4, 8), 4.0, tone=4800, gain=0.55),
        0.30, 'atmos')

# ---- 140-143 the build, and the rewind ----
for b in range(140, 144):
    i = b - 140
    atmos(b, 1, g=0.7, seed=b)
    kit(b, ['A', 'B', 'E', 'R'][i], gain=0.72 + 0.06 * i, hpf=200 - 8 * i,
        seed=b, ghost=0.8)
    bass(b, b, sub_g=0.9, wood=0.7)
s.place(s.pos(140), riser(64, gain=0.60, f0=220.0, f1=3000.0), 0.55, 'fx')
scratches(141, 8, n=4, span=1.0, gain=0.64, pan=0.4)
roll(s, 142, 0, 12, spacing=1.2, gain=0.72, accel=True, p1=1.4, bus='break')
roll(s, 143, 0, 16, spacing=0.9, gain=0.88, accel=True, p1=1.9, bus='break')
# Two bars of the break spun backwards into the downbeat of 144.
rewind_into(s, 144, np.concatenate([dubplate(amen.bar(0), **PLATE),
                                    dubplate(amen.bar(3), **PLATE)]),
            gain=0.62, accel=3.6)
s.place(s.pos(144) - int(2 * STEP), subdrop(4, f0=95.0, f1=24.0, gain=1.0),
        0.95, 'fx')


# ============================================================= 144-175 DROP 3
# The peak. Everything that has been on the record, plus the strings under it
# for the first time in a drop - which is the one element drop 2 did not have.
DROP3 = ['A', 'C', 'G', 'B', 'D', 'A', 'C', 'E',
      'A', 'G', 'D', 'B', 'C', 'A', 'E', 'R']
s.place(s.pos(144), impact(24, gain=1.0), 0.68, 'fx')
s.place(s.pos(144), crash808(28, gain=0.65), 0.48, 'drums')
s.place(s.pos(144), airhorn(8, note=67, gain=0.8), 0.32, 'lead')
s.place(s.pos(144), orchhit(G3, 3, gain=0.75), 0.28, 'lead')
for b in range(144, 176):
    i = b - 144
    atmos(b, 1, g=0.35, seed=b)
    kit(b, DROP3[i % 16], gain=1.0, hpf=172, seed=b + 130, top=0.19, ghost=0.92,
        locks={10: dict(rat=4, curve='accel', p1=1.4, g1=0.55)}
        if i % 16 == 9 else
        ({12: dict(rat=6, curve='accel', p1=1.7, g1=0.45)} if i % 16 == 15 else None))
    bass(b, b)
    if i % 8 == 0:
        s.place(s.pos(b), ens([midi(n) for n in STRINGS[b % 4]], 132, gain=0.40,
                              voices=3, cutoff=1150, attack=0.55, bow=0.5,
                              seed=b), 0.40, 'pad')
s.place(s.pos(160), crash808(20, gain=0.55), 0.36, 'drums')
throw(s, s.pos(151, 12), shape(CHARS['X'], hpf=220, pan=0.35), 0.52, times=5,
      delay_steps=3.0, fb=0.56)
scratches(155, 12, n=2, span=2.0, cycles=(2.5, 4.0), gain=0.55, pan=-0.4)
scratches(171, 12, n=4, span=1.0, gain=0.60, pan=0.42, seg=CHARS['C'])
throw(s, s.pos(168, 6), dubsiren(5, f0=1020.0, lfo=7.5, gain=0.5,
                                 shape='square'), 0.44, times=4,
      delay_steps=3.0, fb=0.5)
roll(s, 175, 8, 8, spacing=1.0, gain=0.85, p1=1.6, bus='break')


# =========================================================== 176-191 roll-out
for b in range(176, 192):
    i = b - 176
    atmos(b, 1, g=0.55, seed=b)
    kit(b, ['A', 'B', 'A', 'D', 'A', 'C', 'A', 'B'][i % 8], gain=0.95,
        hpf=172, seed=b + 60, top=0.13 if i < 8 else 0.0, ghost=1.0 - 0.03 * i)
    bass(b, b, sub_g=1.0, wood=0.85 if i < 10 else 0.5,
         riff=RIFF if i < 8 else RIFF_LOW)
throw(s, s.pos(184, 14), dubsiren(4, f0=800.0, lfo=5.0, gain=0.5), 0.42,
      times=5, delay_steps=3.0, fb=0.55)
s.place(s.pos(188), smear(amen.get(0, 4, 4), 3.0, tone=5000, gain=0.5),
        0.26, 'atmos')


# =============================================================== 192-207 outro
# Mirrors the intro: the filter closes, the tune goes, the break is left
# alone for a DJ to mix out of.
for b in range(192, 208):
    i = b - 192
    atmos(b, 1, g=0.8 + 0.02 * i, seed=b)
    fade = max(0.0, 1 - i / 16.0)
    cut = 12000 - 640 * i
    edit(s, b, BARS['A' if i % 4 < 3 else 'H'], gain=0.9 * (0.55 + 0.45 * fade),
         bus='break', hpf=175, seed=b + 200, ghost=0.8, humanise=0.0)
    if i < 12:
        t = s.pos(b, 0)
        s.place(t, cthump(3.4, tune=TUNE, decay=0.155), 0.95 * fade + 0.2, 'drums')
        s.hit(t)
        s.place(s.pos(b, 8), cthump(3.4, tune=TUNE, decay=0.155), 0.8 * fade + 0.15, 'drums')
        s.place(s.pos(b, 4), ccrack(3.0, bottom=0.6, seed=b % 7), 0.85 * fade + 0.15, 'drums')
        s.place(s.pos(b, 12), ccrack(3.0, bottom=0.6, seed=(b + 2) % 7), 0.8 * fade + 0.12, 'drums')
    if i < 8:
        bass(b, b, sub_g=0.85 * fade + 0.15, wood=0.5 * fade, riff=RIFF_LOW)
s.place(s.pos(204), drone(midi(G1), 64, gain=0.45), 0.26, 'atmos')
scratches(195, 12, n=2, span=2.0, cycles=(2.0, 3.0), gain=0.45, pan=0.4)
# The deck stopped, which is how a dubplate ends.
s.place(s.pos(206), tape_stop(dubplate(amen.bar(0), **PLATE), stop_s=1.4),
        0.40, 'break')
throw(s, s.pos(196, 6), dubsiren(5, f0=700.0, lfo=4.0, gain=0.5), 0.40,
      times=6, delay_steps=3.0, fb=0.6)
# The break closes down over the last four bars.
s.bus['break'][s.pos(192):] = sweep_lp(s.bus['break'][s.pos(192):], 13000, 900,
                                       curve=1.6)


# ================================================================== the mix
s.bus['pad'] = bus_reverb(s.bus['pad'], decay=3.4, wet=0.36, tone=2800)
s.bus['atmos'] = bus_reverb(s.bus['atmos'], decay=2.6, wet=0.26, tone=3000)
s.bus['lead'] = bus_reverb(s.bus['lead'], decay=1.6, wet=0.22, tone=4200)
s.bus['fx'] = bus_reverb(s.bus['fx'], decay=2.2, wet=0.22, tone=3800)
# A short room on the break so the chops read as one kit in one place, and
# nothing longer: at 166 BPM a tail over half a second is a wash across the
# next two hits.
s.bus['break'] = bus_reverb(s.bus['break'], decay=0.42, wet=0.13, tone=5200)

# The sub is the record: mono, compressed gently so the tune is even, and
# nothing above 200 Hz.
s.bus['sub'] = compress(mono_below(s.bus['sub'], 220), thresh=0.46, ratio=3.0,
                        attack=0.005, release=0.10)
# The wood: the half of the double bass above 130 Hz. What identifies the
# instrument is not its fundamental - the sub bus has that, off the same
# oscillator - it is the box, so the two lifts are on the body resonances
# rather than anywhere a bass EQ preset would put them.
s.bus['bass'] = peak_eq(peak_eq(s.bus['bass'], 250, 1.5, 0.9), 700, 2.0, 0.8)
s.bus['bass'] = mono_below(hp(s.bus['bass'], 110, 2), 170)
# The break is the loudest thing on a jungle record and it has to be heard as
# a KIT, which means the bands the ear reads a stick and a skin in: 1.6 kHz
# for the snare's body, 3.4 kHz for the front of a hat. 320 Hz comes down
# because that is where the bassline lives, and the air shelf is gentle -
# this recording has a ride ringing through every hit of it, so brightness
# taken broadly comes back as a wash rather than as hats.
s.bus['break'] = hp(s.bus['break'], 150, 2)
s.bus['break'] = peak_eq(s.bus['break'], 320, -2.0, 0.9)
s.bus['break'] = peak_eq(s.bus['break'], 1600, 3.0, 0.7)
s.bus['break'] = peak_eq(s.bus['break'], 3400, 2.0, 0.6)
s.bus['break'] = shelf(s.bus['break'], 9000, 2.0, 'high')
s.bus['break'] = compress(s.bus['break'], thresh=0.22, ratio=3.0, attack=0.012,
                          release=0.115, report=True, label='break bus')
# 7 kHz is where that ride stops being bright and starts being painful.
s.bus['break'] = peak_eq(s.bus['break'], 7000, -1.8, 0.8)
s.bus['drums'] = mono_below(peak_eq(hp(s.bus['drums'], 32, 2), 300, -1.5, 0.9), 170)
s.bus['pad'] = shelf(hp(s.bus['pad'], 240, 2), 4000, -2.0, 'high')
s.bus['lead'] = hp(s.bus['lead'], 180, 2)
s.bus['atmos'] = hp(s.bus['atmos'], 260, 2)
s.bus['fx'] = hp(s.bus['fx'], 28, 2)

# Jungle is a bass culture, but the LOUDEST thing on the record is the break.
# The first pass had it 8 dB under the kick layer and 10 under the sub, which
# measured as 54% of the mix below 120 Hz and 0.9% between 800 Hz and 3 kHz -
# a bass record with a break hiding behind it.
GAINS = {'break': 1.90, 'drums': 0.55, 'sub': 0.56, 'bass': 0.42,
         'lead': 1.20, 'pad': 1.90, 'fx': 0.90, 'atmos': 2.20}

# ---- the ride ----
# Section contrast is a level, so it is written as one. Each drop is preceded
# by a dip of two to four decibels half a bar wide: the hole is what the
# arrival lands in, and no arrangement of parts produces it.
ARC = [(0, -10.5), (8, -8.5), (15.5, -7.0),
       (16, -6.2), (24, -4.4), (31.0, -3.4), (31.6, -6.6),
       (32, -1.4), (56, -1.4), (63.4, -2.6),
       (64, -8.6), (72, -7.4), (79.6, -5.6),
       (80, -5.0), (86, -3.2), (87.5, -7.4),
       (88, -0.8), (112, -0.8), (119.4, -2.0),
       (120, -4.2), (127.9, -4.6), (128, -3.6), (135.4, -3.4),
       (136, -12.5), (139.0, -11.0),
       (140, -6.4), (143.0, -4.2), (143.6, -7.6),
       (144, 0.0), (168, 0.0), (175.4, -1.4),
       (176, -2.4), (191, -4.2),
       (192, -6.0), (200, -9.0), (207, -15.0)]
for _b in s.bus:
    s.bus[_b] = ride(s.bus[_b], ARC)

s.report(GAINS)
s.ownership(3000, 16000, GAINS)
s.ownership(60, 200, GAINS, label='60-200 Hz')

# The clipper takes the break's transients off first so the limiter is not
# ducking a whole bar to catch one sample, then 2.5:1 glue, then a
# look-ahead limiter detecting on a 4x upsample. Jungle is a dynamic genre -
# the target is -8 LUFS with the PLR still in the sevens, not -6 flat.
s.render('jungle_ruffneck_166.wav', drive=0.0, duck=0.42, duck_rel=0.095,
         limit=0.0, peak=0.99, gains=GAINS, clip=1.70, fade=2.4,
         comp=dict(thresh=0.42, ratio=2.2, attack=0.010, release=0.120,
                   makeup=1.10),
         brick=dict(gain=1.14, ceiling=0.89, release=0.080))
