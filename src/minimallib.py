"""The high-tech minimal layer: 127 BPM, and a kit made of very small things.

Minimal techno of the Brejcha school is not techno with parts removed. It is a
genre with a different centre of gravity: the kick is *clean* rather than
enormous, a bass rolls in sixteenths underneath it, and everything else is
tiny, bright and placed to the millisecond - clicks, wood, rims, digital
bleeps, a shaker that never lands twice at the same level. The result is a
groove with a hole in the middle exactly the size of one plucked melody, and
that melody is the whole record.

Three things in here do not exist in `core`, and they are what the genre is:

`mkick` - a floor that stays out of the way. Two stages of gentle drive rather
than six of hard clipping, a decay of a fifth of a second, and a real click.
It occupies 40-70 Hz and 2-4 kHz and almost nothing in between, because the
bass has to live in the gap.

`line` - a whole bar of a monophonic voice rendered as ONE unbroken
oscillator. The frequency track is per-sample (so slides really slide and
every note change is smoothed rather than stepped), the phase never restarts,
and each note gets its own amplitude and filter envelope written into the bar
with a max-accumulate. `rollbass` and `acid` are the same function with
different filters: the rolling bass shuts its filter in 60 ms so three
quarters of every note is a gap, and the 303 leaves it open.

The percussion box - `bleep`, `wood`, `rimtick`, `dust`, `shaker`, `conga`.
Nothing here is loud. Six quiet things placed on six different sixteenths are
what "high-tech" means; one loud thing is a drum machine.

Usage:
    from minimallib import *
    s = Session(208, tail=4.0)
    t = s.pos(0); s.hit(t)
    s.place(t, mkick(), bus='drums')
    s.place(s.pos(0), rollbass(BASS_A), bus='bass')
    s.render('minimal_something_127.wav', drive=1.0, clip=1.1, limit=0.94)
"""
import numpy as np
import core
from core import *
from scipy.ndimage import uniform_filter1d

BAR, STEP = core.set_grid(bpm=127)
BPM = core.BPM

def set_tempo(bpm, beats=4):
    """Re-grid the module. 127 is where this genre actually runs, but the
    palette is not tied to it. A bare core.set_grid() is not enough: this
    module keeps its own BAR/STEP and every cached segment was rendered
    against the old grid, so both have to move together."""
    global BAR, STEP, BPM
    BAR, STEP = core.set_grid(bpm=bpm, beats=beats)
    BPM = core.BPM
    core._SEG_CACHE.clear()
    return BAR, STEP

# The bass is the only thing that really ducks. In this genre the pump is a
# groove element, not a rescue: the percussion box has to stay crisp and on
# the grid, or the whole "high-tech" quality goes with it.
Session.DUCKED = {'bass': 1.0, 'mid': 0.72, 'acid': 0.40, 'music': 0.45,
                  'pad': 0.55, 'air': 0.30}


# ---- the floor ----
@cached
def mkick(dur_steps=3.0, tune=46.25, top=190.0, tau=0.014, decay=0.138,
          drive=2.2, punch=1.30, knock=0.72, click=1.0, tick=1.0, gain=1.0):
    """The clean kick, in three tuned layers plus a click.

    A single sine diving onto 46 Hz is a beautiful kick on a spectrum
    analyser and nothing at all on a laptop: 94% of its energy sits below
    60 Hz, and no amount of EQ afterwards can boost a band that has almost
    nothing in it. So the bands are generated, not filtered - `punch` is its
    own oscillator at 2.55x the root (118 Hz, the chest) and `knock` another
    at 4.5x (208 Hz, the thing a phone reproduces). Both are tuned to the
    root, because at this decay length the kick is audibly pitched and an
    untuned one argues with the key.

    Deliberately short. At 127 BPM a beat is 472 ms; this hit is done in 160,
    which leaves 300 ms of every beat for the bass to roll through. A longer
    kick sounds bigger soloed and takes the genre away."""
    n, t = steps(dur_steps)
    # 1: the sub - the weight, and the only thing under 60 Hz
    f = tune + (top - tune) * np.exp(-t / tau)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.tanh(drive * np.sin(ph)) / np.tanh(drive)
    x = x * np.exp(-t / decay)
    # 2: the punch - a second oscillator, not an EQ boost
    fp = tune * 2.20 * (1 + 3.0 * np.exp(-t / 0.020))
    p = np.sin(2 * np.pi * np.cumsum(fp) / SR) * np.exp(-t / 0.048)
    p = np.tanh(1.8 * p) / np.tanh(1.8)
    # 3: the knock - what a small speaker plays instead of the fundamental
    fk = tune * 4.5 * (1 + 1.4 * np.exp(-t / 0.008))
    k = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * np.cumsum(fk) / SR))
    k = k * np.exp(-t / 0.019)
    out = stereo(x + punch * p + knock * k)
    out = np.tanh(1.3 * out) / np.tanh(1.3)
    if click:
        c = np.random.RandomState(3).randn(n) * np.exp(-t / 0.0014) * 0.85 * click
        c += np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.0025) * 0.40 * tick
        c += np.sin(2 * np.pi * 5200 * t) * np.exp(-t / 0.0011) * 0.20 * tick
        out = out + hp(stereo(c), 1800) * 0.55
    return norm(hp(out, 28) * adsr(n, a=0.0004, r=0.012)[:, None], 0.96) * gain


