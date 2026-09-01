"""DISCOLIB - a live band, in a room, on tape.

Disco is not house with strings on it. The two share a kick on every beat and
an open hat on every offbeat and nothing else, and the difference is not a
palette - it is that every part here was PLAYED, and the record is the sound
of seven people in a room disagreeing with each other by a few milliseconds.

So the engine's existing kits do not fit, and the delta is the same in every
one of them:

  `funklib` is the closest thing here - fkick, fsnare, fclap, fhat, tamb,
  brass - and it is an EIGHTIES kit. Every voice in it ends in `_lofi()`,
  because that module is a 12-bit sampler and a gated reverb, and it is
  correct for what it is. Disco is 1977: a 22" bass drum with a felt beater
  in a live room, onto two-inch tape. There is no converter anywhere in the
  chain, and the room is not switched off after 200 ms.

  `houselib` has the four-to-the-floor and the offbeat hat, and its kick is
  a 909 - a machine, and a machine is the one thing this record must not
  sound like.

  `punklib.string()` and `junglelib.contrabass()` are the two good physical
  strings in the engine, and both are right about the physics and wrong about
  the instrument: one is a distorted guitar, the other is a double bass in a
  wooden box. A Precision bass is a plank. Its low end is the pickup, not a
  body resonance, and its top is a wound roundwound string being pulled by a
  finger rather than struck by a plectrum.

What is reused, because it genuinely fits and nothing about it is 1984:

  `funklib.brass`     a real section - every player arrives a few
                      milliseconds apart, a few cents out, and scoops UP to
                      the note. That is a horn line in any decade.
  `houselib.solina`   an ARP Solina: one divide-down oscillator per pitch
                      class, gated rather than retriggered, through a
                      three-rate bucket brigade. It IS the string machine on
                      every Italo and every late-ABBA record.
  `latinlib.conga`    a modal membrane with a fixed shell resonance. Disco
                      percussion is Latin percussion; it arrived by the same
                      road.

What this module adds:

  the kit      dkick dsnare drim dhat dopen dtamb dclap dtom dcrash
  the band     dbass    a Precision through an Ampeg, rendered a bar at a time
               chank    the sixteenth-note muted chank, four strings, a cab
               violins  a string SECTION playing a LINE, not a chord
               voice    the singer, and it is a synthesiser because the
                        alternative is a robot pronouncing vowels
  the room     droom, tape

THE OPEN HAT IS AN INSTRUMENT, NOT A LONGER ENVELOPE.

The offbeat open hat is the genre's signature and it is also the fastest way
to ruin the record. At 120 BPM four of them a bar arrive 500 ms apart, so a
909's own 470 ms decay means every hat is still sounding when the next one
starts and the top of the track becomes one continuous sheet of sand. `dopen`
is built as what it physically is - two discs, so an inharmonic mode set with
a DIFFERENT DECAY PER MODE, plus noise for the sizzle - and it is windowed to
silence well before the next one. Measured: -26 dB in about 190 ms, which is
1.5 steps, against a step of 125 ms.

Nothing in this module normalises a hit to a fixed peak and nothing repeats
its noise. Every voice takes a `seed`, and the caller moves it per event.
"""
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import fftconvolve

import core
from core import *                                              # noqa: F401,F403
from core import _ftrack, _reverb_ir

import funklib
import houselib
import latinlib
from funklib import brass, synbrass                             # noqa: F401
from houselib import solina, _bbd                               # noqa: F401
from latinlib import conga, bongo, guiro, maraca, CONGA, QUINTO, TUMBA  # noqa: F401

BAR, STEP = core.set_grid(bpm=120)
SWING = 0.0


def set_tempo(bpm, beats=4):
    """Move the grid - here and in every module this one borrows from.

    Each genre module keeps its own BAR/STEP, and the ones that render a
    whole section at a time (`solina`) read them directly. Setting only
    core's grid leaves those stale, and a string machine rendered against a
    123 BPM bar in a 120 BPM track drifts a beat every ninety seconds."""
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    for m in (funklib, houselib, latinlib):
        m.BAR, m.STEP = BAR, STEP
        if hasattr(m, 'BPM'):
            m.BPM = BPM
    core._SEG_CACHE.clear()
    return BAR, STEP


def sw(step):
    """Swing the offbeat sixteenths only. Disco barely swings - 52-54% is the
    whole of it - but a dead-straight sixteenth guitar is a sequencer."""
    return step + (SWING if int(step) % 2 else 0.0)


# ================================================================== tape ===
def _asym(x, g=1.0):
    """One tape stage. `tanh` is an ODD function, so driving anything into it
    hard enough leaves odd harmonics only - which is a square wave, and a
    square wave is a chiptune. Tape is asymmetric: the two directions of
    magnetisation do not saturate identically, so it makes even harmonics as
    well, and even harmonics are octaves and fifths. That is the entire
    difference between 'warm' and 'buzzing'."""
    y = np.where(x >= 0, np.tanh(g * x), np.tanh(0.78 * g * x) * 0.90)
    return (y - y.mean(axis=0)).astype(np.float32)


