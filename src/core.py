"""The engine both music modules share: synths, effects, mixer.

Everything here is pure synthesis and knows nothing about any sample. A module
picks the grid once with `set_grid()` and every `dur_steps` argument in the
library is measured against it; one grid (one engine) per process.

    src/core.py      this file - oscillators, ~50 synths, effects, Session
    src/amenlib.py   the Amen module: the break, its slices, 174 BPM
    src/phonklib.py  the phonk module: the 808 kit and cowbell, 160 BPM

Both modules re-export this one, so `from amenlib import *` and
`from phonklib import *` give you the same core API plus that module's kit.
"""
import os, numpy as np, wave
from scipy.signal import butter, sosfiltfilt, fftconvolve, lfilter, resample_poly
from scipy.ndimage import uniform_filter1d, minimum_filter1d

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, 'samples')
RENDERS = os.path.join(ROOT, 'renders')

# ---- the grid ----
BPM = 174.0
BAR = SR * 60.0 / BPM * 4
STEP = BAR / 16.0

def set_grid(bar_samples=None, bpm=None, beats=4):
    """define the bar. Either give it a length in samples (the Amen module
    measures its break) or a tempo. Returns (BAR, STEP) in samples."""
    global BAR, STEP, BPM
    if bar_samples is None:
        bar_samples = SR * 60.0 / bpm * beats
    BAR = float(bar_samples)
    STEP = BAR / 16.0
    BPM = float(bpm) if bpm else SR * 60.0 * beats / BAR
    return BAR, STEP

def steps(dur_steps, floor=8):
    """(n_samples, time_axis) for a duration given in 16th-note steps"""
    n = max(floor, int(dur_steps * STEP))
    return n, np.arange(n, dtype=np.float64) / SR

# ---- i/o ----
def load(path):
    w = wave.open(path, 'rb')
    n, ch = w.getnframes(), w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch).astype(np.float32) / 32768
    w.close()
    return x

def save(path, x):
    x = np.clip(x, -1, 1)
    w = wave.open(path, 'wb')
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes())
    w.close()

# ---- primitives ----
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

def stereo(x): return np.stack([x, x], 1).astype(np.float32)

