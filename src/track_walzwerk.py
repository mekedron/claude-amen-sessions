"""WALZWERK - hard industrial techno at 168 BPM, F Locrian. No acid.

A rolling mill. Not a record with factory samples on it: a record whose
instruments ARE machines, and whose only melodic voice is the building.

Two decisions make it, and both are subtractions.

**No 303 anywhere.** Every industrial record this project has made leans on
`acidline` for its hook, and a 303 is the one thing in the palette that is
unmistakably a synthesiser. Take it away and something else has to carry
pitch across four minutes - which is what `girder()` is for. A beam the size
of the hall, excited by friction rather than struck, gliding F1 to the
tritone above it and back over forty seconds. An object that size cannot
change pitch. That is the whole surrealism of the record and it is one
gesture, not a sequence of notes.

**The machines run on their own cycles.** `mill()` is a machine tool: it
bites, screeches while the edge is in the metal, labours, exhales, and idles
in between. Three of them run at 6, 10 and 14 steps - three, five and seven
bars - panned apart, so they agree with the bar and with each other exactly
once every 105 bars. That is what a shop sounds like from the gantry. Every
cycle is EVEN, so every hit still lands on an eighth: a pitched, ringing
figure that never touches a beat or an offbeat eighth is not heard as
polymeter, it is heard as a second machine playing badly.

Around them: `press()` stamping plate on the two, `pipe()` - a tube struck
from the inside, its bracket buzzing while it is still moving - and the forge,
the chains, the steam and the stepper motors that were already here.

And underneath the two drops, `shear()`: the plate letting go. One
oscillator, split at 92 Hz so the weight stays clean, everything above it
through a wavefolder whose amount ramps across the phrase and a resonant
lowpass whose cutoff is moved by a lane that accelerates from a quarter to a
thirty-second. It never retriggers - the gesture is the acceleration.
Wherever it plays, the kick's own clean sub layer comes almost all the way
out: two sines at 43 Hz with unrelated phases cancel, and letting the shear
own the bottom is what makes the drop change character rather than merely get
louder.

F Locrian, and the b5 is the point. The root and the B a tritone above it are
the two notes the whole record is built from: the pipes are tuned to them, the
girder glides between them, and the stabs play both at once.

    ANFAHRT | WALZWERK | STANZE | LEERLAUF | HOCHOFEN
            | RISS | UEBERLAST | ABSTICH (56) | NACHSCHICHT | SCHICHTENDE

ABSTICH is fifty-six bars, so it has its own re-drop at 184: two bars
stripped to the kick and the beam, a hole, and it lands again. Fifty-six bars
at one level is a plateau however loud the level is.

The offbeat kicks are a shorter, drier, low-passed voice rather than the same
kick fired more often, and the kick itself is capped at 6.8 kHz. A doubly
hard-clipped kick with a noise exhale falls to silence between hits at four a
bar and only 15.7 dB at eight, so above that density the top of the kit stops
being events and becomes one continuous rasp - the hats own everything above
6.8 kHz and the kick keeps all of the weight and all of the beater.

256 bars, 6:06. The kick is on every beat from bar 8 to the end except in the
four holes. The lowest point is bar 136 and the peak starts at 160, which is
62% of the way through and runs to 84%. The body of the record spans 6.3 dB
and the holes are 0.17 of a bar at -10 dB: enough to feel, not enough to hear
as the record changing volume.
"""
import numpy as np
from industriallib import *

set_tempo(168)
np.random.seed(1681)

# ---- the material ----
ROOT  = 43.65                                    # F1 - kick, sub, girder, hall
TRIT  = 61.74                                    # B1 - the b5, and the other pole

Session.DUCKED = {'bass': 1.0, 'shear': 1.0, 'rumble': 0.92, 'sub': 0.45,
                  'shop': 0.55, 'hall': 0.45, 'struct': 0.80, 'voice': 0.60,
                  'fx': 0.35}

# F Locrian from F2 = 41:  F Gb Ab Bb Cb(B) Db Eb
#   41 F2  42 Gb2  44 Ab2  46 Bb2  47 B2  48 Db3  51 Eb3
#   53 F3  54 Gb3  56 Ab3  58 Bb3  59 B3  60 Db4  63 Eb4  65 F4  66 Gb4

# The pipes. A pipe is a tube and it rings, so it is a part, and a part that
# lands only on weak sixteenths is heard as a separate machine rather than as
# syncopation. The spine is on offbeat eighths - steps the kick never uses -
# with at most one decoration per bar on a weak one.
PIPES = (
    ((2, 54, 0.95), (10, 47, 0.70), (13, 66, 0.34)),
    ((6, 47, 0.85), (10, 54, 0.60), (2, 59, 0.50)),
    ((2, 59, 0.90), (14, 47, 0.75), (7, 54, 0.36)),
    ((6, 54, 0.75), (10, 66, 0.55), (2, 47, 0.95), (15, 59, 0.30)),
)

# Struck plate on the floor of the hall - short, dark, low. Bright ringing
# metal above C5 reads as a glockenspiel and makes a dark record cheerful.
PLATES = (
    ((4, 47, 0.55), (12, 42, 0.40)),
    ((8, 41, 0.60), (14, 47, 0.35)),
    ((4, 44, 0.50), (10, 41, 0.45)),
    ((0, 47, 0.42), (12, 51, 0.38)),
)