def tape(x, drive=1.0, bump=0.9, hiss=1.0, top=15000.0, wow=1.0, seed=0):
    """Two-inch tape at 30 ips, and a console in front of it.

    Four things, none of which is an EQ curve:

    * **The head bump.** The gap between the record and replay heads makes a
      broad resonance an octave or two below where the tape is flat - a dB
      or two around 55 Hz. It is why records from this decade have a bottom
      that a highpass cannot put back.
    * **Asymmetric saturation**, above.
    * **The top goes.** Not a brick wall; a slow slump from about 12 kHz.
    * **Wow and flutter**, at a third of a hertz and at nine, and both very
      small. A tape machine that is perfectly in tune with itself is a DAW.

    The input is normalised before the drive stage, so `drive` means what it
    says rather than meaning `drive x whatever this bus happened to peak at`.
    """
    n = len(x)
    pk = float(np.abs(x).max())
    if pk < 1e-9:
        return x
    y = x / pk
    y = y + bump * 0.28 * bandpass(y, 38, 78, order=2)
    y = _asym(y, 1.0 + 1.6 * drive)
    y = lp(y, top, order=2)
    y = y - 0.10 * hp(y, 11000, order=2)
    if wow:
        t = np.arange(n) / SR
        rs = np.random.RandomState(7700 + seed)
        cents = (0.055 * wow * np.sin(2 * np.pi * 0.33 * t + rs.rand() * 6)
                 + 0.018 * wow * np.sin(2 * np.pi * 9.1 * t + rs.rand() * 6))
        idx = np.clip(np.cumsum(1 + cents / 1200.0 * np.log(2)), 0, n - 1)
        base = np.arange(n)
        y = np.stack([np.interp(idx, base, y[:, c]) for c in range(2)], 1)
    if hiss:
        rs = np.random.RandomState(9100 + seed)
        y = y + hp(rs.standard_normal((n, 2)).astype(np.float32) * 4.5e-4 * hiss,
                   400, order=2)
    return (y * pk).astype(np.float32)


_ROOM_IR = {}

def droom(buf, decay=0.62, wet=0.20, tone=6200, pre=0.008, block_bars=16):
    """One room for the whole kit, and the TAIL only - add it to the bus.

    Seven people in one room means one set of reflections, not seven reverbs.
    Convolved in blocks so a six-minute buffer does not need a six-minute
    FFT."""
    key = (round(decay, 3), int(tone))
    if key not in _ROOM_IR:
        _ROOM_IR[key] = _reverb_ir(decay, tone)
    ir = _ROOM_IR[key]
    out = np.zeros_like(buf)
    k = int(pre * SR)
    blk = int(block_bars * BAR)
    for a in range(0, len(buf), blk):
        seg = buf[a:a + blk]
        w = np.stack([fftconvolve(seg[:, c], ir[:, c]) for c in range(2)], 1)
        e = min(a + k + len(w), len(out))
        out[a + k:e] += w[:e - a - k].astype(np.float32)
    return (buf + wet * hp(lp(out, 7000, order=2), 240, order=2)).astype(np.float32)


# =================================================================== kit ===
@cached
def dkick(dur_steps=4, tune=52.0, gain=1.0, beater=1.0, decay=0.150,
          shell=1.0, seed=0):
    """A 22" bass drum, felt beater, front head on, a blanket inside.

    The three things that separate this from a 909 and from `fkick`:

    * **The beater is felt.** A 909's attack is a filtered impulse - a click
      at 2-4 kHz. Felt on a calf head is a KNOCK: a short burst centred
      around 1.2 kHz with almost nothing above 4, and it is the sound of a
      soft object hitting a taut one.
    * **The shell.** A wooden drum an inch thick and 22 inches across rings
      around 95-160 Hz for a tenth of a second after the head has stopped.
      That band is what makes a kick sound like a drum rather than a sine
      with an envelope on it, and it is the first thing a synthesised kick
      leaves out.
    * **A pillow, not a gate.** The decay is 165 ms because there is a
      blanket against the batter head, which is what everybody did in 1977
      and why the records sound like this.

    `seed` moves the beater's noise per hit. Four hundred identical
    transients a minute is a metronome, not a drummer."""
    n, t = steps(dur_steps, floor=int(0.30 * SR))
    rng = np.random.default_rng(seed * 977 + 3)
    f = tune * (1 + 1.35 * np.exp(-t / 0.020))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    body += 0.34 * np.sin(2 * np.pi * tune * 2.02 * t + 0.7) * np.exp(-t / 0.055)
    st = stereo(body)
    if shell:
        wood = rng.standard_normal(n) * np.exp(-t / 0.028)
        st = st + shell * 0.55 * bandpass(stereo(wood), 95, 165, order=2)
        st = st + shell * 0.22 * bandpass(st, 210, 340, order=2)
    if beater:
        kn = rng.standard_normal(n) * np.exp(-t / 0.0055)
        kn = kn + np.sin(2 * np.pi * 1180 * t) * np.exp(-t / 0.0035) * 0.55
        st = st + bandpass(stereo(kn), 700, 4600, order=2) * 0.85 * beater
    st = _asym(st / max(np.abs(st).max(), 1e-9), 1.45)
    st = st - 0.30 * bandpass(st, 380, 700, order=2)      # the boxy dip
    st = hp(lp(st, 8500, order=2), 32, order=2)
    return norm(st * adsr(n, a=0.0004, r=0.020)[:, None], 0.93) * gain


