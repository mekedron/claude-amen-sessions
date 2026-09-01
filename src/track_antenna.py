"""Antenna (~3:25, 136 bars @164) - post-punk / new wave, A minor.

The third punk record, and the corner the first two never visited: the cold
end of the genre - Manchester 1979 crossed with the German new wave. The
band is the same (two rhythm takes hard panned, a bass, an acoustic kit) but
the roles flip: the BASS carries the tune the way Peter Hook played it, high
on the neck and melodic, the wall answers it, and a one-oscillator synth
doubles the chorus hook the way every 1983 radio record did.

Three different guitars at once, and none of them is a copy of another:
  * the wall     - humbucker into a driven amp, one continuous take per
                   phrase through one amp pass (`riff`), double tracked
  * the shimmer  - single coil on the edge of break-up through a chorus
                   pedal (`jangle`), arpeggios and octaves, always ringing
  * the lead     - one string, more gain, vibrato (`solo`)

  b0-3     static, mains hum, and the bass states the hook alone
  b4-11    THE RIFF: full band - open A5 eighths, the push onto F, G,
           and a single-note turnaround C-B-G-E
  b12-27   verse 1: palm-muted eighths and floor toms, the bass sings,
           the shimmer guitar rains arpeggios over it
  b28-35   pre-chorus: the wall climbs D-F-G and hangs on E major
  b36-51   chorus 1: F-G-Am anthem, lead tune doubled by the synth
  b52-59   the riff again
  b60-71   verse 2, d-beat, lead answers in the gaps
  b72-79   pre-chorus 2
  b80-95   chorus 2, octave lead
  b96-103  bridge: distortion off - clean chords, shimmer, one Juno pad,
           half-time drums. The cold room the genre lives in.
  b104-111 build: the mutes creep back, snare climbing, one rising line
  b112-127 last chorus: gang "oh"s, synth answering, crashes every 2
  b128-131 the riff, last time
  b132-135 outro: one chord left ringing into feedback and hum
"""
import numpy as np
from punklib import *
import synthlib                                 # imports at 116 BPM; fixed below

BAR, STEP = set_tempo(164)                      # rebind the grid for everyone
rng = np.random.default_rng(23)
np.random.seed(23)
s = Session(136, tail=3.5)

# ---- the harmony -------------------------------------------------------
# A minor, Aeolian, with E major borrowed from the harmonic minor at the two
# places the music has to pull home. Power chords stay ambiguous; the bass
# and the lead decide.
Am, F, G, C, E_LO = 45, 41, 43, 48, 40          # wall roots (A2, F2, G2, C3, E2)
Dm3, F3, G3, E3 = 50, 53, 55, 52                # pre-chorus climbs an octave up

CHORUS = [F, G, Am, Am]                          # VI VII i - the anthem cadence
VERSE  = [Am, Am, F, G, Am, Am, F, E_LO]
PRE    = [Dm3, Dm3, F3, F3, G3, G3, E3, E3]      # iv VI VII V, rising
BRIDGE = [Am, F, Dm3, E3]

def ch(prog, b, b0):  return prog[(b - b0) % len(prog)]

SPREAD = 0.88
SLIP = int(0.0034 * SR)
E8 = list(range(0, 16, 2))

# ---- the wall: continuous phrase takes ---------------------------------
# Amp settings for the whole record: hotter than Grip Tape, tighter than
# Curbside. `riff()` renders each 4-bar phrase as one performance through
# one amp pass - ringing, chokes, restrikes, scrapes, hiss and all.
WK = dict(gain=21.0, heavy=0.22, presence=1.6, push=0.8)

