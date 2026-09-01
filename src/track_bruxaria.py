"""BRUXARIA - Brazilian bruxaria funk at 164 BPM, C minor with a Phrygian bII.

The companion to CLASSIC MONTAGE and deliberately not the same record: that
one is cowbell-led phonk house with the bass answering on offbeat 8ths. This
one is led by a chopped voice, its percussion melody is a tuned hand drum,
and its 808 runs a tresillo *against* a four-to-the-floor kick instead of
alternating with it.

    hook | kick in | DROP 1 | breather | build | DROP 2 | MONTAGEM | DROP 3

Everything the references taught, applied from the start rather than fixed
afterwards:

* The low end carries the record - roots sit at 49-69 Hz so the weight lands
  at 60-120, which is audible weight and survives a phone, not only felt
  weight under 60.
* The sub has gaps. A note, its tail through the next 16th, then silence.
* Beat 4 moves: the accent anticipates the next bar's root, and every eighth
  bar ends on a chromatic climb.
* Nothing above 6 kHz to speak of.
* No master tanh - a wide tanh across the sum lifts every tail toward the
  peaks and is the one process that flattens a grid that was programmed
  correctly. Peaks are shaved at the buses instead.
* The beat notes are not on the ducked bus: they are meant to fuse with the
  kick, and ducking them inverts the groove.
* Four themes, separated by rhythm rather than by pitch - two melodies that
  both run straight 8ths are one melody, whatever notes they use.
"""
import numpy as np
from bruxarialib import *

np.random.seed(1964)

# ---- the 8-bar cycle: Cm Cm bVI bVII | Cm Cm bVI bII ----
ROOTS = [36, 36, 32, 34, 36, 36, 32, 37]          # C2 C2 Ab1 Bb1 C2 C2 Ab1 Db2
TRIAD = {0: (48, 51, 55), 1: (48, 51, 55), 2: (44, 48, 51), 3: (46, 50, 53),
         4: (48, 51, 55), 5: (48, 51, 55), 6: (44, 48, 51), 7: (49, 53, 56)}

# Four themes for the chopped voice. What separates them is rhythm and note
# length: `call` is a 3+3+2, `roll` is bursts of 16ths against silence, `wide`
# is two held chops a bar, `answer` is three, all off the beat.
THEMES = {
 'call': [
  [(0,72),(3,75),(6,79),(8,75),(11,72),(14,70)],
  [(0,72),(3,75),(6,79),(8,82),(11,79),(14,75)],
  [(0,80),(3,79),(6,75),(8,72),(11,75),(14,80)],
  [(0,82),(3,79),(6,77),(8,74),(11,70),(14,74)],
  [(0,72),(3,75),(6,79),(8,75),(11,72),(14,70)],
  [(0,72),(3,75),(6,79),(8,84),(11,82),(14,79)],
  [(0,80),(3,84),(6,80),(8,79),(11,75),(14,72)],
  [(0,73),(3,77),(6,80),(8,77),(11,73),(14,72)]],
 'roll': [
  [(0,72),(1,75),(2,79),(3,82),(4,79),(8,75),(10,72),(14,79)],
  [(0,72),(4,75),(8,79),(9,82),(10,84),(11,82),(12,79),(14,75)],
  [(0,80),(1,79),(2,75),(3,72),(6,75),(8,80),(12,84),(14,80)],
  [(0,82),(4,79),(8,77),(9,74),(10,77),(11,79),(12,82),(14,86)],
  [(0,72),(1,75),(2,79),(3,82),(4,79),(8,75),(10,72),(14,79)],
  [(0,72),(1,75),(2,79),(3,82),(4,84),(8,82),(10,79),(14,75)],
  [(0,80),(4,84),(8,86),(9,84),(10,80),(11,79),(12,75),(14,80)],
  [(0,73),(1,77),(2,80),(3,85),(4,80),(8,77),(12,73),(14,72)]],
 'wide': [
  [(0,79),(8,75)], [(0,79),(8,82)], [(0,80),(8,75)], [(0,82),(8,77)],
  [(0,79),(8,75)], [(0,82),(8,84)], [(0,80),(8,84)], [(0,77),(8,73)]],
 'answer': [
  [(2,75),(6,72),(11,79)], [(2,75),(6,79),(11,75)],
  [(2,80),(6,75),(11,72)], [(2,82),(6,77),(11,74)],
  [(2,75),(6,72),(11,79)], [(2,79),(6,82),(11,84)],
  [(2,84),(6,80),(11,75)], [(2,77),(6,73),(11,72)]],
}
# Each theme gets its own vowel, drive and note length. The vowel is what a
# listener hears as "a different sample", and it costs nothing.
THEME_VOICE = {'call':   ('ah', 0.35, 1.00, 2.2),
               'roll':   ('ee', 0.45, 0.55, 2.6),
               'wide':   ('oh', 0.20, 2.40, 1.7),
               'answer': ('aw', 0.30, 1.60, 2.0)}

