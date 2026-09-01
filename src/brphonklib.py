"""The Brazilian phonk layer: the tuned cowbell and the mandelao beat.

140 BPM, and the whole module exists to answer one question the older phonk
kits do not: what does a cowbell sound like when it has to play a melody in
16ths instead of clanging once a bar.

The style borrows its grid from funk mandelao and its metal from phonk. Its
pulse is even - a kick on every beat - and the 3+3+2 that the Brazilian beat
normally puts on the kick lives on a mid tom instead, so the syncopation is
audible without the bottom ever going lopsided.

    agogo   the cowbell, as sixteen resonators struck with a burst of noise
            rather than as two squares under an envelope. Each mode decays at
            its own rate so the spectrum falls apart as the note fades, which
            is what separates struck metal from a gated pulse channel. `hit`
            is one velocity control moving brightness, drive and mallet
            hardness together, because a bar struck harder is not a louder
            bar, it is a different one.
    bumbo   the kick: an 808 dive with a low knock and a hard gate, so at 140
            with four to the floor the low end is silent before the next one.
    grave   the bass: one oscillator split at 130 Hz, the upper half folded
            and driven into the 150-500 Hz grunt the style lives on, gated
            with the kick so the sub has gaps.
    timbau  the mid tom that carries the tresillo.
    caixa   the dry tic between the beats: a body with no ring.
    chique  a shaker - beads accelerating, so its envelope rises before it
            falls, which is what separates it from a hi-hat.
    grito   a shout: a jittering glottal pulse train through moving formants.
            Every other voice in the engine sings.

Usage:
    from brphonklib import *
    s = Session(112, tail=2.0)
    s.hit(s.pos(0, 0))
    s.place(s.pos(0, 0), bumbo(), bus='drums')
    s.place(s.pos(0, 0), agogo(67, 2, hit=1.0), bus='bell')
    s.place(s.pos(0, 0), grave(31, 3), bus='bass')
"""
import numpy as np
from scipy.signal import lfilter
import core
from core import *

BAR, STEP = core.set_grid(bpm=140)
BPM = core.BPM


def _sqph(ph, fmax):
    """band-limited square from a phase array: a saw against itself half a
    cycle late, which cancels the even harmonics"""
    return saw_ph(ph, fmax) - saw_ph(ph + np.pi, fmax)


# ---- the lead: the cowbell, struck ----
# A folded steel plate: a low pair that carries the perceived pitch, then the
# dense inharmonic cluster that carries the metal. (ratio, amplitude, decay in
# seconds at hit=1). The 1.4815 is the ratio the 808 used for its two
# oscillators, and it is here for the same reason - it is what a cowbell is.
# The pair members are split a few thousandths apart because a real bell is
# not symmetric, and the two halves of a split mode beat against each other.
COWBELL_MODES = (
    (1.0000, 1.00, 0.175), (1.0075, 0.55, 0.155),
    (1.4815, 0.95, 0.145), (1.4930, 0.52, 0.125),
    (2.0250, 0.80, 0.110), (2.4300, 0.72, 0.098),
    (2.9600, 0.80, 0.088), (3.4500, 0.85, 0.078),
    (4.1100, 0.90, 0.068), (4.9700, 0.92, 0.058),
    (5.8300, 0.90, 0.048), (6.9000, 0.84, 0.039),
    (8.2500, 0.74, 0.031), (9.8000, 0.62, 0.024),
    (11.600, 0.50, 0.019), (13.900, 0.38, 0.014),
)


