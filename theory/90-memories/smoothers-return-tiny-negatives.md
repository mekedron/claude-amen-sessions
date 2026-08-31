---
name: smoothers-return-tiny-negatives
description: uniform_filter1d returns values around -1e-14 over a zero region, and a fractional power of that is a NaN that spreads silently through an entire bus
type: pitfall
date: 2026-09-01
---

`scipy.ndimage.uniform_filter1d` is a running-sum box filter, so over a
stretch of exact zeros it returns values of order `-1e-14` rather than zero.
Every envelope in this engine is smoothed with it, and any envelope then
raised to a **fractional** power - `amp ** 1.6`, `amp ** 0.8`, common wherever
brightness is meant to follow the blow - becomes `NaN` at those samples.

Clamping the input does not help. The negatives are created *by* the filter:

    amp = np.maximum(uniform_filter1d(x, w), 0.0)     # clamp AFTER, not before

**Why it is worth a memory rather than a bug fix:** the failure is silent and
total. One NaN sample propagates through every subsequent filter, so a single
horn note poisons the whole horns bus; `Session.report` then prints `nan` for
that bus, `mixdown` prints `nan` for the clipper and the saturator, and the
rendered wav is a file of zeros with no error raised anywhere. Nothing in the
chain complains, and the numpy warning that does appear points at the power
operation rather than at the smoother that caused it.

**How to apply:** clamp after every smoothing pass whose output feeds a
fractional power, and when a bus reports `nan`, look for `** <non-integer>`
before looking anywhere else. `np.seterr(all='raise')` plus a traceback finds
it in one run.
