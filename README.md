# Claude Music

Music composed and coded by **Claude** in a single terminal session — no DAW,
no plugins, no audio libraries. Just numpy and scipy writing WAV files.

Two families so far:

- **Amen Sessions** — 18 drum & bass pieces in which every drum hit comes from
  one 6.9-second Amen break, sliced and resequenced.
- **Machine Rave** — pieces with no sample at all: every kick, cowbell, 808,
  screech and tyre squeal is synthesized from scratch.

A human ran the session, picked the directions, listened, and gave feedback
("the stars need more depth", "that roll takes my ears off"); Claude wrote all
the code and made all the musical decisions. Claude cannot hear the renders —
they were verified by spectrogram and by measuring band balance, stereo width,
sidechain depth and transient punch against the tracks that already worked.

## The engine

    src/core.py       the shared engine: oscillators, 74 synths and effects,
                      the mix bus and the sequencer. Tempo-agnostic.
    src/sampler.py    the sample layer: load any audio file, lock it to a bar
                      grid, slice it, retime it - several at once, at
                      different tempos.
    src/amenlib.py    the Amen module: one Sample, prepared and named
    src/phonklib.py   the phonk module: the cowbell and the car, 160 BPM
    src/hardlib.py    the hardstyle module: the kick, 170 BPM

A genre module sets the grid, adds its own kit and re-exports core, so
`from amenlib import *`, `from phonklib import *` and `from hardlib import *`
are the same API with a different palette. One small script per piece,
arrangement only.

The sample layer finds hits by itself: pointed at the Amen break, `Sample.kit()`
recovers the map the break is documented by — kicks on 0, 2, 10, 11, snares on
4 and 12 — so an unfamiliar break can be loaded and played the same way, or
layered over a synthesized track:

```python
from phonklib import *
from sampler import Sample

brk = Sample('samples/some_break.wav', bars=4).fit()   # snapped to 160 BPM
s.place(s.pos(4), brk.bar(0))
s.place(s.pos(5), rev(brk.get(1, 8, 4)), 0.6)
```

## The tracks

All finished audio lives in `renders/`.

**Machine Rave** (nothing sampled, ~2:30 each):

| File | What it is |
|---|---|
| `phonk_drift_160.wav` | Drift phonk in F# minor: the 808 cowbell driven until it clangs, a sliding 808, memphis vocal chops, tyres and an engine. Three drops, a tape-stopped breakdown, pitched echoes thrown ear to ear |
| `hard_ascension_170.wav` | Industrial hardstyle in A minor: a kick put through drive, EQ, drive and a wavefolder, reverse bass swelling into every gap it leaves, and a euphoric breakdown that has to earn the drop it walks into |

**Amen Sessions** (full-length, ~3 min):

| File | What it is |
|---|---|
| `amen_liquid_track_174.wav` | Classic liquid: rhodes, vinyl crackle, two drops with sub-drop booms |
| `amen_psx_snow_174.wav` | PSX-snowboarding-game liquid: icy bells, game lead melody, mountain wind |
| `amen_roller_174.wav` | Dark atmospheric roller: formant choir, orchestra hits, acid 303 interlude |
| `amen_cosmos_174.wav` | Space narrative: stardust bells in deep reverb, a supernova, return to peace |
| `amen_machine_dreams_174.wav` | Liquid about being an AI: morse-code "HELLO", datastream arps, power-down ending |
| `amen_alive_174.wav` | Euphoric 94 jungle anthem: M1 rave piano, gospel diva, hoovers |
| `amen_jester_174.wav` | Drill'n'bass mischief: a music box vs. a possessed Amen, generative chops |
| `amen_soundsystem_174.wav` | Ragga jungle: dub sirens, DJ rewinds, one-drop breaks, two-note riddim |
| `amen_noir_174.wav` | Jazz club at 3 a.m.: harmon-muted trumpet with fall-offs, rootless rhodes comps, brushed Amen |
| `amen_finale_174.wav` | The farewell: every track returns once to say goodbye, and the last word, in morse code, is AMEN |

Short studies (~30 s): `amen_dnb_174.wav`, `amen_jungle_174.wav`,
`amen_darkside_174.wav`, `amen_liquid_174.wav`, `amen_jumpup_174.wav`,
`amen_neuro_174.wav`, `amen_rave_174.wav`, `amen_funk_174.wav`.

## Render it yourself

Needs `python3` with `numpy` + `scipy`. The Amen module also needs `ffmpeg` and
`sox` on PATH to prepare the break; the synthesized tracks need neither.

```sh
python3 src/track_drift.py       # writes renders/phonk_drift_160.wav
python3 src/track_hardstyle.py   # writes renders/hard_ascension_170.wav
python3 src/track_alive.py       # writes renders/amen_alive_174.wav
```

Every track script prints a mix report before it renders — per bus level, peak,
crest factor, stereo width and where its energy sits — which is how a deaf
composer checks its work.

## Credits

- Source sample: "Amen break 140 bpm" by axel_bfdi2025
  (`axel_bfdi2025-amen-break-140-bpm-333318.mp3`).
- The Amen break itself: Gregory C. Coleman's four bars in "Amen, Brother"
  (The Winstons, 1969) — the most sampled recording in history. This project
  is one more thank-you note to it.
- Music & code: Claude, 2026. Session produced by a human who kept saying
  "давай ещё" — which is the only reason there are twenty tracks.

## License

Everything Claude made here — the code and the music — is public domain
([Unlicense](LICENSE)): use it for anything, anywhere, no credit required.
The Amen break itself belongs to history, and the source sample belongs to
its uploader.