@cached
def agogo(note, dur=2.0, gain=1.0, hit=1.0, decay=1.0, ring=0.0, clang=0.9,
          folded=0.30, mute=0.0, seed=7):
    """A cowbell that is struck rather than switched on.

    Two oscillators at f and 1.4815f through a bandpass is how the 808 built
    a cowbell and how every phonk kit since has copied it, and it has one
    problem: a square wave is odd harmonics of f at 1/k, and a single
    envelope over the pair decays all of them together. A spectrum that keeps
    its shape while it fades is the sound of a gated pulse channel, not of
    struck metal - the ear has heard it in games since 1985 and names it
    instantly.

    So this is not an oscillator with an envelope. It is a bank of sixteen
    two-pole resonators, tuned to the inharmonic mode ratios of a folded
    plate, struck with a two-millisecond burst of noise:

      - every mode decays at its own rate, fastest at the top, so the
        spectral centroid falls by half within the note. That fall is the
        cue, and it is the one thing a square pair cannot fake.
      - the modes are inharmonic, so nothing lines up into a harmonic
        series the ear can read as a waveform.
      - the two lowest modes are split into detuned pairs, so the tone beats
        instead of sitting still.
      - the attack is noise through the same resonators, which is what a
        mallet actually does - not a noise layer added on top.

    `hit` is one control for how hard it was struck, and it moves the timbre
    far more than the level: mode k is scaled by `hit ** 0.22k`, so a soft
    strike is the low pair alone (a dull thud) and a hard one lights the
    whole cluster (a bright clang). The mallet gets harder with it too.

    The drive is in two paths, because a single tanh over the sum only ever
    distorts the low pair that dominates it. The body is driven gently; the
    metal band above 1.8f is bandpassed out, driven hard, folded, and mixed
    back - distortion with an EQ between the stages, which is the difference
    between a clang and a fizz.

    Dead centre: a Haas delay combs the clang away the moment anything sums
    to mono.
    """
    n, t = steps(dur)
    f = midi(note)
    rng = np.random.RandomState(seed)
    hitc = float(np.clip(hit, 0.05, 1.6))

    # the mallet: harder strikes are shorter and therefore brighter
    exc = rng.randn(n) * np.exp(-t / (0.0009 + 0.0016 * (1 - min(hitc, 1.2) / 1.2)))
    exc[0] += 2.0

    y = np.zeros(n)
    for k, (r, a, d) in enumerate(COWBELL_MODES):
        fk = f * (r + (ring if k in (2, 3) else 0.0))
        if fk > 15500.0:
            continue
        tau = d * decay * (0.85 + 0.30 * hitc)
        rr = np.exp(-1.0 / (tau * SR))
        w = 2 * np.pi * fk / SR
        m = lfilter([1 - rr], [1.0, -2 * rr * np.cos(w), rr * rr], exc)
        y += a * hitc ** min(0.22 * k, 2.6) * m / max(np.abs(m).max(), 1e-9)
    y = y / max(np.abs(y).max(), 1e-9)

    d1 = 1.4 + 2.0 * hitc                                # the body
    out = np.tanh(d1 * y) / np.tanh(d1)
    top = min(f * 11.0 * (1 - 0.5 * mute), 15500.0)
    met = bandpass(stereo(y), f * 1.8, max(top, f * 2.2))[:, 0]
    d2 = 3.0 + 7.0 * hitc                                # and the metal on top
    met = np.tanh(d2 * met) / np.tanh(d2)
    if folded:
        met = (1 - folded) * met + folded * fold(stereo(met), 1.6)[:, 0]
    out = out + clang * (1 - 0.45 * mute) * met

    out = bandpass(stereo(out), max(f * 0.75, 120.0), min(top * 1.25, 16000.0))
    # velocity is a level as well as a timbre. Normalising every strike to the
    # same peak would leave the riff's contour entirely in the spectrum, and a
    # line of cowbell at one level reads as a sequencer whatever its timbre does.
    lvl = 0.25 + 0.62 * min(hitc, 1.4)
    return norm(out * adsr(n, a=0.0006, r=0.014)[:, None], lvl) * gain * 0.70


# ---- the kick ----
@cached
def bumbo(dur=4.0, tune=47.0, gain=1.0, drive=3.4, knock=1.1, decay=0.17,
          hold=0.60, top=310.0, grit=0.6, click=1.0):
    """Four to the floor at 140, which is a kick every 428 ms.

    The dive and the drive are ordinary; the gate is not. `hold` is the
    fraction of the segment the tail is allowed before a 14 ms cut takes it
    to zero, so the bottom is genuinely empty when the next one lands. Left
    to decay, the tails overlap and the low end reads as one continuous
    rumble with a bump in it rather than four hits.

    `knock` is a second driven sine bandpassed 170-900 Hz. That band is
    lower than a hardstyle kick's bite and is the part a phone reproduces.
    `grit` is a folded saw in the same band: the dirt the style is made of,
    kept off the sub so it costs no headroom down low.
    """
    n, t = steps(dur)
    f = tune + (top - tune) * np.exp(-t / 0.021)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.tanh(drive * np.sin(ph)) * np.exp(-t / decay)

    kf = tune * 3.4 + 700.0 * np.exp(-t / 0.014)
    kn = bandpass(stereo(np.tanh(4.2 * np.sin(2 * np.pi * np.cumsum(kf) / SR))), 170, 900)
    kn *= (np.exp(-t / 0.040) * 0.55 * knock)[:, None]
    if grit:
        g = fold(np.tanh(5.0 * saw_ph(ph, tune * 9)), 1.2) * np.exp(-t / 0.055)
        kn = kn + grit * 0.45 * bandpass(stereo(g), 150, 520)

    ck = hp(stereo(np.random.randn(n) * np.exp(-t / 0.0017)), 1600) * 0.42 * click
    out = stereo(body) + kn + ck

    env = np.ones(n)                                  # the gate: a real gap
    k = int(hold * n)
    cn = min(max(int(0.014 * SR), 8), max(n - k - 1, 8))
    if k + cn < n:
        env[k:k + cn] = np.linspace(1, 0, cn) ** 0.7
        env[k + cn:] = 0
    out = out * env[:, None]
    return norm(hp(out, 26) * adsr(n, a=0.0005, r=0.008)[:, None], 0.96) * gain


