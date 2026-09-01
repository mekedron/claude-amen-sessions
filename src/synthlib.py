"""The synthwave layer: 116 BPM, and a decade rebuilt from its defects.

Every sound this genre is loved for was a limitation. The Juno-106 had one
oscillator, so its chorus had to do the thickening - and that noisy
bucket-brigade is now the definition of a warm 80s pad. The LinnDrum stored
8-bit samples because memory cost money. The gated snare was a big reverb
with a noise gate slammed across it, invented to fix a drum booth and kept
because it sounded enormous. Reproduce the sounds without the defects and
you get a clean modern record that happens to use minor chords.

So the three things in here are the three defects:

`bbd_chorus` - two bucket-brigade delay lines at 22 ms, modulated slowly and
in opposite phase per channel, with the chip's own hiss left in. `junopad`
is one DCO and a sub through a filter into this; bypass the chorus and what
is left is thin and ordinary, which is exactly what a Juno is.

`gatedsnare` - a bright reverb with no pre-delay, cut off dead by a gate
after 220 ms, and mixed loud enough to be most of the sound. Not an effect
on a snare: the snare.

`linnkick`/`linnhat`/`linnclap` - real drums quantised to 8 bits and
decimated without an anti-alias filter, because the folded-back aliasing IS
the texture, and `simmonstom`, which is a pitch sweep rather than a drum.

Everything melodic is rendered with core's `line()`: one unbroken oscillator
per bar, so the lead's portamento really slides and its vibrato can arrive
late the way a played one does.

Usage:
    from synthlib import *
    s = Session(128, tail=4.0)
    s.place(s.pos(0), junopad(CHORDS[0], 16), bus='pad')
    s.render('synth_something_116.wav', drive=0.7, limit=0.92)
"""
import numpy as np
import core
from core import *

BAR, STEP = core.set_grid(bpm=116)
BPM = core.BPM

def set_tempo(bpm, beats=4):
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP

Session.DUCKED = {'bass': 0.55, 'pad': 0.30, 'arp': 0.25, 'music': 0.20}


# ---- the defect that became a decade ----
def bbd_chorus(seg, mode=3, base_ms=22.0, depth_ms=5.2, mix=0.5, noise=0.0035,
               seed=0):
    """The Juno's chorus, and the instrument it turns one oscillator into.

    A bucket-brigade delay is an analogue shift register: the signal is
    clocked through a chain of capacitors, so it comes out delayed, noisier
    and darker than it went in. Two of them at ~22 ms, modulated at 0.5 Hz
    (I) and 2.1 Hz (II) in opposite phase per channel, mixed half and half
    with the dry. `mode` 1, 2 or 3 is the front-panel switch; 3 is both
    buttons down, which the manual does not recommend and everyone used.

    The hiss is not an accident being tolerated - leave it out and the pad
    sits in digital silence between notes and stops sounding like 1984."""
    n = len(seg)
    t = np.arange(n) / SR
    rates = {1: (0.51,), 2: (2.10,), 3: (0.51, 2.10)}[mode]
    rs = np.random.RandomState(seed + 173)
    out = (seg * (1 - mix)).astype(np.float32)
    idx0 = np.arange(n, dtype=np.float64)
    for r in rates:
        for c in (0, 1):
            ph = 2 * np.pi * r * t + (0.0 if c == 0 else np.pi)
            d = (base_ms + depth_ms * np.sin(ph)) * SR / 1000.0
            wet = np.interp(idx0 - d, idx0, seg[:, c].astype(np.float64))
            out[:, c] += (mix / len(rates) * wet).astype(np.float32)
    if noise:
        out = out + lp(np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32),
                       9000) * noise
    return out.astype(np.float32)


