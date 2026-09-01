"""CLASSIC MONTAGE - phonk house at 156 BPM, G minor with a Phrygian bII.

Phonk timbres on a hard-dance skeleton, with the low end of a Brazilian
montagem. The kick is on every beat, the open hat is on every offbeat, the
cowbell plays straight 8ths over the top, and the sub is eight punctuated
events a bar - never a drone.

    hook | walk-in | DROP 1 | breather | build | DROP 2 | MONTAGEM | DROP 3 | out

Three things came out of measuring the references (MONTAGEM LADRAO/TOMADA,
Amor Na Praia, CUTE DEPRESSED, AVANGARD) rather than out of memory:

1. They put 55-60% of their energy under 120 Hz and almost none above 6 kHz,
   and the weight sits at 60-120 rather than under 60 - that is audible
   weight, not just felt weight, and it survives a phone.
2. Their low band always has gaps. A note on the beat, its tail through the
   next 16th, then silence. That silence is what lets the sub be that loud
   and still have a pulse you can jump to.
3. Beat 4 is the loudest event in the bar and it moves - to the next chord,
   or to the b6 below - and every eighth bar ends on a chromatic climb.

The melody is five themes, not one, and what separates them is rhythm:
`hook` hammers straight 8ths, `tres` is a 3+3+2, `run` is bursts of 16ths
against silence, `fall` runs the dotted-8th cycle so it never resolves inside
the bar, and `sparse` is three held notes. Each has its own timbre and note
length too. The form is A A tres sparse A run tres MONTAGEM fall A+2 - the
hook states itself, three other themes take the middle, and it comes back a
tone up at the end.

Under that, `spice()` gives every bar its own ratchets, fill, hat pattern and
timbre from a seed derived from the bar number, so no two bars of the same
theme are stated identically either.
"""
import numpy as np
from driftlib import *

np.random.seed(1590)

# ---- the 8-bar cycle: Gm Gm Eb Ab | Gm Gm Eb F ----
ROOTS = [31, 31, 39, 32, 31, 31, 39, 29]                  # G1 G1 Eb2 Ab1 G1 G1 Eb2 F1
CHAD = {0: (43, 50, 55), 1: (43, 50, 55), 2: (39, 46, 55), 3: (44, 51, 56),
        4: (43, 50, 55), 5: (43, 50, 55), 6: (39, 46, 55), 7: (41, 48, 57)}
CHOIR = {0: (43, 50, 55, 62), 1: (43, 50, 55, 62), 2: (39, 46, 55, 58),
         3: (44, 51, 56, 63), 4: (43, 50, 55, 62), 5: (43, 50, 55, 62),
         6: (39, 46, 55, 58), 7: (41, 48, 57, 60)}

# Five themes, and what separates them is RHYTHM, not just notes. Alternating
# two melodies that both run straight 8ths is one melody with different
# pitches; the ear files it as the same thing. So: `hook` hammers 8ths,
# `fall` runs 8ths downward from the top, `tres` is a 3+3+2 with long notes,
# `run` is bursts of 16ths against silence, `sparse` is three held notes a
# bar. Each section gets one, and the hook returns at the end as the payoff.
THEMES = {
 'hook': [
  [(0,67),(2,67),(4,74),(6,67),(8,70),(10,67),(12,74),(14,72)],
  [(0,67),(2,67),(4,74),(6,67),(8,70),(10,74),(12,75),(14,74)],
  [(0,70),(2,70),(4,75),(6,70),(8,74),(10,70),(12,75),(14,74)],
  [(0,68),(2,68),(4,75),(6,68),(8,72),(10,68),(12,75),(14,74)],
  [(0,67),(2,67),(4,74),(6,67),(8,70),(10,67),(12,74),(14,72)],
  [(0,67),(2,67),(4,74),(6,67),(8,70),(10,74),(12,77),(14,75)],
  [(0,70),(2,70),(4,75),(6,70),(8,74),(10,75),(12,79),(14,77)],
  [(0,69),(2,69),(4,77),(6,74),(8,72),(10,69),(12,72),(14,65)]],
 'fall': [
  [(0,79),(3,75),(6,74),(9,70),(12,67),(15,70)],
  [(0,74),(3,70),(6,67),(9,70),(12,74),(15,75)],
  [(0,75),(3,74),(6,70),(9,75),(12,79),(15,75)],
  [(0,75),(3,72),(6,68),(9,72),(12,80),(15,75)],
  [(0,79),(3,75),(6,74),(9,70),(12,67),(15,70)],
  [(0,77),(3,74),(6,70),(9,74),(12,77),(15,79)],
  [(0,82),(3,79),(6,75),(9,74),(12,79),(15,75)],
  [(0,77),(3,74),(6,72),(9,69),(12,72),(15,74)]],
 'tres': [
  [(0,74),(3,72),(6,70),(8,67),(11,70),(14,74)],
  [(0,74),(3,75),(6,74),(8,70),(11,67),(14,70)],
  [(0,75),(3,74),(6,70),(8,75),(11,79),(14,75)],
  [(0,75),(3,72),(6,68),(8,72),(11,75),(14,80)],
  [(0,74),(3,72),(6,70),(8,67),(11,70),(14,74)],
  [(0,74),(3,75),(6,77),(8,75),(11,74),(14,70)],
  [(0,79),(3,77),(6,75),(8,74),(11,70),(14,75)],
  [(0,77),(3,74),(6,72),(8,69),(11,72),(14,65)]],
 'run': [
  [(0,67),(1,70),(2,74),(3,75),(4,74),(8,70),(10,67),(14,74)],
  [(0,67),(4,70),(8,74),(9,75),(10,77),(11,79),(12,77),(14,74)],
  [(0,70),(1,74),(2,75),(3,79),(4,75),(8,74),(12,70),(14,75)],
  [(0,68),(4,72),(8,75),(9,74),(10,72),(11,68),(12,72),(14,75)],
  [(0,67),(1,70),(2,74),(3,75),(4,74),(8,70),(10,67),(14,74)],
  [(0,74),(4,75),(8,77),(9,79),(10,77),(11,75),(12,74),(14,70)],
  [(0,75),(1,79),(2,82),(3,79),(4,75),(8,74),(12,75),(14,79)],
  [(0,77),(4,74),(8,72),(9,69),(10,72),(11,74),(12,72),(14,65)]],
 'sparse': [
  [(0,74),(6,70),(12,67)], [(0,74),(6,75),(12,74)],
  [(0,75),(6,74),(12,70)], [(0,75),(6,72),(12,68)],
  [(0,74),(6,70),(12,67)], [(0,70),(6,74),(12,77)],
  [(0,79),(6,75),(12,74)], [(0,77),(6,72),(12,69)]],
}