# ---- the bass ----
def grave(note, dur, slide_from=None, glide=0.05, gain=1.0, grind=3.2,
          decay=0.55, hold=0.86, mid=1.0, cut=2200.0, click=1.0, suboct=0.0):
    """One oscillator, split at 130 Hz, and gated.

    Below: a clean mono sine, which is what moves air. Above: the same
    oscillator folded and clipped into the 150-500 Hz grunt - the ear
    rebuilds the missing fundamental from it, so the note survives a phone.
    Splitting one oscillator rather than layering two means the halves can
    never drift out of phase with each other.

    `hold` gates the whole voice the way `bumbo` gates its tail. In this
    style the sub is written as note-then-silence, not as a pad; a bass that
    decays through the gap smears every kick after it.
    """
    n, t = steps(dur)
    f0 = midi(note)
    f = np.full(n, f0) if slide_from is None else f0 + (midi(slide_from) - f0) * np.exp(-t / glide)
    ph = 2 * np.pi * np.cumsum(f) / SR

    env = np.exp(-t / decay) * adsr(n, a=0.002, r=0.04)
    k = int(hold * n)
    cn = min(max(int(0.018 * SR), 8), max(n - k - 1, 8))
    if k + cn < n:
        env[k:k + cn] *= np.linspace(1, 0, cn) ** 0.6
        env[k + cn:] = 0

    low = (np.sin(ph) + 0.20 * np.sin(2 * ph)) * env
    if suboct:
        low = low + suboct * np.sin(0.5 * ph) * env
    up = np.sin(ph) + 0.55 * np.sin(2 * ph) + 0.42 * np.sin(3 * ph) + 0.24 * np.sin(5 * ph)
    up = fold(np.tanh(grind * up), 1.22) * env
    out = stereo(low * 0.95) + lp(hp(stereo(up), 130), cut) * (1.55 * mid)
    if click:
        out += stereo(np.sin(5 * ph) * np.exp(-t / 0.007)) * 0.26 * click
    return norm(mono_below(out, 140), 0.95) * gain


# ---- the tom that carries the tresillo ----
@cached
def timbau(note=41, dur=2.0, gain=1.0, decay=0.085, slap=1.0, drop=6.0, wood=1.0):
    """A hand drum with a 3+3+2 to play.

    Struck skin, not struck metal: the overtones sit at 1, 1.59 and 2.14
    times the fundamental and the pitch falls a few semitones in the first
    20 ms as the head releases. Kept between 90 and 1200 Hz so it reads over
    the kick without taking any of its band.
    """
    n, t = steps(dur)
    f = midi(note)
    ph = 2 * np.pi * np.cumsum(f * 2 ** (drop / 12 * np.exp(-t / 0.020))) / SR
    x = (np.sin(ph) + 0.46 * np.sin(1.593 * ph) + 0.24 * np.sin(2.135 * ph)) * np.exp(-t / decay)
    x += np.random.randn(n) * np.exp(-t / 0.0035) * 0.45 * slap
    out = bandpass(stereo(np.tanh(2.4 * x)), 90, min(1200 * wood, 9000))
    out += hp(stereo(np.random.randn(n) * np.exp(-t / 0.008)), 4200) * 0.13 * slap
    return out * adsr(n, a=0.0007, r=0.012)[:, None] * gain * 0.55