def junopad(notes, dur_steps=16, gain=1.0, cutoff=2600, hpf=180.0, sub=0.55,
            pw=0.5, res=0.0, attack=0.35, release=0.9, chorus_mode=3, seed=None):
    """One DCO, a square sub, a fixed high-pass, a 24 dB low-pass, and the
    chorus. That is the entire Juno-106 voice and it is why the machine
    sounds the way it does: the oscillators are digitally clocked so they
    never drift, which is why its chords are clean rather than fat, and all
    the width has to come from the bucket brigade afterwards."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed) if seed is not None else np.random
    x = np.zeros(n)
    for f in notes:
        drift = 1 + 0.0015 * np.sin(2 * np.pi * rs.uniform(0.05, 0.15) * t + rs.rand() * 6)
        ph = np.cumsum(f * drift) / SR + rs.rand()
        x += 2 * (ph % 1.0) - 1                                   # the DCO saw
        if sub:                                                   # the square sub
            x += sub * np.sign(np.sin(2 * np.pi * (ph * 0.5 % 1.0) + pw))
    x /= (1 + sub) * len(notes)
    out = hp(lp(stereo(x), cutoff, order=4), hpf, order=2)
    if res:
        out = out + res * bandpass(stereo(x), cutoff * 0.85, cutoff * 1.18)
    a = min(int(attack * SR), n // 2); r = min(int(release * SR), n // 2)
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a) ** 1.3
    env[-r:] *= np.linspace(1, 0, r) ** 0.9
    return bbd_chorus(out * env[:, None], mode=chorus_mode) * gain * 0.55


# ---- the kit: eight bits of a real drum ----
@cached
def linnkick(dur_steps=4, tune=52.0, gain=1.0, decay=0.32, click=1.0, bits=8):
    """A LinnDrum kick: a real drum, then eight bits and a decimator with no
    anti-alias filter in front of it. The folded-back aliasing is the grit
    everyone remembers, and modern 24-bit playback of the same sample does
    not have it."""
    n, t = steps(dur_steps)
    f = tune * (1 + 2.6 * np.exp(-t / 0.022))
    x = np.tanh(2.1 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / decay)
    x += 0.45 * np.sin(2 * np.pi * tune * 2.1 * t) * np.exp(-t / 0.05)
    # A LinnDrum kick is a recording of a real drum, and a real drum has a
    # shell: the 150-260 Hz knock a synthesised sine simply does not have,
    # and the band an 80s record is otherwise hollow in.
    x += 0.55 * np.sin(2 * np.pi * tune * 3.35 * t) * np.exp(-t / 0.028)
    c = np.random.RandomState(5).randn(n) * np.exp(-t / 0.0022) * 0.7 * click
    c += np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.004) * 0.35 * click
    out = stereo(x) + hp(stereo(c), 1400) * 0.5
    out = bitcrush(out, bits=bits, downsample=2)
    return norm(hp(out, 30) * adsr(n, a=0.0006, r=0.02)[:, None], 0.95) * gain


@cached
def linnsnare(dur_steps=4, gain=1.0, tune=196.0, bright=1.0, bits=8, seed=0):
    """The dry snare. On its own it is small and 1982; `gatedsnare` is what
    the record actually hears."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 179)
    body = (np.sin(2 * np.pi * tune * t) * np.exp(-t / 0.070)
            + 0.55 * np.sin(2 * np.pi * tune * 1.58 * t) * np.exp(-t / 0.045))
    nz = bandpass(stereo(rs.randn(n)), 900 * bright, 8200 * bright)
    out = stereo(body) * 0.9 + nz * np.exp(-t / 0.105)[:, None] * 1.15
    out = bitcrush(np.tanh(1.5 * out), bits=bits, downsample=2)
    return out * adsr(n, a=0.0007, r=0.02)[:, None] * gain * 0.6


@cached
def gatedsnare(dur_steps=6, gain=1.0, hold=0.22, fall=0.018, decay=2.8,
               tone=7000, wet=1.5, tune=212.0, seed=0):
    """The 1980s in one processor chain.

    A bright reverb with **no pre-delay**, so it starts in the same instant
    as the hit and there is no gap to give the trick away, and a gate keyed
    to the snare that cuts the tail off dead after about 220 ms. The mix is
    the point: the gated reverb is louder than the dry snare. Nothing else
    makes a drum sound this big, and nothing else dates a record this
    precisely - which is the whole reason to use it."""
    n, t = steps(dur_steps)
    dry = linnsnare.uncached(dur_steps, gain=1.0, tune=tune, seed=seed)
    rv = reverb(hp(dry, 300), decay=decay, wet=1.0, tone=tone, predelay=0.0)[:n]
    h = int(hold * SR); f = max(int(fall * SR), 8)
    g = np.zeros(n)
    g[:h] = 1.0
    g[h:h + f] = np.linspace(1, 0, min(f, n - h))
    out = dry + wet * rv * g[:, None]
    return out * adsr(n, a=0.0006, r=0.02)[:, None] * gain * 0.5


@cached
def linnhat(dur_steps=1, open_=False, gain=1.0, bits=8, seed=0):
    n, t = steps(dur_steps if not open_ else max(dur_steps, 3.0))
    rs = np.random.RandomState(seed + 181)
    x = hp(stereo(rs.randn(n)), 7200 if open_ else 8600)
    x = x + bandpass(stereo(rs.randn(n)), 4000, 6800) * 0.35
    dec = 0.20 if open_ else 0.026
    out = bitcrush(x * np.exp(-t / dec)[:, None], bits=bits, downsample=2)
    return out * adsr(n, a=0.0004, r=0.008)[:, None] * gain * 0.42


@cached
def linnclap(dur_steps=3, gain=1.0, bits=8, room=0.55, seed=0):
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 191)
    burst = np.zeros(n)
    for d, a in ((0.0, 1.0), (0.010, 0.8), (0.021, 0.62), (0.033, 0.45)):
        k = int(d * SR)
        burst[k:] += rs.randn(n - k) * np.exp(-np.arange(n - k) / SR / 0.010) * a
    st = bandpass(stereo(burst), 950, 5600)
    st[:, 0] = np.roll(st[:, 0], int(SR * 0.0009))
    if room:
        st = st + room * reverb(st, decay=0.55, wet=1.0, tone=6000, predelay=0.004)[:n]
    return bitcrush(st, bits=bits, downsample=2) * adsr(n, a=0.0005, r=0.02)[:, None] * gain * 0.45