# Each theme also gets its own timbre and note length. Two melodies played on
# the same sound with the same envelope are one melody with different pitches.
THEME_TONE = {'hook':   ((7.6, 0.40, 0.34, 1.00), 1.00),
              'fall':   ((6.6, 0.28, 0.22, 1.14), 1.35),
              'tres':   ((8.2, 0.52, 0.42, 0.82), 1.60),
              'run':    ((6.2, 0.24, 0.16, 1.24), 0.62),
              'sparse': ((5.0, 0.18, 0.00, 0.72), 2.20)}

# Which theme plays where. This is the track's melodic form: the hook states
# itself, `fall` answers it, the breather thins to `sparse`, the two drops
# after the build bring genuinely new rhythms, and the hook returns a tone up.
def theme_of(b):
    for lo, hi, name in ((0, 16, 'hook'), (16, 24, 'tres'), (24, 32, 'sparse'),
                         (32, 40, 'hook'), (40, 48, 'run'), (48, 56, 'tres'),
                         (56, 64, 'hook'), (64, 72, 'fall'), (72, 84, 'hook')):
        if lo <= b < hi:
            return name
    return 'hook'

def theme_notes(b, name=None):
    """(step, note, gap) for the bar; gap = steps until the next note"""
    bar = THEMES[name or theme_of(b)][b % 8]
    return [(st, nt, (bar[i + 1][0] if i + 1 < len(bar) else 16) - st)
            for i, (st, nt) in enumerate(bar)]

# The metrical hierarchy of the bar, as levels. Beat 1 is strongest, beat 3
# next, then 2 and 4, then the offbeats. Eight even 8ths at one level is a
# wall; the same eight through this table is a groove.
WEIGHT = {0: 1.00, 1: 0.50, 2: 0.64, 3: 0.56, 4: 0.86, 5: 0.50, 6: 0.60, 7: 0.56,
          8: 0.94, 9: 0.50, 10: 0.64, 11: 0.56, 12: 0.84, 13: 0.50, 14: 0.60, 15: 0.56}

# Cowbell timbres, rotated so no eight-bar pass sounds like the last one.
TONES = [(7.4, 0.38, 0.34, 1.00), (8.0, 0.46, 0.28, 0.92), (6.8, 0.30, 0.42, 1.08),
         (7.8, 0.50, 0.22, 0.96), (7.2, 0.34, 0.38, 1.04), (8.4, 0.44, 0.30, 0.88)]

