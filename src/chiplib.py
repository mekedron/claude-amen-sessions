"""The console module: a Mega Drive, an NES and a Game Boy on one grid, 138 BPM.

Everything in here is built around one idea, and it is not a timbre. On every
one of these machines the sound chip was written to by the CPU once per video
frame - 60 times a second on NTSC, 50 on PAL - and between those writes NOTHING
moved. Pitch, volume, duty cycle, arpeggio, vibrato: all of it is a staircase
at 60 Hz. That quantisation is the sound. Give a chip voice a smooth glide and
it stops being a chip voice immediately, however correct the waveform is. So
every parameter here is written as a list of per-frame values and expanded by
`fhold`, which steps and holds.

The three machines, and what each one can do that the others cannot:

    NES (Ricoh 2A03, 1983)   2 pulse (12.5/25/50/75% duty), 1 triangle with
                             NO volume control, 1 LFSR noise, 1 DPCM.
                             The triangle is 4-bit: fifteen steps, and that
                             staircase is why NES bass buzzes.
    Game Boy (1989)          2 pulse, 1 user-defined 4-bit 32-sample
                             wavetable, 1 noise. The wave channel is why
                             Game Boy music has timbres the NES never had.
    Mega Drive (YM2612,1988) 6 channels of REAL 4-operator FM with 8
                             algorithms and feedback, plus a PSG and a DAC
                             channel for samples. FM is why a Mega Drive can
                             have a bass that slaps and a bell that rings,
                             and why it never sounds like a beeper.

The limits are not obstacles to work around, they are the composer's
material: a chord has to be an arpeggio because a chip has one voice to spend
on it, and the drum kit has to come out of the noise channel because there is
nowhere else for it to come from.

Reused from `skanklib` on purpose and not rebuilt: `speak`, because a
synthesised utterance crushed to 8 bits is exactly what a DAC channel was for
and the voice is already right; `crush`, and the automation helpers `ramp`
and `sweep_bars`. Everything that makes a sound here is new.

Usage:
    from chiplib import *
    s = Session(64, tail=2.0)
    for b in range(8):
        s.place(s.pos(b), arp((0, 3, 7), 62, 16), 1.0, 'lead')
        psgline(s, b, KIT)
    s.render('chip.wav', clip=1.2, limit=0.9)
"""
import numpy as np
import core
from core import *
from skanklib import speak, crush, ramp, sweep_bars, CONS

BAR, STEP = core.set_grid(bpm=138)
BPM = core.BPM
FPS = 60.0                                   # NTSC. A PAL machine ran at 50.


def set_tempo(bpm, beats=4):
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP


# ---- the frame clock ----
def fhold(vals, n, fps=None):
    """Expand a per-frame list to a per-sample array that STEPS and HOLDS.

    This is the whole module. A vibrato written as a smooth sine is a synth; a
    vibrato written as [0,+1,+2,+1,0,-1,-2,-1] repeating at 60 Hz is a console,
    and the difference is audible in one note."""
    fl = SR / (fps or FPS)
    v = np.asarray(vals, dtype=np.float64)
    if v.ndim == 0:
        return np.full(n, float(v))
    idx = np.minimum((np.arange(n) / fl).astype(np.int64), len(v) - 1)
    return v[idx]


def nframes(dur_steps, fps=None):
    """how many frames a duration lasts"""
    return max(int(dur_steps * STEP / SR * (fps or FPS)), 1)


def vsteps(x, levels=16):
    """A chip volume register is four bits. Sixteen steps, not a fader - and
    a fade written in sixteen steps sounds different from a smooth one."""
    return np.round(np.clip(x, 0, 1) * (levels - 1)) / (levels - 1)


def framecurve(n_frames, v0, v1, curve=1.0, levels=0):
    """a ramp already quantised to frames, and optionally to a register"""
    u = np.linspace(0, 1, max(n_frames, 1)) ** curve
    v = v0 + (v1 - v0) * u
    return vsteps(v, levels) if levels else v