def theme_of(b):
    for lo, hi, nm in ((0, 20, 'call'), (20, 28, 'wide'), (28, 36, 'call'),
                       (36, 44, 'roll'), (44, 52, 'answer'), (52, 60, 'call'),
                       (60, 72, 'call')):
        if lo <= b < hi:
            return nm
    return 'call'

def theme_notes(b, name=None):
    bar = THEMES[name or theme_of(b)][b % 8]
    return [(st, nt, (bar[i + 1][0] if i + 1 < len(bar) else 16) - st)
            for i, (st, nt) in enumerate(bar)]

WEIGHT = {0: 1.00, 1: 0.52, 2: 0.66, 3: 0.62, 4: 0.86, 5: 0.52, 6: 0.64, 7: 0.58,
          8: 0.94, 9: 0.52, 10: 0.66, 11: 0.62, 12: 0.84, 13: 0.52, 14: 0.64, 15: 0.58}

def spice(b):
    """Everything about a bar that does not have to stay the same, seeded off
    the bar number so no combination lands twice in a row."""
    r = np.random.RandomState(6100 + b * 17)
    return dict(
        drumline=r.randint(0, 4),
        ghosts=tuple(r.choice([1, 5, 7, 9, 13, 15], size=r.randint(1, 4), replace=False)),
        whistle=(b % 16 == 11),
        seco_hits=tuple(r.choice([2, 6, 10, 14], size=r.randint(0, 3), replace=False)),
        crush=r.choice([0.30, 0.38, 0.46]),
    )

# The tamborzão: a tuned hand-drum line. Four of them, rotated per bar, all
# built on the same 3+3+2 skeleton so the groove holds while the detail moves.
DRUMLINES = [
    [(0, 52, 1.0), (3, 52, .7), (6, 59, .8), (8, 52, .9), (11, 57, .7), (14, 52, .8)],
    [(0, 52, 1.0), (3, 57, .7), (6, 52, .8), (8, 59, .9), (10, 57, .6), (11, 52, .7), (14, 54, .8)],
    [(0, 52, 1.0), (2, 52, .6), (3, 59, .7), (6, 52, .8), (8, 52, .9), (11, 59, .7), (13, 57, .6), (14, 52, .7)],
    [(0, 52, 1.0), (3, 52, .7), (6, 57, .8), (8, 52, .9), (11, 52, .7), (12, 59, .6), (14, 64, .8)],
]

s = Session(72, tail=2.2)

_ATB, _SEC, _HAT = {}, {}, {}
def atb_(note, decay=0.15, wood=1.0):
    k = (note, decay, wood)
    if k not in _ATB:
        _ATB[k] = atabaque(note, 2.4, decay=decay, wood=wood)
    return _ATB[k]

def hat_(tone):
    if tone not in _HAT:
        _HAT[tone] = hat808(0.8, tone=tone)
    return _HAT[tone]

_SNR = {}
def clap_(bright=1.35, body=0.30):
    k = (bright, body)
    if k not in _SNR:
        _SNR[k] = snare(2.8, drive=3.4, bright=bright, body=body)
    return _SNR[k]

