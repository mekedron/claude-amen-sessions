"""BARHAT - minimal club house at 122 BPM, G Dorian.

Velvet. A room where the music is not the event - people are - and the record
is what makes the room feel expensive. Late, warm, unhurried, and physical
enough that the shoulders start moving before anybody decides to dance.

The whole piece is TWO pitched instruments and a box of percussion. A bass,
and a GUITAR. There is no pad, no string bank, no electric piano and no lead
anywhere in it: what sounds like a bed underneath the record is the guitar's
own reverb tail, which is a decision rather than an accident - a chord thrown
into two and a half seconds of plate is a warmer bed than any pad, and it
costs no second voice ([[minimal-means-fewer-voices]]).

122 BPM. 492 ms a beat, and the kick is on all four, so the felt pulse is the
tempo and not half of it. Slower than this and the body stops moving; faster
and it stops being a conversation.

WHY A GUITAR. A pad states harmony and a guitar plays it, and the entire
difference is in the attack. Four notes arriving at one instant, in tune, is
an organ; a plectrum crossing four strings over seven milliseconds, each one
a few cents out because a person tuned it, is an instrument. `houselib.gtr` is
built on `core.string` - stiffness so the upper partials go progressively
sharp, two polarisations so the note drops a few dB and then rings, the combs
of where it was picked and where the pickup sits, and the coil's own resonance
at 2.4 kHz, which is a neck humbucker and is why this is dark and round rather
than glassy. Velocity moves the SPECTRUM, not the level: a soft stroke leaves
the high modes alone, so a comp breathes across a bar instead of pulsing.

G DORIAN, and the mode is the mood. Dorian is minor with a natural sixth, and
that one note is the difference between sad and cool.

    Gm9  ->  C13  ->  Bbmaj9  ->  F6/9          i - IV - bIII - bVII

Every note of it is in the key; there is no borrowed chord and no accident.
Two things carry it:

  ONE SEMITONE.  Gm9 to C13, the guitar moves exactly one voice by exactly one
                 semitone - F4 to E4 - and that E is the Dorian sixth. The
                 whole identity of the record is one finger moving one fret.
  ONE NOTE ON TOP. A4 sits on top of all four chords and never moves. It is
                 the 9th of Gm9, the 13th of C13, the major 7th of Bbmaj9 and
                 the 3rd of F6/9 - one note, four meanings. The chords colour
                 it; it does not follow them.

THE TOP END IS TRANSIENTS, NOT WASH. A shaker on every sixteenth and four open
hats a bar is a noise bed, and a noise bed at 6-9 kHz is what starts to hurt
after ninety seconds ([[top-end-from-transients-not-wash]],
[[an-open-hat-must-end-before-the-next-one]]). So the band above 3 kHz is paid
for by things that stop: eight short closed hats, two truncated open ones, a
high wooden rim, bongos, and a tambourine that only appears twice in the
record. The shaker runs eighths in three sections and is absent from the rest.

THE DEVELOPMENT HAS NO NEW PARTS IN IT.

  COLOUR   the guitar's amp opens from 2.9 kHz to 5.0 kHz across five minutes
           and shuts again, and its velocity - which is its brightness - rides
           with it. That sweep is the arrangement; in this genre it usually is.
  DENSITY  the comp goes from two chops a bar to eight, and the percussion box
           gains one layer every sixteen bars and loses them all at 80.
  RIDE     section contrast is a GAIN RIDE over the finished buses, written in
           decibels per bar - not per-part gains, which do not sum to a section
           and which the limiter closes anyway ([[section-contrast-belongs-in-level]]).

    HAZE (8) | FLOOR (24) | GROOVE (16) | ROOM (16) | OPEN (16)
    | BREATH (12) | RETURN (16) | HOLD (4) | VELVET (32) | AFTER (16) | OUT (8)

168 bars, 5:30. The floor drops out at 80 and the record is quietest at bar
111.5 - half a bar before the peak at 112, which is 67% of the way in.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
import houselib
from houselib import *

BAR, STEP = houselib.set_tempo(122)
# A shade more lilt than the module default. 7.8% of a step is about 54.9%
# swing: felt in the hips, and still under the line where it reads as garage.
houselib.SWING = 0.078

np.random.seed(1220)
rs = np.random.RandomState(1220)

# ============================================================== material ===
# G Dorian: G A Bb C D E F. The E is the whole point.
ROOTS = [31, 36, 34, 29]                       # G1  C2  Bb1 F1
UP    = [12,  7, 12, 12]                       # the bounce note, per chord:
#                                                C2's octave would land at
#                                                131 Hz, in the guitar's lap,
#                                                so that bar takes the fifth.

# The comp. Four notes, mid register, the shape a player actually holds.
#   Gm9     Bb3 D4  F4  A4   b3  5   b7  9
#   C13     Bb3 D4  E4  A4   b7  9   3   13   <- ONE voice moved, F -> E
#   Bbmaj9  C4  F4  A4  C5   9   5   maj7 9   <- the lift
#   F6/9    A3  C4  F4  G4   3   5   root 9   <- the settle
COMP = [(58, 62, 65, 69),
        (58, 62, 64, 69),
        (60, 65, 69, 72),
        (57, 60, 65, 67)]

RIM_HI, RIM_LO = 83, 78                        # wood, high enough to stay out
BON_M, BON_H = 74, 67                          # of the guitar's own band
CON_HI, CON_MID, CON_LO = 58, 51, 46


# ================================================================= bass ===
# The root under the kick, a sixteenth push behind it, and the octave landing
# on BEAT 3 rather than the root - which is what makes the bar bounce instead
# of sitting down twice. The fifth on the last offbeat rings PAST the bar line
# into the next chord, because `hbass` renders six steps of overhang; cut at
# the bar line that note dies at the moment it is meant to arrive and the
# first half of every bar goes quiet ([[bar-rendered-parts-must-overhang]]).
def bassbar(root, up, sparse=False):
    if sparse:
        return [(0, root, 5.2, 0, 0, 1.00), (10, root + 7, 4.4, 0, 0, 0.68)]
    return [(0,  root,      3.4, 0, 0, 1.00),
            (6,  root + up, 2.0, 0, 0, 0.70),
            (8,  root,      2.6, 0, 0, 0.84),
            (14, root + 7,  3.4, 0, 0, 0.68)]

BASS = [bassbar(r, u) for r, u in zip(ROOTS, UP)]
BASS_SPARSE = [bassbar(r, u, sparse=True) for r, u in zip(ROOTS, UP)]


# ============================================================== the comp ===
# (step, velocity). The chop sits on the offbeat eighths - the jack, the thing
# that makes a groove move sideways instead of forward - and density is the
# arrangement. Level 4 adds sixteenths; nothing new arrives, the same hand
# just plays more of the bar.
CHOP = {
    1: [(6, 0.54)],
    2: [(6, 0.58), (14, 0.46)],
    3: [(2, 0.42), (6, 0.62), (14, 0.50)],
    4: [(2, 0.44), (6, 0.64), (10, 0.42), (14, 0.54)],
}

def chops(level, b, ci):
    """The bar's chords - and, one bar in eight, none at all.

    A hole is a part. Four chords a bar for five minutes is a comp; three
    bars of it and then a bar of nothing is a player, and the bar of nothing
    is the one the listener notices. The rest lands on bar 6 of each eight,
    which is late enough in the phrase that the ear has settled and early
    enough that the turn home still arrives on time."""
    if b % 8 == 6 and level <= 3:
        return []
    out = list(CHOP[level])
    if ci == 3 and level >= 3:
        out.append((15, 0.42))                 # lean into the turn home
    return out


# ============================================================== sections ===
# (bar, name, chop level, amp tone, velocity scale, ring, open hats, shaker,
#  tambourine, percussion tier)
SEC = [(0,   'HAZE',   1, 3400, 0.62, 1, 0, 0, 1),
       (8,   'HAZE',   1, 3700, 0.70, 1, 0, 0, 2),
       (16,  'FLOOR',  2, 4100, 0.80, 1, 2, 0, 2),
       (24,  'FLOOR',  2, 4400, 0.86, 1, 2, 0, 2),
       (32,  'GROOVE', 2, 4800, 0.94, 1, 2, 0, 3),
       (48,  'ROOM',   3, 5200, 1.00, 1, 2, 1, 3),
       (64,  'OPEN',   3, 5800, 1.06, 1, 2, 1, 4),
       (80,  'BREATH', 1, 4000, 0.66, 1, 0, 0, 1),
       (88,  'BREATH', 2, 4500, 0.80, 1, 0, 0, 2),
       (92,  'RETURN', 3, 5400, 1.00, 0, 2, 0, 3),
       (108, 'HOLD',   1, 4300, 0.74, 1, 0, 0, 1),
       (112, 'VELVET', 4, 6400, 1.14, 1, 2, 1, 4),
       (128, 'VELVET', 4, 5000, 1.14, 1, 2, 1, 4),
       (144, 'AFTER',  3, 5400, 1.02, 1, 2, 1, 3),
       (160, 'OUT',    2, 4400, 0.82, 1, 2, 0, 2)]

def sec(b):
    cur = SEC[0]
    for row in SEC:
        if b >= row[0]:
            cur = row
    return cur


# =========================================================== the arrangement
# The gain ride, in decibels per bar. This is the arrangement's shape and it
# is a master fader move, not a set of per-part trims: a section is two
# hundred `place` calls, turning each of them down by the amount that feels
# right leaves the total where it was, and the limiter then closes whatever
# gap survived. Note the DIP immediately before each arrival rather than a
# climb into it - the ear judges a section against the half bar in front of
# it, so the cheapest way to make bar 112 enormous is to make bar 111 small.
ARC = [(0, -11.0), (4, -9.2), (7.5, -9.8), (8, -7.4), (12, -6.6),
       (15.5, -8.2), (16, -5.4), (24, -4.4),
       (31.5, -5.8), (32, -3.2), (40, -2.9),
       (47.5, -4.0), (48, -2.4), (56, -2.1),
       (63.5, -3.2), (64, -1.6), (72, -1.4),
       (79.5, -1.8), (80, -10.2), (84, -9.4), (88, -6.6),
       (91.5, -7.6), (92, -3.0), (100, -2.5), (104, -2.2),
       (107.5, -3.0), (108, -5.4), (110, -6.6), (111.5, -8.2), (111.9, -8.2),
       (112, 0.0), (128, 0.0), (140, -0.3),
       (143.5, -0.9), (144, -2.6), (152, -3.0),
       (159.5, -3.6), (160, -6.4), (164, -8.2), (168, -12.5)]


# ================================================================ render ===
NB = 168
S = Session(NB, tail=4.0)
P = S.pos

def jit(ms=4.0):
    """a few milliseconds of humanisation. Never on the kick and never on the
    sub: the pulse is the one thing the body is counting."""
    return int(rs.normal(0, ms / 1000.0 * SR))


for b in range(NB):
    _, name, LVL, TONE, GV, RING, NOPEN, TAM, PERC = sec(b)
    ci = b % 4

    kick_on = (8 <= b < 80) or (92 <= b)
    hat_on  = (12 <= b < 80) or (92 <= b)
    clap_on = (32 <= b < 80) or (96 <= b < 162)
    bass_on = (20 <= b < 80) or (88 <= b)
    sparse  = (88 <= b < 92) or (b >= 162)
    opens   = (2, 10) if NOPEN else ()

    # ---- the floor -------------------------------------------------------
    if kick_on:
        for st in (0, 4, 8, 12):
            t = P(b, st)
            S.hit(t)                                   # the sidechain trigger
            S.place(t, hkick(decay=0.162, sub=0.60, body=1.15),
                    0.78 if st in (0, 8) else 0.72, 'drums')
    if clap_on:
        for st in (4, 12):
            t = P(b, st) + jit(3)
            S.place(t, hclap(seed=(b + st) % 6), 1.05, 'drums')
            S.place(t, hsnare(seed=(b + st) % 4), 0.80, 'drums')
    if hat_on:
        for st in (2, 6, 10, 14):
            if st not in opens:
                S.place(P(b, sw(st)) + jit(3), hhat(tone=0.84, seed=(b * 4 + st) % 11),
                        1.05 if st in (6, 14) else 0.86, 'hats')
    for st in opens:
        S.place(P(b, sw(st)) + jit(3), hhat(open_=True, tone=0.88, seed=(b + st) % 9),
                1.30, 'hats')
    # ---- the percussion box: short things, and they all stop --------------
    quiet_bar = (b % 8 == 7)                   # the box takes a bar off too
    if PERC >= 1 and not quiet_bar:
        S.place(P(b, sw(11)) + jit(4), rimtick(note=RIM_HI, seed=b % 7),
                1.05, 'perc')
        if b % 4 == 2:
            S.place(P(b, sw(15)) + jit(4), rimtick(note=RIM_LO, seed=(b + 3) % 7),
                    0.74, 'perc')
    if PERC >= 2 and not quiet_bar:
        pat = (((3, BON_M, 'open', 0.56), (13, BON_H, 'open', 0.44))
               if b % 2 == 0 else
               ((7, BON_H, 'tip', 0.42), (11, BON_M, 'open', 0.50)))
        for st, nt, stk, v in pat:
            S.place(P(b, sw(st)) + jit(5),
                    bongo(nt, stk, vel=v, seed=(b * 3 + st) % 9), 0.66, 'perc')
    if PERC >= 3 and b % 4 == 0:
        # Three hits and two shapes. A conga playing a full tumbao would be a
        # part; this is a comment underneath one.
        pat = (((4, CON_MID, 'open', 0.70), (10, CON_LO, 'open', 0.58),
                (15, CON_HI, 'tip', 0.40))
               if b % 4 == 0 else
               ((4, CON_MID, 'open', 0.66), (9, CON_HI, 'open', 0.52),
                (12, CON_LO, 'muff', 0.46)))
        for st, nt, stk, v in pat:
            S.place(P(b, sw(st)) + jit(5),
                    conga(nt, stk, vel=v, seed=(b * 3 + st) % 9), 0.92, 'perc')
    if TAM and b % 4 == 1:
        pat = ((14, 0.62),) if TAM < 2 else ((6, 0.60), (14, 0.48))
        for st, v in pat:
            S.place(P(b, sw(st)) + jit(4), tamb(seed=(b + st) % 8), v, 'perc')

    # ---- the bass --------------------------------------------------------
    if bass_on:
        pat = (BASS_SPARSE if sparse else BASS)[ci]
        S.place(P(b), hbass(tuple(pat), f_hi=2750.0, drive=1.95, res=0.85,
                            hold=0.22, decay=0.50, sub=0.58, tail_steps=6.0),
                0.62 if sparse else 0.76, 'bass')

    # ---- the guitar ------------------------------------------------------
    # One instrument, two right hands. The chop is the heel of the palm on the
    # bridge - 190 ms and gone - and the ring is the same chord allowed to
    # last, once every four bars, which is where the record's warmth comes
    # from once it has been through the plate.
    notes = COMP[ci]
    for st, v in chops(LVL, b, ci):
        vel = round(min(v * GV, 1.0), 2)
        S.place(P(b, sw(st)) + jit(5),
                gtr(notes, 2.2, vel=vel, decay=0.21, damp=0.052, tone=TONE,
                    strum=0.0052, bright=1.50, res_hz=3100.0, presence=1.15,
                    chorus=0.30, tight=165.0, cone=0.55, take=b % 3),
                1.0, 'gtr')
    if RING and ci == 0:
        S.place(P(b, 0) + jit(4),
                gtr(notes, 15.0, vel=round(min(0.52 * GV, 1.0), 2), decay=1.35,
                    damp=0.026, tone=TONE * 0.82, strum=0.0092, chorus=0.44,
                    res_hz=2800.0, presence=0.95, pick=0.28, pickup=0.19,
                    tight=128.0, cone=0.70, take=(b // 4) % 3),
                0.72, 'gtr')

print('  floor, percussion, bass and the comp placed')

# ---- seams ---------------------------------------------------------------
# House does not detonate, so a join is a breath: a reversed swell of
# broadband noise over the last beat, and twice in the record a chord thrown
# into a long delay and abandoned - the dub move, and the cheapest way to make
# a loop that has played forty times feel like something just happened.
for b in (7, 15, 31, 47, 63, 79, 91, 107, 111, 143, 159):
    S.place(P(b, 12), whoosh(4, gain=0.30, rev_=True), 0.46, 'air')
for b, v in ((79, 0.60), (111, 0.52)):
    throw(S, P(b, 14),
          gtr(COMP[b % 4], 6.0, vel=0.62, decay=0.55, damp=0.045, tone=4200),
          gain=v, steps_=3.0, times=6, fb=0.56)


# ================================================================== mix ===
# The buses get their own compression before the master sees them, which is
# the only way to arrive at the clipper without a stack of transients for it
# to eat. `squash`'s release is one sixteenth at this tempo, so the gain
# climbs back between beats and the breathing is in time.
S.bus['drums'] = squash(S.bus['drums'], thresh=0.44, ratio=2.6, attack=0.016,
                        release=0.123, mix=0.80, report='drums')
S.bus['perc'] = squash(S.bus['perc'], thresh=0.15, ratio=3.4, attack=0.008,
                       release=0.123, mix=0.66, report='perc')
# `squash` gives back what a full-scale peak lost, which on a bus this
# transient is a large factor - so one bongo slap arrives at the master way
# above 1.0 and the clipper spends its whole budget on it. Loudness comes from
# removing one peak, not from clipping harder.
S.bus['perc'] = softclip(S.bus['perc'], 0.85, knee=0.55)
S.bus['gtr'] = squash(S.bus['gtr'], thresh=0.22, ratio=2.4, attack=0.012,
                      release=0.145, mix=0.62, report='gtr')

# One room and two distances, and this is where the record gets its bed. The
# comp is dry-ish so the chops stay percussive; the long plate behind it is
# fed hard, and its tail across a chord change is the only sustained pitched
# thing in the piece.
# The guitar's own fundamentals pile 4 dB of the record into 300-800 Hz, and
# that band is where "boxy" lives - a comp that sits on the floor instead of
# floating over it. A wide subtractive bell is the fix; the notes are still
# all there, they just stop being the heaviest thing in the mix.
S.bus['gtr'] = S.bus['gtr'] - 0.34 * bandpass(S.bus['gtr'], 300, 700, order=2)
S.bus['gtr'] = bus_reverb(S.bus['gtr'], decay=3.4, wet=0.44, tone=3600)
S.bus['perc'] = bus_reverb(S.bus['perc'], decay=0.60, wet=0.10, tone=6200)
S.bus['hats'] = bus_reverb(S.bus['hats'], decay=0.42, wet=0.07, tone=8000)
S.bus['hats'] = narrow(S.bus['hats'], 0.62)
S.bus['air'] = bus_reverb(S.bus['air'], decay=3.2, wet=0.32, tone=4400)
for k in ('gtr', 'air'):
    S.bus[k] = mono_below(S.bus[k], 170)
# Several decorrelated buses sum to an image no record has. A trim on each is
# the fix; less reverb on all of them is not.
S.bus['air'] = narrow(S.bus['air'], 0.70)
S.bus['gtr'] = narrow(S.bus['gtr'], 0.80)

# ---- the ride ------------------------------------------------------------
t_bars = np.arange(S.total) / BAR
db = np.interp(t_bars, [p[0] for p in ARC], [p[1] for p in ARC])
ride = uniform_filter1d(10 ** (db / 20.0), int(0.030 * SR)).astype(np.float32)
for k in S.bus:
    S.bus[k] = S.bus[k] * ride[:, None]
print(f'  ride: {db.min():.1f} to {db.max():.1f} dB across {NB} bars')

# Balanced by measurement. `Session.loudness` is the 90th percentile of a
# 300 ms window - how loud a part is WHEN IT PLAYS - so the numbers are
# comparable across buses however transient the part is.
GAINS = {'drums': 0.58, 'perc': 2.30, 'bass': 0.66, 'gtr': 1.72,
         'hats': 3.40, 'air': 1.85}

S.report(GAINS)
S.render('house_barhat_122.wav', drive=0.0, duck=0.66, duck_rel=0.20,
         clip=1.18, peak=0.89, fade=2.6, gains=GAINS,
         brick=dict(gain=1.08, ceiling=0.90))
