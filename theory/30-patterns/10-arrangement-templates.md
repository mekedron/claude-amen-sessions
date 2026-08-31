# Arrangement Templates

Bar-by-bar maps. Convert bars to seconds with `bars * 240 / BPM` (4/4).

## Club track, two drops (128 BPM, ~6:00, 192 bars)

```
bars     section        elements
0-15     intro          kick, hats, one perc
16-31    intro 2        + bass, filtered
32-47    groove         + chords, full drums
48-63    build 1        + riser, snare roll, HP filter rising
64-95    DROP 1         everything; variation every 8
96-111   breakdown      drums out, pads + lead + reverb
112-127  build 2        bigger than build 1; silence in bar 127 beat 4
128-175  DROP 2         + one new element, wider, longer
176-191  outro          subtract to drums, then kick only
```

## EDM / festival (128 BPM, ~3:20, 108 bars)

```
0-7      intro          hook fragment, filtered
8-23     verse          drums + bass + chords + vocal
24-31    build 1        riser + snare roll; last beat silent
32-63    DROP 1         32 bars
64-79    breakdown      chords + vocal, huge reverb
80-87    build 2        16 bars would be better if length allows
88-103   DROP 2         + new lead layer
104-107  outro          short
```

## Trance (138 BPM, ~8:00, 276 bars)

```
0-31     intro          drums + rolling bass (DJ-friendly)
32-63    groove         + pads, arp, atmosphere
64-95    energy         + percussion, first melodic hints
96-159   BREAKDOWN      drums out; pads; the lead melody introduced quietly
160-191  BUILD          snare roll accelerating, riser, filter, white noise
192-255  CLIMAX         full: kick, rolling bass, lead, arps
256-275  outro          subtract; drums last
```

## Drum & bass (174 BPM, ~5:30, 240 bars)

```
0-15     intro          atmosphere, filtered break
16-31    beat in        break at half energy, sub
32-63    DROP 1         full break + bass, 32 bars
64-79    breakdown      halftime or drums out; pads, melody
80-95    build          rolling drums, riser, sub-drop in bar 95
96-127   DROP 2         new bass, more layers
128-159  section 3      variation or a third bass
160-175  breakdown 2    short
176-207  DROP 3         final
208-239  outro          subtract; drums last
```

## Dubstep (140 BPM, ~4:00, 140 bars)

```
0-15     intro          atmosphere, hint of the bass
16-31    groove         drums + sub, half energy
32-47    build          riser, snare roll; 1 bar of silence at 47
48-79    DROP 1         32 bars; bass pattern changes every 4
80-95    breakdown      chords, vocal, no bass
96-111   build 2
112-135  DROP 2         different bass patch
136-139  outro
```

## Techno (134 BPM, ~7:30, 250 bars)

```
0-31     kick + one hat, filter closed
32-63    + percussion 1, filter opening
64-95    + sub bass
96-127   + percussion 2, + the "hook" element
128-159  peak 1: everything, filters open
160-191  breakdown: kick out, pads and reverb, riser
192-223  return, more intense: + one new element
224-249  outro: subtract; kick last
```

## House (124 BPM, ~6:30, 200 bars)

```
0-15     drums only (DJ intro)
16-31    + bass
32-47    + chords
48-63    + vocal / lead
64-79    breakdown: drums reduced, chords and vocal exposed
80-95    build: filter opens, percussion returns
96-159   main: everything; small variations every 8 bars
160-183  reduced section: strip back, then rebuild
184-199  outro: subtract; drums last
```

## Pop song (105 BPM, ~3:10, 83 bars)

```
0-3      intro          4 bars, hook fragment
4-19     verse 1        16 bars
20-27    pre-chorus     8 bars, building
28-43    chorus 1       16 bars
44-51    post-chorus    8 bars
52-59    verse 2        8 bars (shorter)
60-67    pre-chorus     8 bars
68-83    chorus 2       16 bars
84-91    bridge         8 bars, stripped
92-115   chorus 3       24 bars, biggest
116-119  outro          4 bars
```

