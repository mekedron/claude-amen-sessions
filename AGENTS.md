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

## Rule 3 — build the sound the track needs; never settle for one that exists

**Synthesising a new sound is the default, not the last resort.** The engine's
existing synths were each written to satisfy one particular track's
requirements. A function whose name matches what you need is not evidence that
its sound fits — `pad`, `bell` or `bass` was tuned for a piece with a different
tempo, key, register, density and genre.

Reaching for an existing sound because it is there produces tracks that all
sound the same. Adding new synths, new variants and new parameters to the engine
is expected work, not scope creep.

### Before using any existing sound, audit it against this track

State the answers to yourself; do not reuse on autopilot.

1. **Role** — what job does this sound do in *this* arrangement, and does the
   existing one actually do that job, or merely a similar-sounding one?
2. **Register** — does it sit where this arrangement has room, or does it
   collide with the bass, the lead or the vocal?
3. **Envelope** — do its attack and decay fit this tempo? A 400 ms decay that
   worked at 90 BPM smears at 174.
4. **Timbre and genre** — does its harmonic content match what the genre file
   calls for, or is it borrowed from a different style?
5. **Density** — how many elements already occupy its band?

If any answer is "no" or "not quite": **write a new synth, or add parameters to
the existing one so both callers get what they need.** Never bend the
arrangement to fit a sound that is merely available.

### When you do reuse

Reuse deliberately and say so — name which existing sounds you kept and why
they fit this track's requirements. Silent reuse is the failure mode this rule
exists to prevent.

### Where to start a new sound

`theory/10-instruments/` gives the signal path and rebuild recipe for the
machines that defined each genre, and `theory/30-patterns/08-sound-design-recipes.md`
gives the generic constructions. Build from those rather than from whatever the
last track happened to leave behind.

## Rule 4 — house style

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
