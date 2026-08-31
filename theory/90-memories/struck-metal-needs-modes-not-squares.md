---
name: struck-metal-needs-modes-not-squares
description: A cowbell, a clave and a timbale shell are bells - inharmonic bending modes with per-mode decay - not stacks of square waves, and the difference is audible at eight hits a bar
type: decision
date: 2026-09-01
---

Struck metal in this engine is synthesised **modally**: a set of inharmonic
partials at measured ratios, each with its own amplitude and its own decay
time, plus a separate contact transient that is not part of the body's motion
at all. See `campana`, `clave`, `cascara` and `paila` in `src/latinlib.py`.

The 808 approach - two or six detuned square waves through a band-pass, then
folded until it screams - is a different instrument and is already in the
engine twice, as `phonklib.cowbell` and `driftlib.cowbell`. Those are correct
for what they are: a TR-808 cowbell is two squares, and phonk drives it into
distortion to carry a melody.

**Why:** the two are distinguishable by how they *decay*, not by their
spectrum at the moment of the strike. A square stack decays as one envelope,
so every partial dies together and every hit sounds identical. Real metal
loses its high modes first - the ratios are irregular (a hand bell is near
1, 1.47, 1.93, 2.44, 3.02, 3.71) and `tau_k` falls as the mode number rises -
so the timbre changes across the 200 ms of the hit and the ear hears an
object rather than a tone. At one hit a bar nobody would notice. A mambo bell
is struck **eight times a bar for four minutes**, and there a fixed timbre
becomes a machine gun.

Two things follow from the same reasoning:

- **Where it is struck changes which modes are excited, not just the level.**
  A bell hit on the mouth rings low and long; hit on the neck, where the
  player's hand is wrapped round the metal, the low modes are damped and what
  survives is high and dry. Model it as two weight vectors over one mode set.
- **Roll the strike transient off above ~8 kHz and vary it per hit.** The
  contact noise is where fatigue comes from, and it is the part that is
  identical every time unless a seed moves it.

**How to apply:** `membrane()` in the same file does the same job for a
struck skin - Bessel-zero ratios, per-stroke excitation vectors, the m=0
family alone for a centre strike. Between them they cover drums and metal;
reach for a square stack only when the target really is a drum machine.