def spice(b):
    """Everything about a bar that does not have to stay the same. Seeded off
    the bar number, so it is reproducible and never lands on the same
    combination twice in a row."""
    r = np.random.RandomState(9000 + b * 13)
    return dict(
        tone=TONES[(b // 8 + b % 3) % len(TONES)],
        ratchets=tuple(r.choice([0, 2, 4, 6, 8, 10, 12, 14], size=r.randint(0, 3), replace=False)),
        fill=(b % 4 == 3) and FILLS[(b // 4) % len(FILLS)],
        hats=r.choice(['16', '16', '16', '8+', 'shuf']),
        kick_extra=tuple(r.choice([2, 6, 7, 10, 14], size=1)) if b % 4 == 2 else (),
        oct_layer=r.rand() < 0.75,
        throw=(b % 16 == 13),
    )

FILLS = ['roll32', 'stutter', 'roll48', 'kickrun', 'reverse', 'cut', 'climb', 'tom']

s = Session(84, tail=2.6)

# ---- the kit, memoised: a drum machine plays one recording of each hit ----
_HAT = {}
def hat_(tone, open_=False):
    key = (round(tone, 2), open_)
    if key not in _HAT:
        _HAT[key] = hat808(3.4 if open_ else 0.85, open_=open_, tone=tone)
    return _HAT[key]

_SNR = {}
def snr_(drive=3.0, bright=1.25, body=0.55):
    key = (drive, bright, body)
    if key not in _SNR:
        _SNR[key] = snare(3.0, drive=drive, bright=bright, body=body)
    return _SNR[key]

# ================= the parts =================
def cowbells(b, gain=1.0, decay=0.16, octave=0, half=False, pan=0.0, vowel=None,
             tone=None, ratchets=None, trans=0, name=None):
    """One bar of whichever theme this section plays, with a parameter lock
    per step and a timbre that rotates every eight bars. Note length comes
    from the gap to the next note, so a sparse theme rings and a run does
    not - that is most of what makes the themes sound different."""
    sp = spice(b)
    th = name or theme_of(b)
    base, dmul = THEME_TONE[th]
    drive, folded, tear, bright = tone or tuple(
        (x + y) / 2 for x, y in zip(base, sp['tone']))       # theme voice, still rotating
    decay = decay * dmul
    notes = theme_notes(b, name)
    rat = sp['ratchets'] if ratchets is None else ratchets
    for st, nt, gap in notes:
        if half and st >= 8:
            break
        w = WEIGHT[st]
        seg = cowbell(nt + octave + trans, min(gap * 1.15, 3.4), drive=drive,
                      decay=decay * (1.18 if w > 0.9 else 0.86) * (1.5 if gap >= 4 else 1.0),
                      folded=folded, bright=bright,
                      tear=tear * (1.0 if w > 0.9 else 0.7), vowel=vowel)
        s.place(s.pos(b, st), panned(seg, pan) if pan else seg, gain * w, 'music')
        if st in rat and gap >= 2:
            up = cowbell(nt + octave + trans, 1.0, drive=drive * 0.9, decay=decay * 0.4,
                         folded=folded, bright=bright * 1.05, tear=0.0)
            s.place(s.pos(b, st + 1), up, gain * 0.55, 'music')

def fill16(b, gain=0.13, note=55, drive=5.0, bright=0.55):
    """A dark cowbell tick on the offbeat 16ths - the steps the riff leaves
    empty. It never lands on a melody note, so it adds speed without mud."""
    rng = np.random.RandomState(700 + b)
    for st in range(1, 16, 2):
        seg = cowbell(note, 1.0, drive=drive, decay=0.05, folded=0.12,
                      bright=bright, tear=0.0, clang=0.25)
        s.place(s.pos(b, st), panned(seg, rng.uniform(-0.3, 0.3)), gain, 'music')

def bass(b, gain=1.0, style='roll', grind=3.4, growl=0.0, mid=1.0, offbeats=(2, 6, 10, 14),
         accent4=True, trans=0):
    """Eight sub events a bar, and a gap after every one of them.

    Read the low band of any montagem and it is never continuous: a note on
    the beat, its tail through the next 16th, then nothing until the next.
    That silence is what makes half a mix's energy sittable in the sub
    without turning into a drone - a sustained root at this level is a wall,
    and a wall has no pulse to jump to.

    The beat notes are NOT on the ducked bus. They are meant to fuse with the
    kick; ducked, they get dipped to a third exactly on the beat and bloom
    into the offbeat, which inverts the whole groove."""
    r = ROOTS[b % 8] + trans
    prev = ROOTS[(b - 1) % 8] + trans
    nxt = ROOTS[(b + 1) % 8] + trans
    into = prev if abs(prev - r) <= 3 and prev != r else r - 7
    if style == 'hold':
        s.place(s.pos(b, 0), slug(r, 17, slide_from=into, glide=0.08, decay=1.6,
                                  grind=grind * 0.8, growl=growl, mid=mid * 0.8), gain, 'bass')
        return
    for st in (0, 4, 8, 12):
        if st == 12 and accent4:
            continue
        s.place(s.pos(b, st), slug(r, 3.2, slide_from=into if st == 0 else None,
                                   glide=0.05, decay=0.20, grind=grind * 0.9,
                                   growl=growl, mid=mid * 0.85),
                gain * (1.0 if st == 0 else 0.88), 'roll')
    if accent4:
        hit = nxt if nxt != r else r - 4                   # the next chord, or the b6 below
        s.place(s.pos(b, 12), slug(hit, 3.6, slide_from=r, glide=0.04, decay=0.26,
                                   grind=grind, mid=mid), gain * 1.06, 'roll')
    for st in offbeats:
        if st % 4 == 0:
            continue
        nt = r + (12 if style == 'octave' and st % 8 == 6 else 0)
        s.place(s.pos(b, st), slug(nt, 2.0, decay=0.095, grind=grind, mid=mid,
                                   click=0.8), gain * 0.72, 'roll')
    if style == 'run':                                     # the chromatic climb home
        for k in range(6):
            s.place(s.pos(b, 10 + k), slug(nxt - 6 + k, 1.5, decay=0.07,
                                           grind=grind, mid=mid, click=0.6),
                    gain * (0.5 + 0.06 * k), 'roll')

HAT_PAT = {'16': range(16), '8+': [0, 2, 3, 4, 6, 8, 10, 11, 12, 14, 15],
           'shuf': [0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15]}

def drums(b, gain=1.0, kicks=(0, 4, 8, 12), claps=(4, 12), hat_gain=0.5,
          hat_steps=None, ohat=(2, 6, 10, 14), rolls=(), rims=(), snares=(), seed=0):
    sp = spice(b)
    rng = np.random.RandomState(4000 + b * 7 + seed)
    for st in tuple(kicks) + tuple(sp['kick_extra'] if kicks else ()):
        t = s.pos(b, st)
        s.hit(t)
        s.place(t, stomp(4, decay=0.19, gain=0.99 if st == 0 else 0.9),
                gain * (1.0 if st % 4 == 0 else 0.62), 'drums')
    for st in claps:
        s.place(s.pos(b, st), snr_(), gain * 0.72, 'drums')
    for st in snares:
        s.place(s.pos(b, st), snr_(3.2, 1.1, 1.0), gain * 0.9, 'drums')
    for st in rims:
        s.place(s.pos(b, st), panned(rim(1.2, gain=0.5), rng.uniform(-0.4, 0.4)), gain, 'drums')
    for st in ohat:
        s.place(s.pos(b, st), hat_(1.0, True), gain * hat_gain * 0.72, 'drums')
    steps_ = HAT_PAT[sp['hats']] if hat_steps is None else hat_steps
    for st in steps_:
        n_sub = dict(rolls).get(st, 1) if rolls else 1
        for k in range(n_sub):
            v = 1.0 if st % 4 == 0 else (0.66 if st % 2 == 0 else 0.5)
            v *= 1 - 0.12 * k
            seg = hat_(round(1 + rng.uniform(-0.09, 0.09), 2))
            s.place(s.pos(b, st + k / n_sub), panned(seg, rng.uniform(-0.32, 0.32)),
                    gain * hat_gain * v, 'drums')

def fill(b, gain=1.0, trans=0):
    """One bar-end event, a different one every four bars. Eight kinds, cycled
    so the same fill never comes round inside a section."""
    sp = spice(b)
    kind = sp['fill']
    if not kind:
        return
    r = ROOTS[b % 8] + trans
    rng = np.random.RandomState(500 + b)
    if kind == 'roll32':
        for k in range(8):
            s.place(s.pos(b, 12 + k * 0.5), snr_(3.0, 1.2, 0.4),
                    gain * (0.28 + 0.06 * k), 'drums')
    elif kind == 'roll48':
        for k in range(12):
            s.place(s.pos(b, 12 + k / 3), hat_(1.0 + 0.03 * k), gain * (0.25 + 0.04 * k), 'drums')
    elif kind == 'stutter':
        seg = cowbell(theme_notes(b)[-2][1] + trans, 1.0, drive=7.5, decay=0.06,
                      folded=0.4, tear=0.3)
        for k in range(6):
            s.place(s.pos(b, 13 + k * 0.5), panned(seg, 0.5 if k % 2 else -0.5),
                    gain * (0.7 - 0.06 * k), 'music')
    elif kind == 'kickrun':
        for k, st in enumerate((12, 13, 14, 14.5, 15, 15.5)):
            s.hit(s.pos(b, st))
            s.place(s.pos(b, st), stomp(3, decay=0.13, gain=0.85), gain * 0.8, 'drums')
    elif kind == 'reverse':
        s.place(s.pos(b, 12), reverse_crash(8, gain=0.8), gain, 'fx')
    elif kind == 'cut':
        s.place(s.pos(b, 14), zap(2, f0=1800, f1=90, gain=0.5), gain, 'fx')
    elif kind == 'climb':
        for k in range(6):
            s.place(s.pos(b, 10 + k), slug(r - 6 + k, 1.5, decay=0.07, click=0.6),
                    gain * (0.5 + 0.06 * k), 'roll')
    elif kind == 'tom':
        for k, nt in enumerate((55, 51, 48, 44)):
            s.place(s.pos(b, 12 + k), cowbell(nt + trans, 1.4, drive=5.0, decay=0.10,
                                              folded=0.3, bright=0.5, tear=0.0),
                    gain * (0.5 + 0.08 * k), 'music')

def brass(b, gain=1.0, steps_=(0,), dur=4.6, drive=6.0, oct_=0, trans=0):
    notes = tuple(n + oct_ + trans for n in CHAD[b % 8])
    for st in steps_:
        s.place(s.pos(b, st), chad(notes, dur, drive=drive), gain, 'music')

def choir(b, gain=1.0, dur=16, vowel='oh', oct_=0, trans=0):
    notes = tuple(n + oct_ + trans for n in CHOIR[b % 8])
    s.place(s.pos(b, 0), chant(notes, dur, vowel=vowel), gain, 'pad')

def counter(b, gain=0.26, oct_=0, trans=0):
    """The chord's top voice, high and sustained, on strong beats only.

    It states the harmonic hook and nothing else: G held for six bars, then
    Ab in bar 4, then A natural in bar 8 - the one slot the whole progression
    exists for. It deliberately does not follow the riff's rhythm.

    The first version of this put a bell on the last 16th of every beat
    playing the riff's own notes an octave up. That is a flam: the same pitch
    as the cowbell, 96 ms late, on the weakest position in the bar. It read
    as out of time because it was."""
    top = CHAD[b % 8][-1] + 24 + oct_ + trans
    hits = ((0, 7.0),) if b % 4 != 3 else ((0, 5.0), (8, 6.0))
    for st, dur in hits:
        seg = lp(bell(midi(top), dur, gain=1.0), 4000)
        s.place(s.pos(b, st), panned(seg, 0.3 if st == 0 else -0.3), gain, 'music')

def throw(b, step=14, trans=0):
    """A single cowbell hit sent to a climbing delay - the dub trick, and the
    cheapest way to make a repeating bar feel like it went somewhere."""
    sp = spice(b)
    seg = cowbell(theme_notes(b)[-1][1] + trans, 1.6, drive=7.0, decay=0.12,
                  folded=0.4, tear=0.35)
    for k in range(1, 5):
        e = pitched(seg, 2 ** ((k * 5) / 12))
        s.place(s.pos(b, step + k * 1.5), panned(e, 0.7 if k % 2 else -0.7),
                0.45 * 0.62 ** k, 'fx')

# ================= 0-3  the hook, cold =================
s.place(s.pos(0), crackle(16 * 84, gain=0.5), 1.0, 'fx')
s.place(s.pos(0), revs(16 * 3, gears=2, rpm0=32, rpm1=80, gain=0.30), 1.0, 'fx')
for b in range(4):
    cowbells(b, gain=0.92, decay=0.16, half=b == 0, ratchets=())
    if b >= 2:
        drums(b, claps=(), gain=0.85, hat_gain=0.34, hat_steps=range(0, 16, 2),
              ohat=(2, 6, 10, 14) if b == 3 else ())
s.place(s.pos(0, 0), grunt(43, 3.0, gain=0.5, drop=6.0), 1.0, 'fx')
s.place(s.pos(2, 0), turbo(16 * 2, gain=0.5), 1.0, 'fx')
s.place(s.pos(3, 8), reverse_crash(8, gain=0.7), 1.0, 'fx')

# ================= 4-7  the walk-in =================
for b in range(4, 8):
    cowbells(b, gain=0.98, decay=0.16)
    drums(b, gain=0.95, claps=(4, 12) if b >= 5 else (12,), hat_gain=0.44,
          hat_steps=range(16) if b >= 6 else range(0, 16, 2))
    if b >= 6:
        bass(b, gain=0.88, grind=2.8, mid=0.85)
    if b == 7:
        brass(b, gain=0.55)
    fill(b, gain=0.8)
s.place(s.pos(4), crash808(24, gain=0.6), 1.0, 'drums')
s.place(s.pos(6), riser(16 * 2, gain=0.75, f0=200, f1=900), 1.0, 'fx')
s.place(s.pos(7, 12), bass_drop(10, note=31, gain=0.42), 1.0, 'bass')

# ================= 8-23  DROP 1 (A then B) =================
for b in range(8, 24):
    ph = b - 8
    cowbells(b, gain=1.0, decay=0.16)
    if spice(b)['oct_layer']:
        cowbells(b, gain=0.30, decay=0.19, octave=-12, pan=-0.4, ratchets=(),
                 tone=(5.4, 0.2, 0.0, 0.7))
    bass(b, gain=0.96, style='run' if ph % 8 == 7 else 'roll', grind=3.2)
    drums(b, hat_gain=0.52, rims=(3, 11) if ph % 2 else ())
    brass(b, gain=0.54, steps_=(0,) if ph % 2 == 0 else (0, 10))
    fill(b)
    if spice(b)['throw']:
        throw(b)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.75), 1.0, 'drums')
    if b >= 16:
        choir(b, gain=0.30)
        counter(b, gain=0.22)
s.place(s.pos(11, 12), skid(6, gain=0.45), 1.0, 'fx')
s.place(s.pos(15, 12), grunt(41, 3.0, gain=0.55), 1.0, 'fx')
s.place(s.pos(19, 12), turbo(10, gain=0.4, f0=1100), 1.0, 'fx')
s.place(s.pos(23, 8), skid(8, gain=0.6, f0=1400), 1.0, 'fx')

# ================= 24-31  the breather =================
# The kick keeps walking - taking it away here would lose the room. What goes
# is everything else, so the drop has somewhere to come back from.
for b in range(24, 32):
    ph = b - 24
    cowbells(b, gain=0.60, decay=0.20, half=ph % 2 == 0, ratchets=(),
             tone=(5.2, 0.2, 0.0, 0.75))
    bass(b, gain=0.86, style='hold' if ph % 4 < 2 else 'roll', grind=2.4, mid=0.7)
    drums(b, gain=0.8, claps=(12,) if ph % 2 else (4, 12), hat_gain=0.34,
          hat_steps=range(0, 16, 2), ohat=(6, 14))
    choir(b, gain=0.55, vowel='oh' if ph % 4 < 2 else 'aw')
    if ph >= 4:
        counter(b, gain=0.30)
    if ph in (3, 7):
        brass(b, gain=0.48, steps_=(8,), dur=5.0, drive=5.0)
    if ph == 5:
        throw(b, step=8)
s.place(s.pos(24), grunt(38, 4.0, gain=0.7, drop=7.0), 1.0, 'fx')
s.place(s.pos(26), revs(16 * 3, gears=3, rpm0=34, rpm1=100, gain=0.34), 1.0, 'fx')
s.place(s.pos(27, 12), skid(10, gain=0.55), 1.0, 'fx')

# ================= 32-39  the build =================
for b in range(32, 40):
    ph = b - 32
    cowbells(b, gain=0.78 + 0.04 * ph, decay=0.15, octave=12 if ph >= 6 else 0,
             tone=(6.0 + 0.28 * ph, 0.25 + 0.03 * ph, 0.15 + 0.03 * ph, 0.8 + 0.06 * ph))
    if ph < 6:
        bass(b, gain=0.86 - 0.08 * ph, grind=2.6, mid=0.7,
             offbeats=(2, 6, 10, 14) if ph < 4 else (6, 14))
    sub = (1, 2, 2, 3, 3, 4, 6, 8)[ph]
    drums(b, gain=0.92, kicks=(0, 4, 8, 12) if ph < 6 else ((0, 8) if ph == 6 else (0,)),
          claps=(4, 12) if ph < 4 else ((12,) if ph < 6 else ()),
          ohat=(2, 6, 10, 14) if ph < 5 else (),
          hat_gain=0.34 + 0.05 * ph, hat_steps=range(0, 16, 2 if ph < 3 else 1),
          rolls={st: sub for st in range(0, 16, 2)} if ph >= 4 else ())
    choir(b, gain=0.5 + 0.06 * ph, vowel='ah' if ph >= 4 else 'oh')
    if ph >= 2:
        s.place(s.pos(b, 0), snr_(3.2, 1.1, 1.0), 0.5 + 0.06 * ph, 'drums')
s.place(s.pos(32), riser(16 * 7 + 12, gain=1.0, f0=170, f1=1600), 1.0, 'fx')
s.place(s.pos(35), turbo(16 * 4 + 12, gain=0.75), 1.0, 'fx')
s.place(s.pos(38), revs(16 * 1 + 12, gears=1, rpm0=72, rpm1=200, gain=0.5, grit=4.0), 1.0, 'fx')
s.place(s.pos(39, 8), reverse_crash(8, gain=0.9), 1.0, 'fx')
# steps 12-15 of bar 39: nothing. That gap is what makes bar 40 land.
s.place(s.pos(39, 14), bass_drop(10, note=31, gain=0.5), 1.0, 'bass')

# ================= 40-55  DROP 2 =================
for b in range(40, 56):
    ph = b - 40
    cowbells(b, gain=1.0, decay=0.16)
    cowbells(b, gain=0.36, decay=0.19, octave=-12, pan=-0.42, ratchets=(),
             tone=(5.6, 0.22, 0.0, 0.7))
    if ph >= 8 and theme_of(b) == 'run':
        fill16(b, gain=0.13)
        cowbells(b, gain=0.22, decay=0.12, octave=12, pan=0.45, ratchets=(),
                 vowel=('ah', 'ee'), tone=(6.4, 0.3, 0.2, 1.15))
    bass(b, gain=1.0, style='run' if ph % 8 == 7 else ('octave' if ph >= 8 else 'roll'),
         grind=3.8, growl=6.0 if ph % 8 >= 6 else 0.0)
    drums(b, hat_gain=0.56, rims=(3, 11) if ph % 4 >= 2 else ())
    brass(b, gain=0.68, steps_=(0,) if ph % 2 == 0 else (0, 10), drive=6.5)
    choir(b, gain=0.40 if ph < 8 else 0.52, vowel='oh' if ph % 8 < 4 else 'aw')
    counter(b, gain=0.26 if ph < 8 else 0.32)
    fill(b)
    if spice(b)['throw']:
        throw(b)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(22, gain=0.8), 1.0, 'drums')
s.place(s.pos(44, 12), grunt(41, 3.0, gain=0.6), 1.0, 'fx')
s.place(s.pos(47, 10), skid(10, gain=0.6, f0=1350), 1.0, 'fx')
s.place(s.pos(48), revs(16 * 4, gears=4, rpm0=42, rpm1=160, gain=0.30), 1.0, 'fx')
s.place(s.pos(52, 12), grunt(38, 3.0, gain=0.65), 1.0, 'fx')
s.place(s.pos(55, 12), skid(8, gain=0.7, f0=1500), 1.0, 'fx')

# ================= 56-63  MONTAGEM =================
# The reference texture, straight: kick on every beat, one enormous sub note
# behind each, nothing above 2 kHz, no melody. One chord for eight bars.
for b in range(56, 64):
    ph = b - 56
    r = 31
    for st in (0, 4, 8):
        s.place(s.pos(b, st), slug(r, 3.4, decay=0.24, grind=4.2, mid=0.9,
                                   click=0.9), 1.12, 'roll')
    hit = 27 if ph % 2 == 0 else 26                        # the b6, then the 5th below
    s.place(s.pos(b, 12), slug(hit, 4.0, slide_from=r, glide=0.05, decay=0.30,
                               grind=4.4, mid=1.0), 1.22, 'roll')
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), slug(r, 1.8, decay=0.075, grind=4.0, mid=1.0,
                                   click=0.8), 0.55, 'roll')
    drums(b, gain=1.0, claps=(12,), hat_gain=0.24,
          hat_steps=(2, 6, 10, 14) if ph % 2 else (6, 14), ohat=())
    # a chopped, filtered cowbell texture instead of the tune
    rng = np.random.RandomState(300 + b)
    for st in (0, 3, 6, 8, 11, 14):
        nt = (55, 58, 51, 55, 62, 51)[(st + ph) % 6]
        s.place(s.pos(b, st), panned(cowbell(nt, 1.6, drive=5.6, decay=0.09,
                                             folded=0.5, bright=0.42, tear=0.0),
                                     rng.uniform(-0.3, 0.3)), 0.34, 'music')
    if ph == 7:                                            # the chromatic climb out
        for k in range(8):
            s.place(s.pos(b, 8 + k), slug(24 + k, 1.6, decay=0.07, grind=4.0, click=0.7),
                    0.45 + 0.06 * k, 'roll')
    if ph == 0:
        s.place(s.pos(b), impact(24, gain=0.34), 1.0, 'fx')
