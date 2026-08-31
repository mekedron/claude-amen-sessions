---
name: bells-are-not-a-default-top-layer
description: Ringing tuned metal is a deliberate instrument choice per track, never the reflex answer to "the top of the mix feels empty"
type: preference
date: 2026-09-01
---

`bell()` lives in `core.py`, so it is available in every track, and it has been
reached for across many of them as a sparkle layer above the snare. The user
hears the result as a habit rather than as a choice, and he is right to: no
instruction or memory ever asked for it.

**Tuned metal is legitimate only when the genre or the track's concept asks for
it**, not when the top octave feels thin.

| Legitimate | Why |
|---|---|
| `campana` / mambo bell, agogô, clave (`latinlib.py`) | The genre is built on them — a mambo bell is struck eight times a bar |
| `cowbell` (`phonklib.py`, `driftlib.py`) | A TR-808 cowbell carrying a melody *is* drift phonk |
| A track whose premise is bells — icy bells, a music box, stardust | The concept carries it, and it was named before the code was written |

| Not legitimate |
|---|
| "The top of the mix feels empty, add a bell" |
| A high ringing counter-melody added to a dark track because there was room |
| A bell on the last 16th of every beat as a groove ornament |

**How to apply:** before adding tuned metal, name which of the three legitimate
reasons applies. If none does, the top of the mix wants something else — air or
noise texture, a high pad, a filtered vocal, a shaker, the harmonics of a part
that is already playing, or nothing at all. An empty top octave is a valid
arrangement decision, and in a dark track it is usually the correct one.

**Why:** a bright inharmonic attack with a long ring is the acoustic signature
of a small struck object, and small struck objects read as toys. The scale it
plays does not override that, which is why this keeps making dark records sound
cheerful. See [[pitched-metal-reads-as-cheerful]] for the register, decay and
level fixes when a bell genuinely belongs, and
[[struck-metal-needs-modes-not-squares]] for how to synthesise one properly.

This is the failure mode Rule 3 in `AGENTS.md` exists to catch: an existing
function in `core.py` was used because it was there, not because the track
asked for it.

Related: [[pitched-metal-reads-as-cheerful]], [[struck-metal-needs-modes-not-squares]]