# ---- the pulse channel ----
def _pulse(ph, duty, fmax, nyq=17000.0, kmax=90):
    """A band-limited pulse of any duty, built from its own series: harmonic k
    has amplitude sin(pi*k*duty)/k. `duty` may be per-sample, which is how the
    Game Boy's duty sweeps and the C64's PWM are done."""
    x = np.zeros(len(ph))
    k = 1
    while fmax * k < nyq and k < kmax:
        x += np.sin(k * ph) * (np.sin(np.pi * k * duty) / k)
        k += 1
    return x * (4.0 / np.pi)


@cached
def pulse(note, dur_steps=4, gain=1.0, duty=0.5, vol=None, pitch=None,
          detune=0.0, decay=0.0, levels=16, seed=0):
    """The square channel: an NES pulse, a Game Boy pulse, a PSG tone.

    `vol`, `duty` and `pitch` are per-FRAME lists - a tuple of values that the
    voice steps through 60 times a second and holds between. `pitch` is in
    semitones relative to the note, so a slide, a vibrato and an arpeggio are
    all the same thing written differently."""
    n, t = steps(dur_steps, floor=int(0.02 * SR))
    nf = nframes(dur_steps)
    semi = fhold(pitch if pitch is not None else (0.0,), n)
    f = midi(note) * 2.0 ** ((semi + detune) / 12.0)
    ph = 2 * np.pi * np.cumsum(f) / SR
    d = fhold(duty if np.ndim(duty) else (duty,), n)
    x = _pulse(ph, d, float(f.max()))
    v = fhold(vsteps(vol, levels) if vol is not None
              else framecurve(nf, 1.0, 1.0), n)
    if decay:
        v = v * vsteps(np.exp(-t / decay), levels)
    return stereo(x * v).astype(np.float32) * gain * 0.26


# ---- the triangle channel ----
@cached
def tri(note, dur_steps=4, gain=1.0, pitch=None, levels=16, soft=0.0):
    """The NES triangle, and the two things everyone gets wrong about it.

    It has NO volume control - it is on or it is off, which is why an NES bass
    line never swells and why its only dynamic is note length. And it is FOUR
    BITS: fifteen discrete levels, so it is not a triangle at all, it is a
    staircase, and the corners of that staircase are the buzz. Round it off
    and you have a flute."""
    n, t = steps(dur_steps, floor=int(0.02 * SR))
    semi = fhold(pitch if pitch is not None else (0.0,), n)
    f = midi(note) * 2.0 ** (semi / 12.0)
    ph = np.cumsum(f) / SR
    ideal = 2 * np.abs(2 * (ph % 1.0) - 1) - 1
    x = np.round(ideal * (levels / 2)) / (levels / 2)     # the staircase
    if soft:
        x = x * (1 - soft) + ideal * soft
    x = lp(stereo(x), 15500, order=2)
    k = max(int(0.0015 * SR), 2)                          # the channel gate only
    env = np.ones(n); env[:k] = np.linspace(0, 1, k); env[-k:] = np.linspace(1, 0, k)
    return (x * env[:, None]).astype(np.float32) * gain * 0.42


# ---- the noise channel ----
_LFSR = {}


def _lfsr_seq(short=False):
    """The real thing: a 15-bit shift register, XOR of bit 0 with bit 1 fed
    back into bit 14. Tap bit 6 instead and the period collapses from 32767
    steps to 93, which stops being noise and becomes a metallic pitched buzz -
    that is the NES's "short mode", and it is the sound of every laser and
    every robot in every game on the machine."""
    if short not in _LFSR:
        n = 93 if short else 32767
        tap = 6 if short else 1
        reg = 1
        out = np.empty(n, dtype=np.float32)
        for i in range(n):
            bit = (reg ^ (reg >> tap)) & 1
            reg = (reg >> 1) | (bit << 14)
            out[i] = 1.0 if (reg & 1) else -1.0
        _LFSR[short] = out
    return _LFSR[short]