s.place(s.pos(58), grunt(36, 5.0, gain=0.7, drop=8.0), 1.0, 'fx')
s.place(s.pos(60), revs(16 * 3, gears=3, rpm0=40, rpm1=140, gain=0.42, grit=3.6), 1.0, 'fx')
s.place(s.pos(62), riser(16 * 2, gain=0.8, f0=220, f1=1700), 1.0, 'fx')

# ================= 64-79  DROP 3, and the last eight up a tone =================
for b in range(64, 80):
    ph = b - 64
    tr = 2 if ph >= 8 else 0                               # the lift, once, at the end
    cowbells(b, gain=1.0, decay=0.16, trans=tr)
    cowbells(b, gain=0.40, decay=0.20, octave=-12, pan=-0.45, ratchets=(), trans=tr,
             tone=(5.8, 0.24, 0.0, 0.7))
    cowbells(b, gain=0.22, decay=0.11, octave=12, pan=0.48, ratchets=(), trans=tr,
             vowel=('ah', 'ee'), tone=(6.6, 0.3, 0.22, 1.2))
    if theme_of(b) == 'hook':
        fill16(b, gain=0.15, note=55 + tr)
    bass(b, gain=1.0, style='run' if ph % 8 == 7 else 'octave', grind=4.0,
         growl=8.0 if ph % 4 == 3 else 0.0, trans=tr)
    drums(b, hat_gain=0.6, rims=(3, 11))
    choir(b, gain=0.55, vowel='ah' if ph % 4 >= 2 else 'oh', trans=tr)
    counter(b, gain=0.30, trans=tr)
    fill(b, trans=tr)
    if ph >= 8:
        # the brass doubles the riff two octaves down: cowbell and brass in unison
        for st, nt, gap in theme_notes(b):
            if st % 4 == 0:
                s.place(s.pos(b, st), chad((nt - 24 + tr, nt - 12 + tr), 3.4,
                                           drive=6.8, scoop=1.8), 0.46, 'music')
        brass(b, gain=0.5, dur=4.0, drive=7.0, trans=tr)
    else:
        brass(b, gain=0.74, steps_=(0, 10), drive=7.0)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(24, gain=0.9), 1.0, 'drums')
