"""GLAVNAYA SCENA - uplifting trance at 138 BPM, F# minor.

The main stage, half past midnight, and the record everyone came for. This is
the most unashamed thing in the catalogue: no dark register, no menace, no
holes left deliberately in the spectrum. Trance is the one genre here whose
entire craft is spent on a single gesture - accumulate, withhold, release -
and the whole arrangement is built to make one moment, bar 192, land as hard
as fifty thousand people can take.

Everything follows from that one decision.

THE SHAPE. Thirteen and a half decibels between the quietest bar and the
loudest, which is more contrast than any other record here. Bar 128 is the
floor: the drums stop dead after a bridge that had already been thinning for
sixteen bars, and what is left is a pad, a string section and a lead melody
with nothing under it. Bar 192 is the roof, at 75% of the way through, and
between them is a build thirty-two bars long. A drop is only enormous because
of what preceded it; the breakdown is not a rest, it is the mechanism.

THE HARMONY IS DELIBERATELY PLAIN. `i - bVI - bIII - bVII` in F# minor is
F#m - D - A - E, two bars each. Those are also `vi - IV - I - V` in A major,
and that ambiguity is the euphoria: the bass anchors the minor, the lead lands
on the notes that read major, and the same four chords are heard as sad or
triumphant depending only on which voice you follow. Sophistication would kill
it. There is not one seventh chord in the record.

THE ROLLING BASS is the engine. Three sixteenths after every kick - the kick
owns steps 0, 4, 8 and 12 and the bass owns everything else - so the low band
never stops moving while the pulse stays unambiguous. It is rendered as one
phase track per eight bars with the sub taken as sin(ph/2) off that same
track, so the octave is the character layer cut in half rather than a second
oscillator underneath it.

THE LEAD is one melody, stated six times across the record and never once at
full strength before bar 192. It appears at bar 56 as a two-bar fragment
behind a filter, it plays through the first drop in a single register with the
top rolled off, it is exposed alone and almost dry in the breakdown, and only
in the climax does it arrive in three octaves at once. Sixteen bars, an arch,
one climax note - the E6 in bar 5 - and it ends on the ninth of the E chord,
which is unresolved, which is why the loop has to come round again.

    INTRO | PULSE | GROOVE | ASCENT | BUILD I | DROP I (32) | BRIDGE
          | BREAKDOWN (32) | BUILD II (32) | CLIMAX (48) | OUTRO

256 bars, 7:25. Quietest bar 128; peak bar 192; the last beat before it is
empty, which is the oldest trick in the genre and still the one that works.
"""
import numpy as np
from trancelib import *

set_tempo(138)
np.random.seed(1380)

Session.DUCKED = {'bass': 1.00, 'pad': 0.58, 'lead': 0.42, 'arp': 0.30,
                  'air': 0.34, 'music': 0.50}

# F# natural minor from F#1 = MIDI 30 (46.25 Hz): F# G# A B C# D E.
# The root is where a club subwoofer sits best, and the kick is tuned to it.
ROOT = 46.25

# --- the four chords, two bars each ---------------------------------------
# Voice-led rather than transposed: F# and A are held from i into bVI, A is
# held from bVI into bIII, E is held from bIII into bVII. The top line is
# F# F# E E - it moves twice in eight bars, which is what lets a supersaw
# chord sit under a melody without arguing with it.
PAD = ((54, 57, 61, 66),        # i    F#m   F#3 A3 C#4 F#4
       (54, 57, 62, 66),        # bVI  D/F#  F#3 A3 D4  F#4
       (52, 57, 61, 64),        # bIII A     E3  A3 C#4 E4
       (52, 56, 59, 64))        # bVII E     E3  G#3 B3 E4

# The bass plays the chord roots at MIDI 38-45, so its own fundamental sits at
# 73-110 Hz and the sub an octave below covers 37-55. Nothing leaps more than
# a fifth: a rolling bass that jumps two octaves loses power on every high
# note, and the whole point of this part is that it never lets go.
BASS = ((0, 42), (32, 38), (64, 45), (96, 40))          # F#2 D2 A2 E2

# The arp pool per chord, an octave above the pad. `arp_seq` folds in the
# octave above and runs a SEVEN-note cycle over a sixteen-step bar, so the
# figure starts on a different note every bar and does not come home until
# bar 7. Four notes over sixteen steps is what "every arp sounds the same"
# means, and no amount of reverb fixes it.
ARP = ((66, 69, 73),            # F#4 A4 C#5
       (66, 69, 74),            # F#4 A4 D5
       (69, 73, 76),            # A4  C#5 E5
       (64, 68, 71))            # E4  G#4 B4

CH = (0, 0, 1, 1, 2, 2, 3, 3)   # which chord each bar of the loop is on