@cached
def dsnare(dur_steps=4, tune=196.0, gain=1.0, snap=1.0, decay=0.125,
           room=1.0, seed=0, ghost=0.0):
    """A 14x5.5 wood shell with the wires on, three feet from a ribbon mic.

    A snare is two heads and forty strands of wire, and the wires are a
    separate instrument that happens to be bolted to the drum: they rattle
    for longer than the head rings and they carry everything above 2 kHz.
    `ghost` is the drummer's left hand at a fifth of the force - which is not
    the same hit quieter, because a soft stroke does not drive the wires at
    all, so it is nearly all shell and no sizzle."""
    n, t = steps(dur_steps, floor=int(0.42 * SR))
    rng = np.random.default_rng(seed * 811 + 5)
    v = 1.0 - 0.72 * ghost
    pd = 1 + 0.17 * np.exp(-t / 0.010)
    head = (np.sin(2 * np.pi * tune * pd * t) * np.exp(-t / 0.052)
            + 0.52 * np.sin(2 * np.pi * tune * 1.593 * pd * t + 1.1) * np.exp(-t / 0.036)
            + 0.30 * np.sin(2 * np.pi * tune * 2.135 * t + 2.3) * np.exp(-t / 0.026)
            + 0.16 * np.sin(2 * np.pi * tune * 2.917 * t + 0.4) * np.exp(-t / 0.017))
    nz = rng.standard_normal(n)
    wires = bandpass(stereo(nz), 1900, 9500, order=2) * (
        np.exp(-t / (decay * (0.55 + 0.45 * v))))[:, None] * 1.30 * snap * v ** 1.4
    stick = bandpass(stereo(nz * np.exp(-t / 0.0014)), 2400, 8000, order=2) * 0.45 * v
    st = stereo(head * (0.85 + 0.35 * v))
    st = st + 0.30 * bandpass(st, 230, 420, order=2)       # the shell
    dry = _asym((st + wires + stick) / max(np.abs(st + wires + stick).max(), 1e-9), 1.55)
    if room:
        ir = _reverb_ir(0.45, 7200)
        wet = np.stack([fftconvolve(dry[:, c], ir[:, c])[:n] for c in range(2)], 1)
        dry = dry + room * 0.30 * hp(wet.astype(np.float32), 320, order=2)
    dry = hp(lp(dry, 13500, order=2), 120, order=2)
    return (dry * adsr(n, a=0.0005, r=0.020)[:, None]).astype(np.float32) * gain * 1.00


@cached
def drim(dur_steps=2, tune=780.0, gain=1.0, seed=0):
    """Cross-stick: the shoulder of the stick on the rim with the tip resting
    on the head. Almost no wires, all wood."""
    n, t = steps(dur_steps, floor=int(0.14 * SR))
    rng = np.random.default_rng(seed * 613 + 7)
    x = (np.sin(2 * np.pi * tune * t) * np.exp(-t / 0.020)
         + 0.6 * np.sin(2 * np.pi * tune * 1.74 * t + 1.4) * np.exp(-t / 0.012))
    click = rng.standard_normal(n) * np.exp(-t / 0.0016)
    st = bandpass(stereo(x) + 0.7 * stereo(click), 420, 6500, order=2)
    st = np.tanh(1.7 * st)
    return (st * adsr(n, a=0.0004, r=0.012)[:, None]).astype(np.float32) * gain * 0.40


# The six inharmonic ratios of a pair of hi-hat cymbals. Two discs of the same
# alloy are never quite the same disc, which is why the set is not a series.
_HAT_R = (1.000, 1.342, 1.612, 1.996, 2.441, 2.786)

@cached
def dhat(dur_steps=1, gain=1.0, tone=1.0, decay=0.028, seed=0, foot=0.0):
    """Closed. Two discs clamped together by a foot, struck near the edge:
    a very short burst of metal and air, and nothing else. 28 ms."""
    n, t = steps(dur_steps, floor=int(0.045 * SR))
    rng = np.random.default_rng(seed * 439 + 11)
    x = sum(np.sin(2 * np.pi * 3150 * r * tone * t + rng.random() * 6)
            for r in _HAT_R) / 6.0
    x = x * 0.55 + rng.standard_normal(n) * 0.85
    st = hp(stereo(x), 5200 - 900 * foot, order=2)
    st = st + 0.40 * bandpass(st, 7000, 12000, order=2)
    env = np.exp(-t / (decay * (1 + 1.4 * foot))) * adsr(n, a=0.0004, r=0.008)
    return (np.tanh(1.4 * st) * env[:, None]).astype(np.float32) * gain * 0.30


@cached
def dopen(dur_steps=3, gain=1.0, tone=1.0, seed=0, tail=0.165, sizzle=1.0):
    """The offbeat open hat, and the reason this module exists.

    An open hat is not a closed hat with the envelope opened. It is the same
    two discs with the foot OFF, so they are free to ring against each other
    - and metal sheds its high modes first, which means the sound changes
    colour as it dies. One envelope across all six ratios is a sample being
    faded out; six different ones is an object.

    `tail` is the hard stop. At 120 BPM the next offbeat arrives 500 ms
    later, and a hat that is still sounding when it does turns the top of the
    record into a continuous sheet of sand - the single most common way this
    genre goes wrong. Everything is windowed to silence by `tail * 1.6`
    seconds with a raised cosine, which is what a real player's foot does and
    what an exponential never does."""
    n, t = steps(dur_steps, floor=int(0.36 * SR))
    rng = np.random.default_rng(seed * 353 + 13)
    x = np.zeros(n)
    for i, r in enumerate(_HAT_R):
        # the top of the pair dies first
        tau = tail * (0.98 - 0.11 * i) * (0.9 + 0.2 * rng.random())
        x += np.sin(2 * np.pi * 3150 * r * tone * t + rng.random() * 6) * np.exp(-t / tau)
    x /= 6.0
    air = rng.standard_normal(n) * np.exp(-t / (tail * 0.62)) * 0.95 * sizzle
    st = hp(stereo(x * 0.75 + air), 4700, order=2)
    st = st + 0.45 * bandpass(st, 6500, 13000, order=2)
    # the hard stop: a raised cosine to silence, not an exponential that never
    # quite gets there
    stop = int(min(tail * 1.65, dur_steps * STEP / SR) * SR)
    w = np.ones(n)
    if stop < n:
        L = min(int(0.045 * SR), stop)
        w[stop - L:stop] = 0.5 * (1 + np.cos(np.linspace(0, np.pi, L)))
        w[stop:] = 0.0
    env = w * adsr(n, a=0.0005, r=0.010)
    return (np.tanh(1.35 * st) * env[:, None]).astype(np.float32) * gain * 0.34


