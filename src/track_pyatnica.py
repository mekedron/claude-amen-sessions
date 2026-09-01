"""Pyatnica (~4:34, 128 bars @112) - boogie funk, E dorian, no vocals.

1983, the Friday in the title, and the moment disco turned into boogie: the
kick is still on every beat but everything above it has stopped being polite.

Nothing here is borrowed from another genre. Every voice was built for this
record in `funklib`, because the job each one does is specific to it:

  slapbar    the lead instrument. One string, rendered a bar at a time, with
             the fret rattle mixed against the note by peak rather than by
             taste - a slap whose click is buried is a synth bass
  envfilter  the same bass through a Mu-Tron: the filter answers the hand
  organ      nine sine drawbars, no filter anywhere, through a Leslie whose
             two rotors change speed at different rates
  saxline    a tenor - one air column, a fixed 800 Hz body, and the growl
  suitcase   a Rhodes, where velocity moves the timbre and not the volume
  clavi      a hammer throwing a string at a fret, into a wah pedal
  talkbox    a synth up a tube into a mouth
  vocoder    sixteen bands of a chord, opened and closed by written vowels
  brass      four players who arrive a few milliseconds apart and out of tune
  the kit    a 1982 machine: 8-bit samples, and the snare's reverb gated

The harmony is two chords for most of the record - Em9 and A13, the Dorian
vamp - and the movement comes from rhythm, which is how this music works.
The chorus is the one place it goes anywhere: Cmaj9 - D9 - Bm7 - Em9,
landing home on the tonic every fourth bar.

Everything interlocks and nothing doubles. The clav owns the left and plays
on the 16ths the guitar rests on; the guitar owns the right and plays the
ones the clav leaves; the bass fills the beat the kick leaves open; the
horns and the sax only ever answer. No more than three midrange instruments
sound at once, which is why a record with eleven of them stays legible.

  b0-3     the clav alone, wah opening, the organ swelling in behind it
  b4-11    the vamp: bass, machine, clav, wah guitar
  b12-27   verse 1 - the Rhodes comps, the tenor answers twice
  b28-35   pre-chorus: the Leslie changes gear, horns climb, hang on the five
  b36-51   chorus 1 - the talkbox sings, horns answer in the gaps
  b52-59   breakdown: the bass through the envelope filter, congas, one stab
  b60-75   verse 2 - the tenor takes the answers, Rhodes underneath
  b76-83   pre-chorus 2
  b84-99   chorus 2 - the vocoder harmonises the hook
  b100-107 bridge: eight bars of tenor over a ii-V-I, half the machine
  b108-123 last chorus - horns on every eighth, everybody
  b124-127 outro: back to the vamp, subtract, one last stab
"""
import numpy as np
from funklib import *

rng = np.random.default_rng(19)
np.random.seed(19)
s = Session(128, tail=3.0)

# ---- the harmony -------------------------------------------------------
# E dorian: E F# G A B C# D. The C# is the whole point - it is what makes
# the IV chord major, and a IV major in a minor key is the difference
# between funk and a lament.
CH = {
    'Em9':   dict(root=28, clav=(55, 59, 62, 66), keys=(52, 55, 59, 62, 66),
                  org=(55, 59, 62, 66), brass=(71, 74, 78), voc=(59, 62, 66, 71), third=3),
    'A13':   dict(root=33, clav=(55, 61, 66, 69), keys=(49, 55, 61, 64, 66),
                  org=(55, 61, 64, 66), brass=(73, 76, 78), voc=(61, 64, 66, 73), third=4),
    'Cmaj9': dict(root=36, clav=(55, 59, 62, 64), keys=(52, 55, 59, 62, 64),
                  org=(55, 59, 62, 64), brass=(71, 74, 76), voc=(59, 62, 64, 71), third=4),
    'D9':    dict(root=38, clav=(54, 60, 64, 69), keys=(50, 54, 60, 64, 69),
                  org=(54, 57, 60, 64), brass=(72, 74, 78), voc=(57, 60, 64, 69), third=4),
    'Bm7':   dict(root=35, clav=(59, 62, 66, 69), keys=(50, 54, 59, 62, 66),
                  org=(54, 59, 62, 66), brass=(69, 74, 78), voc=(59, 62, 66, 69), third=3),
    'B7#9':  dict(root=35, clav=(51, 54, 57, 62), keys=(51, 54, 57, 62, 66),
                  org=(51, 54, 57, 62), brass=(69, 74, 78), voc=(57, 62, 63, 69), third=4),
    'Am9':   dict(root=33, clav=(55, 59, 60, 64), keys=(48, 52, 55, 59, 64),
                  org=(52, 55, 59, 64), brass=(72, 76, 79), voc=(55, 59, 64, 67), third=3),
    'Gmaj9': dict(root=31, clav=(59, 62, 66, 69), keys=(50, 55, 59, 62, 66),
                  org=(55, 59, 62, 66), brass=(71, 74, 78), voc=(59, 62, 66, 71), third=4),
}