def lp(seg, hz, order=4):
    sos = butter(order, min(float(hz), SR * 0.49), 'low', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def hp(seg, hz, order=2):
    sos = butter(order, max(float(hz), 12.0), 'high', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def bandpass(seg, lo_hz, hi_hz, order=2):
    lo = max(float(lo_hz), 15.0)
    hi = min(float(hi_hz), SR * 0.48)
    if hi <= lo * 1.05:
        hi = min(lo * 1.5, SR * 0.48)
    sos = butter(order, [lo, hi], 'band', fs=SR, output='sos')
    return sosfiltfilt(sos, seg, axis=0).astype(np.float32)

def adsr(n, a=0.008, r=0.06):
    a = min(int(a * SR), n // 2); r = min(int(r * SR), n // 2)
    env = np.ones(n)
    if a: env[:a] = np.linspace(0, 1, a)
    if r: env[-r:] *= np.linspace(1, 0, r)
    return env

def fade_edges(seg, ms=3.0):
    seg = seg.copy()
    k = min(int(SR * ms / 1000), len(seg) // 2)
    if k > 0:
        seg[:k] *= np.linspace(0, 1, k)[:, None]
        seg[-k:] *= np.linspace(1, 0, k)[:, None]
    return seg

def _lfo01(t, hz):
    """unipolar cosine LFO starting at 0"""
    return 0.5 - 0.5 * np.cos(2 * np.pi * hz * t)

def norm(x, peak=0.95):
    return (x * (peak / max(np.abs(x).max(), 1e-9))).astype(np.float32)

# ---- waveshaping ----
def dirty(seg, g=2.0):
    """tanh drive, level-compensated"""
    return (np.tanh(g * seg) / np.tanh(g)).astype(np.float32)

sat = dirty

def drive_asym(seg, g=2.0, asym=0.26, compensate=True):
    """Drive that keeps its even harmonics.

    `np.tanh` is an odd function, so pushing anything into it hard enough
    produces a square wave - odd harmonics only, every even one gone - and a
    waveform with no even harmonics reads as a chiptune whatever else is done
    to it. Real non-linearities are not symmetric: a valve, a lip, a reed and
    a loudspeaker cone all behave differently on the two halves of the cycle,
    and that asymmetry is the entire source of the second harmonic.

    Squashing one half harder puts DC on the signal, so it comes straight back
    off. Normalise before this, or `g` does not mean what it says."""
    x = np.asarray(seg, dtype=np.float32)
    y = np.where(x >= 0, np.tanh(g * x), np.tanh((1 - asym) * g * x) * (1 - asym * 0.5))
    y = y - y.mean(axis=0)
    if compensate:
        y = y / np.tanh(g)
    return y.astype(np.float32)


def fold(seg, g=1.6):
    """wavefolder: nastier than tanh - the sound of a cowbell pushed too far"""
    return np.sin(g * np.pi * 0.5 * np.clip(seg, -2, 2)).astype(np.float32)

def bitcrush(seg, bits=6, downsample=4):
    """lo-fi glitch: amplitude quantize + sample-rate reduction"""
    q = 2 ** (bits - 1)
    x = np.round(seg * q) / q
    if downsample > 1:
        x = np.repeat(x[::downsample], downsample, axis=0)[:len(seg)]
    return x.astype(np.float32)

# ---- caching ----
_SEG_CACHE = {}
def cached(fn):
    """A drum machine plays one recording of a kick, not four hundred fresh
    ones. Wrap a deterministic voice in this and the same arguments give back
    the same segment, so a six-minute track renders in seconds. Never wrap a
    voice that relies on fresh randomness per call - `pad`, `strings`, `vox`
    and `drone` all randomise their phases on purpose."""
    def wrap(*a, **kw):
        key = (fn.__name__, a, tuple(sorted(kw.items())))
        if key not in _SEG_CACHE:
            _SEG_CACHE[key] = fn(*a, **kw)
        return _SEG_CACHE[key]
    wrap.__name__ = fn.__name__
    wrap.__doc__ = fn.__doc__
    wrap.uncached = fn
    return wrap

# ---- automation lanes ----
# One value per step, turned into one value per sample. An LFO gives a
# shape that repeats; a lane is sixteen unrelated numbers, which is what
# makes a part read as a sequence of events rather than as a texture.
def steplane(values, n, kind='hold', smooth=0.003):
    """A per-sample parameter timeline from one value per step.

    This is the module's unit of composition. A wobble is an LFO: one shape,
    repeated, with a rate. A lane is sixteen unrelated numbers - the cutoff
    on step 5 has nothing to do with the cutoff on step 6 - which is what
    makes a bass line read as a sequence of events rather than as a texture.

    kind='hold'  stepped, edges rounded so the filter does not click
        'ramp'   linear between step centres
        'exp'    geometric between step centres (use for anything in Hz)
    """
    v = np.atleast_1d(np.asarray(values, dtype=np.float64))
    k = len(v)
    if k == 1:
        return np.full(n, v[0])
    if k == n:                    # already a per-sample lane - leave it alone
        return v
    if kind == 'hold':
        out = v[np.minimum(np.arange(n) * k // max(n, 1), k - 1)]
    else:
        x = (np.arange(k) + 0.5) * n / k
        w = np.log(np.maximum(v, 1e-6)) if kind == 'exp' else v
        out = np.interp(np.arange(n), x, w)
        if kind == 'exp':
            out = np.exp(out)
    if smooth:
        out = uniform_filter1d(out, max(int(smooth * SR), 3))
    return out


def ptlane(points, n, kind='ramp', smooth=0.003):
    """A lane from (step, value) breakpoints instead of one value per step -
    for the things that move across a phrase rather than per note."""
    pts = sorted(points)
    x = [min(int(p * STEP), n - 1) for p, _ in pts]
    y = np.array([v for _, v in pts], dtype=np.float64)
    if kind == 'hold':
        out = np.empty(n)
        edge = x + [n]
        for i in range(len(y)):
            out[edge[i]:edge[i + 1]] = y[i]
        out[:edge[0]] = y[0]
    else:
        w = np.log(np.maximum(y, 1e-6)) if kind == 'exp' else y
        out = np.interp(np.arange(n), x, w)
        if kind == 'exp':
            out = np.exp(out)
    if smooth:
        out = uniform_filter1d(out, max(int(smooth * SR), 3))
    return out


def scanlane(n, rates, lo=0.0, hi=8.0, shape='sine', curve=1.0, smooth=0.005,
             phase0=0.0):
    """A modulation lane whose RATE is sequenced rather than its value.

    This is the difference between a bass line and an arpeggio. An arpeggio is
    a sequence of notes: each event starts, is heard and ends. A drum & bass
    bass is one note that never stops, and the rhythm is how fast its timbre
    is moving - a long stretched sweep across half a bar, then four beats of
    sixteenths, then a bar of thirty-seconds. Nothing is re-triggered.

    `rates` is one value per step, in cycles per beat: 0 holds the lane still
    (the long stretch), 0.25 is one cycle per bar, 1 a quarter, 2 an eighth,
    4 a sixteenth, 8 a thirty-second, 2.667 an eighth triplet. The phase is
    integrated from the rate, so a rate change accelerates the movement
    without restarting it - which is what makes it read as one gesture
    speeding up rather than as two patterns cut together.
    """
    r = steplane(rates, n, 'hold', 0.020)
    ph = phase0 + 2 * np.pi * np.cumsum(r * (BPM / 60.0 / SR))
    if shape == 'saw':
        u = (ph / (2 * np.pi)) % 1.0
    elif shape == 'sawdown':
        u = 1.0 - ((ph / (2 * np.pi)) % 1.0)
    elif shape == 'square':
        u = (np.sin(ph) > 0).astype(np.float64)
    elif shape == 'tri':
        u = 2 * np.abs(((ph / (2 * np.pi)) % 1.0) - 0.5)
    else:
        u = 0.5 - 0.5 * np.cos(ph)
    u = np.clip(u, 0, 1) ** curve
    if smooth:
        u = uniform_filter1d(u, max(int(smooth * SR), 3))
    return lo + (hi - lo) * u

def rlane(n, k, lo, hi, seed=0, kind='hold'):
    """k random values in [lo, hi] spread over n samples. Structured chance:
    the pattern is fixed by the seed, so it repeats when the bar repeats, but
    it is not a shape anyone can hum."""
    rs = np.random.RandomState(seed)
    return steplane(lo + (hi - lo) * rs.rand(k), n, kind)


# ---- oscillators ----
def square(f, t, nyq=16500.0, kmax=60):
    """band-limited square: odd harmonics only, nothing above nyq"""
    x = np.zeros(len(t)); k = 1
    while f * k < nyq and k < kmax:
        x += np.sin(2 * np.pi * f * k * t) / k
        k += 2
    return x * (4 / np.pi)

def saw(f, t, nyq=16500.0, kmax=80, phase=0.0):
    """band-limited sawtooth"""
    x = np.zeros(len(t)); k = 1
    while f * k < nyq and k < kmax:
        x += np.sin(2 * np.pi * f * k * t + phase) / k
        k += 1
    return x * (2 / np.pi)

# ---- wavetable ----
_WT = {}

def wtable(name, K, f0=80.0, frames=24):
    """A wavetable stored as harmonic amplitudes, one row per frame.

    Every software wavetable synth stores single-cycle time-domain buffers and
    fights aliasing with mipmaps. Storing the frames as SPECTRA instead makes
    the oscillator exactly band-limited by construction - the table is built
    with only the harmonics that fit under Nyquist for the note being played -
    and it makes the position scan an interpolation between amplitude vectors,
    which is what the parameter is conceptually anyway.

    `f0` is the fundamental the table will be played at; the formant tables
    need it because a formant is fixed in hertz while a harmonic is not.
    """
    key = (name, K, round(f0, 1), frames)
    if key in _WT:
        return _WT[key]
    k = np.arange(1, K + 1, dtype=np.float64)
    A = np.zeros((frames, K + 1))
    for i in range(frames):
        u = i / max(frames - 1, 1)
        if name == 'growl':
            # a saw whose resonant peak climbs the harmonic series while a
            # notch walks down it, and whose odd harmonics come forward in
            # the middle of the scan. Sweeping this is not a filter sweep:
            # the shape of the waveform is different at every position.
            c = 2.0 + 22.0 * u ** 1.4
            bump = 1 + 7.0 * u * np.exp(-((k - c) / (1.6 + 3.5 * u)) ** 2)
            odd = 1 + 1.3 * np.sin(np.pi * u) * (k % 2)
            nc = 3.0 + 24.0 * (1 - u)
            notch = 1 - 0.8 * np.exp(-((k - nc) / 2.2) ** 2)
            a = bump * odd * notch / k
        elif name == 'morph':
            # sine -> triangle -> saw -> square -> narrow pulse -> dense
            seg = u * 4.0
            saw = 1 / k
            tri = np.where(k % 2 == 1, 1 / k ** 2, 0.0)
            sq = np.where(k % 2 == 1, 1 / k, 0.0)
            pul = np.abs(np.sin(k * np.pi * 0.12)) / k
            sine = np.where(k == 1, 1.0, 0.0)
            pts = [sine, tri, saw, sq, pul]
            j = min(int(seg), 3)
            f = seg - j
            a = pts[j] * (1 - f) + pts[j + 1] * f
        elif name == 'vowel':
            # five vowels as frames. The formants are in hertz, so which
            # harmonic they land on depends on the note - which is exactly
            # why a formant reads as a vocal tract and a filter does not.
            V = [(300, 870, 2240), (570, 840, 2410), (730, 1090, 2440),
                 (530, 1840, 2480), (270, 2290, 3010)]
            seg = u * (len(V) - 1)
            j = min(int(seg), len(V) - 2)
            f = seg - j
            a = np.zeros_like(k)
            for (fa, fb) in ((V[j], 1 - f), (V[j + 1], f)):
                for m, (fq, w, g) in enumerate(zip(fa, (0.16, 0.13, 0.11),
                                                   (1.0, 0.75, 0.42))):
                    a = a + fb * g * np.exp(-((k * f0 - fq) / (w * fq)) ** 2)
            a = (a + 0.12) / k ** 0.5
        elif name == 'witch':
            # The 'Do You Even Witch' sample, partial by partial: a resonant
            # hump on the third to sixth harmonic (+5 to +9 dB over a saw's
            # own 1/k), then about a decibel of loss per partial after it,
            # and nothing left by the twentieth. The scan walks the hump up
            # the series, which is the same gesture the sample makes.
            c = 3.0 + 15.0 * u ** 1.3
            hump = 1 + 2.2 * np.exp(-((k - c) / (1.5 + 2.2 * u)) ** 2)
            a = hump / k ** (1.15 - 0.25 * u)
        elif name == 'reeseb':
            # The 'Witch House Reese' sample: a saw's own slope to the fourth
            # partial, a 4-6 dB dip through the fifth to the fourteenth, then
            # a recovery - one broad gap travelling through the harmonics,
            # which is what a swept notch leaves and what makes a reese a
            # reese rather than a detuned saw.
            nc = 5.0 + 20.0 * u
            dip = 1 - 0.55 * np.exp(-((k - nc) / (3.2 + 2.0 * u)) ** 2)
            a = dip / k ** 0.92
        elif name == 'hollow':
            # odd harmonics, with the emphasis moving up the series
            c = 3.0 + 20.0 * u
            odd = np.where(k % 2 == 1, 1.0, 0.22 + 0.5 * u)
            a = odd * (1 + 1.6 * np.exp(-((k - c) / 3.0) ** 2)) / k
        elif name == 'rip':
            # the harsh end: a moving comb over a shallow slope, which is a
            # lot of energy where the ear is most sensitive. use it on one
            # patch of a pair, never on both
            comb = 0.35 + 0.65 * (0.5 + 0.5 * np.cos(k * (0.35 + 1.1 * u)))
            a = comb / k ** (0.55 + 0.35 * (1 - u))
        elif name == 'metal':
            # harmonics thinned to a sparse, near-inharmonic comb that gets
            # sparser as the scan advances
            rs = np.random.RandomState(7)
            mask = (np.sin(k * (1.1 + 2.6 * u)) > -0.2 + 0.6 * u).astype(float)
            a = mask * (1 / k ** (0.7 + 0.5 * u)) * (0.7 + 0.6 * rs.rand(K))
        else:
            a = 1 / k
        # Equal RMS per frame. A wavetable whose frames differ in level
        # turns a position scan into a volume envelope, and then every
        # modulation of the scan is heard as a tremolo instead of as a
        # change of timbre.
        A[i, 1:] = a * (0.35 / max(np.sqrt((a ** 2).sum() / 2), 1e-9))
    _WT[key] = A
    return A

def wtscan(ph, table, pos):
    """Read a spectral wavetable with a per-sample position.

    `pos` is the scan: a per-sample index into the table's frames, and moving
    it is the defining gesture of this kind of bass. A filter changes how much
    of a fixed spectrum you hear; this changes which spectrum there is.

    The harmonics are advanced by one complex multiply per partial rather than
    by a sine call, which is about four times faster and drifts by nothing -
    the multiplier is on the unit circle.
    """
    frames, K1 = table.shape
    K = K1 - 1
    n = len(ph)
    p = np.clip(np.asarray(pos, dtype=np.float64), 0, frames - 1)
    if p.ndim == 0:
        p = np.full(n, float(p))
    i0 = np.floor(p).astype(np.intp)
    i1 = np.minimum(i0 + 1, frames - 1)
    fr = p - i0
    z = np.exp(1j * ph)
    zk = np.ones(n, dtype=np.complex128)
    out = np.zeros(n)
    live = table.max(axis=0)
    for kk in range(1, K + 1):
        zk *= z
        if live[kk] < 2e-4:
            continue
        a = table[i0, kk] * (1 - fr) + table[i1, kk] * fr
        out += a * zk.imag
    return out

def sawstack(ph, f_max, voices=3, detune=14.0, seed=0, kmax=140, nyq=16500.0):
    """A detuned sawtooth stack - the oscillator at the centre of almost all
    electronic bass and lead design, and the one this engine was missing.

    One saw is a spectrum. Several saws a few cents apart are a spectrum whose
    every partial beats against its neighbours, and the beat rate rises with
    the partial number: at 14 cents the fundamental of an 87 Hz bass throbs
    at 0.7 Hz while its 40th partial shimmers at 28 Hz. That spread is what
    makes a detuned stack sound alive at the bottom and wide at the top from
    a single mono signal, and it is why the reese bass is built this way and
    not out of a filter.

    Band-limited by construction - every voice is a sum of sines that stops
    below `nyq` - so it can be transposed and layered without aliasing.
    `ph` is a phase array (2*pi*cumsum(f)/SR), so glides come for free;
    `f_max` is the highest fundamental the phase track reaches.

    voices=1 is a plain saw, 2-3 is a reese, 7 with detune 25-40 is a supersaw.
    """
    rs = np.random.RandomState(seed)
    offs = np.linspace(-1, 1, voices) if voices > 1 else np.zeros(1)
    out = np.zeros(len(ph))
    for o in offs:
        r = 2.0 ** (o * detune / 1200.0)
        out += saw_ph(ph * r + rs.rand() * 2 * np.pi, f_max * r, nyq, kmax)
    return out / voices

def saw_ph(ph, f, nyq=16500.0, kmax=80):
    """band-limited sawtooth from a phase array - for glides and vibrato.
    ph = 2*pi*cumsum(f_inst)/SR; f is the highest frequency it reaches."""
    x = np.zeros(len(ph)); k = 1
    while f * k < nyq and k < kmax:
        x += np.sin(k * ph) / k
        k += 1
    return x * (2 / np.pi)

# ---- the plucked string ----
def ks(f, n, decay=0.55, damp=0.42, pick=0.26, seed=0, hardness=0.55):
    """Karplus-Strong: a noise burst going round a delay line SR/f long, run
    through a two-tap lowpass on every lap so the top end dies first, exactly
    as it does on a real string. `pick` is where along the string it was hit
    (a comb notch - hit it at 1/4 and the 4th harmonic is missing), `damp` is
    how fast the highs go, `decay` is the note length in seconds.

    The cheapest physical model there is, and the only way to get a string
    that behaves like one: a guitar, a clav and a bass all come out of this
    function with different arguments and a different amplifier after it."""
    rng = np.random.default_rng(seed)
    # The two-tap loop filter has a phase delay of `damp` samples, and it is
    # inside the loop - so the string is that much longer than SR/f and plays
    # flat. Barely at 82 Hz, eleven cents at 988 Hz, which on a lead is the
    # difference between a guitar and a sad guitar. Take it back out here.
    L = max(SR / float(f) - damp, 4.0)
    Li = max(int(np.floor(L)), 2)
    frac = L - Li
    m = min(Li, n)

    e = rng.standard_normal(m)
    d = max(1, min(int(pick * Li), m - 1))
    e[d:] -= e[:-d]                                   # pick position comb
    if m > 8:                                         # pick hardness: a soft
        k = max(2, int(hardness * 12))                # pick has less top
        e = np.convolve(e, np.ones(k) / k, 'same')
    exc = np.zeros(n)
    exc[:m] = e

    a = np.exp(-Li / max(decay * SR, 1.0))            # loss per round trip
    out = exc.copy()
    if n <= Li:
        return out                                    # shorter than one lap:
    buf = exc                                         # only the pick exists
    for _ in range(int(n / Li) + 1):
        if np.abs(buf).max() < 1e-5:
            break
        sh = np.zeros(n)
        sh[Li:] = (1 - frac) * buf[:n - Li]
        if frac > 0 and n > Li + 1:
            sh[Li + 1:] += frac * buf[:n - Li - 1]
        sh = (1 - damp) * sh + damp * np.roll(sh, 1)  # the loop filter
        buf = sh * a
        out += buf
    return out




# ---- the string, mode by mode ----
def string(f0, n, decay=0.95, B=1.1e-4, pick=0.27, pickup=0.13, seed=0,
           bright=1.0, damp=0.025, top=6500.0, polar=1.0, retrig=0.0,
           res_hz=3000.0, res_q=2.4, bend=None, tilt=0.0):
    """A stiff steel string.

    `core.ks` gives a string whose partials are exact integer multiples of the
    fundamental and whose amplitude decays as one clean exponential. Neither
    is true of steel, and both are audible: perfect harmonicity is what an
    organ has, and a single decay rate is what a synthesiser has.

    Real behaviour, and what it costs to have it:

    * **Stiffness.** A steel string resists bending, so the nth mode sits at
      `n*f0*sqrt(1 + B*n^2)` - progressively sharp. By the 20th partial a
      wound low E is most of a semitone above where the maths says it should
      be, and that stretch is a large part of why a piano and a guitar sound
      like objects rather than tones.
    * **Two polarisations.** The string swings both across the fretboard and
      into it, at slightly different frequencies and very different decay
      rates. That is why a plucked note drops a few dB immediately and then
      rings for a second: two decays, not one. It is also where the shimmer
      in the top comes from.
    * **Where it was plucked and where it is heard.** The pluck cannot excite
      a mode that has a node at the pluck point, and the pickup cannot hear
      one that has a node above the pickup. Two independent combs.
    * **A magnetic pickup senses velocity, not displacement**, so every
      partial arrives scaled by its own frequency - a 6 dB/octave tilt - and
      the coil then resonates against the cable capacitance a few kHz up and
      rolls off above it. Displacement falls as 1/k^2, velocity brings it back
      to 1/k, and the resonance decides where the guitar is bright.
    * **How hard it was hit changes the spectrum, not the level.** `tilt`
      shades the whole partial series: negative rolls the top off, which is
      what a soft stroke physically does. The output is normalised, so a
      scalar here would do nothing at all - loudness is the caller's job and
      timbre is this function's."""
    rng = np.random.default_rng(seed)
    t = np.arange(n, dtype=np.float64) / SR
    kmax = int(min(top / f0, 190))
    if kmax < 1:
        kmax = 1
    k = np.arange(1, kmax + 1, dtype=np.float64)
    fk = k * f0 * np.sqrt(1 + B * k * k)               # stiffness
    keep = fk < SR * 0.45
    k, fk = k[keep], fk[keep]
    a = np.sin(k * np.pi * pick) / k ** 2              # the pluck
    a = a * np.sin(k * np.pi * pickup)                 # the pickup's own comb
    # A magnetic pickup senses velocity, so every partial arrives scaled by
    # its own frequency - that is the `+1` exponent. `tilt` is the STRIKE on
    # top of it: a hard pluck bends the string into a sharp corner and puts
    # energy into the high modes, a soft one rounds the corner off and does
    # not. So playing quietly is DARKER as well as lower, which is the whole
    # reason a comped chord breathes across a bar instead of pulsing, and it
    # cannot be had from a fader.
    a = a * (fk / f0) ** (1.0 + tilt) * bright
    # A pickup is a coil, and a coil with the cable's capacitance across it is
    # a resonant lowpass - it peaks a few dB somewhere between 2 and 5 kHz and
    # then falls away. That peak is not a tone control someone added; it is
    # the instrument, and it is a large part of why an electric guitar sounds
    # electric rather than like a very quiet acoustic.
    r = fk / res_hz
    a = a / np.sqrt((1 - r * r) ** 2 + (r / res_q) ** 2)
    tau = decay / (1 + damp * k ** 1.35)               # the top dies first
    out = np.zeros(n)
    ph = rng.random(len(k)) * 6.283
    det = 0.0022 * (0.6 + 0.8 * rng.random(len(k)))    # the second polarisation
    # Tremolo picking re-excites a string that never stopped. For evenly
    # spaced picks the re-swelling envelope is exactly exp(-(t mod P)/tau),
    # and the oscillator underneath it keeps its phase - which is why this
    # sounds like one note being picked and not like a row of notes.
    et = (t % retrig) if retrig else t
    # `bend` is a per-sample frequency multiplier - vibrato, a bent note, a
    # bottleneck sliding between two pitches. Integrating it once here gives
    # every partial the same glide for the cost of nothing: a fretted note
    # and a slide are the same string, and the difference between them is
    # entirely in this array.
    pb = t if bend is None else np.cumsum(np.asarray(bend, dtype=np.float64)[:n]) / SR
    for i in range(len(k)):
        out += a[i] * np.exp(-et / tau[i]) * np.sin(2 * np.pi * fk[i] * pb + ph[i])
        if polar:
            out += polar * 0.62 * a[i] * np.exp(-et / (tau[i] * 0.55)) * \
                np.sin(2 * np.pi * fk[i] * (1 + det[i]) * pb + ph[i] + 1.3)
    out /= max(np.abs(out).max(), 1e-9)
    # the plectrum itself: a click against a wound string, not part of the
    # string's motion at all
    m = min(int(0.004 * SR), n)
    click = rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.0011)
    out[:m] += click * 0.20 * bright
    return out


# ---- segment tools ----
def pitched(seg, factor):
    """factor<1 -> slower+lower, >1 -> faster+higher."""
    n = len(seg)
    idx = np.arange(0, n - 1, factor)
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], axis=1)
    return fade_edges(out.astype(np.float32))

def rev(seg): return fade_edges(seg[::-1])

def panned(seg, p):
    """equal-power pan: p in [-1 (left), +1 (right)]"""
    out = seg.copy()
    a = (p + 1) * np.pi / 4
    out[:, 0] *= np.cos(a) * 1.41
    out[:, 1] *= np.sin(a) * 1.41
    return out

def mono_below(seg, hz=120, order=4):
    """Fold everything under `hz` to the centre.

    The ear locates low frequencies by arrival time, not level, so there is
    no width down there to lose - but a club system that sums the bass, or a
    single earbud, will cancel whatever was out of phase. Reverb tails and
    Haas delays leak stereo into the sub without anyone hearing it until the
    track is on a big rig and the low end is quietly gone."""
    mid = seg.mean(axis=1)
    side = (seg[:, 0] - seg[:, 1]) * 0.5
    side = hp(np.stack([side, side], 1), hz, order)[:, 0]
    return np.stack([mid + side, mid - side], 1).astype(np.float32)

def side_boost(seg, hz=300.0, amount=0.8):
    """Widen only above `hz`, by adding a high-passed copy of the side signal
    back into the side. The centre is untouched and nothing below `hz` moves,
    so the low end stays where a club system can use it while the midrange
    opens up - which is how a reference with a quiet midrange still sounds
    enormous in it."""
    mid = seg.mean(axis=1)
    side = (seg[:, 0] - seg[:, 1]) * 0.5
    side = side + amount * hp(np.stack([side, side], 1), hz)[:, 0]
    return np.stack([mid + side, mid - side], 1).astype(np.float32)

def narrow(seg, amount=0.75):
    """Mid/side width control. 1.0 leaves it alone, 0.0 is mono, above 1.0
    widens. Unlike `mono_below` this acts on the whole spectrum, which is
    what a bus of decorrelated noise and reverb needs - several such buses
    sum to an image wider than anything a real record has, and the fix is a
    trim on each rather than less reverb on all of them."""
    mid = seg.mean(axis=1)
    side = (seg[:, 0] - seg[:, 1]) * 0.5 * amount
    return np.stack([mid + side, mid - side], 1).astype(np.float32)

def widen(seg, ms=0.9):
    """Haas widening: nudge the right channel late"""
    out = seg.copy()
    out[:, 1] = np.roll(out[:, 1], int(SR * ms / 1000))
    return out

def wah(seg, lfo_hz=2.0, lo=400, hi=3200):
    """funky wah: LFO crossfade between dark and bright filterings of a segment"""
    t = np.arange(len(seg)) / SR
    m = _lfo01(t, lfo_hz)[:, None]
    return (lp(seg, lo) * (1 - m) + lp(seg, hi) * m).astype(np.float32)

def shelf(seg, hz, db, kind='high'):
    """gentle shelving EQ: add (or subtract) a filtered copy of the signal"""
    g = 10 ** (db / 20) - 1
    part = hp(seg, hz) if kind == 'high' else lp(seg, hz)
    return (seg + g * part).astype(np.float32)

def peak_eq(seg, hz, db, width=0.5):
    """A bell: add (or subtract) a band-passed copy of the signal. Broad
    boosts and narrow cuts - a wide +2 dB is inaudible as an EQ move and
    audible as the instrument being there, which is the whole trick."""
    g = 10 ** (db / 20) - 1
    return (seg + g * bandpass(seg, hz * (1 - width), hz * (1 + width))).astype(np.float32)

def sweep_lp(seg, f0, f1, curve=1.0):
    """filter sweep: crossfade a dark and a bright copy over the segment"""
    u = (np.linspace(0, 1, len(seg)) ** curve)[:, None]
    return (lp(seg, f0) * (1 - u) + lp(seg, f1) * u).astype(np.float32)

def morph_lp(seg, f_lo, f_hi, env, bands=9, res=0.0, order=4):
    """A lowpass whose cutoff MOVES, approximated by crossfading a bank of
    static filters; `env` is 0..1 per sample and picks where in the bank each
    sample sits. `res` adds a resonant peak that travels with the cutoff.

    This is the difference between an instrument and a beep. A fixed filter
    with an envelope on the amplitude only changes how loud a note is; a
    moving filter changes what it is made of while it sounds, which is what
    every plucked or struck thing in the physical world does."""
    n = len(seg)
    fs = np.geomspace(max(f_lo, 40), min(f_hi, SR * 0.45), bands)
    u = np.clip(np.asarray(env, dtype=np.float64), 0, 1)[:n] * (bands - 1)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(fs):
        w = np.clip(1 - np.abs(u - i), 0, 1)
        if w.max() < 1e-4:
            continue
        y = lp(seg, f, order)
        if res:
            y = y + res * bandpass(seg, f * 0.82, f * 1.22, order=2)
        out += (y * w[:, None]).astype(np.float32)
    return out

def notch(seg, hz, width=0.16, depth=1.0):
    """One band taken out. A notch is not an EQ cut you hear as 'less
    treble' - move it and the ear tracks the gap, not the tone, which is why
    a swept notch reads as motion where a swept lowpass reads as brightness."""
    return (seg - depth * bandpass(seg, hz * (1 - width), hz * (1 + width))).astype(np.float32)

def stretch(seg, factor, grain=0.075, jitter=0.35, seed=0):
    """Change a segment's length without changing its pitch.

    `pitched()` is a tape deck: it moves length and pitch together, which is
    the jungle sound and is wrong the moment the material is tuned. This is
    overlap-add granular resynthesis - read the source slower or faster than
    the output is written, one Hann-windowed grain at a time, and cross-fade
    the seams.

    factor > 1 makes it longer. `jitter` randomises the read position by a
    fraction of a grain, which is what stops the overlaps from combing into a
    metallic ring: with no jitter, two grains a fixed distance apart phase
    against each other at a frequency you can hear as a pitch.
    """
    seg = np.asarray(seg, dtype=np.float32)
    if seg.ndim == 1:
        seg = stereo(seg)
    n = len(seg)
    if abs(factor - 1.0) < 1e-3 or n < 256:
        return seg
    g = max(int(grain * SR), 128)
    hop_out = g // 2
    hop_in = hop_out / float(factor)
    m = max(int(n * factor), g + 1)
    out = np.zeros((m + g, 2), dtype=np.float32)
    win = np.hanning(g).astype(np.float32)[:, None]
    rs = np.random.RandomState(seed)
    for k in range(0, m, hop_out):
        a = int(k * hop_in / hop_out + rs.uniform(-jitter, jitter) * g)
        a = int(np.clip(a, 0, n - g - 1)) if n > g + 1 else 0
        out[k:k + g] += seg[a:a + g] * win
    return fade_edges(out[:m] * 0.98, 2.0)


# ---- the moving filter ----
def _bq(kind, f, q):
    """One RBJ biquad's coefficients at cutoff f Hz and quality q."""
    w = 2 * np.pi * min(max(f, 12.0), SR * 0.47) / SR
    cw, sw = np.cos(w), np.sin(w)
    al = sw / (2 * max(q, 0.3))
    a0 = 1 + al
    if kind == 'lp':
        b = np.array([(1 - cw) / 2, 1 - cw, (1 - cw) / 2])
    elif kind == 'hp':
        b = np.array([(1 + cw) / 2, -(1 + cw), (1 + cw) / 2])
    elif kind == 'bp':
        b = np.array([al, 0.0, -al])
    elif kind == 'notch':
        b = np.array([1.0, -2 * cw, 1.0])
    else:                                                   # peaking, q=gain
        A = q
        al = sw / 2 * 1.4
        b = np.array([1 + al * A, -2 * cw, 1 - al * A])
        a0 = 1 + al / A
        return b / a0, np.array([1.0, -2 * cw / a0, (1 - al / A) / a0])
    return b / a0, np.array([1.0, -2 * cw / a0, (1 - al) / a0])


def svf(seg, cut, q=1.0, kind='lp', block=64, sat=0.0):
    """A resonant filter whose cutoff and resonance MOVE, done properly.

    Coefficients are recomputed every `block` samples and the delay line is
    carried across the boundary, so this is one continuous filter being
    turned rather than a crossfade between several. At q above about 4 it
    rings; at 10 with `sat` it screams and clips its own resonance, which is
    the sound the crossfade bank in `core.morph_lp` structurally cannot make.

    `cut` and `q` may be scalars or per-sample arrays.
    """
    seg = np.asarray(seg, dtype=np.float32)
    n = len(seg)
    cut = np.asarray(cut, dtype=np.float64)
    if cut.ndim == 0:
        cut = np.full(n, float(cut))
    qq = np.asarray(q, dtype=np.float64)
    if qq.ndim == 0:
        qq = np.full(n, float(qq))
    out = np.empty_like(seg)
    zi = np.zeros((2, 2))
    for a in range(0, n, block):
        b_ = min(a + block, n)
        bb, aa = _bq(kind, float(cut[a]), float(qq[a]))
        for c in range(2):
            y, zi[c] = lfilter(bb, aa, seg[a:b_, c].astype(np.float64), zi=zi[c])
            out[a:b_, c] = y
    if sat:
        out = np.tanh(sat * out) / np.tanh(sat)
    return out.astype(np.float32)


def resample(seg, ratio, keep=True):
    """One resampling pass. Bouncing a patch to audio and playing it back at
    a different rate does something no knob does: it moves every partial by
    the same ratio, so a stack that was harmonic before the pass is harmonic
    at a new fundamental and everything downstream of it - notches, formants,
    filter resonance - is now at the wrong place relative to the note. Two
    passes with a filter between them is where bass designers get harmonic
    relationships they did not program."""
    y = pitched(seg, ratio)
    if not keep:
        return y
    n = len(seg)
    if len(y) >= n:
        return y[:n]
    return np.pad(y, ((0, n - len(y)), (0, 0)))


def gate(seg, pattern, smooth=0.0018, floor=0.0):
    """A step gate. Silence inside a note is a parameter: the holes are what
    make a held bass read as sixteen events."""
    n = len(seg)
    g = steplane(np.asarray(pattern, dtype=np.float64), n, 'hold', smooth)
    return (seg * np.clip(g, floor, 1.0)[:, None]).astype(np.float32)


def chorus(seg, voices=3, depth_ms=5.5, rate=0.33, base_ms=13.0, mix=0.5, spread=1.0):
    """Several short delays, each modulated at its own slow rate and in
    opposite phase per channel. It is what a single oscillator has instead of
    a section: the detune is in the *time* domain, so the pitch stays exact
    while the thickness moves. Nothing on a hardstyle lead is left without it."""
    n = len(seg)
    t = np.arange(n) / SR
    out = np.array(seg, dtype=np.float32, copy=True) * (1 - mix)
    for v in range(voices):
        r = rate * (1 + 0.37 * v)
        base = base_ms * (1 + 0.23 * v)
        for ch in range(2):
            phase = v * 2.1 + ch * np.pi
            d = (base + depth_ms * np.sin(2 * np.pi * r * t + phase)) / 1000 * SR
            idx = np.clip(np.arange(n) - d, 0, n - 1)
            w = 0.5 + 0.5 * spread * (1 if ch == v % 2 else -1) * 0.4
            out[:, ch] += mix / voices * w * np.interp(idx, np.arange(n), seg[:, ch])
    return out.astype(np.float32)

def flanger(seg, rate=0.25, depth_ms=3.6, base_ms=0.5, fb=0.55, mix=0.85,
            taps=3, phase=0.0, env=None, spread=0.0):
    """A comb whose teeth move: the signal against a delayed copy of itself,
    the delay walking between `base_ms` and `base_ms + depth_ms`.

    A delay of d ms cancels every frequency at odd multiples of 1/(2d) Hz, so
    a 0.5-4 ms delay puts a rake of notches right through the harmonics of a
    bass note and drags them across it. This - not the detune - is what makes
    a Reese move; the detuned saws only supply something dense enough for the
    notches to bite into. Pass `env` (0..1 per sample) to sweep it by hand
    instead of by LFO."""
    n = len(seg)
    if env is None:
        t = np.arange(n) / SR
        env = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t + phase)
    env = np.clip(np.asarray(env, dtype=np.float64), 0, 1)[:n]
    base = np.arange(n, dtype=np.float64)
    out = np.array(seg, dtype=np.float32, copy=True)
    for c in range(2):
        # `spread` puts the two channels' notches in different places. That
        # is width the mono sum averages out instead of cancelling - unlike a
        # Haas delay, which nulls one fixed frequency the moment it sums.
        e = env if (c == 0 or not spread) else np.roll(env, int(spread * n))
        d = (base_ms + depth_ms * e) / 1000.0 * SR
        for k in range(1, taps + 1):
            idx = np.clip(base - d * k, 0, n - 1)
            g = mix * (fb ** (k - 1)) * (1.0 if k % 2 else -1.0)
            out[:, c] += (g * np.interp(idx, base, seg[:, c])).astype(np.float32)
    return (out / (1.0 + mix)).astype(np.float32)

def phaser(seg, rate=0.3, lo=280.0, hi=2600.0, stages=4, depth=0.85,
           bands=7, env=None):
    """Notches at `stages` harmonically-spaced points, all sweeping together
    between `lo` and `hi`. Softer than a flanger - the notches are not evenly
    spaced, so it swirls instead of ringing."""
    n = len(seg)
    if env is None:
        t = np.arange(n) / SR
        env = 0.5 - 0.5 * np.cos(2 * np.pi * rate * t)
    env = np.clip(np.asarray(env, dtype=np.float64), 0, 1)[:n]
    fs = np.geomspace(lo, hi, bands)
    u = env * (bands - 1)
    out = np.zeros((n, 2), dtype=np.float32)
    for i, f in enumerate(fs):
        w = np.clip(1 - np.abs(u - i), 0, 1)
        if w.max() < 1e-4:
            continue
        y = seg
        for k in range(stages):
            c = f * (1.0 + 1.35 * k)
            if c > SR * 0.42:
                break
            y = notch(y, c, width=0.22, depth=depth)
        out += (y * w[:, None]).astype(np.float32)
    return out

def split(seg, hz=110.0, order=4):
    """(below, above) - the multiband move every modern bass patch is built
    on: the sub stays a clean mono sine, everything else gets destroyed."""
    return lp(seg, hz, order), hp(seg, hz, order)

def sync_saw(t, f_master, ratio):
    """Hard sync: a saw running at `f_master * ratio` whose phase is reset by
    an oscillator at `f_master`. The pitch you hear stays at f_master; the
    ratio only changes the timbre, and sweeping it is the metallic tearing
    sound that no filter makes. `ratio` may be an array."""
    mph = (np.asarray(f_master, dtype=np.float64) * t) % 1.0
    return 2 * ((mph * ratio) % 1.0) - 1

def morph_formant(seg, v0='ah', v1='ee', env=None, wet=1.0, gain=1.6):
    """Crossfade a signal between two vowels. The formant pair does not move
    with pitch, so the note changes and the vowel does not - which is what
    makes it read as a voice rather than a filter."""
    n = len(seg)
    if env is None:
        env = np.linspace(0, 1, n)
    env = np.clip(np.asarray(env, dtype=np.float64), 0, 1)[:n][:, None]
    def vf(v):
        return sum(bandpass(seg, fc * 0.74, fc * 1.30) * g
                   for fc, g in zip(FORMANTS[v], (1.0, 0.72, 0.34)))
    out = vf(v0) * (1 - env) + vf(v1) * env
    return (seg * (1 - wet) + out * wet * gain).astype(np.float32)

def wow(seg, depth_ms=1.8, rate=0.7):
    """cassette wow: slow pitch drift from an uneven tape speed"""
    n = len(seg)
    t = np.arange(n) / SR
    idx = np.clip(np.arange(n) + depth_ms / 1000 * SR * np.sin(2 * np.pi * rate * t), 0, n - 1)
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], 1)
    return out.astype(np.float32)

