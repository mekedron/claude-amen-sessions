"""The Amen layer: one sample, prepared and sliced, on top of the shared engine.

This module is nothing but a `Sample` with names: it fetches the source mp3,
trims 4 exact bars at 140 BPM, speeds them to 174 the old jungle way (pitch
rises with the tempo), sets the session grid from the result and labels the
hits. Everything else - synths, effects, the sequencer - comes from core, and
the generic cutting API comes from sampler, so a second break can be layered
in with `Sample('samples/other.wav', bars=4).fit()`.

Slice map (4 bars x 16 steps, from spectral analysis of the sample):
bars 0/1 identical: kick 0,2; snare 4; ghosts 6-9; kicks 10-11; snare 12.
bar 2 ends with kick@12 snare@14. bar 3 is the shifted bar, crash accent @10.

Usage:
    from amenlib import *
    s = Session(22)                     # 22 bars + tail
    s.place(s.pos(0), bar_of(0))        # whole bar
    s.pat(1, [(0, K), (4, SN), (12, S2, 0.8)])   # (step, slice[, gain])
    s.place(s.pos(2, 0), sub(55.0, 4), 0.3)      # synth bass
    s.render('my_beat.wav')
"""
import os
import core
from core import *
from sampler import Sample, prepare

SRC_MP3 = os.path.join(SAMPLES, 'axel_bfdi2025-amen-break-140-bpm-333318.mp3')
BREAK_WAV = os.path.join(SAMPLES, 'amen_174.wav')

# 0.03118 = detected onset of the first hit; 6.85714 = 4 bars at 140 BPM
prepare(SRC_MP3, BREAK_WAV, trim=0.03118, length=6.85714, speed=174 / 140)

amen = Sample(BREAK_WAV, bars=4, name='amen')
BAR, STEP = core.set_grid(bar_samples=amen.bar_len)
brk = amen.x

get = amen.get
bar_of = amen.bar

# ---- slice library ----
K   = amen.get(0, 0)        # kick + ride
K2  = amen.get(0, 2)        # second kick
SN  = amen.get(0, 4, 2)     # snare with tail
SN1 = amen.get(0, 4)        # tight snare (rolls)
G   = amen.get(0, 6)        # ghost/hat
S2  = amen.get(0, 12, 2)    # second snare
CR  = amen.get(3, 10, 2)    # crash accent from bar 4
