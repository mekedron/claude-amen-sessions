"""TRASSA - synthwave at 116 BPM, F minor.

Trassa is the highway. This is the outrun end of the genre: four on the
floor rather than the backbeat, a sixteenth-note bass that never stops, and
a lead that holds one note for most of a bar while the chords move under it.

The palette is the 1980s rebuilt from its limitations rather than from its
recordings. `junopad` is one digitally-clocked oscillator and a square sub -
the Juno-106 could not drift and could not detune, so all of its width comes
from `bbd_chorus` afterwards, and with the chorus off the pad is thin and
ordinary. The snare is a bright reverb with no pre-delay cut off dead after
220 ms and mixed louder than the drum. The kit is real drums quantised to
eight bits and decimated with no anti-alias filter, because the aliasing is
the texture. The whole mix then goes through `cassette` - wow at half a
hertz, flutter at eight and a half, and nothing above 15.5 kHz.

The harmony is the four chords this genre is made of, i - bVI - bIII - bVII,
voiced so the top note is Ab4 for three chords running and only moves on the
fourth. A held top note recoloured by the chord underneath it is the oldest
trick in the file and it is what makes a four-chord loop bearable for four
minutes.

The tune is sixteen bars and about twenty notes. It climbs to C6 in bar 9 -
the climax, a little past the half - and comes down to the second degree of
the key, which is a note that cannot end anything, so the loop has to go
round again.

    INTRO (8) | DRIVE (8) | VERSE 1 (16) | CHORUS 1 (16) | VERSE 2 (16)
    | BREAKDOWN (16) | CHORUS 2 (16) | FINAL (24) | OUTRO (8)

128 bars, 4:25.
"""
import numpy as np
from synthlib import *

np.random.seed(1986)

# ---- the material ----
# i - bVI - bIII - bVII in F minor, voiced to hold Ab4 on top for three bars
CHORDS = [[53, 60, 65, 68],        # Fm    F3  C4  F4  Ab4
          [49, 61, 65, 68],        # Db    Db3 Db4 F4  Ab4
          [56, 60, 63, 68],        # Ab    Ab3 C4  Eb4 Ab4
          [51, 58, 63, 67]]        # Eb    Eb3 Bb3 Eb4 G4   <- the top finally moves
ROOTS = (41, 37, 44, 39)           # F2 Db2 Ab2 Eb2 - the bass anchor per bar

# The bass: sixteenths that never stop, with the octave jump this genre runs on.
# Velocity follows the metrical tier so a wall of sixteenths still has a pulse.
BVEL = {0: 1.00, 1: 0.62, 2: 0.78, 3: 0.60, 4: 0.88, 5: 0.60, 6: 0.76, 7: 0.58,
        8: 0.94, 9: 0.62, 10: 0.78, 11: 0.60, 12: 0.86, 13: 0.60, 14: 0.80, 15: 0.66}
JUMPS = {1: (7, 15), 3: (11, 14, 15)}          # which steps go up an octave, per bar

def _bassbar(bar):
    root = ROOTS[bar]
    up = JUMPS.get(bar, (15,))
    return [(bar * 16 + st, root + (12 if st in up else 0), 1.15, 1 if st == 0 else 0,
             0, BVEL[st]) for st in range(16)]

BASS = [ev for bar in range(4) for ev in _bassbar(bar)]

# The tune: sixteen bars, twenty notes, one climax. Rendered four bars at a
# time so each chunk is one unbroken oscillator and the slides really slide.
LEAD = [
    [(0, 72, 8, 1, 0), (8, 75, 6, 0, 0), (14, 77, 3, 0, 1),
     (16, 77, 10, 0, 0), (26, 75, 6, 0, 0),
     (32, 72, 8, 0, 0), (40, 70, 8, 0, 0),
     (48, 70, 12, 0, 0), (60, 72, 4, 0, 1)],
    [(0, 72, 6, 1, 0), (6, 75, 4, 0, 1), (10, 77, 6, 0, 0),
     (16, 80, 12, 1, 0), (28, 77, 4, 0, 0),
     (32, 75, 8, 0, 0), (40, 72, 8, 0, 0),
     (48, 70, 16, 0, 0)],
    [(0, 77, 6, 1, 0), (6, 80, 4, 0, 1), (10, 82, 6, 0, 0),
     (16, 84, 12, 1, 1), (28, 82, 4, 0, 0),            # C6 - the top of the record
     (32, 80, 8, 0, 0), (40, 77, 8, 0, 0),
     (48, 75, 12, 0, 0), (60, 77, 4, 0, 1)],
    [(0, 77, 8, 1, 0), (8, 75, 8, 0, 0),
     (16, 73, 12, 0, 0), (28, 72, 4, 0, 0),
     (32, 72, 8, 0, 0), (40, 68, 8, 0, 0),
     (48, 67, 16, 0, 0)],                              # the second degree: unfinished
]