VAMP   = ['Em9', 'A13']
PRE    = ['Cmaj9', 'Cmaj9', 'D9', 'D9', 'Cmaj9', 'Cmaj9', 'B7#9', 'B7#9']
CHORUS = ['Cmaj9', 'D9', 'Bm7', 'Em9']
BRIDGE = ['Am9', 'D9', 'Gmaj9', 'Gmaj9', 'Am9', 'D9', 'Cmaj9', 'B7#9']

SECTIONS = [(0, 'intro'), (4, 'groove'), (12, 'verse'), (28, 'pre'),
            (36, 'chorus'), (52, 'break'), (60, 'verse2'), (76, 'pre2'),
            (84, 'chorus2'), (100, 'bridge'), (108, 'chorus3'), (124, 'outro')]
END = 128
VAMPY = {'intro', 'groove', 'verse', 'verse2', 'break', 'outro'}


def section(b):
    name, b0 = SECTIONS[0]
    for st, nm in SECTIONS:
        if b >= st:
            name, b0 = nm, st
    return name, b0


def chord(b):
    name, b0 = section(b)
    if name in VAMPY:
        return VAMP[(b - b0) % 2]
    if name.startswith('pre'):
        return PRE[(b - b0) % 8]
    if name == 'bridge':
        return BRIDGE[(b - b0) % 8]
    return CHORUS[(b - b0) % 4]


def C(b): return CH[chord(b)]


# ---- the bass ----------------------------------------------------------
# Offsets from the root; -1 means "the third of whatever chord this is", so
# one written line plays correctly over a minor vamp and a dominant chorus.
# Everything else is root, fourth, fifth, flat seven and the octave - the
# five notes that are safe on both, which is why funk basslines transpose
# across a progression without being rewritten.
P_VAMP = ((0, 0, 't'), (3, 12, 'p'), (5, 0, 'g'), (6, 10, 't'), (8, 0, 't'),
          (9, 0, 'g'), (11, 12, 'p'), (13, 0, 'g'), (14, 7, 't'))
P_ANS  = ((0, 0, 't'), (2, 0, 'g'), (3, 12, 'p'), (6, 0, 't'), (7, -1, 'h'),
          (8, 5, 't'), (10, 0, 'g'), (11, 12, 'p'), (12, 0, 't'), (14, 10, 't'))
P_BUSY = ((0, 0, 't'), (1, 0, 'g'), (3, 12, 'p'), (4, 0, 'g'), (5, 10, 't'),
          (6, 0, 'g'), (7, 12, 'p'), (9, 0, 't'), (10, 0, 'g'), (11, 15, 'p'),
          (12, 7, 't'), (13, 0, 'g'), (14, 0, 't'), (15, 0, 'g'))
P_DRIVE = ((0, 0, 't'), (3, 12, 'p'), (6, 0, 't'), (8, 7, 't'), (10, 0, 'g'),
           (11, 12, 'p'), (14, 0, 't'))
P_HOLD = ((0, 0, 't'), (5, 0, 'g'), (8, 12, 'p'), (13, 0, 'g'), (14, 7, 'h'))
P_INTRO = ((0, 0, 't'), (6, 0, 'g'), (8, 0, 't'), (11, 12, 'p'), (14, 0, 'g'))
P_MUTRON = ((0, 0, 't'), (1, 0, 'g'), (2, 12, 'p'), (4, 0, 'g'), (5, 0, 't'),
            (7, 10, 'p'), (8, 0, 'g'), (9, 5, 't'), (11, 12, 'p'), (12, 0, 'g'),
            (13, 0, 't'), (15, 0, 'g'))


def notes_for(b, pat):
    c = C(b)
    r, th = c['root'], c['third']
    return tuple((sw(st), r + (th if off == -1 else off), k) for st, off, k in pat)


def bassbarfor(b, pat, level=0.52, **kw):
    s.place(s.pos(b), slapbar(notes_for(b, pat), take=b % 3, **kw), level, 'bass')


def mutron(b, pat, level=0.52, sens=1.35):
    """The breakdown bass: the same hand, a filter that answers it."""
    seg = slapbar(notes_for(b, pat), take=b % 3, mid=0.25, comp=1.1)
    out = squash(envfilter(seg, sens=sens, lo=150, hi=2900, res=4.0), 2.0, 0.62)
    s.place(s.pos(b), out, level, 'bass')


# ---- the clav and the guitar -------------------------------------------
# Two 16th-note instruments that must not play the same 16ths. The clav takes
# the downbeat side of every beat, the guitar the "e" and "a" between them -
# together they make a continuous line neither of them contains, which is the
# oldest trick in this music and the reason funk sounds busy and mixes clean.
#   X = a chord, x = the palm on the strings, . = nothing
CLAV_A = "X.xx.xX..xX.x.x."
CLAV_B = "X.x.Xx..X.xxX.x."
GTR_A  = "..X..x.x.X..x.xX"
GTR_B  = ".x..X..x.X.x..xX"
WEIGHT = {0: 1.0, 4: 0.80, 8: 0.90, 12: 0.78, 2: 0.62, 6: 0.58, 10: 0.62, 14: 0.60}


