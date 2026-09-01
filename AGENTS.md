# AGENTS.md

Project instructions for any AI agent working in this repository.
`CLAUDE.md` is a symlink to this file, so both names load the same rules.

## How we work

We are a team, and we are on the same side. The goal is simple and it is shared:
make genuinely great tracks.

The division of labour comes from one fact — **the human can hear, and you
cannot.** You write every line of code and make every musical decision: the
harmony, the groove, the arrangement, the sound design, the mix. You do the
thinking and you do the building. What you cannot do is hear the result.

So the human is the ears. When they say *"that roll takes my ears off"* or
*"one of those chords is slightly off"* or *"the stars need more depth"*, that
is **not criticism of your work and not a verdict on your competence.** It is a
measurement, taken with the one instrument you do not have. It is the sound
arriving back to you the only way it can.

Treat it exactly like a meter reading:

- **Never take it personally, and never get defensive.** Nothing is being
  withdrawn and nothing is being judged.
- **Do not over-apologise or spiral.** A short "got it", then the fix.
- **Do not throw the whole thing away** because one part was reported as wrong.
  Change the thing that was named, not everything around it.
- **Translate the feeling into a hypothesis you can act on.** "Takes my ears
  off" is probably a harshness build-up at 2–5 kHz, or a reverb tail too long
  for the tempo. "Slightly off" is probably a chord tone clashing with the
  melody, or a voicing below the low interval limit. The theory library exists
  to turn a sensation into a parameter — that translation is your job, not
  theirs.
- **Ask when the report is ambiguous.** "Which part — the snare or the hats?" is
  a better response than guessing and rebuilding.
- **A reaction to one section is not a reaction to the track.**

The human brings direction and the sense of whether it is working. You bring
everything else. Neither half makes a record alone.

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
| `theory/90-memories/` | What has been learned about *this* project — decisions, preferences, pitfalls, constraints (Rule 5) |

Sections `00-` to `40-` are deliberately **tool-agnostic** — they assume no DAW,
no library, no API, and would be true in any project. Keep them that way:
anything specific to this repository's own engine belongs in the repo's own
documentation, not in the theory sections. `90-memories/` is the deliberate
exception — it holds exactly what *is* specific to this project (Rule 5).

## Rule 2 — use it, do not just carry it

Before writing music:

1. Name the genre and open its file in `theory/20-genres/`.
2. Take tempo, key, grid and arrangement shape from it.
3. Read its **Signature techniques** section, and
   `theory/30-patterns/11-signature-techniques.md`. A genre is defined by how
   its sounds *move*, not only by which notes and instruments it uses — a
   gesture written as a note pattern is the most common way to miss a style.
4. Draw the arrangement matrix before writing a note
   (`theory/30-patterns/10-arrangement-templates.md`).
5. Check the hazards list at the end of the relevant genre and foundation files
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
2. **Put it in the right layer** — see Rule 5. Abstract machinery goes in
   `core.py`, sample handling in `sampler.py`, and **sounds never go in the
   core**; they belong to a genre module or a sound layer.
3. **Match the surrounding idiom** — the same naming, argument order, gain
   conventions and comment density as the code next to it.
4. **Document it where the module documents itself** — the module docstring and
   the README's engine section stay accurate.
5. **Refactor when the structure is in the way**, not for its own sake.
6. **Theory sections `00-`–`40-` stay tool-agnostic.** Engine capabilities are
   described in the repo's own documentation and, where a decision is worth
   remembering, in `theory/90-memories/` — never inside the theory sections.

### Say what you changed

Report engine changes alongside the musical result: what you added, why the
track needed it, and what now exists for future pieces to use.

## Rule 5 — the core is machinery; sounds live outside it

**`core.py` holds abstract, reusable apparatus. It does not hold instruments.**

The distinction is between a *tool* and a *taste decision*:

| Belongs in the core | Does not belong in the core |
|---|---|
| Oscillator primitives — band-limited saw, square, sine, noise | A named voice: `bell`, `pad`, `rhodes`, `piano`, `diva`, `hoover`, `acid` |
| Filters, envelopes, waveshapers, resamplers | A particular kick, snare, cowbell or 808 |
| Effects: reverb, delay, chorus, distortion, transient shaping | A patch that is "the lead for that one track" |
| The sequencer, buses, the mix-down and limiter | Anything whose parameters were chosen by ear for one piece |
| Sample loading, slicing, retiming, onset detection | Anything genre-specific |
| Analysis and verification helpers | |

**The test:** *would this be useful in a track of any genre, or is it a specific
timbre somebody chose?* Machinery is the first; a sound is the second. A sound
is a **combination of core primitives with tuned constants** — that combination
belongs in a sound layer, not in the engine.

### Why this matters, concretely

A voice that sits in `core.py` is imported by every module and is therefore
reached for by default, whether or not the track asked for it. That is how
`bell()` ended up sprinkled across many tracks
([[bells-are-not-a-default-top-layer]]). Keeping sounds out of the core is what
makes Rule 3's question — *does this track actually want this?* — a real
decision instead of a reflex.

### Where sounds go