def tape_stop(seg, stop_s=0.55):
    """the deck loses power: read rate falls 1 -> 0 and the pitch goes with it"""
    n = len(seg)
    m = max(int(stop_s * SR), 2)
    idx = np.cumsum(np.linspace(1.0, 0.0, m) ** 1.4)
    idx = idx[idx < n - 1]
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], 1)
    out *= (np.linspace(1, 0.15, len(out)) ** 0.7)[:, None]
    return out.astype(np.float32)

def rewind(seg, accel=3.0):
    """DJ rewind: play the segment backwards, spinning faster as it goes"""
    n = len(seg)
    rate = np.linspace(1.0, accel, n)
    idx = np.cumsum(rate); idx = idx[idx < n - 1]
    r = seg[::-1]
    out = np.stack([np.interp(idx, np.arange(n), r[:, c]) for c in range(2)], axis=1)
    return fade_edges(out.astype(np.float32))

def scratch(seg, cycles=2.0, depth=1.9, cut=True, gain=1.0):
    """A baby scratch: the record dragged back and forth under the needle.

    The playback rate is a cosine that goes negative, so the sound reverses and
    the pitch goes with it - one index track, no crossfading of separate takes.
    `cut` closes the fader on the backward half, which turns a drag into the
    chirp everyone actually recognises."""
    n = len(seg)
    u = np.linspace(0, 1, n)
    rate = 1.0 + depth * np.sin(2 * np.pi * cycles * u)
    idx = np.clip(np.cumsum(rate) * 0.5, 0, n - 1)
    base = np.arange(n, dtype=np.float64)
    out = np.stack([np.interp(idx, base, seg[:, c]) for c in range(2)], 1)
    if cut:
        g = np.clip(np.sign(rate) * 0.5 + 0.5, 0.12, 1.0)
        out *= uniform_filter1d(g, max(int(0.003 * SR), 3))[:, None]
    return fade_edges(out.astype(np.float32)) * gain

def spin(seg, r0=0.55, r1=1.0, curve=1.4):
    """A record brought up to speed by hand, or let go of. The pitch goes with
    the rate because on a turntable it always did, and a time-stretcher - which
    would hold the pitch - gets the one thing about this gesture wrong."""
    n = len(seg)
    m = int(n / max(min(r0, r1), 0.05) * 1.3) + 16
    u = np.linspace(0, 1, m) ** curve
    idx = np.cumsum(r0 + (r1 - r0) * u)
    idx = idx[idx < n - 1]
    out = np.stack([np.interp(idx, np.arange(n), seg[:, c]) for c in range(2)], 1)
    return fade_edges(out.astype(np.float32), ms=1.5)

# ---- space ----
_IR_CACHE = {}
def _reverb_ir(decay, tone):
    key = (round(decay, 2), int(tone))
    if key not in _IR_CACHE:
        n = int(decay * SR)
        t = np.arange(n) / SR
        rs = np.random.RandomState(hash(key) & 0xffff)
        ir = rs.randn(n, 2).astype(np.float32) * np.exp(-3 * t / decay)[:, None]
        ir = hp(lp(ir, tone), 150)          # dark tail, no low-end mud
        ir /= np.sqrt((ir ** 2).sum(axis=0, keepdims=True))
        _IR_CACHE[key] = ir
    return _IR_CACHE[key]

def reverb(seg, decay=3.0, wet=0.5, tone=4000, predelay=0.015):
    """space: convolution with a synthetic stereo IR; output rings past the input"""
    ir = _reverb_ir(decay, tone)
    pre = int(predelay * SR)
    out = np.zeros((len(seg) + pre + len(ir), 2), dtype=np.float32)
    out[:len(seg)] += seg
    for c in range(2):
        out[pre:pre + len(seg) + len(ir) - 1, c] += wet * fftconvolve(seg[:, c], ir[:, c])
    return out

def shimmer(seg, decay=6.0, wet=0.55, tone=3000, passes=3, fb=0.55,
            damp=4200, shift=2.0, predelay=0.02):
    """A reverb with a pitch shift inside its feedback path.

    `reverb()` above is one convolution: what goes in comes back darker and
    later and otherwise unchanged. Put a transposition in the loop and each
    pass returns an octave above the one before it, so a held chord grows a
    choir of its own harmonics that was never played - the partials arrive
    late, in tune, and from further away every time. It is the only reverb
    that adds notes.

    Each pass is re-reverberated, so the tail does not merely rise in pitch,
    it also spreads: pass three has been through six seconds of room three
    times and has no transient left in it at all. `damp` darkens the loop,
    which is what stops the octaves from stacking into a whistle - without
    it the top pass runs away, and that is the failure mode of every shimmer
    ever built.

    `shift` of 2.0 is the octave. 1.5 is a fifth and stacks into a dominant
    ninth over four passes, which is bright and slightly wrong; 0.5 is an
    octave DOWN and turns the same device into weight rather than air.
    """
    x = np.asarray(seg, dtype=np.float32)
    total = len(x) + int((decay * (passes + 1) + 1.0) * SR)
    out = np.zeros((total, 2), dtype=np.float32)
    g = 1.0
    for i in range(passes + 1):
        r = reverb(x, decay=decay, wet=1.0, tone=tone, predelay=predelay)
        r = r[:total]
        out[:len(r)] += r * (wet * g)
        if i == passes:
            break
        # the next pass is this tail transposed, darkened and sent round
        # again. Damping in the loop is not a tone control - it is what
        # keeps the octaves from accumulating into a whistle.
        up = resample(r, shift, keep=False)
        x = lp(up[:total], damp)
        g *= fb
    return out


def delay(seg, steps_=3.0, times=4, fb=0.45, ping=True, damp=400):
    """echoes ringing off into the mix, alternating channels when ping=True"""
    d = int(steps_ * STEP)
    out = np.zeros((len(seg) + d * times + 1, 2), dtype=np.float32)
    out[:len(seg)] += seg
    for i in range(1, times + 1):
        e = lp(seg, max(4200 - damp * i, 700)) * fb ** i
        if ping:
            e = panned(e, 0.6 if i % 2 else -0.6)
        out[i * d:i * d + len(seg)] += e
    return out

# ---- bass ----
def _ftrack(notes, n, glide=0.022, os_=1):
    """One frequency per sample from (step, midi) events. Smoothing the step
    edges IS the portamento - there is no separate glide stage, and because
    the track is never discontinuous the phase built from it never is either."""
    ev = sorted(notes)
    m = n * os_
    edge = [min(int(st * STEP) * os_, m) for st, _ in ev] + [m]
    f = np.empty(m)
    f[:edge[0]] = midi(ev[0][1])
    for i, (_, nt) in enumerate(ev):
        f[edge[i]:edge[i + 1]] = midi(nt)
    return uniform_filter1d(f, max(int(glide * SR * os_), 3))


