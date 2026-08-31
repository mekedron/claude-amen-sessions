---
name: fm-index-turns-a-rhodes-into-a-bell
description: Raising an FM operator's index to fill the presence band is how you build a bell on purpose, and a chord of them through one shared waveshaper reads as a single metallic note
type: pitfall
date: 2026-09-01
---

An electric piano measured with almost nothing between 800 Hz and 3 kHz, so
its 1:7 and 1:14 operators had their indices raised until that band filled.
He named the result in one listen: **"звучит как какой-то колокол, либо же
каубелл"**, and **"они как будто не звучат аккордами - там как будто одна
нота звучит"**.

Both complaints follow from the same arithmetic.

- **A high index at a ratio above about 3 is the definition of a bell.**
  Sidebands land at `c ± n·m` and at index 2.5 the carrier keeps almost none
  of the energy - `J0(2.5) = -0.05` - so what is heard is a cloud of partials
  at 6, 8, 13 and 15 times the fundamental. That is a mode set with no
  relation to a harmonic series, which is what a struck bell has and what
  `theory/90-memories/struck-metal-needs-modes-not-squares.md` says to build
  one out of.
- **A shared waveshaper across a chord is an intermodulator.** Four notes
  summed and then put through one `tanh` produce sum and difference tones
  between every pair of partials, and with a bell-dense spectrum on each note
  the result has no identifiable fundamentals left. Four notes become one
  event.

The trap is that the measurement improved the whole way. Presence-band share
went from 0.5% to 12.5% and the instrument got steadily worse.

**How to apply:** a soft chord in any house or downtempo genre is
**subtractive**, not FM. Two sawtooths a few cents apart per note, summed with
NO shared drive before the filter, one gentle lowpass, and a bucket brigade
after it - `houselib.chord`. A saw at 200 Hz under a 1.6 kHz lowpass has ten
harmonics spread from the fundamental to 2 kHz, which fills the same band
with nothing bright anywhere in it. And the attack is half of "soft": 4 ms is
a stab whatever the spectrum, 30-40 ms is a key being pressed.