@cached
def ktail(dur_steps=3.0, tune=46.25, decay=0.21, tone=190, gain=1.0, harm=0.30):
    """The kick's own sub tail, on its own bus so it can be pushed without
    making the transient louder. Not a rumble: a clean sine that holds the
    fundamental through the first half of the beat and gets out."""
    n, t = steps(dur_steps)
    ph = 2 * np.pi * tune * t
    x = np.sin(ph) * np.exp(-t / decay) * np.minimum(t / 0.004, 1)
    # one octave up at a third of the level: a pure 46 Hz sine is felt and
    # never heard, and the ear needs the harmonic to know what note it is
    x = x + harm * np.sin(2 * ph) * np.exp(-t / (decay * 0.7)) * np.minimum(t / 0.004, 1)
    return lp(stereo(x), tone) * adsr(n, a=0.004, r=0.05)[:, None] * gain * 0.7


# ---- one bar of a monophonic voice, as one oscillator ----
# `line()` and `_line_envs()` live in core: rendering a whole bar of a
# monophonic voice as one unbroken oscillator is an engine technique, not a
# genre one, and the synthwave module needs it too. What stays here are the
# presets - the same renderer wearing this genre's four instruments.

def rollbass(pattern, dur_bars=1, **kw):
    """The rolling bass: a filter that shuts in 60 ms, so three quarters of
    every sixteenth is silence and the pattern reads as a pulse rather than a
    note. Cached - the same bar plays dozens of times."""
    kw = dict(dict(f_lo=115.0, f_hi=3000.0, res=2.4, decay=0.090, cut_decay=0.062,
                   drive=2.7, sub=0.32, low=68.0, detune=0.010), **kw)
    return cached_line(pattern, dur_bars, **kw)


# The supply model moved to core - it is machinery, not a taste decision, and
# the dark-acid 303 in industriallib needs the same circuit.
def _accent_sag(pattern, n, depth, hold=0.006, dur=0.055):
    return core.accent_sag(pattern, n, depth, hold, dur, step=STEP)


def acidline(pattern, dur_bars=1, cutoff=0.30, res=5.2, envmod=0.85,
             decay=0.17, cut_decay=0.085, drive=5.0, wave='saw', acc_amt=0.55,
             sag=0.28, f_lo=150.0, f_hi=5800.0, slide_tau=0.055, gain=1.0,
             low=165.0, bands=11, tame=9000.0, even=0.16, glide_ms=2.0):
    """A TB-303, built the way the machine is built rather than as a preset
    of a general line renderer.

    Three things separate this from a resonant lowpass with an envelope on it,
    and all three are in `theory/10-instruments/02-analog-monosynths.md`:

    **18 dB per octave, not 24.** The 303's filter is a three-pole diode
    ladder. The extra pole every other synth has is exactly what kills the
    imitation: at 24 dB the resonant peak sits on top of silence, at 18 there
    is still an audible bed of harmonics above the cutoff for it to sit on,
    and that bed is what the ear hears as "squelch" rather than "bleep".

    **The overdrive is after the filter and is most of the sound.** Not a
    little tanh scaled down by the resonance - a real stage, driven hard,
    with an asymmetric term so it makes even harmonics as well as odd. Take
    it out and what is left is a synth playing a pattern.

    **`cutoff` and `envmod` are two knobs, not one.** `cutoff` is where the
    filter rests; `envmod` is how far above that each note's envelope throws
    it. Turning them against each other over sixteen bars, while the pattern
    stays fixed, IS the performance - the pattern is not the sound.

    pattern: [(step, note, dur_steps, accent, slide[, velocity]), ...]
    """
    n = int(round(dur_bars * BAR + 1.5 * STEP))
    fs, amp, cut = core._line_envs(pattern, n, decay, cut_decay, acc_amt, 0.0,
                              glide_ms, slide_tau)
    ph = 2 * np.pi * np.cumsum(fs) / SR
    top = float(fs.max())
    if wave == 'square':
        x = (2 / np.pi) * sum(np.sin(k * ph) / k for k in range(1, 46, 2)) * 2
    else:
        x = saw_ph(ph, top, kmax=72)
    env = np.clip(cutoff + envmod * cut, 0.0, 1.0)
    st = stereo(x * amp)
    # order=3: the pole the imitations add, and the one this filter never had
    out = morph_lp(st, f_lo, f_hi, env, bands=bands, res=res, order=3)
    out = out / (1 + res * 0.30)
    sagg = _accent_sag(pattern, n, sag)
    out = out * sagg[:, None]
    # the stage that makes it acid
    out = np.tanh(drive * out) / np.tanh(drive)
    if even:
        y = out * out * np.sign(out)
        out = out + even * (y - y.mean(axis=0, keepdims=True))
    out = lp(out, tame, order=2)                    # tame the fizz, keep the bite
    out = hp(out, low, order=4)                     # the sub belongs to the kick
    return fade_edges(out.astype(np.float32), 2.0) * gain * 0.55


@cached
def _acid_cached(key, dur_bars, **kw):
    return acidline(list(key), dur_bars, **kw)


