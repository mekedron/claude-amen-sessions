`verify.clicks()` lowpasses at 2 kHz before it looks for a discontinuity,
because a transient IS a big jump between two samples and a detector that
does not band-limit finds every kick and every hat. That works. What it does
not survive is a **sawtooth in the bass**.

On `glavnaya_scena` the detector reported twenty steps, clustered in the intro
and the outro - exactly the sparse sections where a click would be audible -
at 15-23x the local slope. Both the rolling bass and the kick tripped it. The
test that settled it took one line: render a **bare, continuous, ungated,
un-enveloped** band-limited saw at 92 Hz and hand it to the same detector.

    a bare 92 Hz saw, nothing gated      4 hits, 15-16x, step 0.080
    the same phase as a sine             none

Nothing was cut, so nothing was a click. A band-limited saw whose partials
reach 3.2 kHz reconstructs its own reset edge over about fourteen samples, and
that edge is still 0.08 per sample after a 2 kHz lowpass - twelve times what a
92 Hz sine does. The detector is measuring the waveform.

**How to apply:** when the detector fires on a part built from saws, do not
start smoothing envelopes. Measure the ENVELOPE instead, which is what
`note-envelopes-need-a-release` is really about:

    env = uniform_filter1d(np.abs(x.mean(1)), 220)
    print(np.abs(np.diff(env)).max() / env.max())

Under about 2% of the peak is a decay. Near the peak is a cut. The rolling
bass measured 0.7% and the kick 0.9%, and both were correct.

The same reasoning covers a square, a pulse and any hard-synced oscillator.
It does NOT cover a sine, a filtered pad or anything whose spectrum stops
below a couple of kilohertz - there, the detector is telling the truth and
something really is being switched off.

Related: [[note-envelopes-need-a-release]], [[a-repeated-hit-must-not-be-identical]]
