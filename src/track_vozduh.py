"""VOZDUH (~4:51, 208 bars @174) - liquid drum & bass in E dorian.

The opposite problem to a drill track. There the break was torn apart; here it
has to ROLL - stay continuous for four minutes without ever playing the same
bar twice. The move is `roll()`: the anchors (kick on 1, snare on 2, kick on
the and-of-3, snare on 4) are nailed down and never move, and only the ghost
notes between them are dealt out fresh - reversed, pitched, half-speed,
borrowed from another bar. The count is rock solid, the surface never repeats.
That is the whole difference between a roller and a loop.

One tune, never played the same way twice. Nine voices take turns with it -
glass, bell, pluck, a formant choir, a diva, a muted horn and the same horn
with a fall-off, a vibrato lead, piano, rhodes, strings - and every statement
is a different transformation: a diatonic sequence two degrees up, an
inversion, a fragment, an augmentation at half speed, an ornamented version
with grace notes. Between the statements are the flight shapes, which is what
this track is actually about: rise() climbs in terraces that close up as they
go, cascade() falls straight down the scale, flutter() beats two neighbouring
notes against each other. A slow voice is placed EARLY by its measured attack
(PRE_MS) so its peak lands on the beat instead of a third of a bar behind it -
vox takes 290 ms to speak and a step here is 86 ms.

Air is a mix decision more than a note decision:
  - the theme sits at MIDI 76-97, above everything else in the arrangement
  - the pad is high-passed and swept with notches rather than a lowpass: a
    moving lowpass reads as brightness, which is another way of saying louder;
    a moving notch reads as motion, because the ear tracks the travelling gap
  - reverbs are kept under 2.6 s - at 174 BPM a 3 s tail covers two bars and
    turns everything to fog, which is the usual way "atmospheric" goes wrong
  - the sub is short and clean; weight comes from the note being low, not loud

Harmony: Em9 - A6/9 - Dmaj9 - Bm7, two bars each, voiced rootless so the bass
owns the bottom. Voice leading is nearly static - three common tones between
every pair - and the dorian C# sits inside the middle two chords, which is the
light that keeps this from being a sad record.

  b0-15    air only: rhodes, pad, crackle, the break far away behind a filter
  b16-31   the roll arrives, sub underneath
  b32-63   drop 1: the roller
  b64-87   breakdown: drums gone, a climb, then the diva takes the tune
  b88-95   build
  b96-143  drop 2: 48 bars, the long one, arp and counter-theme layered in
  b144-159 the turn: chords a fourth away, halftime, the horn dives
  b160-191 drop 3: everything, the theme up an octave
  b192-207 outro: the roll thins out to a pulse and a held chord
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(0x5EA)
np.random.seed(0x5EA)
s = Session(208, tail=4.0)

# ------------------------------------------------------------------ key ----
# rootless voicings: the bass owns the bottom, these just colour it
CHORDS = [[55, 59, 62, 66],      # Em9    G  B  C  F#  -> E G B D F#
          [54, 59, 61, 64],      # A6/9   F# B  C# E
          [54, 57, 61, 64],      # Dmaj9  F# A  C# E
          [54, 57, 59, 62]]      # Bm7    F# A  B  D
ROOTS = [28, 33, 38, 35]         # E1 A1 D2 B1 - 41, 55, 73, 62 Hz
MIDS  = [40, 45, 50, 47]         # an octave up: what a phone reconstructs from
SCALE = [76, 78, 79, 81, 83, 85, 86, 88, 90]     # E dorian, E5 to F#6

# The theme: 8 bars, one phrase per chord, long notes and long holes.
# Every note is a chord tone or a 6th/9th/13th over the chord under it.
THEME = [(0, 83), (6, 88), (10, 86), (14, 83),          # over Em9
         (32, 85), (38, 81), (44, 83),                  # over A6/9
         (64, 78), (68, 83), (74, 85), (78, 88),        # over Dmaj9
         (98, 86), (104, 83), (108, 78)]                # over Bm7

TICK32 = int(0.5 * STEP)
TICK64 = int(0.25 * STEP)

def swirl(seg, rate=0.22, lo=380.0, hi=3200.0, depth=0.72, bands=5):
    """Two notches sweeping together across the pad.

    A moving lowpass reads as brightness - the pad gets brighter and duller,
    which is another way of saying louder and quieter. A moving notch reads as
    motion instead: the ear tracks the travelling gap, not the tone, so the pad
    moves without ever changing weight. That is what keeps this mix airy while
    something is always happening inside it."""
    n = len(seg)
    t = np.arange(n) / SR
    env = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t)
    fs = np.geomspace(lo, hi, bands)
    u = env * (bands - 1)
    out = np.array(seg, dtype=np.float32)
    for i, f in enumerate(fs):
        w = np.clip(1.0 - np.abs(u - i), 0.0, 1.0)
        if w.max() < 1e-4:
            continue
        cut = bandpass(seg, f * 0.86, f * 1.16)
        cut = cut + bandpass(seg, f * 2.3 * 0.86, min(f * 2.3 * 1.16, SR * 0.45))
        out -= (depth * 0.5) * (cut * w[:, None]).astype(np.float32)
    return out.astype(np.float32)

def ci(b):  return (b // 2) % 4          # chords move every two bars

# ------------------------------------------------------------ the roll ----
# ghost slices: quiet hits from the break that are not the count
GHOSTS = [(0, 6), (0, 7), (0, 9), (0, 14), (0, 15), (2, 6), (3, 2), (3, 6),
          (1, 6), (1, 9), (2, 9), (3, 14)]
ANCHORS = [(0, K, 1.00), (4, SN, 0.98), (10, K2, 0.86), (12, S2, 0.98)]

def roll(b, heat=0.5, gain=0.92, ghost_g=0.44, seed=0, anchors=ANCHORS,
         air=0.35):
    """The liquid roller. The anchors are sacred and never move; the ghosts
    between them are re-dealt every bar. A break that repeats is a loop - a
    break whose ghosts change is a drummer."""
    r = np.random.default_rng(0x11FE + b * 13 + seed)
    for st, seg, g in anchors:
        s.place(s.pos(b, st), seg, gain * g)
        if st in (0, 10):
            s.hit(s.pos(b, st))
    for st in (1, 2, 3, 5, 6, 7, 9, 11, 13, 14, 15):
        if r.random() > 0.30 + heat * 0.55:
            continue
        gb, gs = GHOSTS[int(r.integers(len(GHOSTS)))]
        seg = get(gb, gs, 1.0)
        d = r.random()
        if d < 0.16:   seg = rev(seg)                       # a breath before the beat
        elif d < 0.28: seg = pitched(seg, float(r.choice([1.5, 2.0])))
        elif d < 0.36: seg = pitched(seg, 0.5)
        elif d < 0.44 * heat + 0.08:
            seg = hp(seg, 2200)                             # only the top of the hit
        if r.random() < air:
            seg = shelf(seg, 6000, 3.5)
        s.place(s.pos(b, st), panned(seg, float(r.uniform(-0.5, 0.5))),
                ghost_g * float(r.uniform(0.5, 1.0)))

def breathe(b, gain=0.9, lo=420, hi=9000, rate=0.5, src=0):
    """a whole bar of break under a filter that opens and closes across it -
    movement without another element"""
    bar = bar_of(src)
    t = np.arange(len(bar)) / SR
    env = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t / (len(bar) / SR))
    s.place(s.pos(b), morph_lp(bar, lo, hi, env, bands=7), gain)
    s.hit(s.pos(b, 0))

def ghostwash(b0, b1, cycle=7, gain=0.055):
    """high, reversed ghost hits on a 7-step cycle: the air between the drums.
    Seven against sixteen means it lands somewhere new for seven bars."""
    src = shelf(shelf(hp(rev(get(0, 6, 1)), 3400), 9000, 5.0), 13000, 5.0)
    for i in range(int((b1 - b0) * 16 / cycle)):
        s.place(s.pos(b0) + int(i * cycle * STEP),
                panned(src, np.sin(i * 2.3) * 0.85), gain)

def edit(b, n=32, keep=(0, 4, 10, 12), seed=0, gain=0.9, warp=0.25):
    """micro-slice shuffle with the count pinned - the zub4atka move, used
    sparingly here because liquid wants continuity, not damage"""
    r = np.random.default_rng(0xED17 + seed)
    pieces = amen.chop(n, bar=0)
    slots = list(range(n))
    free = [i for i in slots if i * 16 // n not in keep]
    shuffled = list(free); r.shuffle(shuffled)
    m = dict(zip(free, shuffled))
    for slot in slots:
        pick = m.get(slot, slot)
        seg = pieces[pick]
        if slot not in [k * n // 16 for k in keep] and r.random() < warp:
            seg = rev(seg) if r.random() < 0.5 else pitched(seg, 2.0)
        s.place(s.pos(b) + int(slot * 16 / n * STEP), seg,
                gain if pick * 16 // n in keep else gain * 0.66)

# ---------------------------------------------------------- instruments ----
def keys(b, gain=0.10, dur=8, spread=0.35):
    """rhodes, the sound of the genre: struck once per chord, left to ring"""
    ch = [midi(n) for n in CHORDS[ci(b)]]
    s.place(s.pos(b), reverb(panned(shelf(rhodes(ch, dur, 0.9), 3200, 3.0), spread),
                             decay=2.2, wet=0.34, tone=6200), gain, 'music')

def padchord(b, gain=0.075, dur=32, cut=2600, sweep=0.22):
    """the pad never gets louder, it only moves: swept notches instead of a filter
    envelope, high-passed at 300 so it never touches the bass"""
    ch = [midi(n) for n in CHORDS[ci(b)]]
    p = pad(ch, dur, cut, wide=0.7)
    p = swirl(p, rate=sweep, lo=380, hi=3400, depth=0.72)
    s.place(s.pos(b), hp(shelf(shelf(p, 6000, 3.0), 12000, 5.0), 230), gain, 'pad')

# ---------------------------------------------------------- the melody ----
# One tune is not a part. These are the transformations from
# theory/00-foundations/08-melody.md, and every statement in the track picks a
# different voice and a different transformation, so the tune is recognisable
# the whole way through and never arrives the same way twice.
LADDER = [64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 85, 86, 88, 90, 91,
          93, 95, 97, 98]                      # E dorian, four octaves

def _ix(n):
    return min(range(len(LADDER)), key=lambda i: abs(LADDER[i] - n))

def seq(notes, k):
    """diatonic sequence: the same shape, k scale degrees away"""
    return [(st, LADDER[max(0, min(len(LADDER) - 1, _ix(n) + k))]) for st, n in notes]

def invert(notes):
    """flip every interval around the first note - the bird turning over"""
    a = _ix(notes[0][1])
    return [(st, LADDER[max(0, min(len(LADDER) - 1, a - (_ix(n) - a)))]) for st, n in notes]

def frag(notes, a, b, shift=0.0):
    """take a piece of it and move it - urgency without new material"""
    return [(st + shift, n) for st, n in notes[a:b]]

def augment(notes, f=2.0):
    """stretch it out: the same line, half the speed, twice the air"""
    return [(st * f, n) for st, n in notes]

def ornament(notes, rng_):
    """grace notes a step above, landing on the beat - a flick of the wing"""
    out = []
    for st, n in notes:
        if rng_.random() < 0.45 and st >= 1:
            out.append((st - 0.5, LADDER[min(len(LADDER) - 1, _ix(n) + 1)]))
        out.append((st, n))
    return out

# flight shapes
def rise(st0, lo=76, n=9, span=14.0, climb=8):
    """terraced climb with the steps closing up as it goes: gaining height"""
    i0 = _ix(lo)
    u = np.linspace(0, 1, n) ** 1.7
    return [(st0 + float(u[k]) * span,
             LADDER[min(len(LADDER) - 1, i0 + int(round(climb * k / max(n - 1, 1))))])
            for k in range(n)]

def cascade(st0, hi=95, n=12, span=6.0):
    """the dive: straight down the scale, fast, and it lands on a chord tone"""
    i0 = _ix(hi)
    return [(st0 + k * span / n, LADDER[max(0, i0 - k)]) for k in range(n)]

def flutter(st0, note, n=8, span=3.0, width=1):
    """two notes beating against each other - wingbeats"""
    i0 = _ix(note)
    return [(st0 + k * span / n, LADDER[i0 + (width if k % 2 else 0)]) for k in range(n)]

def soar(st0, notes_):
    """long held notes, high, with the vibrato arriving late: hanging on the air"""
    return notes_

# ---- the voices ----------------------------------------------------------
def _v_bell(f, d):   return shelf(blend(bell(f, d), pluck(f, d * 0.4, 0.4)), 9000, 4.0)
def _v_pluck(f, d):  return shelf(pluck(f, max(d * 0.8, 0.5)), 7000, 3.5)
def _v_glass(f, d):  return shelf(bell(f, d * 1.4, 0.8), 11000, 4.5)
def _v_vox(f, d):    return shelf(vox([f], d, 0.9, 'oo'), 6000, 2.0)
def _v_diva(f, d):   return shelf(diva(f, d, 0.75), 7000, 2.5)
def _v_horn(f, d):   return horn(f, d, 0.7, fall=0.0)
def _v_dive(f, d):   return horn(f, d, 0.7, fall=5.0)          # the fall-off
def _v_lead(f, d):   return lp(lead(f, d, 0.55, vib=5.2), 7000)
def _v_piano(f, d):  return shelf(piano([f], d, 0.6), 8000, 2.5)
def _v_keys(f, d):   return shelf(rhodes([f], d, 0.85), 6000, 2.5)
def _v_air(f, d):    return shelf(strings([f, f * 2], d, 0.5), 9000, 3.0)

VOICES = {'bell': _v_bell, 'pluck': _v_pluck, 'glass': _v_glass, 'vox': _v_vox,
          'diva': _v_diva, 'horn': _v_horn, 'dive': _v_dive, 'lead': _v_lead,
          'piano': _v_piano, 'keys': _v_keys, 'air': _v_air}

# Measured attack of each voice, in milliseconds to 90% of peak. A step at 174
# is 86 ms, so a 290 ms attack lands a third of a bar late and the melody smears.
# The fix is the one an orchestrator uses: place the slow instrument EARLY so
# its peak, not its start, arrives on the beat.
PRE_MS = {'bell': 0, 'pluck': 0, 'glass': 0, 'piano': 0, 'keys': 0, 'horn': 0,
          'lead': 55, 'air': 100, 'diva': 200, 'vox': 250, 'dive': 300}

def sing(b0, notes, voice='bell', gain=0.11, oct_=0, wet=0.42, dur=5.0,
         decay=2.4, pan=0.45, tone=6500):
    """one statement of the tune, in one voice, wherever it is asked for"""
    v = VOICES[voice]
    pre = int(PRE_MS.get(voice, 0) * SR / 1000)
    for st, note in notes:
        f = midi(note + 12 * oct_)
        seg = v(f, dur)
        s.place(max(s.pos(b0) + int(st * STEP) - pre, 0),
                reverb(panned(seg, np.sin(st * 0.9 + b0) * pan), decay=decay,
                       wet=wet, tone=tone), gain, 'music')

def theme(b0, gain=0.115, oct_=0, wet=0.42, dur=5.0, notes=None, decay=2.4):
    sing(b0, notes or THEME, 'bell', gain, oct_, wet, dur, decay)

# The second bird: long notes in the gap under the tune, answering it. Every
# note is a chord tone or a 9th/11th over whichever chord is under it.
COUNTER = [(4, 71), (12, 74), (20, 76), (28, 71), (36, 73), (48, 76),
           (60, 74), (68, 78), (80, 76), (92, 73), (104, 71), (116, 74)]

def leadin(b_target, gain=0.20, decay=2.2, src=None):
    """reversed reverb ending exactly on the downbeat - the join you feel and
    do not hear. Cheaper than a riser and it does not raise the level."""
    seg = rev(reverb(src if src is not None else S2, decay=decay, wet=0.95))
    s.place(s.pos(b_target) - len(seg), seg, gain, 'fx')

def blend(*segs):
    n = max(len(x) for x in segs)
    out = np.zeros((n, 2), dtype=np.float32)
    for x in segs:
        out[:len(x)] += x
    return out

def arpline(b, gain=0.055, cycle=7, shape='updown', rate=0.5, octs=(0, 1),
            gate=None, wave='saw', f_hi=7000, decay=0.09, pan=0.6):
    # high-passed off the body band: the theme owns 800-3000, not this
    """arp_seq gives it a cycle coprime with the bar so it walks; arpvoice
    gives every note a filter that closes while it sounds"""
    notes = [n + 12 for n in CHORDS[ci(b)]]
    for st, note, dur, vel in arp_seq(notes, bars=1, shape=shape, rate=rate,
                                      cycle=cycle, octaves=octs, gate=gate,
                                      accents=(0, 3), tail=0.9, rotate=b * 2,
                                      jitter=0.02, seed=b):
        seg = hp(arpvoice(midi(note), max(dur, 0.4), wave=wave, f_lo=700,
                          f_hi=f_hi, res=1.3, decay=decay, detune=0.006), 900)
        s.place(s.pos(b, st), panned(seg, np.sin(st * 1.7) * pan),
                gain * vel, 'music')

def bassline(b, sub_g=0.38, mid_g=0.12, dur=16, note=None):
    i = ci(b)
    root = midi(ROOTS[i] if note is None else note)
    s.place(s.pos(b), sub(root, dur), sub_g, 'bass')
    if mid_g:
        mid = dirty(hp(reese(midi(MIDS[i]), dur, 700), 130), 2.4)
        s.place(s.pos(b), shelf(mid, 800, 4.5), mid_g, 'bass')

# =========================== b0-15: air only ================================
s.place(s.pos(0), crackle(256), 0.34, 'fx')
s.place(s.pos(0), wind(256, 0.5), 0.085, 'fx')
for b in range(0, 16, 2):
    padchord(b, 0.085 if b < 8 else 0.10)
    keys(b, 0.085 if b < 8 else 0.105)
sing(0, THEME, 'glass', 0.085, wet=0.58, decay=2.8, dur=6.0)
sing(8, THEME, 'bell', 0.10, wet=0.5)
sing(13, rise(0, 76, 8, 12.0, 7), 'air', 0.055, wet=0.5, dur=3.0)
for b in range(8, 16):                                  # the break, far off
    s.place(s.pos(b), lp(bar_of(b % 2), 420 + (b - 8) * 190), 0.30 + (b - 8) * 0.03)
ghostwash(12, 16, 7, 0.055)
s.place(s.pos(14), riser(32, 0.30, 200, 800), 1.0, 'fx')

# =========================== b16-31: the roll arrives ========================
s.place(s.pos(16), CR, 0.55)
for b in range(16, 32):
    roll(b, heat=0.30 + (b - 16) * 0.02, gain=0.88, ghost_g=0.38)
    bassline(b, 0.30, 0.09)
    if b % 2 == 0:
        padchord(b, 0.09); keys(b, 0.10)
leadin(16, 0.16)
sing(16, THEME, 'pluck', 0.105, wet=0.40, dur=3.2)
sing(24, THEME, 'bell', 0.11)
sing(24, COUNTER, 'keys', 0.055, wet=0.35, dur=6.0)
sing(30, cascade(4, 93, 11, 7.0), 'glass', 0.075, wet=0.45, dur=1.6)
ghostwash(16, 32, 7, 0.085)
s.pat(31, [(12, SN1, 0.5), (13, SN1, 0.62), (14, SN1, 0.74), (15, SN1, 0.85)])

# =========================== b32-63: drop 1 =================================
s.place(s.pos(32), subdrop(10, 76, 30), 0.40, 'bass')
s.place(s.pos(32), CR, 0.78)
for b in range(32, 64):
    if b % 8 == 6:    breathe(b, 0.88, 500, 8500)
    elif b % 16 == 13: edit(b, 32, seed=b, gain=0.9, warp=0.3)
    else:             roll(b, heat=0.5, gain=0.92)
    bassline(b, 0.35, 0.13)
    if b % 2 == 0:
        padchord(b, 0.075); keys(b, 0.10)
    if b >= 40:
        arpline(b, 0.035, cycle=7, rate=0.5)
leadin(32, 0.20)
sing(32, THEME, 'vox', 0.105, wet=0.42, dur=6.0)
sing(40, seq(THEME, 2), 'bell', 0.115)
sing(40, COUNTER, 'keys', 0.05, wet=0.35, dur=6.0)
sing(48, THEME, 'glass', 0.115, oct_=1, wet=0.45, dur=4.0)
sing(56, frag(THEME, 0, 7), 'pluck', 0.11, wet=0.38, dur=3.0)
sing(58, flutter(8, 88, 8, 3.0), 'bell', 0.075, wet=0.4, dur=1.4)
sing(62, cascade(2, 95, 12, 8.0), 'glass', 0.085, wet=0.5, dur=1.8)
ghostwash(32, 64, 7, 0.105)
ghostwash(36, 64, 11, 0.07)
s.place(s.pos(48), CR, 0.5)
s.pat(63, [(10, SN1, 0.5), (12, SN1, 0.66), (13, SN1, 0.74), (14, SN1, 0.85),
           (15, rev(SN1), 0.7)])

# =========================== b64-87: breakdown ==============================
s.place(s.pos(64), impact(24), 0.26, 'fx')
s.place(s.pos(64), crackle(160), 0.30, 'fx')
for b in range(64, 88, 2):
    padchord(b, 0.135, cut=3200, sweep=0.14)
    keys(b, 0.145, spread=0.45)
sing(64, rise(0, 74, 10, 20.0, 9), 'air', 0.075, wet=0.55, dur=4.0)
sing(66, THEME, 'diva', 0.115, wet=0.55, decay=2.8, dur=6.0)   # the voice
sing(74, augment(THEME, 1.5), 'lead', 0.075, wet=0.5, dur=7.0) # hanging on the air
sing(80, invert(THEME), 'keys', 0.10, wet=0.5, dur=5.0)        # turning over
sing(80, COUNTER, 'glass', 0.06, oct_=1, wet=0.5, dur=3.0)
sing(86, cascade(0, 97, 14, 10.0), 'bell', 0.085, wet=0.5, dur=1.8)
for b in range(72, 88):                                  # a pulse returns
    s.place(s.pos(b, 0), lp(K, 3000), 0.34)
    s.place(s.pos(b, 8), lp(SN, 4200), 0.26)
    s.place(s.pos(b), sub(midi(ROOTS[ci(b)]), 16), 0.22, 'bass')
for b in range(80, 88):
    arpline(b, 0.032, cycle=9, rate=0.5, wave='tri', f_hi=5200)
ghostwash(76, 88, 7, 0.075)

# =========================== b88-95: build ==================================
for b in range(88, 96):
    roll(b, heat=0.35 + (b - 88) * 0.06, gain=0.55 + (b - 88) * 0.05,
         ghost_g=0.3 + (b - 88) * 0.03)
    bassline(b, 0.24 + (b - 88) * 0.012, 0.08)
    if b % 2 == 0:
        padchord(b, 0.11); keys(b, 0.115)
    arpline(b, 0.035, cycle=7, rate=0.5)
sing(88, rise(0, 71, 14, 28.0, 13), 'air', 0.085, wet=0.45, dur=3.0)
sing(90, THEME, 'bell', 0.105)
s.place(s.pos(92), riser(64, 0.40, 200, 1100), 1.0, 'fx')
for st in np.arange(8, 16, 0.5):
    s.place(s.pos(95, st), SN1, 0.30 + (st - 8) * 0.055)

# =========================== b96-143: drop 2, the long one ==================
s.place(s.pos(96), subdrop(12, 84, 28), 0.44, 'bass')
s.place(s.pos(96), CR, 0.85)
for b in range(96, 144):
    if b % 8 == 6:     breathe(b, 0.9, 520, 9500, rate=0.5)
    elif b % 16 == 11: edit(b, 32, seed=b * 3, gain=0.92, warp=0.35)
    elif b % 16 == 15: roll(b, heat=0.8, gain=0.92, ghost_g=0.52)
    else:              roll(b, heat=0.55, gain=0.93)
    bassline(b, 0.36, 0.15)
    if b % 2 == 0:
        padchord(b, 0.07); keys(b, 0.095)
    arpline(b, 0.038, cycle=[7, 9, 11][(b // 8) % 3], rate=0.5,
            shape=['updown', 'converge', 'thumb'][(b // 16) % 3],
            wave='saw' if b % 4 else 'square')
leadin(96, 0.22)
PLAN = [(96,  THEME,               'bell',  0.115, 0),
        (104, seq(THEME, 2),       'vox',   0.105, 0),
        (112, THEME,               'horn',  0.095, 0),
        (120, THEME,               'glass', 0.115, 1),
        (128, ornament(THEME, rng),'pluck', 0.100, 0),
        (136, invert(THEME),       'piano', 0.090, 0)]
for b0, nts, v, g, oc in PLAN:
    sing(b0, nts, v, g, oct_=oc, wet=0.42, dur=5.0)
for b0 in (100, 116, 132):
    sing(b0, COUNTER, 'keys', 0.05, wet=0.35, dur=6.0)
sing(110, flutter(8, 90, 10, 3.5), 'bell', 0.07, wet=0.4, dur=1.3)
sing(126, flutter(4, 85, 8, 3.0, 2), 'glass', 0.07, wet=0.45, dur=1.5)
sing(142, cascade(0, 97, 14, 11.0), 'glass', 0.09, wet=0.5, dur=1.8)
ghostwash(96, 144, 7, 0.115)
ghostwash(100, 144, 11, 0.08)
ghostwash(98, 144, 5, 0.06)
s.place(s.pos(112), CR, 0.5); s.place(s.pos(128), CR, 0.55)
s.pat(143, [(8, SN1, 0.45), (10, SN1, 0.55), (12, SN1, 0.68), (13, SN1, 0.76),
            (14, SN1, 0.86), (15, SN1, 0.95)])

# =========================== b144-159: the turn =============================
# same shapes a fourth away - the only new harmony in the track
TURN = [40, 45, 38, 33]                                  # E2 A2 D2 A1
for b in range(144, 160):
    s.pat(b, [(0, K, 0.85), (8, SN, 0.82), (14, K2, 0.5)])
    s.hit(s.pos(b, 0))
    s.place(s.pos(b, 6), get(0, 6, 1), 0.3)
    s.place(s.pos(b), sub(midi(TURN[(b // 4) % 4]), 16), 0.30, 'bass')
    if b % 2 == 0:
        padchord(b, 0.125, cut=3000, sweep=0.16); keys(b, 0.13)
    if b >= 152:
        arpline(b, 0.035, cycle=9, rate=0.5, wave='tri', f_hi=6000)
sing(144, THEME, 'dive', 0.115, wet=0.5, dur=6.0)      # horn with the fall-off
sing(148, COUNTER, 'keys', 0.06, wet=0.4, dur=6.0)
sing(152, seq(THEME, 2), 'piano', 0.10, wet=0.45, dur=4.0)
sing(156, rise(0, 78, 12, 22.0, 11), 'air', 0.08, wet=0.45, dur=3.0)
ghostwash(148, 160, 7, 0.085)
s.place(s.pos(158), riser(32, 0.38, 220, 1200), 1.0, 'fx')

# =========================== b160-191: drop 3 ===============================
s.place(s.pos(160), subdrop(10, 80, 29), 0.42, 'bass')
s.place(s.pos(160), CR, 0.85)
for b in range(160, 192):
    if b % 8 == 6:     breathe(b, 0.9, 560, 10000)
    elif b % 16 == 13: edit(b, 32, seed=b * 7, gain=0.92, warp=0.4)
    else:              roll(b, heat=0.62, gain=0.94, ghost_g=0.5)
    bassline(b, 0.36, 0.16)
    if b % 2 == 0:
        padchord(b, 0.075); keys(b, 0.095)
    arpline(b, 0.042, cycle=[9, 7, 11][(b // 8) % 3], rate=0.5,
            shape=['converge', 'updown'][(b // 8) % 2], octs=(0, 1))
leadin(160, 0.22)
sing(160, THEME, 'bell', 0.125, oct_=1, wet=0.42, dur=4.0)
sing(160, COUNTER, 'pluck', 0.06, wet=0.35, dur=4.0)
sing(168, seq(THEME, 2), 'diva', 0.105, wet=0.48, dur=6.0)
sing(176, THEME, 'vox', 0.10, wet=0.45, dur=6.0)
sing(178, flutter(10, 93, 10, 3.5), 'glass', 0.075, wet=0.45, dur=1.4)
sing(184, augment(THEME, 1.5), 'lead', 0.08, wet=0.5, dur=7.0)
sing(190, cascade(0, 98, 15, 12.0), 'bell', 0.095, wet=0.5, dur=1.8)
ghostwash(160, 192, 7, 0.115)
ghostwash(164, 192, 11, 0.085)
s.place(s.pos(176), CR, 0.5)

# =========================== b192-207: outro ================================
for b in range(192, 200):
    g = 0.9 - (b - 192) * 0.10
    if b < 196:
        roll(b, heat=0.35, gain=g, ghost_g=0.30)
    else:
        s.pat(b, [(0, K, g * 0.8), (8, SN, g * 0.7)])
        s.hit(s.pos(b, 0))
    s.place(s.pos(b), sub(midi(ROOTS[ci(b)]), 16), 0.26 - (b - 192) * 0.02, 'bass')
    if b % 2 == 0:
        padchord(b, 0.11); keys(b, 0.11)
sing(192, THEME, 'glass', 0.115, wet=0.55, decay=2.8, dur=5.0)
sing(196, COUNTER, 'keys', 0.05, wet=0.4, dur=6.0)
s.place(s.pos(198), crackle(160), 0.34, 'fx')
s.place(s.pos(198), wind(160, 0.5), 0.09, 'fx')
for b in range(200, 208, 2):
    padchord(b, 0.10 - (b - 200) * 0.008, dur=32, cut=2200, sweep=0.1)
keys(200, 0.10); keys(204, 0.085, dur=16)
sing(200, [(st, n) for st, n in THEME if st < 48], 'keys', 0.095,
     wet=0.6, decay=3.0, dur=6.0)                        # the phrase, unfinished
s.place(s.pos(206), reverb(bell(midi(88), 6), decay=5.0, wet=0.8), 0.085, 'music')
s.place(s.pos(206), sub(midi(28), 16), 0.12, 'bass')

s.bus['music'] = mono_below(s.bus['music'], 260)
s.bus['pad'] = mono_below(s.bus['pad'], 460)
s.bus['bass'] = mono_below(s.bus['bass'], 120)
s.bus['main'] = shelf(shelf(s.bus['main'], 5600, 2.6), 12000, 5.0)
s.bus['main'] = shelf(s.bus['main'], 240, -1.3, 'low')  # room for the pad
s.bus['music'] = shelf(s.bus['music'], 12500, 4.0)

GAINS = {'main': 1.16, 'bass': 0.55, 'music': 0.99, 'pad': 1.95, 'fx': 0.70}
s.report(GAINS)
s.render('amen_vozduh_174.wav', drive=1.15, duck=0.30, limit=0.94,
         clip=1.0, gains=GAINS, fade=2.5)