# ================= the parts =================
def chops(b, gain=1.0, octave=0, pan=0.0, trans=0, name=None, half=False):
    """One bar of whichever theme this section plays. Note length comes from
    the gap to the next note, so `wide` rings and `roll` does not."""
    th = name or theme_of(b)
    vowel, grit, dmul, drive = THEME_VOICE[th]
    sp = spice(b)
    for st, nt, gap in theme_notes(b, name):
        if half and st >= 8:
            break
        seg = chopvoice(nt + octave + trans, min(gap * 1.05 * dmul, 6.0),
                        vowel=vowel, grit=sp['crush'] if grit > 0.25 else grit,
                        drive=drive, bright=1.0 if st % 4 == 0 else 0.9)
        p = pan if pan else (0.14 if st % 4 == 2 else -0.10 if st % 4 == 3 else 0.0)
        s.place(s.pos(b, st), panned(seg, p) if p else seg, gain * WEIGHT[st], 'music')

def tambor(b, gain=1.0, line=None, ghosts=True, wood=1.0, trans=0):
    """The percussion melody: a tuned hand drum on the 3+3+2, with ghost hits
    on the 16ths between."""
    sp = spice(b)
    rng = np.random.RandomState(2200 + b)
    for st, nt, v in DRUMLINES[sp['drumline'] if line is None else line]:
        s.place(s.pos(b, st), panned(atb_(nt + trans, 0.15, wood), rng.uniform(-0.40, 0.40)),
                gain * v, 'perc')
    if ghosts:
        for st in sp['ghosts']:
            s.place(s.pos(b, st), panned(atb_(52 + trans, 0.055, wood * 0.8),
                                         rng.uniform(-0.6, 0.6)), gain * 0.30, 'perc')

def bass(b, gain=1.0, style='tres', grind=3.6, mid=1.0, trans=0):
    """The 808 runs a tresillo against a kick that does not.

    Steps 0 and 8 land with the kick and fuse with it; 3, 6, 11 and 14 fall in
    its gaps. Step 14 carries the accent and anticipates the next bar's root,
    which is why the bar points forward instead of just repeating."""
    r = ROOTS[b % 8] + trans
    nxt = ROOTS[(b + 1) % 8] + trans
    prev = ROOTS[(b - 1) % 8] + trans
    into = prev if abs(prev - r) <= 4 and prev != r else r - 7
    if style == 'hold':
        s.place(s.pos(b, 0), slug(r, 17, slide_from=into, glide=0.08, decay=1.5,
                                  grind=grind * 0.8, mid=mid * 0.8), gain, 'bass')
        return
    big = ((0, 0.22, 1.00), (8, 0.20, 0.94)) if style == 'tres' else ((0, 0.22, 1.0),)
    for st, dec, g in big:
        s.place(s.pos(b, st), slug(r, 3.4, slide_from=into if st == 0 else None,
                                   glide=0.05, decay=dec, grind=grind, mid=mid,
                                   suboct=0.45), gain * g, 'roll')
    for st in (3, 6, 11):
        s.place(s.pos(b, st), slug(r, 2.2, decay=0.10, grind=grind, mid=mid,
                                   click=0.8), gain * 0.74, 'roll')
    for st in (4, 12):
        s.place(s.pos(b, st), slug(r, 1.8, decay=0.075, grind=grind, mid=mid * 0.7,
                                   click=0.5), gain * 0.60, 'roll')
    hit = nxt if nxt != r else r - 4                   # anticipate, or drop to the b6
    s.place(s.pos(b, 14), slug(hit, 3.0, slide_from=r, glide=0.04, decay=0.24,
                               grind=grind, mid=mid, suboct=0.5), gain * 1.02, 'roll')
    if style == 'climb':                               # the chromatic way home
        for k in range(6):
            s.place(s.pos(b, 9 + k), slug(nxt - 6 + k, 1.4, decay=0.065,
                                          grind=grind, mid=mid, click=0.6),
                    gain * (0.48 + 0.06 * k), 'roll')