def _amp(notes, n, decay=0.0, attack=0.0025, floor=0.0):
    """An envelope that swells at every attack and never returns to zero.

    Rendering a bass note by note breaks the fundamental: two segments that
    overlap at unrelated phases cancel, and the ear hears the gap as grit.
    Max-accumulating one envelope over one continuous oscillator means an
    attack re-excites a note that never stopped, which is what a string does.
    """
    amp = np.full(n, float(floor))
    for st, _ in sorted(notes):
        k = min(int(st * STEP), n - 1)
        if decay > 0:
            d = np.exp(-np.arange(n - k) / SR / decay)
        else:
            d = np.ones(n - k)
        np.maximum(amp[k:], d, out=amp[k:])
    return uniform_filter1d(amp, max(int(attack * SR), 3))


@cached
def subbar(notes, dur_steps=16, gain=1.0, glide=0.030, decay=0.0, h2=0.62,
           h3=0.18, drive=1.25, floor=0.0, gatep=None):
    """The sub: one sine, one phase, one bar, mono, no reverb, no distortion
    worth the name.

    It carries the second harmonic deliberately. With an F1 root at 43.7 Hz
    the fundamental lives in 20-60 Hz and the octave lands at 87 Hz, and the
    references put a quarter of their total energy in 60-120 - that band is
    not the kick, it is the sub's octave. A pure sine measures thin on every
    system smaller than a club.
    """
    n = int(dur_steps * STEP)
    f = _ftrack(notes, n, glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + h2 * np.sin(2 * ph) + h3 * np.sin(3 * ph)
    x *= _amp(notes, n, decay, 0.004, floor)
    if gatep is not None:
        x *= np.clip(steplane(gatep, n, 'hold', 0.004), 0, 1)
    y = np.tanh(drive * x) / np.tanh(drive)
    out = lp(stereo(y), 145, 4)
    return (out * adsr(n, a=0.004, r=0.006)[:, None]).astype(np.float32) * gain * 0.9


def sub(freq, dur_steps, gain=1.0):
    """clean sub sine with a tiny downward glide for punch"""
    n, t = steps(dur_steps)
    glide = freq * (1 + 0.12 * np.exp(-t / 0.02))
    ph = 2 * np.pi * np.cumsum(glide) / SR
    x = np.tanh(1.5 * (np.sin(ph) + 0.15 * np.sin(2 * ph))) * 0.75
    return stereo(x * adsr(n)) * gain

def wobble(freq, dur_steps, lfo_hz, gain=1.0):
    """jungle 'wow' sub: pitch + amp LFO"""
    n, t = steps(dur_steps)
    l = np.sin(2 * np.pi * lfo_hz * t)
    ph = 2 * np.pi * np.cumsum(freq * (1 + 0.03 * l)) / SR
    x = np.tanh(1.6 * np.sin(ph)) * (0.6 + 0.4 * (l * 0.5 + 0.5))
    return stereo(x * adsr(n, r=0.1)) * gain

def reese(freq, dur_steps, cutoff=350, gain=1.0):
    """two detuned saws, lowpassed - dark rolling bass"""
    n, t = steps(dur_steps)
    def s(f): return 2 * ((f * t) % 1.0) - 1
    x = s(freq * 0.995) + s(freq * 1.005) + 0.5 * s(freq * 2.003)
    x = lp(stereo(np.tanh(1.2 * x / 2.5)), cutoff)
    x[:, 1] = np.roll(x[:, 1], int(SR * 0.0008))
    return x * adsr(n, a=0.012, r=0.08)[:, None] * gain

def sawbass(freq, dur_steps, lfo_hz=2.0, gain=1.0):
    """jump-up mid saw: detuned saws + talky filter wobble (layer sub() under it)"""
    n, t = steps(dur_steps)
    x = sum(2 * ((freq * d * t) % 1.0) - 1 for d in (0.994, 1.0, 1.006)) / 3
    x = np.tanh(2.5 * x)
    dark, bright = lp(stereo(x), 300), lp(stereo(x), 3000)
    m = _lfo01(t, lfo_hz)[:, None]
    out = np.tanh(1.5 * (dark * (1 - m) + bright * m))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0006))
    return out * adsr(n, a=0.01, r=0.05)[:, None] * gain

def growl(freq, dur_steps, lfo_hz=4.0, fm=3.0, gain=1.0):
    """neuro growl: FM sine+saw, moving bandpass character, heavy tanh"""
    n, t = steps(dur_steps)
    depth = fm * (0.4 + 0.6 * _lfo01(t, lfo_hz))
    x = np.sin(2 * np.pi * freq * t + depth * np.sin(2 * np.pi * freq * 1.5 * t))
    x += 0.5 * (2 * ((freq * t) % 1.0) - 1)
    x = np.tanh(3 * x)
    dark, bright = lp(stereo(x), 180), lp(stereo(x), 2500)
    m = _lfo01(t, lfo_hz)[:, None]
    out = np.tanh(1.3 * (dark * (1 - m * 0.9) + bright * m))
    return out * adsr(n, a=0.006, r=0.05)[:, None] * gain

def funkbass(freq, dur_steps, gain=1.0, pop=False):
    """staccato slap-style pluck: saw+square, filter chirp, fast decay.
    pop=True -> brighter/snappier (octave-pop accents)."""
    n, t = steps(dur_steps)
    x = 0.6 * (2 * ((freq * t) % 1.0) - 1) + 0.4 * np.sign(np.sin(2 * np.pi * freq * t))
    x = np.tanh(1.8 * x)
    dark, bright = lp(stereo(x), 250), lp(stereo(x), 2200 if not pop else 3500)
    m = np.exp(-t / (0.05 if pop else 0.08))[:, None]     # filter chirp: bright attack
    out = dark * (1 - m) + bright * m
    env = np.exp(-t / (0.1 if pop else 0.16)) * adsr(n, a=0.004, r=0.02)
    return out * env[:, None] * gain

def upright(freq, dur_steps, gain=1.0):
    """double bass pluck: warm decaying body, finger thump, slight scoop into pitch"""
    n, t = steps(dur_steps)
    scoop = freq * (1 - 0.03 * np.exp(-t / 0.015))
    ph = 2 * np.pi * np.cumsum(scoop) / SR
    x = (np.sin(ph) + 0.6 * np.sin(2 * ph) * np.exp(-t / 0.35)
         + 0.3 * np.sin(3 * ph) * np.exp(-t / 0.2)
         + 0.12 * np.sin(4 * ph) * np.exp(-t / 0.1))     # upper partials carry the pitch
    x += lp(stereo(np.random.randn(n)), 300)[:, 0] * np.exp(-t / 0.015) * 0.4
    x = np.tanh(1.4 * x)
    out = stereo(x)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0007))
    return out * (np.exp(-t / 0.55) * adsr(n, a=0.004, r=0.04))[:, None] * gain

def subdrop(dur_steps=8, f0=75.0, f1=28.0, gain=1.0, drive=1.5, decay=1.1):
    """bass-drop boom: sine falling f0->f1 with a long decay"""
    n, t = steps(dur_steps)
    f = f1 + (f0 - f1) * np.exp(-t / 0.25)
    x = np.tanh(drive * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return stereo(x * np.exp(-t / decay) * adsr(n, a=0.004, r=0.1)) * gain

# ---- keys, leads, voices ----
def clav(notes, dur_steps, gain=1.0):
    """short funky clav/organ chord stab (notes = list of freqs)"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        x += (2 * ((f * t) % 1.0) - 1) + 0.3 * np.sign(np.sin(2 * np.pi * f * 2 * t))
    x /= len(notes)
    out = hp(lp(stereo(np.tanh(1.5 * x)), 4000), 300)
    env = np.exp(-t / 0.12) * adsr(n, a=0.003, r=0.02)
    return out * env[:, None] * gain

def rhodes(notes, dur_steps, gain=1.0):
    """soft e-piano chord: sine body + decaying 'tine' ping, light tremolo"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        x += (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.9)
              + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.35)
              + 0.18 * np.sin(2 * np.pi * 7 * f * t) * np.exp(-t / 0.05))
    x = np.tanh(1.3 * x / len(notes)) * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t))
    out = lp(stereo(x), 5000)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return out * adsr(n, a=0.004, r=0.08)[:, None] * gain

def piano(notes, dur_steps, gain=1.0):
    """90s rave/house piano stab: bright, punchy, slightly detuned"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        for d, g in ((0.997, 0.8), (1.0, 1.0), (1.004, 0.8)):
            x += g * (2 * ((f * d * t) % 1.0) - 1) * 0.6
        x += 0.5 * np.sin(2 * np.pi * f * t)
        x += 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.4)
    x = np.tanh(1.6 * x / (len(notes) * 2))
    out = hp(lp(stereo(x), 5200), 160)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0007))
    env = (0.4 * np.exp(-t / 0.06) + 0.6 * np.exp(-t / 0.5)) * adsr(n, a=0.002, r=0.04)
    return out * env[:, None] * gain

def pluck(freq, dur_steps, gain=1.0):
    """gentle melodic pluck (pairs well with Session.place_echo)"""
    n, t = steps(dur_steps)
    x = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * 2 * freq * t)
    out = stereo(np.tanh(x) * np.exp(-t / 0.22))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0012))
    return out * adsr(n, a=0.003, r=0.03)[:, None] * gain

def ep(notes, dur_steps, gain=1.0, vel=0.8, bark=1.0, trem=4.6, spread=1.0,
       decay=1.35, seed=0):
    """The tine electric piano, as FM rather than as a stack of sines.

    `rhodes()` sums three fixed sine layers with three fixed decays, so every
    note in every chord has the same timbre and the same length. A real tine
    does neither. Two things here are the whole difference:

    **Velocity is brightness, not level.** A hammer thrown harder drives the
    tine further into the pickup's non-linear field, so the harmonics rise
    faster than the fundamental does. `vel` moves the modulation index, and
    the level barely follows - which is why a soft chord sounds soft rather
    than merely quiet.

    **High notes die first.** Decay scales as 2**(-(note-60)/22), because a
    short stiff tine sheds energy faster than a long one. A chord voiced
    across two octaves therefore thins from the top down as it rings, and the
    root is still there when the ninth has gone. That is the sound the fixed
    envelope cannot make.

    Ratio 1:1 with a fast index decay is the body; a second operator near the
    14th harmonic, gone in 60 ms, is the strike on the metal.
    """
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    x = np.zeros((n, 2), dtype=np.float64)
    v = float(np.clip(vel, 0.05, 1.4))
    for i, f in enumerate(sorted(notes)):
        note = 69 + 12 * np.log2(max(f, 1e-6) / 440.0)
        tau = decay * 2.0 ** (-(note - 60) / 22.0)
        det = 1.0 + rs.uniform(-3.5, 3.5) / 1200.0          # per-note, cents
        w = 2 * np.pi * f * det * t
        idx_b = (0.9 + 2.6 * v) * np.exp(-t / (0.16 * tau))  # body index
        idx_t = (2.2 * v ** 1.6) * np.exp(-t / 0.055) * bark  # the tine strike
        body = np.sin(w + idx_b * np.sin(w)) * np.exp(-t / tau)
        tine = np.sin(14.0 * w + idx_t * np.sin(w)) * np.exp(-t / 0.075) * (0.25 * v)
        y = body + tine
        # Each note sits in its own place: the pan follows the register, so a
        # voicing opens across the field the way a real instrument's strings do.
        p = np.clip((note - 60) / 30.0, -1, 1) * 0.35 * spread
        ang = (p + 1) * np.pi / 4
        x[:, 0] += y * np.cos(ang) * 1.41
        x[:, 1] += y * np.sin(ang) * 1.41
    x = np.tanh(1.15 * x / max(len(notes), 1) ** 0.7)
    if trem:
        lfo = 1 + 0.10 * np.sin(2 * np.pi * trem * t)
        x[:, 0] *= lfo
        x[:, 1] *= 2 - lfo                                   # the suitcase pan
    out = hp(lp(x.astype(np.float32), 6200, 2), 90, 2)
    return out * adsr(n, a=0.0025, r=0.05)[:, None] * gain


def ens(notes, dur_steps, gain=1.0, voices=4, cutoff=3200, attack=0.30,
        bow=0.5, drift=1.0, seed=0):
    """A string section: several players, not one detuned oscillator.

    `strings()` and `pad()` start every voice at the same instant with a fixed
    detune, which is a chorus - one sound, widened. An ensemble is a set of
    players who disagree, and the disagreement is in three places at once:
    each voice enters 10-70 ms late, each drifts in pitch on its own slow
    random walk of a few cents, and each has its own bow noise. Sum those and
    the beating is aperiodic, which is why a section sounds like weather and a
    chorused saw sounds like a machine.
    """
    n, t = steps(dur_steps, floor=int(0.2 * SR))
    rs = np.random.RandomState(seed)
    out = np.zeros((n, 2), dtype=np.float64)
    for f in notes:
        for v in range(voices):
            cents = rs.uniform(-9, 9) * drift
            # A slow random walk, not an LFO: real intonation wanders and
            # never comes back to exactly where it was.
            walk = uniform_filter1d(rs.randn(n), max(int(0.35 * SR), 3))
            walk *= drift * 6.0 / max(np.abs(walk).max(), 1e-9)
            ratio = 2.0 ** ((cents + walk) / 1200.0)
            ph = 2 * np.pi * np.cumsum(f * ratio) / SR + rs.rand() * 6.28
            y = saw_ph(ph, f * 1.05, kmax=90)
            lag = int(rs.uniform(0.010, 0.070) * SR)
            y = np.concatenate([np.zeros(lag), y])[:n]
            pan = (v / max(voices - 1, 1) - 0.5) * 1.6 + rs.uniform(-0.2, 0.2)
            ang = (np.clip(pan, -1, 1) + 1) * np.pi / 4
            out[:, 0] += y * np.cos(ang)
            out[:, 1] += y * np.sin(ang)
    out /= max(len(notes) * voices, 1) ** 0.75
    if bow:
        # Rosin: band-passed noise that follows the swell, not a constant hiss.
        nz = bandpass(np.stack([rs.randn(n), rs.randn(n)], 1), 1800, 7000, 2)
        out += nz * bow * 0.045
    y = lp(out.astype(np.float32), cutoff, 4)
    a = min(int(attack * SR), n // 2)
    r = min(int(0.45 * SR), n // 2)
    env = np.ones(n, dtype=np.float32)
    env[:a] = np.linspace(0, 1, a) ** 1.6
    env[-r:] *= np.linspace(1, 0, r) ** 1.3
    return (y * env[:, None]).astype(np.float32) * gain * 0.7

# ---- arpeggios ----
# The metrical hierarchy of a 4/4 bar, as velocities. Beat 1 is strongest,
# beat 3 next, then 2 and 4, then the "and"s, then the remaining 16ths. An
# arpeggio that ignores this is a row of identical events, not a part.
_STEP_WEIGHT = {0: 1.00, 4: 0.78, 8: 0.88, 12: 0.74,
                2: 0.60, 6: 0.56, 10: 0.60, 14: 0.56}

def arp_seq(notes, bars=1, shape='up', rate=1.0, cycle=None, octaves=(0,),
            gate=None, ratchets=(), accents=(), tail=0.95, rotate=0,
            jitter=0.0, swing=0.0, seed=0):
    """Turn a chord into a part instead of a loop of itself.

    Returns [(step, midi_note, dur_steps, velocity), ...] across `bars` bars,
    ready to hand to any voice.

    The one decision that matters is `cycle`. A four-note pattern on a
    sixteen-step bar divides the bar exactly, so it lands identically every
    half-bar for the length of the track - that is what "all the arps sound
    the same" means, and no amount of reverb fixes it. Give the cycle a length
    coprime with 16 (5, 7, 9, 11) and the pattern walks: it starts on a
    different note every bar and does not come back around until bar 5, 7, 9
    or 11. Same notes, same synth, and it stops being wallpaper.

    shape    order the pool is played in
    cycle    notes before the pattern repeats - use 5/7/9/11, not 4 or 8
    octaves  octave offsets folded into the pool
    gate     0/1 mask over the cycle: which steps are silent (holes matter)
    ratchets indices in the cycle that fire twice at double speed
    accents  indices in the cycle that hit at full velocity
    tail     note length as a fraction of the step
    rotate   start the cycle somewhere other than its first note
    jitter   timing humanisation in steps (keep under ~0.06)
    swing    delay of every second note, as a fraction of a step
    """
    rs = np.random.RandomState(seed + 1)
    pool = [n + 12 * o for o in octaves for n in notes]
    if shape == 'down':
        pool = pool[::-1]
    elif shape == 'updown':
        pool = pool + pool[-2:0:-1]
    elif shape == 'downup':
        pool = pool[::-1] + pool[1:-1]
    elif shape == 'converge':                      # outside in: low, high, low, high
        lo, hi = pool[:], pool[::-1]
        pool = [x for pair in zip(lo, hi) for x in pair][:len(pool)]
    elif shape == 'thumb':                         # Alberti: root between every note
        root = pool[0]
        pool = [x for n in pool[1:] for x in (root, n)]
    elif shape == 'random':
        pool = list(rs.permutation(pool))
    cyc = int(cycle or len(pool))
    seq = [pool[i % len(pool)] for i in range(cyc)]

    out = []
    total = 16.0 * bars
    st = 0.0
    i = 0
    while st < total - 1e-6:
        k = (i + rotate) % cyc
        if gate is None or gate[k % len(gate)]:
            grid = int(round(st)) % 16
            v = _STEP_WEIGHT.get(grid, 0.42)
            if k in accents:
                v = min(1.0, v + 0.35)
            v *= 1.0 + 0.06 * rs.randn()
            pos = st + (swing * rate if int(st / rate) % 2 else 0.0)
            pos += jitter * rs.randn()
            if k in ratchets:                      # one step, two hits
                out.append((pos, seq[k], rate * 0.45 * tail, float(np.clip(v, 0.05, 1.2))))
                out.append((pos + rate * 0.5, seq[k], rate * 0.45 * tail,
                            float(np.clip(v * 0.72, 0.05, 1.2))))
            else:
                out.append((pos, seq[k], rate * tail, float(np.clip(v, 0.05, 1.2))))
        st += rate
        i += 1
    return out

@cached
def arpvoice(freq, dur_steps, gain=1.0, wave='saw', detune=0.007, f_lo=300,
             f_hi=6500, res=1.5, decay=0.11, open_=1.0, floor_=0.05, sub=0.0,
             drive=1.6, bands=7):
    """An arp note whose spectrum moves while it sounds: detuned oscillators
    through a filter that closes as the note decays.

    `pluck` and `bell` hold one timbre for the whole note and only get
    quieter - fine once, but sixteen of them a bar is the sound people call
    raw. Here the filter starts at `f_hi` and falls to `f_lo` on every single
    note, which is what a plucked string does and what a 303 does."""
    n, t = steps(dur_steps)
    if wave == 'square':
        x = square(freq * (1 - detune), t) + square(freq * (1 + detune), t)
    elif wave == 'tri':
        x = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * freq * t)) * 2
    else:
        x = saw(freq * (1 - detune), t) + saw(freq * (1 + detune), t)
    if sub:
        x = x + sub * np.sin(np.pi * freq * t * 2 * 0.5)
    cut = floor_ + (open_ - floor_) * np.exp(-t / decay)
    out = morph_lp(stereo(x / 2), f_lo, f_hi, cut, bands=bands, res=res)
    out = np.tanh(drive * out / (1 + res * 0.4))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    env = np.exp(-t / max(decay * 1.9, 0.02)) * adsr(n, a=0.0025, r=0.02)
    return out * env[:, None] * gain * 0.5

def bell(freq, dur_steps, gain=1.0):
    """icy glass bell: sine + inharmonic shimmer partials, long ring"""
    n, t = steps(dur_steps)
    x = (np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.8)
         + 0.5 * np.sin(2 * np.pi * freq * 2.756 * t) * np.exp(-t / 0.3)
         + 0.25 * np.sin(2 * np.pi * freq * 5.404 * t) * np.exp(-t / 0.12))
    out = stereo(np.tanh(x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0014))
    return out * adsr(n, a=0.002, r=0.05)[:, None] * gain

def lead(freq, dur_steps, gain=1.0, vib=5.5):
    """bright detuned-saw game lead with delayed vibrato"""
    n, t = steps(dur_steps)
    vibr = 1 + 0.008 * np.sin(2 * np.pi * vib * t) * np.minimum(t / 0.15, 1)
    x = np.zeros(n)
    for d in (0.99, 1.0, 1.01):
        ph = np.cumsum(freq * d * vibr) / SR
        x += 2 * (ph % 1.0) - 1
    x = np.tanh(1.5 * x / 3)
    out = lp(stereo(x), 3800)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0010))
    return out * adsr(n, a=0.01, r=0.06)[:, None] * gain

def hoover(freq, dur_steps, gain=1.0, sweep=0.35):
    """rave hoover stab: thick detuned saw stack with a falling pitch sweep.
    sweep = how far above the note the attack starts (0.35 = siren, ~0.1 = in-tune)"""
    n, t = steps(dur_steps)
    penv = 1 + sweep * np.exp(-t / 0.09)
    x = np.zeros(n)
    for d in (0.985, 0.992, 1.0, 1.008, 1.015):
        ph = np.cumsum(freq * d * penv) / SR
        x += 2 * (ph % 1.0) - 1
    x /= 5
    ph = np.cumsum(freq * 0.5 * penv) / SR
    x += 0.4 * (2 * (ph % 1.0) - 1)                       # octave below
    x = np.tanh(2 * x)
    out = lp(stereo(x), 3500)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0011))
    env = np.exp(-t / 0.35) * adsr(n, a=0.005, r=0.04)
    return out * env[:, None] * gain

def acid(freq, dur_steps, cutoff=900, res=4.0, gain=1.0, accent=False):
    """303-ish squelch: saw through a narrow resonant band + drive"""
    n, t = steps(dur_steps)
    x = 2 * ((freq * t) % 1.0) - 1
    fc = float(np.clip(cutoff * (1.6 if accent else 1.0), 150, 8000))
    st = stereo(x)
    out = lp(st, fc * 1.2) + res * bandpass(st, fc * 0.85, fc * 1.18)
    out = np.tanh(1.8 * out / (1 + res * 0.5))
    env = np.exp(-t / (0.09 if accent else 0.16)) * adsr(n, a=0.003, r=0.02)
    return out * env[:, None] * gain

def orchhit(root_midi, dur_steps=3, gain=1.0):
    """jungle orchestra hit: minor stab across octaves + noise burst, fast decay"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for off in (-12, 0, 3, 7, 12, 15):
        f = midi(root_midi + off)
        x += (2 * ((f * t) % 1.0) - 1) * (1.4 if off <= 0 else 1.0)
    x = np.tanh(x / 4)
    x += 0.25 * np.random.randn(n) * np.exp(-t / 0.02)
    out = lp(stereo(x), 4500)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0008))
    return out * (np.exp(-t / 0.25) * adsr(n, a=0.003, r=0.03))[:, None] * gain

