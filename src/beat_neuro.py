"""Neurofunk: surgical double-snare edits, FM growl bass in F, dirty break."""
from amenlib import *

s = Session(22)

F2, Ab2, C2, Eb2 = midi(41), midi(44), midi(36), midi(39)
F1 = midi(29)

def grr(b, st, f, ln, lfo=4.0, fm=3.0):
    s.place(s.pos(b, st), growl(f, ln, lfo, fm), 0.38)
    s.place(s.pos(b, st), sub(f / 2 if f > 60 else f, ln), 0.26)

# intro: tension - filtered break, growl swells
s.place(s.pos(0), lp(bar_of(0), 700), 0.85)
s.place(s.pos(1), lp(bar_of(2), 700), 0.85)
grr(1, 8, F2, 8, 1.0, 1.5)
s.place(s.pos(2), bar_of(0))
s.place(s.pos(3), bar_of(3))
s.pat(3, [(12, SN1, 0.7), (14, SN1, 0.9)])
s.place(s.pos(4) - len(CR), rev(CR), 0.9)

# drop 1: tight 2-bar cell with a stepper edit in bar B
for b in range(4, 12):
    if b % 2 == 0:
        s.place(s.pos(b), dirty(bar_of(0), 1.6))
    else:
        s.pat(b, [(0, K), (2, K2), (4, SN), (6, SN1, 0.5), (8, K),
                  (10, SN1, 0.9), (11, K2, 0.8), (12, S2), (14, rev(SN1), 0.8)])
    cell = b % 4
    if cell in (0, 1):
        grr(b, 0, F2, 3, 4.0)
        grr(b, 6, F2, 2, 8.0, 4.0)
        grr(b, 10, Ab2, 2, 6.0)
        grr(b, 12, F2, 3, 4.0)
    else:
        grr(b, 0, Eb2, 3, 4.0)
        grr(b, 6, C2, 2, 8.0, 4.0)
        grr(b, 10, C2, 2, 3.0)
        grr(b, 12, Eb2, 4, 12.0, 5.0)   # fast tearing 16th wobble
s.place(s.pos(4), CR, 0.9)
s.pat(11, [(12, SN1, 0.8), (13, SN1, 0.9), (14, SN1), (15, SN1)])

# mid: stripped machine groove, growl holds long notes
for b in (12, 13, 14, 15):
    s.pat(b, [(0, K), (4, SN), (6, G, 0.5), (8, K2, 0.85), (10, G, 0.5),
              (12, S2), (15, G, 0.6)])
grr(12, 0, F2, 14, 2.0, 2.0)
grr(13, 0, F2, 14, 3.0, 3.0)
grr(14, 0, Ab2, 14, 4.0, 4.0)
grr(15, 0, C2, 10, 6.0, 5.0)
s.place(s.pos(15, 12), rev(CR), 0.85)

# drop 2: same cell, break dirtier, extra ghost edits
for b in range(16, 20):
    s.place(s.pos(b), dirty(bar_of([0, 3, 2, 1][b - 16]), 2.2), 0.95)
    s.pat(b, [(6.5, G, 0.45), (14.5, G, 0.4)])
    grr(b, 0, F2 if b % 2 == 0 else Ab2, 3, 4.0)
    grr(b, 6, F2, 2, 8.0, 4.0)
    grr(b, 10, C2 if b % 2 else Eb2, 2, 6.0)
    grr(b, 12, F2, 4, 10.0, 5.0)
s.place(s.pos(16), CR, 0.9)

# outro
s.pat(20, [(0, K), (2, K2), (4, SN), (8, S2), (12, SN1, 0.8), (14, SN1)])
grr(20, 0, F2, 16, 1.5, 2.0)
s.pat(21, [(0, K), (4, SN), (6, pitched(CR, 0.4), 0.85)])
s.place(s.pos(21, 0), sub(F1, 12), 0.3)

s.render('amen_neuro_174.wav', drive=1.6)