def acid(pattern, dur_bars=1, **kw):
    """cached acidline - the same bar plays dozens of times, and the knob
    positions are part of the cache key, so a swept line is a sequence of
    distinct cached bars rather than one bar repeated"""
    return _acid_cached(tuple(tuple(p) for p in pattern), dur_bars, **kw)


def holdbass(pattern, dur_bars=1, **kw):
    """A sub that holds instead of rolling. `rollbass` decays into a gap on
    every sixteenth; this one sustains through the bar and is put back down
    by the sidechain four times a beat - so the pump is not an effect on the
    bass, the pump IS the bass part. The other half of the genre's low end,
    and the reason two minimal records with the same kick can feel nothing
    alike."""
    kw = dict(dict(f_lo=90.0, f_hi=560.0, res=0.9, decay=1.1, cut_decay=0.55,
                   hold=0.66, drive=1.9, sub=0.55, sub_lp=115.0, low=0.0,
                   detune=0.0, wave='tri', tail_steps=2.0), **kw)
    return cached_line(pattern, dur_bars, **kw)


def midbass(pattern, dur_bars=1, **kw):
    """The other half of the bass. A sub is felt and not heard; on a phone,
    in a car and through one earbud the bassline that reaches the listener is
    this one - the same notes an octave up, through a filter that leaves
    150-1200 Hz alone, with no sub content at all so it cannot muddy the
    layer underneath. Two layers, one instrument: play them from the same
    pattern and let the octave do the separating."""
    kw = dict(dict(f_lo=150.0, f_hi=1900.0, res=2.6, decay=0.13, cut_decay=0.085,
                   drive=2.4, sub=0.0, low=78.0, detune=0.013, hold=0.10,
                   spread=0.7, wave='saw'), **kw)
    pat = tuple((ev[0], ev[1] + 12) + tuple(ev[2:]) for ev in pattern)
    return cached_line(pat, dur_bars, **kw)


def stabline(pattern, dur_bars=1, **kw):
    """A mid-register counter-line: brighter, longer, still one oscillator."""
    kw = dict(dict(f_lo=380.0, f_hi=5600.0, res=2.0, decay=0.16, cut_decay=0.085,
                   drive=1.7, sub=0.0, low=260.0, detune=0.014, spread=0.9), **kw)
    return cached_line(pattern, dur_bars, **kw)


# ---- the percussion box ----
@cached
def mhat(dur_steps=0.7, open_=False, gain=1.0, tone=1.0, seed=0):
    """Closed hat: metallic squares plus noise, gone in 25 ms. Short enough
    that sixteen of them a bar read as texture, not as a hiss."""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 3.2))
    rs = np.random.RandomState(seed + 11)
    sq = sum(square(f * tone, t) for f in (318.0, 448.0, 561.0, 727.0, 855.0, 1103.0)) / 6
    x = sq * 0.55 + rs.randn(n) * 0.9
    dec = 0.20 if open_ else 0.021
    out = hp(stereo(np.tanh(1.5 * x)), 7600 if open_ else 8800)
    out = out + bandpass(stereo(x), 3800, 6400) * 0.30
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0004))
    return out * (np.exp(-t / dec) * adsr(n, a=0.0003, r=0.008))[:, None] * gain * 0.42


@cached
def shaker(dur_steps=0.7, gain=1.0, seed=0, bright=1.0):
    """A shaker is a hat with a slower attack: the beads have to travel."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 23)
    x = bandpass(stereo(rs.randn(n)), 4200 * bright, 12000 * bright)
    env = np.minimum(t / 0.006, 1.0) * np.exp(-t / 0.030)
    out = x * env[:, None]
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0006))
    return out * gain * 0.50


@cached
def rimtick(dur_steps=0.6, gain=1.0, f=1620.0, seed=0):
    """The rim. Two milliseconds of pitched wood - the single most useful
    sound in this genre, because it marks a sixteenth without occupying it."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 31)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.0055)
    x += np.sin(2 * np.pi * f * 2.31 * t) * np.exp(-t / 0.0030) * 0.5
    x += rs.randn(n) * np.exp(-t / 0.0022) * 0.55
    out = bandpass(stereo(np.tanh(2.2 * x)), 900, 8500)
    return out * adsr(n, a=0.0003, r=0.006)[:, None] * gain * 0.55


@cached
def wood(note=79, dur_steps=0.8, gain=1.0, seed=0):
    """A tuned knock. Pitched percussion is how a minimal track gets a melody
    without adding an instrument - put these on the notes of the key."""
    n, t = steps(dur_steps)
    f = midi(note)
    rs = np.random.RandomState(seed + 41)
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.028)
         + 0.45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.010)
         + 0.25 * np.sin(2 * np.pi * f * 4.13 * t) * np.exp(-t / 0.005))
    x += rs.randn(n) * np.exp(-t / 0.0016) * 0.35
    out = bandpass(stereo(np.tanh(1.8 * x)), 400, 9000)
    return out * adsr(n, a=0.0004, r=0.010)[:, None] * gain * 0.50


