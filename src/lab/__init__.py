"""src/lab - the bench.

Diagnostics for a project whose composer cannot hear. `verify.py` measures a
finished WAV; this measures the things you are still holding: one voice, one
bus, one bar, one section.

    import sys; sys.path.insert(0, 'src')
    from lab import *

    band_table([('old hat', hat909(2.2, open_=True)), ('new hat', openhat(3.4))])
    sections(verify._read(path), 142, [('INTRO', 0, 16), ('DROP', 16, 48)])
    walk(x, 142, 0, 14)                       # where does bar 6 jump?
    edges(techkick(), 'kick')
    varies(lambda s: techkick(cseed=s), label='kick click')
    alias_error(lambda sr: my_layer_at(sr), label='grit')

THIS FOLDER IS OPTIONAL AND IT IS YOURS. Nothing in `core.py`,
`industriallib.py` or any track imports it - delete it and every record here
still renders. The thresholds in it ("worse than -30 dB is audible", "a peak
belongs at 60-90%") are the ones that happened to be right for the problems
they came from, not laws; change them, add functions, throw away the ones
that stop earning their place. Each tool exists because a human heard
something and this was the measurement that found it, so the natural way for
the folder to grow is: hear a problem, find it once by hand, then put the
finding here so it is never found by hand again.
"""
from .spectrum import (SR, BANDS, shares, width, band_table, sections, walk)
from .voices import (edges, varies, alias_error, envelope_steps)

__all__ = ['SR', 'BANDS', 'shares', 'width', 'band_table', 'sections', 'walk',
           'edges', 'varies', 'alias_error', 'envelope_steps']