s.place(s.pos(68, 12), grunt(41, 3.0, gain=0.7), 1.0, 'fx')
s.place(s.pos(71, 8), skid(10, gain=0.7, f0=1500), 1.0, 'fx')
s.place(s.pos(72), turbo(16 * 2, gain=0.5), 1.0, 'fx')
s.place(s.pos(76), revs(16 * 3, gears=4, rpm0=50, rpm1=170, gain=0.34), 1.0, 'fx')
s.place(s.pos(75, 12), grunt(38, 4.0, gain=0.8, drop=9.0), 1.0, 'fx')
s.place(s.pos(79, 8), skid(12, gain=0.8, f0=1650), 1.0, 'fx')

# ================= 80-83  out =================
for b in (80, 81):
    cowbells(b, gain=0.85 - 0.2 * (b - 80), decay=0.16, trans=2)
    bass(b, gain=0.82, grind=2.6, mid=0.7, trans=2)
    drums(b, gain=0.82, hat_gain=0.36, hat_steps=range(0, 16, 2))
    choir(b, gain=0.45, trans=2)
s.place(s.pos(82), tape_stop(np.concatenate(
    [cowbell(n, 2.0, drive=6.0, tear=0.25) for n in (69, 72, 76, 77, 76, 72, 69)]), 1.35),
    0.75, 'music')
