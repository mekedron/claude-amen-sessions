---
name: section-contrast-belongs-in-level
description: A breakdown that measures within 1 dB of the drops is not a breakdown, however different its instrumentation - measure the per-section RMS before calling an arrangement finished
type: pitfall
date: 2026-09-01
---

Before a track is finished, measure **RMS per section** and look at the curve.
`src/analyze.py` prints it. The lowest section must sit **3-6 dB under** the
drops, and the lowest of all must be the one immediately before the biggest.

A first pass of `descarga` had a sixteen-bar breakdown in which the drums
stopped entirely, the piano switched from the guajeo to a written solo, and
the break vanished. It measured **-13.2 dB against the drop's -12.5** - a
difference of 0.7 dB, which is inaudible. Every part had been *changed* and
none had been *turned down*, so the percussion, congas, bass and piano
between them refilled the hole the drums left within one bar.

**Why:** contrast is relative and the ear judges the drop against what it
just heard. Removing an element only reads as removal if the total energy
drops with it; a section that swaps a loud thing for another loud thing reads
as a variation, not as a fall. And a drop is only big because the thing
before it was small - so a breakdown that fails to fall also spends the drop
that follows it.

The fix was a gain ramp across the whole section rather than a different
arrangement: every part entering at 0.55 of its drop level and climbing back
over sixteen bars. That moved it to -16.2 dB, 3.7 dB under the drop, and the
band curve moved with it - the 3-16 kHz content fell 11 dB, because that is
where the break lives and the break was gone.

## Section gains are not the same thing as a ride

On `blendung` every section already had its own gains, written into every
`place()` call, and the record still measured **-5 to -6.5 LUFS from bar 8 to
bar 167 without a single break in it** - the void as loud as the drop, and the
arrival at bar 120 reading 0.9 dB *quieter* than the bars before it. Two
reasons, and both are structural rather than careless:

1. **Per-part gains do not sum to a section.** A section is two hundred
   `place()` calls across nine buses. Turning each of them down by the amount
   that feels right leaves the total roughly where it was, because what
   actually changed was which parts are playing, and a different set of loud
   parts is still loud.
2. **The limiter closes whatever gap survives.** At +5.6 dB of input push it
   was pulling 8.2 dB at the peaks and 2.4 dB on average, which is a
   compressor across the whole arrangement: it lifts the quiet sections into
   the loud ones by definition.

The fix is one **gain ride over the finished buses**, written in decibels per
bar and interpolated per sample - a master fader move, and as much a part of
the arrangement as the notes:

    ARC = [(0, -3.4), ..., (80, -7.6), ..., (120, -0.4), ...,
           (168, -8.5), ..., (184, 0.0), ...]
    ride = 10 ** (np.interp(t, bars, db) / 20)
    ride = uniform_filter1d(ride, int(0.030 * SR))     # no zipper
    for b in s.bus: s.bus[b] *= ride[:, None]

Put a **dip immediately before each drop**, not a climb: two points half a bar
apart taking the mix down 2-3 dB, then the drop at 0 dB. And back the master
off far enough that the ride survives it - `brick=dict(gain=1.24)` here, 0.8 dB
of mean reduction. With both, the same arrangement went from a 1.5 dB spread
across four minutes to -16.3 at the trough and -4.9 at the peak.

**How to apply:** print the section table before mixing anything. Check three
things: the curve rises overall, the minimum precedes the maximum, and the
peak lands 60-90% of the way through. Fix a flat curve with a ride over the
buses, not with EQ, not with more parts, and not by turning individual parts
down. See [[bar-rendered-parts-must-overhang]] and
[[industrial-techno-measures-too-dark]].