@cached
def noise(dur_steps=1, gain=1.0, rate=8000.0, short=False, vol=None,
          decay=0.03, levels=16):
    """The noise channel. One LFSR clocked at `rate`, and every drum on an NES
    is this with a different rate and a different four-bit envelope."""
    n, t = steps(dur_steps, floor=int(0.01 * SR))
    seq = _lfsr_seq(short)
    r = fhold(rate if np.ndim(rate) else (rate,), n)
    idx = (np.cumsum(r) / SR).astype(np.int64) % len(seq)
    x = seq[idx]
    v = fhold(vsteps(vol, levels), n) if vol is not None else 1.0
    env = vsteps(np.exp(-t / decay), levels) * v
    return stereo(x * env).astype(np.float32) * gain * 0.28


# ---- the Game Boy wave channel ----
@cached
def wavech(note, dur_steps=4, gain=1.0, table=None, pitch=None, vol=None,
           bits=4, size=32, levels=16, seed=0):
    """The Game Boy's third voice: thirty-two four-bit samples the programmer
    could write anything into, played back as a loop. It is a wavetable
    oscillator with a table so small and so coarse that the quantisation IS
    the timbre - which is why Game Boy music has organ, bell and vocal-ish
    tones the NES could never make."""
    n, _ = steps(dur_steps, floor=int(0.02 * SR))
    if table is None:
        rng = np.random.default_rng(seed + 7)
        table = np.sin(2 * np.pi * np.arange(size) / size) + 0.4 * np.sin(
            4 * np.pi * np.arange(size) / size + rng.random())
    tbl = np.asarray(table, dtype=np.float64)
    q = 2 ** (bits - 1)
    tbl = np.round(np.clip(tbl / max(np.abs(tbl).max(), 1e-9), -1, 1) * (q - 1)) / (q - 1)
    semi = fhold(pitch if pitch is not None else (0.0,), n)
    f = midi(note) * 2.0 ** (semi / 12.0)
    ph = (np.cumsum(f) / SR) % 1.0
    x = tbl[(ph * len(tbl)).astype(np.int64) % len(tbl)]   # no interpolation
    v = fhold(vsteps(vol, levels), n) if vol is not None else 1.0
    out = lp(stereo(x * v), 15500, order=2)
    k = max(int(0.0015 * SR), 2)
    env = np.ones(n); env[:k] = np.linspace(0, 1, k); env[-k:] = np.linspace(1, 0, k)
    return (out * env[:, None]).astype(np.float32) * gain * 0.34


# some tables worth having. Four bits is enough for a lot less than you think.
WAVES = {
    'organ':  np.sin(2*np.pi*np.arange(32)/32) + 0.5*np.sin(4*np.pi*np.arange(32)/32)
              + 0.3*np.sin(6*np.pi*np.arange(32)/32),
    'reed':   np.sign(np.sin(2*np.pi*np.arange(32)/32)) * 0.6
              + np.sin(2*np.pi*np.arange(32)/32),
    'bell':   np.sin(2*np.pi*np.arange(32)/32) + 0.7*np.sin(2*np.pi*3.4*np.arange(32)/32),
    'vox':    np.sin(2*np.pi*np.arange(32)/32) + 0.8*np.sin(6*np.pi*np.arange(32)/32)
              + 0.4*np.sin(10*np.pi*np.arange(32)/32),
    'saw':    2*(np.arange(32)/32) - 1,
    'ramp':   1 - 2*(np.arange(32)/32),
}


# ---- the Mega Drive: four-operator FM ----
# The eight YM2612 algorithms. For each: which operators modulate operator i
# (0-indexed, and every dependency points backwards so one pass evaluates
# them), and which operators are heard.
FM_MODS = {
    0: ((), (0,), (1,), (2,)),        1: ((), (), (0, 1), (2,)),
    2: ((), (), (1,), (0, 2)),        3: ((), (0,), (), (1, 2)),
    4: ((), (0,), (), (2,)),          5: ((), (0,), (0,), (0,)),
    6: ((), (0,), (), ()),            7: ((), (), (), ()),
}
FM_CARR = {0: (3,), 1: (3,), 2: (3,), 3: (3,), 4: (1, 3),
           5: (1, 2, 3), 6: (1, 2, 3), 7: (0, 1, 2, 3)}


