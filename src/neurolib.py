"""The neurofunk layer: the tight kit, the reese and the growl, at 174 BPM.

Neurofunk is not a break genre. Where jungle chops a recording, this end of
drum & bass builds every hit from parts - a kick that is over in 100 ms so the
bass can have the bar, a snare assembled from a tuned body, a crack and a
fizz, and hats short enough to read as grid rather than as cymbals. The drums
are engineered to leave holes; the bass lives in them.

The bass is the composition, and it is built the way the record was:

    source  ->  multiband split  ->  destroy the top, keep the sub clean
            ->  moving notches (reese) or moving formants (talk)
            ->  distortion  ->  resample and do it again

`nsub()` is always the anchor: one clean mono sine, monophonic, no reverb, no
distortion. Everything called a "bass" in this file is the layer ABOVE it -
`reesemid`, `growlmid`, `talkmid`, `screech`, `wub` all high-pass themselves
off the sub so the two never fight for the same 40 Hz.

Usage:
    from neurolib import *
    s = Session(64, tail=3.0)
    t = s.pos(0); s.hit(t)
    s.place(t, nkick(), bus='drums')
    s.place(t, nsub(29, 8), bus='sub')
    s.place(t, growlmid(41, 4, lfo=6.0), bus='bass')
    s.render('neuro_something_174.wav', drive=1.3, limit=0.9, clip=0.95)
"""
import numpy as np
import core
from core import *
from core import _lfo01, _reverb_ir
from scipy.signal import fftconvolve

BAR, STEP = core.set_grid(bpm=174.0)
BPM = core.BPM

# The sub and the mid bass are one instrument in two bands, so they duck as
# one. The atmosphere ducks a little too - at 174 BPM a pad that does not
# move out of the way turns the gaps between the drums into fog.
Session.DUCKED = {'sub': 1.0, 'body': 0.95, 'bass': 0.85, 'texture': 0.7,
                  'music': 0.5, 'pad': 0.6, 'atmos': 0.35}


# ---- utilities ----
def bus_reverb(buf, decay=2.2, wet=0.22, tone=4200, block_bars=24):
    """Reverb across a whole bus in blocks, so a five-minute buffer never
    asks for a five-minute FFT."""
    n = len(buf)
    out = np.array(buf, dtype=np.float32, copy=True)
    ir = _reverb_ir(decay, tone)
    step_n = max(int(block_bars * BAR), 1)
    for a in range(0, n, step_n):
        seg = buf[a:a + step_n]
        if np.abs(seg).max() < 1e-5:
            continue
        for c in range(2):
            y = fftconvolve(seg[:, c], ir[:, c])
            e = min(a + len(y), n)
            out[a:e, c] += (wet * y[:e - a]).astype(np.float32)
    return out


def mangle(seg, pitch=1.0, drive=2.6, lo=130, hi=6000, crush=0, fold_=0.0):
    """One resampling pass, in place of bouncing to disk: re-pitch, crush,
    distort, band-limit. Two or three of these on a growl produce harmonic
    relationships the oscillator never generated - which is the whole reason
    bass designers resample instead of turning a knob further."""
    x = pitched(seg, pitch) if abs(pitch - 1.0) > 1e-6 else seg
    if crush:
        x = bitcrush(x, crush, 1)
    if fold_:
        x = (1 - fold_) * x + fold_ * fold(x, 1.35)
    x = np.tanh(drive * x) / np.tanh(drive)
    return bandpass(x, lo, hi, order=2).astype(np.float32)


def snoise(n, rs):
    """Decorrelated stereo noise. Two independent streams are genuinely wide
    and genuinely mono-safe: summed they make a quieter noise, where one
    stream Haas-delayed into the other makes a comb with a fixed null. Every
    noise layer in this kit is built from this, which is why the snare stays
    the width of the room and still survives a club sum."""
    return np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)


def hi_spread(seg, hz=420.0, amount=0.4, f_l=780.0, f_r=1450.0):
    """Width above `hz` only, made by notching the two channels at different
    frequencies instead of delaying one. The mono sum keeps both notches -
    two shallow dips - rather than cancelling a band outright."""
    low, high = split(seg, hz)
    l = notch(high, f_l, width=0.3, depth=amount)
    r = notch(high, f_r, width=0.3, depth=amount)
    return (low + np.stack([l[:, 0], r[:, 1]], 1)).astype(np.float32)