@cached
def mallet(note=78, dur_steps=3.0, gain=1.0, hard=0.30, tube=0.80, decay=0.60,
           seed=0):
    """A tuned bar over a resonator tube, struck with a soft mallet.

    `wood` is a dry knock and stops there. This is the instrument: a marimba
    bar is undercut so its first overtone lands on 4x the fundamental - two
    octaves, not a musical third - and the second near 9.2x, which is why a
    marimba sounds hollow and pure where a random partial stack sounds like a
    bell. Under each bar hangs a quarter-wave pipe tuned to the fundamental,
    and that is the part of the sound that sings after the wood has stopped;
    it is modelled here as a narrow resonance with its own longer envelope.

    `hard` is the mallet. A wound-yarn head is heavy and slow, so it barely
    excites the upper partials and the note arrives round; wind the head
    tighter and the 4x and 9.2x come up and the attack gets a click. Keep it
    low and the instrument reads as tubes being struck rather than as a
    xylophone being hit."""
    n, t = steps(dur_steps)
    f = midi(note)
    rs = np.random.RandomState(seed + 61)
    bar_ = (np.sin(2 * np.pi * f * t) * np.exp(-t / decay)
            + (0.34 + 0.85 * hard) * np.sin(2 * np.pi * f * 4.0 * t)
              * np.exp(-t / (decay * 0.20))
            + (0.13 + 0.42 * hard) * np.sin(2 * np.pi * f * 9.2 * t)
              * np.exp(-t / (decay * 0.07)))
    strike = rs.randn(n) * np.exp(-t / (0.0016 + 0.005 * (1 - hard))) * (0.55 + 0.9 * hard)
    x = stereo(bar_) + bandpass(stereo(strike), 700, 3000 + 6000 * hard)
    if tube:
        # the pipe: a narrow resonance on the fundamental that outlives the bar
        pipe = bandpass(stereo(np.sin(2 * np.pi * f * t)), f * 0.88, f * 1.14, order=2)
        x = x + tube * pipe * (np.exp(-t / (decay * 1.7)) * np.minimum(t / 0.004, 1))[:, None]
    x = hp(x, f * 0.55, order=2)
    env = adsr(n, a=0.0028 + 0.004 * (1 - hard), r=0.04)
    x[:, 1] = np.roll(x[:, 1], int(SR * 0.0009))
    return x * env[:, None] * gain * 0.42


@cached
def conga(note=57, dur_steps=1.6, gain=1.0, slap=0.0, seed=0):
    """A membrane: a sine dropping a fourth in 25 ms with noise on the strike.
    `slap` swaps the open tone for the edge of the hand."""
    n, t = steps(dur_steps)
    f0 = midi(note)
    f = f0 * (1 + 0.32 * np.exp(-t / 0.025))
    rs = np.random.RandomState(seed + 53)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.055 if slap else 0.13))
    x += 0.35 * np.sin(2 * np.pi * np.cumsum(f * 1.58) / SR) * np.exp(-t / 0.035)
    x += rs.randn(n) * np.exp(-t / (0.006 if slap else 0.003)) * (0.75 if slap else 0.35)
    out = bandpass(stereo(np.tanh(1.7 * x)), 120, 7000)
    if slap:
        out = out + bandpass(stereo(rs.randn(n) * np.exp(-t / 0.010)), 1800, 8000) * 0.4
    return out * adsr(n, a=0.0006, r=0.012)[:, None] * gain * 0.55


@cached
def tom(note=43, dur_steps=2.0, gain=1.0, decay=0.10, seed=0, skin=0.5):
    """A low tuned drum for the 150-300 Hz band, which in a mix this clean is
    otherwise empty: the kick stops at 60 and the percussion box starts at
    1500. Two sines a fifth apart with a short pitch dive and a skin noise on
    the strike."""
    n, t = steps(dur_steps)
    f0 = midi(note)
    rs = np.random.RandomState(seed + 59)
    f = f0 * (1 + 0.55 * np.exp(-t / 0.018))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / decay)
    x += 0.40 * np.sin(1.5 * ph) * np.exp(-t / (decay * 0.55))
    x += 0.18 * np.sin(2.7 * ph) * np.exp(-t / (decay * 0.25))
    x += skin * rs.randn(n) * np.exp(-t / 0.0035)
    out = bandpass(stereo(np.tanh(1.5 * x)), 70, 4500)
    return out * adsr(n, a=0.0008, r=0.02)[:, None] * gain * 0.6


@cached
def mclap(dur_steps=3.0, gain=1.0, spread=1.0, room=0.55, seed=0):
    """Four hands, 9 ms apart, into a small bright room. Wide on purpose -
    it is the one element allowed to sit outside the centre."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 67)
    burst = np.zeros(n)
    for d, a in ((0.0, 1.0), (0.0085, 0.85), (0.0175, 0.7), (0.0275, 0.55)):
        k = int(d * SR)
        burst[k:] += rs.randn(n - k) * np.exp(-np.arange(n - k) / SR / 0.0085) * a
    body = rs.randn(n) * np.exp(-t / 0.10) * 0.45
    st = (bandpass(stereo(burst), 1100, 6200)
          + bandpass(stereo(body), 700, 3600) * 0.6
          + bandpass(stereo(body), 210, 480) * 0.75)      # the body, not just the snap
    st[:, 0] = np.roll(st[:, 0], int(SR * 0.0007 * spread))
    st[:, 1] = np.roll(st[:, 1], -int(SR * 0.0005 * spread))
    if room:
        st = st + room * reverb(st, decay=0.30, wet=1.0, tone=5200, predelay=0.006)[:n]
    return st * adsr(n, a=0.0004, r=0.02)[:, None] * gain * 0.42


@cached
def mride(dur_steps=2.0, gain=1.0, seed=0):
    """A ping with a wash under it - the continuous energy a hat cannot give
    without becoming fatiguing."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 71)
    ping = sum(np.sin(2 * np.pi * f * t) for f in (2470.0, 3310.0, 4520.0)) / 3
    ping *= np.exp(-t / 0.08)
    wash = hp(stereo(rs.randn(n)), 6500) * np.exp(-t / 0.22)[:, None] * 0.35
    out = bandpass(stereo(ping), 2000, 9000) + wash
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0008))
    return out * adsr(n, a=0.0006, r=0.03)[:, None] * gain * 0.32