## Trap / hip-hop (140 BPM, ~2:50, 100 bars)

```
0-7      intro          melody loop, filtered
8-15     hook 1         full beat
16-31    verse 1        beat reduced under the vocal
32-39    hook           full
40-55    verse 2
56-63    hook
64-71    bridge / beat switch
72-87    hook (double)
88-95    outro
```

## Ambient (no fixed tempo, ~10:00)

```
0:00-1:30   one element alone
1:30-3:30   second layer fades in over 30 s
3:30-5:30   harmonic shift; the first real event
5:30-7:30   density peak (4-5 layers)
7:30-9:00   subtraction back toward the opening
9:00-10:00  decay to silence
```

## Rock song (120 BPM, ~3:40, 110 bars)

```
0-7      intro          the main riff
8-23     verse 1        16 bars
24-31    pre-chorus     8 bars
32-47    chorus 1       16 bars
48-63    verse 2        16 bars
64-71    pre-chorus
72-87    chorus 2
88-95    solo / bridge  8-16 bars over the verse or a new progression
96-119   chorus 3       final, extended
120-127  outro          riff + fade or a hard stop
```

## Cinematic cue (~2:30)

```
0:00-0:30   establish: one texture, one motif
0:30-1:00   development: add layers, the harmony moves
1:00-1:30   tension: ostinato, rising, percussion enters
1:30-1:50   climax: full ensemble, hit points aligned to the edit
1:50-2:15   resolution or aftermath: subtract, sustain
2:15-2:30   tail: decay to silence or a single held note
```

## The arrangement matrix — use this for every track

Draw the grid before writing anything.

```
bars:        0-7  8-15 16-23 24-31 32-39 40-47 48-55 56-63
kick          -    x     x     x     x     -     x     x
sub bass      -    -     x     x     x     -     x     x
hats          x    x     x     x     x     x     x     x
clap          -    -     x     x     x     -     x     x
pad           x    x     x     -     -     x     x     x
lead          -    -     -     x     x     -     x     x
vocal         -    -     -     -     x     x     x     -
riser         -    -     -     -     -     -     x     -
impact        -    -     x     -     -     -     x     -
```

Then verify:

- [ ] Every column has at least one element that the previous column did not.
- [ ] Every column has at least one element **removed** relative to the previous.
- [ ] No row is entirely `x` (that element is wallpaper) or a single `x` (wasted).
- [ ] Every section boundary lands on a multiple of 8.
- [ ] The lowest-density column immediately precedes the highest-density one.
- [ ] The peak occurs 60–75% of the way through.

## Duration reference

| BPM | 8 bars | 16 bars | 32 bars | 64 bars | 128 bars |
|---|---|---|---|---|---|
| 80 | 24.0 s | 48.0 s | 1:36 | 3:12 | 6:24 |
| 90 | 21.3 s | 42.7 s | 1:25 | 2:51 | 5:41 |
| 100 | 19.2 s | 38.4 s | 1:17 | 2:34 | 5:07 |
| 110 | 17.5 s | 34.9 s | 1:10 | 2:20 | 4:39 |
| 120 | 16.0 s | 32.0 s | 1:04 | 2:08 | 4:16 |
| 128 | 15.0 s | 30.0 s | 1:00 | 2:00 | 4:00 |
| 140 | 13.7 s | 27.4 s | 0:55 | 1:50 | 3:39 |
| 150 | 12.8 s | 25.6 s | 0:51 | 1:42 | 3:25 |
| 160 | 12.0 s | 24.0 s | 0:48 | 1:36 | 3:12 |
| 174 | 11.0 s | 22.1 s | 0:44 | 1:28 | 2:57 |

## Related

- Why: `../00-foundations/11-form-and-arrangement.md`
- Transitions between these blocks: `06-transitions-and-fx.md`
