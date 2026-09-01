`Session.loudness` defaults to the 90th percentile of a 300 ms window, and
its docstring is right about why: whole-track RMS says a 16th-note clav part
is 25 dB under the bass when the ear puts it 6 dB under. But the 90th
percentile only answers "how loud is this WHEN IT PLAYS" down to about a ten
percent duty cycle.

A horn section is nowhere near that. `revashol` has sixteen brass stabs in
sixteen bars - a **five percent** duty cycle - so ninety percent of its
windows are silence, and an automatic fader built on that number came out
**thirty dB wrong**: it measured the horns at -35 dB and asked for a gain of
1.74 when the ear wanted them 11 dB under the drums.

    pct=90   drums -5.2   horns -35.4     a 30 dB error
    pct=99   drums          horns          right, and unchanged for the kit

**How to apply:** when computing faders from measurement, use `pct=99` for
every bus. For a dense part (drums, bass, a pad) the 99th and the 90th
percentile are within a dB of each other, so nothing is lost; for a sparse
one the 99th finds the actual hits, which is the question a fader answers.
And guard the divide - a bus that is silent in the measurement window returns
-inf and produces a gain of thirty million, which then sets the whole
record's peak and hands the clipper a mix that is nine million over.

    lv = S.loudness(S.bus[k][window], pct=99)
    GAINS[k] = clip(10 ** ((ref + TARGET[k] - lv) / 20), 0.05, 12.0) if lv > -70 else 1.0

Related: [[section-contrast-belongs-in-level]]