@cached
def bleep(note=93, dur_steps=0.7, gain=1.0, ratio=2.41, index=2.6, decay=0.035,
          bend=0.0):
    """The digital blip. Two-operator FM at an inharmonic ratio with the index
    on an envelope, so the spectrum collapses as it decays - a struck object
    that never existed. This is the sound the genre is named after; use it
    small, high and often, never twice at the same pitch."""
    n, t = steps(dur_steps)
    f = midi(note) * (1 + bend * np.exp(-t / 0.012))
    ph = 2 * np.pi * np.cumsum(f) / SR
    ie = index * np.exp(-t / (decay * 0.5))
    x = np.sin(ph + ie * np.sin(ratio * ph))
    env = np.exp(-t / decay) * np.minimum(t / 0.0008, 1.0)
    out = stereo(x * env)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0005))
    return hp(out, 600) * adsr(n, a=0.0003, r=0.006)[:, None] * gain * 0.5


@cached
def dust(dur_steps=16.0, gain=1.0, density=22, seed=0, lo=2000, hi=11000):
    """Micro-clicks scattered across a bar. Individually inaudible; together
    they are the difference between a loop and a room with something in it."""
    n, _ = steps(dur_steps)
    rs = np.random.RandomState(seed + 83)
    x = np.zeros((n, 2), dtype=np.float32)
    for _ in range(density):
        k = rs.randint(0, max(n - 400, 1))
        L = rs.randint(24, 260)
        tt = np.arange(L) / SR
        g = rs.uniform(0.15, 0.7)
        p = rs.uniform(-0.85, 0.85)
        c = rs.randn(L) * np.exp(-tt / rs.uniform(0.0007, 0.004)) * g
        seg = panned(stereo(c), p)
        x[k:k + L] += seg
    return bandpass(x, lo, hi) * gain * 0.45


# ---- the melody ----
@cached
def plink(freq, dur_steps=2.0, gain=1.0, detune=0.006, f_lo=520.0, f_hi=7200.0,
          res=2.6, decay=0.085, ring=0.30, drive=1.5, glass=0.35, seed=0):
    """The hook voice. Detuned saws through a filter that falls from 7 kHz to
    500 Hz in under a tenth of a second, with a glass partial ringing on
    after it - half pluck, half bell. Every note is a different sound because
    the filter is moving while it sounds; sixteen static notes would be the
    thing people call raw."""
    n, t = steps(dur_steps)
    x = saw(freq * (1 - detune), t) + saw(freq * (1 + detune), t) \
        + 0.6 * square(freq * (1 + detune * 2.6), t)
    cut = np.exp(-t / decay)
    out = morph_lp(stereo(x / 2.6), f_lo, f_hi, 0.04 + 0.96 * cut, bands=8, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    if glass:
        g = (np.sin(2 * np.pi * freq * 2.0 * t) * np.exp(-t / 0.28)
             + 0.5 * np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t / 0.14))
        out = out + glass * stereo(g) * 0.35
    env = (ring + (1 - ring) * np.exp(-t / 0.05)) * np.exp(-t / 0.42)
    env *= adsr(n, a=0.0018, r=0.02)
    # Dead centre. A 1 ms Haas nudge here reads as width on headphones and
    # combs a hole in the hook the moment anything sums to mono; width comes
    # from the reverb send instead, which is decorrelated rather than delayed.
    return out * env[:, None] * gain * 0.8


@cached
def chime(freq, dur_steps=4.0, gain=1.0, ratio=1.42, index=1.9, decay=0.9):
    """The counter-melody: an FM bell with an inharmonic partner, long ring.
    Sits an octave above the hook and answers it."""
    n, t = steps(dur_steps)
    ph = 2 * np.pi * freq * t
    ie = index * np.exp(-t / 0.13)
    x = np.sin(ph + ie * np.sin(ratio * ph)) * np.exp(-t / decay)
    x += 0.35 * np.sin(2 * ph) * np.exp(-t / (decay * 0.35))
    out = stereo(x)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0016))
    return hp(out, 400) * adsr(n, a=0.0015, r=0.06)[:, None] * gain * 0.45