# F1/F2/F3 of the spoken vowels. F1 and F2 alone identify the vowel; F3 near
# 2500-3000 Hz is what stops it sounding like two bandpasses.
FORMANTS = {'ee': (270, 2290, 3010), 'ih': (390, 1990, 2550),
            'eh': (560, 1840, 2480), 'ae': (660, 1720, 2410),
            'ah': (700, 1220, 2600), 'uh': (640, 1190, 2390),
            'aw': (570, 840, 2410), 'oh': (450, 800, 2830),
            'oo': (325, 700, 2530)}

def vox(notes, dur_steps, gain=1.0, vowel='ah'):
    """formant choir pad: saw stack through vowel bandpasses, slow attack, vibrato"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        vibr = 1 + 0.006 * np.sin(2 * np.pi * 4.8 * t + np.random.rand() * 6)
        for d in (0.995, 1.0, 1.005):
            ph = np.cumsum(f * d * vibr) / SR
            x += 2 * (ph % 1.0) - 1
    x /= 3 * len(notes)
    st = stereo(x)
    out = sum(bandpass(st, fc * 0.75, fc * 1.3) * g
              for fc, g in zip(FORMANTS[vowel], (1.0, 0.6, 0.25)))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0016))
    a = int(0.3 * SR); r = int(0.35 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, min(a, n)); env[-r:] *= np.linspace(1, 0, min(r, n))
    return out * env[:, None] * gain * 1.6

def diva(freq, dur_steps, gain=1.0):
    """gospel diva wail: single-voice formant lead with deep delayed vibrato"""
    n, t = steps(dur_steps)
    vibr = 1 + 0.018 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(t / 0.35, 1)
    x = np.zeros(n)
    for d in (0.997, 1.0, 1.003):
        ph = np.cumsum(freq * d * vibr) / SR
        x += 2 * (ph % 1.0) - 1
    st = stereo(x / 3)
    out = sum(bandpass(st, fc * 0.72, fc * 1.32) * g
              for fc, g in zip((800, 1150, 2900), (1.0, 0.7, 0.35)))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0012))
    a = min(int(0.06 * SR), n // 2); r = min(int(0.15 * SR), n // 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain * 1.8

def horn(freq, dur_steps, gain=1.0, fall=0.0):
    """harmon-muted trumpet: reedy tone through a tight bandpass, breath,
    delayed vibrato; fall = semitones to drop at the phrase end (noir fall-off)"""
    n, t = steps(dur_steps)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 4.7 * t) * np.minimum(t / 0.4, 1)
    fenv = np.ones(n)
    if fall > 0:
        k = int(n * 0.75)
        fenv[k:] = 2 ** (-fall / 12 * np.linspace(0, 1, n - k))
    f = freq * vib * fenv
    ph = np.cumsum(f) / SR
    x = 0.6 * (2 * (ph % 1.0) - 1) + 0.4 * np.sign(np.sin(2 * np.pi * ph))
    st = stereo(np.tanh(1.3 * x))
    out = bandpass(st, 700, 2600) * 1.8
    out += hp(stereo(np.random.randn(n) * 0.05), 3000) * np.minimum(t / 0.1, 1)[:, None]
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0010))
    return out * adsr(n, a=0.04, r=0.09)[:, None] * gain

def strings(notes, dur_steps, gain=1.0):
    """ensemble strings: wide detuned saw stack, brighter and faster than pad"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        for d in (0.992, 0.997, 1.003, 1.008):
            x += 2 * ((f * d * t + np.random.rand()) % 1.0) - 1
    x /= 4 * len(notes)
    out = hp(lp(stereo(x), 5500), 200)
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0013))
    a = int(0.09 * SR); r = int(0.2 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, min(a, n)); env[-r:] *= np.linspace(1, 0, min(r, n))
    return out * env[:, None] * gain