# The bass. F Locrian from F1 = 29: F Gb Ab Bb Cb(B) Db Eb, and the line
# lives on the root with the b2 above it and the b7 below. Written as
# (step, midi, length) with real gaps in it - a held pitch under a moving
# filter is a texture, and what the ear reports about a texture in the sub is
# "low-frequency noise". The kick owns 0, 4, 8 and 12, so the line answers on
# the offbeat eighths and only doubles the beat when it wants the weight.
BASS_A = ((0, 29, 2.5), (6, 29, 2.0), (10, 30, 2.5), (14, 29, 1.5))
BASS_B = ((0, 29, 2.0), (4, 29, 1.5), (6, 29, 1.5), (10, 27, 2.5), (14, 29, 1.5))
BASS_C = ((0, 29, 2.0), (3, 29, 1.0), (6, 30, 2.0), (10, 29, 2.0),
          (12, 29, 1.5), (14, 35, 1.5))
BASS_D = ((0, 29, 3.0), (6, 27, 2.0), (10, 29, 2.0), (13, 30, 1.5))

# The tritone, played as one object. No third, nothing to soften it.
STAB_A = (midi(41), midi(47), midi(53))
STAB_B = (midi(42), midi(48), midi(54))

s = Session(256, tail=4.0)

# ---- the floor ----
def floor(b, gain=1.0, beats=(0, 4, 8, 12), rum=1.0, wg=0.9, extra=(),
          tune=ROOT, drive=13.0, decay=0.125, lpf=None, rdecay=0.62,
          rtone=155, rdrive=2.9, hiss=0.45, air=0.32):
    # `rdecay` is shorter wherever the shear plays. A rumble is the kick's
    # room and at 0.85 s its tail spans two beats, which is longer than the
    # holes the bass line is made of - so the growl fills them and the line
    # reads as one continuous low noise however well it is written.
    """Three layers, one instrument: the punch, the room it is standing in,
    and the weight underneath both.

    `extra` are additional kicks off the beat - the schranz gear. They are a
    SHORTER AND DRIER voice, not the same kick fired more often. An
    industrial kick is hard-clipped twice and carries a noise exhale, and at
    178 ms apart those exhales overlap: measured in 2-9 kHz, four kicks a bar
    fall to silence between hits and eight fall only 15.7 dB, so the top of
    the kit stops being eight events and becomes one continuous rasp. Half
    the decay, a quarter of the hiss and a lowpass at 5 kHz takes that to
    18.1 dB and keeps the density.

    They get no `weight` either, because eight sine hits a bar at 44 Hz is
    one long smear rather than eight times the floor, and no rumble: two
    overlapping reverb tails 178 ms apart are a drone, not a pump."""
    for st in beats:
        t = s.pos(b, st)
        s.hit(t)
        k = industrialkick(tune=tune, drive=drive, decay=decay, hiss=hiss,
                           air=air, seed=(b * 4 + int(st)) % 71)
        # The second hard clip inside the kick is broadband by construction,
        # and above about 7 kHz its products are not punch - they are the
        # fizz that four or eight overlapping kicks sum into. The hats own
        # that band; the kick keeps everything under it, which is all of the
        # weight and all of the beater.
        s.place(t, lp(k, lpf if lpf else 6800), gain, 'drums')
        if rum:
            r = rumble(dur_steps=4.5, tune=tune, decay=rdecay, tone=rtone, drive=rdrive)
            s.place(t, lp(r, min(lpf * 1.6, 600)) if lpf else r, rum, 'rumble')
        if wg:
            s.place(t, weight(tune, 2.6, 0.095), wg, 'sub')
    for st in extra:
        t = s.pos(b, st)
        s.hit(t)
        s.place(t, lp(industrialkick(tune=tune * 1.02, drive=drive * 0.88,
                                     decay=decay * 0.55, hiss=0.16, air=0.18,
                                     seed=(b * 7 + int(st) * 3) % 89), 5000),
                gain * 0.76, 'drums')

def tops(b, gain=1.0, sixteenths=True, opens=(), claps=(4, 12), clapg=0.68,
         hatg=1.0):
    for st in claps:
        s.place(s.pos(b, st), distclap(2.6, drive=3.6), gain * clapg, 'drums')
    if sixteenths:
        for i in range(16):
            if i % 4 == 0:
                continue                                 # the kick owns the beat
            v = 0.64 if i % 2 else 0.34
            s.place(s.pos(b, i), metalhat(0.6, grit=0.6), gain * v * hatg * 1.15, 'drums')
    for st in opens:
        s.place(s.pos(b, st), openhat(3.0, decay=0.24, metal=0.7),
                gain * 0.60 * hatg, 'drums')

# ---- the shop ----
# Three machines. Their cycles are 6, 10 and 14 steps, so they come home
# together once every 105 bars and never inside a section. `offset` carries
# each machine's phase across the chunk boundary, and `seed` moves per chunk
# so no eleven seconds of factory is ever bit-identical to another eleven.
MACHINES = (
    dict(cycle=6.0,  note=41, tool=1180.0, whine=1870.0, pan=-0.55, motor=0.50),
    dict(cycle=10.0, note=47, tool=1720.0, whine=2640.0, pan=+0.60, motor=0.42,
         screech=1.0),
    dict(cycle=14.0, note=44, tool=830.0,  whine=1420.0, pan=-0.12, motor=0.62,
         screech=0.35, cut=0.9),
)

def shop(b0, bars, gain=1.0, which=(0, 1, 2), lvl=(1.0, 1.0, 1.0), seed=0):
    for j in which:
        m = dict(MACHINES[j])
        cyc = m.pop('cycle')
        for b in range(b0, b0 + bars, 8):
            s.place(s.pos(b),
                    mill(dur_steps=128, cycle=cyc, offset=(b * 16) % int(cyc),
                         seed=seed + b * 3 + j * 29, **m),
                    gain * lvl[j], 'shop')

def pipes(b, idx=0, gain=1.0):
    for st, note, g in PIPES[idx % len(PIPES)]:
        s.place(s.pos(b, st),
                pipe(note, 7.0, knocks=5 + (st % 3), rattle=0.75, air=0.35,
                     seed=note * 3 + b),
                gain * g, 'shop')