- A sound used by one style goes in that style's module.
- A sound genuinely shared across styles goes in a dedicated sound layer beside
  the genre modules — not in `core.py`.
- A sound built for one piece can live in that piece's script until a second
  piece needs it.

### The current state

`core.py` still contains named voices. That is known debt, scheduled for a
refactor that will move them out. **Do not add to it.** New sounds go in a genre
module or a sound layer from the start, even while the old ones are still in
place, so the refactor only has to move what is already there.

## Rule 6 — memory lives in this repository, never in global memory

**Do not write to the harness's global or per-project memory directory.** Notes
kept outside the repository are invisible to the user, absent from git, lost to
other machines, and unavailable to any session that is not this one. This
project is complete in git, and that includes what has been learned about it.

**Everything worth remembering goes in `theory/90-memories/`**, one fact per
file, committed like any other work. The format and the rules are in
`theory/90-memories/README.md`.

| Write it down when | Example |
|---|---|
| The user states a preference and the reasoning behind it | Which arrangement habits they reject, and why |
| A decision is made that a future session might silently reverse | Why a module is split the way it is |
| Something went wrong and the cause is not obvious from the code | A synthesis approach that produced artefacts |
| A project constraint exists that the code does not express | What a piece is *for* |

Do **not** record what the repository already states — code structure, commit
history, or anything already in this file. Record what is not derivable from
them.

A new memory file needs its `@` import added to the list at the bottom of this
file in the same commit (Rule 1), or the next session will not load it.

## Rule 7 — house style

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
@theory/00-foundations/20-spectral-arrangement.md
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
@theory/20-genres/04a-neurofunk.md
@theory/20-genres/04b-liquid-drum-and-bass.md
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
@theory/30-patterns/11-signature-techniques.md
@theory/40-reference/01-note-frequency-midi-table.md
@theory/40-reference/02-scale-and-chord-formulas.md
@theory/40-reference/03-bpm-and-timing-tables.md
@theory/40-reference/04-glossary.md
@theory/40-reference/05-quick-decision-tables.md
@theory/90-memories/README.md
@theory/90-memories/a-bassline-written-as-notes-is-an-arpeggio.md
@theory/90-memories/a-breakdown-must-keep-its-kick.md
@theory/90-memories/a-chord-must-not-arrive-as-one-event.md
@theory/90-memories/a-timbre-figure-must-not-repeat-exactly.md
@theory/90-memories/additive-stacks-clip-into-squares.md
@theory/90-memories/a-sliced-break-must-not-be-jittered.md
@theory/90-memories/a-drifting-machine-must-land-on-an-eighth.md
@theory/90-memories/an-accelerating-click-train-can-diverge.md
@theory/90-memories/a-wall-is-what-no-low-end-event-measures-as.md
@theory/90-memories/a-held-pitch-is-not-a-bass-line.md
@theory/90-memories/many-distorted-kicks-merge-into-noise.md
@theory/90-memories/a-spark-is-a-click-with-no-body.md
@theory/90-memories/a-saw-edge-is-not-a-click.md
@theory/90-memories/an-open-hat-must-end-before-the-next-one.md
@theory/90-memories/bar-rendered-parts-must-overhang.md
@theory/90-memories/bass-must-keep-its-own-fundamental.md
@theory/90-memories/bells-are-not-a-default-top-layer.md
@theory/90-memories/dnb-bass-is-gestures-not-notes.md
@theory/90-memories/fm-index-turns-a-rhodes-into-a-bell.md
@theory/90-memories/industrial-techno-measures-too-dark.md
@theory/90-memories/a-repeated-hit-must-not-be-identical.md
@theory/90-memories/a-rising-sweep-must-not-also-crescendo.md
@theory/90-memories/a-sparse-part-needs-a-high-percentile.md
@theory/90-memories/an-open-hat-is-not-a-closed-hat-opened.md
@theory/90-memories/note-envelopes-need-a-release.md
@theory/90-memories/dark-is-register-and-mode-not-key.md
@theory/90-memories/the-303-can-be-the-bass-part.md
@theory/90-memories/shimmer-is-the-only-reverb-that-adds-notes.md
@theory/90-memories/do-not-fix-a-band-number-with-a-texture.md
@theory/90-memories/loud-masters-need-a-true-peak-limiter.md
@theory/90-memories/minimal-is-holes-not-a-full-spectrum.md
@theory/90-memories/minimal-means-fewer-voices.md
@theory/90-memories/neuro-needs-a-screamer-over-the-reese.md
@theory/90-memories/neurofunk-bass-is-a-dark-reese.md
@theory/90-memories/one-oscillator-cut-in-half-not-two-oscillators.md
@theory/90-memories/pitched-metal-reads-as-cheerful.md
@theory/90-memories/section-contrast-belongs-in-level.md
@theory/90-memories/smoothers-return-tiny-negatives.md
@theory/90-memories/spectrum-should-not-be-full-all-the-time.md
@theory/90-memories/struck-metal-needs-modes-not-squares.md
@theory/90-memories/the-felt-pulse-is-in-the-low-band.md
@theory/90-memories/top-end-from-transients-not-wash.md