def _ym_env(t, ar, d1, sl, d2):
    """The YM's five-stage envelope, and the reason FM sounds alive: it is on
    the OPERATOR, not on the voice. A modulator whose envelope falls faster
    than its carrier's is a note whose brightness dies before its loudness
    does - which is what every struck and plucked object in the world does,
    and what a filterless synth otherwise cannot."""
    a = np.minimum(t / max(ar, 1e-4), 1.0)
    dec = sl + (1.0 - sl) * np.exp(-t / max(d1, 1e-4))
    return a * dec * (np.exp(-t / d2) if d2 else 1.0)


# (ratio, level, attack, decay1, sustain, decay2, detune_hz)
PATCHES = {
    # index collapses in 60 ms and the carrier rings on: the Mega Drive bass
    'bass':   (dict(alg=4, fb=1.6), ((1.0, 3.2, 0.001, 0.055, 0.10, 0.00, 0.0),
                                     (1.0, 1.00, 0.001, 0.9, 0.55, 0.0, 0.0),
                                     (0.5, 2.1, 0.001, 0.085, 0.06, 0.00, 0.3),
                                     (1.0, 0.85, 0.001, 1.1, 0.60, 0.0, 0.0))),
    'lead':   (dict(alg=4, fb=0.9), ((2.0, 2.4, 0.004, 0.32, 0.45, 0.0, 0.0),
                                     (1.0, 1.00, 0.006, 1.4, 0.80, 0.0, 0.0),
                                     (3.0, 1.5, 0.004, 0.22, 0.30, 0.0, 0.6),
                                     (1.0, 0.80, 0.006, 1.6, 0.75, 0.0, -0.6))),
    'brass':  (dict(alg=2, fb=1.1), ((1.0, 2.0, 0.030, 0.5, 0.70, 0.0, 0.0),
                                     (1.0, 1.6, 0.020, 0.6, 0.65, 0.0, 0.4),
                                     (1.0, 1.4, 0.035, 0.7, 0.75, 0.0, 0.0),
                                     (1.0, 1.00, 0.025, 2.0, 0.85, 0.0, -0.4))),
    # non-integer ratios: the partials are not multiples of anything, which is
    # the one thing a filter can never make and the reason FM owns bells
    'bell':   (dict(alg=5, fb=0.4), ((1.0, 4.0, 0.001, 0.30, 0.00, 0.0, 0.0),
                                     (1.0, 1.00, 0.001, 2.4, 0.00, 0.0, 0.0),
                                     (3.51, 0.55, 0.001, 1.1, 0.00, 0.0, 0.0),
                                     (7.02, 0.30, 0.001, 0.55, 0.00, 0.0, 0.0))),
    'organ':  (dict(alg=7, fb=0.0), ((1.0, 1.00, 0.004, 3.0, 1.00, 0.0, 0.0),
                                     (2.0, 0.55, 0.004, 3.0, 1.00, 0.0, 0.3),
                                     (3.0, 0.30, 0.004, 3.0, 1.00, 0.0, -0.3),
                                     (4.0, 0.22, 0.004, 3.0, 1.00, 0.0, 0.0))),
    'pluck':  (dict(alg=4, fb=1.2), ((1.0, 2.8, 0.001, 0.10, 0.05, 0.0, 0.0),
                                     (1.0, 1.00, 0.001, 0.55, 0.10, 0.0, 0.0),
                                     (2.0, 1.6, 0.001, 0.07, 0.00, 0.0, 0.5),
                                     (1.0, 0.70, 0.001, 0.70, 0.12, 0.0, -0.5))),
    'stab':   (dict(alg=3, fb=1.8), ((1.0, 3.4, 0.001, 0.045, 0.00, 0.0, 0.0),
                                     (1.5, 2.2, 0.001, 0.06, 0.00, 0.0, 0.0),
                                     (1.0, 1.9, 0.002, 0.09, 0.10, 0.0, 0.7),
                                     (1.0, 1.00, 0.002, 0.34, 0.15, 0.0, 0.0))),
}