def drums(b, gain=1.0, kicks=(0, 4, 8, 12), claps=(4, 12), hats=True,
          hat_gain=0.34, hat_steps=None, rolls=(), secos=None):
    sp = spice(b)
    rng = np.random.RandomState(3300 + b * 5)
    for st in kicks:
        t = s.pos(b, st)
        s.hit(t)
        s.place(t, stomp(4, tune=65.4, decay=0.155, drive=3.4,
                         gain=0.99 if st == 0 else 0.93), gain, 'drums')
    for st in claps:
        s.place(s.pos(b, st), clap_(), gain * 0.78, 'drums')
    for st in (sp['seco_hits'] if secos is None else secos):
        s.place(s.pos(b, st), panned(seco(), rng.uniform(-0.35, 0.35)), gain * 0.42, 'perc')
    if not hats:
        return
    for st in (range(0, 16, 2) if hat_steps is None else hat_steps):
        n_sub = dict(rolls).get(st, 1) if rolls else 1
        for k in range(n_sub):
            v = (1.0 if st % 4 == 0 else 0.6) * (1 - 0.12 * k)
            s.place(s.pos(b, st + k / n_sub),
                    panned(hat_(round(1 + rng.uniform(-0.08, 0.08), 2)), rng.uniform(-0.3, 0.3)),
                    gain * hat_gain * v, 'drums')

def stabs(b, gain=1.0, steps_=(0,), trans=0):
    """A dry organ-ish triad on the downbeat - the harmony stated once a bar
    and then out of the way."""
    notes = [midi(n + trans) for n in TRIAD[b % 8]]
    for st in steps_:
        s.place(s.pos(b, st), lp(clav(notes, 3.0), 2600), gain, 'music')

def whistle(b, step=12, gain=0.5):
    s.place(s.pos(b, step), tuim(6.0, gain=gain), 1.0, 'fx')

# ================= 0-3  the hook, cold =================
s.place(s.pos(0), crackle(16 * 72, gain=0.40), 1.0, 'fx')
for b in range(4):
    chops(b, gain=0.95, half=b == 0)
    tambor(b, gain=0.7 + 0.1 * b, ghosts=b >= 2)
    if b >= 2:
        drums(b, kicks=(0, 4, 8, 12), claps=(), gain=0.8, hat_gain=0.22, secos=())
whistle(1, 12, 0.45)
s.place(s.pos(3, 8), reverse_crash(8, gain=0.6), 1.0, 'fx')

# ================= 4-7  the kick walks in =================
for b in range(4, 8):
    chops(b, gain=1.0)
    tambor(b, gain=0.9)
    drums(b, gain=0.95, claps=(12,) if b < 6 else (4, 12), hat_gain=0.30)
    if b >= 6:
        bass(b, gain=0.9, grind=3.0, mid=0.85)
    if b == 7:
        stabs(b, gain=0.45)
s.place(s.pos(4), crash808(20, gain=0.5), 1.0, 'drums')
s.place(s.pos(6), riser(16 * 2, gain=0.6, f0=210, f1=900), 1.0, 'fx')
s.place(s.pos(7, 12), bass_drop(9, note=36, gain=0.40), 1.0, 'bass')

# ================= 8-19  DROP 1 =================
for b in range(8, 20):
    ph = b - 8
    chops(b, gain=1.0)
    chops(b, gain=0.26, octave=-12, pan=-0.4)
    tambor(b, gain=1.0)
    bass(b, gain=1.0, style='climb' if ph % 8 == 7 else 'tres', grind=3.6)
    drums(b, hat_gain=0.34, rolls={14: 3} if ph % 4 == 3 else ())
    stabs(b, gain=0.42, steps_=(0,) if ph % 2 == 0 else (0, 11))
    if spice(b)['whistle']:
        whistle(b, 12, 0.42)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(18, gain=0.6), 1.0, 'drums')
s.place(s.pos(15, 12), tuim(8.0, gain=0.5, f0=4200, f1=1200), 1.0, 'fx')

# ================= 20-27  the breather =================
# The kick keeps walking. What leaves is the chop's density and the tamborzão's
# ghosts, so the drop has somewhere to come back from.
for b in range(20, 28):
    ph = b - 20
    chops(b, gain=0.68)
    tambor(b, gain=0.62, line=0, ghosts=False, wood=0.7)
    bass(b, gain=0.9, style='hold' if ph % 4 < 2 else 'tres', grind=2.6, mid=0.7)
    drums(b, gain=0.82, claps=(12,) if ph % 2 else (4, 12), hat_gain=0.24,
          hat_steps=range(0, 16, 4), secos=())
    stabs(b, gain=0.55, steps_=(0, 8))
    if ph == 5:
        whistle(b, 8, 0.5)