@cached
def dtamb(dur_steps=1, gain=1.0, seed=0, ring=0.0, shake=0.0):
    """A dozen little cymbals on a wooden hoop, and they are all slightly
    different sizes - which is why one band-passed noise burst has never
    sounded like a tambourine. `shake` is the hoop moving back the other way
    a few milliseconds later; `ring` is how long the jingles are allowed to
    keep talking about it."""
    n, t = steps(dur_steps, floor=int(0.10 * SR))
    rng = np.random.default_rng(seed * 271 + 17)
    x = rng.standard_normal(n) * 0.55
    for r in (1.0, 1.13, 1.27, 1.41, 1.62, 1.79, 2.04, 2.31):
        x += np.sin(2 * np.pi * 5100 * r * t + rng.random() * 6) * (0.22 + 0.10 * rng.random())
    st = hp(stereo(x), 4400, order=2)
    env = np.exp(-t / (0.011 + 0.20 * ring))
    if shake:
        d = int((0.020 + 0.010 * rng.random()) * SR)
        e2 = np.zeros(n); e2[d:] = np.exp(-np.arange(n - d) / SR / 0.010) * shake
        env = env + e2
    return (np.tanh(1.3 * st) * (env * adsr(n, a=0.0004, r=0.014))[:, None]
            ).astype(np.float32) * gain * 0.26


@cached
def dclap(dur_steps=3, gain=1.0, seed=0, hands=9, spread=1.0):
    """A room of people, not a drum machine's four bursts.

    Nine pairs of hands do not land together and are not standing in the same
    place, so this is nine noise bursts scattered over 45 ms, each panned
    somewhere different, and then the room they are all in. The scatter is
    what a clap IS - tighten it and it becomes a snare."""
    n, t = steps(dur_steps, floor=int(0.42 * SR))
    rng = np.random.default_rng(seed * 199 + 19)
    st = np.zeros((n, 2), dtype=np.float32)
    for h in range(hands):
        d = int(abs(rng.normal(0.0, 0.013)) * SR)
        if d >= n - 64:
            continue
        L = n - d
        b = rng.standard_normal(L) * np.exp(-np.arange(L) / SR / (0.0035 + 0.004 * rng.random()))
        one = np.zeros(n); one[d:] = b
        lo, hi = 700 * (0.8 + 0.5 * rng.random()), 3600 * (0.8 + 0.5 * rng.random())
        st += panned(bandpass(stereo(one), lo, hi, order=2),
                     rng.uniform(-0.75, 0.75) * spread) / hands ** 0.6
    st = st + bandpass(stereo(rng.standard_normal(n) * np.exp(-t / 0.055)),
                       900, 3200, order=2) * 0.35
    ir = _reverb_ir(0.55, 6000)
    wet = np.stack([fftconvolve(st[:, c], ir[:, c])[:n] for c in range(2)], 1)
    st = st + 0.42 * hp(wet.astype(np.float32), 500, order=2)
    st = np.tanh(1.5 * st / max(np.abs(st).max(), 1e-9))
    return (hp(st, 320, order=2) * adsr(n, a=0.0006, r=0.030)[:, None]
            ).astype(np.float32) * gain * 0.48


@cached
def dtom(dur_steps=2, tune=150.0, gain=1.0, seed=0, size=1.0):
    """An acoustic tom, tuned. Two head modes and a shell - NOT the Simmons
    pitch-dive, which is the other decade's tom and would drag this record
    six years forward on its own."""
    n, t = steps(dur_steps, floor=int(0.34 * SR))
    rng = np.random.default_rng(seed * 149 + 23)
    f = tune * (1 + 0.19 * np.exp(-t / 0.028))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) * np.exp(-t / (0.30 * size))
         + 0.44 * np.sin(1.594 * ph + 1.2) * np.exp(-t / (0.14 * size))
         + 0.20 * np.sin(2.136 * ph + 0.3) * np.exp(-t / (0.075 * size)))
    head = bandpass(stereo(rng.standard_normal(n) * np.exp(-t / 0.0055)),
                    600, 4200, order=2) * 0.58
    st = stereo(x) + head
    st = st + 0.28 * bandpass(st, tune * 1.15, tune * 2.1, order=2)
    st = _asym(st / max(np.abs(st).max(), 1e-9), 1.35)
    return (hp(st, 60, order=2) * adsr(n, a=0.0006, r=0.025)[:, None]
            ).astype(np.float32) * gain * 0.55