@cached
def simmonstom(note=45, dur_steps=3, gain=1.0, sweep=1.5, decay=0.24, noise=0.35,
               seed=0):
    """The hexagonal pad. Not a drum with a pitch - a pitch sweep with a
    drum's envelope: a sine falling an octave and a half in a quarter of a
    second, noise on the strike, through a resonant low-pass. Every pop
    record between 1983 and 1986 ends its eight-bar phrases with a run of
    these."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 193)
    f0 = midi(note)
    f = f0 * (1 + sweep * np.exp(-t / (decay * 0.55)))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    x += 0.3 * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * np.cumsum(f) / SR)) \
         * np.exp(-t / (decay * 0.6))
    x += noise * rs.randn(n) * np.exp(-t / 0.010)
    out = lp(stereo(np.tanh(1.4 * x)), 4200, order=4)
    out = out + 0.5 * bandpass(stereo(x), 900, 2400)
    return hp(out, 55) * adsr(n, a=0.0008, r=0.03)[:, None] * gain * 0.55


# ---- the melodic voices ----
def retrobass(pattern, dur_bars=1, **kw):
    """Driving eighths with octave jumps, through a filter that shuts on
    every note. One oscillator per bar, so the octave leaps are a real
    instrument moving rather than two samples crossfading."""
    kw = dict(dict(f_lo=210.0, f_hi=3000.0, res=2.3, decay=0.12, cut_decay=0.090,
                   drive=2.5, sub=0.52, sub_lp=112.0, low=44.0, detune=0.007,
                   wave='saw', hold=0.10), **kw)
    return cached_line(pattern, dur_bars, **kw)


def sawlead(pattern, dur_bars=1, **kw):
    """The lead. Bright saws, portamento between the notes that are marked
    to slide, and a vibrato that arrives 0.35 s into a held note instead of
    on the attack - which is the difference between a synthesiser sounding
    and somebody playing one. Chorus it, delay it, and double it an octave
    down if it needs to be the chorus of the song."""
    kw = dict(dict(f_lo=420.0, f_hi=7600.0, res=1.5, decay=0.9, cut_decay=0.45,
                   hold=0.86, drive=1.7, sub=0.0, low=260.0, detune=0.011,
                   wave='saw', slide_tau=0.075, glide_ms=4.0,
                   vib=(26.0, 5.4, 0.35), tail_steps=3.0), **kw)
    return cached_line(pattern, dur_bars, **kw)


@cached
def retroarp(freq, dur_steps=1.0, gain=1.0, detune=0.006, f_lo=560.0,
             f_hi=6800.0, res=2.0, decay=0.075, drive=1.6, sub=0.0):
    """The sixteenth-note arp that never stops. Plucky, filtered, and quiet -
    it is the motion of the track, not a part anyone is meant to follow."""
    n, t = steps(dur_steps)
    x = saw(freq * (1 - detune), t) + saw(freq * (1 + detune), t)
    if sub:
        x = x + sub * square(freq * 0.5, t)
    out = morph_lp(stereo(x / 2), f_lo, f_hi, 0.05 + 0.95 * np.exp(-t / decay),
                   bands=7, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0010))
    env = np.exp(-t / (decay * 2.1)) * adsr(n, a=0.0018, r=0.02)
    return out * env[:, None] * gain * 0.45


@cached
def dx7ep(freq, dur_steps=8, gain=1.0, index=2.4, ping=14.0, decay=2.6,
          velocity=0.8):
    """The DX7 electric piano, which has no filter and does not need one: the
    modulator's own envelope collapses faster than the carrier's, so the note
    is bright at the strike and pure by the time it decays - which is what a
    struck object does. `velocity` drives the modulator level, not the
    output, so playing harder changes the timbre rather than the volume."""
    n, t = steps(dur_steps)
    ph = 2 * np.pi * freq * t
    tine = velocity * 0.9 * np.exp(-t / 0.055)
    body = velocity * index * np.exp(-t / 0.42)
    x = np.sin(ph + tine * np.sin(ping * ph) + body * np.sin(ph))
    x = x * np.exp(-t / decay)
    out = stereo(x)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0014))
    return bbd_chorus(hp(out, 120), mode=1, depth_ms=3.4, mix=0.35) \
        * adsr(n, a=0.0012, r=0.05)[:, None] * gain * 0.5


# ---- the medium ----
def cassette(seg, hiss=0.0016, wow_ms=1.1, wow_hz=0.55, flutter_ms=0.28,
             flutter_hz=8.5, top=15500.0, sat=1.25, seed=0):
    """What the decade was actually heard on. Wow at half a hertz, flutter
    at eight and a half, a top end that stops before 16 kHz, tape saturation,
    and a noise floor. Applied to a bus, not a voice - the whole record went
    through one machine, and that is why it sounds like one thing."""
    rs = np.random.RandomState(seed + 197)
    x = wow(seg, depth_ms=wow_ms, rate=wow_hz)
    x = wow(x, depth_ms=flutter_ms, rate=flutter_hz)
    x = np.tanh(sat * x) / np.tanh(sat)
    x = lp(x, top, order=2)
    if hiss:
        n = len(x)
        x = x + hp(np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32),
                   1200) * hiss
    return x.astype(np.float32)
