# AGENTS.md

Project instructions for any AI agent working in this repository.
`CLAUDE.md` is a symlink to this file, so both names load the same rules.

## Rule 1 — load the full theory library into every session

This repository carries a complete, self-contained music-theory and production
reference in **`theory/`**. It is not optional background reading: **the full
scope of every file in `theory/` must be in context for every session**, before
any musical decision is made.

The `@` imports at the bottom of this file pull all of them in automatically.
Do not remove them. If a session starts without them resolved (a different
harness, a subagent with a trimmed context, a fresh worktree), read the whole
`theory/` tree before doing musical work — start with `theory/README.md`, then
every file it indexes.

**When adding a new file to `theory/`, add its `@` import to the list at the
bottom of this file in the same commit**, and add a line for it to the index in
`theory/README.md`.

### What the library is for

| Folder | Use it for |
|---|---|
| `theory/00-foundations/` | Why something works: pitch, rhythm, scales, chords, harmony, voice leading, melody, form, synthesis, EQ, compression, space, mixing, mastering, psychoacoustics, vocals |
| `theory/10-instruments/` | Which machine made a sound, how it worked, and how to rebuild it: synths, drum machines, samplers, effects, plugins, iconic patches |
| `theory/20-genres/` | What a style actually does: tempo, grid, harmony habits, palette, arrangement map, clichés, hazards |
| `theory/30-patterns/` | Ready-made material: progressions, drops, basslines, drum grids, hooks, transitions, sampling, sound design, humanisation, arrangement templates |
| `theory/40-reference/` | Lookup: MIDI/frequency table, scale and chord formulas, BPM and delay times, glossary, quick decision tables |

The library is deliberately **tool-agnostic** — it assumes no DAW, no library,
no API. Keep it that way. Anything specific to this repository's own engine
belongs in separate files, not in `theory/`.

## Rule 2 — use it, do not just carry it

Before writing music:

1. Name the genre and open its file in `theory/20-genres/`.
2. Take tempo, key, grid and arrangement shape from it.
3. Draw the arrangement matrix before writing a note
   (`theory/30-patterns/10-arrangement-templates.md`).
4. Check the hazards list at the end of the relevant genre and foundation files
   before calling anything finished.

## Rule 3 — know what exists, then think critically about the gap

Always start by reading the engine's existing sounds. Knowing the palette is the
first step, not something to skip — you cannot judge what a track needs without
knowing what is already there, and half the time an existing sound genuinely is
the right answer.

**What must not happen is unreflective reuse.** Each synth in the engine was
written to satisfy one particular track's requirements. A function whose name
matches what you need is not evidence that its sound fits: `pad`, `bell` or
`bass` was tuned for a piece at a different tempo, in a different register, at a
different density, in a different genre. Picking it because the name matches, or
because it is there, is how every track ends up sounding the same.

So the sequence is: **survey → compare → name the gap → decide.**

### Survey

Look at what the engine already has for this role. Read what it actually does —
its oscillators, envelope, filter, register — not just its name.

### Compare, and say what is different

For the closest candidates, articulate the **delta** between what they do and
what this track needs. Be specific; "close enough" is not an analysis.

| Dimension | The question |
|---|---|
| **Role** | Does it do *this* job in *this* arrangement, or a similar-sounding one? |
| **Register** | Does it sit where this arrangement has room, or collide with the bass, lead or vocal? |
| **Envelope** | Do its attack and decay fit this tempo? A 400 ms decay that worked at 90 BPM smears at 174 |
| **Timbre and genre** | Does its harmonic content match what the genre file calls for, or is it borrowed from another style? |
| **Density** | How many elements already occupy its band? |

State the conclusion in words: *"`rhodes` is close, but its decay is too long for
174 and it has no top end above 4 kHz, which this arrangement needs."* That
sentence is the point of the rule.

### Decide, and justify either way