@cached
def dcrash(dur_steps=16, gain=1.0, seed=0, size=1.0, decay=1.5):
    """An 18" crash. Ten inharmonic modes, each with its own decay, and the
    top half gone within a second - a cymbal is bright at the moment of the
    strike and dark eight bars later, and a single envelope cannot do that."""
    n, t = steps(dur_steps, floor=int(1.6 * SR))
    rng = np.random.default_rng(seed * 131 + 29)
    ratios = (1.0, 1.41, 1.83, 2.29, 2.77, 3.41, 4.13, 5.32, 6.71, 8.24, 10.1)
    x = np.zeros(n)
    for i, r in enumerate(ratios):
        x += (np.sin(2 * np.pi * 640 / size * r * t + rng.random() * 6)
              * np.exp(-t / (decay * (1.05 - 0.075 * i))))
    x = x / len(ratios) * 1.1 + rng.standard_normal(n) * np.exp(-t / (decay * 0.42)) * 0.80
    st = hp(stereo(x), 1500, order=2)
    st = st + 0.22 * bandpass(st, 4500, 9000, order=2)
    st = lp(st, 12500, order=2)
    st = widen(np.tanh(1.25 * st), 1.20)
    return (st * adsr(n, a=0.0008, r=0.30)[:, None]).astype(np.float32) * gain * 0.30