@cached
def fm4(note, dur_steps=4, gain=1.0, patch='lead', pitch=None, index=1.0,
        decay=0.0, lfo=0.0, lfo_depth=0.0, alg=None, fb=None, ops=None,
        dhz=0.0, attack=0.0, seed=0):
    """One YM2612 channel: four sine operators, one of the eight algorithms,
    and feedback on the first.

    `index` scales every MODULATOR's output and nothing else - that one number
    is the brightness control, and enveloping it is what a filter sweep is on
    a machine with no filter. `pitch` is a per-frame semitone list, so slides
    and vibrato are written the way the CPU wrote them."""
    cfg, o = PATCHES[patch]
    alg = cfg['alg'] if alg is None else alg
    fb = cfg['fb'] if fb is None else fb
    ops = o if ops is None else ops
    n, t = steps(dur_steps, floor=int(0.02 * SR))
    semi = fhold(pitch if pitch is not None else (0.0,), n)
    if lfo:
        nf = nframes(dur_steps)
        semi = semi + fhold(lfo_depth * np.sin(2 * np.pi * lfo
                                               * np.arange(nf) / FPS), n)
    # Detune in HERTZ, not cents. The chip's frequency register is a divider,
    # so two channels written one step apart beat at a rate that barely
    # changes with pitch - which is why chip unison sounds nothing like a
    # supersaw, where the detune is scale-free and the beating speeds up as
    # the note rises.
    f0 = midi(note) * 2.0 ** (semi / 12.0) + dhz
    base = 2 * np.pi * np.cumsum(f0) / SR
    carr = FM_CARR[alg]
    outs = []
    for i, (ratio, lvl, ar, d1, sl, d2, det) in enumerate(ops):
        ph = base * ratio + 2 * np.pi * det * t
        env = _ym_env(t, ar, d1, sl, d2)
        if i == 0 and fb:
            y = np.sin(ph)
            for _ in range(2):                       # the feedback loop, twice
                y = np.sin(ph + fb * y * env)
        else:
            m = sum(outs[j] for j in FM_MODS[alg][i])
            y = np.sin(ph + m)
        scale = lvl if i in carr else lvl * index
        outs.append(y * env * scale)
    x = sum(outs[i] for i in carr) / len(carr)
    if decay:
        x = x * np.exp(-t / decay)
    if attack:
        # a swell written the way the CPU wrote it: the volume register
        # climbing one step per frame
        x = x * fhold(framecurve(max(int(attack * FPS), 1), 0.0, 1.0), n)
    k = max(int(0.002 * SR), 2)
    e = np.ones(n); e[:k] = np.linspace(0, 1, k); e[-k:] = np.linspace(1, 0, k)
    return stereo(x * e).astype(np.float32) * gain * 0.42