s.place(s.pos(24), grunt(41, 4.0, gain=0.55, drop=7.0), 1.0, 'fx')

# ================= 28-35  the build =================
for b in range(28, 36):
    ph = b - 28
    chops(b, gain=0.80 + 0.03 * ph, octave=12 if ph >= 6 else 0)
    tambor(b, gain=0.85 + 0.03 * ph, wood=0.9 + 0.05 * ph)
    if ph < 6:
        bass(b, gain=0.88 - 0.09 * ph, grind=2.8, mid=0.7)
    sub = (1, 2, 2, 3, 4, 4, 6, 8)[ph]
    drums(b, gain=0.92, kicks=(0, 4, 8, 12) if ph < 6 else ((0, 8) if ph == 6 else (0,)),
          claps=(4, 12) if ph < 4 else ((12,) if ph < 6 else ()),
          hat_gain=0.26 + 0.04 * ph, hat_steps=range(0, 16, 2 if ph < 4 else 1),
          rolls={st: sub for st in range(0, 16, 2)} if ph >= 4 else (), secos=())
    stabs(b, gain=0.5 + 0.04 * ph, steps_=(0, 8))
    if ph >= 3:
        s.place(s.pos(b, 0), clap_(1.2, 0.9), 0.5 + 0.05 * ph, 'drums')
s.place(s.pos(28), riser(16 * 7 + 12, gain=0.9, f0=180, f1=1500), 1.0, 'fx')
s.place(s.pos(33), tuim(16 * 2 + 12, gain=0.55, f0=1200, f1=5200, fall=3.0), 1.0, 'fx')
s.place(s.pos(35, 8), reverse_crash(8, gain=0.8), 1.0, 'fx')
# steps 12-15 of bar 35: nothing.
s.place(s.pos(35, 14), bass_drop(9, note=36, gain=0.48), 1.0, 'bass')

# ================= 36-51  DROP 2 =================
for b in range(36, 52):
    ph = b - 36
    chops(b, gain=1.0)
    chops(b, gain=0.28, octave=-12, pan=-0.42)
    if ph >= 8:
        chops(b, gain=0.20, octave=12, pan=0.46, name='answer')
    tambor(b, gain=1.05)
    bass(b, gain=1.0, style='climb' if ph % 8 == 7 else 'tres', grind=4.0,
         mid=1.0 if ph < 8 else 1.1)
    drums(b, hat_gain=0.36, rolls={14: 3, 15: 2} if ph % 4 == 3 else
          ({12: 2} if ph % 4 == 1 else ()))
    stabs(b, gain=0.48, steps_=(0,) if ph % 2 == 0 else (0, 11))
    if spice(b)['whistle']:
        whistle(b, 12, 0.45)
    if ph % 8 == 0:
        s.place(s.pos(b), crash808(20, gain=0.62), 1.0, 'drums')
s.place(s.pos(43, 12), grunt(38, 3.0, gain=0.5), 1.0, 'fx')
s.place(s.pos(51, 12), tuim(8.0, gain=0.55, f0=4600, f1=1300), 1.0, 'fx')

# ================= 52-59  MONTAGEM =================
# One chord, eight bars, no melody. Kick on every beat with an enormous sub
# behind it and dry knocks in the gaps - the reference texture, straight.
for b in range(52, 60):
    ph = b - 52
    r = 36
    for st, dec, g in ((0, 0.26, 1.14), (4, 0.22, 1.00), (8, 0.24, 1.08)):
        s.place(s.pos(b, st), slug(r, 3.6, decay=dec, grind=4.4, mid=0.95, click=0.9,
                                   suboct=0.55), g, 'roll')
    hit = 32 if ph % 2 == 0 else 31                    # the b6, then the 5th below
    s.place(s.pos(b, 12), slug(hit, 4.2, slide_from=r, glide=0.05, decay=0.30,
                               grind=4.6, mid=1.0, suboct=0.6), 1.24, 'roll')
    for st in (3, 6, 11, 14):
        s.place(s.pos(b, st), slug(r, 1.8, decay=0.075, grind=4.2, mid=1.0, click=0.8),
                0.52, 'roll')
    drums(b, gain=1.0, claps=(12,), hat_gain=0.16,
          hat_steps=(2, 6, 10, 14) if ph % 2 else (6, 14), secos=(2, 6, 10, 14))
    tambor(b, gain=0.55, line=ph % 4, ghosts=False, wood=0.55)
    if ph == 7:
        for k in range(8):
            s.place(s.pos(b, 8 + k), slug(29 + k, 1.5, decay=0.065, grind=4.2, click=0.7),
                    0.44 + 0.06 * k, 'roll')
    if ph == 0:
        s.place(s.pos(b), impact(20, gain=0.30), 1.0, 'fx')
