---
name: dnb-bass-is-gestures-not-notes
description: A drum & bass bass is one long note whose modulation rate is sequenced; a sequence of note events reads to him as an arpeggiator
type: preference
date: 2026-09-01
---

The bass line in this genre is **one or two notes across two bars** whose
timbre travels, not a pattern of note events. He described the failure exactly:
"сейчас все эти звуки они играют как просто на простом арпеджиаторе... идут
один за другим... вот этот подход очень прикольно использовать для acid" - and
then described what it should be: "вжууууууУУУУУУУуууу ВЖУЖУЖУЖУжужужужу...
она растягивается по-разному, вытягивается".

So the rhythm is **the rate of the modulation, sequenced per step**, not the
positions of note-ons. `core.scanlane()` integrates a phase from a per-step
rate lane in cycles per beat - 0 holds the timbre still for a long stretch,
0.25 is one sweep per bar, 2 an eighth, 4 a sixteenth, 8 a thirty-second - so
a rate change accelerates a gesture that is already moving instead of
restarting it.

And the phrase is built from **gestures that alternate and recombine**:
"сначала вжух-вжух, один звук, потом пау-пау какой-нибудь другой звук, потом
пау пау пау... они все всегда меняются, сочетаются друг с другом". A gesture
is (rate lane, gate lane, scan range, which patch); a two-bar cell is four or
five of them end to end; a drop uses six different cells so no two bars are
assembled the same way. `machinelib.GESTURES` and `phrase()`.

Two rules that follow:

1. **Do not gate a sustained bass into separate hits.** Only the `pau`
   gestures use the gate, because a stab is what a gate is for. Everything
   else stays open. Measured: the gesture phrase holds amplitude above half
   its level 90% of the time, the note-sequence version 77%.
2. **Cut between patches at gesture boundaries, not on a grid.** Both patches
   share one gesture timeline, so the instrument changes while the rhythm
   carries on.

**Why:** he hears note events as a separate machine playing a scale. The
continuity of the low end and the movement of the timbre are the two things he
listens to first, and a note sequence gives him neither.

Related: [[neurofunk-bass-is-a-dark-reese]], [[sustained-parts-rendered-note-by-note]]
