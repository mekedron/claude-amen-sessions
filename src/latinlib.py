"""The Cuban layer: a rhythm section that can share a bar with the Amen break.

174 BPM is a drum & bass tempo. It is also a salsa tempo - fast, but well
inside the 160-220 a mambo lives in. Two bars at 174 is 2.76 seconds, which is
one son clave, and the Amen's own two-bar shape lines up with it exactly. So
the break and a Cuban rhythm section can be laid on the same grid without
either being retimed, and - the coincidence this whole module exists for -
both traditions leave beat 1 of the bass empty. Jungle calls it the missing
downbeat. Havana calls it the anticipation. It is the same hole.

The law here is the clave: a two-bar timeline that every part has to agree
with, the break included. A figure that contradicts it is `cruzado` - crossed -
and it does not read as syncopation, it reads as a mistake.

    CLAVE3 = (0, 6, 12)     bar A, the three side
    CLAVE2 = (4, 8)         bar B, the two side

What this module adds, and why nothing in the engine already did it:

    membrane    the modes of a struck circular head - 1, 1.593, 2.135, 2.295,
                ... - with a per-stroke EXCITATION, so open, slap, bass, tip
                and muff are five different sets of modes on one drum rather
                than five envelopes on one tone. A tumbao is unplayable
                without that: the pattern IS the four strokes.
                `minimallib.conga` is two sines and a noise burst, one stroke,
                tuned for a percussion box at 127. `bruxarialib.atabaque` has
                the right mode ratios but one fixed slap, one long thin drum,
                and it sets the grid to 164. Neither can play a tumbao.
    campana     a struck hand bell, mouth and neck. The engine's two cowbells
                (`phonklib`, `driftlib`) are 808 cowbells - two squares folded
                until they scream, built to carry a phonk melody. A mambo bell
                is hit eight times a bar for four minutes and must not
                fatigue: a real bell body, a hand damping it, and the strike
                transient rolled off above 8 kHz.
    clave       two rosewood sticks over a cupped hand. Almost no noise in it
                at all, which is why five hits can cut through a whole band at
                a level nothing else would survive.
    guiro       a scrape is not a noise burst. It is an impulse train at the
                rate the stick crosses the ridges, through a gourd.
    montuno     a piano played hard, rendered a bar at a time: stiff strings,
                three courses per note, the hammer's own comb, a soundboard
                convolved rather than EQ'd - and one unbroken oscillator per
                pitch across the whole bar, so a repeated octave swells
                instead of retriggering. `core.piano` is a 90s rave stab: saws
                plus a sine, meant to be hit once a bar, and its 500 ms wash
                turns to mud at eight notes a bar.
    mona        an OPEN brass section. `core.horn` is a harmon mute through a
                tight bandpass, deliberately small, built for a jazz club at
                3 a.m. A trumpet at forte is bright because the wave steepens
                in the bore, not because a filter opened - so the brightness
                here is a waveshaper driven by the envelope, and the section
                is three players with their own timing, tuning and vibrato.
    tumbao      the bass, a bar at a time: beat 1 empty, the fifth or the
                seventh on the and-of-2, and the root of the NEXT chord on
                beat 4. The anticipation is the entire feel, and it is also
                the jungle sub, so it is rendered as one oscillator split at
                110 Hz - clean mono underneath, fingers and wood above.

There is deliberately no coro in here. Salsa's other half is a chorus singing
a fixed line, and formant synthesis reproduces the acoustics of a vowel but
not the articulation of a word - no coarticulation, no consonants, no timing
model - so it arrives as mumbling rather than as singing. The part that
answers a call in this music is the horn section, and `mona` can do it.

Every voice below renders past the end of the bar it is given. That is not a
detail: `tumbao`'s note on beat 4 belongs to the NEXT chord, and a segment cut
at the bar line silences the anticipation exactly where it is meant to land.

Usage:
    from latinlib import *                 # amenlib underneath: grid + slices
    s = Session(184, tail=3.0)
    s.pat(0, [(0, K), (12, SN)])                       # the break
    s.place(s.pos(0, 6), conga(TUMBA, 'bass'), 0.8, 'perc')
    s.place(s.pos(0), tumbao(((6, 45), (12, 43)), 16), 0.5, 'bass')
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import fftconvolve

import core
from core import *
from amenlib import *          # sets the grid from the break; K/SN/G/CR/...

# ---------------------------------------------------------------- clave ----
CLAVE3 = (0, 6, 12)            # son clave, three side  (bar A)
CLAVE2 = (4, 8)                # son clave, two side    (bar B)
RUMBA3 = (0, 6, 14)            # rumba clave: the third stroke a 16th later
CASCARA_A = (0, 2, 5, 6, 8, 10, 13, 14)     # timbale shell, three side
CASCARA_B = (0, 2, 4, 6, 9, 10, 12, 14)     # ... two side
BELL_A = (0, 4, 6, 8, 12, 14)               # campana, mouth on 0/8, neck between
BELL_B = (0, 2, 4, 8, 10, 12)

# drum tunings, in MIDI, of the head - not of the shell
QUINTO, CONGA, TUMBA = 60, 53, 46
MACHO, HEMBRA = 74, 67                       # the two bongos

_IR = {}


# ======================================================= struck membranes ===
# `membrane` - the modes of a struck circular head - lives in core: it is a
# physical model rather than a Cuban one, and every genre with hands on skin
# needs it. HEAD, AXIAL and STROKE arrive with it through `from core import *`.


@cached
def conga(note=CONGA, stroke='open', dur=2.0, gain=1.0, seed=0, shell=1.0,
          size=1.0, vel=1.0):
    """A tumbadora.

    The shell is the other half of the instrument and it does NOT move with
    the tuning: it is a barrel of staves with an open bottom, so it has one
    fixed air resonance around 110-190 Hz depending on the drum's size. Three
    congas tuned to three pitches through one shell resonance sound like one
    drum played three ways; three different shell frequencies is what makes
    them sound like three drums standing next to each other."""
    n, t = steps(max(dur, 0.9), floor=int(0.09 * SR))
    x = membrane(midi(note), n, stroke, load=0.93, damp=0.52,
                 tight=1.0 / max(vel, 0.35) ** 0.35, seed=seed + note)
    st = stereo(np.tanh(1.5 * x * vel))
    if shell:
        # a slap puts its energy into the skin, not into the wood
        w = shell * (0.30 if stroke in ('slap', 'tip', 'toe') else 1.0)
        f = 165.0 / size
        st = st + w * 0.55 * bandpass(st, f * 0.78, f * 1.30, order=2)
        st = st + w * 0.18 * bandpass(st, f * 2.4, f * 3.6, order=2)
    st = st - 0.25 * bandpass(st, 620, 1150)           # the boxy dip of a barrel
    st = hp(st, 55, order=2)
    return (st * adsr(n, a=0.0004, r=0.012)[:, None]).astype(np.float32) * gain * 0.62


@cached
def bongo(note=MACHO, stroke='open', dur=1.2, gain=1.0, seed=0, vel=1.0):
    """The little pair. A bongo head is tacked down, not tensioned by lugs, so
    it is far tighter than a conga: the pitch barely falls, the ring is short,
    and the whole sound sits an octave and a half higher. The martillo - the
    hammer - runs continuous eighths on these all night, so they have to be
    small enough to disappear behind everything else."""
    n, t = steps(max(dur, 0.7), floor=int(0.05 * SR))
    x = membrane(midi(note), n, stroke, load=0.97, damp=0.80, tight=2.6,
                 seed=seed + note * 3)
    st = stereo(np.tanh(1.7 * x * vel))
    st = st + 0.30 * bandpass(st, 380, 560, order=2)   # the little shell
    st = hp(st, 190, order=2)
    return (st * adsr(n, a=0.0003, r=0.008)[:, None]).astype(np.float32) * gain * 0.5


@cached
def paila(note=64, dur=1.4, gain=1.0, seed=0, rim=0.0, vel=1.0):
    """The timbale head: a shallow metal-shelled drum with no bottom skin, so
    the head rings free and bright and the shell rings with it."""
    n, t = steps(max(dur, 0.8), floor=int(0.06 * SR))
    x = membrane(midi(note), n, 'open', load=0.99, damp=0.35, tight=2.0,
                 seed=seed + 71)
    rng = np.random.default_rng(seed + 401)
    st = stereo(np.tanh(1.6 * x * vel))
    st = st + 0.40 * bandpass(st, 900, 2400, order=2)  # the steel shell
    if rim:
        crack = rng.standard_normal(n) * np.exp(-t / 0.0018)
        st = st + bandpass(stereo(crack), 1800, 9000) * 1.5 * rim
    st = hp(st, 150, order=2)
    return (st * adsr(n, a=0.0003, r=0.010)[:, None]).astype(np.float32) * gain * 0.55


# ================================================================= metal ====
# A hand bell is a truncated cone of folded steel. Its partials are not a
# harmonic series and not the membrane's Bessel set either - they are the
# bending modes of a shell, irregular, and the ear builds a "strike note" out
# of the second and third of them rather than hearing the lowest.
BELLMODES = np.array([1.000, 1.472, 1.934, 2.441, 3.021, 3.713, 4.530, 5.402])


@cached
def campana(dur=2.0, gain=1.0, mouth=True, tune=520.0, seed=0, vel=1.0,
            ring=1.0):
    """The mambo bell, held in one hand and hit with a stick.

    Two strokes, and salsa uses both in one pattern: the MOUTH - the open wide
    end - rings low and long, and the NECK, up by the closed end where the
    player's fingers are wrapped round the metal, is dry and high because the
    hand is sitting on the modes that would have sustained.

    This gets struck eight times a bar for four minutes. The reason it does
    not become unbearable is that the strike transient is rolled off above
    8 kHz and moves with the seed: a bell whose attack is identical four
    hundred times is a machine gun."""
    n, t = steps(max(dur, 0.7), floor=int(0.06 * SR))
    rng = np.random.default_rng(seed * 131 + 7)
    r = BELLMODES.copy()
    a = np.array([0.55, 1.00, 0.85, 0.60, 0.42, 0.26, 0.16, 0.10])
    if not mouth:                       # the hand is on the low modes
        a = a * np.array([0.10, 0.28, 0.75, 1.00, 0.95, 0.75, 0.50, 0.34])
        tune = tune * 1.42              # so the modes that survive are higher
        dec = 0.038 * ring
    else:
        dec = 0.175 * ring
    a = a * (1 + 0.07 * rng.standard_normal(len(a)))
    r = r * (1 + 0.006 * rng.standard_normal(len(r)))
    keep = r * tune < SR * 0.45
    r, a = r[keep], a[keep]
    tau = dec / (1 + 0.42 * (r - 1))
    ph = 2 * np.pi * tune * t
    x = (np.sin(np.outer(ph, r) + rng.random(len(r)) * 6.283)
         * np.exp(-np.outer(t, 1.0 / tau)) * a).sum(1) / a.sum()

    # stick on steel: bright, and over in two milliseconds
    m = min(n, int(0.006 * SR))
    tick = rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.0011)
    st = stereo(np.tanh(1.9 * x * vel))
    st[:m] += bandpass(stereo(tick), 2400, 8000) * 0.5 * vel
    st = lp(st, 8600, order=4)                     # nothing above the strike
    st = st + 0.30 * bandpass(st, tune * 1.3, tune * 2.6, order=2)
    st = hp(st, 300, order=2)
    return (st * adsr(n, a=0.0002, r=0.008)[:, None]).astype(np.float32) * gain * 0.42


@cached
def cascara(dur=0.8, gain=1.0, seed=0, vel=1.0, tune=2050.0):
    """A stick on the chrome side of a timbale. Not a rim and not a bell: a
    thin cylinder rung and immediately damped by the drum hanging off it -
    two milliseconds of metal and then nothing. It is the eighth-note engine
    of half of Cuban music and it has to sit almost under the threshold."""
    n, t = steps(max(dur, 0.5), floor=int(0.03 * SR))
    rng = np.random.default_rng(seed * 53 + 3)
    x = np.zeros(n)
    for r, a, d in ((1.0, 1.0, 0.0075), (1.71, 0.6, 0.0042), (2.63, 0.35, 0.0026),
                    (4.10, 0.18, 0.0015)):
        x += a * np.sin(2 * np.pi * tune * r * t + rng.random() * 6) * np.exp(-t / d)
    x += rng.standard_normal(n) * np.exp(-t / 0.0009) * 0.8
    st = bandpass(stereo(np.tanh(1.8 * x * vel)), 700, 9000)
    return (st * adsr(n, a=0.0002, r=0.006)[:, None]).astype(np.float32) * gain * 0.4


@cached
def clave(dur=1.5, gain=1.0, seed=0, tune=2380.0, vel=1.0):
    """Two rosewood sticks, one resting on a cupped hand.

    Almost the whole sound is a single bending mode of a short thick cylinder,
    high and clean, plus the Helmholtz pock of the hand under it - and almost
    no noise at all. That is why five hits a bar cut through a fourteen-piece
    band at a level nothing else on the stage would survive: it owns 2.4 kHz
    completely and asks for nothing else."""
    n, t = steps(max(dur, 0.9), floor=int(0.05 * SR))
    rng = np.random.default_rng(seed * 191 + 11)
    tune = tune * (1 + 0.004 * rng.standard_normal())
    x = np.sin(2 * np.pi * tune * t) * np.exp(-t / 0.042)
    x += 0.30 * np.sin(2 * np.pi * tune * 2.756 * t) * np.exp(-t / 0.009)
    x += 0.11 * np.sin(2 * np.pi * tune * 5.404 * t) * np.exp(-t / 0.0035)
    pock = np.sin(2 * np.pi * 720 * t) * np.exp(-t / 0.024) * 0.42   # the hand
    click = rng.standard_normal(n) * np.exp(-t / 0.0007) * 0.22
    st = stereo(np.tanh(1.5 * (x + pock + click) * vel))
    st = hp(st, 380, order=2)
    return (st * adsr(n, a=0.0002, r=0.010)[:, None]).astype(np.float32) * gain * 0.5


# ============================================================== the gourd ===
@cached
def guiro(dur=4.0, gain=1.0, teeth=16, seed=0, accel=0.0, vel=1.0, tone=1.0):
    """A scrape, which is not a noise burst.

    A stick dragged across a ridged gourd makes one small impact per ridge, so
    the sound is an IMPULSE TRAIN at the rate the stick is travelling - and
    the rate is what the ear hears, not the timbre. A long down-stroke is
    twenty ridges over a beat; the two short up-strokes that answer it are six
    each. Modelling it as filtered noise loses exactly the thing that makes it
    a guiro."""
    n, t = steps(max(dur, 0.6), floor=int(0.04 * SR))
    rng = np.random.default_rng(seed * 313 + 5)
    span = int(n * 0.82)
    u = np.linspace(0, 1, teeth) ** (1.0 + accel)      # the stroke can speed up
    idx = (u * span).astype(int)
    x = np.zeros(n)
    for i, k in enumerate(idx):
        m = min(n - k, int(0.0016 * SR))
        if m < 4:
            continue
        amp = (0.55 + 0.45 * (i / max(teeth - 1, 1))) * (0.8 + 0.4 * rng.random())
        x[k:k + m] += rng.standard_normal(m) * np.exp(
            -np.arange(m) / SR / 0.00035) * amp
    st = bandpass(stereo(x), 1800 * tone, 9000 * tone)
    st = st + 0.9 * bandpass(stereo(x), 380, 900, order=2)     # the gourd body
    st = st * np.minimum(1.0, np.exp(-(t - span / SR) / 0.02))[:, None]
    return (np.tanh(1.6 * st * vel) * adsr(n, a=0.001, r=0.010)[:, None]
            ).astype(np.float32) * gain * 0.34


@cached
def maraca(dur=0.7, gain=1.0, seed=0, vel=1.0, seeds=1.0):
    """The opposite of a shaker. `minimallib.shaker` has a slow attack because
    the beads have to travel; a maraca is snapped, so every seed arrives at
    the wall at once and the attack is instantaneous. That difference is
    audible at a hundredth of the level either of them is mixed at."""
    n, t = steps(max(dur, 0.4), floor=int(0.02 * SR))
    rng = np.random.default_rng(seed * 77 + 19)
    nz = rng.standard_normal(n)
    body = bandpass(stereo(nz), 3000, 9500) * np.exp(-t / (0.011 * seeds))[:, None]
    gourd = bandpass(stereo(nz), 550, 1250, order=2) * np.exp(-t / 0.022)[:, None]
    st = body * 1.0 + gourd * 0.45
    return (np.tanh(1.5 * st * vel) * adsr(n, a=0.0002, r=0.006)[:, None]
            ).astype(np.float32) * gain * 0.4


# ============================================================== the piano ===
def board_ir(seed=0, size=0.13):
    """A grand's soundboard, as something that happens over time.

    The strings of a piano are almost inaudible on their own - a piano is a
    two-square-metre spruce plate with ribs and a bridge, and every note is
    that plate's answer to being pushed. Approximating it with fixed EQ gives
    the same peaks on every note, which is a formant, which is a vowel. So it
    is built the way `punklib.cab_ir` builds a speaker: a direct hit, a dense
    fast spray off the ribs and the case, a slower low tail for the plate, and
    only then the tone shape."""
    key = ('board', seed, size)
    if key in _IR:
        return _IR[key]
    rng = np.random.default_rng(seed + 7717)
    n = int(size * SR)
    t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    ir = np.zeros(n)
    ir[:3] = [1.0, 0.38, -0.14]
    ir += nz * np.exp(-t / 0.0026) * 0.70                     # the bridge
    ir += bandpass(stereo(nz), 90, 420, order=2)[:, 0] * np.exp(-t / 0.045) * 1.5
    ir += bandpass(stereo(nz), 420, 1800, order=2)[:, 0] * np.exp(-t / 0.013) * 1.1
    ir += bandpass(stereo(nz), 1800, 6000, order=2)[:, 0] * np.exp(-t / 0.005) * 0.55
    pad = 512
    st = stereo(np.concatenate([np.zeros(pad), ir, np.zeros(pad)]))
    st = hp(lp(st, 9000, order=6), 45, order=3)
    st = st + 0.9 * bandpass(st, 105, 190)                    # the plate's low modes
    st = st - 0.35 * bandpass(st, 480, 900)                   # the boxy dip
    st = st + 0.35 * bandpass(st, 2200, 4200)                 # the lid, open
    ir = st[pad:pad + n, 0] * np.hanning(2 * n)[n:] ** 0.3
    ir = ir / np.sqrt((ir ** 2).sum())
    _IR[key] = ir.astype(np.float32)
    return _IR[key]


def _piano_note(f0, n, t, strikes, vel, seed, B=2.4e-4, hammer=0.125,
                decay=1.9, hold=None, courses=3):
    """One string course, struck n times inside one bar, as ONE oscillator.

    A hammer hitting a string that is still moving does not start a new note -
    it re-excites the note that never stopped. Rendering each strike as its
    own segment is what makes a repeated octave sound fragmented; here every
    partial keeps one unbroken phase for the whole bar and only its ENVELOPE
    swells, by max-accumulate, at each strike.

    Three details do most of the work:
      * stiffness - a piano wire is thick, so partial k sits at
        k*f0*sqrt(1+B*k^2), and by the 16th it is a quarter-tone sharp. That
        stretch is why a piano and a sine stack are different objects.
      * the hammer strikes at about 1/8 of the length, so it cannot excite the
        8th partial, or the 16th. That missing-partial comb is a piano.
      * felt gets STIFFER the harder it is hit, so the excitation's own
        lowpass opens with velocity. A piano played hard is not a louder piano,
        it is a brighter one - and a montuno is played hard."""
    rng = np.random.default_rng(seed * 6011 + 29)
    kmax = int(min(7200.0 / f0, 34))
    if kmax < 2:
        kmax = 2
    k = np.arange(1, kmax + 1, dtype=np.float64)
    fk = k * f0 * np.sqrt(1 + B * k * k)
    keep = fk < SR * 0.45
    k, fk = k[keep], fk[keep]
    a = np.abs(np.sin(k * np.pi * hammer)) / k ** 1.02          # the hammer's comb
    fc = 1400.0 + 5200.0 * vel ** 1.5                           # the felt hardens
    a = a / np.sqrt(1 + (fk / fc) ** 4)
    tau = decay / (1 + 0.85 * k ** 1.30)                        # the top dies first

    env = np.zeros((n, len(k)))
    for si in strikes:
        m = n - si
        if m < 16:
            continue
        d = np.exp(-np.outer(t[:m], 1.0 / tau))
        if hold:                                                # the damper falls
            hs = min(m, int(hold))
            d[hs:] *= np.exp(-t[:m - hs] / 0.055)[:, None]
        np.maximum(env[si:], d, out=env[si:])

    out = np.zeros(n)
    for c in range(courses):
        # three strings per note, tuned within a cent of each other. The beat
        # between them is the piano's chorus, and the reason its decay has two
        # rates: the courses drift out of phase, cancel, and hand their energy
        # back and forth for a second and a half.
        det = 1.0 + (c - 1) * 0.00035 * (0.7 + 0.6 * rng.random())
        ph = 2 * np.pi * np.outer(t, fk * det) + rng.random(len(k)) * 6.283
        out += (np.sin(ph) * env * a).sum(1)
    return out / (courses * max(a.sum(), 1e-9))


@cached
def montuno(events, dur_steps=16, gain=1.0, vel=0.85, seed=0, hold=2.2,
            decay=1.9, board=1.0, spread=0.85, drive=1.3, tail=5.0, lid=1.0):
    """A salsa piano, one bar at a time.

    `events` is a tuple of (step, (midi, ...), velocity) - the montuno is
    played in octaves with both hands, so most events are two or three notes
    an octave apart, and the same note comes back three or four times a bar.

    `core.piano` is a 90s rave stab: three detuned saws and a sine, one hit a
    bar, 500 ms of wash. Eight of those a bar is mud, and a saw is not a
    string. This is the string. `tail` lets the last note of the bar ring past
    the bar line, which is where a piano's notes actually go."""
    n, t = steps(dur_steps + tail)
    evs = sorted(events)
    per = {}
    for ev in evs:
        st, notes = ev[0], ev[1]
        v = ev[2] if len(ev) > 2 else 1.0
        si = int(round(st * STEP))
        if si >= n:
            continue
        for nt in notes:
            per.setdefault((nt, round(v, 3)), []).append(si)

    x = np.zeros((n, 2))
    thump = np.zeros(n)
    rng = np.random.default_rng(seed * 331 + 3)
    for (nt, v), sts in per.items():
        f0 = midi(nt)
        # thick short wire low down, thin long wire up top
        B = 2.0e-4 * (1 + 2.2 * max(0.0, (55 - nt) / 24.0) ** 2) + 3.0e-5 * max(0, nt - 72)
        y = _piano_note(f0, n, t, sts, vel * v, seed + nt, B=B,
                        decay=decay * (1.0 if nt < 72 else 0.55),
                        hold=int(hold * STEP)) * (0.45 + 0.55 * v)
        # A piano is stereo because its frame is: the bass strings run across
        # the left of it and the treble down the right, and a pair of mics over
        # an open lid hears exactly that. Panning by LEVEL, so it survives
        # being summed - the usual trick of delaying one channel would put a
        # comb filter through the one instrument that is playing all record.
        pan = float(np.clip((nt - 66) / 22.0, -1.0, 1.0)) * spread
        a = (pan + 1) * np.pi / 4
        x[:, 0] += y * np.cos(a) * 1.41
        x[:, 1] += y * np.sin(a) * 1.41
        for si in sts:                        # key, action, hammer shank
            m = min(n - si, int(0.020 * SR))
            if m < 8:
                continue
            tm = np.arange(m) / SR
            thump[si:si + m] += rng.standard_normal(m) * np.exp(-tm / 0.0022) * 0.30 * v
            thump[si:si + m] += rng.standard_normal(m) * np.exp(-tm / 0.0006) * 0.55 * v

    st_ = x.astype(np.float32)
    st_ = st_ + bandpass(stereo(thump), 150, 2600) * 0.6
    st_ = st_ + bandpass(stereo(thump), 2600, 8000) * 0.85
    if board:
        ir = board_ir()
        out = np.zeros_like(st_)
        for c in range(2):
            out[:, c] = fftconvolve(st_[:, c], ir)[:n]
        st_ = st_ * (1 - board * 0.55) + out * board * 2.4
    # The lid. A salsa piano is played with it fully open and a microphone
    # inside, which is where the brightness of a montuno comes from; a pop
    # record's piano is on the short stick with the mics further back, so
    # `lid` is not a tone control, it is where the instrument was recorded.
    st_ = st_ + lid * 0.55 * bandpass(st_, 1600, 4200)
    st_ = np.tanh(drive * st_) / np.tanh(drive)
    st_ = hp(st_, 90, order=2)
    return (st_ * adsr(n, a=0.0008, r=0.006)[:, None]).astype(np.float32) * gain * 0.55