# ================================================================== bass ===
@cached
def dbass(notes, dur_steps=16, tail=6.0, level=1.0, glide=0.016, take=0,
          bright=1.0, drive=1.55, decay=0.55, growl=1.0, amp_hi=3900.0,
          h2=0.30, h3=0.11):
    """A Precision bass, fingered, into an Ampeg, rendered a bar at a time.

    `notes` is `(step, midi[, decay_s[, vel]])`.

    A bass guitar is ONE string that keeps vibrating, so this is one
    continuous phase track through the whole bar with an amplitude that
    swells at every note and never returns to zero. Rendering the octave
    eighths as sixteen independent segments breaks the fundamental: adjacent
    tails meet at unrelated phases and cancel, and what the ear gets back is
    grit where the low end should be.

    What makes it a Precision rather than a double bass or a Rickenbacker:

    * **A plank, not a box.** `junglelib.contrabass` spends most of its
      character on three body resonances, because an upright is a wooden box
      and that is why a 49 Hz note is audible at all. A solid alder body has
      almost no resonance worth modelling, and putting one there is what
      makes a synthesised electric bass sound acoustic and wrong. All the
      colour here comes from the PICKUP - a split coil about a fifth of the
      way up from the bridge, whose comb kills every fifth partial, and whose
      coil resonates against the cable a few kilohertz up.
    * **A finger, not a plectrum.** The pad of a finger pulls the string and
      lets go, so the corner it leaves is rounded: less of the top partials
      than a pick, and a soft thud from the string slapping the last fret
      instead of a bright click.
    * **The growl.** A wound roundwound under a lot of compression puts a
      hard band of energy at 700 Hz - 2.5 kHz that is most of why this
      instrument is audible on a transistor radio, and none of which is the
      fundamental.

    `decay` is the palm. Disco plays octave eighths half-muted, so 0.13-0.2 s
    per note gives the staccato bounce and 0.5-1.2 s gives the sustained line
    under a chorus - and because the envelope max-accumulates, a slow line
    over a fast one never breaks."""
    n = int((dur_steps + tail) * STEP)
    t = np.arange(n) / SR
    evs = sorted((float(e[0]), int(e[1]),
                  float(e[2]) if len(e) > 2 else decay,
                  float(e[3]) if len(e) > 3 else 1.0) for e in notes)
    rng = np.random.default_rng(4400 + take)

    f = _ftrack([(st_, nt) for st_, nt, _, _ in evs], n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR

    amp = np.zeros(n)
    for st_, nt, dec, vel in evs:
        k = min(int(st_ * STEP), n - 1)
        np.maximum(amp[k:], vel * np.exp(-np.arange(n - k) / SR / max(dec, 0.02)),
                   out=amp[k:])
    amp = np.maximum(uniform_filter1d(amp, max(int(0.005 * SR), 3)), 0.0)

    # the fundamental, unbroken
    low = (np.sin(ph) + h2 * np.sin(2 * ph) + h3 * np.sin(3 * ph)) * amp

    # the finger, discrete
    pick = np.zeros(n)
    thud = np.zeros(n)
    for i, (st_, nt, dec, vel) in enumerate(evs):
        k = min(int(st_ * STEP), n - 1)
        m = min(n - k, int(0.30 * SR))
        if m < 64:
            continue
        pick[k:k + m] += string(
            midi(nt), m, decay=max(dec, 0.16) * 0.75, damp=0.052,
            pick=0.26, pickup=0.19,                 # the split coil
            B=3.4e-4 * (55.0 / max(midi(nt), 20.0)) ** 0.35,
            top=4600.0, bright=1.0, res_hz=2650.0, res_q=1.9,
            tilt=-0.28,                             # a finger, not a plectrum
            polar=0.85, seed=int(3907 * take + 53 * nt + 11 * i)) * vel
        c = min(n - k, int(0.014 * SR))
        thud[k:k + c] += (rng.standard_normal(c)
                          * np.exp(-np.arange(c) / SR / 0.0038)) * 0.55 * vel

    st_p = stereo(pick)
    out = (lp(stereo(low), 320, order=4) * 0.62
           + hp(st_p, 150, order=2) * 1.00
           + lp(stereo(thud), 900, order=2) * 0.22)
    if growl:
        out = out + growl * 0.55 * np.tanh(drive * 2.2 * bandpass(out, 700, 2500, order=2))
    out = out + 0.30 * bandpass(out, 260, 560, order=2) * bright
    out = _asym(out / max(np.abs(out).max(), 1e-9), 1.15 * drive)
    # the Ampeg: a convolved cabinet, not a shelf. Its own resonance is what
    # a bass rig sounds like, and it happens over time.
    out = cab(out, seed=take % 4, low=42.0, high=amp_hi, cone=1.45,
              presence=0.55, mic=0.55)
    out = hp(out, 34, order=2)
    return (out * adsr(n, a=0.0010, r=0.004)[:, None]).astype(np.float32) * level * 0.42


# ============================================================== the chank ===
@cached
def chank(notes, dur_steps=1.0, level=1.0, take=0, mute=0.85, bright=1.0,
          up=False, spread=0.0032, ring=0.045, drive=1.0):
    """The sixteenth-note muted chank - the second most disco thing there is.

    Four strings, struck one after another about three milliseconds apart,
    each with its own few cents of error and its own seed, and every one of
    them damped by the heel of the right hand so it is gone before the next
    sixteenth arrives. `up` reverses the order, because an upstroke starts at
    the thin end: same notes, different instrument, and alternating them is
    what makes sixteen hits a bar read as a hand rather than a sequencer.

    A ninth chord, please. The chank's whole function is to put a bright,
    dense, mid-range rhythm where the vocal is not, and a bare triad up there
    is a rock guitar."""
    n, t = steps(dur_steps, floor=int(0.075 * SR))
    order = list(range(len(notes)))
    if up:
        order = order[::-1]
    rng = np.random.default_rng(7100 * take + int(sum(notes)) + (7 if up else 0))
    x = np.zeros(n)
    for j, i in enumerate(order):
        nt = notes[i]
        d = int((0.0030 * j + 0.0012 * rng.random()) * SR)
        if d >= n - 32:
            continue
        f = midi(nt) * (1 + spread * (rng.random() - 0.5) * 2)
        x[d:] += string(f, n - d,
                        decay=ring * (1 - 0.72 * mute) + 0.010,
                        damp=0.045 + 0.075 * mute,
                        pick=0.14 + 0.06 * rng.random(), pickup=0.27,
                        B=1.6e-4, top=6800.0, res_hz=3400.0, res_q=2.2,
                        tilt=-0.10 + 0.25 * (1 - mute),
                        polar=0.7,
                        seed=int(2803 * take + 29 * nt + 5 * j)) * (1 - 0.10 * j)
    st = stereo(x / max(len(notes), 1))
    st = _asym(st / max(np.abs(st).max(), 1e-9), 1.25 * drive)
    st = cab(st, seed=take % 3, low=98.0, high=6400.0 * bright, cone=0.42,
             presence=1.25, mic=0.85)
    env = np.exp(-t / (0.028 + 0.10 * (1 - mute))) * adsr(n, a=0.0005, r=0.010)
    # No norm(). The whole part is the difference between the hits that ring
    # and the hits that only tick.
    return (st * env[:, None]).astype(np.float32) * level * (0.55 - 0.20 * mute)


# ============================================================== the strings ==
def violins(notes, bars=1, tail=8.0, voices=7, level=1.0, octave=0.0,
            cutoff=6200.0, bow=1.0, vib=1.0, drift=1.0, seed=0,
            attack=0.055, gliss=0.010, sub=0.0, body=1.0):
    """A string SECTION playing a LINE.

    `core.ens` is the right idea for a chord - several players, independent
    entries, independent intonation - and it renders a static block for a
    fixed length. Disco strings do not play blocks. They play a phrase, in
    octave unison, with a bow stroke on every note and a vibrato that arrives
    after the note does; and the phrase is the tune, or the answer to it.

    `notes` is `(step, midi, length_steps[, vel])`, and every one of the
    seven players gets its own copy of it - its own entry lag per stroke, its
    own slow random walk of intonation a few cents wide, its own vibrato rate
    between 5.1 and 6.5 Hz that ramps in over 200 ms from each attack. Sum
    those and the beating is aperiodic, which is what a section is; a
    chorused saw is one player standing in a hall of mirrors.

    `gliss` is the port between notes. Small (10 ms) it is a violinist's
    finger; large (0.25 s) the same function is the rising sweep that gets
    this genre from one section to the next.

    The body resonances are fixed and that is correct here, unlike a modelled
    cabinet: the box does not change size when the player changes note, and
    the air resonance near 275 Hz and the wood near 460 are why a violin
    sounds like a violin. The bridge hill at 2-3 kHz is why a section is
    audible over a horn line."""
    n = int(bars * BAR + tail * STEP)
    t = np.arange(n) / SR
    evs = sorted((float(e[0]), int(e[1]), float(e[2]),
                  float(e[3]) if len(e) > 3 else 1.0) for e in notes)
    if not evs:
        return np.zeros((n, 2), dtype=np.float32)
    rs = np.random.RandomState(6100 + seed)
    fmax = max(midi(nt) for _, nt, _, _ in evs)
    kmax = int(np.clip(cutoff * 1.7 / max(min(midi(nt) for _, nt, _, _ in evs), 60), 6, 34))

    layers = [(1.0, 1.0)] + ([(0.5, octave)] if octave else []) \
        + ([(0.25, sub)] if sub else [])
    out = np.zeros((n, 2), dtype=np.float64)
    for mul, lg in layers:
        for v in range(voices):
            lag = rs.uniform(0.006, 0.028)
            cents = rs.uniform(-7, 7) * drift
            walk = uniform_filter1d(rs.randn(n), max(int(0.40 * SR), 3))
            walk *= drift * 5.0 / max(np.abs(walk).max(), 1e-9)
            vr = rs.uniform(5.1, 6.5)
            vph = rs.rand() * 6.283

            # this player's own note list, entered late
            shift = lag * SR / STEP
            f = _ftrack([(st_ + shift, nt) for st_, nt, _, _ in evs], n, gliss)
            # vibrato, ramping in from each attack the way a finger's does
            ramp = np.zeros(n)
            for st_, nt, ln, vl in evs:
                k = min(int((st_ + shift) * STEP), n - 1)
                L = min(n - k, int(ln * STEP) + int(0.35 * SR))
                ramp[k:k + L] = np.minimum(np.arange(L) / SR / 0.22, 1.0)
            vcents = vib * 11.0 * np.sin(2 * np.pi * vr * t + vph) * ramp
            ratio = 2.0 ** ((cents + walk + vcents) / 1200.0)
            ph = 2 * np.pi * np.cumsum(f * mul * ratio) / SR + rs.rand() * 6.283
            y = saw_ph(ph, fmax * mul * 1.05, kmax=kmax)

            # the bow: one stroke per note, and the attack is the instrument
            env = np.zeros(n)
            for st_, nt, ln, vl in evs:
                k = min(int((st_ + shift) * STEP), n - 1)
                L = min(n - k, int(ln * STEP))
                if L < 64:
                    continue
                a = min(int(attack * rs.uniform(0.75, 1.4) * SR), L // 2)
                r = min(int(0.13 * SR), n - k - L)
                seg = np.ones(L + r) * vl
                seg[:a] = np.linspace(0, 1, a) ** 1.5 * vl
                if r > 2:
                    seg[L:] = vl * np.exp(-np.linspace(0, 4.0, r))
                np.maximum(env[k:k + len(seg)], seg, out=env[k:k + len(seg)])
            env = np.maximum(uniform_filter1d(env, max(int(0.008 * SR), 3)), 0.0)

            pan = (v / max(voices - 1, 1) - 0.5) * 1.5 + rs.uniform(-0.15, 0.15)
            ang = (np.clip(pan, -1, 1) + 1) * np.pi / 4
            yv = y * env * lg
            out[:, 0] += yv * np.cos(ang)
            out[:, 1] += yv * np.sin(ang)

    out = (out / max(voices * len(layers), 1) ** 0.72).astype(np.float32)
    if bow:
        rs2 = np.random.RandomState(6200 + seed)
        nz = bandpass(np.stack([rs2.randn(n), rs2.randn(n)], 1).astype(np.float32),
                      1600, 7500, order=2)
        amp = np.maximum(uniform_filter1d(np.abs(out).max(axis=1),
                                          int(0.02 * SR)), 0.0)[:, None]
        out = out + nz * amp * bow * 0.10
    y = lp(out, cutoff, 4)
    if body:
        y = (y
             + body * 0.30 * bandpass(y, 240, 310, order=2)      # the air
             + body * 0.26 * bandpass(y, 400, 540, order=2)      # the main wood
             + body * 0.34 * bandpass(y, 2100, 3200, order=2))   # the bridge hill
        y = y - body * 0.16 * bandpass(y, 800, 1200, order=2)
    y = hp(y, 150 if not octave else 95, order=2)
    return np.tanh(1.15 * y).astype(np.float32) * level * 0.62


def sweep(f_lo, f_hi, dur_steps, level=1.0, voices=6, seed=0, cutoff=5200.0,
          shape=1.6, down=False):
    """The string glissando: the whole section running up (or down) the
    fingerboard in unison. It is the transition of the genre, and it is not a
    riser - a riser is noise, this is a chord with somewhere to go."""
    n = int(dur_steps * STEP)
    t = np.arange(n) / SR
    rs = np.random.RandomState(6600 + seed)
    u = (np.linspace(0, 1, n) ** shape)
    if down:
        u = 1 - u
    out = np.zeros((n, 2), dtype=np.float64)
    for v in range(voices):
        cents = rs.uniform(-9, 9)
        jit = uniform_filter1d(rs.randn(n), int(0.25 * SR))
        jit *= 7.0 / max(np.abs(jit).max(), 1e-9)
        f = midi(f_lo) * (midi(f_hi) / midi(f_lo)) ** u * 2 ** ((cents + jit) / 1200)
        ph = 2 * np.pi * np.cumsum(f) / SR + rs.rand() * 6.283
        y = saw_ph(ph, float(f.max()) * 1.05, kmax=18)
        pan = (v / max(voices - 1, 1) - 0.5) * 1.5
        ang = (np.clip(pan, -1, 1) + 1) * np.pi / 4
        out[:, 0] += y * np.cos(ang)
        out[:, 1] += y * np.sin(ang)
    out = (out / voices ** 0.72).astype(np.float32)
    env = np.minimum(t / 0.12, 1.0) * (0.88 + 0.12 * np.linspace(0, 1, n))
    env *= adsr(n, a=0.010, r=0.14)
    # the tracking lowpass: as the fundamental climbs an octave the cutoff
    # comes down, so the partial count falls and the sweep does not turn into
    # a pile of energy where the ear is least forgiving
    y = morph_lp(out * env[:, None], cutoff * 0.34, cutoff,
                 np.clip(1.0 - 0.72 * u, 0, 1), bands=6, res=0.35)
    y = y + 0.16 * bandpass(y, 1900, 2900, order=2)
    return np.tanh(1.15 * hp(y, 170, order=2)).astype(np.float32) * level * 0.42


# ================================================================ the voice ==
def voice(notes, bars=1, tail=8.0, level=1.0, glide=0.038, det=9.0, take=0,
          cut_lo=620.0, cut_hi=4600.0, vib=1.0, ping=0.55, breath=1.0,
          sq=0.42, res=0.55, attack=0.014, wide=1.0):
    """The singer, and it is a synthesiser on purpose.

    This record has a topline and no vocalist. Formant synthesis would give
    it a robot pronouncing vowels; a Jupiter played legato gives it the two
    things that actually read as singing - it SLIDES between notes, and its
    vibrato arrives a fifth of a second after the note does, never with it.

    Three saws a few cents apart plus a pulse for the body, one continuous
    phase through the whole phrase so the portamento is a portamento; a
    filter that opens on every attack and closes again, which is the breath
    behind a sung note; a sine at twice the phase whose index dies in 70 ms,
    which is the consonant at the front of a word. Integer ratio and a small
    index, because a big one at a non-integer ratio is a bell and this is
    supposed to be a person.

    `notes` is `(step, midi, length_steps[, vel])`."""
    n = int(bars * BAR + tail * STEP)
    t = np.arange(n) / SR
    evs = sorted((float(e[0]), int(e[1]), float(e[2]),
                  float(e[3]) if len(e) > 3 else 1.0) for e in notes)
    if not evs:
        return np.zeros((n, 2), dtype=np.float32)
    rs = np.random.RandomState(8100 + take)

    f = _ftrack([(st_, nt) for st_, nt, _, _ in evs], n, glide)
    ramp = np.zeros(n)
    amp = np.zeros(n)
    opn = np.zeros(n)
    for st_, nt, ln, vl in evs:
        k = min(int(st_ * STEP), n - 1)
        L = min(n - k, int(ln * STEP))
        if L < 64:
            continue
        ramp[k:k + L] = np.minimum(np.arange(L) / SR / 0.20, 1.0)
        a = min(int(attack * SR), L // 2)
        r = min(int(0.11 * SR), n - k - L)
        seg = np.ones(L + r) * vl
        seg[:a] = np.linspace(0, 1, a) ** 1.3 * vl
        if r > 2:
            seg[L:] = vl * np.exp(-np.linspace(0, 4.2, r))
        np.maximum(amp[k:k + len(seg)], seg, out=amp[k:k + len(seg)])
        M = min(n - k, int(0.26 * SR))
        np.maximum(opn[k:k + M], np.exp(-np.arange(M) / SR / 0.085) * vl, out=opn[k:k + M])
    # Clamp AFTER the smoother, not before: uniform_filter1d is a running
    # sum, so over a stretch of exact zeros it returns values of order
    # -1e-14, and `opn ** 1.5` on one of those is a NaN that propagates
    # through every filter after it and renders the bus silent.
    amp = np.maximum(uniform_filter1d(amp, max(int(0.004 * SR), 3)), 0.0)
    opn = np.maximum(uniform_filter1d(opn, max(int(0.006 * SR), 3)), 0.0)

    vcents = vib * 13.0 * np.sin(2 * np.pi * 5.6 * t + rs.rand() * 6) * ramp
    fmax = max(midi(nt) for _, nt, _, _ in evs) * 1.06
    x = np.zeros(n)
    for k, d in enumerate((-det, 0.0, det)):
        ph = 2 * np.pi * np.cumsum(f * 2 ** ((d + vcents) / 1200.0)) / SR + rs.rand() * 6.283
        x += saw_ph(ph, fmax, kmax=46) * (0.85 if d else 1.0)
        if k == 1:
            # the consonant: an octave-up ping that is gone in 70 ms
            x += ping * opn * np.exp(-0.0) * np.sin(2 * ph + 0.8 * opn * np.sin(2 * ph))
            if sq:
                pw = 0.5 + 0.16 * np.sin(2 * np.pi * 0.31 * t + 1.4)
                x += sq * np.where(((ph / (2 * np.pi)) % 1.0) < pw, 0.55, -0.55)
    x /= 3.2

    y = stereo(x * amp)
    y = morph_lp(y, cut_lo, cut_hi, np.clip(0.28 + 0.72 * opn / max(opn.max(), 1e-9), 0, 1),
                 bands=7, res=res)
    if breath:
        nz = bandpass(np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32),
                      2200, 8000, order=2)
        y = y + nz * (opn ** 1.5)[:, None] * 0.055 * breath
    y = _asym(y / max(np.abs(y).max(), 1e-9), 1.30)
    y = y + 0.32 * bandpass(y, 1800, 3400, order=2)      # the presence a voice has
    y = chorus(y, voices=3, depth_ms=5.0, rate=0.36, mix=0.42 * wide)
    return hp(y, 190, order=2).astype(np.float32) * level * 0.55


# ================================================================== tools ===
def throw(S, t, seg, gain=1.0, steps_=3.0, times=5, fb=0.55, bus='fx'):
    """One hit into a long echo, then the send closes. The oldest transition
    in dance music and still the cheapest."""
    for i in range(1, times + 1):
        S.place(int(t + i * steps_ * STEP), lp(seg, max(5200 - 700 * i, 900)),
                gain * fb ** i, bus)


def ramp(a, b, i, n, shape=1.0):
    """linear (or curved) interpolation across a section, for gain rides"""
    u = (i / max(n - 1, 1)) ** shape
    return a + (b - a) * u