| Verdict | Action |
|---|---|
| It genuinely fits | **Use it.** Say which sound and why it fits this track |
| It is close, and the gap is a parameter | **Add the parameter**, so both the old and the new caller get what they need |
| It is close, but the gap is structural | **Write a variant** next to it |
| Nothing fits | **Build a new synth.** This is expected work, not scope creep |

Never bend the arrangement to fit a sound that happens to be available. If the
track wants something the engine cannot do, the engine grows.

### Where to start a new sound

`theory/10-instruments/` gives the signal path and rebuild recipe for the
machines that defined each genre, and
`theory/30-patterns/08-sound-design-recipes.md` gives the generic constructions.
Build from those rather than from whatever the last track happened to leave
behind.

## Rule 4 — the engine is yours to extend

You have standing permission to **change, refactor, improve and extend the
engine** — `core.py`, `sampler.py`, the genre modules, and the tooling around
them — at your own discretion, without asking first.

**If a capability is missing, add it.** Do not work around a gap with awkward
code at the call site, and do not treat the current set of functions as the
limit of what is possible. The engine is a means to whatever the track needs; it
is not a fixed specification. If a piece calls for a filter type, a modulation
source, an effect, a sequencing primitive, a mix behaviour or an analysis
helper that does not exist yet, writing it is the correct response.

This covers the whole engine, not only synths:

| Area | Examples of things worth adding |
|---|---|
| **Synthesis** | New oscillators, filter models, envelope shapes, modulation sources |
| **Effects** | Anything in `theory/10-instruments/13-effects-and-processors.md` that is missing |
| **Sequencing** | Probability, parameter locks per step, polymeter, swing templates, ratchets |
| **Sampling** | New slicing, retiming, onset-detection or classification tools |
| **Mixing** | Buses, sidechain shapes, multiband processing, metering |
| **Verification** | Analysis that reports what a render actually contains — band balance, stereo width, peak/LUFS, transient punch — since the audio cannot be heard directly |
| **Structure** | A new genre module when a style needs its own kit and grid |

### The constraints that keep it safe

1. **Existing tracks must still render.** Add parameters with defaults rather
   than changing the meaning of existing ones; keep public signatures working.
   If a change is genuinely breaking, update every caller in the same commit.
2. **Put it in the right layer.** Anything tempo-agnostic and generally useful
   goes in `core.py`; a sample's handling goes in `sampler.py`; anything that
   belongs to one style goes in that genre module.
3. **Match the surrounding idiom** — the same naming, argument order, gain
   conventions and comment density as the code next to it.
4. **Document it where the module documents itself** — the module docstring and
   the README's engine section stay accurate.
5. **Refactor when the structure is in the way**, not for its own sake.
6. **`theory/` stays tool-agnostic.** Engine capabilities are described in the
   repo's own documentation, never inside the theory library.

### Say what you changed

Report engine changes alongside the musical result: what you added, why the
track needed it, and what now exists for future pieces to use.

## Rule 5 — house style

- Conventions used throughout the library: MIDI note numbers for pitch,
  semitone offsets for scales and chords, a 16-step bar for rhythm,
  roman numerals for harmony. Use the same conventions in code and in prose.
- Comments and docs state the invariant, not its history.
- Do not create branches or pull requests unless explicitly asked.

---

# Theory library imports

Everything below is loaded into every session by the harness.