# The arp runs on a seven-note cycle over a sixteen-step bar, so it starts
# somewhere new every bar and does not come back around until bar seven.
ARPS = [arp_seq([n + 12 for n in ch], bars=1, shape='updown', rate=1.0, cycle=7,
                octaves=(0, 1), gate=(1, 1, 1, 0, 1, 1, 1), accents=(0,),
                rotate=i, jitter=0.012, seed=7 + i)
        for i, ch in enumerate(CHORDS)]

TOMFILL = ((10, 57), (11, 53), (12, 50), (13, 48), (14, 45), (15, 43))

s = Session(128, tail=5.0)

# ---- the parts ----
def drums(b, gain=1.0, four=True, snare=True, hats=True, opens=(), rides=False,
          claps=True, fill=False):
    ks = (0, 4, 8, 12) if four else (0, 8)
    for st in ks:
        t = s.pos(b, st)
        s.hit(t)
        s.place(t, linnkick(tune=52.0), gain, 'drums')
    if snare:
        for st in (4, 12):
            s.place(s.pos(b, st), gatedsnare(6), gain * 0.80, 'drums')
            if claps:
                s.place(s.pos(b, st), linnclap(3), gain * 0.42, 'drums')
    if hats:
        for i in range(0, 16, 2):
            if i in opens:
                continue
            s.place(s.pos(b, i), panned(linnhat(seed=i), 0.18 if i % 4 else -0.12),
                    gain * (0.60 if i % 4 == 0 else 0.38), 'drums')
    for st in opens:
        s.place(s.pos(b, st), linnhat(open_=True, seed=st), gain * 0.44, 'drums')
    if fill:
        for st, note in TOMFILL:
            s.place(s.pos(b, st),
                    panned(simmonstom(note=note, seed=st), -0.55 + 0.22 * (st - 10)),
                    gain * (0.55 + 0.05 * (st - 10)), 'drums')

def pad(b, gain=1.0, cutoff=2600, mode=3, dur=16, attack=0.35):
    s.place(s.pos(b), junopad(([midi(n) for n in CHORDS[b % 4]]), dur,
                              cutoff=cutoff, chorus_mode=mode, attack=attack,
                              seed=b), gain, 'pad')

def arp(b, gain=1.0, decay=0.075, f_hi=6800.0, oct_=0):
    for (st, note, dur, v) in ARPS[b % 4]:
        s.place(s.pos(b, st),
                panned(retroarp(midi(int(note) + 12 * oct_), max(dur, 0.7),
                                decay=decay, f_hi=f_hi),
                       0.30 if int(st) % 2 else -0.26),
                gain * v * 0.85, 'arp')

def bass(b, gain=1.0, f_hi=3000.0):
    s.place(s.pos(b), retrobass(BASS, 4, f_hi=f_hi), gain, 'bass')

def lead(b0, idx, gain=1.0, oct_=0, f_hi=7600.0, echo=True):
    """four bars of the tune, as one oscillator"""
    pat = LEAD[idx] if not oct_ else [(st, n + 12 * oct_) + tuple(r)
                                      for (st, n, *r) in LEAD[idx]]
    seg = sawlead(pat, 4, f_hi=f_hi)
    seg = bbd_chorus(seg, mode=2, depth_ms=4.0, mix=0.42)
    s.place(s.pos(b0), seg, gain, 'lead')
    if echo:
        s.place(s.pos(b0) + int(3 * STEP), lp(seg, 3400), gain * 0.30, 'lead')

def keys(b, gain=1.0, steps_=(2, 10)):
    for st in steps_:
        for n in CHORDS[b % 4][1:]:
            s.place(s.pos(b, st), dx7ep(midi(n), 6, velocity=0.75),
                    gain * 0.34, 'keys')


# ================= INTRO  bars 0-7 =================
for b in range(0, 8):
    u = b / 7
    pad(b, gain=0.75 + 0.25 * u, cutoff=900 + 1400 * u, attack=0.9 if b == 0 else 0.35)
    if b >= 2:
        arp(b, gain=0.35 + 0.45 * u, f_hi=2600 + 3200 * u)
    if b >= 6:
        drums(b, gain=0.5, four=False, snare=False, hats=True)
s.place(s.pos(0), reverse_crash(16, gain=0.5), 1.0, 'fx')
s.place(s.pos(7), rev(crash808(12, gain=0.6)), 1.0, 'fx')