# ========================================================== the horn line ===
BORE = {  # bell_hz, brassiness, duty, attack, breath, cut
    'trumpet': (1350.0, 2.10, 0.38, 0.024, 0.9, 9000.0),
    'bone':    (700.0,  2.60, 0.44, 0.038, 1.1, 6200.0),
    'sax':     (950.0,  1.20, 0.28, 0.022, 1.3, 6800.0),
}


def _brass(phrase, n, t, bore='trumpet', vel=1.0, glide=0.008, seed=0,
           vib=5.6, bright=1.0):
    """One player. Mono float64.

    A brass instrument gets brighter when it is played louder, and it is not
    a filter opening: the pressure wave STEEPENS as it travels the bore, the
    way a wave steepens as it runs up a beach, and by the bell it has grown a
    whole new set of harmonics. So the waveshaper's drive here follows the
    amplitude envelope. Turn that off and the section can only get louder,
    which is the single most obvious thing wrong with a synthesised horn."""
    bell_hz, brassy, duty, atk, breath, cut = BORE[bore]
    rng = np.random.default_rng(seed * 811 + 17)
    evs = sorted(phrase)
    edge = [min(int(st * STEP), n - 1) for st, _, _ in evs] + [n]

    f = np.empty(n)
    f[:edge[0]] = midi(evs[0][1])
    since = np.zeros(n)
    amp = np.zeros(n)
    for i, (_, nt, art) in enumerate(evs):
        a0, b0 = edge[i], edge[i + 1]
        d = np.arange(b0 - a0) / SR
        seg = np.full(b0 - a0, midi(nt))
        if '^' in art:                          # the scoop up into the note
            seg = seg * (1 - 0.048 * np.exp(-d / 0.038))
        if 'f' in art:                          # the fall off the end
            kk = int((b0 - a0) * 0.60)
            seg[kk:] *= 2 ** (-np.linspace(0, 4.5, b0 - a0 - kk) ** 1.35 / 12)
        if 'd' in art:                          # the doit: a rip upward
            kk = int((b0 - a0) * 0.70)
            seg[kk:] *= 2 ** (np.linspace(0, 3.0, b0 - a0 - kk) ** 1.2 / 12)
        f[a0:b0] = seg
        since[a0:b0] = d
        lv = 1.0
        if '>' in art: lv = 1.28
        if '-' in art: lv = 0.72
        e = np.full(b0 - a0, lv)
        rl = min(int((0.030 if '.' in art else 0.055) * SR), (b0 - a0) - 1)
        if '.' in art:                          # staccato: off well before the end
            kk = max(1, int((b0 - a0) * 0.42))
            e[kk:] = 0.0
            e[max(kk - rl, 0):kk] = np.linspace(lv, 0, min(rl, kk))
        elif rl > 1:
            e[-rl:] *= np.linspace(1, 0.15, rl)
        amp[a0:b0] = e
    f = uniform_filter1d(f, max(int(glide * SR), 3))
    # Clamp AFTER the smoother, not before: a running-sum box filter returns
    # values of order -1e-14 where the signal is zero, and a fractional power
    # of a negative number is a NaN - which then spreads through a whole bus.
    amp = np.maximum(uniform_filter1d(amp * np.minimum(since / atk, 1.0) ** 0.7,
                                      max(int(0.006 * SR), 3)), 0.0) * vel

    vibr = 1 + 0.006 * np.sin(2 * np.pi * vib * t + rng.random() * 6) \
        * np.minimum(since / 0.30, 1.0)
    ph = 2 * np.pi * np.cumsum(f * vibr) / SR
    fm = float(f.max()) * 2.6

    # the lip valve: a pulse, not a saw. Duty sets which harmonics survive.
    x = saw_ph(ph, fm) - saw_ph(ph - 2 * np.pi * duty, fm)
    x = 0.55 * saw_ph(ph, fm) + 0.85 * x
    # The shaper only means anything if the signal reaching it is small enough
    # to sit on the curve. Feed it something already past saturation and every
    # dynamic sounds identically bright, which is the failure this whole model
    # exists to avoid.
    x = x / max(float(np.abs(x).max()), 1e-9) * 0.42
    # ... and then the bore steepens it, by an amount that follows the blow
    top = 0.9 + 11.0 * brassy * bright
    dr = 0.9 + 11.0 * brassy * bright * amp ** 1.6
    x = np.tanh(dr * x) / np.tanh(top * 0.42) * 0.42
    # a steepened wave is asymmetric - which is where a brass instrument's
    # even harmonics come from, and why it is not a squarer square
    x = x + 0.30 * brassy * (x * x - float((x * x).mean())) * np.minimum(amp * 2.2, 1.0)
    x = x * amp

    # the bell radiates highs and reflects lows, so the instrument has one
    # fixed resonance that does NOT move with the note
    stx = stereo(x)
    stx = stx + 1.55 * bandpass(stx, bell_hz * 0.72, bell_hz * 1.60, order=2)
    stx = stx + 0.85 * bandpass(stx, bell_hz * 1.8, bell_hz * 3.2, order=2)
    stx = stx - 0.40 * bandpass(stx, bell_hz * 0.20, bell_hz * 0.42)   # the bell reflects lows
    # A bell radiates high frequencies far more efficiently than low ones, and
    # at pianissimo there are barely any high frequencies to radiate. Both
    # effects pull the same way, so the top of the instrument opens with the
    # blow rather than standing still - crossfaded per sample, not switched.
    dark = lp(stx, 1500, order=4)
    br = np.minimum(amp * 1.15, 1.0)[:, None] ** 0.8
    stx = dark * (1 - br) + lp(stx, cut, order=4) * br
    # air past the lips, loudest at the attack
    puff = rng.standard_normal(n) * np.minimum(np.exp(-since / 0.045) + 0.12, 1.0)
    stx = stx + bandpass(stereo(puff), 1500, 7000) * 0.055 * breath * amp[:, None]
    return stx[:, 0].astype(np.float64) * 1.0