def chank(b, pat, voice, bus, level, dur=1.0, pan=0.0, notes=None):
    nts = notes if notes is not None else C(b)['clav']
    for i, ch_ in enumerate(pat):
        if ch_ == '.':
            continue
        v = WEIGHT.get(i, 0.44) * (1.0 + 0.07 * rng.standard_normal())
        seg = voice(nts, dur if ch_ == 'X' else 0.7, take=(i + b) % 3,
                    mute=0.0 if ch_ == 'X' else 1.0)
        if pan:
            seg = panned(seg, pan)
        s.place(s.pos(b, sw(i)), seg, level * v * (1.0 if ch_ == 'X' else 0.52), bus)


# ---- the organ ---------------------------------------------------------
# 888000000 is the first three drawbars out: the sub-octave, the fifth above
# and the note itself. No filter, so the registration IS the tone, and every
# change of colour on this record is a different set of digits.
def orgpad(b, dur=16, level=0.34, bars='888000000', perc=0.0, st=0.0, take=None):
    s.place(s.pos(b, st), organ(C(b)['org'], dur, bars=bars, perc=perc,
                                take=b % 3 if take is None else take), level, 'organ')


def orgstab(b, evs, level=0.40, bars='888800000'):
    for st, ln in evs:
        s.place(s.pos(b, sw(st)), organ(C(b)['org'], ln, bars=bars, perc=0.7,
                                        drive=2.2, take=(b + int(st)) % 3), level, 'organ')


# ---- the horns ---------------------------------------------------------
def hits(b, evs, level=0.5, voicing=None, oct_=0):
    """(step, length[, fall]) - the section answers, it does not accompany."""
    nts = tuple(n + oct_ for n in (voicing or C(b)['brass']))
    for ev in evs:
        st, ln = ev[0], ev[1]
        fall = ev[2] if len(ev) > 2 else 0.0
        s.place(s.pos(b, sw(st)), brass(nts, ln, take=(b + int(st)) % 3,
                                        fall=fall, hold=0.45 if ln > 2 else 0.35),
                level, 'brass')


def blow(b, phrase, level=0.42, take=0, **kw):
    s.place(s.pos(b), saxline(tuple((sw(st), n, a) for st, n, a in phrase),
                              take=take, **kw), level, 'sax')


# ---- the machine -------------------------------------------------------
# Where a real drummer's left hand goes between the backbeats. They are
# inaudible as events and the bar collapses without them - the same reason
# the bass is full of dead notes. A machine record gets them by hand.
SNARE_GHOSTS = ((6, 0.13), (7, 0.09), (10, 0.11), (13, 0.08), (15, 0.14))


def kit(b, floor=True, hats=True, open_=True, clap=True, cab=True,
        ghost=(10.5,), level=1.0, tam=False, ghostsnare=1.0):
    """Kick on every beat and the open hat between them - the felt pulse is
    112 and the body can keep up with it, which is what separates boogie
    from the funk it came out of."""
    if floor:
        for st in (0, 4, 8, 12):
            s.place(s.pos(b, st), fkick(), 0.62 * level, 'drums')
            s.hit(s.pos(b, st))
        for st in ghost:
            s.place(s.pos(b, sw(st)), fkick(click=0.6), 0.30 * level, 'drums')
    for st in (4, 12):
        s.place(s.pos(b, st), fsnare(gate=0.55, seed=b % 3), 0.44 * level, 'drums')
        if clap:
            s.place(s.pos(b, st), fclap(seed=b % 3), 0.36 * level, 'drums')
    for st, v in SNARE_GHOSTS:
        if ghostsnare and (st != 13 or b % 2):
            s.place(s.pos(b, sw(st)), fsnare(2, gate=0.0, snap=0.75, decay=0.055,
                                             seed=(b + st) % 4),
                    v * ghostsnare * level * (0.85 + 0.3 * rng.random()), 'drums')
    if hats:
        for i in range(0, 16, 2):
            s.place(s.pos(b, sw(i)), fhat(seed=i % 4),
                    0.30 * level * (1.0 if i % 4 == 0 else 0.66), 'perc')
    if open_:
        for i in (2, 6, 10, 14):
            s.place(s.pos(b, sw(i)), fhat(3, open_=True, seed=i % 3), 0.24 * level, 'perc')
    if cab:
        for i in range(16):
            v = 0.9 if i % 4 == 0 else (0.55 if i % 2 == 0 else 0.42)
            s.place(s.pos(b, sw(i)), panned(cabasa(seed=i % 5), 0.35),
                    0.26 * level * v, 'perc')
    if tam:
        for st in (4, 12):
            s.place(s.pos(b, st), panned(tamb(ring=0.5, seed=b % 3), -0.4),
                    0.30 * level, 'perc')


def congas(b, level=1.0, seed=0):
    fig = ((2, 230, 0.0), (3, 300, 0.7), (6, 230, 0.0), (7, 190, 0.0),
           (10.5, 300, 0.8), (13, 230, 0.0), (14, 300, 0.0), (15, 190, 0.3))
    for st, tune, sl in fig:
        s.place(s.pos(b, sw(st)),
                panned(conga(2, tune=tune, slap=sl, seed=seed + int(st)), -0.45),
                0.30 * level * (0.9 if int(st) % 4 == 0 else 0.7), 'perc')