# ---- the arpeggio ----
@cached
def arp(offsets, note, dur_steps=4, gain=1.0, voice='pulse', rate=1,
        duty=0.5, patch='lead', octaves=(0,), vol=None, levels=16, seed=0):
    """A chord played on ONE voice by changing its pitch every frame.

    Not an effect and not a stylistic choice - it is what you do when the chip
    has three voices and two of them are already the bass and the drums. At 60
    Hz the ear stops hearing three notes in sequence and starts hearing one
    chord with a buzz on it, and that buzz is the sound of the entire era."""
    nf = nframes(dur_steps)
    seq = [offsets[(i // max(rate, 1)) % len(offsets)]
           + 12 * octaves[(i // (max(rate, 1) * len(offsets))) % len(octaves)]
           for i in range(nf)]
    if voice == 'pulse':
        return pulse(note, dur_steps, gain=gain, duty=duty, pitch=tuple(seq),
                     vol=vol, levels=levels, seed=seed)
    if voice == 'tri':
        return tri(note, dur_steps, gain=gain, pitch=tuple(seq))
    if voice == 'wave':
        return wavech(note, dur_steps, gain=gain, pitch=tuple(seq), vol=vol,
                      table=tuple(WAVES['organ']), seed=seed)
    return fm4(note, dur_steps, gain=gain, patch=patch, pitch=tuple(seq))


# ---- the kit ----
@cached
def psgkick(dur_steps=3, gain=1.0, note=38, drop=26.0, frames=5, tail=0.10):
    """An NES kick: the triangle channel dropped through a handful of
    semitones over four or five FRAMES and then cut. It is a pitch envelope
    written as five numbers, because five numbers is what the CPU had time to
    write, and the staircase is the punch."""
    nf = nframes(dur_steps)
    pit = tuple(max(drop * (1 - i / max(frames, 1)), 0.0) if i < frames else 0.0
                for i in range(nf))
    n, t = steps(dur_steps, floor=int(0.02 * SR))
    seg = tri(note, dur_steps, gain=1.0, pitch=pit)[:n]
    return (seg * vsteps(np.exp(-t / tail))[:, None]).astype(np.float32) * gain * 1.5


@cached
def psgsnare(dur_steps=2, gain=1.0, rate=11000.0, tone=1.0, decay=0.055,
             note=57):
    """Noise for the wires and one pulse for the shell, which is every snare
    on the machine."""
    n, t = steps(dur_steps, floor=int(0.02 * SR))
    nz = noise(dur_steps, rate=rate, decay=decay)[:n]
    sh = pulse(note, dur_steps, duty=0.25, decay=decay * 0.45)[:n] * 0.55 * tone
    return ((nz * 1.5 + sh) * vsteps(np.exp(-t / (decay * 1.6)))[:, None]
            ).astype(np.float32) * gain * 1.15


@cached
def psghat(dur_steps=1, gain=1.0, rate=26000.0, decay=0.012, open_=False):
    return noise(dur_steps, rate=rate, decay=decay * (5.0 if open_ else 1.0),
                 gain=gain * 0.75)


@cached
def psgtom(dur_steps=2, gain=1.0, note=48, drop=9.0, frames=6, tail=0.14):
    nf = nframes(dur_steps)
    pit = tuple(drop * (1 - i / max(frames, 1)) if i < frames else 0.0
                for i in range(nf))
    n, t = steps(dur_steps, floor=int(0.02 * SR))
    return (tri(note, dur_steps, pitch=pit)[:n]
            * vsteps(np.exp(-t / tail))[:, None]).astype(np.float32) * gain * 1.2


@cached
def zap(dur_steps=2, gain=1.0, rate0=20000.0, rate1=2000.0, frames=10,
        decay=0.09, short=True):
    """The laser. Short-mode noise with its clock falling frame by frame - the
    single most recognisable sound effect on the machine, and it is four lines
    of code because that is all the CPU had."""
    nf = nframes(dur_steps)
    r = tuple(rate0 * (rate1 / rate0) ** min(i / max(frames, 1), 1.0)
              for i in range(nf))
    return noise(dur_steps, rate=r, short=short, decay=decay, gain=gain)


# ---- the DAC channel ----
def dac(seg, bits=8, sr_div=4, gain=1.0, hp_hz=180.0):
    """The sample channel: eight bits at about eleven kilohertz, mono, with no
    reconstruction filter worth the name. It is what said SEGA at the start of
    the cartridge, and it is why every sampled drum on the machine sounds like
    it is coming through a wall."""
    x = lp(seg, SR / (2.0 * sr_div) * 1.35, order=2)      # deliberately above
    x = np.repeat(x[::sr_div], sr_div, axis=0)[:len(seg)]  # sr/2, so it folds
    q = 2.0 ** (bits - 1)
    x = np.trunc(x * q) / q
    m = x.mean(axis=1)
    return hp(stereo(m), hp_hz, order=2).astype(np.float32) * gain


@cached
def dackick(dur_steps=3, gain=1.0, tune=52.0, drop=3.2, decay=0.16):
    """A sampled kick as the machine stored it: synthesised clean, then thrown
    through the DAC."""
    n, t = steps(dur_steps, floor=int(0.02 * SR))
    f = tune * (1 + drop * np.exp(-t / 0.017))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    x += np.random.default_rng(3).standard_normal(n) * np.exp(-t / 0.0022) * 0.35
    return norm(dac(stereo(np.tanh(1.6 * x)), bits=8, sr_div=4, hp_hz=30),
                0.92) * gain


# ---- one filter for the whole chip ----
def sidfilter(seg, cutoff=4000.0, res=1.0, mode='lp', frames=None):
    """The C64 had ONE analog filter and all three voices shared it, so it was
    never a per-voice tone control - it was a hand on the whole machine. Pass
    `frames` for a per-frame cutoff list, which is how it was ever automated."""
    n = len(seg)
    if frames is not None:
        env = fhold(frames, n)
        lo, hi = float(np.min(env)) * 0.96, float(np.max(env)) * 1.04
        u = (np.log(np.clip(env, lo, hi) / lo) / np.log(max(hi / lo, 1.001)))
        return morph_lp(seg, lo, hi, u, bands=11, res=res)
    y = lp(seg, cutoff, order=2) if mode == 'lp' else hp(seg, cutoff, order=2)
    return (y + res * bandpass(seg, cutoff * 0.85, cutoff * 1.18, order=2)
            ).astype(np.float32)


def ladder(seg, amount=0.007):
    """The Mega Drive's DAC had a fault: a small step across zero that never
    went away, so quiet passages came out with crossover distortion on them.
    It is a defect and it is half the reason the machine has a sound."""
    return (seg + amount * np.sign(seg)).astype(np.float32)


def console(seg, ladder_=0.006, tone=15000.0, drive=1.15):
    """The output stage: the DAC's step, the analog lowpass on the way out of
    the machine, and the gentle clipping of a cheap amplifier."""
    x = ladder(seg, ladder_)
    x = lp(x, tone, order=2)
    return (np.tanh(drive * x) / np.tanh(drive)).astype(np.float32)


def psgfill(s, b, kind='toms', gain=1.0, bus='drums'):
    """The bar-end. A chip kit has three sounds and no velocity layers, so a
    fill is a change of PATTERN and of noise clock, never of dynamics - and
    without one an eight-bar phrase repeats bit for bit, which is the one way
    a deterministic machine can actually sound wrong."""
    if kind == 'toms':
        for i, (st, nt) in enumerate(zip((12, 13, 14, 15), (55, 51, 48, 45))):
            s.place(s.pos(b, st), psgtom(2, note=nt), gain * (0.85 + 0.05 * i), bus)
    elif kind == 'roll':
        for i, st in enumerate((12, 13, 14, 14.5, 15, 15.5)):
            s.place(s.pos(b, st), psgsnare(2), gain * (0.7 + 0.06 * i), bus)
    elif kind == 'noise':
        s.place(s.pos(b, 12), zap(8, gain=gain * 0.9, rate0=24000, rate1=3000,
                                  frames=14, decay=0.30, short=False), 1.0, bus)
        for st in (14, 15):
            s.place(s.pos(b, st), psgsnare(2), gain * 0.9, bus)
    elif kind == 'kicks':
        for st in (12, 13, 14, 15):
            t = s.pos(b, st)
            s.hit(t)
            s.place(t, psgkick(2), gain * 0.9, bus)
    elif kind == 'stop':                      # a bar of nothing but the last 16th
        s.place(s.pos(b, 15), psgsnare(2), gain, bus)


def psgline(s, b, pat, gain=1.0, bus='drums', seed=0, swing=0.0, register=True):
    """One bar of the chip kit off a 16-step pattern. No velocity layers and
    no humanising: the CPU wrote the same three registers every time, and the
    machine-ness is the point."""
    sw = (swing - 0.5) * 2.0 * STEP if swing else 0.0
    for row in ('kick', 'snare', 'hat', 'ohat', 'tom'):
        chars = pat.get(row, '')
        chars = chars if isinstance(chars, str) else chars[b % len(chars)]
        for i, ch in enumerate(chars):
            if ch == '-':
                continue
            v = {'x': 1.0, '+': 0.66, '.': 0.34, 'o': 1.0}.get(ch, 1.0)
            t = s.pos(b, i) + int(sw if i % 2 else 0)
            if row == 'kick':
                if register:
                    s.hit(t)
                seg = psgkick(3)
            elif row == 'snare':
                seg = psgsnare(2)
            elif row == 'hat':
                seg = psghat(1)
            elif row == 'ohat':
                seg = psghat(3, open_=True)
            else:
                seg = psgtom(2, note=50 - 5 * (i % 3))
            s.place(t, seg, v * gain, bus)


# ---- the layered lead ----
# A chip lead is almost never one channel. On a Mega Drive you spend two or
# three of your six on it, and each one is doing a different job:
#
#   the CORE      the FM voice at pitch - the note itself
#   the BEAT      the same patch one or two hertz away. Not a chorus: two
#                 dividers one step apart, beating at a rate that barely
#                 moves with pitch, which is why chip unison is slow and even
#                 where a supersaw's beating speeds up as it climbs
#   the EDGE      a PSG pulse at 12.5% duty an octave up. It carries almost
#                 no power and it is the reason the lead cuts - the ear finds
#                 the line by its top harmonics, not by its fundamental
#   the BODY      the Game Boy wave channel underneath, hollow and quiet
#   the SWELL     a channel whose volume register climbs one step per frame,
#                 so the note arrives after its own attack
#   the ECHO      the same note written to another channel a few FRAMES late
#                 and quieter. Every composer on these machines faked reverb
#                 this way, and delaying by frames rather than milliseconds is
#                 what keeps it locked to the music
#
# They must not be the same sound louder. Each owns a different octave, a
# different envelope and a different side of the image, and that is the whole
# difference between a thick lead and a loud one.
def leadnote(s, t, note, dur_steps, gain=1.0, bus='lead', patch='lead',
             index=1.0, pitch=None, beat=0.0, beat_hz=1.6, edge=0.0,
             body=0.0, swell=0.0, echo=0.0, echo_frames=5, echo_oct=0,
             spread=0.0, octave=0, wave='organ'):
    """One note of the lead, as a stack of chip channels."""
    nt = note + octave
    fl = SR / FPS
    core_ = fm4(nt, dur_steps, patch=patch, index=index, pitch=pitch)
    s.place(t, panned(core_, -spread) if spread else core_, gain, bus)
    if beat:
        b = fm4(nt, dur_steps, patch=patch, index=index, pitch=pitch, dhz=beat_hz)
        s.place(t, panned(b, spread) if spread else b, gain * beat, bus)
    if edge:
        s.place(t, pulse(nt + 12, dur_steps, duty=0.125, pitch=pitch),
                gain * edge, bus)
    if body:
        s.place(t, wavech(nt - 12, dur_steps, table=tuple(WAVES[wave]),
                          pitch=pitch), gain * body, bus)
    if swell:
        sw = fm4(nt, dur_steps, patch='organ', index=index * 0.8, pitch=pitch,
                 attack=0.10)
        s.place(t, panned(sw, spread * 0.6) if spread else sw, gain * swell, bus)
    if echo:
        e = fm4(nt + echo_oct, dur_steps, patch=patch, index=index * 0.7,
                pitch=pitch)
        s.place(int(t + echo_frames * fl),
                panned(e, -spread * 0.8) if spread else e, gain * echo, bus)


# D natural minor, and the C# that replaces C on every V bar. A harmony line
# has to be built out of the scale, not transposed by a fixed interval, or
# every fourth note lands outside the key.
DMIN = (2, 4, 5, 7, 9, 10, 0)
DMIN_V = (2, 4, 5, 7, 9, 10, 1)


def scale_step(note, k, scale=DMIN, lo=24, hi=108):
    """move `k` scale degrees from `note`, staying in the key"""
    ns = [n for n in range(lo, hi + 1) if n % 12 in scale]
    i = min(range(len(ns)), key=lambda j: abs(ns[j] - note))
    return ns[max(min(i + k, len(ns) - 1), 0)]
