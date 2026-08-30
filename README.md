# Amen Sessions

Drum & bass composed and coded by **Claude** in a single terminal session —
every drum hit in every track comes from **one 6.9-second Amen break sample**,
sliced, resequenced and mangled in Python.
Everything else (basses, pianos, choirs, bells, reverb) is synthesized from
scratch with numpy/scipy. No DAW, no samples beyond the break, no audio
libraries — just math writing WAV files.

A human ran the session, picked the directions, listened, and gave feedback
("the stars need more depth", "one of those chords is slightly off");
Claude wrote all the code and made all the musical decisions. Claude cannot
hear the renders — arrangements were verified by spectrogram.

## The tracks

All finished audio lives in `renders/`. Full-length (~3 min):

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

Short studies (~30 s): `amen_dnb_174.wav`, `amen_jungle_174.wav`,
`amen_darkside_174.wav`, `amen_liquid_174.wav`, `amen_jumpup_174.wav`,
`amen_neuro_174.wav`, `amen_rave_174.wav`, `amen_funk_174.wav`.

## How it works

- `src/amenlib.py` — the whole engine: break preparation (trim, speed-up
  140→174 BPM the old jungle way, pitch and all), a slice library mapped by
  spectral analysis (which 16th holds a kick, which holds the crash), a
  `Session` sequencer, and ~30 synths/effects: `sub`, `wobble`, `reese`,
  `sawbass`, `growl`, `hoover`, `funkbass`, `clav`, `rhodes`, `piano`,
  `diva`, `vox`, `strings`, `bell`, `lead`, `pluck`, `orchhit`, `acid`,
  `zap`, `drone`, `impact`, `riser`, `subdrop`, `pad`, `wind`, `crackle`,
  `hat`, plus `reverb` (IR convolution), `wah`, `bitcrush`, `panned`,
  dub-delay echoes, `dubsiren`, DJ `rewind`.
- `src/beat_*.py` / `src/track_*.py` — one small script per piece,
  arrangement only.
- `samples/` — the one source mp3 (and the prepared break, rebuilt on demand).

## Render it yourself

Needs `python3` with `numpy` + `scipy`, plus `ffmpeg` and `sox` on PATH.

```sh
python3 src/track_alive.py    # writes renders/amen_alive_174.wav
```

The scripts rebuild the prepared break (`samples/amen_174.wav`) from the
source mp3 automatically if it is missing.

## Credits

- Source sample: "Amen break 140 bpm" by axel_bfdi2025
  (`axel_bfdi2025-amen-break-140-bpm-333318.mp3`).
- The Amen break itself: Gregory C. Coleman's four bars in "Amen, Brother"
  (The Winstons, 1969) — the most sampled recording in history. This project
  is one more thank-you note to it.
- Music & code: Claude, 2026. Session produced by a human who kept saying
  "давай ещё" — which is the only reason there are sixteen tracks.

## License

Everything Claude made here — the code and the music — is public domain
([Unlicense](LICENSE)): use it for anything, anywhere, no credit required.
The Amen break itself belongs to history, and the source sample belongs to
its uploader.
