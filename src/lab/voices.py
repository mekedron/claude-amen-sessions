"""Tests for ONE voice, before it ever reaches a mix.

Everything here came out of a real bug that a human heard and the engine
could not see. They are cheap - a few hundred milliseconds of audio - and
each answers one question that no amount of listening to a finished track
will answer cleanly, because in a finished track everything is masked by
everything else.

NOTHING HERE IS FIXED. The thresholds are the ones that happened to be right
in the sessions they came from; move them, and add whatever the next problem
needs. A tool that has never been edited is usually a tool nobody used.
"""
import numpy as np
from scipy.signal import resample_poly

SR = 44100


def _mono(x):
    x = np.asarray(x, dtype=np.float64)
    return x.mean(axis=1) if x.ndim == 2 else x


def edges(seg, label='', quiet_at=0.01, attack_ms=20.0, thresh=25.0):
    """Does this segment start and end at zero, and does it step anywhere?

    An unfaded edge is a click, and so is an envelope that stops instead of
    fading. `core._line_envs` used to end every note at 64% of its level and
    the next sample was zero - a click on most notes of every line the engine
    rendered, inaudible under a loud kick and naked the moment the same
    renderer was put in the bass.

    `worst` is the largest single-sample jump. Compare it to the segment's
    own peak: anything of the same order is a cut, not a decay.

    A big jump inside the first `attack_ms` is NOT reported, because that is
    what a transient is. A kick's click layer is a 1.6 ms noise burst and
    moves half of full scale between two samples on purpose; a detector that
    calls that a defect is describing percussion, not finding a bug. The
    same mistake cost an hour in the session this came from.
    """
    m = _mono(seg)
    d = np.abs(np.diff(m))
    i = int(np.argmax(d)) if len(d) else 0
    pk = float(np.abs(m).max()) if len(m) else 0.0
    bad = []
    if abs(m[0]) > quiet_at * max(pk, 1e-9):
        bad.append('starts loud')
    if abs(m[-1]) > quiet_at * max(pk, 1e-9):
        bad.append('ends loud')
    # Against the LOCAL slope, not the peak. White noise moves half its own
    # peak between two samples all day, so a threshold on absolute step size
    # calls every hat and every noise burst a defect. A real discontinuity is
    # a jump that its own neighbourhood was not making.
    a = int(attack_ms / 1000.0 * SR)
    ratio, at = 0.0, 0
    if len(d) > a + 64:
        w = max(int(0.010 * SR), 9)
        ref = np.convolve(d, np.ones(w) / w, mode='same') + 1e-9
        r = d[a:] / ref[a:]
        j = int(np.argmax(r))
        ratio, at = float(r[j]), a + j
        if ratio > thresh:
            bad.append(f'steps {ratio:.0f}x the local slope at '
                       f'{at / SR * 1000:.0f} ms')
    print(f"  edges {label:20s} start {abs(m[0]):.5f}  end {abs(m[-1]):.5f}  "
          f"worst post-attack step {ratio:5.1f}x local at {at / SR * 1000:6.1f} ms "
          f"(peak {pk:.3f})" + ("   <- " + ", ".join(bad) if bad else "   ok"))
    return ratio


def varies(fn, seeds=(1, 2, 3), label=''):
    """Does a seeded voice actually produce different audio per seed?

    Three separate voices in this engine drew their noise from a hard-coded
    RandomState, so every kick click and every hat in a six-minute record was
    bit-identical. A short bright sound that repeats EXACTLY stops being heard
    as an instrument and starts being heard as a tick - which is what a
    metronome is. `fn` takes a seed and returns a segment.
    """
    segs = [_mono(fn(s)) for s in seeds]
    n = min(len(s) for s in segs)
    diffs = [float(np.abs(segs[i][:n] - segs[i + 1][:n]).max())
             for i in range(len(segs) - 1)]
    worst = min(diffs) if diffs else 0.0
    print(f"  varies {label:19s} smallest difference between seeds {worst:.4f}"
          + ("   <- IDENTICAL, this will read as a tick" if worst < 1e-6 else "   ok"))
    return worst


def alias_error(render, rates=(1, 2, 4), ref=8, label=''):
    """How much of a voice is frequencies that should not exist.

    `render(sr)` must build the SAME voice at the sample rate it is handed
    and return mono. Everything is decimated back to 44.1 kHz and compared
    against the `ref`-times-oversampled version; the difference is aliasing
    and nothing else.

    This is the only honest test. Looking at the spectrum does not work for
    anything with a pitch sweep in it - a swept tone is smeared across
    frequencies by construction, and a naive "is this energy on a harmonic"
    test called a clean layer 51% inharmonic. The real answer for the same
    layer, measured this way, was -21 dB of error at 1x: 9% of a kick's
    attack arriving as fizz, on every kick in six records.

    Rule of thumb: worse than about -30 dB and it is audible on a transient.
    Any waveshaper on a swept source needs 4x.
    """
    def at(sr):
        y = np.asarray(render(sr), dtype=np.float64)
        if sr != SR:
            y = resample_poly(y, 1, sr // SR)
        return y
    r = at(SR * ref)
    print(f"  aliasing {label}" + (":" if label else ""))
    out = {}
    for k in rates:
        y = at(SR * k)
        m = min(len(y), len(r))
        err = y[:m] - r[:m]
        db = 20 * np.log10(max(np.sqrt((err ** 2).mean()), 1e-12)
                           / max(np.sqrt((r[:m] ** 2).mean()), 1e-12))
        out[k] = float(db)
        print(f"    at {k}x: {db:+6.1f} dB against a {ref}x reference"
              + ("   <- audible" if db > -30 else ""))
    return out


def envelope_steps(env, label='', name='envelope'):
    """The largest single-sample jump in a control signal.

    An amplitude or cutoff envelope that ends by stopping is a click, and a
    stepped cutoff swaps filters mid-waveform, which is a tick at the top of
    the spectrum. Compare the number to the envelope's own range.
    """
    e = np.asarray(env, dtype=np.float64).ravel()
    d = np.abs(np.diff(e))
    rng = float(e.max() - e.min()) if len(e) else 0.0
    worst = float(d.max()) if len(d) else 0.0
    print(f"  {name} {label:18s} worst step {worst:.4f} over a range of {rng:.4f}"
          + ("   <- a cut, not a decay" if rng and worst > 0.25 * rng else "   ok"))
    return worst
