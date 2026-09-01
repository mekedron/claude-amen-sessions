"""The desert western layer: a twang, a whistle, a spring and a horse.

Built on the punk module, so the guitar, the amp, the cabinet, the kit and
the continuous bass all come from there - this file only adds what a spaghetti
western needs and moves the grid to 132 BPM.

Three sounds do the work:

**The twang.** The same Karplus-Strong string, but picked over and over while
it is still ringing (`ks(hits=...)`), through a much cleaner amp and into a
spring. Tremolo picking is one string struck repeatedly, not a row of notes,
and rendering it the second way is the difference between Morricone and a
stuck sequencer.

**The spring.** A guitar amp's reverb tank is three steel springs, and what
makes it recognisable is not the tail but the dispersion: high frequencies
travel down a spring faster than low ones, so every transient arrives as a
descending chirp. Discrete bandpassed pre-echoes in front of a bright,
narrow reverb get most of the way there.

**The whistle.** Nearly a sine - a whistle really is that pure - with a
breath band, a scoop up into every note and vibrato that arrives late, the
way a person's does.

Usage:
    from westernlib import *
    s = Session(96, tail=3.0)
    s.place(s.pos(0), spring(twang(50, 16, trem=0.5), wet=0.6), 0.5)
    s.place(s.pos(4), whistle(74, 12), 0.4)
"""
import numpy as np
import core, punklib
from punklib import *

BAR, STEP = punklib.set_tempo(132)
BPM = core.BPM


# ---- the spring ----
def spring(seg, decay=1.5, wet=0.55, tone=3400, boing=0.55, drip=1.0):
    """A reverb tank: bright, narrow, and it chirps before it blooms."""
    band = bandpass(seg, 380, 4800)
    out = reverb(band, decay=decay, wet=wet, tone=tone, predelay=0.004)
    chirp = bandpass(seg, 900, 3800)
    for d, g in ((0.019, 0.55), (0.034, 0.38), (0.051, 0.26), (0.072, 0.16)):
        k = int(d * SR * drip)
        e = min(k + len(chirp), len(out))
        out[k:e] += chirp[:e - k] * g * boing
    return out.astype(np.float32)


