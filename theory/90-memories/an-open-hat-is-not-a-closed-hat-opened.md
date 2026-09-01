---
name: an-open-hat-is-not-a-closed-hat-opened
description: hat909 with open_=True is a 200 ms noise burst centred in the 3-6 kHz ice-pick band; the user hears it as a crackle, and the fix is a different instrument
type: pitfall
date: 2026-09-01
---

The user found this one himself: *"может быть, это и есть открытый хэт. Просто
он такой высокий и короткий, что он звучит как треск."*

He was right, and it measures. `hat909(open_=True)` is band-passed white noise
under a single exponential decay:

| | `hat909` open, as used | `openhat` |
|---|---|---|
| 800-3000 Hz | 30.3% | 0.2% |
| **3000-6000 Hz** | **64.3%** | 12.7% |
| 6000-12000 Hz | 5.4% | 39.1% |
| 12-20 kHz | 0.0% | 40.2% |
| decay to -26 dB | 273 ms | 398 ms |
| two hits differ by | **0.000** | 0.555 |

Two thirds of its energy sat in **3-6 kHz**, which is the band a bright short
sound is an ice-pick in rather than air, and it was over in a quarter of a
second. That is a rattle. As a CLOSED hat the same function is correct - a
28 ms noise tick is what a closed hat is - so the mistake was assuming an
open hat is the same instrument with a longer envelope.

An open hat needs three things noise under one envelope cannot give:

1. **Metal.** A hi-hat is two discs. `openhat` uses the 808's six inharmonic
   square ratios (1, 1.342, 1.612, 1.996, 2.441, 2.786) for the pitched part
   and noise only for the sizzle.
2. **More than one decay.** Real metal sheds its top first, so the sound
   changes colour while it rings. One envelope across all frequencies is a
   sample being faded out.
3. **Height.** Highpass at 4.8-5.5 kHz, not 1.6. Everything a hat is supposed
   to contribute is above 6 kHz.

**How to apply:** `industriallib.openhat()` is that instrument; `hat909` stays
the closed hat. And when swapping a voice, check the LEVEL as well as the
character - `openhat` returns `* 0.42` where `hat909` returns `* 0.55`, and
the swap alone cost this record 3 dB of top end and put it back under 2%
above 3 kHz, which is [[industrial-techno-measures-too-dark]] all over again.

Related: [[a-repeated-hit-must-not-be-identical]],
[[top-end-from-transients-not-wash]]