def plates(b, idx=0, gain=1.0):
    for st, note, g in PLATES[idx % len(PLATES)]:
        s.place(s.pos(b, st), anvil(note, 2.2, decay=0.095, bright=0.75,
                                    ring=0.5, seed=note + b), gain * g, 'shop')

def clink(b, gain=1.0, steps_=(7, 15), seed=0):
    """Filings underfoot. Short, dry and unpitched, which is the one kind of
    figure that is allowed to fall wherever it likes."""
    for st in steps_:
        s.place(s.pos(b, st), chains(2.2, density=6, seed=seed + b * 5 + st),
                gain, 'shop')

def stamp(b, gain=1.0, st=0, tune=ROOT):
    """The press. It is the record's second pulse and it lands on a beat."""
    s.place(s.pos(b, st), press(24, tune=tune, gain=1.0, seed=b % 17), gain, 'shop')

def forge(b, gain=1.0, st=0):
    s.place(s.pos(b, st), hammer(10, tune=44.0, steamy=0.7, seed=b), gain, 'shop')

# ---- the hall ----
def hall(b0, bars, grindg=1.3, sheetg=0.9, bellowg=0.0, res=1.0, crush=0,
         note=41, seed=0):
    """The room: `grind` is its tone and is tuned to the root, `sheet` is its
    top and is tuned to nothing. A bright ringing pitched thing above 3 kHz is
    a toy; an untuned one is a building. `sheetg` stays small wherever the
    drums are playing - the top of a driving section belongs to transients."""
    for b in range(b0, b0 + bars, 4):
        s.place(s.pos(b), grind(64, note=note, gain=grindg, res=res, crush=crush,
                                seed=b + seed), 1.0, 'hall')
    if sheetg:
        for b in range(b0, b0 + bars, 8):
            s.place(s.pos(b), sheet(128, gain=sheetg, seed=b + seed), 1.0, 'hall')
    if bellowg:
        for b in range(b0, b0 + bars, 8):
            s.place(s.pos(b), bellow(128, gain=bellowg, seed=b + seed), 1.0, 'hall')

def drone(b0, bars, gain=1.0, note=29, motor=0.28, seed=0):
    for b in range(b0, b0 + bars, 8):
        s.place(s.pos(b), tunnel(128, note=note, gain=gain, motor=motor,
                                 seed=b + seed), 1.0, 'hall')

# ---- the structure ----
def structure(b0, bars, f0, f1, gain=1.0, friction=0.55, drive=1.8, curve=1.0,
              seed=0, modes=6):
    """One glide across a whole section, placed on the section line. It is
    the only pitched voice on the record that sustains, and it is written as
    a gesture - a single movement from one note to another - rather than as a
    pattern of them."""
    s.place(s.pos(b0), girder(f0, f1, dur_steps=bars * 16, gain=gain, modes=modes,
                              friction=friction, drive=drive, curve=curve,
                              seed=seed), 1.0, 'struct')

# ---- bass and stabs ----
def offbeat(b, gain=1.0, cutoff=430, note=41, steps_=(2, 6, 10, 14), dur=1.9):
    """An offbeat filler for the sections the shear is NOT playing under.
    Never both: `distbass` sits on 2, 6, 10 and 14 and the bass line answers
    on 6, 10 and 14, so the two together fill every sixteenth of 60-400 Hz
    and the line stops being a line. Measured, running them together left 2%
    of the band's steps below -12 dB; the shear alone leaves 25%."""
    for st in steps_:
        s.place(s.pos(b, st), distbass(note, dur, cutoff=cutoff, drive=5.0),
                gain, 'bass')

def stabs(b, chord, gain=1.0, steps_=(6, 14), dur=1.5, drive=8.0):
    for st in steps_:
        s.place(s.pos(b, st), stab(chord, dur, drive=drive, metal=0.45),
                gain, 'shop')

def tear(b0, pat, rates, t0, t1, gain=1.0, bars=8, drive=6.0, res=3.0,
         f_hi=4200.0, body=0.55, depth=0.45, oct_=0, seed=0):
    """One shear phrase, eight bars long and rendered as one call, so the
    oscillator is continuous and the note changes glide instead of
    retriggering. `rates` is one value per bar in cycles per beat - 0.5 is a
    half-note sweep, 4 a sixteenth, 16 a sixty-fourth - and the lane
    integrates them, so a rate change accelerates a movement that is already
    running rather than starting a new one.

    No `crush`. Decimating a bass without an anti-alias filter folds
    everything above 11 kHz back down as inharmonic noise, and on the lowest
    element of the record that is not grit - it is a low frequency
    crackling."""
    p = tuple((st + 16 * k, nt + oct_, d)
              for k in range(bars) for st, nt, d in pat)
    s.place(s.pos(b0), shear(p, bars * 16, gain=gain, rates=tuple(rates),
                             tear=(t0, t1), drive=drive, res=res, f_hi=f_hi,
                             body=body, depth=depth, seed=seed), 1.0, 'shear')

# ---- the voices in the shaft ----
def choir(b0, bars, notes, gain=1.0, vowel='oh', seed=0):
    s.place(s.pos(b0), labourchoir(tuple(midi(n) for n in notes),
                                   dur_steps=bars * 16, gain=gain, vowel=vowel,
                                   size=1.35, voices=5, sag=45.0, seed=seed),
            1.0, 'voice')



# ======================= ANFAHRT  bars 0-15 =======================
# The hall before the shift. One machine idling, the ventilation, and the
# kick arriving alone at bar 8 with nothing on top of it.
hall(0, 16, grindg=1.0, sheetg=1.3, bellowg=1.0, res=0.7, note=41, seed=11)
drone(0, 16, gain=0.9, note=29, motor=0.18)
shop(0, 8, gain=0.55, which=(2,), lvl=(0, 0, 0.8), seed=101)
shop(8, 8, gain=0.75, which=(0, 2), lvl=(0.7, 0, 0.9), seed=101)
for b in range(0, 8):
    clink(b, gain=0.5, steps_=(11,), seed=3)