# --- the melody -----------------------------------------------------------
# Sixteen bars, MIDI 78-88 - a major seventh of range, which is singable, and
# the whole reason a festival crowd can shout it back. An arch: it rises to
# E6 in bar 5, which is 62% of the way through the phrase, and falls from
# there. One climax note. Two climaxes in a phrase is no climax.
#
# The last note is F#5 over an E major chord - the ninth. Unresolved on
# purpose: the phrase cannot end, so the loop has to.
THEME = ((0, 85, 12), (12, 83, 4), (16, 81, 10), (26, 83, 6),
         (32, 85, 12), (44, 86, 4), (48, 83, 10), (58, 81, 6),
         (64, 85, 12), (76, 88, 4), (80, 88, 14), (94, 86, 2),
         (96, 85, 10), (106, 83, 6), (112, 80, 10), (122, 78, 6))
# The answer. Same skeleton, but bars 3-4 and 7-8 climb where the first
# version fell, and it ends a fourth higher - so a second statement is a
# development rather than a repeat.
THEME_B = ((0, 85, 12), (12, 83, 4), (16, 81, 6), (22, 83, 4), (26, 85, 6),
           (32, 86, 10), (42, 88, 6), (48, 86, 10), (58, 85, 6),
           (64, 85, 12), (76, 88, 4), (80, 88, 14), (94, 90, 2),
           (96, 90, 10), (106, 88, 6), (112, 85, 10), (122, 83, 6))
# The two-bar fragment that shows up long before the tune does.
HINT = ((0, 85, 12), (12, 83, 4), (16, 81, 10), (26, 83, 6))

s = Session(256, tail=5.0)


# ============================================================== the floor ===
def floor(b, gain=1.0, steps_=(0, 4, 8, 12), lpf=None, click=1.0, tone=1.0,
          decay=0.185, drive=2.5, sub=1.0, silent=False):
    """Four to the floor. Every hit gets its own seed: the click is a noise
    burst, and four thousand bit-identical noise bursts stop being a drum and
    become a metronome."""
    for st in steps_:
        t = s.pos(b, st)
        s.hit(t)                        # the sidechain trigger, even when muted
        if silent:
            continue
        k = tkick(tune=ROOT, decay=decay, drive=drive, click=click, tone=tone,
                  sub=sub, seed=(b * 16 + int(st)) % 71)
        if lpf:
            k = lp(k, lpf)
        s.place(t, k, gain, 'drums')


def back(b, gain=1.0, steps_=(4, 12), clap=1.0, snare=0.55, room=1.0, tone=1.0):
    """Clap and snare together, which is the trance backbeat: the clap is the
    width and the top, the snare is the 190 Hz fundamental underneath it, and
    without that fundamental the backbeat is not felt in the low band at all."""
    for st in steps_:
        t = s.pos(b, st)
        if clap:
            s.place(t, tclap(room=room, tone=tone, seed=(b * 4 + int(st)) % 53),
                    gain * clap, 'drums')
        if snare:
            s.place(t, tsnare(2.4, bright=tone, room=0.0,
                              seed=(b * 4 + int(st)) % 47),
                    gain * snare, 'drums')


def tops(b, gain=1.0, closed=True, opens=OFFBEAT, tone=1.0, ride=0.0,
         sixteenths=True, hatg=1.0):
    """The offbeat open hat is the one sound that says this genre out loud.
    It is truncated at 340 ms - the offbeats are 435 ms apart at this tempo,
    so each one gets ninety milliseconds of air after it and reads as an
    event instead of as sand."""
    if closed:
        rng = range(16) if sixteenths else range(0, 16, 2)
        for i in rng:
            if i in opens:
                continue
            v = 0.72 if i % 4 == 0 else (0.52 if i % 2 == 0 else 0.30)
            s.place(s.pos(b, i), thhat(0.55, tone=tone, seed=(b * 16 + i) % 67),
                    gain * v * hatg, 'drums')
    for st in opens:
        s.place(s.pos(b, st), thhat(2.6, open_=True, tone=tone,
                                    seed=(b * 4 + int(st)) % 59),
                gain * 0.62 * hatg, 'drums')
    if ride:
        for i in range(1, 16, 2):
            s.place(s.pos(b, i), tride(3.0, tone=tone, seed=(b * 16 + i) % 43),
                    gain * ride * (0.9 if i % 4 == 1 else 0.6), 'drums')