# ================= DRIVE  bars 8-15 =================
for b in range(8, 16):
    u = (b - 8) / 7
    drums(b, gain=0.85 + 0.15 * u, snare=b >= 12, claps=False,
          opens=(6, 14) if b >= 12 else ())
    pad(b, gain=0.90, cutoff=2400)
    arp(b, gain=0.80)
for b in range(8, 16, 4):
    bass(b, gain=0.7 if b < 12 else 1.0, f_hi=1500 if b < 12 else 2600)
s.place(s.pos(8), crash808(16, gain=0.45), 1.0, 'fx')

# ================= VERSE 1  bars 16-31 =================
for b in range(16, 32):
    drums(b, opens=(6, 14), fill=(b % 8 == 7))
    pad(b, gain=0.85, cutoff=2600)
    arp(b, gain=0.85)
    keys(b, gain=0.8)
for b in range(16, 32, 4):
    bass(b)
s.place(s.pos(31, 12), riser(4, gain=0.45, f0=300, f1=1600), 1.0, 'fx')

# ================= CHORUS 1  bars 32-47 =================
for b in range(32, 48):
    drums(b, opens=(2, 6, 10, 14), fill=(b % 8 == 7))
    pad(b, gain=1.0, cutoff=3400)
    arp(b, gain=0.95, f_hi=7400)
    keys(b, gain=0.6, steps_=(10,))
for b in range(32, 48, 4):
    bass(b, f_hi=3400)
for i, b in enumerate(range(32, 48, 4)):
    lead(b, i, gain=0.95)
s.place(s.pos(32), crash808(20, gain=0.65), 1.0, 'fx')
s.place(s.pos(40), crash808(16, gain=0.4), 1.0, 'fx')

# ================= VERSE 2  bars 48-63 =================
for b in range(48, 64):
    u = (b - 48) / 15
    drums(b, opens=(6, 14), fill=(b % 8 == 7))
    pad(b, gain=0.85, cutoff=2600)
    arp(b, gain=0.85, oct_=1 if b >= 56 else 0, decay=0.06)
    keys(b, gain=0.85, steps_=(2, 10, 13))
for b in range(48, 64, 4):
    bass(b)
s.place(s.pos(56), crash808(16, gain=0.35), 1.0, 'fx')
s.place(s.pos(63, 12), riser(4, gain=0.5, f0=400, f1=2200), 1.0, 'fx')

# ================= BREAKDOWN  bars 64-79 =================
# The drums leave. The pad opens, the arp thins, and the tune is played
# alone with a dotted-eighth delay under it.
for b in range(64, 80):
    ph = b - 64
    u = ph / 15
    pad(b, gain=1.0 + 0.15 * u, cutoff=1400 + 2600 * u, mode=3)
    if ph >= 4:
        arp(b, gain=0.45 + 0.35 * u, f_hi=3200 + 3600 * u)
    if ph >= 8:
        drums(b, gain=0.30 + 0.45 * (ph - 8) / 7, four=False, snare=ph >= 12,
              claps=False, hats=ph >= 10, opens=())
    if ph >= 12:
        keys(b, gain=0.5)
for i, b in enumerate(range(64, 80, 4)):
    lead(b, i, gain=0.80 + 0.06 * i, f_hi=5200 + 700 * i)
for b in (76,):
    bass(b, gain=0.6, f_hi=1600)
s.place(s.pos(64), rev(crash808(20, gain=0.7)), 1.0, 'fx')
s.place(s.pos(64), impact(24, gain=0.35), 1.0, 'fx')
s.place(s.pos(72), wind(64, gain=0.35), 1.0, 'air')
s.place(s.pos(78), riser(32, gain=0.55, f0=260, f1=2400), 1.0, 'fx')

# ================= CHORUS 2  bars 80-95 =================
for b in range(80, 96):
    drums(b, opens=(2, 6, 10, 14), fill=(b % 8 == 7))
    pad(b, gain=1.05, cutoff=3600)
    arp(b, gain=1.0, f_hi=7600)
    keys(b, gain=0.65, steps_=(10,))
for b in range(80, 96, 4):
    bass(b, f_hi=3600)
for i, b in enumerate(range(80, 96, 4)):
    lead(b, i, gain=1.0)
s.place(s.pos(80), crash808(20, gain=0.7), 1.0, 'fx')
s.place(s.pos(88), crash808(16, gain=0.4), 1.0, 'fx')