def fill(b, kind='snare', level=1.0):
    if kind == 'snare':
        for i, st in enumerate((12, 13, 13.5, 14, 14.5, 15, 15.5)):
            s.place(s.pos(b, st), fsnare(gate=0.3, seed=i % 3),
                    (0.24 + 0.05 * i) * level, 'drums')
    elif kind == 'toms':
        for i, (st, tn) in enumerate(((10, 240), (11, 200), (12, 165),
                                      (13, 140), (14, 115), (15, 95))):
            s.place(s.pos(b, st), panned(ftom(2, tune=tn, seed=i), 0.5 - 0.2 * i),
                    (0.36 + 0.03 * i) * level, 'drums')
    elif kind == 'stop':
        for st in (12, 14, 15):
            s.place(s.pos(b, st), fsnare(gate=0.5, seed=int(st) % 3), 0.42 * level, 'drums')
    elif kind == 'clap':
        for st in (12, 12.5, 13, 14, 15):
            s.place(s.pos(b, sw(st)), fclap(seed=int(st * 2) % 3), 0.34 * level, 'drums')


def crash(b, st=0, level=0.5):
    s.place(s.pos(b, st), fcrash(seed=b % 3), level, 'drums')


# ---- the talkbox hook --------------------------------------------------
# One arch over the four chorus bars, peaking on the G in bar 3 - about
# two-thirds of the way through the phrase, where a climax belongs. It stays
# inside a tenth because a talkbox is a mouth and a mouth has a range.
HOOK = [
    ((2, 71, 'oh'), (6, 74, 'ah'), (10, 76, 'ee'), (14, 74, 'oh')),
    ((0, 72, 'uh'), (6, 69, 'ah'), (12, 71, 'eh')),
    ((0, 74, 'oh'), (4, 76, 'ah'), (8, 79, 'ah'), (13, 78, 'ee')),
    ((0, 76, 'ee'), (6, 74, 'oh'), (10, 71, 'aw')),
]
HOOK2 = [
    ((2, 71, 'oh'), (6, 74, 'ah'), (9, 76, 'ee'), (11, 78, 'ah'), (14, 76, 'oh')),
    ((0, 74, 'oh'), (5, 72, 'ah'), (8, 69, 'eh'), (12, 71, 'ah')),
    ((0, 74, 'oh'), (3, 76, 'ah'), (6, 78, 'ee'), (8, 79, 'ah'), (13, 78, 'oh')),
    ((0, 76, 'ee'), (4, 78, 'ah'), (8, 74, 'oh'), (11, 71, 'aw')),
]


def sing(b, phrase, level=0.5, oct_=0, take=0):
    s.place(s.pos(b), talkbox(tuple((sw(st), n + oct_, v) for st, n, v in phrase),
                              take=take), level, 'lead')


def speak(b, phrase, level=0.34, take=0):
    """The vocoder gets the hook's syllables without its pitch - the carrier
    is the chord, so the same words come out as a four-part harmony."""
    s.place(s.pos(b), vocoder(C(b)['voc'], tuple((sw(st), v) for st, _, v in phrase),
                              take=take), level, 'voc')


# ---- the tenor ---------------------------------------------------------
SAX_ANS = [
    ((0, 67, '^>'), (2, 71, 'n'), (4, 74, 'g'), (7, 71, 'n'), (9, 69, 'n'), (11, 67, 'f')),
    ((0, 74, '^>'), (3, 71, 'n'), (5, 69, 'n'), (6, 67, 'n'), (9, 69, 'g'), (12, 71, 'f')),
    ((0, 71, 'n'), (2, 74, '>'), (4, 76, 'g'), (8, 74, 'n'), (10, 71, 'n'), (12, 69, 'f')),
]
# Eight bars over the bridge changes. Chord tones on the strong beats, the
# passing notes between them, and the last bar leans on the #9 of the five
# chord and refuses to resolve until the chorus does it.
SAX_SOLO = [
    ((0, 67, '^'), (3, 69, 'n'), (5, 72, 'n'), (8, 76, '>'), (12, 74, 'n')),
    ((0, 74, 'n'), (2, 72, 'n'), (5, 69, 'n'), (8, 66, 'g'), (12, 69, 'n')),
    ((0, 71, '^>'), (4, 74, 'n'), (6, 76, 'n'), (9, 78, 'n'), (12, 79, 'g')),
    ((0, 79, 'g'), (6, 78, 'n'), (9, 76, 'n'), (12, 74, 'f')),
    ((0, 76, '^'), (3, 74, 'n'), (6, 72, 'n'), (9, 69, 'n'), (12, 67, 'n')),
    ((0, 66, '^'), (3, 69, 'n'), (6, 72, 'n'), (9, 74, '>'), (13, 76, 'n')),
    ((0, 79, '>'), (4, 76, 'n'), (7, 79, 'g'), (11, 76, 'n'), (13, 74, 'n')),
    ((0, 75, 'g>'), (5, 74, 'n'), (8, 71, 'n'), (11, 74, 'n'), (13, 75, 'f')),
]

# =======================================================================
# the arrangement
# =======================================================================