s.place(s.pos(82), revs(16 * 2, gears=1, rpm0=130, rpm1=32, gain=0.5, dip=1.0), 1.0, 'fx')
s.place(s.pos(82), downlifter(16, gain=0.8), 1.0, 'fx')
s.place(s.pos(83, 8), grunt(33, 6.0, gain=0.5, drop=4.0), 1.0, 'fx')

# ---- bus treatment ----
s.bus['music'] = reverb(s.bus['music'], decay=0.9, wet=0.09, tone=6000)[:s.total]
s.bus['pad'] = reverb(s.bus['pad'], decay=2.4, wet=0.32, tone=4200)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=2.0, wet=0.26, tone=5200)[:s.total]
s.bus['drums'] = shelf(softclip(wow(s.bus['drums'], depth_ms=0.28, rate=0.45), 1.3),
                       6000, -7.0)
s.bus['music'] = dirty(shelf(shelf(s.bus['music'], 5800, -7.0), 3000, +1.5), 1.28)
# The references put their weight at 60-120 Hz, not under 60 - that is audible
# weight rather than only felt weight, and it is what a phone reproduces.
for nm in ('bass', 'roll'):
    s.bus[nm] = mono_below(shelf(dirty(s.bus[nm], 1.1), 70, +2.5), 150)