def wall_phrase(b0, events, bars=4, gain=1.0, **kw):
    kw = dict(WK, **kw)
    t = s.pos(b0)
    k = (b0 // 4) % 3
    s.place(t, panned(riff(tuple(events), bars=bars, take=k, **kw), -SPREAD),
            gain, 'gtr')
    s.place(t + SLIP, panned(riff(tuple(events), bars=bars, take=10 + k, **kw),
                             SPREAD), gain * 0.98, 'gtr')

# The main riff, 4 bars. Restruck eighths that ring into each other, the
# change to F pushed one eighth early, and a single-note turnaround - the
# things a hand does that a chord sequencer cannot.
RIFF_A = ([(st, Am, 2, 'chord') for st in E8] +
          [(16 + st, Am, 2, 'chord') for st in range(0, 14, 2)] +
          [(30, F, 2, 'chord')] +                                # the push
          [(32 + st, F, 2, 'chord') for st in range(0, 8, 2)] +
          [(40 + st, G, 2, 'chord') for st in range(0, 8, 2)] +
          [(48, Am, 8, 'chord'),                                 # let it ring...
           (56, 48, 2, 'note'), (58, 47, 2, 'note'),             # ...then C B
           (60, 43, 2, 'note'), (62, 40, 2, 'note')])            # G E, home

# Chorus wall: F G Am, eighths, the arrival on Am pushed early.
CHOR_W = ([(st, F, 2, 'chord') for st in E8] +
          [(16 + st, G, 2, 'chord') for st in range(0, 14, 2)] +
          [(30, Am, 2, 'chord')] +
          [(32 + st, Am, 2, 'chord') for st in E8] +
          [(48, Am, 4, 'chord'), (52, Am, 4, 'chord'), (56, Am, 8, 'chord')])

# Pre-chorus: half-note chords first, eighths once it has to climb.
PRE_W1 = [(st, r, 8, 'chord') for i, r in enumerate((Dm3, Dm3, F3, F3))
          for st in (i * 16, i * 16 + 8)]
PRE_W2 = ([(st, G3, 2, 'chord') for st in E8] +
          [(16 + st, G3, 2, 'chord') for st in E8] +
          [(32 + st, E3, 2, 'chord') for st in E8] +
          [(48, E3, 2, 'chord'), (50, E3, 2, 'chord'),
           (52, E3, 4, 'chord'), (56, E3, 8, 'chord')])

# Verse: palm-muted eighths with an octave stab pushed onto every change.
def verse_m(c1, c2, c3, c4, stab3=True):
    ev = ([(st, c1, 2, 'mute') for st in E8] +
          [(16 + st, c2, 2, 'mute') for st in range(0, 14, 2)] +
          [(30, c3, 4, 'oct')] +                                 # the stab
          [(32 + st, c3, 2, 'mute') for st in E8] +
          [(48 + st, c4, 2, 'mute') for st in range(0, 12, 2)])
    ev += [(60, c4, 4, 'chord')] if stab3 else [(60 + st, c4, 2, 'mute')
                                                for st in (0, 2)]
    return ev

VERSE_M1 = verse_m(Am, Am, F, G)
VERSE_M2 = verse_m(Am, Am, F, E_LO)

# The build: the same mutes, thinning out of the rests bar by bar.
def build_m(density):
    steps_ = E8[:2 * density] if density < 4 else E8
    return [(b16 + st, Am, 2, 'mute') for b16 in (0, 16, 32, 48)
            for st in steps_]

# ---- the shimmer guitar ------------------------------------------------
JPAN = 0.42

def arp_bar(notes, order=(0, 1, 2, 3, 2, 1, 2, 3)):
    return [(st, notes[order[i]], 2, 'note') for i, st in enumerate(E8)]

ARPS = {Am:   (57, 64, 69, 72),                 # A3 E4 A4 C5
        F:    (53, 60, 65, 69),                 # F3 C4 F4 A4
        G:    (55, 62, 67, 71),                 # G3 D4 G4 B4
        E_LO: (52, 59, 64, 68),                 # E3 B3 E4 G#4 - the V lights up
        Dm3:  (50, 57, 62, 65),                 # D3 A3 D4 F4
        E3:   (52, 59, 64, 68)}

def shimmer_arps(b0, roots, take=0, gain=0.9, level=1.0):
    ev = []
    for i, r in enumerate(roots):
        ev += [(16 * i + st, n, ln, k) for st, n, ln, k in arp_bar(ARPS[r])]
    s.place(s.pos(b0), panned(jangle(tuple(ev), bars=len(roots), take=take),
                              JPAN), gain * level, 'jangle')

# Chorus octaves: the high two-string line riding the changes - the other
# guitarist refusing to play the same part as the first one.
OCT_W = [(0, 65, 4, 'oct'), (6, 65, 2, 'oct'), (8, 65, 4, 'oct'), (12, 65, 4, 'oct'),
         (16, 67, 4, 'oct'), (22, 67, 2, 'oct'), (24, 67, 4, 'oct'), (28, 67, 4, 'oct'),
         (32, 69, 4, 'oct'), (38, 69, 2, 'oct'), (40, 69, 4, 'oct'), (44, 69, 4, 'oct'),
         (48, 72, 4, 'oct'), (52, 71, 2, 'oct'), (54, 69, 10, 'oct')]

def shimmer_oct(b0, take=0, gain=0.85):
    s.place(s.pos(b0), panned(jangle(tuple(OCT_W), bars=4, take=take, drive=2.6),
                              JPAN), gain, 'jangle')

# ---- the lead ----------------------------------------------------------
def sing(events, gain=0.6, bus='lead', pan=-0.2, oct_=False, ring=1.2, arc=True):
    """(bar, step, note, length[, bend]) - loudness follows the contour."""
    notes = [e[2] for e in events]
    lo, hi = min(notes), max(notes)
    for ev in events:
        b, st, note, ln = ev[:4]
        bend = ev[4] if len(ev) > 4 else 0.0
        v = 1.0
        if arc:
            v = 0.72 + 0.28 * ((note - lo) / max(hi - lo, 1))
            v *= 1.08 if st % 4 == 0 else 0.94
        seg = solo(note, ln + ring, take=(b + int(st)) % 3, bend=bend)
        s.place(s.pos(b, st), panned(seg, pan), gain * min(v, 1.05), bus)
        if oct_:
            s.place(s.pos(b, st) + 90,
                    panned(solo(note - 12, ln + ring, take=(b + 1) % 3, bend=bend),
                           -pan * 0.5), gain * v * 0.5, bus)

# The chorus tune: an arch over F G Am, written to be sung. Starts on the
# sixth of F, climbs through the third of G, lands home on A, and holds the
# fifth for a whole bar at the top.
TUNE = [(0, 69, 4), (4, 72, 2), (6, 74, 8),
        (16, 74, 4), (20, 72, 2), (22, 71, 6), (28, 72, 2), (30, 74, 2),
        (32, 69, 8), (40, 72, 4), (44, 74, 4),
        (48, 76, 12), (60, 74, 2), (62, 72, 2)]
TUNE_LIFT = [(48, 77, 8, 0.3), (56, 76, 8)]      # pass two climbs past pass one

def topline(b0, gain=0.6, oct_=False, lift=False, pan=-0.2):
    tune = ([e for e in TUNE if e[0] < 48] + TUNE_LIFT) if lift else TUNE
    sing([(b0 + e[0] // 16, e[0] % 16) + tuple(e[1:]) for e in tune],
         gain=gain, oct_=oct_, pan=pan)

# ---- the synth ---------------------------------------------------------
# One saw doubling the tune, and a Juno pad under the chords: the 1983 move.
def synth_tune(b0, gain=0.30, lift=False, oct_up=0):
    tune = ([e for e in TUNE if e[0] < 48] + TUNE_LIFT) if lift else TUNE
    pat = [(e[0], e[1] + oct_up, e[2] * 0.92, e[0] % 8 == 0, False)
           for e in tune]
    seg = synthlib.sawlead(tuple(pat), dur_bars=4)
    s.place(s.pos(b0), widen(seg, 0.7), gain, 'synth')

PADS = {F:  (53, 57, 60, 65), G: (55, 59, 62, 67), Am: (57, 60, 64, 69),
        Dm3: (50, 53, 57, 62), F3: (53, 57, 60, 65), G3: (55, 59, 62, 67),
        E3: (52, 56, 59, 64), E_LO: (52, 56, 59, 64)}

def pad(b, root, gain=0.5, cutoff=2200, attack=0.30):
    freqs = tuple(midi(m) for m in PADS[root])
    s.place(s.pos(b), synthlib.junopad(freqs, 17, cutoff=cutoff, attack=attack,
                                       release=0.5, seed=b % 7), gain, 'synth')

# ---- the bass ----------------------------------------------------------
# The tune-carrier. Root eighths would be Grip Tape; this record walks high
# on the neck the way Hook played - the melody lives an octave over the
# root and comes back down for the changes.
BASSV = {
    Am:   ((0, 33), (2, 33), (4, 33), (6, 33), (8, 40), (10, 43), (12, 45), (14, 43)),
    F:    ((0, 29), (2, 29), (4, 29), (6, 29), (8, 36), (10, 33), (12, 29), (14, 31)),
    G:    ((0, 31), (2, 31), (4, 31), (6, 31), (8, 38), (10, 35), (12, 31), (14, 33)),
    E_LO: ((0, 28), (2, 28), (4, 28), (6, 28), (8, 40), (10, 39), (12, 35), (14, 33)),
}
BASSV2 = dict(BASSV)                             # the second Am bar answers down
BASSV2[Am] = ((0, 33), (2, 33), (4, 33), (6, 33), (8, 45), (10, 43), (12, 40), (14, 36))

def bass_verse(b, root, alt=False, gain=0.95):
    evs = (BASSV2 if alt else BASSV)[root]
    s.place(s.pos(b), bassbar(evs, take=b % 3, drive=2.2, bright=1.15), gain, 'bass')

def bass_eighths(b, root, walk_to=None, octpop=False, gain=0.95):
    note = root - 12
    evs = [(st, note) for st in E8]
    if octpop:                                   # the high answer inside the bar
        evs[2] = (4, note + 12); evs[5] = (10, note + 12)
    if walk_to is not None:
        tgt = walk_to - 12
        d = 1 if tgt > note else -1
        evs = [e for e in evs if e[0] < 12] + [(12, tgt - 2 * d), (14, tgt - d)]
    s.place(s.pos(b), bassbar(tuple(evs), take=b % 3, drive=2.2), gain, 'bass')

# The hook, stated by the bass alone before anything else moves.
BASS_RIFF = [((0, 33), (2, 33), (4, 33), (6, 33), (8, 33), (10, 33), (12, 33), (14, 33)),
             ((0, 33), (2, 33), (4, 33), (6, 33), (8, 33), (10, 33), (12, 33), (14, 29)),
             ((0, 29), (2, 29), (4, 29), (6, 29), (8, 31), (10, 31), (12, 31), (14, 31)),
             ((0, 33), (2, 33), (4, 33), (6, 33), (8, 36), (10, 35), (12, 31), (14, 28))]

def bass_riff(b0, gain=0.95):
    for i, evs in enumerate(BASS_RIFF):
        s.place(s.pos(b0 + i), bassbar(evs, take=(b0 + i) % 3, drive=2.2,
                                       bright=1.1), gain, 'bass')

# ---- drums -------------------------------------------------------------
def hats(b, open_at=(), gain=0.9, rate=2):
    for st in range(0, 16, rate):
        o = st in open_at
        v = gain * (1.0 if st % 4 == 0 else 0.62 + 0.08 * rng.random())
        s.place(s.pos(b, st) + int(rng.integers(-70, 70)),
                phat(1.4 if o else 1, open_=o, seed=(st + b) % 5),
                v * (1.15 if o else 1), 'drums')

def kicks(b, pat, gain=1.0):
    for st in pat:
        s.place(s.pos(b, st) + int(rng.integers(-25, 25)),
                pkick(seed=(int(st) + b) % 4, tune=59.0),
                gain * (1.0 if st == 0 else 0.94), 'drums')

def snares(b, pat=(4, 12), gain=1.0, ghost=()):
    for st in pat:
        s.place(s.pos(b, st) + int(0.0025 * SR) + int(rng.integers(-60, 60)),
                psnare(seed=(int(st) + b) % 5, tune=192.0),
                gain * (0.97 + 0.06 * rng.random()), 'drums')
    for st in ghost:
        s.place(s.pos(b, st), psnare(2, seed=2), gain * 0.20, 'drums')

def beat(b, kind, crash=False, gain=1.0):
    # A kick on every beat in every pattern that is not deliberately empty -
    # the felt pulse is the rate of the low-band events, and 164 played on
    # 1 and 3 would feel like 82.
    if kind == 'punk':
        kicks(b, (0, 4, 8, 12)); snares(b); hats(b, gain=0.85 * gain)
    elif kind == 'toms':                          # the Morris verse: floor toms
        kicks(b, (0, 4, 8, 12)); snares(b)        # rolling under the backbeat
        for st, tune in ((2, 112), (6, 138), (10, 112), (14, 138)):
            s.place(s.pos(b, st) + int(rng.integers(-40, 40)),
                    ptom(2, tune=tune, seed=(st + b) % 3), 0.42 * gain, 'drums')
        hats(b, gain=0.5 * gain)
    elif kind == 'dbeat':
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b); hats(b, gain=0.85 * gain)
    elif kind == 'open':
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b)
        hats(b, open_at=(2, 6, 10, 14), gain=0.7 * gain)
    elif kind == 'chorus':                        # ride, driving
        kicks(b, (0, 3, 4, 8, 11, 12)); snares(b, ghost=(7,) if b % 2 else ())
        for st in range(0, 16, 2):
            s.place(s.pos(b, st) + int(rng.integers(-70, 70)),
                    pride(2, seed=(st + b) % 4),
                    (0.95 if st % 4 == 0 else 0.62) * gain, 'drums')
    elif kind == 'skank':
        kicks(b, (0, 4, 8, 12)); snares(b, (2, 6, 10, 14), gain=0.8)
        hats(b, gain=0.8 * gain)
    elif kind == 'half':                          # the bridge: a wider pulse,
        kicks(b, (0, 8)); snares(b, (8,), gain=0.85)   # never a missing one
        for st in range(0, 16, 2):
            s.place(s.pos(b, st), pride(2, seed=st % 3),
                    (0.8 if st % 4 == 0 else 0.5) * gain, 'drums')
    if crash:
        s.place(s.pos(b), pcrash(24, seed=b % 3), 0.55 * gain, 'drums')

def fill(b, kind='toms'):
    if kind == 'toms':
        kicks(b, (0, 4, 8)); snares(b, (4,))
        for i, (st, tune) in enumerate(((8, 200), (9, 200), (10, 160), (11, 160),
                                        (12, 128), (13, 128), (14, 100), (15, 100))):
            s.place(s.pos(b, st), ptom(2, tune=tune), 0.65 + 0.05 * i, 'drums')
    elif kind == 'snare':
        kicks(b, (0,))
        for i, st in enumerate(range(0, 16)):
            s.place(s.pos(b, st), psnare(2, seed=i % 3), 0.42 + 0.045 * i, 'drums')
    elif kind == 'roll32':
        kicks(b, (0,))
        for i in range(16):
            s.place(s.pos(b, 8 + i * 0.5), psnare(1.5, seed=i % 3),
                    0.45 + 0.035 * i, 'drums')
        snares(b, (4,))

# ================= b0-3: static, hum, the bass alone =================
# A record called Antenna opens with what an antenna hears: mains hum and
# the space between stations, and the first instrument tunes in out of it.
_n, _t = steps(64)
hum = stereo(np.sin(2 * np.pi * 50 * _t) + 0.35 * np.sin(2 * np.pi * 150 * _t)
             + 0.15 * np.sin(2 * np.pi * 100 * _t))
hum = hum * (0.05 * np.minimum(_t / 0.5, 1.0))[:, None]
static = hp(stereo(np.random.randn(_n)), 2600) * 0.030
static *= (np.exp(-_t / 2.6) * (1 + 0.6 * np.sin(2 * np.pi * 0.4 * _t)))[:, None]
s.place(s.pos(0), hum + static, 1.0, 'gtr')
bass_riff(0, gain=0.9)
for b in (2, 3):
    kicks(b, (0, 4, 8, 12), gain=0.55 + 0.2 * (b - 2))
    hats(b, gain=0.5 + 0.15 * (b - 2))
s.place(s.pos(3, 12), psnare(1.2, seed=1, rim=1.2), 0.4, 'drums')
s.place(s.pos(3, 14), psnare(1.2, seed=2, rim=1.2), 0.5, 'drums')

# ================= b4-11: THE RIFF =================
for k in range(2):
    b0 = 4 + 4 * k
    wall_phrase(b0, RIFF_A)
    bass_riff(b0)
for b in range(4, 12):
    beat(b, 'punk' if b < 8 else 'open', crash=(b in (4, 8)))
fill(11, 'toms')
shimmer_oct(8, take=1, gain=0.6)                 # the second guitar leans in

# ================= b12-27: verse 1 =================
for k, phr in ((0, VERSE_M1), (1, VERSE_M2), (2, VERSE_M1), (3, VERSE_M2)):
    wall_phrase(12 + 4 * k, phr, gain=0.9)
for i, b in enumerate(range(12, 28)):
    root = ch(VERSE, b, 12)
    bass_verse(b, root, alt=(i % 8 in (4, 5)))
    beat(b, 'toms' if b < 20 else 'punk', crash=(b in (12, 20)))
if True:
    shimmer_arps(12, (Am, Am, F, G), take=0)
    shimmer_arps(16, (Am, Am, F, E_LO), take=1)
    shimmer_arps(20, (Am, Am, F, G), take=2)
    shimmer_arps(24, (Am, Am, F, E_LO), take=3)
fill(19, 'toms')
fill(27, 'snare')
# the lead answers in the holes, low and restrained
sing([(17, 8, 72, 4), (17, 12, 71, 4), (18, 0, 69, 10),
      (25, 8, 71, 4), (25, 12, 72, 4), (26, 0, 74, 8), (26, 8, 76, 6, 0.3)],
     gain=0.34, pan=0.25)

# ================= b28-35: pre-chorus =================
wall_phrase(28, PRE_W1, gain=0.92)
wall_phrase(32, PRE_W2, gain=0.95)
for b in range(28, 36):
    root = ch(PRE, b, 28)
    bass_eighths(b, root - 12 if root > 47 else root)     # the bass climbs too
    pad(b, root, gain=0.62, cutoff=1900, attack=0.4)
    beat(b, 'open' if b < 32 else 'skank', crash=(b == 28))
fill(34, 'roll32')
s.bus['drums'][s.pos(35):s.pos(36)] *= 0.0        # the bar before the anthem
for i in range(8):
    s.place(s.pos(35, 8 + i), psnare(1.5, seed=i % 3), 0.55 + 0.05 * i, 'drums')
s.place(s.pos(35, 15.4), psnare(1, seed=1), 1.0, 'drums')
s.place(s.pos(36) - int(0.9 * SR), rev(pcrash(20, seed=2)), 0.5, 'drums')

# ================= chorus machine =================
def chorus_section(b0, bars=16, kind='chorus', gang_=False, oct_=False,
                   crash_every=4, mel=0.62, synth_gain=0.55):
    for k in range(bars // 4):
        wall_phrase(b0 + 4 * k, CHOR_W)
        shimmer_oct(b0 + 4 * k, take=k % 3, gain=0.92)
        topline(b0 + 4 * k, gain=mel, oct_=oct_, lift=(k % 2 == 1))
        synth_tune(b0 + 4 * k, gain=synth_gain, lift=(k % 2 == 1))
    for b in range(b0, b0 + bars):
        root = ch(CHORUS, b, b0)
        nxt = ch(CHORUS, b + 1, b0)
        bass_eighths(b, root, walk_to=nxt if (b - b0) % 4 == 3 else None,
                     octpop=(root == Am))
        pad(b, root, gain=0.50, cutoff=2400)
        beat(b, kind, crash=((b - b0) % crash_every == 0))
        if (b - b0) % 8 == 7 and b - b0 < bars - 1:
            fill(b, 'toms')
    if gang_:
        for k in range(bars // 4):
            for i, note in enumerate((65, 67, 69)):
                s.place(s.pos(b0 + 4 * k + i, 0.4),
                        gang(note, 14, vowel='oh', seed=i + k, rasp=0.3),
                        0.34, 'gang')

# ================= b36-51: chorus 1 =================
chorus_section(36, 16, mel=0.66, synth_gain=0.55)

# ================= b52-59: the riff =================
for k in range(2):
    wall_phrase(52 + 4 * k, RIFF_A)
    bass_riff(52 + 4 * k)
for b in range(52, 60):
    beat(b, 'dbeat', crash=(b == 52))
shimmer_oct(56, take=2, gain=0.6)
fill(59, 'toms')

# ================= b60-71: verse 2 =================
for k, phr in ((0, VERSE_M1), (1, VERSE_M2), (2, VERSE_M1)):
    wall_phrase(60 + 4 * k, phr, gain=0.9)
for i, b in enumerate(range(60, 72)):
    root = ch(VERSE, b, 60)
    bass_verse(b, root, alt=(i % 8 in (4, 5)))
    beat(b, 'dbeat' if b < 68 else 'skank', crash=(b == 60))
shimmer_arps(60, (Am, Am, F, G), take=4)
shimmer_arps(64, (Am, Am, F, E_LO), take=5)
shimmer_arps(68, (Am, Am, F, G), take=6)
fill(67, 'toms')
fill(71, 'snare')
sing([(62, 8, 74, 4), (62, 12, 72, 4), (63, 0, 71, 10),
      (65, 8, 76, 4), (65, 12, 77, 4), (66, 0, 76, 8), (66, 8, 74, 6),
      (69, 8, 71, 4), (69, 12, 72, 4), (70, 0, 74, 12, 0.3)],
     gain=0.36, pan=0.3)

# ================= b72-79: pre-chorus 2 =================
wall_phrase(72, PRE_W1, gain=0.92)
wall_phrase(76, PRE_W2, gain=0.95)
for b in range(72, 80):
    root = ch(PRE, b, 72)
    bass_eighths(b, root - 12 if root > 47 else root)
    pad(b, root, gain=0.66, cutoff=2000, attack=0.4)
    beat(b, 'open' if b < 76 else 'skank', crash=(b == 72))
fill(78, 'roll32')
s.bus['drums'][s.pos(79):s.pos(80)] *= 0.0
for i in range(12):
    s.place(s.pos(79, 4 + i), psnare(1.5, seed=i % 3), 0.5 + 0.04 * i, 'drums')
s.place(s.pos(79, 15.4), psnare(1, seed=1), 1.0, 'drums')

# ================= b80-95: chorus 2 =================
chorus_section(80, 16, oct_=True, synth_gain=0.60)

# ================= b96-103: bridge =================
# The wall goes away and the cold room is what is left: clean chords, the
# shimmer guitar, one pad, and a pulse that never actually stops.
s.place(s.pos(96), pcrash(40, seed=1), 0.5, 'drums')
for b in range(96, 104):
    root = ch(BRIDGE, b, 96)
    shape = 'min' if root in (Am, Dm3) else 'maj'
    s.place(s.pos(b), panned(clean(root, 16, shape, take=b % 3), -0.4),
            0.5, 'gtr')
    bass_eighths(b, root if root < 48 else root - 12, gain=0.7)
    pad(b, root, gain=0.85, cutoff=1700, attack=0.5)
    beat(b, 'half', gain=0.8)
BR_ARP = {Am: ARPS[Am], F: ARPS[F], Dm3: ARPS[Dm3], E3: ARPS[E3]}
shimmer_arps(96, (Am, F, Dm3, E3), take=7, gain=1.0)
shimmer_arps(100, (Am, F, Dm3, E3), take=8, gain=1.0)
sing([(97, 8, 69, 8), (98, 0, 72, 8), (98, 8, 74, 8), (99, 8, 76, 10),
      (101, 8, 74, 4), (101, 12, 72, 4), (102, 0, 71, 8), (102, 8, 68, 14, 0.4)],
     gain=0.4, pan=0.15)

# ================= b104-111: the build =================
for k in range(2):
    wall_phrase(104 + 4 * k, build_m(1 + 2 * k), gain=0.55 + 0.25 * k)
for i, b in enumerate(range(104, 112)):
    bass_eighths(b, Am, octpop=(i >= 4))
    kicks(b, (0, 4, 8, 12))
    if i < 4:
        snares(b, (12,), gain=0.7)
        hats(b, gain=0.5)
    else:
        snares(b, (4, 12)); hats(b, gain=0.7, rate=2 if i < 6 else 1)
sing([(108, 0, 76, 8), (108, 8, 77, 8), (109, 0, 79, 8), (109, 8, 77, 8),
      (110, 0, 76, 16, 0.5)], gain=0.45, pan=0.0)
fill(110, 'roll32')
s.bus['drums'][s.pos(111):s.pos(112)] *= 0.0
for i in range(8):
    s.place(s.pos(111, 8 + i), psnare(1.5, seed=i % 3), 0.55 + 0.05 * i, 'drums')
s.place(s.pos(111, 15.4), psnare(1, seed=1), 1.0, 'drums')
s.place(s.pos(112) - int(0.9 * SR), rev(pcrash(20, seed=2)), 0.5, 'drums')

# ================= b112-127: last chorus =================
chorus_section(112, 16, kind='open', gang_=True, oct_=True, crash_every=2,
               mel=0.66, synth_gain=0.64)
# the synth answers in the gap the tune leaves at the top of each phrase
for k in (0, 1, 2, 3):
    pat = ((8, 81, 2, True, False), (10, 79, 2, False, False),
           (12, 77, 2, False, False), (14, 76, 2, False, True))
    seg = synthlib.sawlead(pat, dur_bars=1)
    s.place(s.pos(112 + 4 * k + 3), widen(seg, 0.7), 0.52, 'synth')

# ================= b128-131: the riff, last time =================
wall_phrase(128, RIFF_A)
bass_riff(128)
for b in range(128, 132):
    beat(b, 'open', crash=True)
for i, note in enumerate((65, 67, 69)):
    s.place(s.pos(128 + i, 0.4), gang(note, 15, vowel='oh', seed=9 + i, rasp=0.5),
            0.36, 'gang')

# ================= b132-135: outro =================
for b in (132, 133):
    wall_phrase(b, [(st, Am, 2, 'mute') for st in E8], bars=1, gain=1.0)
    bass_eighths(b, Am)
    beat(b, 'skank')
fill(134, 'toms')
wall_phrase(134, [(0, Am, 2, 'mute'), (2, Am, 2, 'mute'),
                  (4, Am, 2, 'mute'), (6, Am, 2, 'mute')], bars=1)
bass_eighths(134, Am)
# the last chord, and the amp left on
wall_phrase(135, [(0, Am, 16, 'chord')], bars=1, tail=32)
s.place(s.pos(135), pbass(Am - 12, 24), 0.95, 'bass')
s.place(s.pos(135), pkick(), 1.0, 'drums')
s.place(s.pos(135), psnare(), 1.0, 'drums')
s.place(s.pos(135), pcrash(48, seed=0, size=1.7), 0.8, 'drums')
sq = solo(81, 40, gain=26.0, decay=9.0, vib=5.0, vib_depth=0.02, take=1)
sw = np.linspace(0, 1, len(sq)) ** 2.4
sw[-int(0.5 * SR):] *= np.linspace(1, 0.1, int(0.5 * SR))
s.place(s.pos(135, 4), reverb(sq * sw[:, None], decay=2.2, wet=0.3), 0.22, 'lead')

# ---- the fader ---------------------------------------------------------
SECTIONS = [(0, 0.34), (2, 0.44), (4, 0.78), (8, 0.86),
            (12, 0.68), (20, 0.76),
            (28, 0.82), (32, 0.92),
            (36, 1.00),
            (52, 0.90),
            (60, 0.70), (68, 0.78),
            (72, 0.84), (76, 0.94),
            (80, 1.00),
            (96, 0.80), (100, 0.86),
            (104, 0.62), (108, 0.82),
            (112, 1.05),
            (128, 1.00), (132, 0.96), (136, 0.96)]

def fader():
    g = np.ones(s.total, dtype=np.float32)
    ramp = int(0.10 * SR)
    for (b0, v0), (b1, _) in zip(SECTIONS, SECTIONS[1:] + [(999, 0)]):
        a = s.pos(b0); e = min(s.pos(b1), s.total) if b1 < 999 else s.total
        if a >= s.total:
            break
        g[a:e] = v0
    for b, _ in SECTIONS[1:]:
        a = s.pos(b)
        if ramp < a < s.total - ramp:
            g[a - ramp:a + ramp] = np.linspace(g[a - ramp], g[a + ramp], 2 * ramp)
    return g[:, None]

# ---- the rooms ---------------------------------------------------------
# One room for the kit, a small one for the wall - and a LARGER, darker one
# for the shimmer guitar and the pad, because the cold half of this genre is
# a reverb decision as much as a writing one.
s.bus['drums'] += room(s.bus['drums'], decay=0.62, wet=0.30, tone=5600)
s.bus['gtr'] += room(s.bus['gtr'], decay=0.34, wet=0.13, tone=4200)
s.bus['jangle'] += room(s.bus['jangle'], decay=1.5, wet=0.34, tone=4600)
s.bus['jangle'] += delay(s.bus['jangle'], steps_=6.0, times=2, fb=0.25,
                         ping=True, damp=1100)[:s.total] * 0.30
s.bus['lead'] += room(s.bus['lead'], decay=1.1, wet=0.22, tone=4800)
s.bus['synth'] += room(s.bus['synth'], decay=1.3, wet=0.24, tone=4200)
s.bus['gang'] += room(s.bus['gang'], decay=1.4, wet=0.40, tone=4000)

# ---- make room for the tune --------------------------------------------
def duck_band(target, trigger, lo=850, hi=3400, depth=0.38, sens=3.0):
    env = np.abs(trigger).max(axis=1)
    env = uniform_filter1d(env, int(0.025 * SR))
    env = np.clip(env / max(env.max(), 1e-9) * sens, 0, 1)
    g = uniform_filter1d(1 - depth * env, int(0.04 * SR)).astype(np.float32)
    return target - bandpass(target, lo, hi) * (1 - g)[:, None]

s.bus['gtr'] = duck_band(s.bus['gtr'], s.bus['lead'])
s.bus['gtr'] = duck_band(s.bus['gtr'], s.bus['gang'], lo=500, hi=2600, depth=0.35)
s.bus['gtr'] = duck_band(s.bus['gtr'], s.bus['jangle'], lo=2200, hi=4800, depth=0.25)

# lead compression: sustain, and a crest the master does not have to fight
_pk = float(np.abs(s.bus['lead']).max()) or 1.0
s.bus['lead'] = softclip(s.bus['lead'] / _pk * 2.4, 1.0, knee=0.35) * _pk * 0.50
s.bus['lead'] += delay(s.bus['lead'], steps_=6.0, times=2, fb=0.28,
                       ping=True, damp=900)[:s.total] * 0.45

# ---- bus tone ----------------------------------------------------------
s.bus['bass'] = hp(s.bus['bass'], 33, order=2)
s.bus['drums'] = shelf(hp(s.bus['drums'], 32, order=2), 8500, 4.0, 'high')
s.bus['gtr'] = hp(s.bus['gtr'], 82, order=2)
s.bus['jangle'] = hp(s.bus['jangle'], 180, order=2)
s.bus['synth'] = hp(s.bus['synth'], 160, order=2)

for _b in ('drums', 'gtr', 'bass'):
    s.bus[_b] = mono_below(s.bus[_b], 130)

AUTO = fader()
for _b in s.bus:
    s.bus[_b] *= AUTO

GAINS = {'drums': 0.30, 'gtr': 0.26, 'bass': 0.34, 'lead': 0.20,
         'jangle': 0.21, 'synth': 0.20, 'gang': 0.24}
s.report(GAINS)
s.render('punk_antenna_164.wav', drive=1.15, duck=0.0,
         gains=GAINS, clip=1.18, fade=0.8,
         brick=dict(gain=1.15, ceiling=0.89))