# ---- b0-3: the clav on its own, the organ swelling in behind it ----
for b in range(0, 4):
    chank(b, CLAV_A if b % 2 == 0 else CLAV_B, clavi, 'clav',
          0.28 + 0.10 * b, pan=-0.55)
    for i in range(0, 16, 2):
        s.place(s.pos(b, sw(i)), fhat(seed=i % 4), 0.10 + 0.05 * b, 'perc')
    if b >= 2:
        orgpad(b, 16, 0.20 + 0.10 * (b - 2), bars='808000000')
        for i in range(16):
            s.place(s.pos(b, sw(i)), panned(cabasa(seed=i % 5), 0.35),
                    0.10 * (0.9 if i % 4 == 0 else 0.5), 'perc')
bassbarfor(3, P_INTRO, 0.32)
hits(3, ((12, 2), (14, 2, 2.0)), 0.34)
s.place(s.pos(4) - int(6 * STEP), reverse_crash(6), 0.30, 'drums')

# ---- b4-11: the vamp stated ----
for b in range(4, 12):
    kit(b, tam=(b % 4 == 3))
    bassbarfor(b, P_VAMP if b % 2 == 0 else P_ANS)
    chank(b, CLAV_A if b % 2 == 0 else CLAV_B, clavi, 'clav', 0.40, pan=-0.55)
    if b >= 6:
        chank(b, GTR_A if b % 2 == 0 else GTR_B, fgtr, 'gtr', 0.26, pan=0.55)
    if b >= 8:
        orgpad(b, 16, 0.26, bars='888000000')
crash(4, 0, 0.42)
hits(7, ((10, 2), (12, 3, 1.5)), 0.36)
hits(11, ((8, 2), (10, 2), (12, 4, 3.0)), 0.42)
fill(11, 'clap')

# ---- b12-27: verse 1, the Rhodes comps ----
for b in range(12, 28):
    i = b - 12
    kit(b, ghost=(10.5,) if i % 4 != 3 else (10.5, 15), tam=(i % 4 == 3))
    bassbarfor(b, (P_VAMP, P_ANS, P_VAMP, P_BUSY)[i % 4])
    chank(b, CLAV_A if b % 2 == 0 else CLAV_B, clavi, 'clav', 0.40, pan=-0.55)
    chank(b, GTR_A if b % 2 == 0 else GTR_B, fgtr, 'gtr', 0.26, pan=0.55)
    if i % 8 >= 4:
        congas(b, 0.85, seed=i)
    # the Rhodes takes the comping the organ had; they never both do it
    if i % 4 in (0, 2):
        s.place(s.pos(b, sw(2)), suitcase(C(b)['keys'], 6, vel=0.75, take=b % 3),
                0.34, 'keys')
    if i % 8 == 6:
        s.place(s.pos(b, sw(10)), suitcase(C(b)['keys'], 6, vel=0.85, take=b % 3),
                0.36, 'keys')
    if i % 8 == 3:
        orgstab(b, ((10, 2), (12, 2)), 0.24)
blow(19, SAX_ANS[0], 0.40, take=0)
blow(27, SAX_ANS[2], 0.44, take=2)
hits(23, ((12, 2), (14, 2)), 0.34)
hits(27, ((4, 2), (6, 2)), 0.36)
fill(27, 'toms')
crash(12, 0, 0.38)

# ---- b28-35: pre-chorus, the climb, the Leslie changes gear ----
CLIMB = ((71, 76, 79), (72, 76, 79), (74, 78, 81), (74, 79, 83),
         (76, 79, 83), (76, 81, 84), (78, 81, 86), (78, 83, 86))
for b in range(28, 36):
    i = b - 28
    kit(b, ghost=(10.5, 15), tam=True, level=1.0 + 0.03 * i)
    bassbarfor(b, P_DRIVE if i < 6 else P_BUSY, 0.54)
    chank(b, CLAV_A, clavi, 'clav', 0.42, pan=-0.55)
    chank(b, GTR_A, fgtr, 'gtr', 0.28, pan=0.55)
    orgpad(b, 16, 0.30 + 0.02 * i, bars='888800000', perc=0.4 if i % 2 == 0 else 0.0)
    congas(b, 0.9, seed=i)
    hits(b, ((0, 4),) if i < 6 else ((0, 2), (4, 2), (8, 2), (12, 4)),
         0.36 + 0.02 * i, voicing=CLIMB[i])
s.place(s.pos(30), riser(int(6 * 16), f0=200, f1=900), 0.10, 'fx')
fill(35, 'snare', 1.1)
s.place(s.pos(35, 15), downlifter(4, f0=1800, f1=90), 0.20, 'fx')

# ---- b36-51: chorus 1 ----
for b in range(36, 52):
    i = b - 36
    kit(b, ghost=(10.5, 14.5), tam=True)
    bassbarfor(b, (P_DRIVE, P_VAMP, P_DRIVE, P_ANS)[i % 4], 0.56)
    chank(b, CLAV_B if b % 2 else CLAV_A, clavi, 'clav', 0.40, pan=-0.55)
    chank(b, GTR_B if b % 2 else GTR_A, fgtr, 'gtr', 0.28, pan=0.55)
    orgpad(b, 16, 0.30, bars='888800000')
    sing(b, HOOK[i % 4], 0.46, take=i % 4)
    congas(b, 0.8, seed=i)
    if i % 4 == 1:
        hits(b, ((10, 2), (12, 2)), 0.34)
    if i % 4 == 3:
        hits(b, ((8, 2), (10, 2), (12, 4, 2.0)), 0.40)
