---
name: additive-stacks-clip-into-squares
description: A summed partial stack peaks near the sum of its amplitudes, so a tanh sized for a single oscillator hard-clips it and deletes its even harmonics
type: pitfall
date: 2026-09-01
---

Any voice built by **summing partials** - an additive low end, a modal bell, a
drawbar organ, a formant stack - has a peak near the SUM of its amplitudes, not
near one. Six partials at `(1.00, 0.70, 0.99, 0.50, 0.48, 0.38)` peak at about
4.05. Handing that to `np.tanh(1.15 * x)` is not saturation: it is
`tanh(4.66) = 0.9998` for most of the waveform, which is a hard clip into a
near-square.

**And a square has no even harmonics at all**, so the second partial the stack
existed to supply is the first thing destroyed. On `tvar` the sub was built
from partials measured off a reference sample - h2 deliberately only 3 dB under
h1 - and it came out **10 dB** under, leaving a hole in 60-120 Hz that three
rounds of EQ could not fill because the energy was never generated.

The failure is silent. Nothing errors, the level looks right because `tanh` is
bounded, and the spectrum looks plausible because the odd partials survive.

**How to apply:** normalise before every non-linearity, by the sum of the
amplitudes for a coherent stack (partials that share a phase) and by
`sqrt(sum of squares)` for uncorrelated ones:

    sb = sum(g * np.sin(k * ph) for k, g in enumerate(SUBP, 1)) / sum(SUBP)
    x  = np.tanh(1.30 * sb)

`core.drive_asym` says the same thing in its docstring for the same reason.
The rule is wider than that one function: it applies to `tanh`, `fold`,
`softclip` and `bitcrush` alike, and it is why a stack that measured correct
partial by partial can still measure wrong once assembled.

Related: [[bass-must-keep-its-own-fundamental]], [[struck-metal-needs-modes-not-squares]]
