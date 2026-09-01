---
name: a-bassline-written-as-notes-is-an-arpeggio
description: A bass line whose notes are evenly spaced on different scale degrees reads as an arpeggiator; write the rhythm first, keep the root, and gate the holes
type: pitfall
date: 2026-09-01
---

`ruffneck` opened with a bass line that was correct in every way a checklist
can measure - in key, reggae-placed, four bars, a real melodic contour, the
tune of the record. He rejected it in one listen: **"мне не нравится эта
басовая линия, что она просто как арпеджио... как будто она просто
перебирается"**.

The line was `(0, G1) (6, Bb1) (10, C2) (14, D2)`. Four notes, four different
degrees, spacings of 6, 4, 4 - and nothing else in it. That is the definition
of an arpeggiator: a scale walked at a fixed rate. Everything else about it
was right and it still sounded like a machine reading a chord.

Three things separate a riff from that, and all three are needed:

1. **The root dominates.** Three of the four hits in a bar are the tonic. The
   one that is not is a *gesture* - a lift to the third, a drop to the b7
   below - and it happens in the same place every bar until it is a hook.
2. **The spacings are uneven.** 6, 3, 5, 2 rather than 4, 4, 4, 4. Anything
   that lands on every fourth sixteenth is heard as a rate, not as a phrase.
3. **The holes are written.** `subbar` holds each pitch until the next event,
   so a bass with no gate is a drone with pitch changes in it. The rhythm
   lives in the silences: `junglelib.figure()` takes `(step, midi, length)`
   and returns the notes *and* a step gate, because a note that is never
   switched off cannot have a rhythm.

Then **move the same rhythm to another degree** rather than writing a new
bar. Bar 3 of `ruffneck` is bar 1 with every pitch on the bVI and the timing
untouched, and that is what makes four bars read as one idea.

**How to apply:** write the rhythm before any pitch - as x and . on sixteen
steps - and only then decide which hits are not the root. If the part still
works with every note on the tonic, it is a riff; if it collapses, it was
being carried by the pitch sequence and it is an arpeggio.

Related: [[dnb-bass-is-gestures-not-notes]], [[bass-must-keep-its-own-fundamental]]