# =============================================================== the parts ===
def bassline(b0, bars=8, gain=1.0, gate=ROLL, cutoff=560.0, f_hi=3200.0,
             res=1.6, decay=0.052, sub=0.52, drive=1.9, detune=17.0):
    """One phrase, one phase track. The chord changes glide because the
    oscillator never restarts, and the gate cuts a continuous sound into notes
    rather than triggering separate ones."""
    reps = max(bars // 8, 1)
    notes = tuple((st + 128 * r, n) for r in range(reps) for st, n in BASS)
    s.place(s.pos(b0), rollbass(notes, dur_bars=bars, gate=gate, cutoff=cutoff,
                                f_hi=f_hi, res=res, decay=decay, sub=sub,
                                drive=drive, detune=detune),
            gain, 'bass')


def pads(b, gain=1.0, dur=16, cutoff=2600.0, hpf=230.0, attack=0.55,
         release=1.2, sweep=0.0, gate_=None, oct_=0, voices=3, wide=1.0):
    """Two bars of chord. Voiced low and wide, high-passed at 230 so it lives
    entirely above the bass, and optionally chopped by `tgate` - a sustained
    pad through a sixteenth-note gate is a rhythm part with no new instrument
    in the arrangement, which is the cheapest density there is."""
    ch = tuple(n + 12 * oct_ for n in PAD[CH[b % 8]])
    seg = tpad(ch, dur_steps=dur, cutoff=cutoff, hpf=hpf, attack=attack,
               release=release, sweep=sweep, voices=voices, wide=wide,
               seed=b % 8)
    if gate_ is not None:
        seg = tgate(seg, **gate_)
    s.place(s.pos(b), seg, gain, 'pad')


def arp(b, gain=1.0, rate=1.0, cycle=7, octaves=(0, 1), shape='up',
        f_hi=6800.0, f_lo=420.0, decay=0.085, res=1.7, rotate=0, gate=None,
        drive=1.6, det=0.008):
    """One bar of sixteenth-note pluck. `arpvoice` is the right instrument
    and it is already in core: detuned saws through a filter that closes on
    every single note, which is what a plucked string does and what sixteen
    identical bell hits a bar do not."""
    pool = list(ARP[CH[b % 8]])
    for st, note, dur, vel in arp_seq(pool, bars=1, shape=shape, rate=rate,
                                      cycle=cycle, octaves=octaves,
                                      rotate=rotate, gate=gate, tail=0.85,
                                      seed=b):
        s.place(s.pos(b, st),
                arpvoice(midi(note), dur, f_lo=f_lo, f_hi=f_hi, decay=decay,
                         res=res, drive=drive, detune=det),
                gain * vel, 'arp')


def lead(b0, theme=THEME, bars=8, gain=1.0, low=0.0, top=0.0, spread=34.0,
         hpf=270.0, lpf=12000.0, sub=0.30, mix=0.68, attack=0.014,
         release=0.11, vib=9.0, drive=1.1, width=1.0):
    """The melody. `stack3` places it in up to three octaves at once, all
    sharing one reverb, so the ear hears one instrument three octaves tall
    rather than three parts playing the same tune."""
    stack3(s, s.pos(b0), theme, bus='lead', gain=gain, low=low, top=top,
           dur_steps=bars * 16, spread=spread, hpf=hpf, lpf=lpf, sub=sub,
           mix=mix, attack=attack, release=release, vib=vib, drive=drive,
           width=width)


def strings(b, notes, gain=1.0, dur=32, cutoff=3000, attack=0.45, seed=0):
    """A section, not a chorused saw: every player enters late by a different
    amount and drifts in pitch on its own random walk, so the beating never
    settles into a pattern."""
    s.place(s.pos(b), ens([midi(n) for n in notes], dur, cutoff=cutoff,
                          attack=attack, drift=1.1, seed=seed),
            gain, 'pad')


# ================================================== INTRO: 0-15 (0:00) =====
# Drums and air only, and the kick behind a filter that opens across sixteen
# bars. No bass yet: the bottom two octaves are the first thing this record
# spends, and it does not spend them here.
s.place(s.pos(0), crowd(64, gain=0.55, roar=0.05, seed=3), 1.0, 'crowd')
s.place(s.pos(0), wind(64, gain=0.30), 0.5, 'air')
for b in range(16):
    u = b / 15
    if b >= 2:
        floor(b, gain=0.55 + 0.42 * u, lpf=320 + 2600 * u,
              click=0.25 + 0.75 * u, tone=0.75 + 0.3 * u, decay=0.17)
    tops(b, gain=0.20 + 0.55 * u, sixteenths=b >= 8,
         opens=OFFBEAT if b >= 6 else (2, 10), tone=0.62 + 0.35 * u)
    if b >= 8:
        pads(b, gain=0.26 + 0.30 * u, dur=18, cutoff=900 + 1400 * u,
             attack=1.4, release=1.6, voices=2) if b % 2 == 0 else None
s.place(s.pos(0), uplift(32, gain=0.30, f0=200, f1=2600, q=3.0, curve=1.4,
                         swell=1.4, seed=1), 1.0, 'fx')
s.place(s.pos(14), uplift(32, gain=0.42, f0=260, f1=5200, q=4.5, seed=2), 1.0, 'fx')

# ================================================== PULSE: 16-31 (0:28) ====
# The bass arrives, thinned to two sixteenths per beat, and the open hats go
# to all four offbeats. Bar 24 brings the backbeat.
for b in range(16, 32):
    u = (b - 16) / 15
    floor(b, gain=1.0, click=0.9 + 0.2 * u, tone=1.0)
    tops(b, gain=0.85, tone=0.95, hatg=0.9)
    if b >= 24:
        back(b, gain=0.62 + 0.25 * u, snare=0.42, tone=0.9)
    if b % 2 == 0:
        pads(b, gain=0.42, dur=18, cutoff=1500 + 900 * u, attack=1.1, voices=3)
bassline(16, 8, gain=0.80, gate=ROLL8, cutoff=430, f_hi=2200, decay=0.060)
bassline(24, 8, gain=0.92, gate=ROLL8, cutoff=500, f_hi=2700, decay=0.056)
s.place(s.pos(23, 8), uplift(8, gain=0.40, f0=400, f1=6000, q=5.0, seed=4), 1.0, 'fx')
s.place(s.pos(24), tcrash(24, gain=0.42, seed=1), 1.0, 'air')

# ================================================= GROOVE: 32-47 (0:56) ====
# Full roll on the bass, the pad on every bar, and the arp - filtered down at
# first, opening over sixteen bars. This is the section that establishes what
# the record is; nothing new happens in it after bar 40.
for b in range(32, 48):
    u = (b - 32) / 15
    floor(b, gain=1.0, click=1.05, tone=1.05)
    tops(b, gain=0.92, tone=1.0)
    back(b, gain=0.92, snare=0.50)
    pads(b, gain=0.52 + 0.14 * u, dur=17, cutoff=1900 + 1100 * u, attack=0.55)
    if b >= 36:
        arp(b, gain=0.30 + 0.34 * u, f_hi=1600 + 4800 * u, f_lo=340,
            decay=0.075, rotate=b % 7)
bassline(32, 16, gain=1.0, cutoff=560, f_hi=3200)
s.place(s.pos(32), tcrash(24, gain=0.46, seed=2), 1.0, 'air')
s.place(s.pos(40), tcrash(20, gain=0.34, seed=3), 1.0, 'air')

# ================================================= ASCENT: 48-63 (1:23) ====
# The first melodic hint: two bars of the theme, an octave down, behind a
# low-pass, arriving from the back of the room. It is the same four notes the
# whole festival will be shouting in four minutes, and it is barely audible.
for b in range(48, 64):
    u = (b - 48) / 15
    floor(b, gain=1.0, click=1.1, tone=1.1)
    tops(b, gain=0.95, tone=1.05, ride=0.22 if b >= 56 else 0.0)
    back(b, gain=1.0, snare=0.52)
    pads(b, gain=0.62, dur=17, cutoff=2600 + 900 * u, attack=0.50)
    arp(b, gain=0.66, f_hi=6400 + 1400 * u, f_lo=420, decay=0.085,
        rotate=b % 7, octaves=(0, 1))
bassline(48, 16, gain=1.05, cutoff=600, f_hi=3400)
for b0 in (56, 60):
    lead(b0, tuple((st, n - 12, d) for st, n, d in HINT), bars=2, gain=0.34,
         hpf=200, lpf=2600, sub=0.0, spread=26.0, vib=6.0, attack=0.10,
         release=0.4, width=0.7)
s.place(s.pos(48), tcrash(24, gain=0.48, seed=4), 1.0, 'air')
s.place(s.pos(56), tcrash(20, gain=0.36, seed=5), 1.0, 'air')

# ================================================ BUILD I: 64-79 (1:51) ====
# Five dimensions at once, which is the minimum for a build that does
# anything: rhythmic density (the roll), pitch (the riser), register (the
# whole mix high-passing so the bass disappears), loudness, and space. Then
# the last beat is empty.
for b in range(64, 80):
    u = (b - 64) / 15
    hp_hz = 30 + 300 * (u ** 2.4)
    floor(b, gain=1.0 - 0.25 * u, click=1.15, tone=1.15,
          sub=1.0 - 0.75 * u, decay=0.175, silent=(b == 79))
    tops(b, gain=0.95 + 0.25 * u, tone=1.05 + 0.25 * u, ride=0.30)
    back(b, gain=1.0, snare=0.5, tone=1.05) if b < 76 else None
    pads(b, gain=0.62 + 0.30 * u, dur=17, cutoff=3000 + 2500 * u,
         hpf=230 + hp_hz, attack=0.40)
    arp(b, gain=0.70 + 0.25 * u, f_hi=7600, f_lo=520 + 900 * u, decay=0.075,
        rotate=b % 7)
bassline(64, 8, gain=1.05, cutoff=620, f_hi=3600)
bassline(72, 4, gain=0.85, gate=ROLL8, cutoff=700, f_hi=4000, sub=0.32)
bassline(76, 2, gain=0.50, gate=(2, 6, 10, 14), cutoff=900, f_hi=4400, sub=0.0)
roll(s, 76, 4, gain=0.55, rates=(2.0, 1.0, 1.0, 0.5), v0=0.30, v1=1.0,
     bright=1.15, seed=5)
s.place(s.pos(72), uplift(64, gain=0.60, f0=280, f1=9000, q=6.5, curve=2.3,
                          tone=460, tone1=3400, seed=6), 1.0, 'fx')
s.place(s.pos(78), uplift(16, gain=0.55, f0=900, f1=11000, q=8.0, curve=1.6,
                          seed=7), 1.0, 'fx')
s.place(s.pos(79, 8), rev(tcrash(16, gain=0.75, seed=6)), 1.0, 'fx')
s.place(s.pos(79, 12), subdive(6, gain=0.70, f0=92, f1=28, seed=1), 1.0, 'bass')
s.place(s.pos(78), crowd(32, gain=0.60, roar=0.55, seed=7), 1.0, 'crowd')

# ================================================== DROP I: 80-111 (2:19) ==
# The lead in one register with the top rolled off at 8 kHz, no octave above
# it, and the pad ungated. Every one of those is held back on purpose: the
# same melody at bar 192 arrives in three octaves with the filter open, and
# the only way that reads as bigger is if this one was not.
s.place(s.pos(80), boom(28, gain=0.42, seed=1), 1.0, 'fx')
s.place(s.pos(80), tcrash(32, gain=0.62, seed=7), 1.0, 'air')
s.place(s.pos(80), crowd(48, gain=0.70, roar=0.85, seed=8), 1.0, 'crowd')
for b in range(80, 112):
    u = (b - 80) / 31
    ph = b - 80
    floor(b, gain=1.0, click=1.15, tone=1.12, decay=0.19)
    tops(b, gain=1.0, tone=1.12, ride=0.28)
    back(b, gain=1.05, snare=0.55, tone=1.05)
    pads(b, gain=0.66, dur=17, cutoff=3400, attack=0.36)
    arp(b, gain=0.72, f_hi=7400, f_lo=460, decay=0.080, rotate=b % 7)
    if ph % 8 == 7:                       # a turnaround fill every eight bars
        roll(s, b, 1, gain=0.40, rates=(1.0,), v0=0.45, v1=0.95, seed=ph)
for b0 in range(80, 112, 8):
    bassline(b0, 8, gain=1.08, cutoff=600, f_hi=3400)
lead(80, THEME, bars=16, gain=0.90, low=0.36, top=0.0, spread=32.0,
     hpf=300, lpf=8000, sub=0.26, mix=0.62, vib=8.0)
lead(96, THEME_B, bars=16, gain=0.95, low=0.40, top=0.0, spread=34.0,
     hpf=300, lpf=9000, sub=0.28, mix=0.65, vib=9.0)
for b in (88, 96, 104):
    s.place(s.pos(b), tcrash(24, gain=0.40, seed=b % 9), 1.0, 'air')

# ================================================== BRIDGE: 112-127 (3:15) =
# The drop subtracts rather than ending. The lead goes first, then the arp
# thins, then the pad, and the last four bars close the filter on everything -
# so that when the drums stop at 128 the room has already been emptying for
# half a minute and the silence is the arrival of something, not the absence
# of it.
for b in range(112, 128):
    u = (b - 112) / 15
    floor(b, gain=1.0 - 0.30 * u, click=1.1 - 0.6 * u, tone=1.1 - 0.4 * u,
          lpf=None if b < 122 else 6000 - 900 * (b - 122))
    tops(b, gain=1.0 - 0.55 * u, tone=1.1 - 0.5 * u,
         opens=OFFBEAT if b < 122 else (2, 10), sixteenths=b < 120)
    back(b, gain=1.0 - 0.45 * u, snare=0.5, tone=1.0 - 0.3 * u)
    pads(b, gain=0.66 - 0.20 * u, dur=17, cutoff=3400 - 1900 * u, attack=0.42)
    if b < 124:
        arp(b, gain=0.70 - 0.45 * u, f_hi=7200 - 4200 * u, f_lo=440,
            decay=0.080, rotate=b % 7)
bassline(112, 8, gain=1.05, cutoff=580, f_hi=3200)
bassline(120, 4, gain=0.88, cutoff=480, f_hi=2400, sub=0.50)
bassline(124, 3, gain=0.55, gate=ROLL8, cutoff=380, f_hi=1500, sub=0.20)
s.place(s.pos(126), downlift(24, gain=0.55, f0=7000, f1=140, seed=2), 1.0, 'fx')
s.place(s.pos(127, 8), rev(tcrash(12, gain=0.55, seed=8)), 1.0, 'fx')

# =============================================== BREAKDOWN: 128-159 (3:43) =
# No drums for sixteen bars. The bottom two octaves are gone, the top octave
# is gone, and what is left is the middle - a pad, a string section and the
# melody, with a shimmer reverb underneath that returns each pass an octave
# higher, so the chords grow a choir of their own harmonics that nobody
# played. Bars 128-135 are the quietest on the record by four decibels.
s.place(s.pos(128), downlift(32, gain=0.42, f0=9000, f1=180, seed=3), 1.0, 'fx')
s.place(s.pos(128), crowd(96, gain=0.42, roar=0.25, seed=9), 1.0, 'crowd')
for b in range(128, 160):
    u = (b - 128) / 31
    pads(b, gain=0.56 + 0.30 * u, dur=18,
         cutoff=1500 + 2600 * u, hpf=210, attack=1.5 - 0.9 * u, release=1.8,
         voices=3, wide=1.15)
    if b >= 136:
        pads(b, gain=0.24 + 0.20 * u, dur=17, cutoff=3200, hpf=380,
             attack=0.7, oct_=1, voices=2, wide=0.8)

for b in range(128, 180, 4):
    strings(b, PAD[CH[b % 8]], gain=0.40 + 0.011 * (b - 128), dur=68,
            cutoff=2400 + 34 * (b - 128), attack=0.85, seed=b)

# The melody, exposed. Almost dry compared with everything around it, one
# register, no sub - the whole point is that it is small here.
lead(136, THEME, bars=16, gain=0.72, low=0.0, top=0.24, spread=28.0,
     hpf=300, lpf=7000, sub=0.0, mix=0.58, attack=0.055, release=0.34,
     vib=11.0, width=0.85)

# 144: the kick comes back as a pulse under the melody, on the beats only,
# filtered and without its click. A breakdown that removes the pulse entirely
# reads as a gap; one that keeps it reads as space.
for b in range(144, 160):
    u = (b - 144) / 15
    floor(b, gain=0.30 + 0.42 * u, lpf=180 + 1400 * u, click=0.0 + 0.5 * u,
          tone=0.6 + 0.4 * u, decay=0.15, sub=0.55 + 0.4 * u)
    if b >= 148:
        tops(b, gain=0.18 + 0.42 * u, sixteenths=b >= 152, opens=(2, 10),
             tone=0.7 + 0.3 * u)
    if b >= 152:
        arp(b, gain=0.22 + 0.34 * u, f_hi=2200 + 4200 * u, f_lo=380,
            decay=0.090, rotate=b % 7, octaves=(0,))
# The gated pad: one instrument, chopped into sixteenths, and suddenly the
# section has a rhythm part that was not there a bar ago.
for b in range(152, 160):
    pads(b, gain=0.34, dur=17, cutoff=4200, hpf=420, attack=0.06,
         release=0.5, oct_=1, voices=2,
         gate_=dict(rate_steps=1.0, duty=0.46, depth=0.92))
s.place(s.pos(144), tcrash(28, gain=0.34, seed=9), 1.0, 'air')
s.place(s.pos(152), uplift(48, gain=0.34, f0=300, f1=6000, q=4.0, curve=2.0,
                           seed=8), 1.0, 'fx')

# ================================================ BUILD II: 160-191 (4:38) =
# Thirty-two bars, and every dimension climbs the whole way: the roll goes
# eighths to sixteenths to thirty-seconds, two risers overlap, the high-pass
# on the pad and the arp walks from 230 Hz to 700, the bass returns and is
# then taken away again, and the crowd comes up underneath all of it.
for b in range(160, 192):
    u = (b - 160) / 31
    v = u ** 1.5
    hp_hz = 230 + 520 * (u ** 2.6)
    floor(b, gain=0.78 + 0.28 * u, click=0.55 + 0.62 * u, tone=0.95 + 0.25 * u,
          sub=1.0 - 0.80 * (max(u - 0.55, 0) / 0.45),
          silent=(b == 191))
    tops(b, gain=0.55 + 0.50 * u, tone=0.95 + 0.35 * u,
         ride=0.10 + 0.28 * u, sixteenths=True)
    if b < 188:
        back(b, gain=0.60 + 0.45 * u, snare=0.5, tone=1.0 + 0.1 * u)
    pads(b, gain=0.50 + 0.34 * u, dur=17, cutoff=2600 + 3000 * u, hpf=hp_hz,
         attack=0.40 - 0.28 * u,
         gate_=dict(rate_steps=1.0, duty=0.46 + 0.12 * u, depth=0.92 - 0.5 * u))
    arp(b, gain=0.44 + 0.36 * u, f_hi=4200 + 4000 * u, f_lo=420 + 700 * u,
        decay=0.085 - 0.02 * u, rotate=b % 7)
    pads(b, gain=0.40 + 0.22 * u, dur=17, cutoff=3400 + 1800 * u, hpf=400,
         attack=0.5 - 0.3 * u, oct_=1, voices=2, wide=0.9)
bassline(160, 16, gain=1.02, cutoff=540, f_hi=3000, sub=0.50)
bassline(176, 8, gain=1.00, cutoff=620, f_hi=3600, sub=0.44)
bassline(184, 4, gain=0.78, gate=ROLL8, cutoff=760, f_hi=4200, sub=0.20)
bassline(188, 2, gain=0.44, gate=(2, 6, 10, 14), cutoff=1000, f_hi=4800, sub=0.0)

# The melody one last time before it is taken away - filtered, gated, and
# under the build rather than over it, so the drop is a recognition.
lead(176, THEME, bars=16, gain=0.52, low=0.0, top=0.30, spread=30.0,
     hpf=420, lpf=6200, sub=0.0, mix=0.60, vib=8.0, width=0.9)

roll(s, 184, 8, gain=0.80, rates=(2.0, 2.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.25),
     v0=0.22, v1=1.15, bright=1.2, curve=1.8, seed=11)
s.place(s.pos(168), uplift(96, gain=0.34, f0=240, f1=5000, q=4.0, curve=2.6,
                           swell=2.6, seed=9), 1.0, 'fx')
s.place(s.pos(176), uplift(128, gain=0.74, f0=300, f1=11000, q=7.0, curve=2.4,
                           tone=380, tone1=3800, seed=10), 1.0, 'fx')
s.place(s.pos(188), uplift(32, gain=0.92, f0=1100, f1=13000, q=9.0, curve=1.5,
                           tone=900, tone1=5600, seed=11), 1.0, 'fx')
s.place(s.pos(184), crowd(96, gain=0.55, roar=0.75, seed=12), 1.0, 'crowd')

# The gap. Bar 191 loses the kick, the snare roll stops on step 8, and the
# last two beats carry a reverse crash and a sine falling from 92 Hz to 26.
# One beat of nothing before an arrival is the oldest device in dance music
# and it is still the reason a drop lands: it takes the masking away, so the
# first bar of the drop hits an ear that has just been rested.
s.place(s.pos(191, 8), rev(tcrash(16, gain=0.95, seed=12)), 1.0, 'fx')
s.place(s.pos(191, 10), subdive(8, gain=0.95, f0=95, f1=26, decay=1.0, seed=2),
        1.0, 'bass')
s.place(s.pos(191, 12), downlift(6, gain=0.40, f0=11000, f1=600, q=6.0, seed=4),
        1.0, 'fx')

# ================================================= CLIMAX: 192-239 (5:34) ==
# Forty-eight bars. The lead arrives in three octaves at once with the filter
# fully open and a sub under it, the pad is wide and ungated, the arp runs
# two octaves, and the ride is on every offbeat sixteenth. Nothing here is
# louder than the first drop by more than a decibel - what is different is
# that there are three registers of melody where there was one, and that is
# what the ear reads as bigger.
s.place(s.pos(192), boom(32, gain=0.62, seed=2), 1.0, 'fx')
s.place(s.pos(192), tcrash(40, gain=0.85, seed=13), 1.0, 'air')
s.place(s.pos(192), crowd(128, gain=0.95, roar=1.0, seed=13), 1.0, 'crowd')
for b in range(192, 240):
    ph = b - 192
    u = ph / 47
    floor(b, gain=1.0, click=1.2, tone=1.15, decay=0.195, drive=2.6)
    tops(b, gain=1.05, tone=1.15, ride=0.34)
    back(b, gain=1.10, snare=0.58, tone=1.08)
    pads(b, gain=0.70, dur=17, cutoff=3800, attack=0.32, wide=1.15)
    arp(b, gain=0.76, f_hi=8200, f_lo=480, decay=0.078, rotate=b % 7,
        octaves=(0, 1))
    if ph >= 32:                       # the last sixteen: a second arp line
        arp(b, gain=0.34, rate=1.0, cycle=11, shape='updown', octaves=(1,),
            f_hi=9000, f_lo=900, decay=0.052, rotate=(b * 3) % 11, det=0.012)
    if ph % 8 == 7:
        roll(s, b, 1, gain=0.42, rates=(1.0,), v0=0.45, v1=1.0, seed=ph)
for b0 in range(192, 240, 8):
    bassline(b0, 8, gain=1.10, cutoff=640, f_hi=3600)
lead(192, THEME, bars=16, gain=1.00, low=0.44, top=0.32, spread=36.0,
     hpf=280, lpf=13000, sub=0.32, mix=0.70, vib=9.0)
lead(208, THEME_B, bars=16, gain=1.02, low=0.46, top=0.34, spread=38.0,
     hpf=280, lpf=14000, sub=0.32, mix=0.72, vib=10.0)
lead(224, THEME, bars=16, gain=1.05, low=0.48, top=0.38, spread=40.0,
     hpf=270, lpf=15000, sub=0.34, mix=0.74, vib=10.0)
for b in (200, 208, 216, 224, 232):
    s.place(s.pos(b), tcrash(24, gain=0.44, seed=b % 11), 1.0, 'air')
s.place(s.pos(216), crowd(64, gain=0.55, roar=0.55, seed=14), 1.0, 'crowd')

# =================================================== OUTRO: 240-255 (6:57) =
# Mirror of the intro: the melody goes, then the arp, then the pad, then the
# bass, and the drums are the last thing left - which is what a DJ needs to
# mix out of and what the shape of the record wants anyway.
s.place(s.pos(240), downlift(48, gain=0.48, f0=10000, f1=200, seed=5), 1.0, 'fx')
s.place(s.pos(240), crowd(80, gain=0.62, roar=0.45, seed=15), 1.0, 'crowd')
for b in range(240, 256):
    u = (b - 240) / 15
    floor(b, gain=1.0 - 0.55 * u, click=1.15 - 0.9 * u, tone=1.15 - 0.5 * u,
          lpf=None if b < 248 else 7000 - 700 * (b - 248))
    tops(b, gain=1.0 - 0.70 * u, tone=1.1 - 0.55 * u,
         opens=OFFBEAT if b < 250 else (2, 10), sixteenths=b < 250)
    if b < 250:
        back(b, gain=1.0 - 0.70 * u, snare=0.5, tone=1.0 - 0.4 * u)
    if b < 248:
        pads(b, gain=0.62 - 0.40 * u, dur=17, cutoff=3400 - 2200 * u)
    if b < 246:
        arp(b, gain=0.60 - 0.50 * u, f_hi=7000 - 4000 * u, f_lo=440,
            decay=0.080, rotate=b % 7)
bassline(240, 8, gain=1.02, cutoff=600, f_hi=3200)
bassline(248, 4, gain=0.72, gate=ROLL8, cutoff=440, f_hi=2000, sub=0.44)
lead(240, tuple((st, n, d) for st, n, d in THEME[:8]), bars=4, gain=0.52,
     low=0.30, top=0.0, spread=30.0, hpf=300, lpf=6000, sub=0.20, vib=8.0)
s.place(s.pos(255), downlift(16, gain=0.42, f0=8000, f1=120, seed=6), 1.0, 'fx')


# ================================================================ the mix ===
# Space. Three sends, and they are not the same size: the pad gets a shimmer
# because it is the only part with nowhere to be in time, the lead gets a
# plate plus a dotted-eighth delay because that combination IS the trance
# lead sound, and the arp gets a short room so it stays a rhythm part.
s.bus['pad']  = bus_reverb(s.bus['pad'],  decay=4.2, wet=0.40, tone=4200)
s.bus['lead'] = bus_reverb(s.bus['lead'], decay=2.6, wet=0.30, tone=5200)
s.bus['arp']  = bus_reverb(s.bus['arp'],  decay=1.5, wet=0.20, tone=5600)
s.bus['air']  = bus_reverb(s.bus['air'],  decay=3.2, wet=0.34, tone=4800)
s.bus['fx']   = bus_reverb(s.bus['fx'],   decay=2.8, wet=0.30, tone=4000)
s.bus['crowd'] = bus_reverb(s.bus['crowd'], decay=3.6, wet=0.35, tone=2600)

# A dotted eighth at 138 BPM is 326 ms - three sixteenths, so the echoes fall
# between the melody's own notes instead of on top of them. Filtered in the
# feedback, so each repeat is darker than the one before it.
_lead_d = delay(s.bus['lead'], steps_=3.0, times=4, fb=0.30, ping=True, damp=700)
s.bus['lead'] = _lead_d[:s.total].astype(np.float32)
_arp_d = delay(s.bus['arp'], steps_=3.0, times=3, fb=0.22, ping=True, damp=900)
s.bus['arp'] = _arp_d[:s.total].astype(np.float32)

# Everything above the bass gets out of the bottom two octaves, and everything
# below 150 Hz is mono - a club sums the low end, and a wide sub is a sub that
# is thrown away.
s.bus['pad']  = hp(s.bus['pad'], 200, order=2)
s.bus['lead'] = hp(s.bus['lead'], 170, order=2)
s.bus['arp']  = hp(s.bus['arp'], 320, order=2)
s.bus['air']  = hp(s.bus['air'], 400, order=2)
s.bus['crowd'] = hp(s.bus['crowd'], 260, order=2)
s.bus['fx']   = hp(s.bus['fx'], 34, order=2)
s.bus['drums'] = softclip(s.bus['drums'], 1.10, knee=0.85)
s.bus['bass']  = softclip(s.bus['bass'], 1.02, knee=0.88)
for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 150)
s.bus['pad']  = side_boost(s.bus['pad'], 500, 0.85)
s.bus['lead'] = side_boost(s.bus['lead'], 700, 0.55)
s.bus['air']  = side_boost(s.bus['air'], 900, 0.70)

