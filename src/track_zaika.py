"""ZAIKA - drill'n'bass, G dorian, 174 BPM.

The stutterer. A tune a music box could play, over a break that cannot get
through a bar without tripping.

That contrast is the whole design, and it is the Richard D. James trick: the
drums are doing something almost unlistenably complicated while the harmony
does something a child could hum, and neither one apologises for the other.
The failure mode of this style is a track where everything is broken, which
is just noise with a tempo. So four things here are never broken:

- **The pulse is not in the break.** `thump` on beats 1 and 3, `crack` on 2
  and 4, in nearly every bar of the record, and the sub is one continuous
  oscillator underneath. The break rides on top with its bottom cut at
  150 Hz. It can fall apart completely - and in the third drop it does, for
  a beat at a time - and the body still knows where the beat is.

- **The tune repeats.** Eight bars, stated whole in the breakdown, answered
  by itself a sixth below, and back in full over the last drop. It is G dorian
  pentatonic with exactly one note from outside it: the natural sixth, E,
  which is what makes the mode sound warm rather than sad.

- **Nothing plays a block chord.** There is no keyboard on this record. A
  chord whose notes all start on the same sample, with one spectrum and one
  envelope, reads as a preset pasted in from another session - and next to a
  break cut into thirty pieces it reads as that very loudly. So the harmony is
  a string section that has no attack at all, each player entering late and
  drifting in pitch on its own, and single felt-piano notes dropped one at a
  time across the bar. The felt piano is modelled string by string: stiff
  partials that go sharp with mode number, a prompt sound several dB above the
  tail, a second polarisation dying at half the rate, and the thud of the
  hammer, which is the part that makes it an object rather than a tone.

- **The edits are written, not sprayed.** Every bar is an ordinary bar with
  one to three steps interfered with. The interference is a parameter lock:
  this snare is a six-hit ratchet that accelerates, that kick is reversed and
  a fifth down, this one is stretched to twice its length without moving in
  pitch. A bar with eight locks in it is used four times on the record.

    intro        0-15    room, strings, the break arriving filtered and stuttering
    approach    16-31    the kit plain, the sub, first ratchets
    build 1     32-39
    DROP 1      40-71    edit A: the groove, broken once a bar
    breakdown   72-87    the theme, strings, no drums
    build 2     88-95
    DROP 2      96-127   edit B: harder - stretches, a 7-step tick, glitches
    machines   128-139   no bass at all: ratchets, tape stops, dub delay
    build 3    140-143
    DROP 3     144-175   edit C: the theme over the worst of the edits
    outro      176-191

G dorian, not G minor: the natural 6 is in the chords (C9 is the dorian IV)
and in the tune. The one chord from outside the mode is Dbmaj9#11, a tritone
away, and it lands once per eight bars in the second half - the harmonic
equivalent of the thing the drums do all the time.
"""
import numpy as np
from idmlib import *

s = Session(192, tail=3.0)
rs = np.random.RandomState(7401)

# ============================================================ harmony
# G dorian: G A Bb C D E F. Voiced rootless in the octave above middle C,
# because the bass has the root and the break owns everything above 3 kHz -
# the keys live in the one band nothing else is using.
G1, C2, Eb2, F2, Bb1, D2 = 31, 36, 39, 41, 34, 38
CH = {
    'Gm9':   [58, 62, 65, 69],          # Bb D F A   over G
    'C9':    [58, 64, 67, 74],          # Bb E G D   over C   - the dorian IV
    'Ebmaj9': [55, 62, 65, 67],         # G  D F G   over Eb
    'F69':   [57, 60, 65, 67],          # A  C F G   over F
    'Dbmaj9': [56, 60, 65, 68],         # Ab C F Ab  over Db  - the outsider
    'Cm9':   [58, 63, 67, 70],          # Bb Eb G Bb over C
    'Abmaj7': [60, 63, 67, 72],         # C  Eb G C  over Ab
    'Bb69':  [58, 62, 65, 69],          # Bb D F A   over Bb
}
ROOT = {'Gm9': G1, 'C9': C2, 'Ebmaj9': Eb2, 'F69': F2, 'Dbmaj9': 37,
        'Cm9': C2, 'Abmaj7': 32, 'Bb69': 34}

PROG = ['Gm9', 'C9', 'Ebmaj9', 'F69']            # 2 bars each -> 8-bar cycle
PROG_B = ['Gm9', 'C9', 'Ebmaj9', 'Dbmaj9']       # the second half's version
BREAKD = ['Cm9', 'Abmaj7', 'Ebmaj9', 'Gm9']