@cached
def mona(phrase, dur_steps=16, gain=1.0, bore='trumpet', players=3, vel=1.0,
         seed=0, width=0.7, bright=1.0, room=0.0):
    """A section, not a horn.

    `phrase` is (step, midi, articulation):

        'n' plain   '>' accented   '-' soft   '.' short
        '^' scooped into from below   'f' falls off the end   'd' rips up

    Three players do not play in unison: they arrive within about eight
    milliseconds of each other, they are a few cents apart, and their vibrato
    is out of phase. That spread is the whole difference between a section and
    a chorus effect - a chorus modulates one player, and it sounds like it."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(seed * 97 + 41)
    out = np.zeros((n, 2), dtype=np.float64)
    for p in range(players):
        lag = int(rng.normal(0, 0.0030) * SR) + (0 if p == 0 else int(0.0015 * SR))
        cents = 0.0 if p == 0 else rng.normal(0, 4.5)
        ph = [(st, nt + cents / 100.0, art) for st, nt, art in phrase]
        y = _brass(ph, n, t, bore, vel=vel, seed=seed * 13 + p,
                   vib=5.2 + 0.7 * p, bright=bright)
        if lag > 0:
            y = np.concatenate([np.zeros(lag), y[:-lag]])
        elif lag < 0:
            y = np.concatenate([y[-lag:], np.zeros(-lag)])
        pan = 0.0 if players == 1 else (p / (players - 1) - 0.5) * 2 * width
        out[:, 0] += y * np.cos((pan + 1) * np.pi / 4)
        out[:, 1] += y * np.sin((pan + 1) * np.pi / 4)
    out = (out / players).astype(np.float32)
    out = hp(out, 180, order=2)
    if room:
        out = out + reverb(out, decay=0.9, wet=room, tone=5200)[:n] * 0.5
    return (out * adsr(n, a=0.002, r=0.010)[:, None]).astype(np.float32) * gain * 0.75


# ================================================================ the bass ==
@cached
def tumbao(notes, dur_steps=16, gain=1.0, sub=0.75, decay=0.42, glide=0.020,
           seed=0, drive=1.7, wood=1.0, cut=1600.0, tail=7.0):
    """One bar of the bass. `notes` is (step, midi[, velocity]).

    The tumbao is defined by where it does NOT play. Beat 1 is empty; the
    fifth or the seventh arrives on the and-of-2; and the note on beat 4 is
    the root of the chord that has not started yet. That anticipation is the
    reason salsa leans forward, and it is also, exactly, the missing downbeat
    of a jungle bassline - which is the only reason a Cuban rhythm section and
    the Amen break can share a bar at all.

    Rendered as one oscillator for the whole bar, as `punklib.bassbar` is:
    one frequency track, smoothed into portamento, one unbroken phase, and an
    amplitude that swells at each pluck by max-accumulate instead of ever
    returning to zero. A baby bass plucked twice in a bar is one string that
    was already moving.

    `tail` is how far past the bar the segment runs. It is not a nicety: the
    note on beat 4 belongs to the NEXT chord, so cutting the segment at the
    bar line silences the anticipation exactly where it is supposed to arrive,
    and leaves a hole under the first half of every bar."""
    n, t = steps(dur_steps + tail)
    evs = sorted(notes)
    edge = [min(max(int(ev[0] * STEP), 0), n) for ev in evs] + [n]  # last note holds
    edge = list(np.maximum.accumulate(edge))
    rng = np.random.default_rng(seed * 617 + 23)

    f = np.full(n, midi(evs[0][1]))
    for i, ev in enumerate(evs):
        f[edge[i]:edge[i + 1]] = midi(ev[1])
    f = uniform_filter1d(f, max(int(glide * SR), 3))
    ph = 2 * np.pi * np.cumsum(f) / SR

    amp = np.zeros(n)
    for i, ev in enumerate(evs):
        k = edge[i]
        v = ev[2] if len(ev) > 2 else 1.0
        d = np.exp(-np.arange(n - k) / SR / decay) * v
        np.maximum(amp[k:], d, out=amp[k:])
    amp = uniform_filter1d(amp, max(int(0.006 * SR), 3))

    # the string: a fat fundamental with just enough second and third to be
    # findable on a phone, and a body resonance that does not move with it
    low = (np.sin(ph) + 0.42 * np.sin(2 * ph) + 0.21 * np.sin(3 * ph)
           + 0.10 * np.sin(4 * ph) + 0.05 * np.sin(5 * ph)) * amp
    st_ = stereo(low)
    st_ = st_ + 0.85 * bandpass(st_, 190, 420, order=2)          # the box
    st_ = st_ + 0.45 * bandpass(st_, 620, 1100, order=2)

    pluck = np.zeros(n)                                          # the finger
    for i, ev in enumerate(evs):
        k = edge[i]
        v = ev[2] if len(ev) > 2 else 1.0
        m = min(n - k, int(0.045 * SR))
        if m < 16:
            continue
        tm = np.arange(m) / SR
        cl = rng.standard_normal(m) * np.exp(-tm / 0.0035)
        cl += np.sin(2 * np.pi * midi(ev[1]) * 5.4 * tm) * np.exp(-tm / 0.006) * 0.7
        pluck[k:k + m] += cl * 0.55 * v * wood

    st_ = st_ + bandpass(stereo(pluck), 320, cut) * 1.1
    st_ = np.tanh(drive * st_) / np.tanh(drive)
    lo, hi = split(st_, 110.0)
    lo = stereo(lo.mean(axis=1))                                 # the sub is mono
    out = lo * sub * 1.15 + hi
    out = hp(out, 30, order=2)
    return (out * adsr(n, a=0.0012, r=0.004)[:, None]).astype(np.float32) * gain * 0.8



def _morph_band(seg, track, bands=7, q=0.30, w=1.0):
    """A bandpass whose centre follows a control signal.

    Filtering with one fixed band per vowel and switching between them clicks,
    and a mouth does not switch anyway - it travels. So build `bands` fixed
    bandpasses spanning the range the track actually covers and crossfade
    between them with a triangular weight, which is a linear interpolation in
    the filter's output rather than in its coefficients and therefore stable."""
    lo, hi = float(track.min()), float(track.max())
    if hi <= lo * 1.02:
        return bandpass(seg, lo * (1 - q), lo * (1 + q)) * w
    cs = np.geomspace(lo, hi, bands)
    out = np.zeros_like(seg)
    lg = np.log(np.clip(track, lo, hi))
    step_ = (np.log(hi) - np.log(lo)) / (bands - 1)
    for c in cs:
        wgt = np.clip(1.0 - np.abs(lg - np.log(c)) / step_, 0, 1)
        if wgt.max() < 1e-3:
            continue
        out += bandpass(seg, c * (1 - q), c * (1 + q)) * wgt[:, None]
    return out * w


