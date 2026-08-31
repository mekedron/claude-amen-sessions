---
name: loud-masters-need-a-true-peak-limiter
description: Clipping and bus compression cannot reach commercial density; a look-ahead limiter can, and PLR measured against dBTP flatters masters that clip
type: decision
date: 2026-09-01
---

`core.brickwall()` is the engine's loudness stage. `core.limiter()` averages
its gain curve, so it pulls at peaks rather than stopping them - it is a
safety net, and pushing it just turns the track down. `brickwall` takes the
minimum required gain over a look-ahead window, releases with a one-pole, and
detects on a 4x upsample so it holds a **true** peak.

Two numbers worth keeping:

- Commercial neurofunk (Magnetude, 2024-25) measures a crest factor of
  **4.2-4.5 dB inside a drop** and spends **65% of its time within 6 dB of
  the ceiling**. A soft clipper alone reaches about 8 dB; bus compression
  cannot tell a transient from a bar and makes it worse.
- Those masters read **+3 to +4 dBTP**. `verify.py` computes PLR against true
  peak, so a master with inter-sample overs reads as *more* dynamic than a
  clean one at the same loudness. Compare sample-peak PLR when judging: at
  -1.0 dBTP and -6.3 LUFS, PLR reads 5.3 where Exile reads 7.9, and yet
  Exile's sample-peak PLR is 3.8 against this track's 5.3.

**Order matters.** The clipper runs first and takes the spikes off; if it
does not, the limiter has to duck a whole bar to catch one sample and the
master gets *quieter* the harder it is pushed. Pushing the limiter from
+3.8 dB to +8.3 dB with the clipper backed off measured 0.5 dB louder and
1 dB *worse* in crest.

**Why:** the density in this genre is not a mastering flourish, it is the
sound. But an over is an over: the references distort in an encoder and this
engine does not have to.

**How to apply:** `s.render(..., clip=<peak/1.6>, comp=dict(...),
brick=dict(gain=..., ceiling=0.89))`. Keep the clipper under ~2% of samples
shaped and let the limiter do 3-5 dB.

Related: [[section-contrast-belongs-in-level]]