def pad(notes, dur_steps, cutoff=1800, gain=1.0, wide=0.0):
    """soft detuned-saw chord, slow attack (notes = list of freqs)"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for f in notes:
        for d in (0.996, 1.0, 1.004):
            x += 2 * ((f * d * t + np.random.rand()) % 1.0) - 1
    x /= 3 * len(notes)
    out = lp(stereo(x), cutoff)
    if wide:
        out = widen(out, wide)
    a = int(0.25 * SR); r = int(0.3 * SR)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain

def drone(freq, dur_steps, gain=1.0):
    """deep space drone: sine layers breathing on slow independent LFOs"""
    n, t = steps(dur_steps)
    x = np.zeros(n)
    for mult, amp, rate in ((0.5, 0.5, 0.031), (1.0, 1.0, 0.043), (1.498, 0.4, 0.057),
                            (2.005, 0.25, 0.071), (2.997, 0.12, 0.089)):
        breath = 0.55 + 0.45 * np.sin(2 * np.pi * rate * t + np.random.rand() * 6)
        x += amp * np.sin(2 * np.pi * freq * mult * t + np.random.rand() * 6) * breath
    x += 0.15 * lp(stereo(2 * ((freq * t) % 1.0) - 1), 600)[:, 0]
    out = stereo(np.tanh(x / 2))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.002))
    a = min(int(2.0 * SR), n // 2); r = min(int(2.5 * SR), n // 2)
    env = np.ones(n); env[:a] = np.linspace(0, 1, a); env[-r:] *= np.linspace(1, 0, r)
    return out * env[:, None] * gain

# ======================================================= struck membranes ===
# Bessel zeros of an ideal circular head, as ratios to the (0,1) mode. The
# axisymmetric ones - 1.000, 2.295, 3.598 - are the only modes a strike in the
# CENTRE can excite, because every other mode has a node through the middle.
# That single fact is why the bass stroke of a conga sounds hollow and low and
# the open stroke at the edge sings: they are not two envelopes, they are two
# different drums inside the same skin.
# Bessel zeros j(m,n) divided by j(0,1), out to the 23rd mode. Past about the
# tenth these are inaudible individually and only matter as the density that
# makes a skin sound like a skin rather than like a tuned pipe.
HEAD = np.array([1.0000, 1.5934, 2.1356, 2.2954, 2.6531, 2.9174, 3.1555,
                 3.5001, 3.5985, 3.6475, 4.0590, 4.1318, 4.2305, 4.6011,
                 4.6102, 4.8319, 4.9033, 5.0836, 5.1308, 5.4122, 5.5405,
                 5.5532, 5.6510])
AXIAL = np.zeros(23); AXIAL[[0, 3, 8, 16]] = 1.0          # the m=0 family

# The pitched part of a conga really does all live under a kilohertz - 23
# modes of a head tuned to F3 only reach 980 Hz. So the crack of a slap is not
# the head at all: it is the hand. `crack` is a rung contact resonance, the
# fingers hitting a stretched skin near the rim, and it is what tells the two
# strokes apart from across a room.
#            fund  upper  decay   drop  nz    nz_lo  nz_hi  nz_tau  axial crack crk_hz crk_tau
STROKE = {
    'open': (1.00, 1.00, 0.400,  1.5, 0.34,   250,  5000, 0.0035, 0.00, 0.10, 1500, 0.0035),
    'slap': (0.10, 1.35, 0.048,  3.2, 3.20,  1400,  9500, 0.0028, 0.00, 1.55, 2150, 0.0090),
    'bass': (1.30, 0.26, 0.130,  3.6, 0.42,   110,  1300, 0.0048, 0.95, 0.00, 1200, 0.0020),
    'muff': (0.85, 0.68, 0.068,  2.0, 0.40,   300,  4000, 0.0030, 0.10, 0.16, 1700, 0.0030),
    'tip':  (0.28, 0.90, 0.036,  1.0, 1.10,   900,  8000, 0.0016, 0.00, 0.45, 2600, 0.0035),
    'heel': (1.00, 0.22, 0.085,  3.0, 0.32,   100,   900, 0.0052, 0.00, 0.00, 1200, 0.0020),
    'toe':  (0.24, 0.72, 0.028,  1.0, 0.85,   800,  7000, 0.0014, 0.00, 0.35, 2400, 0.0028),
}


def membrane(f0, n, stroke='open', load=0.94, tight=1.0, damp=0.55,
             seed=0, spread=1.0):
    """One struck drumhead, mode by mode. Returns mono float64, length n.

    `load` is the air the head has to drag with it. An ideal membrane's modes
    sit at the Bessel ratios above; a real head loaded by the air column
    inside the shell has its upper modes pulled DOWN toward harmonicity, which
    is why a conga has a pitch you can tune to a key and a snare drum does
    not. Raising it toward 1.0 gives back the ideal - clangier, more gong.

    `damp` is the hand. Higher modes always die first, and how much faster is
    the difference between a drum that rings and a drum a player is standing
    over."""
    fu, up, dec, drop, nz, nlo, nhi, ntau, ax, ck, ckhz, cktau = STROKE[stroke]
    rng = np.random.default_rng(seed * 977 + 13)
    t = np.arange(n, dtype=np.float64) / SR

    r = HEAD ** load                                   # the air loads the head
    a = np.where(np.arange(len(r)) == 0, fu, up) / r ** 1.15
    a = a * (1 - ax) + a * AXIAL * ax * 2.4            # centre strike: m=0 only
    a = a * (1 + 0.10 * rng.standard_normal(len(r)))   # no two hits are equal
    keep = r * f0 < SR * 0.45
    r, a = r[keep], a[keep]

    # The head is momentarily tighter under the hand and relaxes; that fall is
    # what says struck skin instead of struck metal.
    f = f0 * 2 ** (drop / 12 * np.exp(-t / 0.020))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tau = dec / tight / (1 + damp * (r - 1) ** 1.25)
    osc = np.sin(np.outer(ph, r) + rng.random(len(r)) * 6.283)
    env = np.exp(-np.outer(t, 1.0 / tau))
    x = (osc * env * a).sum(1) / max(np.abs(a).sum(), 1e-9)

    # the hand itself, which is not part of the head's motion at all
    m = min(n, int(0.030 * SR))
    tm = np.arange(m) / SR
    hand = rng.standard_normal(m) * np.exp(-tm / ntau)
    hand = bandpass(stereo(hand), nlo, nhi)[:, 0]
    x[:m] += hand * nz * 0.9
    if ck:
        # the contact resonance: three close partials, because a hand is not a
        # tuning fork, rung by the strike and gone in ten milliseconds
        cr = sum(w * np.sin(2 * np.pi * ckhz * q * tm + rng.random() * 6)
                 for q, w in ((1.0, 1.0), (1.47, 0.55), (2.11, 0.28)))
        x[:m] += cr * np.exp(-tm / cktau) * ck * 0.55
    return x


# ---- the 808 drum machine ----
def kick(dur_steps=4, tune=51.0, top=290.0, punch=1.0, drive=2.6, gain=1.0, decay=0.34):
    """808 kick: a fast pitch dive into a saturated sine, with a click on top"""
    n, t = steps(dur_steps)
    f = tune + (top - tune) * np.exp(-t / 0.028)
    x = np.tanh(drive * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / decay)
    click = np.random.randn(n) * np.exp(-t / 0.0018) * 0.5 * punch
    click += np.sin(2 * np.pi * 1700 * t) * np.exp(-t / 0.004) * 0.35 * punch
    out = stereo(x) + hp(stereo(click), 900)
    return norm(out * adsr(n, a=0.0006, r=0.02)[:, None], 0.95) * gain

def rawkick(dur_steps=3, tune=55.0, rise=1.9, tau=0.06, drive=9.0, gain=1.0,
            decay=0.3, punch=1.0, tone=4200, weight=0.45, mid=2.8, raw=0.5,
            scream=0.35):
    """The hard-dance kick, where the kick is the instrument and its tail is
    the bass note. A sine dives onto `tune`, then goes through the chain that
    makes it hurt: drive, EQ, drive again, wavefold - every stage after an EQ
    makes new harmonics, and that is where the scream comes from. `raw` is how
    far into the folder it goes and `scream` adds the overtone on top; both at
    0 give a clean hardstyle kick, both up give industrial hardcore. Tune it
    to the root: at this much distortion the tail is audibly pitched, so an
    untuned kick fights the key."""
    n, t = steps(dur_steps)
    f = tune * (1 + rise * np.exp(-t / tau))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.tanh(drive * np.sin(ph))                                  # stage 1: drive
    x = lp(stereo(x), tone)
    x = x + weight * bandpass(x, tune * 0.8, tune * 2.4)             # EQ: the chest
    x = x + mid * bandpass(x, 240, 1900)                             # EQ: the part you hear
    x = np.tanh(2.1 * x / (1 + mid * 0.35))                          # stage 2: drive the EQ
    x = x + 0.8 * bandpass(x, 900, 4600)                             # EQ: presence
    if raw:                                                          # stage 3: the grit
        grit = np.tanh(7 * (saw_ph(ph, tune * 14) + 0.4 * np.sin(1.5 * ph)))
        grit = bandpass(stereo(grit), 300, 6800) * np.exp(-t / (decay * 0.7))[:, None]
        x = x + raw * 1.5 * fold(grit, 1.1)
    if scream:                                                       # and the scream on top
        sc = np.tanh(5 * saw_ph(2 * ph, tune * 20)) * np.exp(-t / min(0.07, decay * 0.35))
        x = x + scream * bandpass(stereo(sc), 1500, 9000) * 1.2
    tail = lp(x, 11000) * np.exp(-t / decay)[:, None]
    pf = tune * (1 + 7.0 * np.exp(-t / 0.012))
    pnch = np.tanh(6 * np.sin(2 * np.pi * np.cumsum(pf) / SR)) * np.exp(-t / 0.03)
    click = np.random.randn(n) * np.exp(-t / 0.0022) * 0.8
    click += np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.003) * 0.5
    out = tail + 0.8 * stereo(pnch) * punch + hp(stereo(click), 3000) * 0.55 * punch
    return norm(hp(out, 32) * adsr(n, a=0.0004, r=0.015)[:, None], 0.97) * gain

def splitkick(dur_steps=3.0, tune=58.27, gain=1.0, punch=1.0, drive=7.0,
              bite=1.0, click=1.0, tail=1.0, hold=0.70, sat=1.15, h3=0.05,
              glide=0.35, cut=0.020, sub_lp=118.0, tail_decay=0.0):
    """The hard-dance kick built the way the records are: as two instruments
    that happen to start together.

    Measured off a hardstyle reference, the sustained part of the kick is a
    *clean* sine - first harmonic 48% of the energy, second 0.5%, third 2.4% -
    holding at a near-constant level for about 70% of the beat and then
    stopping. All the distortion is in the first 35 ms. That split is the
    whole sound:

      - the tail is loud, pure and low, so it moves air without putting
        anything in the midrange (in the reference, 93% of the tail's energy
        is between 45 and 75 Hz);
      - the punch is short, driven and broadband, so the hit is defined;
      - and the gap before the next one is real silence.

    Distorting the tail instead - the obvious way to build a "hard" kick -
    fills the midrange with harmonics, so the kick fights the lead, the mix
    needs the lead louder to compete, and the low end ends up a third of what
    it should be. It also turns the tail into a decay, and a decay reads as a
    boom that trails off rather than a hit with an end.

    `hold` is the fraction of the segment the tail holds before it is cut, so
    the gap scales with whatever `dur_steps` the tempo calls for."""
    n, t = steps(dur_steps)

    f = tune * (1 + glide * np.exp(-t / 0.012))          # the tail
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) + h3 * np.sin(3 * ph)
    body = np.tanh(sat * body) / np.tanh(sat)
    env = np.ones(n)
    a = max(int(0.003 * SR), 2)
    env[:a] = np.linspace(0, 1, a) ** 0.5
    if tail_decay:
        env *= np.exp(-t / tail_decay)
    k = int(hold * n)
    cn = min(max(int(cut * SR), 8), max(n - k - 1, 8))
    if k + cn < n:
        env[k:k + cn] = env[k:k + cn] * np.linspace(1, 0, cn)
        env[k + cn:] = 0
    out = lp(stereo(body * env), sub_lp) * tail

    pf = tune * 2.0 + (780 - tune * 2.0) * np.exp(-t / 0.011)    # the punch
    p = stereo(np.tanh(drive * np.sin(2 * np.pi * np.cumsum(pf) / SR)))
    p = p * np.exp(-t / 0.038)[:, None]
    # the knock: in the reference a third of the punch's energy is 75-110 Hz,
    # and that band is the part of a kick a laptop or a phone can actually
    # reproduce - the 55 Hz tail below it is felt on a rig and silent anywhere else
    p = p + 0.95 * bandpass(p, 70, 145) + 0.45 * bandpass(p, 145, 260)
    p = p + bite * 0.9 * bandpass(p, 500, 1400)
    out = out + punch * 0.5 * np.tanh(1.6 * p)

    ck = np.random.randn(n) * np.exp(-t / 0.0018) * 0.9          # the click
    ck = ck + np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.0028) * 0.5
    out = out + click * 0.4 * hp(stereo(ck), 1800)

    return norm(hp(out, 26) * adsr(n, a=0.0004, r=0.012)[:, None], 0.97) * gain

def snare(dur_steps=3, gain=1.0, drive=2.4, bright=1.0, body=1.0):
    """phonk snare: a clap stack over a short tuned body, driven hard"""
    n, t = steps(dur_steps)
    nz = np.random.randn(n)
    tail = hp(stereo(nz), 1500 * bright) * np.exp(-t / 0.115)[:, None]
    burst = np.zeros(n)
    for d in (0.0, 0.009, 0.019, 0.030):
        k = int(d * SR)
        burst[k:] += np.random.randn(n - k) * np.exp(-np.arange(n - k) / SR / 0.011)
    claps = bandpass(stereo(burst), 900, 5200 * bright) * 0.55
    tone = (0.55 * np.sin(2 * np.pi * 195 * t) * np.exp(-t / 0.055)
            + 0.35 * np.sin(2 * np.pi * 330 * t) * np.exp(-t / 0.04)) * body
    out = np.tanh(drive * (stereo(tone) + tail * 1.15 + claps)) / np.tanh(drive)
    return out * adsr(n, a=0.0008, r=0.02)[:, None] * gain

def rim(dur_steps=1, gain=1.0):
    """rimshot tick for the in-between 16ths"""
    n, t = steps(dur_steps)
    x = np.sin(2 * np.pi * 1750 * t) * np.exp(-t / 0.008)
    x += np.random.randn(n) * np.exp(-t / 0.004) * 0.6
    out = bandpass(stereo(np.tanh(2 * x)), 700, 7000)
    return out * adsr(n, a=0.0005, r=0.01)[:, None] * gain * 0.7

HAT808 = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)   # the six 808 cymbal squares

def hat808(dur_steps=1, open_=False, gain=1.0, tone=1.0):
    """808 hat: six detuned squares through a highpass, noise for the sizzle"""
    n, t = steps(dur_steps if not open_ else max(dur_steps, 3))
    x = sum(square(f * tone, t) for f in HAT808) / 6 + np.random.randn(n) * 0.55
    dec = 0.24 if open_ else 0.026
    out = hp(stereo(np.tanh(1.4 * x)), 5800 if open_ else 7000)
    return out * (np.exp(-t / dec) * adsr(n, a=0.0004, r=0.01))[:, None] * gain * 0.55

def crash808(dur_steps=16, gain=1.0):
    """cymbal wash for the top of a drop"""
    n, t = steps(dur_steps)
    x = sum(square(f * 2.1, t) for f in HAT808) / 6 + np.random.randn(n) * 1.4
    out = hp(stereo(np.tanh(1.2 * x)), 3800)
    return widen(out, 1.3) * (np.exp(-t / 0.9) * adsr(n, a=0.001, r=0.15))[:, None] * gain * 0.34

def reverse_crash(dur_steps=8, gain=1.0):
    return np.ascontiguousarray(crash808(dur_steps, gain)[::-1])

# ---- 808 bass ----
def eight08(note, dur_steps, slide_from=None, glide=0.055, drive=2.4, gain=1.0,
            decay=0.75, click=True):
    """808 bass: a sine gliding into the note, saturated so it reads anywhere"""
    n, t = steps(dur_steps)
    f0 = midi(note)
    f = np.full(n, f0) if slide_from is None else f0 + (midi(slide_from) - f0) * np.exp(-t / glide)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.09 * np.sin(3 * ph)
    x = np.tanh(drive * x) / np.tanh(drive)
    if click:
        x = x + np.sin(4 * ph) * np.exp(-t / 0.009) * 0.35
    env = np.exp(-t / decay) * adsr(n, a=0.002, r=0.045)
    return norm(stereo(x * env), 0.92) * gain

def bass_drop(dur_steps=12, note=30, gain=1.0):
    """the hit that lands a drop: falling sub plus a noise blast"""
    n, t = steps(dur_steps)
    boom = subdrop(dur_steps, f0=midi(note) * 3.4, f1=midi(note), drive=1.9, decay=0.9)[:n]
    nz = np.random.randn(n)
    m = np.exp(-t / 0.35)[:, None]
    noise = (hp(stereo(nz), 2000) * m + lp(stereo(nz), 800) * (1 - m)) * np.exp(-t / 0.75)[:, None]
    return norm((boom + 0.45 * noise) * adsr(n, a=0.001, r=0.2)[:, None], 0.95) * gain

# ---- percussion and noise ----
def hat(dur_steps=0.6, open_=False, gain=1.0):
    """noise hi-hat / shaker tick"""
    n, t = steps(dur_steps)
    x = hp(stereo(np.random.randn(n)), 8000)
    return x * (np.exp(-t / (0.05 if open_ else 0.014)) * adsr(n, a=0.001, r=0.01))[:, None] * gain * 0.5

def crackle(dur_steps, gain=1.0):
    """vinyl atmosphere: soft hiss + sparse dust pops"""
    n, _ = steps(dur_steps)
    hiss = hp(lp(stereo(np.random.randn(n) * 0.35), 7500), 1800)
    pops = np.zeros(n)
    idx = np.random.randint(0, n, size=max(4, int(n / SR * 9)))
    pops[idx] = np.random.uniform(0.4, 1.0, len(idx)) * np.random.choice([-1, 1], len(idx))
    return (hiss * 0.5 + lp(stereo(pops), 4200)) * adsr(n, a=0.05, r=0.1)[:, None] * gain * 0.5

def wind(dur_steps, gain=1.0):
    """mountain wind: dark noise with a slow drifting swell"""
    n, t = steps(dur_steps)
    x = lp(stereo(np.random.randn(n)), 900)
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t + np.random.rand() * 6)
    return x * (swell * np.hanning(n))[:, None] * gain * 0.6

def grains(src, dur_steps=16, gain=1.0, density=34, size=(0.03, 0.13),
           pitch=(0.5, 2.0), seed=0, spreadw=1.0):
    """A granular cloud built from a segment the track already contains.
    Texture made of the record's own material sits in the mix by
    construction - it shares the harmonic series of whatever generated it,
    where a stock atmosphere sample has to be EQ'd into agreement."""
    n = int(dur_steps * STEP)
    rs = np.random.RandomState(seed)
    src = np.asarray(src, dtype=np.float32)
    out = np.zeros((n, 2), dtype=np.float32)
    for _ in range(int(density * dur_steps / 16 * 16)):
        gl = int(rs.uniform(*size) * SR)
        a = rs.randint(0, max(len(src) - gl - 1, 1))
        g = src[a:a + gl]
        if len(g) < 32:
            continue
        g = pitched(g, rs.uniform(*pitch))
        w = np.hanning(len(g))
        pos = rs.randint(0, max(n - len(g) - 1, 1))
        pan = 0.5 + 0.5 * spreadw * rs.uniform(-1, 1)
        e = min(pos + len(g), n)
        out[pos:e, 0] += g[:e - pos, 0] * w[:e - pos] * (1 - pan)
        out[pos:e, 1] += g[:e - pos, 1] * w[:e - pos] * pan
    return (hp(out, 260, 2) * gain * 0.5).astype(np.float32)


# ---- fx ----
def riser(dur_steps, gain=1.0, f0=180.0, f1=760.0):
    """build-up sweep: noise opening up + rising tone, quadratic swell"""
    n, t = steps(dur_steps)
    u = (t / t[-1])[:, None]
    noise = np.random.randn(n)
    x = (lp(stereo(noise), 400) * (1 - u) ** 2
         + lp(stereo(noise), 2500) * 2 * u * (1 - u)
         + hp(stereo(noise), 1200) * u ** 2)
    ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR
    x += 0.3 * stereo(np.sin(ph)) * u
    return x * (u ** 2) * gain * 0.55

def downlifter(dur_steps, gain=1.0, f0=1600.0, f1=60.0):
    """post-drop sweep down"""
    n, t = steps(dur_steps)
    u = t / t[-1]
    ph = 2 * np.pi * np.cumsum(f0 * (f1 / f0) ** u) / SR
    x = stereo(np.sin(ph) + 0.35 * np.sin(2 * ph)) + bandpass(stereo(np.random.randn(n)), 200, 3000) * 0.6
    return (widen(x, 1.5) * np.exp(-t / 0.6)[:, None] * gain * 0.4).astype(np.float32)

def whoosh(dur_steps, gain=1.0, rev_=False):
    """doppler pass-by: filtered noise sweeping across the head"""
    n, t = steps(dur_steps)
    u = t / t[-1]
    if rev_: u = u[::-1]
    nz = np.random.randn(n)
    x = (lp(stereo(nz), 500) * ((1 - u) ** 2)[:, None]
         + bandpass(stereo(nz), 700, 3500) * (2 * u * (1 - u))[:, None]
         + hp(stereo(nz), 3000) * (u ** 2)[:, None])
    p = np.linspace(-0.95, 0.95, n) * (-1 if rev_ else 1)
    a = (p + 1) * np.pi / 4
    x[:, 0] *= np.cos(a) * 1.41; x[:, 1] *= np.sin(a) * 1.41
    return (x * (np.sin(np.pi * (t / t[-1])) ** 1.2)[:, None] * gain * 0.45).astype(np.float32)

def impact(dur_steps=24, gain=1.0):
    """supernova: deep falling boom + noise blast darkening as it decays"""
    n, t = steps(dur_steps)
    f = 26 + (95 - 26) * np.exp(-t / 0.3)
    boom = np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 2.2)
    blast = np.random.randn(n)
    m = np.exp(-t / 0.5)[:, None]
    noise = (hp(stereo(blast), 1500) * m + lp(stereo(blast), 700) * (1 - m)) * np.exp(-t / 1.1)[:, None]
    out = stereo(boom) + 0.5 * noise
    return out * adsr(n, a=0.002, r=0.3)[:, None] * gain

