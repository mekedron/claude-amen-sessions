---
name: dark-is-register-and-mode-not-key
description: Asked for a darker track, the answer is not the key name - it is how low the parts sit and which scale degrees actually sound
type: feedback
date: 2026-09-01
---

The user asked for `finsternis` to be *"более в какую-то типа знаешь такую
темную минорную"*, and separately for the acid itself to be *"именно типа
низкий, понимаешь, такой типа низкий, низкий эйсид"*. Both were satisfied,
and the key name did almost none of the work.

**In 12-TET a key is a transposition and nothing else.** "The character of
Eb minor" is a leftover from unequal temperaments. Three things do the work:

**1. Register.** Moving the record from F# to D# is not darker because it is
D#; it is darker because everything is three semitones lower. The kick went
from 46.25 Hz to 38.89 Hz, which put 43% of its energy into 20-40 Hz where a
body feels it rather than hears it - and cost only 0.5 dB more than the
higher kick through a 55 Hz highpass, because the harmonics carry it. Check
that number before going below about 41 Hz; under it the kick is felt on a
rig and gone on a laptop.

**2. Which degrees sound.** The first draft of this line was root, fifth and
octave with the b2 sliding past on its way somewhere. That is a POWERFUL
shape, not a dark one: the perfect fifth is the most stable interval there
is, and the octave is confirmation. Darkening it meant almost deleting the
fifth, landing the b2 **on** beats instead of through them, leaning on the
b6, and flattening the fifth to the b5 - one note, and Phrygian becomes
Locrian, which is a tritone standing on the kick.

**3. Where the bass instrument lives.** Every 303 in this project
high-passes itself at 165-240 Hz because "the sub belongs to the kick" -
correct when the line is a hook over a bassline, wrong when the line IS the
bassline. `industriallib.deepacid()` is the same machine written to own
60-300 Hz: it measures 15% in 60-120 and 62% in 120-300 where the old one
measures 0% and 8%. See [[the-303-can-be-the-bass-part]].

**How to apply:** when the request is "darker", do not reach for a key.
Ask which band the parts occupy, and count how often the fifth and the octave
are sounding against how often the b2 and the b6 are. And measure the result
per section - `finsternis` has 0.02% of its energy above 3 kHz in the umbra
and 6.3% in the last section, which is what makes the last section arrive.

Related: [[industrial-techno-measures-too-dark]]