crash(36, 0, 0.50)
crash(44, 0, 0.34)
fill(51, 'stop', 1.0)

# ---- b52-59: the breakdown, the bass through the envelope filter ----
for b in range(52, 60):
    i = b - 52
    mutron(b, (P_MUTRON, P_ANS)[i % 2], 0.60)
    chank(b, CLAV_A if b % 2 == 0 else CLAV_B, clavi, 'clav', 0.44, pan=-0.55)
    for j in range(16):
        v = 0.9 if j % 4 == 0 else (0.55 if j % 2 == 0 else 0.42)
        s.place(s.pos(b, sw(j)), panned(cabasa(seed=j % 5), 0.35), 0.24 * v, 'perc')
    if i >= 2:
        congas(b, 1.0, seed=i)
    if i >= 3:
        orgstab(b, ((6, 2), (10, 2), (14, 2)), 0.30, bars='800000888')
    if i >= 4:
        for st in (4, 12):
            s.place(s.pos(b, st), fclap(seed=b % 3), 0.34, 'drums')
        for j in (2, 6, 10, 14):
            s.place(s.pos(b, sw(j)), fhat(seed=j % 4), 0.20, 'perc')
    if i >= 6:
        kit(b, hats=False, cab=False, clap=False, open_=True, ghost=(10.5, 15))
blow(58, SAX_ANS[1], 0.46, take=1)
hits(59, ((8, 2), (10, 2), (12, 4, 3.0)), 0.44)
fill(59, 'toms', 1.05)

# ---- b60-75: verse 2, the tenor takes the answers ----
for b in range(60, 76):
    i = b - 60
    kit(b, ghost=(10.5, 15) if i % 2 else (10.5,), tam=True)
    bassbarfor(b, (P_BUSY, P_ANS, P_VAMP, P_BUSY)[i % 4])
    chank(b, CLAV_A if b % 2 == 0 else CLAV_B, clavi, 'clav', 0.40, pan=-0.55)
    chank(b, GTR_A if b % 2 == 0 else GTR_B, fgtr, 'gtr', 0.30, pan=0.55)
    congas(b, 0.9, seed=i)
    if i % 4 in (0, 2):
        s.place(s.pos(b, sw(2)), suitcase(C(b)['keys'], 6, vel=0.8, take=b % 3),
                0.32, 'keys')
    if i % 8 == 5:
        s.place(s.pos(b, sw(10)), suitcase(C(b)['keys'], 8, vel=0.9, take=b % 3),
                0.34, 'keys')
    if i % 8 == 7:
        orgstab(b, ((8, 2), (10, 2)), 0.26)
for k, b in enumerate((63, 67, 71, 75)):
    blow(b, SAX_ANS[k % 3], 0.42 + 0.02 * k, take=k)
crash(60, 0, 0.42)
crash(68, 0, 0.30)
fill(75, 'clap', 1.05)

# ---- b76-83: pre-chorus 2 ----
for b in range(76, 84):
    i = b - 76
    kit(b, ghost=(10.5, 15), tam=True, level=1.0 + 0.03 * i)
    bassbarfor(b, P_DRIVE if i < 6 else P_BUSY, 0.55)
    chank(b, CLAV_A, clavi, 'clav', 0.42, pan=-0.55)
    chank(b, GTR_A, fgtr, 'gtr', 0.30, pan=0.55)
    orgpad(b, 16, 0.32 + 0.02 * i, bars='888800000', perc=0.4 if i % 2 == 0 else 0.0)
    congas(b, 0.95, seed=i)
    hits(b, ((0, 4),) if i < 6 else ((0, 2), (4, 2), (8, 2), (12, 4)),
         0.38 + 0.02 * i, voicing=CLIMB[i])
s.place(s.pos(78), riser(int(6 * 16), f0=200, f1=1100), 0.11, 'fx')
fill(83, 'snare', 1.15)
s.place(s.pos(83, 15), downlifter(4, f0=1800, f1=90), 0.22, 'fx')

# ---- b84-99: chorus 2, the vocoder harmonises the hook ----
for b in range(84, 100):
    i = b - 84
    kit(b, ghost=(10.5, 14.5), tam=True)
    bassbarfor(b, (P_DRIVE, P_BUSY, P_DRIVE, P_ANS)[i % 4], 0.56)
    chank(b, CLAV_B if b % 2 else CLAV_A, clavi, 'clav', 0.40, pan=-0.55)
    chank(b, GTR_B if b % 2 else GTR_A, fgtr, 'gtr', 0.30, pan=0.55)
    orgpad(b, 16, 0.32, bars='888800000')
    sing(b, HOOK2[i % 4], 0.46, take=i % 4)
    speak(b, HOOK2[i % 4], 0.30, take=i % 4)
    congas(b, 0.85, seed=i)
    if i % 4 == 1:
        hits(b, ((10, 2), (12, 2)), 0.36)
    if i % 4 == 3:
        hits(b, ((8, 2), (10, 2), (12, 4, 2.0)), 0.42)