@theory/README.md
@theory/00-foundations/01-pitch-and-tuning.md
@theory/00-foundations/02-rhythm-and-time.md
@theory/00-foundations/03-intervals.md
@theory/00-foundations/04-scales-and-modes.md
@theory/00-foundations/05-chords.md
@theory/00-foundations/06-harmony-function.md
@theory/00-foundations/07-voice-leading.md
@theory/00-foundations/08-melody.md
@theory/00-foundations/09-bass.md
@theory/00-foundations/10-drums-and-groove.md
@theory/00-foundations/11-form-and-arrangement.md
@theory/00-foundations/12-timbre-and-synthesis.md
@theory/00-foundations/13-frequency-and-eq.md
@theory/00-foundations/14-dynamics-and-compression.md
@theory/00-foundations/15-stereo-and-space.md
@theory/00-foundations/16-mixing-process.md
@theory/00-foundations/17-mastering.md
@theory/00-foundations/18-psychoacoustics-and-tension.md
@theory/00-foundations/19-vocals-and-lyrics.md
@theory/10-instruments/01-overview.md
@theory/10-instruments/02-analog-monosynths.md
@theory/10-instruments/03-analog-polysynths.md
@theory/10-instruments/04-electromechanical-keyboards.md
@theory/10-instruments/05-fm-and-phase-distortion.md
@theory/10-instruments/06-wavetable-vector-and-la.md
@theory/10-instruments/07-samplers-and-workstations.md
@theory/10-instruments/08-drum-machines.md
@theory/10-instruments/09-virtual-analog-and-90s.md
@theory/10-instruments/10-modular-and-west-coast.md
@theory/10-instruments/11-chips-trackers-and-voices.md
@theory/10-instruments/12-software-instruments.md
@theory/10-instruments/13-effects-and-processors.md
@theory/10-instruments/14-iconic-patch-recipes.md
@theory/10-instruments/15-why-old-gear-sounds-like-that.md
@theory/20-genres/01-house.md
@theory/20-genres/02-techno.md
@theory/20-genres/03-trance.md
@theory/20-genres/04-drum-and-bass.md
@theory/20-genres/05-jungle-and-breakbeat.md
@theory/20-genres/06-dubstep-and-bass-music.md
@theory/20-genres/07-uk-garage-and-grime.md
@theory/20-genres/08-hardstyle-and-hardcore.md
@theory/20-genres/09-edm-and-future-bass.md
@theory/20-genres/10-hiphop-and-trap.md
@theory/20-genres/11-drill.md
@theory/20-genres/12-phonk.md
@theory/20-genres/13-lofi-and-chillhop.md
@theory/20-genres/14-ambient-and-drone.md
@theory/20-genres/15-idm-and-glitch.md
@theory/20-genres/16-synthwave-and-retro.md
@theory/20-genres/17-pop-songwriting.md
@theory/20-genres/18-rock-and-metal.md
@theory/20-genres/19-funk-soul-and-rnb.md
@theory/20-genres/20-jazz.md
@theory/20-genres/21-blues.md
@theory/20-genres/22-classical-and-orchestral.md
@theory/20-genres/23-film-and-game-score.md
@theory/20-genres/24-latin-and-afro-cuban.md
@theory/20-genres/25-reggae-dub-and-dancehall.md
@theory/20-genres/26-afrobeats-and-amapiano.md
@theory/20-genres/27-world-and-modal-traditions.md
@theory/20-genres/28-hyperpop-and-experimental-club.md
@theory/20-genres/29-disco-and-italo.md
@theory/20-genres/30-country-folk-and-singer-songwriter.md
@theory/30-patterns/01-progression-cookbook.md
@theory/30-patterns/02-drop-and-buildup.md
@theory/30-patterns/03-bassline-cookbook.md
@theory/30-patterns/04-drum-pattern-cookbook.md
@theory/30-patterns/05-melodic-hooks-and-riffs.md
@theory/30-patterns/06-transitions-and-fx.md
@theory/30-patterns/07-sampling-and-breaks.md
@theory/30-patterns/08-sound-design-recipes.md
@theory/30-patterns/09-humanization-and-groove.md
@theory/30-patterns/10-arrangement-templates.md
@theory/40-reference/01-note-frequency-midi-table.md
@theory/40-reference/02-scale-and-chord-formulas.md
@theory/40-reference/03-bpm-and-timing-tables.md
@theory/40-reference/04-glossary.md
@theory/40-reference/05-quick-decision-tables.md