# ================================================================ the coro ==
# The vowels a chorus actually sings, as the three formants that identify
# them. A coro is not a pad: it is three men in a room singing one short line
# over and over, and what makes it read as words rather than as a chord is
# that the vowel MOVES between the notes.
VOWEL = {'a': (730, 1090, 2600), 'e': (560, 1840, 2480), 'i': (270, 2290, 3010),
         'o': (450, 800, 2830), 'u': (325, 700, 2530), 'ah': (700, 1220, 2600)}


def coro(phrase, dur_steps=16, gain=1.0, voices=3, seed=0, vel=1.0,
         base=0, wide=0.75, air=0.35):
    """Three men singing one line. `phrase` is (step, midi, vowel).

    `core.vox` is a formant choir PAD: a 300 ms attack, one vowel held for the
    whole segment, and a slow release - correct for an atmosphere and useless
    for a coro, which is a sung sentence in the middle of a fast record. The
    two things that make this one read as words are that the vowel travels
    between notes on a real glide (a mouth cannot teleport) and that the three
    singers are not in tune with each other and never start together."""
    n, t = steps(dur_steps)
    evs = sorted(phrase)
    edge = [min(max(int(st * STEP), 0), n) for st, _, _ in evs] + [n]
    edge = list(np.maximum.accumulate(edge))
    rng = np.random.default_rng(seed * 1009 + 61)

    f = np.full(n, midi(evs[0][1] + base))
    F = np.tile(np.array(VOWEL[evs[0][2]], float), (n, 1))
    since = np.zeros(n)
    amp = np.zeros(n)
    for i, (_, nt, vw) in enumerate(evs):
        a0, b0 = edge[i], edge[i + 1]
        d = np.arange(b0 - a0) / SR
        # every sung note is approached from underneath; a voice slides into
        # pitch, it does not arrive at it
        f[a0:b0] = midi(nt + base) * (1 - 0.030 * np.exp(-d / 0.045))
        F[a0:b0] = VOWEL[vw]
        since[a0:b0] = d
        e = np.ones(b0 - a0)
        r = min(int(0.075 * SR), (b0 - a0) - 1)
        if r > 1:
            e[-r:] *= np.linspace(1, 0.0, r)
        amp[a0:b0] = e
    f = uniform_filter1d(f, max(int(0.012 * SR), 3))
    F = uniform_filter1d(F, max(int(0.045 * SR), 3), axis=0)     # the mouth moves
    amp = uniform_filter1d(amp * np.minimum(since / 0.045, 1.0) ** 0.8,
                           max(int(0.010 * SR), 3)) * vel

    out = np.zeros((n, 2), dtype=np.float64)
    for v in range(voices):
        det = 1.0 + rng.normal(0, 0.0035)
        lag = int(abs(rng.normal(0, 0.006)) * SR)
        vibr = 1 + 0.012 * np.sin(2 * np.pi * (4.6 + 0.5 * v) * t + rng.random() * 6) \
            * np.minimum(since / 0.28, 1.0)
        ph = 2 * np.pi * np.cumsum(f * det * vibr) / SR
        x = saw_ph(ph, float(f.max()) * 1.6)
        # the glottis is a pulse, not a saw: a bit of asymmetry per singer
        x = x + 0.25 * np.sign(np.sin(ph)) * (0.6 + 0.5 * rng.random())
        st = stereo(x)
        y = np.zeros((n, 2), dtype=np.float32)
        for j, w in enumerate((1.0, 0.62, 0.28)):
            y += _morph_band(st, F[:, j], w=w)
        # a vocal tract is a filter, not a gate: the glottal source itself
        # radiates too, and leaving it out is what makes a formant synth sound
        # like two bandpasses instead of like a throat
        y = y + lp(st, 1100, order=2) * 0.30 + hp(lp(st, 4000), 2400) * 0.10
        y = y + hp(stereo(rng.standard_normal(n) * 0.02), 3500) * air * amp[:, None]
        pan = 0.0 if voices == 1 else (v / (voices - 1) - 0.5) * 2 * wide
        yy = y[:, 0] * amp
        if lag:
            yy = np.concatenate([np.zeros(lag), yy[:-lag]])
        out[:, 0] += yy * np.cos((pan + 1) * np.pi / 4)
        out[:, 1] += yy * np.sin((pan + 1) * np.pi / 4)
    out = (out / voices).astype(np.float32)
    out = hp(out, 150, order=2)
    return (out * adsr(n, a=0.004, r=0.020)[:, None]).astype(np.float32) * gain * 1.05