def stepped(n, values, smooth=0.004):
    """A tempo-synced stepped LFO: `values` spread evenly over n samples,
    with the edges rounded so the filter does not click on every step."""
    v = np.asarray(values, dtype=np.float64)
    idx = np.minimum((np.arange(n) * len(v) // max(n, 1)), len(v) - 1)
    out = v[idx]
    k = max(int(smooth * SR), 1)
    return np.convolve(out, np.ones(k) / k, mode='same')


# ---- the kit ----
@cached
def nkick(dur_steps=3.0, tune=52.0, top=215.0, tau=0.011, decay=0.10,
          drive=3.2, click=1.0, gain=1.0, seed=0):
    """A kick with the sustain cut off. At 174 BPM there are only two of
    these a bar and the bass has to occupy everything between them, so the
    body is gone in ~100 ms and the weight is carried by the click: 2-5 kHz
    is what still reads as a kick once a growl is sitting on 60-400 Hz."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 3)
    f = tune + (top - tune) * np.exp(-t / tau)
    body = np.tanh(drive * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / decay)
    tail = np.sin(2 * np.pi * tune * 0.99 * t) * np.exp(-t / (decay * 1.3)) * 0.32
    clk = bandpass(stereo(rs.randn(n) * np.exp(-t / 0.0018)), 1800, 6500) * 0.95 * click
    clk += stereo((np.sin(2 * np.pi * 2400 * t) + 0.8 * np.sin(2 * np.pi * 3600 * t))
                  * np.exp(-t / 0.005) * 0.62 * click)
    out = np.tanh(1.25 * (stereo(body + tail) + clk))
    return norm(out * adsr(n, a=0.0004, r=0.02)[:, None], 0.95) * gain


@cached
def nsnare(dur_steps=4.0, gain=1.0, bright=1.0, body=1.0, tune=193.0,
           room=0.30, drive=2.3, seed=0):
    """Three layers welded together: a tuned body at ~190 Hz that gives it a
    pitch, a band-passed crack that gives it its attack, and a long fizz that
    gives it size. Only the crack and the fizz are widened - the body stays
    centred, or the snare loses its front when the club sums to mono."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 11)
    crack = bandpass(snoise(n, rs), 850, min(9000 * bright, 17000)) * np.exp(-t / 0.048)[:, None]
    fizz = hp(snoise(n, rs), 5200) * np.exp(-t / 0.135)[:, None] * 0.42
    tone = (0.85 * np.sin(2 * np.pi * tune * t) * np.exp(-t / 0.045)
            + 0.50 * np.sin(2 * np.pi * tune * 1.72 * t) * np.exp(-t / 0.030)) * body
    x = stereo(tone) * 0.9 + crack * 1.55 + fizz
    x = np.tanh(drive * x) / np.tanh(drive)
    if room:
        x = reverb(x, decay=0.30, wet=room, tone=7000, predelay=0.004)[:n]
    return norm(x * adsr(n, a=0.0006, r=0.03)[:, None], 0.95) * gain


@cached
def nghost(dur_steps=1.0, gain=1.0, bright=1.0, seed=0):
    """The quiet snare between the loud ones. Neurofunk inherits its ghost
    notes from the break it stopped using."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 17)
    x = bandpass(snoise(n, rs), 1900, 8000 * bright) * np.exp(-t / 0.020)[:, None]
    x += stereo(np.sin(2 * np.pi * 205 * t) * np.exp(-t / 0.018)) * 0.35
    return np.tanh(1.6 * x) * adsr(n, a=0.0005, r=0.01)[:, None] * gain * 0.5


@cached
def nhat(dur_steps=0.8, open_=False, gain=1.0, tone=1.0, seed=0):
    """Short and metallic: six detuned squares under noise, high-passed."""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 3.0))
    rs = np.random.RandomState(seed + 5)
    metal = sum(square(f * tone * 2.3, t) for f in HAT808) / 6
    x = stereo(0.55 * metal) + snoise(n, rs) * 0.8
    out = hp(np.tanh(1.5 * x), 7600 if open_ else 9800, order=3)
    dec = 0.17 if open_ else 0.014
    return out * (np.exp(-t / dec) * adsr(n, a=0.0003, r=0.008))[:, None] * gain * 0.5


@cached
def nride(dur_steps=2.0, gain=1.0, tone=1.0, seed=0):
    """ping with a wash under it - carries 16ths without the hiss of a hat"""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 23)
    ping = np.sin(2 * np.pi * 3150 * tone * t) * np.exp(-t / 0.035) * 0.5
    ping += np.sin(2 * np.pi * 4720 * tone * t) * np.exp(-t / 0.02) * 0.3
    wash = hp(snoise(n, rs), 7000) * np.exp(-t / 0.16)[:, None] * 0.35
    return (stereo(ping) + wash) * adsr(n, a=0.0004, r=0.02)[:, None] * gain * 0.5


@cached
def ntick(dur_steps=0.6, gain=1.0, f=1850.0, seed=0):
    """rim/click for the in-between 16ths"""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 29)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006)
    x += rs.randn(n) * np.exp(-t / 0.0025) * 0.55
    out = bandpass(stereo(np.tanh(2.2 * x)), 900, 8000)
    return out * adsr(n, a=0.0004, r=0.008)[:, None] * gain * 0.55


@cached
def dust(dur_steps=16.0, gain=1.0, density=26, seed=0):
    """The dirt a chopped break leaves behind: sparse band-passed noise
    grains scattered off the grid. Under a programmed kit it does the job the
    ghost notes of a sampled break used to do - it stops the drums sounding
    like a drum machine without adding anything you can name."""
    n, _ = steps(dur_steps)
    rs = np.random.RandomState(seed + 31)
    x = np.zeros(n)
    for _ in range(int(density * dur_steps / 16)):
        a = rs.randint(0, max(n - 900, 1))
        m = rs.randint(200, 900)
        tt = np.arange(m) / SR
        x[a:a + m] += rs.randn(m) * np.exp(-tt / rs.uniform(0.004, 0.02)) * rs.uniform(0.2, 0.8)
    out = bandpass(stereo(x), 3200, 11000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0011))
    return out * gain * 0.35


def roll(s, b, st, count, spacing=0.5, bus='drums', gain=0.8, accel=False,
         seed=0, **kw):
    """a snare roll: `count` hits from step `st`, optionally accelerating"""
    pos = float(st)
    sp = float(spacing)
    for i in range(count):
        v = gain * (0.55 + 0.45 * (i + 1) / count)
        s.place(s.pos(b, pos), nsnare(2.0, bright=1.05, room=0.18,
                                      seed=seed + i % 3, **kw), v, bus)
        pos += sp
        if accel:
            sp *= 0.86


# ---- the bass: the sub ----
@cached
def nsub(note, dur_steps, glide=None, gain=1.0, decay=0.0, drive=1.3,
         click=0.0):
    """The anchor. One sine, dead centre, monophonic, nothing done to it.

    Every other bass voice in this file high-passes itself above 100 Hz so
    this one owns the bottom alone. Two sub notes overlapping cancel and jump
    in level; keep it strictly one at a time."""
    n, t = steps(dur_steps)
    f0 = midi(note)
    f = np.full(n, f0) if glide is None else f0 + (midi(glide) - f0) * np.exp(-t / 0.05)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    x = np.tanh(drive * x) / np.tanh(drive)
    if click:
        x = x + np.sin(4 * ph) * np.exp(-t / 0.008) * click
    env = adsr(n, a=0.004, r=0.035)
    if decay:
        env = env * np.exp(-t / decay)
    return stereo(x * env) * gain * 0.9


# ---- the bass: the mid layers ----
@cached
def reesemid(note, dur_steps, gain=1.0, detune=13.0, cutoff=2600, sweep=1.0,
             rate=0.8, depth_ms=4.6, drive=2.0, low=95, tilt=4.5, kmax=44,
             spread=0.14, seed=0):
    """Three saws - one exactly on pitch, two symmetrically detuned - then a
    moving comb.

    The detune alone gives a slow beat and nothing else: at 87 Hz, 17 cents
    is under a hertz. What moves is the flanger, whose notches walk across
    the harmonics and bite a different amount on each oscillator because they
    are not in phase with each other. That is a Reese.

    The centre oscillator is what keeps it a note. Detune every oscillator
    and there is no longer a frequency the ear can call the pitch - it hears
    a chord of near-misses, which is the difference between a bass that
    sounds driven and one that sounds broken.

    `sweep` walks the comb once across the note on top of the LFO. Without
    it a note shorter than a beat only sees a fraction of an LFO cycle and
    the reese is static - which is the difference between the 1993 version of
    this sound and the modern one.

    The drive comes AFTER the filter and after a normalise, so it actually
    clips; `tilt` then lifts the harmonics it made. A reese that is all
    fundamental disappears on a phone, and this is a mid-range instrument -
    `nsub` is underneath it doing the low end."""
    n, t = steps(dur_steps)
    f = midi(note)
    rs = np.random.RandomState(seed + 7)
    x = np.zeros(n)
    for c in (-detune, 0.0, detune):
        x += saw(f * 2 ** (c / 1200), t, kmax=kmax, phase=rs.rand() * 6.28)
    out = lp(stereo(np.tanh(1.5 * x / 3)), cutoff)
    env = np.clip(sweep * (t / max(t[-1], 1e-9))
                  + (1 - sweep) * _lfo01(t, rate), 0, 1) if sweep else None
    out = flanger(out, rate=rate, depth_ms=depth_ms, base_ms=0.45, fb=0.65,
                  mix=0.9, taps=4, env=env, spread=spread)
    out = np.tanh(drive * norm(out, 0.85)) / np.tanh(drive)
    out = shelf(out, 850, tilt, 'high')
    out = hp(out, low, order=4)
    return norm(out, 0.9) * adsr(n, a=0.006, r=0.04)[:, None] * gain * 0.55


@cached
def growlmid(note, dur_steps, gain=1.0, ratio=2.0, fm=4.0, lfo=6.0, sync=2.2,
             f_lo=250, f_hi=4600, res=1.9, drive=2.2, low=92, open_=1.0,
             floor_=0.18, bands=7, seed=0):
    """The growl. FM at an inharmonic ratio, a hard-synced saw over it, and a
    resonant lowpass driven by an LFO fast enough that the modulation is
    heard as timbre rather than as rhythm.

    `lfo` is the whole personality: 2-4 Hz reads as a wobble, 8-20 Hz as a
    growl, past 30 as a scream.

    `ratio` must be a whole number to keep a pitch. FM at ratio 1.5 puts its
    sidebands at 0.5, 2.5 and 5.5 times the note - the harmonic series of an
    octave BELOW it - so half the energy lands between the note's own
    harmonics and the ear reads the result as detuned rather than as driven.
    2.0 is the defined growl, 3.0 the bright one; 1.5 is available when a
    part is meant to sound rotten, and nowhere else."""
    n, t = steps(dur_steps)
    f = midi(note)
    m = _lfo01(t, lfo)
    idx = fm * (0.25 + 0.75 * m)
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * ratio * t))
    x += 0.7 * saw(f, t, kmax=36)
    x += 0.55 * sync_saw(t, f * 1.004, sync * (1 + 0.8 * m))
    x = np.tanh(2.0 * x / 2.3)
    cut = np.clip(floor_ + (open_ - floor_) * (0.3 + 0.7 * m), 0, 1)
    out = morph_lp(stereo(x), f_lo, f_hi, cut, bands=bands, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out = hp(out, low, order=4)
    return out * adsr(n, a=0.004, r=0.035)[:, None] * gain * 0.55


@cached
def snarl(note, dur_steps, gain=1.0, lfo=18.0, pattern=None, fm=3.0, ratio=2.0,
          sync=2.6, tear=2.2, f_lo=150, f_hi=9000, res=3.8, drive=3.0,
          fold_=0.45, bright=1.0, transient=1.0, punch=1.8, low=95,
          decay=0.0, crush=0, seed=0):
    """The aggressive one. Four things separate it from `growlmid`, and each
    was a number that came up short when the two were measured side by side.

    **A front edge.** A growl that fades in has +4 dB of attack over its own
    body; a hit that sounds violent has +12 to +18. So there is a real
    transient welded onto the front - a band-passed noise burst and a click,
    5 ms long - and the filter opens fully underneath it.

    **Teeth.** The old voice put 6 to 17 dB less energy above 1 kHz than
    below it, which is all weight and no bite. A wavefolder rather than a
    tanh, plus a square in the source, moves the balance up: `fold` keeps
    generating new partials after `tanh` has flattened out.

    **Depth, not just rate.** Modulating the cutoff quickly is not the same
    as modulating it far. The fast growls swung 5.9 dB; this one swings the
    filter across its whole range, which is 15-20.

    **Odd harmonics.** Even-harmonic distortion is warm - octaves and fifths.
    Odd is hollow and hard, and it is what a screaming bass is made of.

    `pattern` sequences the cutoff in steps instead of an LFO; `crush` adds a
    resampling pass, which is where the last of the nastiness comes from."""
    n, t = steps(dur_steps)
    f = midi(note)
    m = stepped(n, pattern) if pattern else _lfo01(t, lfo)

    # source: sync + square for the odd harmonics, FM at an integer ratio so
    # the sidebands stay on the note's own series
    x = sync_saw(t, f, sync * (1 + tear * m))
    x += 0.8 * square(f, t, kmax=34)
    x += 0.7 * np.sin(2 * np.pi * f * t
                      + fm * (0.2 + 0.8 * m) * np.sin(2 * np.pi * f * ratio * t))
    x = np.tanh(1.6 * x / 2.3)

    # the filter slams shut and open across its whole range, not a corner of it
    cut = np.clip(0.04 + 0.96 * m, 0, 1)
    if decay:
        cut = np.clip(cut * np.exp(-t / decay) + 0.05, 0, 1)
    out = morph_lp(stereo(x), f_lo, f_hi * bright, cut, bands=8, res=res)

    # a wavefolder, not a saturator: tanh stops making partials once it is
    # flat, and folding does not
    out = (1 - fold_) * np.tanh(drive * out) + fold_ * fold(out * 1.3, 1.5)
    if crush:
        out = mangle(out, pitch=1.0, drive=drive * 0.8, lo=low, hi=11000,
                     crush=crush, fold_=0.2)
    out = hp(out, low, order=4)
    out = shelf(out, 1400, 4.0 * bright, 'high')      # teeth, not weight
    out = hi_spread(out, hz=420, amount=0.32, f_l=900, f_r=1700)

    # A note that holds one level has no front, however hard it is driven.
    # The punch is a shaped envelope: a spike that is gone in 12 ms over a
    # body 5 dB below it, which is what makes a hit read as a hit.
    env = (1.0 + punch * np.exp(-t / 0.012)) * adsr(n, a=0.0012, r=0.03)
    out = out * env[:, None]

    # the transient goes on last, after every zero-phase filter in the chain.
    # sosfiltfilt runs forwards and backwards, so anything sharp put through
    # it comes out smeared in both directions - which is exactly what a
    # transient must not be.
    if transient:
        rs = np.random.RandomState(seed + 71)
        k = min(int(0.007 * SR), n)
        tt = np.arange(k) / SR
        nz = rs.randn(k, 2).astype(np.float32)
        cl = nz * np.exp(-tt / 0.0018)[:, None] * 0.9
        cl += stereo((np.sin(2 * np.pi * 2100 * tt) + 0.8 * np.sin(2 * np.pi * 3400 * tt)
                      + 0.5 * np.sin(2 * np.pi * 5600 * tt)) * np.exp(-tt / 0.0026)) * 0.6
        cl[:, 0] *= 1.0 - 0.12 * rs.rand()
        out[:k] += np.tanh(1.8 * cl) * transient * 1.4

    return norm(out, 0.95) * gain * 0.45


@cached
def talkmid(note, dur_steps, v0='oo', v1='ee', gain=1.0, fm=3.0, lfo=5.0,
            drive=2.0, low=95, ratio=2.0, seed=0):
    """The bass that says a word. A growl source through two formant pairs,
    crossfading from one vowel to the other over the note - the formants sit
    where they sit regardless of the pitch, which is why the ear hears a
    mouth instead of a filter."""
    n, t = steps(dur_steps)
    f = midi(note)
    m = _lfo01(t, lfo)
    x = np.sin(2 * np.pi * f * t + fm * (0.3 + 0.7 * m) * np.sin(2 * np.pi * f * ratio * t))
    x += 0.6 * saw(f, t, kmax=40)
    src = np.tanh(2.2 * stereo(x / 1.7))
    out = morph_formant(src, v0, v1, env=np.linspace(0, 1, n) ** 0.8, wet=0.92, gain=1.7)
    out = np.tanh(drive * out) / np.tanh(drive)
    out = hp(out, low, order=4)
    return out * adsr(n, a=0.005, r=0.04)[:, None] * gain * 0.5


@cached
def wub(note, dur_steps, pattern=(0.15, 0.9, 0.3, 1.0, 0.2, 0.7, 0.45, 1.0),
        gain=1.0, f_lo=210, f_hi=5200, res=2.4, drive=2.2, low=92, seed=0):
    """A held note whose filter is sequenced. The pitch does not move; the
    cutoff plays the rhythm, one value per slot of `pattern`."""
    n, t = steps(dur_steps)
    f = midi(note)
    rs = np.random.RandomState(seed + 13)
    x = saw(f, t, kmax=40) + saw(f * 1.005, t, kmax=40, phase=rs.rand() * 6.28)
    x += 0.5 * square(f * 0.5, t, kmax=30)
    x = np.tanh(1.7 * x / 2.5)
    cut = stepped(n, pattern)
    out = morph_lp(stereo(x), f_lo, f_hi, cut, bands=7, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out = hp(out, low, order=4)
    return out * adsr(n, a=0.004, r=0.03)[:, None] * gain * 0.55


@cached
def talkline(note, dur_steps, vowels=('oo', 'ah', 'ee'), gain=1.0, fm=3.0,
             lfo=5.0, ratio=2.0, drive=2.0, low=95, curve=1.0, seed=0):
    """`talkmid` with more than one syllable: the note walks through a whole
    list of vowels instead of crossfading between two.

    Two vowels read as a filter opening. Three or more read as a mouth
    changing shape, because the formant pair jumps to a new place instead of
    sliding through the space between - which is what makes it sound like it
    is saying something rather than being swept."""
    n, t = steps(dur_steps)
    f = midi(note)
    m = _lfo01(t, lfo)
    x = np.sin(2 * np.pi * f * t + fm * (0.3 + 0.7 * m) * np.sin(2 * np.pi * f * ratio * t))
    x += 0.6 * saw(f, t, kmax=40)
    src = np.tanh(2.2 * stereo(x / 1.7))
    u = (np.linspace(0, 1, n) ** curve) * (len(vowels) - 1)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, v in enumerate(vowels):
        w = np.clip(1 - np.abs(u - i), 0, 1)
        if w.max() < 1e-4:
            continue
        vf = sum(bandpass(src, fc * 0.74, fc * 1.30) * g
                 for fc, g in zip(FORMANTS[v], (1.0, 0.72, 0.34)))
        out += (vf * w[:, None]).astype(np.float32)
    out = np.tanh(drive * out * 1.7) / np.tanh(drive)
    out = hp(out, low, order=4)
    return out * adsr(n, a=0.005, r=0.04)[:, None] * gain * 0.5


@cached
def funkmid(note, dur_steps, gain=1.0, f_lo=320, f_hi=6800, res=2.2,
            decay=0.07, drive=2.2, low=95, seed=0):
    """The bouncing mid bass. Same oscillators as the growl, but the filter
    snaps shut in 70 ms instead of being driven by an LFO, so every note has
    a bright front and a dark back and the line reads as plucked.

    A growl fills its note; this one leaves most of it empty. That gap is the
    whole difference between a bassline that broods and one that bounces."""
    n, t = steps(dur_steps)
    f = midi(note)
    rs = np.random.RandomState(seed + 19)
    x = saw(f, t, kmax=48) + 0.55 * square(f * 1.004, t, kmax=36)
    x = np.tanh(1.6 * x / 1.6)
    out = morph_lp(stereo(x), f_lo, f_hi, np.exp(-t / decay), bands=7, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out = hp(out, low, order=4)
    env = np.exp(-t / max(decay * 2.6, 0.03)) * adsr(n, a=0.002, r=0.02)
    return out * env[:, None] * gain * 0.55


@cached
def chank(notes, dur_steps=1.0, gain=1.0, lo=420, hi=4200, decay=0.045,
          drive=2.6, seed=0):
    """The muted 16th-note funk chord: a chord played as percussion. Band
    limited well above the bass and gone in 50 ms, so sixteen of them a bar
    add groove and no mud."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 53)
    x = np.zeros(n)
    for f in notes:
        x += saw(f, t, kmax=26, phase=rs.rand() * 6.28) + 0.4 * square(f * 2, t, kmax=18)
    x = np.tanh(drive * x / (2 * len(notes)))
    out = bandpass(stereo(x), lo, hi, order=2)
    out += 0.25 * hp(stereo(rs.randn(n) * np.exp(-t / 0.002)), 2500)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    env = np.exp(-t / decay) * adsr(n, a=0.0015, r=0.012)
    return out * env[:, None] * gain * 0.5


@cached
def blip(freq, dur_steps=1.0, gain=1.0, bend=0.30, decay=0.06, seed=0):
    """A bright bleep that bends down into pitch. Cheap, cheerful, and the
    one voice here that is allowed to sound like a toy."""
    n, t = steps(dur_steps)
    f = freq * (1 + bend * np.exp(-t / 0.022))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = saw_ph(ph, freq * (1 + bend) * 30, kmax=30) * 0.6 + np.sin(ph)
    out = lp(stereo(np.tanh(1.5 * x)), 7000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0011))
    return out * (np.exp(-t / decay) * adsr(n, a=0.001, r=0.015))[:, None] * gain * 0.5


def whoop(dur_steps=8, f0=280.0, f1=1500.0, gain=1.0, curve=1.9, seed=0):
    """A rising whistle with a body: the fill that says something good is
    about to happen, without the eight bars a riser needs."""
    n, t = steps(dur_steps)
    u = (t / max(t[-1], 1e-9)) ** curve
    f = f0 * (f1 / f0) ** u
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)
    out = stereo(np.tanh(1.4 * x))
    rs = np.random.RandomState(seed + 59)
    out += bandpass(snoise(n, rs), 900, 6000) * (0.25 * u)[:, None]
    out = widen(out, 1.1)
    return out * (np.sin(np.pi * t / max(t[-1], 1e-9)) ** 0.6)[:, None] * gain * 0.4