crash(84, 0, 0.50)
crash(92, 0, 0.34)
fill(99, 'toms', 1.05)

# ---- b100-107: the bridge, eight bars of tenor ----
# Half the machine, the harmony finally goes somewhere - a ii-V-I in G,
# twice - and the horn section shuts up so one player can talk.
for b in range(100, 108):
    i = b - 100
    for st in (0, 8):
        s.place(s.pos(b, st), fkick(), 0.52, 'drums')
        s.hit(s.pos(b, st))
    s.place(s.pos(b, 12), fsnare(gate=0.7, seed=b % 3), 0.44, 'drums')
    s.place(s.pos(b, 12), fclap(seed=b % 3), 0.32, 'drums')
    for j in (2, 6, 10, 14):
        s.place(s.pos(b, sw(j)), fhat(3, open_=True, seed=j % 3), 0.20, 'perc')
    if i >= 3:
        for j in range(16):
            s.place(s.pos(b, sw(j)), panned(cabasa(seed=j % 5), 0.35),
                    0.18 * (0.9 if j % 4 == 0 else 0.5), 'perc')
    mutron(b, P_HOLD, 0.46, sens=1.1)
    s.place(s.pos(b), moogbar(notes_for(b, P_HOLD), take=b % 3), 0.15, 'bass')
    s.place(s.pos(b), suitcase(C(b)['keys'], 16, vel=0.5, take=b % 3), 0.26, 'keys')
    if i >= 2:
        orgpad(b, 16, 0.22, bars='808000008')
    congas(b, 0.45, seed=i)
    blow(b, SAX_SOLO[i], 0.50, take=10 + i, bright=1.1)
hits(107, ((8, 2), (10, 2), (12, 4, 3.0)), 0.46)
fill(107, 'snare', 1.15)
s.place(s.pos(107, 15), downlifter(4, f0=2000, f1=80), 0.22, 'fx')

# ---- b108-123: last chorus ----
for b in range(108, 124):
    i = b - 108
    kit(b, ghost=(10.5, 14.5, 15), tam=True)
    bassbarfor(b, (P_DRIVE, P_BUSY, P_DRIVE, P_BUSY)[i % 4], 0.58)
    chank(b, CLAV_B if b % 2 else CLAV_A, clavi, 'clav', 0.42, pan=-0.55)
    chank(b, GTR_B if b % 2 else GTR_A, fgtr, 'gtr', 0.32, pan=0.55)
    orgpad(b, 16, 0.34, bars='888888000')
    sing(b, HOOK2[i % 4], 0.48, take=i % 4)
    speak(b, HOOK2[i % 4], 0.32, take=i % 4)
    congas(b, 1.0, seed=i)
    hits(b, ((0, 2), (6, 2)) if i % 2 == 0 else ((2, 2), (8, 2), (12, 4, 2.0)),
         0.34 if i % 2 == 0 else 0.40)
    if i in (5, 13):
        blow(b, SAX_ANS[i % 3], 0.40, take=20 + i)
crash(108, 0, 0.55)
crash(116, 0, 0.36)

# ---- b124-127: the outro ----
for b in range(124, 128):
    i = b - 124
    kit(b, tam=(i < 2), open_=(i < 3), cab=(i < 3), clap=(i < 2),
        hats=(i < 3), level=1.0 - 0.15 * i)
    bassbarfor(b, (P_VAMP, P_ANS, P_VAMP, P_HOLD)[i], 0.52 - 0.03 * i)
    chank(b, CLAV_A if b % 2 == 0 else CLAV_B, clavi, 'clav', 0.40 - 0.04 * i, pan=-0.55)
    orgpad(b, 16, 0.30 - 0.06 * i, bars='888000000')
    if i < 2:
        chank(b, GTR_A, fgtr, 'gtr', 0.26, pan=0.55)
    if i < 3:
        congas(b, 0.8 - 0.2 * i, seed=i)
hits(127, ((0, 6, 3.0),), 0.44)
s.place(s.pos(127, 0), fcrash(seed=1), 0.40, 'drums')
s.place(s.pos(127, 0), suitcase(CH['Em9']['keys'], 16, vel=0.9), 0.32, 'keys')
s.place(s.pos(127), slapbar(((0, 28, 't'), (0.5, 28, 'g')), decay=0.9), 0.50, 'bass')

# =======================================================================
# the mix
# =======================================================================
# ---- the speaker ----
# One rotor for the whole record, so its phase never restarts, and it changes
# gear where the arrangement does. The organist's right foot is on that
# switch and it is the only automation this instrument has.
_rate = np.full(s.total, 0.85, dtype=np.float64)
for a, b in ((28, 52), (76, 100), (108, 124)):
    _rate[s.pos(a):s.pos(b)] = 6.6
_rate[s.pos(100):s.pos(108)] = 1.1
s.bus['organ'] = leslie(s.bus['organ'], rate=_rate, depth=1.0)

