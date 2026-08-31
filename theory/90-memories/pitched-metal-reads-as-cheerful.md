---
name: pitched-metal-reads-as-cheerful
description: Ringing tuned percussion above the snare makes a dark track sound happy, whatever the notes are
type: pitfall
date: 2026-09-01
---

Tuned metal that rings for more than about 150 ms in the octave above the
snare reads as a glockenspiel and makes a dark record sound cheerful, even
when every note is in the key and in the minor scale. The user has now
rejected this twice on the same track: first an FM bell playing its own
motif, then `mclank` percussion at C6/Eb6/F5/Ab6 - "как будто вообще не в
попадке к атмосфере трека... получается какой-то весёлый".

What fixes it, in order of how much it matters:

1. **Register.** Drop the same hits an octave and a half, into F4-C5.
2. **Decay.** `damp=3.0` or higher, so the object is struck rather than rung.
3. **Lowpass at 2.4-2.8 kHz.** The inharmonic partials above that are what
   the ear hears as "bell".
4. **Count.** Two hits a bar, not four.
5. **Level.** Half of what feels right in solo.

For a melodic voice in a dark track, the answer is not a quieter bell but a
different instrument: a slow bowed attack, a fifth underneath, a filter that
opens across the phrase, and a vibrato that fades in - `mgloom()` in
`src/machinelib.py`. An instant attack with a bright inharmonic front is a
small hard object, and that is what sounds like a music box.

**Why:** brightness plus a fast attack plus a long ring is the acoustic
signature of a small struck object, and small struck objects are the sound of
toys and music boxes. The scale it is playing does not override that.

Related: [[struck-metal-needs-modes-not-squares]]