# ---- the dry tic ----
@cached
def caixa(dur=1.0, gain=1.0, tune=340.0, decay=0.026, snap=1.0, bright=1.0):
    """The tic between the beats: a body and no ring.

    `rim` is a 1750 Hz sine that rings for 8 ms - all ping, no weight. This
    is a pitched knock that stops dead, with a noise snap over it, which is
    what the tamborzao pattern is played on.
    """
    n, t = steps(dur)
    f = tune * 2 ** (7.0 / 12 * np.exp(-t / 0.008))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    x += np.random.randn(n) * np.exp(-t / 0.0022) * 0.8 * snap
    out = bandpass(stereo(np.tanh(3.2 * x)), 220, min(6800 * bright, 15000))
    out += hp(stereo(np.random.randn(n) * np.exp(-t / 0.0035)), 3600) * 0.40 * snap
    return out * adsr(n, a=0.0004, r=0.007)[:, None] * gain * 0.55


# ---- the shaker ----
@cached
def chique(dur=1.0, gain=1.0, decay=0.030, rise=1.0, tone=1.0, seed=0):
    """A shaker, not a hi-hat.

    The beads travel before they land, so the envelope *rises* over the
    first few milliseconds and then falls - a hi-hat's exponential decay
    from an instant peak is the one thing that gives a programmed 16th line
    away. A slow high-passed band on top is the hiss of the shell.
    """
    rng = np.random.RandomState(seed)
    n, t = steps(dur)
    nz = rng.randn(n)
    env = (1 - np.exp(-t / (0.0035 * rise))) * np.exp(-t / decay)
    out = hp(stereo(nz), 6200 * tone) * env[:, None]
    out += bandpass(stereo(nz), 2400, 5200) * (env * 0.35)[:, None]
    return out * adsr(n, a=0.0004, r=0.006)[:, None] * gain * 0.42


# ---- the shout ----
def grito(dur=3.0, gain=1.0, f0=170.0, drop=4.0, vowel=('ae', 'ah'), rasp=1.0,
          bright=1.0):
    """A shouted syllable.

    Every voice in the engine sings: a stack of saws held at a pitch through
    a fixed vowel. A shout is not that. It is a glottal pulse train whose
    rate jitters by a few percent because the fold is not under control,
    falling `drop` semitones as the breath runs out, through formants that
    move within the syllable. The rasp is the pulses clipping, not a filter.
    """
    n, t = steps(dur)
    u = np.clip(t / t[-1], 0, 1)
    jit = 1 + 0.028 * np.sin(2 * np.pi * 23.0 * t) + 0.018 * np.sin(2 * np.pi * 7.3 * t)
    f = f0 * 2 ** (-drop / 12 * u ** 1.4) * jit
    ph = 2 * np.pi * np.cumsum(f) / SR
    pulse = np.tanh(6.0 * rasp * (saw_ph(ph, f0 * 26) ** 2 - 0.32))       # the glottis

    st = stereo(pulse)
    m = (u ** 0.6)[:, None]
    v0, v1 = FORMANTS[vowel[0]], FORMANTS[vowel[-1]]
    out = np.zeros_like(st)
    for i, g in enumerate((0.90, 0.85, 0.55)):
        out += (bandpass(st, v0[i] * 0.72, v0[i] * 1.35) * (1 - m)
                + bandpass(st, v1[i] * 0.72, v1[i] * 1.35) * m) * g
    out += hp(stereo(np.random.randn(n)), 3600) * (np.exp(-t / 0.030) * 0.22)[:, None]
    env = (1 - np.exp(-t / 0.010)) * np.exp(-t / (0.22 + 0.1 * u.mean()))
    out = lp(np.tanh(2.2 * out), min(7000 * bright, 15000))
    return widen(out, 0.22) * (env * adsr(n, a=0.002, r=0.03))[:, None] * gain * 0.9


# ---- the whistle call ----
def apito(dur=4.0, gain=1.0, f0=2350.0, trill=11.0, breath=0.5):
    """The samba whistle used as a call: a tone with a fast trill on it and
    the pea rattling inside. It holds its pitch and shakes, where a falling
    noise band would read as a drop rather than a summons."""
    n, t = steps(dur)
    warble = 1 + 0.055 * np.sin(2 * np.pi * trill * t)
    ph = 2 * np.pi * np.cumsum(f0 * warble) / SR
    tone = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    band = bandpass(stereo(np.random.randn(n)), f0 * 0.78, f0 * 1.30)
    out = stereo(tone) * (1 - breath) + band * breath * 0.55
    env = (1 - np.exp(-t / 0.008)) * np.minimum(1.0, np.exp(-(t - t[-1] * 0.7) / 0.09))
    return widen(out, 0.7) * (env * adsr(n, a=0.004, r=0.02))[:, None] * gain * 0.4