def chord_at(b, alt=False):
    p = PROG_B if alt else PROG
    return p[(b // 2) % 4]


# ============================================================ the tune
# Eight bars. Bars 1-4 rise and settle, 5-8 answer them a third lower and
# fall - a period, question and answer, and the only note outside the
# pentatonic is the E in bar 3.
#
# It is played on the electric piano, in the octave below where the instinct
# to write it puts it. A bright inharmonic attack with a long ring, up where a
# glockenspiel lives, reads as a toy however good the notes are - and a toy is
# exactly what a tune this simple would become. A tine has the attack without
# the ringing top, and the string doubling underneath gives it a body a
# struck bell has not got.
#   58 Bb3  60 C4  62 D4  64 E4  65 F4  67 G4  69 A4  70 Bb4  72 C5  74 D5
THEME = ((0, 62, 3.5), (4, 65, 2.5), (7, 67, 3.0), (12, 70, 4.0),
         (18, 69, 2.5), (22, 67, 3.0), (26, 65, 2.0), (29, 62, 5.0),
         (32, 58, 3.0), (36, 62, 2.5), (39, 64, 3.5), (44, 65, 4.0),
         (50, 67, 3.0), (54, 70, 2.5), (57, 72, 4.0), (62, 70, 3.0),
         (64, 67, 6.0), (72, 65, 3.0), (76, 62, 4.0),
         (84, 60, 3.0), (88, 62, 8.0), (104, 58, 12.0))

# The counter-line the electric piano answers with in the breakdown: the same
# shape, half the speed, a sixth below.
ANSWER = ((0, 50, 8.0), (12, 53, 6.0), (20, 55, 8.0), (32, 53, 6.0),
          (40, 50, 8.0), (52, 48, 10.0))


def theme(b0, gain=1.0, bus='lead', voice='felt', octave=0, from_=0, to=200,
          decay=0.55, spread=0.0, bow=0.0, vel=0.62):
    """Place the tune from bar b0. `from_`/`to` are step numbers into the
    eight-bar phrase, so a fragment can answer a drop without the whole melody
    having to arrive. `bow` doubles it with a string a fifth below, which is
    what turns a line into a voice."""
    for st, nt, dur in THEME:
        if st < from_ or st >= to:
            continue
        f = midi(nt + 12 * octave)
        if voice == 'glass':
            seg = glass(f, dur, decay=decay, spread=spread, damp=2400)
        elif voice == 'bow':
            seg = ens([f, f / 1.5], dur * 1.5, voices=3, cutoff=2400,
                      attack=0.10, seed=int(st))
        else:
            seg = felt([f], dur, vel=vel, roll=0.0, seed=int(st), spread=0.0,
                       hammer=0.6, room=0.34)
        s.place(s.pos(b0, st), seg, gain, bus)
        if bow:
            s.place(s.pos(b0, st), ens([f / 1.5, f], dur * 1.4, voices=3,
                                       cutoff=2000, attack=0.12, seed=int(st)),
                    gain * bow, 'pad')


# ============================================================ the kit
def kit(b, gain=1.0, kicks=(0, 8), snares=(4, 12), extra=(), tune=48.0,
        crack_g=1.0, sc=True, seed=0):
    """The scaffolding: the two hits a bar that are never allowed to move.

    Everything else on this record is negotiable. These are not, and that is
    what buys the break the right to disintegrate."""
    for k in kicks:
        t = s.pos(b, k)
        s.place(t, thump(tune=tune, gain=1.0 if k in (0, 8) else 0.7),
                gain * 0.95, 'drums')
        if sc and k in (0, 8):
            s.hit(t)
    for k in snares:
        s.place(s.pos(b, k), crack(seed=seed + int(k), gain=1.0 if k in (4, 12) else 0.6),
                gain * crack_g * 0.55, 'drums')
    for k in extra:
        s.place(s.pos(b, k), tick(seed=seed + int(k * 3)), gain * 0.30, 'drums')


# ============================================================ the edits
# The plain bar, straight off the sample's own first bar: kick, ghost, kick,
# hat, snare, hats, the late kick pair, the second snare. Every cell below is
# this bar with something taken out or moved.
PLAIN = "KgkhShhh hhqQD.hi"
CELLS = {
    'A': "Kg.hS.h. h.qQD.hi",     # the drop's bar - holes cut for the bass
    'B': "K..hS.hg h.qQD.h.",     # sparser, for the first half of a phrase
    'C': "K.khS.h. .hqQDghi",     # busier ghosts
    'D': "K...S... ...QD...",     # skeleton - under the theme
    'E': "hhK.S.hg h.qQD.Xh",     # the shifted bar, from the sample's bar 4
    'F': "Kg.hS.h. h.qQD.h.",
}

# Locks that get reused. `rat` fires the step as a ratchet; `dur` is how long
# it has; `curve` is how the repeats are spaced; `p1` is where the pitch ends
# up; `str_` stretches without moving the pitch; `rev_` reverses.
TRILL = dict(rat=6, dur=2.0, curve='accel', p1=1.55, g1=0.55, hold=0.72)
DRAG = dict(rat=4, dur=2.0, curve='decel', p0=1.12, p1=0.78, g1=0.7, hold=0.80)
BURST = dict(rat=9, dur=2.0, curve='even', semis=[0, 0, 3, 0, 5, 0, 7, 3, 12],
             g1=0.5, hold=0.58, drift=0.25)
GALLOP = dict(rat=6, dur=2.0, curve='gallop', p1=1.25, g1=0.6, hold=0.68)
STRETCH2 = dict(str_=2.0, gain=0.85)
BACKWARDS = dict(rev_=True, pitch=0.75, gain=0.9)
SPLIT = dict(rat=3, dur=1.0, curve='even', p1=2.0, g1=0.75, hold=0.8)


def bar_locks(b, level=1, seed=0):
    """How badly this bar stutters.

    level 0  nothing - the break plays
    level 1  one interference, on a weak step
    level 2  two, one of them on the second snare
    level 3  three or four, including a whole beat replaced

    The positions rotate on a five-bar cycle against a four-bar phrase, so
    the same interference never lands in the same place twice inside a
    sixteen-bar section."""
    r = np.random.RandomState(seed * 977 + b)
    out = {}
    if level <= 0:
        return out
    spot = [14, 7, 11, 15, 6][b % 5]
    out[spot] = [TRILL, DRAG, GALLOP, SPLIT, TRILL][(b // 2) % 5]
    if level >= 2:
        out[12] = dict(BURST) if b % 4 == 3 else dict(TRILL, rat=4, p1=0.7)
    if level >= 3:
        out[4] = dict(STRETCH2) if b % 8 in (5,) else dict(BACKWARDS)
        if r.rand() < 0.5:
            out[10] = dict(rat=5, dur=1.5, curve='accel', p1=1.9, g1=0.5,
                           crush=6, down=3)
        else:
            out[2] = dict(pitch=r.choice([0.5, 0.75, 1.5]), gain=0.85)
    return out


def cell_for(b, level):
    if level >= 3 and b % 8 == 7:
        return 'E'
    return CELLS[['B', 'A', 'C', 'A'][(b // 2) % 4] if level else 'A']


def brk(b, level=1, gain=1.0, cell=None, hats=1.0, seed=0, extra_locks=None,
        swing=0.0):
    """One bar of chopped break."""
    tab = cell or cell_for(b, level)
    locks = bar_locks(b, level, seed)
    if extra_locks:
        locks.update(extra_locks)
    edit(s, b, tab, locks=locks, gain=gain, ghost=hats, seed=seed + b,
         swing=swing, bus='break')


# ============================================================ the bass
def bassline(b0, bars=8, gain=1.0, alt=False, busy=False, subg=1.0):
    """Sub and wood, both rendered as one oscillator across the whole block.

    The notes are the chord roots plus a passing note into each change; the
    sub carries them mono under 145 Hz and `wood` puts the same line in the
    200-1500 Hz band, which is the only place a phone will hear a bass at
    all."""
    notes, wnotes = [], []
    for k in range(bars):
        b = b0 + k
        r = ROOT[chord_at(b, alt)]
        st = k * 16
        notes.append((st, r))
        wnotes.append((st, r))
        if busy:
            wnotes.append((st + 6, r + 12))
            wnotes.append((st + 10, r))
        if k % 2 == 1:
            nxt = ROOT[chord_at(b + 1, alt)]
            notes.append((st + 14, nxt - 2 if nxt > r else nxt + 2))
            wnotes.append((st + 14, nxt - 2 if nxt > r else nxt + 2))
        else:
            notes.append((st + 10, r + 7))
            wnotes.append((st + 10, r + 7))
    # Six steps of overhang: the last note of a block is an approach note
    # into the next chord, and cutting it at the bar line kills the one event
    # that makes the line lean forward. Session.place sums, so the blocks
    # overlapping costs nothing.
    s.place(s.pos(b0), subbar(tuple(notes), 16 * bars + 6, h2=0.44, h3=0.11,
                              decay=0.0, glide=0.028), subg * 0.95, 'sub')
    s.place(s.pos(b0), wood(tuple(wnotes), 16 * bars + 6, decay=0.26,
                            cut=(300, 1650), tone=0.60), gain * 0.5, 'bass')


# ============================================================ harmony
# There is no chord instrument on this record.
#
# A chord played by a keyboard - any keyboard - arrives as one event with one
# spectrum, and next to a break that has been cut into thirty pieces it reads
# as something pasted in from a different session. So the harmony is carried
# by two things that are not keyboards: a string section that never has an
# attack at all, and single felt-piano notes dropped one at a time. Between
# them they say the same four chords, and neither of them ever plays a block.
def bed(b, alt=False, dur=32, gain=1.0, seed=0, voices=4, cut=2400):
    """The chord as a section: separate players, separate entries, separate
    intonation. It fades up rather than starting."""
    ch = [midi(n) for n in CH[chord_at(b, alt)]]
    y = ens(ch, dur, voices=voices, cutoff=cut, attack=0.42, bow=0.55,
            seed=seed + b)
    # A section that holds one colour for two bars is a synth pad. Opening a
    # resonant filter across the phrase is what a bow does when the player
    # leans into the note, and it is the difference between a chord and a
    # crescendo.
    n = len(y)
    lane = np.geomspace(cut * 0.42, cut * 1.35, n)
    y = svf(y, lane, 1.15, 'lp', block=256)
    s.place(s.pos(b), chorus(y, voices=2, depth_ms=4.0, rate=0.21, mix=0.32),
            gain, 'pad')


def drops(b, alt=False, gain=0.5, n=3, vel=0.5, at=(2, 7, 11), octave=1,
          seed=0, dur=6):
    """Two or three notes of the chord, one at a time, in the octave above the
    tune. Arpeggiated rather than voiced: the harmony is stated across the bar
    instead of at the start of it."""
    ch = CH[chord_at(b, alt)]
    rs = np.random.RandomState(seed * 31 + b)
    picks = [ch[i % len(ch)] for i in rs.permutation(len(ch))[:n]]
    for st, nt in zip(at, picks):
        s.place(s.pos(b, st + rs.uniform(-0.12, 0.12)),
                felt([midi(nt + 12 * octave)], dur, vel=vel * (0.75 + 0.5 * rs.rand()),
                     roll=0.0, seed=int(nt) + b, hammer=0.5, spread=0.0,
                     room=0.4),
                gain, 'keys')


# ============================================================ utilities
def hole(b, s0=14.0, s1=16.0, curve=1.4):
    """Cut everything to silence over the end of a bar."""
    a, e = s.pos(b, s0), s.pos(b, s1)
    ramp = np.linspace(1, 0, e - a)[:, None] ** curve
    for name in s.bus:
        s.bus[name][a:e] *= ramp


def sweep(b0, b1, bus, f0, f1, kind='lp', q=1.1):
    a, e = s.pos(b0), s.pos(b1)
    if bus not in s.bus:
        return
    s.bus[bus][a:e] = svf(s.bus[bus][a:e], np.geomspace(f0, f1, e - a), q, kind,
                          block=256)


def level(b0, b1, g0, g1, buses, curve=1.0):
    """Ramp whole buses across a range of bars, after the fact."""
    a, e = s.pos(b0), s.pos(b1)
    ramp = (np.linspace(g0, g1, e - a) ** curve)[:, None]
    for name in buses:
        if name in s.bus:
            s.bus[name][a:e] *= ramp


def riser_in(b, bars=4, gain=0.5):
    s.place(s.pos(b), riser(16 * bars, f0=200, f1=900), gain, 'atmos')


# ================================================================ intro 0-15
for b in range(0, 16, 4):
    s.place(s.pos(b), hush(64, seed=b, lo=500, hi=4800), 1.0, 'atmos')
    s.place(s.pos(b), crackle(64), 0.35, 'atmos')

for b in range(0, 16, 2):
    bed(b, dur=32, gain=0.55 if b < 8 else 0.75, seed=2)
    if b >= 6:
        drops(b, gain=0.32, n=2, vel=0.4, at=(3, 11), seed=2)

# The break arrives as a rumour: one bar in four, filtered down to a thud,
# and already stuttering.
for b in (4, 8, 12, 14):
    brk(b, level=1 if b < 12 else 2, gain=0.55 if b < 12 else 0.75,
        extra_locks={0: dict(cut=900, kind='lp', q=0.8)}, seed=3)
for b in range(8, 16):
    kit(b, gain=0.5 if b < 12 else 0.75, snares=(4, 12) if b >= 10 else (12,),
        seed=b)
s.place(s.pos(2), grains(S, 32, density=16, seed=11, pitch=(0.35, 1.2)), 0.5, 'atmos')
s.place(s.pos(10), grains(C, 32, density=22, seed=12, pitch=(0.4, 1.6)), 0.35, 'atmos')
theme(8, gain=0.30, from_=0, to=16, vel=0.42)
sweep(0, 12, 'break', 380, 2600)
riser_in(14, 2, 0.35)
roll(s, 15, 8, 8, 0.5, gain=0.5, accel=True, p1=1.3)

# ============================================================= approach 16-31
for b in range(16, 32):
    lvl = 1 if b < 24 else 2
    brk(b, level=lvl, gain=0.92, seed=5)
    kit(b, gain=0.95, seed=b)
    if b % 2 == 0:
        bed(b, gain=0.75, seed=3)
    if b >= 20 and b % 4 == 2:
        drops(b, gain=0.36, n=2, vel=0.48, at=(6, 13), seed=3)
for b0 in (16, 24):
    bassline(b0, 8, gain=0.75, subg=0.8, busy=b0 >= 24)
s.place(s.pos(16), C, 0.5, 'break')
for b in range(18, 32, 4):
    s.place(s.pos(b), hush(64, seed=b, lo=700, hi=6000), 0.7, 'atmos')
theme(24, gain=0.38, from_=0, to=32, vel=0.5)

# ============================================================== build 1 32-39
for b in range(32, 40):
    brk(b, level=2 if b < 38 else 3, gain=0.95, seed=9)
    kit(b, gain=1.0, seed=b, extra=(6, 14) if b >= 36 else ())
    if b % 2 == 0:
        bed(b, gain=0.8, seed=4)
bassline(32, 8, gain=0.8, subg=0.9, busy=True)
sweep(36, 40, 'break', 200, 400, kind='hp', q=0.9)
riser_in(36, 4, 0.55)
roll(s, 38, 8, 8, 0.5, gain=0.55, accel=True, p1=1.4)
roll(s, 39, 0, 16, 0.5, gain=0.7, accel=True, p0=0.9, p1=1.7)
s.place(s.pos(40) - len(C), rev(C), 0.8, 'break')
hole(39, 15.0, 16.0, 2.2)

# ============================================================== DROP 1 40-71
s.place(s.pos(40), subdrop(10, 85, 30), 0.45, 'sub')
s.place(s.pos(40), C, 0.75, 'break')
for b in range(40, 72):
    lvl = 2 if b % 8 < 6 else 3
    brk(b, level=lvl, gain=1.0, seed=13, swing=0.02 if b % 4 == 2 else 0.0)
    kit(b, gain=1.0, seed=b, extra=(6,) if b % 4 == 1 else ())
    if b % 2 == 0:
        bed(b, gain=0.85, seed=5)
    if b % 4 == 1:
        drops(b, gain=0.40, n=3, vel=0.55, at=(2, 7, 13), seed=5)
    if b % 8 == 7:
        s.place(s.pos(b, 12), glitch(S1, 7, 2.0, seed=b, crush=6), 0.55, 'break')
    if b == 55:
        s.place(s.pos(b, 8), stut(sl(2, 8, 2), 8, 8.0, curve='accel',
                                  p1=1.35, g1=0.6, hold=0.7, hpf=150), 0.8, 'break')
for b0 in range(40, 72, 8):
    bassline(b0, 8, gain=0.85, subg=1.0, busy=(b0 - 40) // 8 % 2 == 1)
theme(48, gain=0.42, from_=0, to=32, vel=0.6)
theme(64, gain=0.46, from_=0, to=64, vel=0.66, bow=0.30)
for b in (56, 64):
    s.place(s.pos(b), C, 0.5, 'break')
hole(63, 15.0, 16.0)
level(40, 72, 0.87, 0.87, ('break', 'drums', 'keys', 'lead', 'pad', 'bass'))
roll(s, 71, 8, 12, 0.5, gain=0.6, accel=True, p1=1.5)

# =========================================================== breakdown 72-87
# Everything stops. The tune arrives whole, on the felt piano, with the
# section under it and the same tune answering itself a sixth below - and the
# only percussion for eight bars is grains of the break it just came out of.
#
# It is also 4 dB quieter, and that is a level ramp rather than a thinner
# arrangement. A breakdown that swaps loud things for other loud things
# measures the same as the drop and spends the drop that follows it.
for i, b in enumerate(range(72, 88, 2)):
    ch = BREAKD[i % 4]
    s.place(s.pos(b), ens([midi(n) for n in CH[ch]], 32, voices=5,
                          cutoff=2500, attack=0.5, bow=0.6, seed=b), 1.0, 'pad')
    s.place(s.pos(b), subbar(((0, ROOT[ch] - 12), (14, ROOT[ch] - 12)), 32,
                             h2=0.4, h3=0.06), 0.35, 'sub')
for b in range(72, 88, 4):
    s.place(s.pos(b), hush(64, seed=b, lo=400, hi=5200), 1.0, 'atmos')
    s.place(s.pos(b), crackle(64), 0.3, 'atmos')
theme(72, gain=0.62, vel=0.55, bow=0.55)
# one bright answer, damped and an octave up - the only bell on the record
theme(76, gain=0.16, voice='glass', octave=1, from_=32, to=64, decay=0.45,
      spread=0.3)
for st, nt, dur in ANSWER:
    s.place(s.pos(76, st), felt([midi(nt), midi(nt + 7)], dur, vel=0.42,
                                roll=0.075, seed=int(st), room=0.42), 0.5, 'keys')
# the chord spelled out one note at a time, over three beats
for i, b in ((0, 78), (1, 86)):
    ch = BREAKD[(b - 72) // 2 % 4]
    for st, seg in scatter([midi(n + 12) for n in CH[ch]], 10, 3.5, vel=0.42,
                           seed=b, order='random'):
        s.place(s.pos(b, 4 + st), seg, 0.42, 'keys')
s.place(s.pos(74), grains(S, 48, density=14, seed=21, pitch=(0.3, 1.1)), 0.4, 'atmos')
s.place(s.pos(82), grains(C, 32, density=20, seed=22, pitch=(0.5, 1.9)), 0.3, 'atmos')
# the heartbeat returns
for b in range(80, 88):
    kit(b, gain=0.55 if b < 84 else 0.8, kicks=(0, 8), snares=(12,) if b < 84 else (4, 12),
        seed=b)
for b in (84, 86):
    brk(b, level=1, gain=0.5, cell=CELLS['D'], seed=17)
level(72, 88, 0.52, 1.0, ('pad', 'keys', 'lead', 'sub'), curve=0.85)

# ============================================================= build 2 88-95
for b in range(88, 96):
    brk(b, level=2 if b < 92 else 3, gain=0.85 + 0.02 * (b - 88), seed=23)
    kit(b, gain=1.0, seed=b, extra=(6, 14))
    if b % 2 == 0:
        bed(b, alt=True, gain=0.8, seed=6)
bassline(88, 8, gain=0.8, alt=True, subg=0.9, busy=True)
sweep(92, 96, 'break', 180, 520, kind='hp', q=0.9)
riser_in(92, 4, 0.6)
roll(s, 94, 8, 8, 0.5, gain=0.6, accel=True, p1=1.4)
roll(s, 95, 0, 20, 0.4, gain=0.75, accel=True, p0=0.85, p1=1.9)
s.place(s.pos(96) - len(C), rev(C), 0.9, 'break')
hole(95, 15.2, 16.0, 2.4)

# ============================================================= DROP 2 96-127
# Harder. The same groove with three new weapons: a stretched snare that
# takes two steps to say one hit, a tick line on a seven-step cycle that
# never lines up with the bar, and glitches on the eighth.
s.place(s.pos(96), subdrop(10, 90, 27), 0.5, 'sub')
s.place(s.pos(96), C, 0.8, 'break')
for b in range(96, 128):
    lvl = 3 if b % 4 in (2, 3) else 2
    extra = {}
    if b % 8 == 4:
        extra[8] = dict(str_=2.2, gain=0.8)
    if b % 8 == 6:
        extra[6] = dict(rat=7, dur=2.0, curve='decel', p0=1.5, p1=0.6, g1=0.5)
    brk(b, level=lvl, gain=1.0, seed=29, extra_locks=extra,
        swing=0.025 if b % 4 == 1 else 0.0)
    kit(b, gain=1.0, seed=b)
    for k in poly(7, 16, offset=(b * 3) % 7):
        s.place(s.pos(b, k), tick(seed=b * 5 + k, f=2600), 0.22, 'drums')
    if b % 2 == 0:
        bed(b, alt=True, gain=0.82, seed=7)
    if b % 4 == 3:
        drops(b, alt=True, gain=0.42, n=3, vel=0.6, at=(3, 9, 14), seed=7)
    if b % 8 == 7:
        s.place(s.pos(b, 10), glitch(S2, 9, 3.0, seed=b, crush=5, down=5), 0.6, 'break')
    if b == 119:
        s.place(s.pos(b), stut(sl(0, 0, 4), 12, 16.0, curve='decel', p0=1.5,
                               p1=0.7, g1=0.55, hold=0.6, hpf=150), 0.75, 'break')
for b0 in range(96, 128, 8):
    bassline(b0, 8, gain=0.9, alt=True, subg=1.0, busy=True)
theme(104, gain=0.44, from_=0, to=64, vel=0.68)
theme(120, gain=0.48, from_=32, to=128, vel=0.72, bow=0.28)
for b in (104, 112, 120):
    s.place(s.pos(b), C, 0.45, 'break')
hole(111, 14.0, 16.0)
hole(127, 15.0, 16.0, 2.0)
level(96, 128, 0.93, 0.93, ('break', 'drums', 'keys', 'lead', 'pad', 'bass'))

# ========================================================== machines 128-139
# No bass, no chords, no tune: twelve bars of nothing but the knife. This is
# where the record admits what it is made of. The kit still keeps the pulse,
# quieter, and a dub delay turns the ratchets into a room.
for b in range(128, 140):
    kit(b, gain=0.75, seed=b, crack_g=0.8)
    lv = [3, 2, 3, 3][(b - 128) % 4]
    brk(b, level=lv, gain=0.9, seed=31,
        extra_locks={2: dict(rat=5, dur=2.0, curve='gallop', p1=1.4, g1=0.5),
                     10: dict(rev_=True, pitch=0.6)} if b % 4 == 2 else None)
    if b % 4 == 3:
        s.place_echo(s.pos(b, 12), shape(S3, hpf=200, gain=0.8), 0.4,
                     times=4, delay_steps=3.0, fb=0.55, bus='texture')
    if b % 4 == 1:
        s.place(s.pos(b, 8), glitch(K2, 8, 2.5, seed=b, crush=4, down=7), 0.5, 'break')
for b in (130, 134, 138):
    s.place(s.pos(b), grains(BAR3, 32, density=30, seed=b, pitch=(0.5, 2.2)),
            0.35, 'texture')
s.place(s.pos(133, 8), tape_stop(shape(amen.bar(0), hpf=150), 0.45), 0.7, 'break')
s.place(s.pos(137, 0), rewind(shape(amen.bar(2), hpf=150), 3.0), 0.6, 'break')
s.place(s.pos(136), hush(64, seed=99, lo=800, hi=7000), 0.9, 'atmos')
sweep(128, 134, 'break', 5200, 1400)
sweep(134, 140, 'break', 1400, 9000)

# ============================================================ build 3 140-143
for b in range(140, 144):
    brk(b, level=3, gain=1.0, seed=37)
    kit(b, gain=1.0, seed=b, extra=(6, 14))
    bed(b, alt=b % 4 == 3, gain=0.85, seed=8)
bassline(140, 4, gain=0.85, subg=0.95, busy=True)
riser_in(140, 4, 0.7)
roll(s, 142, 8, 10, 0.5, gain=0.6, accel=True, p1=1.5)
roll(s, 143, 0, 24, 0.34, gain=0.8, accel=True, p0=0.8, p1=2.1)
s.place(s.pos(144) - len(C), rev(C), 1.0, 'break')
hole(143, 15.4, 16.0, 2.6)

# ============================================================ DROP 3 144-175
s.place(s.pos(144), subdrop(12, 95, 26), 0.55, 'sub')
s.place(s.pos(144), C, 0.85, 'break')
for b in range(144, 176):
    lvl = 3 if b % 8 not in (0, 4) else 2
    extra = {}
    if b % 8 == 2:
        extra[14] = dict(BURST)
    if b % 8 == 5:
        extra[4] = dict(str_=2.4, gain=0.8)
        extra[12] = dict(rat=11, dur=2.0, curve='accel', p1=2.2, g1=0.35,
                         hold=0.6, drift=0.2)
    if b % 16 == 11:
        extra[8] = dict(rev_=True, str_=1.6, pitch=0.5, gain=0.9)
    brk(b, level=lvl, gain=1.0, seed=41, extra_locks=extra,
        swing=0.02 if b % 4 == 3 else 0.0)
    kit(b, gain=1.0, seed=b, extra=(6,) if b % 2 else ())
    for k in poly(5, 16, offset=(b * 2) % 5):
        s.place(s.pos(b, k), tick(seed=b * 7 + k, f=3100), 0.16, 'drums')
    if b % 2 == 0:
        bed(b, alt=True, gain=0.9, seed=9)
    if b % 8 == 2:
        drops(b, alt=True, gain=0.44, n=3, vel=0.62, at=(2, 6, 11), seed=9)
    if b % 8 == 7:
        s.place(s.pos(b, 12), glitch(S1, 9, 2.0, seed=b, crush=6), 0.55, 'break')
    if b == 167:
        s.place(s.pos(b), stut(sl(3, 4, 2), 14, 16.0, curve='accel', p1=2.0,
                               g1=0.4, hold=0.55, drift=0.3, hpf=150), 0.8, 'break')
for b0 in range(144, 176, 8):
    bassline(b0, 8, gain=0.95, alt=True, subg=1.0, busy=True)
theme(144, gain=0.52, vel=0.75, bow=0.32)
theme(152, gain=0.34, voice='bow', from_=0, to=64)
theme(160, gain=0.55, vel=0.8, bow=0.30)
theme(168, gain=0.52, from_=0, to=80, vel=0.76)
for b in (152, 160, 168):
    s.place(s.pos(b), C, 0.5, 'break')
    bed(b, alt=True, dur=32, gain=0.55, seed=11, voices=5)
hole(159, 15.0, 16.0)
hole(175, 14.5, 16.0, 2.0)

# ============================================================== outro 176-191
for b in range(176, 184):
    brk(b, level=2 if b < 180 else 1, gain=0.9 - 0.06 * (b - 176), seed=43,
        cell=CELLS['D'] if b >= 182 else None)
    kit(b, gain=0.9 - 0.05 * (b - 176), seed=b,
        snares=(4, 12) if b < 182 else (12,))
    if b % 2 == 0:
        bed(b, gain=0.7, seed=12)
bassline(176, 8, gain=0.7, subg=0.85)
theme(176, gain=0.46, from_=0, to=64, vel=0.6, bow=0.25)
sweep(180, 184, 'break', 9000, 900)
for b in range(184, 192, 2):
    ch = ['Cm9', 'Abmaj7', 'Ebmaj9', 'Gm9'][(b - 184) // 2]
    s.place(s.pos(b), ens([midi(n) for n in CH[ch]], 32, voices=5,
                          cutoff=2200, attack=0.55, bow=0.5, seed=b), 0.9, 'pad')
    s.place(s.pos(b), subbar(((0, ROOT[ch] - 12),), 32, h2=0.35, h3=0.05), 0.3, 'sub')
for b in range(184, 192, 4):
    s.place(s.pos(b), hush(64, seed=b, lo=400, hi=4200), 0.9, 'atmos')
    s.place(s.pos(b), crackle(64), 0.35, 'atmos')
theme(184, gain=0.40, from_=0, to=32, vel=0.45, bow=0.35)
s.place(s.pos(190), glass(midi(67), 24, decay=1.6, damp=2200), 0.26, 'lead')

# ================================================================ mix
for name, kw in (('keys', dict(decay=1.8, wet=0.20, tone=4200)),
                 ('lead', dict(decay=2.4, wet=0.26, tone=4600)),
                 ('pad', dict(decay=3.4, wet=0.30, tone=3200)),
                 ('texture', dict(decay=2.0, wet=0.35, tone=5000))):
    if name in s.bus:
        s.bus[name] = bus_reverb(s.bus[name], **kw)

# The break is where all the width is: it was recorded in a room with cymbals
# and the edits scatter it across the field. Everything else stays near the
# middle, so the stutters read as movement rather than as a wide mix.
s.bus['break'] = side_boost(s.bus['break'], 2200, 0.8)
# The cymbals are in the sample and the sample is from 1969, so the air above
# 9 kHz has to be put back rather than turned up.
s.bus['break'] = shelf(s.bus['break'], 8800, 4.5, 'high')
s.bus['break'] = peak_eq(s.bus['break'], 2500, 2.0, 0.8)
# Ratchets, glitches and buffer repeats sum: a bar where all three land inside
# one beat peaks 8 dB above the rest of the record. Catching that here, on the
# bus, costs one transient; leaving it for the master clipper costs 8 dB off
# whatever else is playing at that moment.
s.bus['break'] = softclip(s.bus['break'], 1.15, knee=0.7)
s.bus['keys'] = hp(s.bus['keys'], 170, 2)
s.bus['pad'] = hp(s.bus['pad'], 190, 2)
s.bus['lead'] = hp(s.bus['lead'], 150, 2)
s.bus['atmos'] = hp(s.bus['atmos'], 280, 2)
if 'texture' in s.bus:
    s.bus['texture'] = hp(s.bus['texture'], 260, 2)

# Scaled so the bus sum peaks a little over 1.0. The clipper then shaves the
# tips of two or three transients a bar - which is inaudible - instead of a
# quarter of the record, which is the "it sounds distorted" complaint.
GAINS = {'break': 1.60, 'drums': 0.50, 'sub': 0.29, 'bass': 0.78,
         'keys': 1.35, 'pad': 0.78, 'lead': 1.20, 'atmos': 0.60,
         'texture': 1.00}
s.report(GAINS)

# Clipper first, then glue, then the look-ahead limiter. In that order the
# limiter never has to duck a whole bar to catch one sample. This lands
# deliberately short of a neurofunk master's density: the whole point of the
# record is that a bar can empty out, and a crest of 4 dB would fill the
# holes back in.
s.render('amen_zaika_174.wav', drive=0.0, duck=0.28, duck_rel=0.095,
         limit=0.0, peak=0.99, gains=GAINS, clip=1.15, fade=2.4,
         comp=dict(thresh=0.34, ratio=2.2, attack=0.008, release=0.12,
                   makeup=1.15),
         brick=dict(gain=1.28, ceiling=0.89, release=0.080))
