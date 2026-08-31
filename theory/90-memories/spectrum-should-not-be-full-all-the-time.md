---
name: spectrum-should-not-be-full-all-the-time
description: Tracks come out with every frequency band occupied from first bar to last; which bands are used should change between sections and many genres are deliberately band-limited
type: pitfall
date: 2026-09-01
---

Tracks are being built so that the whole spectrum is filled for the whole
duration — sub, low-mid, mid, presence and air all occupied from the first bar
to the last. The user noticed the pattern across several tracks and asked
whether it is always correct. It is not.

**What goes wrong:**

1. Masking is zero-sum — two elements in a band means one is inaudible, so
   adding content makes the mix less legible, not more.
2. A drop feels big because the build removed the low end. A permanently full
   spectrum has nothing left to open.
3. Occupied bands cost headroom, so a full-everything mix ends up perceptually
   quieter at the same LUFS.
4. Much of what identifies a genre is what it leaves out: lo-fi has no sub and
   no air, dub's bass is dark above 800 Hz, jazz and folk have nothing below
   40 Hz at all, techno is mid-forward, jungle keeps the sub out of the intro.

**How to apply:** budget the bands before writing, give each one a single
primary owner at a time, and make the band map differ between sections — the
sub absent in the intro, the build high-passed, the drop returning the bottom
two octaves at once. Every band should be empty somewhere in the track. Check a
spectrogram of the whole track rather than an analyser on a loop: if the picture
is a solid rectangle from start to finish, that is the failure.

**Do not** add a layer because a band looks empty on an analyser, and do not
treat the pink-noise reference slope as a per-moment target — it is a
statistical tendency of finished full-range masters, and a consequence of good
arrangement rather than a cause.

Full detail in `theory/00-foundations/20-spectral-arrangement.md`.

Related: [[bells-are-not-a-default-top-layer]]