# ---- the twang ----
@cached
def twang(note, dur_steps, level=1.0, trem=0.0, rate=1.0, bright=1.0, decay=1.7,
          take=0, drive=2.4, wob=0.0, vib=0.006, vib_hz=5.1, dual=0.55):
    """Duane Eddy's low string: bright, clean-ish, all attack and no gain.
    `rate` in steps is the tremolo picking interval; `trem` fades it in."""
    n, t = steps(dur_steps)
    # The pickup sits almost on the bridge (`pickup=0.08`), which is the whole
    # of "twang": near the bridge the string barely moves, so the low modes
    # are weak and the high ones survive, and the coil resonance is set high
    # and sharp on top of that.
    x = string(midi(note), n, decay=decay, damp=0.016, pick=0.30, pickup=0.08,
               B=1.0e-4, top=7000.0, res_hz=3900.0, res_q=3.0, bright=1.0,
               retrig=(rate * STEP / SR) if trem else 0.0,
               bend=(1 + vib * np.sin(2 * np.pi * vib_hz * t)
                     * np.minimum(t / 0.28, 1.0)) if vib else None,
               seed=int(6151 * take + 29 * note))
    y = stereo(np.tanh(drive * x) / np.tanh(drive))
    y = cab(y, seed=3, low=92.0, high=5600.0, cone=0.50, presence=1.7 * bright)
    if dual:
        # A second amp, off to the side. One guitar into two different
        # speakers, mic'd differently, is how a twang gets its size on a
        # record - and it is the cheapest way to stop a single synthesised
        # voice reading as a single synthesised voice, because the two paths
        # disagree about the same note.
        x2 = string(midi(note), n, decay=decay * 1.15, damp=0.022, pick=0.21,
                    pickup=0.16, B=1.0e-4, top=6200.0, res_hz=2600.0, res_q=2.0,
                    retrig=(rate * STEP / SR) if trem else 0.0,
                    bend=(1 + vib * 1.4 * np.sin(2 * np.pi * (vib_hz * 0.83) * t)
                          * np.minimum(t / 0.28, 1.0)) if vib else None,
                    seed=int(6151 * take + 29 * note + 7717))
        y2 = cab(stereo(np.tanh(drive * 0.7 * x2) / np.tanh(drive * 0.7)),
                 seed=4, low=110.0, high=5000.0, cone=0.30, presence=1.1 * bright)
        y = panned(y, -0.30) + dual * panned(y2, 0.34)
    y = y + 0.45 * bandpass(y, 1800, 4200) * bright              # the twang
    y = y + 0.25 * bandpass(y, 700, 1500) * bright               # and its bark
    if trem:                                                     # a hand, not a
        rng = np.random.default_rng(int(6151 * take + 29 * note))   # sequencer
        P = max(int(rate * STEP), 16)
        v = 1 + 0.26 * rng.standard_normal(n // P + 2)
        y = y * uniform_filter1d(np.repeat(v, P)[:n], P // 3)[:, None]
    if wob:                                                      # amp tremolo
        y = y * (1 - wob * 0.5 * (1 - np.cos(2 * np.pi * 5.6 * t)))[:, None]
    return norm(y * adsr(n, a=0.0015, r=0.05)[:, None], 0.88) * level


# ---- the whistle ----
@cached
def whistle(note, dur_steps, level=1.0, vib=5.0, vib_depth=0.013, scoop=0.6,
            air=1.0, seed=0, wobble=1.0):
    """A person whistling, which is not a sine wave with vibrato on it.

    A whistle is a jet of air across a hole, and the hole is the mouth - a
    Helmholtz resonator the tongue retunes for every note. That means two
    things a pure oscillator does not have. There is a great deal of
    turbulence noise, ten to twenty per cent of the energy, and it is not
    hiss somewhere else in the spectrum: the cavity resonates it, so the
    noise sits AROUND the pitch and slides with it. And the airflow is a
    person's breath, so neither the loudness nor the pitch holds still -
    there is a slow random drift underneath the deliberate vibrato.

    Without those the sound has one partial and no noise floor, and one
    partial with no noise floor is a games console."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(seed + 13)
    f = midi(note)
    ramp = np.minimum(t / 0.30, 1.0)

    drift = uniform_filter1d(rng.standard_normal(n), max(int(0.075 * SR), 3))
    drift = drift / max(float(np.abs(drift).max()), 1e-9) * 0.007 * wobble
    bend = 2 ** (-scoop / 12 * np.exp(-t / 0.055))
    ff = f * bend * (1 + vib_depth * np.sin(2 * np.pi * vib * t) * ramp + drift)
    ph = 2 * np.pi * np.cumsum(ff) / SR
    tone = np.sin(ph) + 0.085 * np.sin(2 * ph) + 0.020 * np.sin(3 * ph)

    nz = rng.standard_normal(n)
    breath = bandpass(stereo(nz), f * 0.80, f * 1.28, order=2)[:, 0] * 3.0
    breath += bandpass(stereo(nz), f * 1.85, f * 3.4, order=2)[:, 0] * 0.55
    breath += hp(stereo(nz), 4200)[:, 0] * 0.09

    amp_w = uniform_filter1d(rng.standard_normal(n), max(int(0.045 * SR), 3))
    amp_w = 1 + 0.18 * wobble * amp_w / max(float(np.abs(amp_w).max()), 1e-9)

    on_tone = np.minimum(np.maximum(t - 0.030, 0) / 0.045, 1.0)   # air first,
    on_air = np.minimum(t / 0.018, 1.0)                           # then the note
    x = tone * on_tone + breath * 0.78 * air * on_air
    env = amp_w * adsr(n, a=0.001, r=0.10)
    out = stereo(x) * env[:, None]
    return norm(out, 0.85) * level


# ---- the bottleneck, and the noise a hand makes ----
@cached
def slide(note_from, note_to, dur_steps, level=1.0, take=0, glide=0.45,
          vib=4.6, vib_depth=0.007, drive=2.0, bright=1.0, curve=0.8):
    """A bottleneck slide.

    There is no fret, so the pitch is a continuous curve and the arrival has
    no attack of its own. That is why a slide answers a picked phrase so
    well - it is the same instrument making a sound the picked one cannot,
    which is exactly what layering is for. The glass also damps the string,
    so it has less top than a fretted note and a slower onset."""
    n, t = steps(dur_steps)
    span = max(glide * n / SR, 1e-3)
    u = np.clip(t / span, 0, 1) ** curve
    ramp = np.minimum(t / 0.25, 1.0)
    bend = 2 ** ((note_to - note_from) / 12 * u) * \
        (1 + vib_depth * np.sin(2 * np.pi * vib * t) * ramp)
    x = string(midi(note_from), n, decay=2.2, damp=0.020, pick=0.28, pickup=0.11,
               B=1.0e-4, top=6500.0, bend=bend, res_hz=3400.0, res_q=2.6,
               seed=int(5471 * take + 37 * note_from + 11 * note_to))
    y = stereo(np.tanh(drive * x) / np.tanh(drive))
    y = cab(y, seed=3, low=92.0, high=5600.0, cone=0.55, presence=1.4 * bright)
    y = lp(y, 4800, order=2)                       # the glass takes the top off
    return norm(y * adsr(n, a=0.012, r=0.09)[:, None], 0.88) * level


@cached
def fretnoise(dur_steps=1.5, gain=1.0, seed=0, wound=1.0, up=False):
    """Fingers dragged along a wound string.

    The windings pass under the fingertip at a rate that rises and falls with
    the hand, so it is a rasp with a pitch in it rather than a hiss. Every
    guitar record ever made is full of this between the notes, and a
    synthesised one has none - which is a large part of why a synthesised one
    does not sound played, however good the notes are."""
    n, t = steps(dur_steps, floor=int(0.03 * SR))
    rng = np.random.default_rng(seed + 131)
    u = np.linspace(0, 1, n)
    speed = np.sin(np.pi * u) ** 0.7                   # the hand starts and stops
    rate = 800 + 2800 * speed * (1.3 if up else 1.0)
    ph = 2 * np.pi * np.cumsum(rate) / SR
    rasp = (np.sign(np.sin(ph)) * 0.5 + 0.5) * rng.standard_normal(n) * wound
    x = rasp + rng.standard_normal(n) * 0.45
    out = bandpass(stereo(x), 1300, 5400)
    out = out * (speed * np.exp(-np.maximum(u - 0.55, 0) * 4))[:, None]
    return norm(out, 0.7) * gain * 0.5


# ---- the trumpet ----
@cached
def trumpet(note, dur_steps, level=1.0, rip=0.0, fall=0.0, vib=5.6, seed=0,
            voices=2, blare=1.0):
    """An OPEN trumpet, two of them in unison and not quite in tune.

    Not the harmon-muted one `core.horn` makes - that is a jazz club at three
    in the morning, intimate and close. This is the other trumpet: a mariachi
    plays it across a valley. The differences are all physical. A brass tube
    gets brighter as it is blown harder, so the spectrum has to open during
    the attack rather than being filtered to a fixed shape; there is a
    resonance around 1.2 kHz that is the instrument's own body and is most of
    why a trumpet is a trumpet; and `rip` is the gesture the genre is built
    on - the pitch smeared up into the note from below instead of arriving."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(seed + 91)
    f = midi(note)
    bend = np.ones(n)
    if rip:
        bend = bend * 2 ** (-rip / 12 * np.exp(-t / 0.048))
    if fall:
        k = int(n * 0.70)
        bend[k:] *= 2 ** (-fall / 12 * np.linspace(0, 1, n - k) ** 1.6)
    ramp = np.minimum(t / 0.24, 1.0)
    x = np.zeros(n)
    for v in range(voices):
        det = 1 + 0.0045 * (v - (voices - 1) / 2) * 2
        ph = 2 * np.pi * np.cumsum(
            f * det * bend * (1 + 0.010 * np.sin(2 * np.pi * vib * t + v) * ramp)) / SR
        x += saw_ph(ph, f * det)
    st_ = stereo(x / voices)
    bloom = np.minimum(t / 0.060, 1.0) ** 0.55          # brass opens as it blows
    y = morph_lp(st_, 850, 7000, bloom, bands=7)
    y = y + 1.20 * bandpass(y, 950, 1550) * blare       # the body of the horn
    y = y + 0.55 * bandpass(y, 2000, 3800) * blare      # and the edge of it
    y = np.tanh(1.7 * y)
    y = y + hp(stereo(rng.standard_normal(n)), 4500) * 0.045 * bloom[:, None]
    y[:, 1] = np.roll(y[:, 1], int(SR * 0.0011))
    return norm(hp(y, 180) * adsr(n, a=0.028, r=0.11)[:, None], 0.88) * level


# ---- percussion the kit does not have ----
@cached
def tamb(dur_steps=1, gain=1.0, open_=False, seed=0):
    """Jingles: many thin inharmonic rings, not a noise burst."""
    n, t = steps(dur_steps, floor=int(0.05 * SR))
    rng = np.random.default_rng(seed + 51)
    x = np.zeros(n)
    for r in (1.0, 1.27, 1.61, 2.03, 2.44, 3.1, 3.9, 4.8):
        x += np.sin(2 * np.pi * 2400 * r * t + rng.random() * 6) / 8
    x = x * 0.8 + rng.standard_normal(n) * 0.5
    d = 0.30 if open_ else 0.035
    out = hp(stereo(x), 3800) * (np.exp(-t / d) * adsr(n, a=0.0008, r=0.02))[:, None]
    return norm(out, 0.85) * gain * 0.34


@cached
def handclap(dur_steps=2, gain=1.0, hands=5, seed=0):
    """Several people, never quite together. The scatter IS the sound: put
    them all on the same sample and it is one clap, loud."""
    n, t = steps(dur_steps, floor=int(0.1 * SR))
    rng = np.random.default_rng(seed + 61)
    burst = np.zeros(n)
    for i in range(hands):
        k = int(abs(rng.normal(0, 0.009)) * SR)
        if k < n:
            burst[k:] += rng.standard_normal(n - k) * np.exp(
                -np.arange(n - k) / SR / 0.010) * (0.7 + 0.3 * rng.random())
    body = bandpass(stereo(burst), 700, 5200)
    tail = bandpass(stereo(rng.standard_normal(n)), 1100, 4200) * np.exp(-t / 0.055)[:, None] * 0.35
    out = np.tanh(1.6 * (body + tail))
    return norm(widen(out, 0.7), 0.85) * gain * 0.5


@cached
def woodblock(dur_steps=1, tune=1150.0, gain=1.0, seed=0):
    """A hard, dry, pitched click. Two of them in a gallop are a horse."""
    n, t = steps(dur_steps, floor=int(0.03 * SR))
    rng = np.random.default_rng(seed + 71)
    x = (np.sin(2 * np.pi * tune * t) + 0.5 * np.sin(2 * np.pi * tune * 2.7 * t))
    x = x * np.exp(-t / 0.011) + rng.standard_normal(n) * np.exp(-t / 0.0016) * 0.5
    return norm(bandpass(stereo(x), 500, 7000), 0.85) * gain * 0.45


def hooves(s, b, bus='perc', gain=0.5, pan=0.25, seed=0):
    """The gallop: two short and one long, three times a bar. Every western
    ever made runs on this rhythm and nobody has ever got tired of it."""
    for beat_ in range(4):
        for st, g, tn in ((0.0, 0.55, 1250.0), (1.0, 0.7, 1100.0), (2.0, 1.0, 980.0)):
            s.place(s.pos(b, beat_ * 4 + st),
                    panned(woodblock(1, tune=tn, seed=(beat_ + seed) % 3),
                           pan * (1 if beat_ % 2 else -1)), gain * g, bus)


# ---- the wind ----
def wind_bed(dur_steps, gain=1.0, seed=0, low=95.0, high=1900.0):
    """Filtered noise with a cutoff that wanders. The desert, for free."""
    n, t = steps(dur_steps)
    rng = np.random.default_rng(seed + 81)
    nz = stereo(rng.standard_normal(n))
    env = uniform_filter1d(rng.standard_normal(n), int(0.6 * SR))
    env = (env - env.min()) / max(float(np.ptp(env)), 1e-9)
    out = morph_lp(bandpass(nz, low, high), low * 1.5, high, env, bands=7)
    amp = 0.4 + 0.6 * uniform_filter1d(np.abs(env), int(0.25 * SR))
    return (out * amp[:, None]).astype(np.float32) * gain * 0.5


def phrase(s, events, b0, fn, bus, gain=1.0, pan=0.0, oct_=0, vary=True, **kw):
    """Place a line, giving every note its own take so a repeated note is not
    a repeated recording."""
    for i, (st, note, ln) in enumerate(events):
        if vary and 'take' not in kw:
            seg = fn(note + oct_, ln, take=i % 3, **kw)
        else:
            seg = fn(note + oct_, ln, **kw)
        s.place(s.pos(b0 + st // 16, st % 16), panned(seg, pan), gain, bus)


def bus_spring(buf, decay=1.5, wet=0.45, tone=3400, boing=0.5, block_bars=12):
    """The tank across a whole bus, in blocks. Returns the WET only - add it."""
    out = np.zeros_like(buf)
    blk = int(block_bars * BAR)
    for a in range(0, len(buf), blk):
        seg = buf[a:a + blk]
        if np.abs(seg).max() < 1e-6:
            continue
        w_ = spring(seg, decay=decay, wet=wet, tone=tone, boing=boing)
        dry = bandpass(seg, 380, 4800)      # spring() returns dry+wet and its
        w_[:len(dry)] -= dry                # tail is longer than the input
        e = min(a + len(w_), len(out))
        out[a:e] += w_[:e - a]
    return out
