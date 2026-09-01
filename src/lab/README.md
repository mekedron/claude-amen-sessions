# `src/lab` — the bench

A composer who cannot hear has to measure. `verify.py` measures a finished
WAV on disk; **this folder measures the things you are still holding** — one
voice, one bus, one bar, one section — while you are building them.

## This folder is optional, and it is yours

Nothing in `core.py`, `sampler.py`, any genre module or any track imports it.
**Delete the whole directory and every record in this repository still
renders.** It carries no state and no opinions that the engine depends on.

So: change it. The thresholds in here — *"worse than −30 dB aliasing is
audible"*, *"a peak belongs at 60–90% of the way through"*, *"a section curve
under 4 dB is flat"* — are the numbers that happened to be right for the
problems they came from. They are starting points, not laws. Move them when
they are wrong, and say in a comment why.

**And nobody has to use these at all.** If you are working on something these
tools do not fit — a sampler question, a groove question, a question about
whether two parts are stepping on each other in time rather than in
frequency — write your own. Put it here if it belongs here, put it somewhere
else if it does not, or keep it inline if it is a one-off. New files are
welcome and so are new folders. The only thing worth preserving is the habit:

> Hear a problem → find it once by hand → leave the finding behind as
> something that can never be missed by hand again.

Every function here exists because a human said *"there is a crackle"* or
*"the kicks are dull"* and this was the measurement that turned the sentence
into a number. That is the whole idea, and the list below is just where it
had got to on one particular night.

## What is here now

### `spectrum.py` — where the energy is

| | |
|---|---|
| `shares(seg)` | percentage of a segment's energy per band. The most-used measurement there is: it is how you find out a "bass" is a low-mid, or that a "bright" hat lives in the ice-pick band |
| `width(seg)` | side energy as a percentage of mid. ~0 mono, 100 wide, past 200 the channels are nearly uncorrelated and will lose level when summed |
| `band_table([(label, seg), ...])` | several segments side by side. Numbers only mean something next to other numbers — use it to compare a new voice against the one it replaces |
| `sections(x, bpm, marks)` | the arrangement, measured: loudness, width and bands per named section, then whether the curve rises, whether the minimum precedes the maximum, and where the peak sits |
| `walk(x, bpm, a, b)` | bar by bar, so a jump can be **located** instead of guessed at |

### `voices.py` — one voice, before it reaches a mix

| | |
|---|---|
| `edges(seg)` | does it start and end at zero, and does it step anywhere after its attack? Unfaded edges and envelopes that stop instead of fading are clicks |
| `varies(fn, seeds)` | does a seeded voice actually differ per seed? A short bright sound that repeats *exactly* stops being an instrument and becomes a tick |
| `alias_error(render, ...)` | render the same voice at several rates against an oversampled reference. The only honest aliasing test — a spectrum tells you nothing about anything with a pitch sweep in it |
| `envelope_steps(env)` | the largest jump in a control signal, against its own range |

### Also worth knowing about, living elsewhere

- `Session.ownership(lo, hi, gains)` in `core.py` — **which bus** owns a band,
  as a share of the whole mix. `report()` says where each bus's own energy
  sits, which cannot answer the question that matters about a top end: not
  "is this bus bright" but "what is the listener standing under".
- `verify.clicks(x, bpm)` — discontinuities, band-limited so that transients
  do not drown the signal.
- `verify.ticks(x, bpm)` — crackle. Separates a fault from a part by **grid
  lock**: nine ticks a second at 142 BPM is a hi-hat line if their phases
  agree and dust if they do not.

## Using it

```python
import sys; sys.path.insert(0, 'src')
from lab import *
import verify

band_table([('old', hat909(2.2, open_=True)), ('new', openhat(3.4))])
sections(verify._read('renders/track.wav'), 142,
         [('INTRO', 0, 16), ('DROP', 16, 48), ('BREAK', 48, 64)])
walk(verify._read('renders/track.wav'), 142, 0, 14)
edges(techkick(), 'kick')
varies(lambda s: techkick(cseed=s), label='kick click')
```

`alias_error` needs a function that can build the same voice at any sample
rate, which most voices cannot do as written — write the two or three lines
inline for the layer under suspicion:

```python
def grit(sr):
    t = np.arange(int(0.05 * sr)) / sr
    f = 38.89 * (1 + 3.2 * np.exp(-t / 0.019))
    ph = 2 * np.pi * np.cumsum(f) / sr
    return fold(np.tanh(6 * saw_ph(ph, 38.89 * 11 * 4.2, nyq=sr * 0.45)), 1.0)

alias_error(grit, label='the kick grit')      # 1x: -21 dB.  4x: -34 dB.
```