def zap(dur_steps=2, f0=2400.0, f1=70.0, gain=1.0):
    """laser zap FX: fast exponential pitch fall"""
    n, t = steps(dur_steps)
    f = f1 + (f0 - f1) * np.exp(-t / 0.045)
    x = np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return stereo(x * np.exp(-t / 0.11) * adsr(n, a=0.001, r=0.02)) * gain * 0.7

def dubsiren(dur_steps, f0=650.0, lfo=3.0, gain=1.0, shape='tri'):
    """dub siren: sine swept by a triangle/square pitch LFO (feed to place_echo)"""
    n, t = steps(dur_steps)
    if shape == 'square':
        mod = np.sign(np.sin(2 * np.pi * lfo * t))
    else:
        mod = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * lfo * t))
    f = f0 * (1 + 0.35 * mod)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    out = stereo(np.tanh(1.3 * x))
    out[:, 1] = np.roll(out[:, 1], int(SR * 0.0009))
    return out * adsr(n, a=0.01, r=0.12)[:, None] * gain * 0.7

def airhorn(dur_steps=6, note=69, gain=1.0, wobble=6.0, drive=3.2, spread=1.0,
            bend=0.045):
    """The rave airhorn. A stack of fifths through three resonant bands, with
    the fast tremolo and the small pitch scoop at the start that make it read
    as an object being blown rather than a synth playing a note."""
    n, t = steps(dur_steps)
    f0 = midi(note)
    f = f0 * (1 - bend * np.exp(-t / 0.05)) * (1 + 0.010 * np.sin(2 * np.pi * wobble * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(a * saw_ph(ph * r, f0 * r) for r, a in ((1.0, 1.0), (1.5, 0.75), (2.0, 0.5)))
    air = np.stack([np.random.randn(n), np.random.randn(n)], 1) * 0.30
    st = np.tanh(drive * (stereo(x) + air * spread) / 2)     # air past the reed
    body = (1.6 * bandpass(st, 700, 1800) + 1.1 * bandpass(st, 1900, 3600)
            + 0.5 * bandpass(st, 3800, 7000))
    env = adsr(n, a=0.012, r=0.06) * (0.78 + 0.22 * _lfo01(t, wobble))
    return np.tanh(1.4 * body) * env[:, None] * gain * 0.55

def crowd(dur_steps=16, gain=1.0, roar=0.0, seed=0):
    """A room full of people: band-limited noise for the mass, a slow swell for
    its breathing, and whistles on top. `roar` lifts it from the murmur between
    two records to the noise a room makes when the drop lands."""
    n, t = steps(dur_steps)
    rs = np.random.RandomState(seed)
    nz = np.stack([rs.randn(n), rs.randn(n)], 1).astype(np.float32)   # two ears, two crowds
    voices = bandpass(nz, 300, 2600) + 0.35 * bandpass(nz, 2600, 7000)
    swell = 0.5 + 0.35 * _lfo01(t, 0.13) + 0.8 * roar
    whistle = np.zeros(n)
    for _ in range(2 + int(7 * roar)):
        k = rs.randint(0, max(n - 4000, 1))
        L = min(rs.randint(1500, 6000), n - k)
        tt = np.arange(L) / SR
        wf = rs.uniform(1900, 3400) * (1 + 0.05 * np.sin(2 * np.pi * 7 * tt))
        whistle[k:k + L] += np.sin(2 * np.pi * np.cumsum(wf) / SR) * np.hanning(L) * rs.uniform(0.2, 0.6)
    out = voices * swell[:, None] + 0.5 * bandpass(stereo(whistle), 1500, 5000)
    return np.tanh(1.2 * out) * adsr(n, a=0.08, r=0.25)[:, None] * gain * 0.28

# ---- the cabinet, as a real impulse response ----
_CAB_IR_CACHE = {}


def cab_ir(seed=0, size=0.10, low=70.0, high=4800.0, cone=1.0, presence=1.0):
    """A speaker is not an EQ curve.

    A tone control changes level per frequency and nothing else; a loudspeaker
    in a wooden box has a hundred milliseconds of behaviour after the signal
    stops - the cone's own resonance, the air in the cabinet, the reflections
    off the back panel, the breakup where the paper stops moving as one piece.
    Approximating that with a stack of fixed bandpass boosts gives a fixed
    pattern of peaks, and a fixed pattern of peaks on every note is a formant:
    the guitar ends up pronouncing a vowel.

    So build the response as something that happens over TIME - a direct hit
    followed by a dense, fast-decaying spray of reflections, with a slower low
    tail for the box - and only then give it the tone shape. Convolved, that
    has the same average spectrum as the filter stack and sounds nothing like
    it, because now the peaks ring instead of merely standing there."""
    key = (seed, size, low, high, cone, presence)
    if key in _CAB_IR_CACHE:
        return _CAB_IR_CACHE[key]
    rng = np.random.default_rng(seed + 1301)
    n = int(size * SR)
    t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    ir = np.zeros(n)
    ir[:4] = [1.0, 0.45, -0.18, 0.07]                  # the cone's first move
    ir += nz * np.exp(-t / 0.0038) * 0.85              # inside the box
    ir += lp(stereo(nz), 300, order=2)[:, 0] * np.exp(-t / 0.016) * 0.26  # the box
    ir += bandpass(stereo(nz), 300, 2000, order=2)[:, 0] * np.exp(-t / 0.009) * 1.9
    # Pad before filtering. `sosfiltfilt` extends the signal at both edges to
    # settle the filter, and an impulse response starts with a full-scale
    # discontinuity at sample zero - filtered as-is, that edge is smeared into
    # low-frequency junk that no amount of highpass order removes, because it
    # is being created by the padding rather than passed by the filter.
    pad = 512
    st = stereo(np.concatenate([np.zeros(pad), ir, np.zeros(pad)]))
    st = hp(lp(st, high, order=8), low, order=3)
    st = lp(st, high * 1.12, order=6)                   # speakers stop dead
    st = st + (0.95 * cone) * bandpass(st, 86, 155)    # cabinet resonance
    st = st + 0.12 * bandpass(st, 180, 380)            # the chest
    st = st - 0.52 * bandpass(st, 520, 1050)           # the boxy dip
    st = st + (0.30 * presence) * bandpass(st, 1600, 3200)
    ir = st[pad:pad + n, 0] * np.hanning(2 * n)[n:] ** 0.25   # no cliff at the end
    ir = ir / np.sqrt((ir ** 2).sum())
    _CAB_IR_CACHE[key] = ir.astype(np.float32)
    return _CAB_IR_CACHE[key]


def cab(x, seed=0, low=70.0, high=4800.0, cone=1.0, presence=1.0, tilt=0.0,
        mic=1.0):
    """Convolve with a cabinet, then put a microphone in front of it.

    Nobody has ever heard a guitar cabinet on a record - they have heard a
    dynamic microphone an inch from one, and the microphone is not neutral.
    The standard one has a presence peak of several dB between 4 and 6 kHz,
    which lands exactly where the speaker is falling away, and the sum of the
    two is the bite that a cab alone does not have. Leave the mic out and the
    guitar is correct and dull. `tilt` shelves the result for the rare case
    where a track needs the amp darker or brighter than the speaker is."""
    ir = cab_ir(seed, low=low, high=high, cone=cone, presence=presence)
    out = np.zeros_like(x)
    for c in range(2):
        out[:, c] = fftconvolve(x[:, c], ir)[:len(x)]
    if mic:
        out = out + mic * 0.75 * bandpass(out, 3000, 5400)   # the presence peak
        out = out + mic * 0.20 * bandpass(out, 120, 260)     # proximity effect
    if tilt:
        out = shelf(out, 1600, tilt, 'high')
    return out.astype(np.float32)


# ---- mix tools ----
def duck_env(n, hits, depth=0.35, hold=0.012, release=0.19, attack=0.0022):
    """sidechain curve: dip to `depth` on every registered kick, then recover.

    `attack` is not decoration. Dropping the gain from 1.0 to depth inside a
    single sample is a step discontinuity in the waveform - a click. Normally
    the kick that triggered it lands on top and masks it, so nobody hears it;
    the moment the kick is quiet or absent - an intro where the floor is still
    fading in, a ghost trigger keeping the pump alive through a breakdown -
    the click is the only thing left. 2 ms is still far faster than any
    compressor and costs the pump nothing."""
    env = np.ones(n, dtype=np.float32)
    if not hits:
        return env
    h, r = int(hold * SR), int(release * SR)
    a = max(int(attack * SR), 2)
    curve = np.concatenate([np.linspace(1.0, depth, a),
                            np.full(h, depth),
                            depth + (1 - depth) * (1 - np.exp(-np.linspace(0, 4, r)))]).astype(np.float32)
    for t in hits:
        t = int(t); e = min(t + len(curve), n)
        if t < n:
            np.minimum(env[t:e], curve[:e - t], out=env[t:e])
    return env

def accent_sag(pattern, n, depth=0.28, hold=0.006, dur=0.055, step=None):
    """The power supply giving way under an accent.

    A 303's accent is not a velocity. The accent circuit shares its supply
    with the filter, so an accented step momentarily starves the rest of the
    voice: the note hits harder and then everything sags for about 50 ms and
    climbs back. That dip is the "wow" nobody has ever managed to remove from
    an acid line, and a synth that only raises the level on an accent does
    not sound like one.

    Returns a per-sample gain of length `n`. `pattern` is the usual
    (step, note, dur, accent, slide) list; only the accent flag is read.
    """
    g = np.ones(n, dtype=np.float64)
    if not depth:
        return g
    sp = STEP if step is None else step
    h, d = int(hold * SR), max(int(dur * SR), 8)
    curve = np.concatenate([np.linspace(1.0, 1.0 - depth, max(h, 2)),
                            (1.0 - depth) + depth * (1 - np.exp(-np.linspace(0, 3.5, d)))])
    for ev in pattern:
        if not ev[3]:
            continue
        a = int(round(ev[0] * sp))
        e = min(a + len(curve), n)
        if a < n:
            np.minimum(g[a:e], curve[:e - a], out=g[a:e])
    return g

def softclip(x, ceiling=1.0, knee=0.65):
    """rounds off the peaks and leaves the body alone: everything under
    knee*ceiling passes untouched, the rest curves into the ceiling"""
    a = knee * ceiling
    y = np.abs(x)
    out = np.array(x, dtype=np.float32, copy=True)
    over = y > a
    out[over] = np.sign(x[over]) * (a + (ceiling - a) * np.tanh((y[over] - a) / (ceiling - a)))
    return out

def compress(x, thresh=0.30, ratio=4.0, attack=0.006, release=0.13,
             makeup=0.0, report=False, label='comp'):
    """A compressor, which is not a limiter and not a clipper.

    A clipper takes the top off the loudest samples; a limiter holds a
    ceiling. Neither makes a mix denser - they make it flatter. What raises
    the average without flattening the peaks is gain reduction that engages
    fast, holds, and recovers slowly, so the quiet part of every bar comes up
    to meet the loud part. Measure a finished record in this genre and it
    sits 3-4 dB above what clipping alone can reach at the same crest factor;
    the difference is this.

    Attack is a running minimum over the detector, so the reduction is fully
    engaged within the window rather than sliding in; release is a one-pole,
    so it lets go the way an analogue unit does."""
    det = np.maximum(np.abs(x[:, 0]), np.abs(x[:, 1]))
    det = uniform_filter1d(det, max(int(attack * SR), 1))
    g = np.ones_like(det)
    over = det > thresh
    g[over] = (thresh + (det[over] - thresh) / ratio) / det[over]
    # Attack is instant, release is a one-pole, and the elementwise minimum
    # is what makes it so: where the signal is getting louder the raw curve
    # wins, and where it is getting quieter the lagging one does. Smoothing
    # both directions instead turns a compressor into a slow AGC that pulls
    # the quiet parts down with the loud ones.
    a = np.exp(-1.0 / max(release * SR, 1.0))
    # Start the release filter AT the first gain value. Left at zero it opens
    # from silence over the release time, which mutes the first tenth of a
    # second of whatever it is put on.
    rel = lfilter([1 - a], [1, -a], g, zi=np.array([a * g[0]]))[0]
    g = np.minimum(g, rel).astype(np.float32)
    mk = 10 ** (makeup / 20)
    if report:
        print(f"  {label}: max {-20*np.log10(max(g.min(),1e-3)):.1f} dB, "
              f"mean {-20*np.log10(max(g.mean(),1e-6)):.2f} dB of gain reduction, "
              f"makeup {makeup:+.1f} dB")
    return (x * g[:, None] * mk).astype(np.float32)

def parallel_comp(x, blend=0.35, thresh=0.06, ratio=10.0, attack=0.0005,
                  release=0.09):
    """New York compression: a crushed copy under the dry one. The transients
    stay where they are and everything between them comes up."""
    y = compress(x, thresh, ratio, attack, release)
    y = y * (max(np.abs(x).max(), 1e-9) / max(np.abs(y).max(), 1e-9))
    return ((1 - blend) * x + blend * y).astype(np.float32)

def limiter(x, thresh=0.92, smooth=0.02, report=False):
    """smoothed peak limiter: the gain reduction is averaged, so it pulls, not clicks"""
    pk = np.maximum(np.abs(x[:, 0]), np.abs(x[:, 1]))
    g = np.minimum(1.0, thresh / np.maximum(pk, 1e-6))
    g = uniform_filter1d(g, max(int(smooth * SR), 3))
    if report:
        print(f"  limiter: max {-20*np.log10(max(g.min(),1e-6)):.1f} dB, "
              f"mean {-20*np.log10(g.mean()):.2f} dB of gain reduction")
    return (x * g[:, None]).astype(np.float32)

def brickwall(x, ceiling=0.985, gain=1.0, lookahead=0.0015, release=0.08,
              report=False):
    """A look-ahead limiter that actually holds the ceiling.

    `limiter()` above averages its gain curve, so a short peak is pulled at
    rather than stopped - it is a safety net, and asking it for loudness just
    turns it down. This one takes the minimum of the required gain over the
    look-ahead window, so the gain is already down before the transient
    arrives, and releases with a one-pole so it lets go the way a mastering
    limiter does. `gain` is the input push: this is where a master gets loud,
    and every dB of it is a dB of crest factor traded for density.

    A commercial neurofunk master measures a crest factor of 4-5 dB inside a
    drop and spends 65% of its time within 6 dB of the ceiling. That is not
    reachable with a clipper - a clipper only removes the sharpest tips - and
    it is not reachable with bus compression, which cannot tell a transient
    from a bar. It needs this.
    """
    y = np.asarray(x, dtype=np.float32) * gain
    # True peak, not sample peak. A clipper leaves square corners whose
    # reconstructed waveform overshoots by several dB between the samples -
    # both reference masters measure +3 to +4 dBTP for exactly this reason -
    # and that overshoot is what distorts in an MP3 encoder and in a DAC.
    # Detecting on a 4x upsample and holding the ceiling there costs about a
    # decibel of loudness and removes the overs.
    up = np.maximum(np.abs(resample_poly(y[:, 0], 4, 1)),
                    np.abs(resample_poly(y[:, 1], 4, 1)))
    m = (len(up) // 4) * 4
    pk = up[:m].reshape(-1, 4).max(axis=1)
    pk = np.pad(pk, (0, max(len(y) - len(pk), 0)), mode='edge')[:len(y)]
    pk = np.maximum(pk, np.maximum(np.abs(y[:, 0]), np.abs(y[:, 1])))
    g = np.minimum(1.0, ceiling / np.maximum(pk, 1e-9))
    la = max(int(lookahead * SR), 1)
    g = minimum_filter1d(g, la * 2 + 1)
    a = np.exp(-1.0 / max(release * SR, 1.0))
    rel = lfilter([1 - a], [1, -a], g, zi=np.array([a * g[0]]))[0]
    g = uniform_filter1d(np.minimum(g, rel), la)
    out = np.clip(y * g[:, None], -ceiling, ceiling)
    if report:
        print(f"  brickwall: +{20*np.log10(max(gain,1e-9)):.1f} dB in, "
              f"{-20*np.log10(max(g.min(),1e-6)):.1f} dB max / "
              f"{-20*np.log10(g.mean()):.2f} dB mean reduction")
    return out.astype(np.float32)

def _decay_max(x, tau):
    """A peak follower that falls at an exponential rate instead of tracking
    the signal down. Written blockwise because the closed form -
    a**n * cummax(x * a**-n) - overflows the moment n gets large, and a
    per-sample loop over ten million samples is not an option."""
    a = float(np.exp(-1.0 / max(tau * SR, 1.0)))
    blk = max(int(6 * tau * SR), 256)
    k = np.arange(blk, dtype=np.float64)
    dec, inv = a ** k, a ** (-k)
    out = np.empty(len(x), dtype=np.float64)
    carry = 0.0
    for i in range(0, len(x), blk):
        seg = np.asarray(x[i:i + blk], dtype=np.float64)
        m = len(seg)
        y = np.maximum(dec[:m] * np.maximum.accumulate(seg * inv[:m]), carry * dec[:m])
        out[i:i + m] = y
        carry = float(y[-1])
    return out


def squash(seg, thresh=0.28, ratio=6.0, attack=0.010, release=0.14, makeup=None,
           mix=1.0, report=None):
    """A compressor you are meant to hear.

    `limiter` exists to stop peaks and is designed to be invisible. This one
    is the opposite: a slow-ish attack lets every transient through at full
    height and then clamps the body behind it, and a release timed to the bar
    lets the gain climb back up before the next hit. That climb is the pump -
    it is not a side effect of the compression, it is the instrument. Set the
    release near a 16th and the whole mix breathes in time.

    Gain reduction is shared across both channels, so the stereo image does
    not wander. `mix` < 1 blends the compressed copy back under the dry one -
    parallel compression, which raises the quiet detail without flattening
    the attacks at all."""
    det = np.maximum(np.abs(seg[:, 0]), np.abs(seg[:, 1]))
    env = _decay_max(det, release)
    over = np.maximum(env / max(thresh, 1e-6), 1.0)
    g = over ** (1.0 / ratio - 1.0)
    g = uniform_filter1d(g, max(int(attack * SR), 3))
    if makeup is None:
        # what a full-scale peak loses, given back - so the fader does not move
        makeup = (1.0 / max(thresh, 1e-6)) ** (1.0 - 1.0 / ratio)
    out = (seg * (g * makeup)[:, None]).astype(np.float32)
    if report:
        gr = -20 * np.log10(np.maximum(g, 1e-6))
        print(f"  squash[{report}]: {gr.max():.1f} dB max, {gr.mean():.1f} dB mean "
              f"gain reduction, pumping {1000*release:.0f} ms "
              f"({release*BPM/60*4:.2f} of a beat)")
    return (out * mix + seg * (1 - mix)).astype(np.float32)


def bus_reverb(buf, decay=2.0, wet=0.25, tone=4000, block_bars=24):
    """Reverb across a whole bus, one block at a time (overlap-add), so a
    six-minute buffer never asks for a six-minute FFT. One shared space that
    several parts are sent into is what makes them sound like they are in the
    same room; a separate reverb per voice makes a collage."""
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


def _line_envs(pattern, n, decay, cut_decay, acc_amt, hold, glide_ms, slide_tau,
               release=0.006, cut_smooth=0.004):
    """Per-sample frequency, amplitude and cutoff for a whole bar.

    The frequency track is forward-filled through every gap, so the
    oscillator that renders it never sees a jump to zero and never restarts.
    Note changes are smoothed by `glide_ms`; a note flagged `slide` gets a
    real exponential approach from the previous pitch instead.

    A note whose amplitude envelope simply stops is a click. With a 240 ms
    decay a one-step note at 142 BPM is still at 64% of its level when its
    span ends, and `amp` outside that span is zero - so the waveform steps
    from 0.64 to 0 in a single sample, on most notes, for the length of the
    record. `release` fades it out instead; 6 ms is far shorter than any
    note and removes the step completely. `cut_smooth` does the same job
    for the filter envelope, where a step swaps the filter bank
    mid-waveform - audible as a tick at the top of the spectrum.
    """
    fs = np.zeros(n)
    amp = np.zeros(n)
    cut = np.zeros(n)
    prev = None
    for ev in pattern:
        st, note, dur, acc, slide = ev[:5]
        vel = ev[5] if len(ev) > 5 else 1.0
        a = int(round(st * STEP))
        b = min(int(round((st + dur) * STEP)), n)
        if a >= n or b <= a:
            continue
        m = b - a
        tt = np.arange(m) / SR
        f = midi(note)
        if slide and prev is not None:
            fs[a:b] = f + (prev - f) * np.exp(-tt / slide_tau)
        else:
            fs[a:b] = f
        lvl = vel * (1.0 + (acc_amt if acc else 0.0))
        e = (np.minimum(tt / 0.0022, 1.0)
             * (hold + (1 - hold) * np.exp(-tt / (decay * (0.82 if acc else 1.0)))))
        np.maximum(amp[a:b], lvl * e, out=amp[a:b])
        rn = int(release * SR)
        if rn and b < n:
            rb = min(b + rn, n)
            np.maximum(amp[b:rb], (lvl * e[-1]) * np.linspace(1, 0, rb - b),
                       out=amp[b:rb])
        c = (0.58 + (0.42 if acc else 0.0)) * np.exp(-tt / (cut_decay * (1.7 if acc else 1.0)))
        np.maximum(cut[a:b], c, out=cut[a:b])
        prev = f
    if pattern:
        fs[0] = fs[0] or midi(pattern[0][1])
    else:
        fs[0] = 100.0
    idx = np.maximum.accumulate(np.where(fs > 0, np.arange(n), 0))   # hold, never zero
    fs = fs[idx]
    k = max(int(glide_ms / 1000.0 * SR), 3)
    fs = uniform_filter1d(fs, k)          # micro-portamento; also kills the step
    if cut_smooth:
        cut = uniform_filter1d(cut, max(int(cut_smooth * SR), 3))
    return fs, amp, cut


def line(pattern, dur_bars=1, wave='saw', detune=0.010, f_lo=150.0, f_hi=3400.0,
         res=2.2, decay=0.13, cut_decay=0.065, hold=0.0, acc_amt=0.5,
         drive=2.0, glide_ms=2.5, slide_tau=0.05, base=0.05, bands=9,
         sub=0.0, sub_lp=115.0, low=0.0, gain=1.0, spread=0.0, tail_steps=1.5,
         vib=None):
    """A whole bar of a monophonic voice as ONE continuous oscillator.

    pattern: [(step, note, dur_steps, accent, slide[, velocity]), ...]

    `sub` mixes in a clean sine on the same phase, lowpassed and kept dead
    centre - the multiband split every bass patch in this genre is built on:
    the bottom stays a pure tone, the top gets the filter and the drive.
    `hold` is what separates a bass from a pad: 0 lets every note decay into
    a gap (the roll), 1 holds it flat until the next one.

    The buffer runs `tail_steps` past the bar so the last note's decay
    finishes into the next one instead of being cut at the bar line - a fade
    every 1.9 seconds is a pulse the ear finds immediately."""
    n = int(round(dur_bars * BAR + tail_steps * STEP))
    fs, amp, cut = _line_envs(pattern, n, decay, cut_decay, acc_amt, hold,
                              glide_ms, slide_tau)
    if vib:
        # cents, Hz, and the delay before it arrives. A lead that starts
        # vibrating on the attack sounds like a synthesiser; one that starts
        # straight and warms up after a third of a second sounds played.
        cents, vhz, vdel = vib
        tt = np.arange(n) / SR
        amt = np.clip((tt - vdel) / max(vdel, 0.05), 0, 1)
        fs = fs * (2 ** (cents / 1200.0 * amt * np.sin(2 * np.pi * vhz * tt)))
    ph = 2 * np.pi * np.cumsum(fs) / SR
    top = float(fs.max())
    if wave == 'square':
        x = (2 / np.pi) * sum(np.sin(k * ph) / k for k in range(1, 42, 2)) * 2
    elif wave == 'tri':
        x = (8 / np.pi ** 2) * sum((-1) ** ((k - 1) // 2) * np.sin(k * ph) / k ** 2
                                   for k in range(1, 24, 2))
    else:
        x = saw_ph(ph, top, kmax=64)
        if detune:
            x = 0.5 * x + 0.5 * saw_ph(ph * (1 + detune), top * (1 + detune), kmax=64)
    st = stereo(x * amp)
    out = morph_lp(st, f_lo, f_hi, base + (1 - base) * cut, bands=bands, res=res)
    out = np.tanh(drive * out / (1 + res * 0.42))
    if low:
        out = hp(out, low, order=4)
    if spread:
        out[:, 1] = np.roll(out[:, 1], int(SR * spread / 1000.0))
    if sub:
        s = lp(stereo(np.sin(ph) * amp), sub_lp, order=4)
        out = out + sub * s
    return fade_edges(out.astype(np.float32), 2.0) * gain * 0.7


@cached
def _line_cached(key, dur_bars, **kw):
    return line(list(key), dur_bars, **kw)


def cached_line(pattern, dur_bars=1, **kw):
    """`line` with the bar cached. The same bar plays dozens of times, and
    every knob position is part of the cache key - so a line whose filter is
    being swept across a section is a sequence of distinct cached bars
    rather than one bar repeated, and costs one render each."""
    return _line_cached(tuple(tuple(p) for p in pattern), dur_bars, **kw)


# ---- sequencer ----
class Session:
    """Mixes on named buses. Buses listed in DUCKED are sidechained against
    every kick registered with hit(); everything else passes through."""
    DUCKED = {'bass': 1.0, 'music': 0.7, 'pad': 0.85}

    def __init__(self, nbars, tail=1.5):
        self.total = int(round(nbars * BAR)) + int(SR * tail)
        self.bus = {}
        self.hits = []

    def _buf(self, name):
        if name not in self.bus:
            self.bus[name] = np.zeros((self.total, 2), dtype=np.float32)
        return self.bus[name]

    def place(self, t, seg, gain=1.0, bus='main'):
        # A humanised event can be nudged before bar 0; trim it rather than
        # letting a negative index wrap and write to the end of the track.
        t = int(t)
        a = max(t, 0)
        e = min(t + len(seg), self.total)
        if a < self.total and e > a:
            self._buf(bus)[a:e] += seg[a - t:e - t] * gain

    def hit(self, t):
        """register a sidechain trigger (a kick) at t"""
        self.hits.append(int(t))

    def pos(self, b, s=0.0): return int(round(b * BAR + s * STEP))

    def pat(self, b, events, bus='main'):
        """events: (step, segment[, gain])"""
        for ev in events:
            g = ev[2] if len(ev) > 2 else 1.0
            self.place(self.pos(b, ev[0]), ev[1], g, bus)

    def place_echo(self, t, seg, gain=1.0, times=3, delay_steps=3.0, fb=0.5, bus='main'):
        """place seg plus decaying dub echoes"""
        for i in range(times + 1):
            self.place(t + int(i * delay_steps * STEP), seg, gain * fb ** i, bus)

    def loudness(self, buf, window=0.3, pct=90):
        """Short-term RMS at the `pct`th percentile, in dB.

        Whole-track RMS is the wrong number for balancing anything
        percussive. A 16th-note clav part is silent between its events, so
        its mean level says it is 25 dB under the bass while the ear puts it
        6 dB under - and a mix balanced on that number buries every
        transient instrument on the record. A 300 ms window is roughly the
        ear's own integration time, and the 90th percentile asks how loud
        the part is WHEN IT PLAYS rather than on average over four minutes,
        which is the question a fader actually answers."""
        m = buf.mean(axis=1).astype(np.float64)
        w = max(int(window * SR), 64)
        e = uniform_filter1d(m ** 2, w)[::w // 4]
        v = float(np.percentile(np.sqrt(np.maximum(e, 0)), pct))
        return 20 * np.log10(max(v, 1e-9))

    def report(self, gains=None):
        """what each bus is contributing - level, punch, and where it sits"""
        bands = [(20, 60), (60, 200), (200, 800), (800, 3000), (3000, 10000), (10000, 20000)]
        print(f"{'bus':8s} {'loud':>6s} {'rms':>7s} {'peak':>6s} {'crest':>6s} {'side%':>6s} |"
              + "".join(f"{a//1:>7d}" for a, _ in bands))
        for name in sorted(self.bus):
            b = self.bus[name] * (gains or {}).get(name, 1.0)
            m = b.mean(axis=1)
            r = float(np.sqrt((m ** 2).mean())) or 1e-9
            spec = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
            f = np.fft.rfftfreq(len(m), 1 / SR)
            sh = [spec[(f >= lo) & (f < hi)].sum() / max(spec.sum(), 1e-9) * 100 for lo, hi in bands]
            side = float(np.sqrt(((b[:, 0] - b[:, 1]) ** 2).mean())) / r * 100
            print(f"{name:8s} {self.loudness(b):6.1f} {r:7.3f} {np.abs(m).max():6.3f} "
                  f"{np.abs(m).max()/r:6.2f} {side:6.0f} |"
                  + "".join(f"{v:7.1f}" for v in sh))

    def ownership(self, lo=3000, hi=16000, gains=None, label=None):
        """Which bus owns a band, as a percentage of the total energy in it.

        `report()` says where each bus's OWN energy sits, which cannot answer
        the question that matters about a top end: not "is this bus bright"
        but "what is the listener hearing up there". A ride that is 60% of
        its own spectrum and 3% of the mix is fine; one that is 20% of its
        own spectrum and 60% of the mix is the thing that hurts after ninety
        seconds.

        A sustained source above about 20% of 3-16 kHz is a noise bed. The
        fix is the voice - shorter decay, less noise, lower level - not a
        shelf on the bus.
        """
        tot, per = 0.0, {}
        for name, buf in self.bus.items():
            m = buf.mean(axis=1) * (gains or {}).get(name, 1.0)
            e = float((bandpass(np.stack([m, m], 1), lo, hi)[:, 0] ** 2).mean())
            per[name] = e
            tot += e
        print(f"  {label or f'{lo}-{hi} Hz'} ownership: " + "  ".join(
            f"{k} {100 * v / max(tot, 1e-12):.0f}%"
            for k, v in sorted(per.items(), key=lambda kv: -kv[1]) if v / max(tot, 1e-12) > 0.005))
        return {k: v / max(tot, 1e-12) for k, v in per.items()}

    def mixdown(self, drive=1.2, duck=0.34, limit=0.0, peak=0.94, gains=None,
                clip=0.0, duck_rel=0.19, comp=None, brick=None):
        env = duck_env(self.total, self.hits, depth=duck, release=duck_rel)
        mix = np.zeros((self.total, 2), dtype=np.float32)
        for name, buf in self.bus.items():
            g = (gains or {}).get(name, 1.0)
            if name in self.DUCKED and self.hits:
                buf = buf * (1 - (1 - env) * self.DUCKED[name])[:, None]
            mix += buf * g
        mix = hp(mix, 25)
        if clip:
            # Shave the sharpest transients before the saturator sees them.
            # A clipper takes 1-2 dB off the very tip of a kick, where the ear
            # is masked anyway, and leaves the body alone - which is exactly
            # what a wide tanh does not do.
            before = float(np.abs(mix).max())
            touched = float((np.abs(mix).max(axis=1) > 0.8 * clip).mean()) * 100
            mix = softclip(mix, clip, knee=0.8)
            print(f"  clipper: {before:.2f} -> {float(np.abs(mix).max()):.2f} peak, "
                  f"{touched:.2f}% of samples shaped "
                  f"({'transients only' if touched < 2 else 'THIS IS EATING THE BODY'})")
        if comp:
            mix = compress(mix, report=True, label='glue', **comp)
        pk = float(np.abs(mix).max())
        if drive:
            mix = np.tanh(drive * mix) / np.tanh(drive)
            after = float(np.abs(mix).max())
            print(f"  saturation: bus sum peaks {pk:.2f} -> {after:.2f} "
                  f"({20*np.log10(max(after,1e-9)/max(pk,1e-9)):+.1f} dB). "
                  f"More than about -1 dB here and the tanh is distorting every "
                  f"transient, not gluing the mix.")
        if limit:
            mix = limiter(mix, limit, report=True)
        if brick:
            mix = brickwall(mix, report=True, **brick)
            return mix * min(peak / max(np.abs(mix).max(), 1e-9), 1.0)
        return mix * (peak / max(np.abs(mix).max(), 1e-9))

    def render(self, filename, drive=1.2, duck=0.34, limit=0.0, peak=0.94,
               fade=1.2, gains=None, clip=0.0, duck_rel=0.19, comp=None,
               brick=None):
        m = self.mixdown(drive, duck, limit, peak, gains, clip, duck_rel, comp,
                         brick)
        fi = int(0.01 * SR); m[:fi] *= np.linspace(0, 1, fi)[:, None]
        fo = int(fade * SR); m[-fo:] *= np.linspace(1, 0, fo)[:, None]
        os.makedirs(RENDERS, exist_ok=True)
        path = os.path.join(RENDERS, filename)
        save(path, m)
        print(f"{filename}: {self.total/SR:.2f}s rms={np.sqrt((m**2).mean()):.3f}")
        return path