s.place(s.pos(3), steam(12, f0=500, f1=5200, gain=0.55), 1.0, 'fx')
s.place(s.pos(6), press(24, tune=ROOT, gain=0.45, seed=2), 1.0, 'fx')
for b in range(8, 16):
    floor(b, gain=0.92, rum=0.7 + 0.04 * (b - 8), wg=0.75)
    if b >= 12:
        tops(b, gain=0.55, sixteenths=False, claps=(), opens=(6, 14))
    clink(b, gain=0.55, steps_=(7, 15), seed=5)
# The pawl, not a spark. `servo()` is an accelerating train of 10 ms clicks
# band-passed 1800-11000 Hz, which is an arc: nothing was struck, so it has
# no body and nothing in the room answers it. Everything else in this shop is
# a struck object and this has to be one too - `ratchet()` puts its energy in
# 300-2000 Hz, where the pipes and the plates already live.
s.place(s.pos(14), ratchet(16, rate=9.0, accel=3.0, note=64, gain=0.60, seed=4),
        1.0, 'shop')

# ======================= WALZWERK  bars 16-47 =======================
# The floor, and deliberately only the floor. No stabs, no plates, no bass and
# no shear for thirty-two bars: everything this section does not have is what
# STANZE arrives with. A record whose every section owns the same instruments
# has no drops in it however the faders move.
hall(16, 32, grindg=1.35, sheetg=0.55, res=1.0, note=41, seed=23)
drone(16, 32, gain=0.85, note=29, motor=0.26)
shop(16, 16, gain=0.85, which=(0, 2), lvl=(0.8, 0, 0.9), seed=211)
shop(32, 16, gain=1.0, lvl=(0.9, 0.7, 1.0), seed=211)
structure(16, 32, ROOT, ROOT * 1.09, gain=0.50, friction=0.5, seed=31)
for b in range(16, 48):
    ph = b - 16
    last = (b == 47)
    floor(b, gain=1.0, rum=1.0, wg=0.9, beats=(0, 4, 8) if last else (0, 4, 8, 12))
    tops(b, gain=0.80 + 0.12 * (ph >= 16),
         sixteenths=ph >= 8, claps=() if last else ((4, 12) if ph >= 8 else (12,)),
         opens=(6, 14) if ph % 2 == 0 else (14,))
    pipes(b, idx=ph // 2, gain=0.70 + 0.25 * (ph >= 16))
    clink(b, gain=0.6, seed=7)
    if ph >= 24:
        offbeat(b, gain=0.42, cutoff=390, note=41)
for b in (16, 24, 32, 40):
    stamp(b, gain=0.85 if b >= 32 else 0.6)
forge(39, gain=0.7)
s.place(s.pos(44), ratchet(64, rate=5.0, accel=4.5, note=62, gain=0.62, seed=6),
        1.0, 'shop')
s.place(s.pos(45), riser(48, gain=0.5, f0=190, f1=1700), 1.0, 'fx')
s.place(s.pos(47, 8), steam(8, f0=700, f1=7600, gain=0.75, seed=3), 1.0, 'fx')

# ======================= STANZE  bars 48-79  ** DROP 1 ** ==============
# The press room, and the first time the bottom of the record changes.
# `wg` drops to a third: the shear owns the sub here, and the kick's clean
# sine gets out of its way rather than cancelling against it.
hall(48, 32, grindg=1.45, sheetg=0.5, res=1.15, crush=8, note=47, seed=37)
drone(48, 32, gain=0.8, note=30, motor=0.32)
shop(48, 32, gain=1.05, lvl=(1.0, 0.85, 0.9), seed=307)
structure(48, 32, ROOT * 1.09, TRIT, gain=0.58, friction=0.6, drive=2.0, seed=53)
tear(48, BASS_A, (0.5, 1, 1, 2, 2, 1, 4, 2), 0.12, 0.50, gain=0.88, seed=1)
tear(56, BASS_A, (1, 2, 2, 4, 2, 4, 4, 2), 0.18, 0.60, gain=0.94, seed=2)
tear(64, BASS_D, (0.5, 1, 2, 4, 2, 4, 8, 4), 0.22, 0.66, gain=0.96,
     drive=6.5, seed=3)
tear(72, BASS_B, (2, 4, 2, 8, 4, 4, 8, 4), 0.26, 0.72, gain=1.0, drive=7.0,
     seed=4)
for b in range(48, 80):
    ph = b - 48
    last = (b == 79)
    floor(b, gain=1.02, rum=1.0, wg=0.32, rdecay=0.52,
          beats=(0, 4, 8) if last else (0, 4, 8, 12),
          extra=() if last else ((14,) if ph % 4 == 3 else ((6,) if ph % 8 == 5 else ())))
    tops(b, gain=0.95, claps=() if last else (4, 12), opens=(6, 14))
    pipes(b, idx=ph // 2 + 1, gain=0.95)
    clink(b, gain=0.6, seed=9)
    if ph % 4 == 2:
        plates(b, idx=ph // 4, gain=0.6)
    if ph >= 8:
        stabs(b, STAB_A if ph % 8 < 4 else STAB_B, gain=0.52 + 0.12 * (ph >= 24))
for b in range(48, 80, 2):
    stamp(b, gain=0.95 if b >= 64 else 0.8)
forge(71, gain=0.8)
s.place(s.pos(48), alarm(48, f0=160, f1=380, cycles=1.0, gain=0.26), 1.0, 'fx')
s.place(s.pos(79, 8), downlifter(10, gain=0.6, f0=2400, f1=70), 1.0, 'fx')

# ======================= LEERLAUF  bars 80-95 =======================
# Idle. Everything the drop was made of goes: the shear, the stabs, the
# plates, the bass, the fast machines and the sixteenths. The kick stays,
# because a breakdown that takes the pulse away is not quiet, it is missing.
hall(80, 16, grindg=1.30, sheetg=1.05, bellowg=0.85, res=0.85, note=41, seed=59)
drone(80, 16, gain=0.78, note=29, motor=0.12)
shop(80, 16, gain=0.62, which=(2,), lvl=(0, 0, 0.85), seed=401)
structure(80, 16, TRIT, ROOT, gain=0.62, friction=0.75, drive=1.6, curve=1.5,
          seed=71)
choir(80, 16, (41, 48, 53, 59), gain=0.55, vowel='oh', seed=5)
for b in range(80, 96):
    ph = b - 80
    floor(b, gain=0.74, rum=0.0 if ph < 10 else 0.28, wg=0.55,
          decay=0.110, hiss=0.5, lpf=2600 if ph < 4 else None)
    if ph >= 10:
        tops(b, gain=0.40, sixteenths=ph >= 13, claps=(), opens=(14,))
    if ph % 4 == 1:
        pipes(b, idx=ph // 4, gain=0.50)
    clink(b, gain=0.40, steps_=(11,), seed=13)
s.place(s.pos(82), groan(41, 24, gain=0.42, fall=3.0, vowel='uh', seed=3), 1.0, 'voice')
s.place(s.pos(88), press(28, tune=ROOT, gain=0.45, seed=5), 1.0, 'fx')
s.place(s.pos(92), ratchet(24, rate=7.0, accel=3.4, note=64, gain=0.60, seed=8),
        1.0, 'shop')
s.place(s.pos(94), riser(32, gain=0.55, f0=200, f1=1900), 1.0, 'fx')

# ======================= HOCHOFEN  bars 96-135  ** DROP 2 ** ===========
# The furnace. Sixteen bars of groove to re-establish the floor, then the
# shear comes back at 112 with eighth-note kicks under it and does not stop
# until the tear at 136.
hall(96, 40, grindg=1.5, sheetg=0.5, res=1.2, crush=7, note=41, seed=83)
drone(96, 40, gain=0.85, note=29, motor=0.34)
shop(96, 40, gain=1.1, lvl=(1.0, 0.95, 0.85), seed=503)
structure(96, 20, ROOT, TRIT, gain=0.66, friction=0.55, drive=2.1, seed=97)
structure(116, 20, TRIT, ROOT * 1.06, gain=0.66, friction=0.68, drive=2.1, seed=113)
choir(96, 20, (41, 47, 53, 60), gain=0.40, vowel='oh', seed=9)
choir(116, 20, (42, 48, 54, 59), gain=0.44, vowel='uh', seed=11)
tear(112, BASS_B, (1, 2, 4, 2, 8, 4, 4, 8), 0.24, 0.68, gain=0.96,
     drive=6.5, seed=5)
tear(120, BASS_C, (2, 4, 8, 4, 4, 8, 8, 4), 0.30, 0.74, gain=1.0,
     drive=7.0, seed=6)
tear(128, BASS_D, (0.5, 1, 2, 4, 8, 4, 8, 8), 0.26, 0.72, gain=1.0,
     drive=7.0, seed=7)
for b in range(96, 136):
    ph = b - 96
    last = (b == 135)
    ex = ()
    if 8 <= ph < 16:
        ex = (14,) if ph % 4 == 3 else ()
    elif ph >= 16:
        ex = (14,) if ph % 4 != 3 else (6, 14)
    floor(b, gain=1.05, rum=1.0, wg=0.88 if ph < 16 else 0.30,
          rdecay=0.85 if ph < 16 else 0.52,
          beats=(0, 4, 8) if last else (0, 4, 8, 12), extra=() if last else ex)
    tops(b, gain=1.0, claps=() if last else (4, 12), opens=(6, 14),
         hatg=1.0 + 0.15 * (ph >= 24))
    pipes(b, idx=ph // 2, gain=1.0)
    clink(b, gain=0.65, seed=17)
    if ph >= 16:
        if ph < 16:                        # the shear takes over at 112
            offbeat(b, gain=0.60, cutoff=450 + 6 * ph, note=41)
        stabs(b, STAB_A if ph % 8 < 4 else STAB_B, gain=0.55, steps_=(6, 14))
    if ph % 4 == 2:
        plates(b, idx=ph // 4 + 2, gain=0.62)
for b in range(96, 136, 2):
    stamp(b, gain=0.85 if b < 112 else 1.0)
for b in (103, 119, 131):
    forge(b, gain=0.85)
s.place(s.pos(112), alarm(64, f0=155, f1=330, cycles=1.0, gain=0.30), 1.0, 'fx')
s.place(s.pos(135, 8), steam(8, f0=850, f1=8600, gain=0.7, seed=13), 1.0, 'fx')

# ======================= RISS  bars 136-151 =======================
# The tear. The floor of the record: the machines stop, the hats stop, the
# bass stops, and for eight bars there is a kick, a beam and a choir.
hall(136, 16, grindg=1.10, sheetg=1.00, bellowg=0.80, res=0.7, note=42, seed=127)
drone(136, 16, gain=0.68, note=30, motor=0.10)
shop(136, 8, gain=0.40, which=(2,), lvl=(0, 0, 0.65), seed=601)
structure(136, 16, ROOT * 1.06, TRIT * 1.03, gain=0.60, friction=0.85, drive=1.5,
          curve=1.8, modes=7, seed=131)
choir(136, 16, (41, 47, 54, 59), gain=0.52, vowel='oo', seed=13)
for b in range(136, 152):
    ph = b - 136
    floor(b, gain=0.64 + 0.02 * ph, rum=0.0 if ph < 9 else 0.30, wg=0.48,
          decay=0.100, hiss=0.42, lpf=2200 if ph < 6 else None)
    if ph >= 11:
        tops(b, gain=0.36, sixteenths=False, claps=(), opens=(14,))
    if ph >= 12 and ph % 2 == 0:
        pipes(b, idx=ph // 2, gain=0.42)
    if ph % 4 == 3:
        clink(b, gain=0.35, steps_=(11,), seed=19)
s.place(s.pos(138), groan(42, 32, gain=0.52, fall=4.0, vowel='uh', seed=7), 1.0, 'voice')
s.place(s.pos(144), screamer(20, note=54, gain=0.30, vowel='eh', drive=6.0,
                             crush=7, fall=5.0, seed=3), 1.0, 'voice')
s.place(s.pos(147), press(32, tune=ROOT * 0.94, gain=0.5, seed=9), 1.0, 'fx')

# ======================= UEBERLAST  bars 152-159 =======================
# Eight bars of overload: the machines all come back, the kicks densify bar
# by bar, the stepper motor accelerates the whole way, and the shear ramps
# from a half-note sweep to a sixty-fourth. Then the last beat is empty.
hall(152, 8, grindg=1.5, sheetg=0.9, res=1.3, crush=6, note=41, seed=149)
drone(152, 8, gain=0.9, note=29, motor=0.4)
shop(152, 8, gain=1.15, lvl=(1.0, 1.0, 1.0), seed=701)
structure(152, 8, TRIT * 1.03, ROOT * 2, gain=0.76, friction=0.7, drive=2.4,
          curve=0.7, seed=151)
tear(152, BASS_A, (0.25, 0.5, 1, 2, 4, 4, 8, 8), 0.10, 0.76, gain=1.0,
     drive=7.0, seed=8)
for b in range(152, 160):
    ph = b - 152
    last = (b == 159)
    ex = (14,) if ph >= 2 else ()
    if ph >= 5:
        ex = (6, 14)
    if last:
        ex = (2, 6, 10)
    floor(b, gain=0.92 + 0.02 * ph, rum=0.85, wg=0.34, rdecay=0.52,
          beats=(0, 4) if last else (0, 4, 8, 12), extra=ex)
    tops(b, gain=0.85, claps=() if last else (4, 12), opens=(6, 14),
         sixteenths=not last)
    pipes(b, idx=ph, gain=0.85 + 0.03 * ph)
    if ph % 2 == 0:
        plates(b, idx=ph // 2, gain=0.6)
    clink(b, gain=0.6, seed=31)
    stabs(b, STAB_B, gain=0.55 + 0.05 * ph,
          steps_=(6, 14) if ph < 4 else (2, 6, 10, 14))
for b in (153, 155, 157):
    stamp(b, gain=0.9)
s.place(s.pos(152), ratchet(96, rate=4.5, accel=5.0, note=59, gain=0.66, seed=11),
        1.0, 'shop')
s.place(s.pos(154), riser(80, gain=0.62, f0=180, f1=2400), 1.0, 'fx')
s.place(s.pos(156), alarm(64, f0=180, f1=520, cycles=1.0, gain=0.40), 1.0, 'fx')
s.place(s.pos(159, 4), steam(8, f0=900, f1=9500, gain=0.85, seed=11), 1.0, 'fx')

# ======================= ABSTICH  bars 160-215  ** THE DROP ** =========
# The tap. Fifty-six bars, the shear at full the whole way, the press on
# every bar, and the girder over the top of it. This is the record.
hall(160, 56, grindg=1.6, sheetg=0.55, res=1.3, crush=7, note=41, seed=163)
drone(160, 56, gain=0.9, note=29, motor=0.36)
shop(160, 56, gain=1.15, lvl=(1.0, 1.0, 0.95), seed=811)
structure(160, 24, ROOT * 2, TRIT, gain=0.68, friction=0.5, drive=2.3, curve=0.8,
          seed=167)
structure(184, 16, TRIT, ROOT, gain=0.70, friction=0.62, drive=2.3, seed=179)
structure(200, 16, ROOT, TRIT * 1.02, gain=0.74, friction=0.7, drive=2.4, seed=191)
choir(160, 24, (41, 47, 53, 59, 65), gain=0.42, vowel='oh', seed=17)
choir(184, 16, (42, 48, 54, 60), gain=0.46, vowel='ah', seed=19)
choir(200, 16, (41, 47, 54, 59), gain=0.48, vowel='oh', seed=23)
TEARS = ((160, BASS_B, (2, 4, 2, 8, 4, 4, 8, 4), 0.30, 0.74, 7.0),
         (168, BASS_C, (1, 2, 4, 8, 4, 8, 4, 8), 0.28, 0.76, 7.0),
         (176, BASS_D, (4, 8, 4, 8, 8, 4, 8, 8), 0.34, 0.78, 7.5),
         (184, BASS_A, (0.25, 0.5, 2, 4, 8, 4, 8, 8), 0.16, 0.72, 6.5),
         (192, BASS_C, (2, 4, 8, 4, 8, 8, 4, 8), 0.32, 0.78, 7.5),
         (200, BASS_B, (1, 2, 4, 8, 8, 4, 8, 8), 0.30, 0.80, 7.5),
         (208, BASS_C, (4, 8, 4, 8, 8, 4, 8, 8), 0.36, 0.82, 8.0))
for i, (b0, pt, rt, t0, t1, dr) in enumerate(TEARS):
    tear(b0, pt, rt, t0, t1, gain=1.0, drive=dr, seed=20 + i)
# Bars 182-183 are the re-drop: two bars stripped to the kick and the beam,
# a hole on the last beat, and then it lands again a hair louder. Fifty-six
# bars at one level is a plateau however loud the level is.
LULL = (182, 183)
for b in range(160, 216):
    ph = b - 160
    lull = b in LULL
    last = (b == 183)
    ex = (14,) if ph % 4 != 3 else (6, 14)
    if 24 <= ph < 32 or 48 <= ph < 56:
        ex = (6, 14) if ph % 4 != 3 else (2, 6, 10, 14)
    floor(b, gain=1.08, rum=1.0 if not lull else 0.45,
          wg=0.30 if not lull else 0.55, rdecay=0.50,
          beats=(0, 4, 8) if last else (0, 4, 8, 12),
          extra=() if lull else ex)
    tops(b, gain=1.05 if not lull else 0.42, claps=() if lull else (4, 12),
         opens=(6, 14) if not lull else (14,), hatg=1.15,
         sixteenths=not lull)
    if not lull:
        pipes(b, idx=ph // 2, gain=1.05)
        plates(b, idx=ph // 2, gain=0.55 if ph % 2 else 0.68)
        stabs(b, STAB_A if (ph // 4) % 2 == 0 else STAB_B, gain=0.62,
              steps_=(6, 14) if ph % 4 != 3 else (2, 6, 10, 14))
    clink(b, gain=0.7 if not lull else 0.35, seed=23)
for b in range(160, 216):
    if b in LULL:
        continue
    stamp(b, gain=1.0 if b % 2 == 0 else 0.55, st=0 if b % 2 == 0 else 8)
s.place(s.pos(183, 4), steam(8, f0=950, f1=9200, gain=0.8, seed=29), 1.0, 'fx')
for b in (167, 183, 199, 211):
    forge(b, gain=0.9)
s.place(s.pos(160), alarm(96, f0=165, f1=430, cycles=1.5, gain=0.34), 1.0, 'fx')
s.place(s.pos(192), alarm(96, f0=175, f1=500, cycles=1.5, gain=0.38), 1.0, 'fx')
s.place(s.pos(183, 8), steam(10, f0=800, f1=8200, gain=0.6, seed=17), 1.0, 'fx')
s.place(s.pos(215, 8), steam(10, f0=800, f1=8800, gain=0.7, seed=21), 1.0, 'fx')

# ======================= NACHSCHICHT  bars 216-247 =======================
# The night shift. One gear down and subtracting; the shear runs for another
# sixteen bars and then the weight comes back to the kick as it goes.
hall(216, 32, grindg=1.45, sheetg=0.7, res=1.1, note=42, seed=211)
drone(216, 32, gain=0.85, note=30, motor=0.28)
shop(216, 32, gain=1.05, lvl=(0.95, 0.8, 0.9), seed=907)
structure(216, 16, TRIT * 1.02, ROOT, gain=0.64, friction=0.6, drive=2.0, seed=223)
structure(232, 16, ROOT, ROOT * 1.12, gain=0.56, friction=0.75, drive=1.8,
          curve=1.4, seed=227)
choir(216, 16, (41, 47, 53, 59), gain=0.40, vowel='oh', seed=29)
tear(216, BASS_B, (2, 4, 8, 4, 4, 8, 8, 4), 0.32, 0.76, gain=0.95,
     drive=7.0, seed=31)
tear(224, BASS_A, (1, 2, 4, 4, 2, 4, 4, 2), 0.24, 0.62, gain=0.80,
     drive=6.5, seed=32)
for b in range(216, 248):
    ph = b - 216
    u = ph / 31
    floor(b, gain=1.03 - 0.12 * u, rum=1.0 - 0.35 * u,
          wg=0.32 if ph < 16 else 0.60 + 0.25 * u,
          rdecay=0.52 if ph < 16 else 0.85,
          extra=(14,) if ph % 4 != 3 and ph < 24 else ())
    tops(b, gain=1.0 - 0.35 * u, claps=(4, 12) if ph < 24 else (12,),
         opens=(6, 14) if ph < 16 else (14,), sixteenths=ph < 28)
    pipes(b, idx=ph // 2 + 2, gain=0.95 - 0.35 * u)
    clink(b, gain=0.65 - 0.2 * u, seed=29)
    if ph < 24:
        if ph >= 16:                       # the shear stops at 232
            offbeat(b, gain=0.60 - 0.3 * u, cutoff=440, note=41)
        stabs(b, STAB_A if ph % 8 < 4 else STAB_B, gain=0.55 - 0.25 * u)
    if ph % 4 == 2:
        plates(b, idx=ph // 4, gain=0.6 - 0.2 * u)
for b in range(216, 244, 2):
    stamp(b, gain=0.95 - 0.3 * (b - 216) / 28)
forge(231, gain=0.8)
s.place(s.pos(247, 8), downlifter(12, gain=0.6, f0=2400, f1=60), 1.0, 'fx')

# ======================= SCHICHTENDE  bars 248-255 =======================
# End of shift. The machines wind down one at a time; the ventilation is the
# last thing still running.
hall(248, 8, grindg=1.5, sheetg=1.4, bellowg=1.5, res=0.8, note=41, seed=241)
drone(248, 8, gain=1.0, note=29, motor=0.08)
shop(248, 8, gain=0.7, which=(2,), lvl=(0, 0, 0.8), seed=997)
for b in range(248, 254):
    u = (b - 248) / 5
    floor(b, gain=0.85 - 0.5 * u, rum=0.6 - 0.5 * u, wg=0.7 - 0.5 * u,
          lpf=3000 - 400 * (b - 248))
    if b < 252:
        tops(b, gain=0.45 - 0.35 * u, sixteenths=False, claps=(), opens=(14,))
s.place(s.pos(248), press(32, tune=ROOT, gain=0.55, seed=13), 1.0, 'fx')
s.place(s.pos(250), groan(41, 40, gain=0.55, fall=5.0, vowel='oh', seed=11),
        1.0, 'voice')
s.place(s.pos(252), steam(20, f0=600, f1=5000, gain=0.55, seed=27), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['shop']   = bus_reverb(s.bus['shop'],   decay=1.6, wet=0.22, tone=5400)
s.bus['fx']     = bus_reverb(s.bus['fx'],     decay=3.2, wet=0.32, tone=4600)
s.bus['hall']   = bus_reverb(s.bus['hall'],   decay=2.6, wet=0.22, tone=4200)
s.bus['struct'] = bus_reverb(s.bus['struct'], decay=3.4, wet=0.26, tone=3400)
s.bus['voice']  = bus_reverb(s.bus['voice'],  decay=3.0, wet=0.38, tone=3800)

s.bus['shop']   = hp(s.bus['shop'], 138)            # 20-138 is the kick and the line
s.bus['hall']   = hp(s.bus['hall'], 58)
s.bus['struct'] = hp(s.bus['struct'], 92)
s.bus['voice']  = hp(s.bus['voice'], 180)

# The distortion is the record, so it happens on the buses and not only in
# the voices. A wavefolder for the last stage on the shop: tanh stops making
# partials once it is flat and folding does not, which is the difference
# between a loud machine and a screaming one.
# Gentle, because the kick is already hard-clipped twice inside itself. A
# heavy bus stage on top of that is not making the kit harder, it is
# intermodulating overlapping kicks with each other, and that is heard as a
# hoarse noise rather than as drive.
s.bus['drums']  = softclip(drive_asym(s.bus['drums'], 1.22, asym=0.18), 1.02, knee=0.86)
s.bus['rumble'] = softclip(s.bus['rumble'], 1.02, knee=0.85)
s.bus['sub']    = softclip(s.bus['sub'], 1.0, knee=0.9)
s.bus['shear']  = softclip(s.bus['shear'], 1.06, knee=0.80)
s.bus['shop']   = softclip(0.80 * s.bus['shop'] + 0.20 * fold(s.bus['shop'], 1.15),
                           1.05, knee=0.8)
s.bus['bass']   = drive_asym(s.bus['bass'], 1.8, asym=0.25)

for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 170)
s.bus['shop']  = side_boost(s.bus['shop'], 520, 0.45)
s.bus['hall']  = narrow(s.bus['hall'], 0.84)

# ---- the arc ----
# Every section already has its own parts and its own gains, and that is not
# a level: a different set of loud parts is still loud. This is the ride, in
# decibels per bar. The notches before 48, 96, 160 and 184 are the holes in
# front of the drops - a gap means every bus at once, so it can only be made
# here and not in the arrangement. They are 0.17 of a bar at -10 dB, which is
# a stumble; deeper or longer than that and the hole stops reading as part of
# the beat and starts reading as the record changing volume, which is the one
# thing this whole ride exists to avoid.
ARC = [(0, -7.4), (4, -6.2), (8, -4.4), (12, -3.8), (15.9, -3.8),
       (16, -3.4), (24, -3.0), (32, -2.6), (40, -2.2), (44, -1.9),
       (47.0, -1.8), (47.80, -1.8), (47.87, -10.5), (47.99, -10.5),
       (48, -2.6), (56, -2.3), (64, -2.1), (72, -1.9), (79.4, -1.9),
       (79.7, -3.4), (79.99, -3.4),
       (80, -3.8), (86, -3.4), (90, -3.0), (93, -2.6), (95.4, -2.3),
       (95.84, -9.5), (95.99, -9.5),
       (96, -2.0), (104, -1.7), (112, -0.8), (124, -0.6), (135.4, -0.6),
       (135.84, -10.0), (135.99, -10.0),
       (136, -5.4), (140, -5.0), (144, -4.4), (148, -3.6), (151.5, -3.2),
       (152, -3.0), (154, -2.2), (156, -1.4), (158, -0.7),
       (159.6, -0.7), (159.82, -11.0), (159.99, -11.0),
       (160, -0.4), (168, -0.2), (176, -0.2), (181.9, -0.2),
       (182, -4.4), (183.4, -3.6), (183.82, -10.0), (183.99, -10.0),
       (184, 0.0), (192, 0.0), (200, 0.0), (208, 0.0), (215.9, 0.0),
       (216, -1.0), (232, -1.8), (244, -3.0), (247.9, -3.0),
       (248, -4.4), (252, -7.0), (256, -12.0)]
_bars = np.array([p[0] for p in ARC]) * BAR
_db = np.array([p[1] for p in ARC])
_ride = 10 ** (np.interp(np.arange(s.total, dtype=np.float64), _bars, _db) / 20.0)
_ride = uniform_filter1d(_ride, int(0.020 * SR))                 # no zipper
for b in s.bus:
    s.bus[b] = (s.bus[b] * _ride[:, None]).astype(np.float32)

GAINS = {'drums': 0.80, 'rumble': 0.44, 'sub': 0.32, 'bass': 0.18,
         'shear': 0.58, 'shop': 0.66, 'struct': 0.37, 'hall': 0.30,
         'voice': 0.26, 'fx': 0.30}
# Scale the sum to a known peak before the clipper, so `clip=` only ever sees
# the tip of a transient instead of doing the mixing.
_sum = sum(s.bus[k] * GAINS[k] for k in s.bus)
GAINS = {k: v * (2.00 / max(float(np.abs(_sum).max()), 1e-9)) for k, v in GAINS.items()}
del _sum

s.report(GAINS)
s.ownership(3000, 16000, GAINS, 'top  3-16k')
s.ownership(20, 120, GAINS, 'low  20-120')
s.render('industrial_walzwerk_168.wav', drive=0.70, duck=0.42, duck_rel=0.15,
         clip=1.35, peak=0.95, fade=2.4, gains=GAINS,
         brick=dict(gain=1.22, ceiling=0.89))