# ---- the phrase: bass as one continuous voice ----
def _lock(pattern, n, key, default, smooth=0.028):
    """read one parameter-locked column of a pattern into a per-sample array"""
    out = np.full(n, float(default))
    for ev in pattern:
        st, note, dur = ev[0], ev[1], ev[2]
        kw = ev[3] if len(ev) > 3 else {}
        a = int(st * STEP); b = min(int((st + dur) * STEP), n)
        if a >= n or b <= a:
            continue
        v = kw.get(key, default)
        if isinstance(v, (tuple, list)):
            out[a:b] = stepped(b - a, v, smooth=smooth)
        else:
            out[a:b] = float(v)
    k = max(int(smooth * SR), 1)
    return np.convolve(out, np.ones(k) / k, mode='same')


def _phrase_freq(pattern, n, glide):
    """instantaneous frequency and gate for a whole phrase, with real slides"""
    f = np.zeros(n)
    amp = np.zeros(n)
    prev = None
    for ev in pattern:
        st, note, dur = ev[0], ev[1], ev[2]
        kw = ev[3] if len(ev) > 3 else {}
        a = int(st * STEP); b = min(int((st + dur) * STEP), n)
        if a >= n or b <= a:
            continue
        tt = np.arange(b - a) / SR
        tgt = midi(note)
        if kw.get('slide') and prev is not None:
            f[a:b] = tgt + (prev - tgt) * np.exp(-tt / glide)
        else:
            f[a:b] = tgt
        g = kw.get('amp', 1.0)
        if isinstance(g, (tuple, list)):
            env = stepped(b - a, g, smooth=0.004)
        else:
            env = np.full(b - a, float(g))
        # only the edges of a note are shaped; the middle is left alone, so a
        # legato phrase has no attack in it at all
        k = min(int(0.004 * SR), (b - a) // 2)
        if k > 1 and not kw.get('legato'):
            env[:k] *= np.linspace(0, 1, k)
        if k > 1:
            env[-k:] *= np.linspace(1, 0, k)
        amp[a:b] = np.maximum(amp[a:b], env)
        prev = tgt
    if f.max() == 0:
        f[:] = 55.0
    # a gap in the pattern keeps the last frequency, so the oscillator never
    # has to jump when the gate opens again
    idx = np.maximum.accumulate(np.where(f > 0, np.arange(n), 0))
    return f[idx], amp


def neurophrase(pattern, dur_bars=1, gain=1.0, f_lo=170, f_hi=7000, res=2.6,
                drive=3.0, low=95, glide=0.045, ratio=2.0, vowels=None,
                bands=9, spread=0.0, smooth=0.008, octave=0, sync_mul=1.0,
                fm_mul=1.0, lfo_depth=0.55, square=0.0, fold_=0.0, punch=0.0,
                transient=0.0, tilt=0.0, seed=0):
    """A whole phrase of bass rendered as ONE voice, the way the records do it.

    Everything else in this module is a note: it starts, it decays, it stops,
    and the next note starts a fresh oscillator. Measure a finished neurofunk
    record and that is not what is there. The mid bass makes four to six
    attacks in a bar - a quarter of what a written-out riff makes - and the
    low end sounds for 85% of it. What moves is not the notes. It is the
    filter, the sync ratio, the FM index and the vowel, sequenced per
    sixteenth across the whole bar, over an oscillator that never restarts.

    That is the difference between a bassline and a bass. A retriggered
    envelope puts a transient at the front of every event and resets the
    timbre with it; here the timbre carries across the note change, so a bar
    is one gesture instead of sixteen small ones.

    pattern: [(step, note, dur_steps, {...}), ...] where the dict locks this
    note's parameters, each of which may be a single value or a tuple that is
    stepped through the note:

        cut    0..1 filter position     sync   hard-sync ratio
        fm     FM index                 vow    0..1 position between vowels
        amp    0..1 gate                slide  glide from the previous note
        lfo    Hz of the fast modulation on the cutoff and the index
        legato no attack shaping at the note's start

    **`lfo` may be a tuple, and that is the whole point.** A single value is
    a growl at a fixed rate. A tuple is a rate that CHANGES while one note is
    still sounding - and because the modulator's phase is integrated from the
    rate rather than reset per step, the growl accelerates and decelerates
    continuously instead of jumping. One long note given `(4, 9, 18, 34, 20,
    8)` starts as a slow sweep, tears into a scream and settles again, which
    is what a bassline in this genre actually does. A row of short notes each
    at its own fixed rate is an arpeggiator with a filter on it, however
    varied the notes are.

    `lfo` is what separates this from a slow filter sweep, and it is worth
    measuring. Take the amplitude envelope of 200-1200 Hz on a finished
    record and look at how fast it wobbles: 13-28% of that movement sits
    between 10 and 90 Hz. That band is the growl. Modulation slower than
    5 Hz reads as a filter opening; between 10 and 20 Hz it reads as the
    sixteenth-note grid; past 20 it stops being rhythm and becomes timbre.

    `spread` renders the phrase twice with different oscillator phases and
    puts one in each channel - genuinely decorrelated width, which is what a
    finished record measures at 400-1200 Hz and a Haas delay cannot give.
    """
    n = int(round(dur_bars * BAR))
    f, amp = _phrase_freq(pattern, n, glide)
    f = f * 2 ** (octave / 12.0)      # the mid layer sits above its own sub
    # The steps glide into each other rather than jumping. A hard step in the
    # cutoff is a transient, and a bar full of them reads as a gate chopping
    # the bass up - the references make four to six attacks in a bar, not
    # forty. `smooth` is what keeps the movement without the edges.
    cut = np.clip(_lock(pattern, n, 'cut', 0.55, smooth), 0, 1)
    # `sync_mul=0` flattens the ratio to 1 and turns the voice into a plain
    # filtered saw: the body layer between the sub and the character layer.
    # A hard sync edge at 33 Hz is a buzz once per cycle, not a growl, so the
    # bottom two octaves of the bass are built without one.
    syn = 1.0 + (_lock(pattern, n, 'sync', 1.0, smooth) - 1.0) * sync_mul
    fmi = _lock(pattern, n, 'fm', 1.2, smooth) * fm_mul
    vow = np.clip(_lock(pattern, n, 'vow', 0.0, smooth), 0, 1)
    # The rate is smoothed, then integrated. Smoothing makes the acceleration
    # continuous; integrating means the modulator never restarts, so a rate
    # that triples across a note glides up to it rather than stepping.
    lf = _lock(pattern, n, 'lfo', 0.0, 0.045)
    if lfo_depth and lf.max() > 0.01:
        m = 0.5 - 0.5 * np.cos(2 * np.pi * np.cumsum(lf) / SR)
        cut = np.clip(cut * (1 - lfo_depth + lfo_depth * m), 0, 1)
        fmi = fmi * (1 - 0.5 * lfo_depth + 0.5 * lfo_depth * m)
        syn = syn * (1 - 0.35 * lfo_depth + 0.35 * lfo_depth * m)

    def voice(ph_off):
        ph = 2 * np.pi * (np.cumsum(f) / SR + ph_off)
        mph = (ph / (2 * np.pi)) % 1.0
        x = 2 * ((mph * syn) % 1.0) - 1                      # hard sync
        x += 0.75 * np.sin(ph + fmi * np.sin(ratio * ph))    # FM, integer ratio
        x += 0.5 * saw_ph(ph, float(f.max()) * 26, kmax=26)
        if square:
            # odd harmonics: hollow and hard where even ones are warm
            x += square * (2.0 * (np.sign(np.sin(ph)) * 0.5) )
        return np.tanh(1.7 * x / (2.2 + square))

    if spread:
        rs = np.random.RandomState(seed + 61)
        l, r = voice(rs.rand()), voice(rs.rand())
        src = np.stack([l, (1 - spread) * l + spread * r], 1).astype(np.float32)
    else:
        src = stereo(voice(0.0))
    out = morph_lp(src, f_lo, f_hi, cut, bands=bands, res=res)
    if vowels:
        out = morph_formant(out, vowels[0], vowels[1], env=vow, wet=0.5, gain=1.35)
    if fold_:
        # a wavefolder keeps generating partials after a tanh has gone flat
        out = (1 - fold_) * np.tanh(drive * out / (1 + res * 0.35)) \
              + fold_ * fold(out * 1.2 / (1 + res * 0.35), 1.45)
    else:
        out = np.tanh(drive * out / (1 + res * 0.35))
    out = hp(out, low, order=4)
    if tilt:
        out = shelf(out, 1400, tilt, 'high')
    if punch:
        # every note gets a front edge, the long ones included
        env = np.ones(n)
        for ev in pattern:
            a = int(ev[0] * STEP)
            if 0 <= a < n:
                k = min(int(0.05 * SR), n - a)
                env[a:a + k] += punch * np.exp(-np.arange(k) / SR / 0.012)
        out = out * env[:, None]
    out = out * amp[:, None]
    if transient:
        rs = np.random.RandomState(seed + 83)
        for ev in pattern:
            a = int(ev[0] * STEP)
            if not (0 <= a < n):
                continue
            k = min(int(0.007 * SR), n - a)
            tt = np.arange(k) / SR
            cl = rs.randn(k, 2).astype(np.float32) * np.exp(-tt / 0.0018)[:, None] * 0.9
            cl += stereo((np.sin(2 * np.pi * 2100 * tt) + 0.8 * np.sin(2 * np.pi * 3400 * tt))
                         * np.exp(-tt / 0.0026)) * 0.6
            out[a:a + k] += np.tanh(1.8 * cl) * transient * 1.2
    return out.astype(np.float32) * gain * 0.6


def subphrase(pattern, dur_bars=1, gain=1.0, glide=0.045, drive=1.4, seed=0):
    """The same phrase, as the clean mono sine underneath it. One oscillator,
    one continuous phase, so a slide really slides and two notes never overlap
    into a level jump."""
    n = int(round(dur_bars * BAR))
    f, amp = _phrase_freq(pattern, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    x = np.tanh(drive * x) / np.tanh(drive)
    return stereo(x * amp).astype(np.float32) * gain * 0.9


@cached
def _phrase_cached(key, dur_bars, **kw):
    pat = [(p[0], p[1], p[2], dict(p[3])) for p in key]
    return neurophrase(pat, dur_bars, **kw)


def phrase(pattern, dur_bars=1, **kw):
    """cached neurophrase - the same bar is played dozens of times"""
    key = tuple((p[0], p[1], p[2],
                 tuple(sorted((k, v) for k, v in (p[3] if len(p) > 3 else {}).items())))
                for p in pattern)
    return _phrase_cached(key, dur_bars, **kw)


@cached
def _subphrase_cached(key, dur_bars, **kw):
    pat = [(p[0], p[1], p[2], dict(p[3])) for p in key]
    return subphrase(pat, dur_bars, **kw)


def subph(pattern, dur_bars=1, **kw):
    key = tuple((p[0], p[1], p[2],
                 tuple(sorted((k, v) for k, v in (p[3] if len(p) > 3 else {}).items())))
                for p in pattern)
    return _subphrase_cached(key, dur_bars, **kw)


@cached
def screech(note, dur_steps, r0=1.6, r1=7.0, gain=1.0, drive=3.0, low=300,
            hi=9000, curve=1.6, seed=0):
    """Hard sync swept from r0 to r1: the pitch never moves, the timbre tears
    upward. The one gesture in this genre that a filter cannot fake."""
    n, t = steps(dur_steps)
    f = midi(note)
    u = (t / max(t[-1], 1e-9)) ** curve
    ratio = r0 + (r1 - r0) * u
    x = sync_saw(t, f, ratio) + 0.6 * sync_saw(t, f * 1.008, ratio * 0.75)
    x = np.tanh(drive * x / 1.6)
    out = bandpass(stereo(x), low, hi, order=2)
    out = widen(out, 0.9)
    env = np.exp(-t / max(0.09 * dur_steps, 0.05)) * adsr(n, a=0.003, r=0.03)
    return out * env[:, None] * gain * 0.4


@cached
def neurolead(note, dur_steps, gain=1.0, r0=1.0, r1=3.4, fm=1.6, ratio=2.0,
              lfo=9.0, f_lo=620, f_hi=9500, res=3.0, decay=0.09, drive=3.2,
              low=260, curve=1.4, vowels=None, pattern=None, seed=0):
    """A lead built the way the bass is, and for the same reason.

    A melody in this genre is not a synth patch playing notes - it is the
    same designed sound as the bass, an octave and a half up. The sync ratio
    sweeps from `r0` to `r1` inside every single note, so the timbre tears
    upward while the pitch stays exactly where it is: hard sync is periodic
    at the master oscillator, so every partial still lands on the note's own
    harmonic series and the line remains singable while it screams.

    That is the whole difference between this and an arpeggiator. An arp
    holds one timbre and changes the note; this holds the note and changes
    what it is made of. Give consecutive notes different `r1` values and no
    two events in the bar sound like the same instrument.

    `pattern` replaces the smooth sweep with a stepped one - the ratio jumps
    between fixed values instead of gliding, which puts a rhythm inside a
    note that is only a sixteenth long. It is worth measuring: a smooth
    sweep moves the spectral centroid about 1.4 octaves across a note, a
    stepped one moves it 2.6 and puts ten times as much energy above
    2.5 kHz. Nearly every note of a lead in this genre has one."""
    n, t = steps(dur_steps)
    f = midi(note)
    u = (t / max(t[-1], 1e-9)) ** curve
    m = _lfo01(t, lfo)
    shape = stepped(n, pattern) if pattern else u
    ratio_env = r0 + (r1 - r0) * shape
    x = sync_saw(t, f, ratio_env)
    x += 0.6 * sync_saw(t, f * 1.006, ratio_env * 0.66)
    x += 0.5 * np.sin(2 * np.pi * f * t
                      + fm * (0.3 + 0.7 * m) * np.sin(2 * np.pi * f * ratio * t))
    x = np.tanh(1.8 * x / 2.1)
    # The filter OPENS as the sync tears upward. A cutoff that closes over
    # the note is a plucked-string gesture - correct for an arpeggiator, and
    # the exact thing that cancels a sync sweep, because the harmonics the
    # sync is generating are removed as fast as they appear.
    cut = np.clip((0.3 + 0.7 * shape) * (0.55 + 0.45 * m)
                  * np.exp(-t / max(decay * 3.5, 0.05)), 0, 1)
    out = morph_lp(stereo(x), f_lo, f_hi, cut, bands=7, res=res)
    if vowels:
        out = morph_formant(out, vowels[0], vowels[1], env=u, wet=0.45, gain=1.3)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out = hp(out, low, order=4)
    out = hi_spread(out, hz=700, amount=0.3, f_l=1600, f_r=2900)
    env = np.exp(-t / max(decay * 2.2, 0.04)) * adsr(n, a=0.002, r=0.025)
    return out * env[:, None] * gain * 0.45


@cached
def stab(notes, dur_steps=2.0, gain=1.0, drive=5.0, lo=320, hi=6000,
         decay=0.09, metal=0.4, seed=0):
    """A chord used as percussion: saws clipped flat, band-limited above the
    bass, with a metallic transient on the front."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 37)
    x = np.zeros(n)
    for f in notes:
        for d in (0.994, 1.0, 1.007):
            x += saw(f * d, t, kmax=30, phase=rs.rand() * 6.28)
    x = np.tanh(drive * x / (3 * len(notes)))
    out = bandpass(stereo(x), lo, hi, order=2)
    out += metal * hp(stereo(rs.randn(n) * np.exp(-t / 0.004)), 3000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    env = np.exp(-t / decay) * adsr(n, a=0.002, r=0.02)
    return out * env[:, None] * gain * 0.5


# ---- atmosphere ----
def voidpad(notes, dur_steps, cutoff=760, gain=1.0, wide=1.6, seed=None):
    """Dark, slow, and never the same twice: detuned saws with independent
    random phases and a noise bed, low-passed hard so it sits under
    everything. Not cached - the randomness is the point."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed) if seed is not None else np.random
    x = np.zeros(n)
    for f in notes:
        for d in (0.994, 0.999, 1.005):
            x += 2 * ((f * d * t + rs.rand()) % 1.0) - 1
    x /= 3 * len(notes)
    x += lp(stereo(rs.randn(n)), 500)[:, 0] * 0.25
    out = lp(stereo(np.tanh(1.2 * x)), cutoff)
    out = widen(out, wide)
    a = min(int(0.45 * SR), n // 2)
    r = min(int(0.6 * SR), n // 2)
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a) ** 1.5
    env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain


def metaldrone(freq, dur_steps, gain=1.0, seed=None):
    """Inharmonic partials beating slowly against each other - the sound of
    a very large object that has not moved for a long time."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed) if seed is not None else np.random
    x = np.zeros(n)
    for mult, amp, rate in ((1.0, 1.0, 0.037), (2.41, 0.45, 0.053),
                            (3.83, 0.28, 0.071), (5.19, 0.16, 0.089),
                            (0.5, 0.6, 0.029)):
        breath = 0.5 + 0.5 * np.sin(2 * np.pi * rate * t + rs.rand() * 6)
        x += amp * np.sin(2 * np.pi * freq * mult * t + rs.rand() * 6) * breath
    out = stereo(np.tanh(x / 2.2))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0022))
    a = min(int(1.4 * SR), n // 2)
    r = min(int(1.8 * SR), n // 2)
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain


@cached
def sonar(dur_steps=4.0, freq=760.0, gain=1.0, seed=0):
    """one ping. Give it to place_echo and a long reverb and it is a room."""
    n, t = steps(dur_steps)
    x = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.09)
    x += 0.4 * np.sin(2 * np.pi * freq * 1.5 * t) * np.exp(-t / 0.05)
    return stereo(np.tanh(1.4 * x)) * adsr(n, a=0.002, r=0.05)[:, None] * gain * 0.5


def chatter(dur_steps=8.0, gain=1.0, seed=0):
    """Radio traffic with the words removed: band-limited noise gated into
    syllables, squashed into a comms bandwidth."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 41)
    env = np.zeros(n)
    p = 0
    while p < n:
        ln = rs.randint(int(0.05 * SR), int(0.22 * SR))
        if rs.rand() < 0.55:
            e = min(p + ln, n)
            env[p:e] = rs.uniform(0.3, 1.0) * np.hanning(max(e - p, 2))[:e - p]
        p += ln + rs.randint(int(0.02 * SR), int(0.2 * SR))
    src = rs.randn(n) * (1 + 0.6 * np.sin(2 * np.pi * 140 * t))
    out = bandpass(stereo(src * env), 480, 2600, order=2)
    out = np.tanh(2.5 * out)
    return out * gain * 0.3


def scrape(dur_steps=8.0, gain=1.0, f0=380.0, f1=5200.0, seed=0, rev_=False):
    """metal dragged across metal: a resonant band sweeping over noise"""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 43)
    u = t / max(t[-1], 1e-9)
    if rev_:
        u = u[::-1]
    src = stereo(rs.randn(n))
    out = morph_lp(src, f0, f1, u, bands=7, res=3.2)
    out = np.tanh(2.0 * out)
    out = widen(out, 1.4)
    return out * (np.sin(np.pi * (t / max(t[-1], 1e-9))) ** 0.7)[:, None] * gain * 0.35


@cached
def glass(freq, dur_steps, gain=1.0, seed=0):
    """cold bell: struck, inharmonic, and gone before it gets warm"""
    n, t = steps(dur_steps)
    x = (np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.55)
         + 0.45 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t / 0.22)
         + 0.22 * np.sin(2 * np.pi * freq * 5.41 * t) * np.exp(-t / 0.09)
         + 0.12 * np.sin(2 * np.pi * freq * 8.93 * t) * np.exp(-t / 0.04))
    out = stereo(np.tanh(1.2 * x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0016))
    return out * adsr(n, a=0.001, r=0.06)[:, None] * gain * 0.6