s.place(s.pos(54), grunt(36, 5.0, gain=0.6, drop=8.0), 1.0, 'fx')
s.place(s.pos(58), riser(16 * 2, gain=0.75, f0=230, f1=1700), 1.0, 'fx')

# ================= 60-71  DROP 3, the last six a tone up =================
for b in range(60, 72):
    ph = b - 60
    tr = 2 if ph >= 6 else 0
    chops(b, gain=1.0, trans=tr)
    chops(b, gain=0.30, octave=-12, pan=-0.45, trans=tr)
    chops(b, gain=0.20, octave=12, pan=0.48, trans=tr, name='answer')
    tambor(b, gain=1.1, trans=tr)
    bass(b, gain=1.0, style='climb' if ph % 8 == 7 else 'tres', grind=4.2,
         mid=1.1, trans=tr)
    drums(b, hat_gain=0.38, rolls={14: 4, 15: 3} if ph % 4 == 3 else
          ({12: 2, 13: 2} if ph % 2 else ()))
    stabs(b, gain=0.52, steps_=(0, 8), trans=tr)
    if ph in (0, 6):
        s.place(s.pos(b), crash808(20, gain=0.7), 1.0, 'drums')
    if ph == 3 or ph == 9:
        whistle(b, 12, 0.5)
s.place(s.pos(65, 12), grunt(36, 4.0, gain=0.6, drop=9.0), 1.0, 'fx')
s.place(s.pos(71, 8), tuim(10.0, gain=0.6, f0=5000, f1=1100), 1.0, 'fx')
s.place(s.pos(71, 12), tape_stop(np.concatenate(
    [chopvoice(n, 2.0, vowel='ah') for n in (72, 75, 79, 82)]), 0.8), 0.6, 'music')

# ---- bus treatment ----
s.bus['music'] = reverb(s.bus['music'], decay=0.8, wet=0.08, tone=5200)[:s.total]
s.bus['perc'] = reverb(s.bus['perc'], decay=1.0, wet=0.10, tone=4200)[:s.total]
s.bus['fx'] = reverb(s.bus['fx'], decay=1.8, wet=0.24, tone=4600)[:s.total]
s.bus['drums'] = shelf(softclip(s.bus['drums'], 1.25), 5200, -9.0)
s.bus['music'] = dirty(shelf(s.bus['music'], 4600, -9.0), 1.22)
s.bus['perc'] = notch(hp(shelf(dirty(s.bus['perc'], 1.15), 5000, -8.0), 150),
                      215, width=0.40, depth=0.45)
for nm in ('bass', 'roll'):
    s.bus[nm] = mono_below(shelf(dirty(s.bus[nm], 1.1), 70, +2.5), 150)
s.bus['fx'] = shelf(softclip(s.bus['fx'], 0.8), 5200, -8.0)
# Peaks shaved where they are made, so the master clipper does not have to
# shave the record to reach a level.
for nm in ('drums', 'perc', 'fx', 'music'):
    s.bus[nm] = lp(s.bus[nm], 11500)
for nm, ceil in (('drums', 0.56), ('roll', 0.60), ('bass', 0.60),
                 ('music', 0.42), ('perc', 0.40), ('fx', 0.30)):
    s.bus[nm] = softclip(s.bus[nm], ceil, knee=0.7)

GAINS = {'drums': 1.15, 'bass': 0.90, 'roll': 0.92, 'music': 0.80, 'perc': 0.72, 'fx': 0.34}
s.report(GAINS)
s.render('bruxaria_164.wav', drive=0, duck=0.32, limit=0.80, peak=0.995,
         fade=0.8, gains=GAINS, clip=1.37)