def glasspad(notes, dur_steps=32, gain=1.0, cutoff=2600, wide=1.8, seed=None,
             attack=0.9, res=0.0):
    """The breakdown. Five detuned saws per note with a slow filter breathing
    across the whole phrase - this is the only wide, long, warm thing in the
    track, which is why the breakdown feels like a different room."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed) if seed is not None else np.random
    x = np.zeros(n)
    for f in notes:
        vib = 1 + 0.0035 * np.sin(2 * np.pi * rs.uniform(0.15, 0.4) * t + rs.rand() * 6)
        for d in (0.9935, 0.9975, 1.0, 1.0026, 1.0068):
            x += 2 * ((np.cumsum(f * d * vib) / SR + rs.rand()) % 1.0) - 1
    x /= 5 * len(notes)
    breath = 0.35 + 0.65 * (0.5 - 0.5 * np.cos(2 * np.pi * t / max(t[-1], 1e-6)))
    out = morph_lp(stereo(x), cutoff * 0.28, cutoff, breath, bands=7, res=res)
    out = hp(out, 170)
    if wide:
        out = widen(out, wide)
    a = min(int(attack * SR), n // 2)
    r = min(int(0.7 * SR), n // 2)
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a) ** 1.6
    env[-r:] *= np.linspace(1, 0, r) ** 0.8
    return out * env[:, None] * gain * 0.7


def whisper(dur_steps=8, gain=1.0, v0='oo', v1='ah', note=60, seed=0, breath=1.0):
    """A voice with the pitch taken out: noise through a moving vowel pair,
    plus a thin pitched core so it reads as a person and not as a filter."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 97)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    core_ = stereo(saw(midi(note), t) * 0.25) * (1 - breath * 0.6)
    src = nz * breath + core_
    env = np.linspace(0, 1, n) ** 0.8
    out = morph_formant(src, v0, v1, env=env, wet=1.0, gain=2.2)
    swell = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.3
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0021))
    return bandpass(out, 260, 4200) * swell[:, None] * gain * 0.5


# ---- fx ----
def sweepnoise(dur_steps=16, gain=1.0, f0=300.0, f1=9000.0, q=0.45, curve=1.8,
               seed=0, rev_=False, res=1.0):
    """The long band-passed noise sweep this genre lives on: a resonant hole
    travelling up the spectrum for four bars. Not a riser - it is quiet, it
    is continuous, and you only notice it when it stops."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 101)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    u = (np.linspace(0, 1, n) ** curve)
    if rev_:
        u = u[::-1]
    fs = np.geomspace(f0, f1, 11)
    out = np.zeros((n, 2), dtype=np.float32)
    idx = u * (len(fs) - 1)
    for i, f in enumerate(fs):
        w = np.clip(1 - np.abs(idx - i), 0, 1)
        if w.max() < 1e-4:
            continue
        out += bandpass(nz, f * (1 - q), f * (1 + q)) * res * w[:, None]
    swell = np.sin(np.pi * np.linspace(0, 1, n)) ** 0.7
    return out * swell[:, None] * gain * 0.35


@cached
def revblip(note=88, dur_steps=4, gain=1.0):
    """A blip played backwards: the cheapest lead-in there is, and the one
    that does not announce itself the way a riser does."""
    seg = bleep.uncached(note, dur_steps, gain=1.0, ratio=1.73, index=3.4,
                         decay=dur_steps * STEP / SR * 0.42)
    return np.ascontiguousarray(seg[::-1]) * gain


@cached
def mcrash(dur_steps=20, gain=1.0, tone=1.0, decay=0.85, seed=0):
    """A minimal-techno crash: bright filtered noise with a handful of
    inharmonic partials on top, high-passed hard so it marks a section
    without putting anything in the kick's way. Not an 808 cymbal - those six
    detuned squares are a hip-hop timbre and read as retro the moment the
    rest of the mix is this clean."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 107)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    body = hp(nz, 4200 * tone) * np.exp(-t / decay)[:, None]
    shim = sum(np.sin(2 * np.pi * f * tone * t) for f in
               (3170.0, 4410.0, 5230.0, 6890.0, 8110.0)) / 5
    shim = hp(stereo(shim), 3000) * np.exp(-t / (decay * 0.55))[:, None]
    out = body + 0.35 * shim
    out = out * (np.minimum(t / 0.0015, 1.0))[:, None]
    return widen(out, 1.4) * adsr(n, a=0.0006, r=0.20)[:, None] * gain * 0.30