s.bus['pad'] = mono_below(lp(s.bus['pad'], 5200), 250)
s.bus['fx'] = shelf(softclip(s.bus['fx'], 0.85), 6000, -6.0)
# A short-window limiter per bus catches the tips where they are made, so the
# master clipper does not have to shave 4% of the record to reach a level.
# Peaks are shaved where they are made. A softclip leaves everything under
# knee*ceiling untouched and curves only the tips, so the bar-scale envelope -
# the thing the whole groove is - survives, and the master clipper is not
# asked to shave 4% of the record to reach a level.
for nm, ceil in (('drums', 0.56), ('roll', 0.60), ('bass', 0.60), ('music', 0.42), ('fx', 0.32)):
    s.bus[nm] = softclip(s.bus[nm], ceil, knee=0.7)

GAINS = {'drums': 1.18, 'bass': 0.92, 'roll': 0.92, 'music': 0.94, 'pad': 0.34, 'fx': 0.40}
s.report(GAINS)
# No master tanh: every bus is saturated where it should be, and a wide tanh
# across the sum lifts each tail about 2 dB toward the peaks - the one process
# that can flatten a grid that was programmed correctly.
s.render('phonk_montage_156.wav', drive=0, duck=0.30, limit=0.80, peak=0.995,
         fade=0.9, gains=GAINS, clip=1.46)