# ---- the pedals ----
# The clav goes through a lowpass rocking once every two bars; the guitar
# through an actual wah, twice a bar, with the resonance up. Sixteen
# identical 16ths become a part without a single note changing.
s.bus['clav'] = autowah(s.bus['clav'], per_bar=2.0, lo=460, hi=4600, res=1.7)
s.bus['gtr'] = pedal(s.bus['gtr'], per_bar=0.5, lo=540, hi=3400, res=4.5,
                     phase=np.pi, mix=0.78)

# ---- the room ----
s.bus['drums'] += room(s.bus['drums'], decay=0.42, wet=0.14, tone=6500)
s.bus['perc'] += room(s.bus['perc'], decay=0.36, wet=0.10, tone=8000)
s.bus['brass'] += room(s.bus['brass'], decay=1.3, wet=0.26, tone=5000)
s.bus['sax'] += room(s.bus['sax'], decay=1.5, wet=0.24, tone=4600)
s.bus['keys'] += room(s.bus['keys'], decay=1.1, wet=0.16, tone=4800)
s.bus['lead'] += room(s.bus['lead'], decay=1.5, wet=0.20, tone=4200)
s.bus['voc'] += room(s.bus['voc'], decay=1.8, wet=0.24, tone=5200)
s.bus['organ'] += room(s.bus['organ'], decay=0.9, wet=0.10, tone=4200)

# ---- the compressors, because everything on a 1983 record went through one ----
s.bus['clav'] = squash(s.bus['clav'], 3.2, 0.52)
s.bus['gtr'] = squash(s.bus['gtr'], 3.2, 0.52)
s.bus['brass'] = squash(s.bus['brass'], 2.2, 0.60)
s.bus['keys'] = squash(s.bus['keys'], 2.0, 0.62)
s.bus['sax'] = squash(s.bus['sax'], 2.6, 0.58)
s.bus['organ'] = squash(s.bus['organ'], 1.9, 0.64)

# the talkbox is the voice, so it gets what a voice gets: the tail of a held
# note pulled up to meet the syllable that started it, then a dotted eighth
_pk = float(np.abs(s.bus['lead']).max()) or 1.0
s.bus['lead'] = softclip(s.bus['lead'] / _pk * 2.8, 1.0, knee=0.35) * _pk * 0.48
s.bus['lead'] += delay(s.bus['lead'], steps_=3.0, times=3, fb=0.34,
                       ping=True, damp=900)[:s.total] * 0.38

# ---- make room for whatever is talking ----
# The clav, the guitar, the organ and the talkbox all live at 800-3000 Hz.
# Turning the talkbox up only makes all of them louder; instead the
# accompaniment steps out of that one band wherever a lead is playing, and
# steps straight back in when it stops.
def duck_band(target, trigger, lo=800, hi=3200, depth=0.34, sens=3.2):
    env = np.abs(trigger).max(axis=1)
    env = uniform_filter1d(env, int(0.030 * SR))
    env = np.clip(env / max(env.max(), 1e-9) * sens, 0, 1)
    g = uniform_filter1d(1 - depth * env, int(0.05 * SR)).astype(np.float32)
    return target - bandpass(target, lo, hi) * (1 - g)[:, None]


_voices = np.maximum(np.abs(s.bus['lead']), np.abs(s.bus['sax']))
s.bus['clav'] = duck_band(s.bus['clav'], _voices)
s.bus['gtr'] = duck_band(s.bus['gtr'], _voices, depth=0.30)
s.bus['organ'] = duck_band(s.bus['organ'], _voices, lo=700, hi=3000, depth=0.32)
s.bus['keys'] = duck_band(s.bus['keys'], s.bus['brass'], lo=900, hi=3000, depth=0.30)

# ---- bus tone ----
# The bass owns everything under 110 Hz and is the only thing down there;
# the kick is short enough to sit in the gap rather than fight it.
s.bus['bass'] = mono_below(hp(s.bus['bass'], 31, order=2), 130)
s.bus['drums'] = shelf(hp(s.bus['drums'], 36, order=2), 7500, 4.0, 'high')
s.bus['perc'] = shelf(hp(s.bus['perc'], 320, order=2), 7000, 3.5, 'high')
s.bus['clav'] = hp(s.bus['clav'], 200, order=2)
s.bus['gtr'] = hp(s.bus['gtr'], 260, order=2)
s.bus['keys'] = peak_eq(hp(s.bus['keys'], 150, order=2), 2200, 2.5, width=0.6)
s.bus['organ'] = hp(s.bus['organ'], 110, order=2)
s.bus['brass'] = hp(s.bus['brass'], 240, order=2)
s.bus['sax'] = hp(s.bus['sax'], 220, order=2)
s.bus['lead'] = hp(s.bus['lead'], 170, order=2)
s.bus['voc'] = hp(s.bus['voc'], 280, order=2)

GAINS = {'drums': 0.44, 'perc': 1.45, 'bass': 0.56, 'clav': 1.55, 'gtr': 1.45,
         'keys': 1.30, 'brass': 0.66, 'organ': 0.44, 'sax': 0.38, 'voc': 0.70,
         'lead': 0.34, 'fx': 0.30}
s.report(GAINS)
s.render('funk_pyatnica_112.wav', drive=1.1, duck=0.78, limit=0.94,
         gains=GAINS, clip=0.72, fade=1.6)