@cached
def mimpact(dur_steps=12, tune=46.25, gain=1.0, decay=0.55, seed=0):
    """The mark on the downbeat of a new section. Tuned to the root and
    high-passed at 45 Hz: a big untuned boom down there would simply be a
    second kick arriving at the same instant as the first, and the two would
    sum into a level jump rather than an event."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 113)
    f = tune * 2 * (1 + 1.6 * np.exp(-t / 0.10))
    boom = np.tanh(1.7 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / decay)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    air = (hp(nz, 2600) * np.exp(-t / 0.045)[:, None]
           + bandpass(nz, 300, 1600) * np.exp(-t / 0.20)[:, None] * 0.5)
    out = stereo(boom) + 0.55 * air
    return hp(out, 45) * adsr(n, a=0.0008, r=0.15)[:, None] * gain * 0.55


def mriser(dur_steps=32, gain=1.0, f0=400.0, f1=11000.0, rate_steps=1.0,
           res=1.0, seed=0, tone=0.35):
    """A riser that counts. The resonant band climbs in sixteenth-note steps
    instead of gliding, so the build reads as a machine counting up to
    something rather than as a whoosh - which is the difference between this
    genre and festival EDM. A quiet rising sine underneath gives the ear a
    pitch to follow."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 127)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    nsteps = max(int(dur_steps / rate_steps), 2)
    idx = np.minimum((np.arange(n) / (n / nsteps)).astype(int), nsteps - 1)
    fs = np.geomspace(f0, f1, nsteps)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(fs):
        w = (idx == i)
        if not w.any():
            continue
        out[w] = bandpass(nz, f * 0.55, f * 1.55)[w] * res
    if tone:
        fr = np.geomspace(f0 * 0.5, f1 * 0.25, n)
        out = out + tone * stereo(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.5
    swell = (np.linspace(0, 1, n) ** 1.7)
    out = out * swell[:, None]
    return hp(out, 200) * gain * 0.40


@cached
def mdown(dur_steps=6, gain=1.0, f0=3200.0, f1=180.0, seed=0):
    """The other half of a transition: a short dry fall that spends the
    energy a riser just built. Stops at 180 Hz - anything lower is the
    kick's."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 131)
    u = t / max(t[-1], 1e-9)
    f = f0 * (f1 / f0) ** u
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.7
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)
    band = np.zeros((n, 2), dtype=np.float32)
    fs = np.geomspace(f0, f1, 9)
    ii = np.minimum((u * 9).astype(int), 8)
    for i, ff in enumerate(fs):
        w = (ii == i)
        if w.any():
            band[w] = bandpass(nz, ff * 0.6, ff * 1.6)[w]
    out = stereo(x) + 0.8 * band
    return hp(out, 150) * np.exp(-t / (0.55 * max(t[-1], 0.1)))[:, None] * gain * 0.4


def tapeflutter(seg, depth_ms=0.9, rate=5.5):
    """A touch of instability on something too perfect."""
    return wow(seg, depth_ms=depth_ms, rate=rate)


def gate(seg, rate_steps=1.0, duty=0.5, depth=1.0, soft=0.004):
    """Chop a sustained sound into the grid. A pad through a 16th gate is a
    rhythm part, and it costs nothing."""
    n = len(seg)
    p = max(int(rate_steps * STEP), 8)
    on = max(int(p * duty), 2)
    k = max(int(soft * SR), 4)
    env = np.zeros(n)
    for a in range(0, n, p):
        b = min(a + on, n)
        env[a:b] = 1.0
    env = uniform_filter1d(env, k)
    env = 1 - depth * (1 - env)
    return (seg * env[:, None]).astype(np.float32)


def stutter(seg, slice_steps=1.0, repeats=4, decay=1.0, pitch=1.0):
    """Take the head of a segment and fire it repeatedly, optionally rising."""
    L = max(int(slice_steps * STEP), 16)
    head = fade_edges(seg[:L], 1.5)
    out = np.zeros((L * repeats, 2), dtype=np.float32)
    for i in range(repeats):
        h = head if pitch == 1.0 else pitched(head, pitch ** i)
        m = min(len(h), L)
        out[i * L:i * L + m] += h[:m] * (decay ** i)
    return out

# ---- the dub end of the genre: a chord, and the room it is thrown into ----
@cached
def dubstab(notes, dur_steps=1.4, gain=1.0, detune=0.008, f_lo=380.0,
            f_hi=4200.0, res=2.4, decay=0.055, drive=2.0, low=230.0,
            spread=1.0, seed=0):
    """A chord stab built to be thrown away.

    Everything about it is decided by what happens next: it is short (55 ms
    of decay), it is high-passed at 230 Hz and rolled off on top, and it has
    almost no sustain - because the part the listener hears is not this, it
    is six echoes of it. A stab with a long tail turns a delay into mud
    inside two repeats, and a stab with real low end turns it into mud
    inside one.

    `notes` are frequencies, not MIDI - hand it the voicing you want."""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        x += saw(f * (1 - detune), t) + saw(f * (1 + detune), t)
        x += 0.4 * square(f * (1 + detune * 2.2), t)
    x /= 2.4 * len(notes)
    cut = np.exp(-t / (decay * 1.4))
    out = morph_lp(stereo(x), f_lo, f_hi, 0.10 + 0.90 * cut, bands=7, res=res)
    out = np.tanh(drive * out / (1 + res * 0.35))
    out = hp(out, low, order=4)
    if spread:
        out[:, 1] = np.roll(out[:, 1], int(SR * 0.0013 * spread))
    env = np.exp(-t / decay) * adsr(n, a=0.0016, r=0.014)
    return out * env[:, None] * gain * 0.55


def dubecho(seg, steps_=3.0, times=7, fb=0.62, damp0=5200.0, darken=0.62,
            hp_hz=280.0, drive=1.9, drift=1.1, ping=True, spread=0.62,
            seed=0):
    """A tape echo, not a digital one.

    Four things separate the two, and only the first is in a plain delay:
    each repeat is darker than the last (geometrically - `darken` is the
    factor per pass, not a subtraction); each repeat is high-passed, or the
    low end accumulates until the fifth echo is a rumble; each repeat goes
    through the saturation the tape and its preamp add, which is what makes
    a long feedback settle into a warm blur instead of a ringing copy; and
    each repeat wanders in pitch, because the transport never held speed.

    Set `times` high and `fb` near 0.7 and the tail stops being an effect
    and becomes the part - which is the whole trick dub taught this genre."""
    d = int(steps_ * STEP)
    n = len(seg) + d * times + 1
    out = np.zeros((n, 2), dtype=np.float32)
    out[:len(seg)] += seg
    rs = np.random.RandomState(seed + 149)
    e = seg
    for i in range(1, times + 1):
        e = lp(e, max(damp0 * darken ** (i - 1), 620.0), order=2)
        e = hp(e, hp_hz, order=2)
        e = np.tanh(drive * e) / np.tanh(drive)
        if drift:
            e = wow(e, depth_ms=drift * rs.uniform(0.6, 1.4),
                    rate=rs.uniform(0.35, 1.1))
        g = fb ** i
        y = panned(e, (spread if i % 2 else -spread)) if ping else e
        a = i * d
        out[a:a + len(y)] += (y * g).astype(np.float32)
    return out


# ---- hard sync: the one timbre a filter cannot make ----
@cached
def syncarp(freq, dur_steps=1.0, gain=1.0, r0=3.4, r1=1.15, decay=0.075,
            f_lo=520.0, f_hi=7000.0, res=1.6, drive=2.2, sub=0.22, seed=0):
    """An arp note whose *waveform* tears rather than whose filter closes.

    A second saw runs at `ratio` times the pitch and has its phase reset by
    the first, so the note you hear stays put while the harmonic that is
    being cut in half slides down through the spectrum. Sweeping a filter
    makes a note get darker; sweeping a sync ratio makes it change what it
    is made of, and there is no filter setting that sounds like it. This is
    the arp for a track that already has a filter doing the other job."""
    n, t = steps(dur_steps)
    ratio = r1 + (r0 - r1) * np.exp(-t / decay)
    x = sync_saw(t, freq, ratio)
    x = x + 0.45 * sync_saw(t, freq * 1.004, ratio * 0.997)
    if sub:
        x = x + sub * np.sin(2 * np.pi * freq * t)
    out = morph_lp(stereo(x / 1.7), f_lo, f_hi, np.exp(-t / (decay * 2.2)),
                   bands=6, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0007))
    env = np.exp(-t / (decay * 2.6)) * adsr(n, a=0.0012, r=0.016)
    return hp(out, 300) * env[:, None] * gain * 0.5


@cached
def clang(note=72, dur_steps=1.2, gain=1.0, decay=0.055, bright=1.0, seed=0):
    """Struck metal. Inharmonic partials with individually short decays and
    a noise transient on the strike - `wood` is a harmonic knock and `bleep`
    is FM; this is the third thing, and it is what a techno record uses when
    it wants a percussion hit that is also a pitch."""
    n, t = steps(dur_steps)
    f = midi(note)
    rs = np.random.RandomState(seed + 151)
    x = np.zeros(n)
    for r, a, dk in ((1.0, 1.0, 1.0), (2.71, 0.62, 0.55), (4.19, 0.42, 0.34),
                     (6.83, 0.28, 0.20), (9.37, 0.16, 0.12)):
        x += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (decay * dk))
    x += rs.randn(n) * np.exp(-t / 0.0018) * 0.5
    out = bandpass(stereo(np.tanh(1.6 * x)), 500 * bright, 13000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0006))
    return out * adsr(n, a=0.0004, r=0.010)[:, None] * gain * 0.45


def hum(note=33, dur_steps=32, gain=1.0, seed=0, cutoff=520.0, motor=0.30):
    """The room the machines are in. A saw and a band of noise held under a
    slow resonant sweep, with a low motor beating under it - `glasspad` is a
    chord and this is not: it has one pitch and its job is to make a
    breakdown feel like somewhere rather than like an absence."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed + 157)
    f = midi(note)
    x = np.zeros(n)
    for m, a, d in ((1.0, 1.0, 1.0), (2.0, 0.45, 0.997), (3.0, 0.22, 1.004),
                    (4.0, 0.12, 0.994)):
        drift = 1 + 0.0022 * np.sin(2 * np.pi * rs.uniform(0.03, 0.09) * t + rs.rand() * 6)
        x += a * (2 * ((np.cumsum(f * m * d * drift) / SR + rs.rand()) % 1.0) - 1)
    x /= 1.8
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32) * 0.30
    sweep = 0.30 + 0.70 * (0.5 - 0.5 * np.cos(2 * np.pi * t / max(t[-1], 1e-6) * 1.5))
    out = morph_lp(stereo(x) + nz, cutoff * 0.30, cutoff * 3.2, sweep, bands=7, res=1.1)
    if motor:
        out = out * (1 - motor + motor * core._lfo01(t, BPM / 60.0 / 2))[:, None]
    out = hp(out, 90, order=4)
    a_ = min(int(1.6 * SR), n // 2); r_ = min(int(2.2 * SR), n // 2)
    env = np.ones(n); env[:a_] = np.linspace(0, 1, a_) ** 1.4
    env[-r_:] *= np.linspace(1, 0, r_) ** 0.9
    return widen(out, 0.9) * env[:, None] * gain * 0.5