# ================= FINAL  bars 96-119 =================
# The last chorus is the biggest one: the tune doubled an octave down, the
# arp an octave up, and open hats on every offbeat.
for b in range(96, 120):
    drums(b, opens=(2, 6, 10, 14), fill=(b % 8 == 7))
    pad(b, gain=1.10, cutoff=3800)
    arp(b, gain=1.0, oct_=1, f_hi=8000)
    keys(b, gain=0.7, steps_=(2, 10))
for b in range(96, 120, 4):
    bass(b, f_hi=3800)
for i, b in enumerate(range(96, 112, 4)):
    lead(b, i, gain=1.0)
    lead(b, i, gain=0.42, oct_=-1, f_hi=4200, echo=False)   # the octave double
for i, b in enumerate(range(112, 120, 4)):
    lead(b, i + 2, gain=1.0)
    lead(b, i + 2, gain=0.42, oct_=-1, f_hi=4200, echo=False)
s.place(s.pos(96), crash808(24, gain=0.8), 1.0, 'fx')
s.place(s.pos(112), crash808(20, gain=0.55), 1.0, 'fx')

# ================= OUTRO  bars 120-127 =================
for b in range(120, 128):
    ph = b - 120
    u = ph / 7
    drums(b, gain=1.0 - 0.8 * u, snare=ph < 5, hats=ph < 6,
          opens=(6, 14) if ph < 4 else (), claps=False, fill=(ph == 3))
    pad(b, gain=1.05 - 0.15 * u, cutoff=3400 - 1800 * u)
    if ph < 5:
        arp(b, gain=0.9 - 0.18 * ph, f_hi=7000 - 900 * ph)
for b in (120,):
    bass(b, gain=0.85)
s.place(s.pos(124), junopad([midi(n) for n in CHORDS[0]], 48, cutoff=1500,
                            attack=1.4, seed=99), 0.9, 'pad')
s.place(s.pos(127, 8), rev(crash808(10, gain=0.3)), 1.0, 'fx')

# ---- bus space, then the master ----
s.bus['lead']  = bus_reverb(s.bus['lead'],  decay=2.4, wet=0.26, tone=5200)
s.bus['arp']   = bus_reverb(s.bus['arp'],   decay=1.6, wet=0.22, tone=5800)
s.bus['pad']   = bus_reverb(s.bus['pad'],   decay=3.6, wet=0.30, tone=4200)
s.bus['keys']  = bus_reverb(s.bus['keys'],  decay=2.0, wet=0.28, tone=5000)
s.bus['drums'] = bus_reverb(s.bus['drums'], decay=0.7, wet=0.10, tone=6000)
s.bus['fx']    = bus_reverb(s.bus['fx'],    decay=3.2, wet=0.32, tone=4600)

s.bus['pad']  = hp(s.bus['pad'], 128, order=2)   # Db3/Eb3 are the pad's floor
s.bus['arp']  = hp(s.bus['arp'], 300, order=2)
s.bus['lead'] = hp(s.bus['lead'], 280, order=2)
s.bus['keys'] = hp(s.bus['keys'], 200, order=2)
s.bus['fx']   = hp(s.bus['fx'], 60)

s.bus['drums'] = squash(s.bus['drums'], thresh=0.34, ratio=2.8, attack=0.018,
                        release=0.129, mix=0.6, makeup=1.15, report='drums')
s.bus['bass']  = squash(s.bus['bass'], thresh=0.34, ratio=3.4, attack=0.008,
                        release=0.129, report='bass')

for b in s.bus:
    s.bus[b] = mono_below(s.bus[b], 140)

GAINS = {'drums': 0.98, 'bass': 0.44, 'pad': 2.05, 'arp': 1.55, 'lead': 1.00,
         'keys': 1.45, 'fx': 0.60, 'air': 0.55}
s.report(GAINS)

# The whole record went through one machine, so the tape goes on the master
# rather than on any voice. Mastered gently on purpose: this decade did not
# sound loud, and a synthwave track squeezed to a modern number stops sounding
# like the thing it is imitating.
mix = s.mixdown(drive=0.45, duck=0.30, limit=0.0, peak=0.90, gains=GAINS,
                clip=1.50, duck_rel=0.20)
mix = cassette(mix, hiss=0.0014, wow_ms=1.0, flutter_ms=0.26, top=15500, sat=1.2)
mix = limiter(mix, 0.93, report=True)
mix = mix * (0.93 / max(float(np.abs(mix).max()), 1e-9))
fi = int(0.01 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(3.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
import os
save(os.path.join(RENDERS, 'synth_trassa_116.wav'), mix)
print(f"synth_trassa_116.wav: {len(mix)/SR:.2f}s rms={np.sqrt((mix**2).mean()):.3f}")