# The ride. Section gains written into two hundred place() calls do not sum to
# a section - what changes is which parts are playing, and a different set of
# loud parts is still loud. This is one fader across the finished buses, and
# it is as much part of the arrangement as the notes are.
ARC = [(0, -9.2), (4, -7.6), (8, -6.6), (16, -5.4), (24, -4.6),
       (32, -3.6), (40, -3.1), (48, -2.4), (56, -2.1),
       (64, -2.0), (72, -1.7), (78, -1.4), (79.5, -3.4), (79.95, -3.4),
       (80, -0.6), (96, -0.5), (111.9, -0.5),
       (112, -2.4), (120, -3.2), (127.9, -4.6),
       (128, -16.4), (132, -15.8), (136, -13.2), (144, -9.4),
       (152, -6.6), (159.9, -5.8),
       (160, -5.2), (168, -4.0), (176, -3.0), (184, -1.9), (190, -1.2),
       (191.5, -5.2), (191.95, -5.2),
       (192, 0.0), (208, 0.0), (224, 0.0), (239.9, 0.0),
       (240, -1.8), (248, -4.4), (255, -9.0), (256, -13.0)]
_bars = np.array([p[0] for p in ARC]) * BAR
_db = np.array([p[1] for p in ARC])
_ride = 10 ** (np.interp(np.arange(s.total, dtype=np.float64), _bars, _db) / 20.0)
_ride = np.maximum(uniform_filter1d(_ride, int(0.030 * SR)), 0.0)
for b in s.bus:
    s.bus[b] = (s.bus[b] * _ride[:, None]).astype(np.float32)

GAINS = {'drums': 0.90, 'bass': 0.82, 'pad': 2.30, 'lead': 1.48, 'arp': 1.60,
         'air': 2.40, 'fx': 0.95, 'crowd': 0.62}
s.report(GAINS)
s.ownership(3000, 16000, GAINS, 'top  3-16k')
s.ownership(60, 300, GAINS, 'bass 60-300 ')
s.render('trance_glavnaya_scena_138.wav', drive=1.0, duck=0.46, duck_rel=0.16,
         clip=1.06, peak=0.95, fade=3.0, gains=GAINS,
         brick=dict(gain=1.26, ceiling=0.89))
