"""Oldschool jungle: thin hp intro, shuffled chops, wobble sub, half-speed breakdown."""
from amenlib import *

s = Session(22)

s.place(s.pos(0), hp(bar_of(0), 800), 0.85)
s.place(s.pos(1), hp(bar_of(1), 800), 0.9)
s.place(s.pos(1, 14), SN1, 0.7); s.place(s.pos(1, 15), SN1, 0.9)
s.place(s.pos(2), bar_of(0)); s.place(s.pos(3), bar_of(3))
s.place(s.pos(4) - len(CR), rev(CR), 0.9)

for b in range(4, 12):
    if b % 4 == 0:
        s.place(s.pos(b), bar_of(0)); s.place(s.pos(b), CR, 0.85)
    elif b % 4 == 1:
        s.pat(b, [(0, K), (2, K2), (4, SN), (6, G, 0.8), (8, S2), (10, K),
                  (11, K2, 0.8), (12, SN1), (13, SN1, 0.7), (14, S2)])
    elif b % 4 == 2:
        s.place(s.pos(b), bar_of(2))
    else:
        s.pat(b, [(0, K), (1, SN1, 0.5), (2, K2), (4, SN), (7, K2, 0.8),
                  (8, SN1, 0.6), (10, rev(SN1)), (12, S2), (14, SN1), (15, SN1, 0.7)])
for b in range(4, 12):
    f = 55.0 if b % 4 < 2 else 43.65   # A1 / F1
    s.place(s.pos(b, 0), wobble(f, 14, 2.2), 0.36)

s.place(s.pos(12), pitched(bar_of(0), 0.5), 0.9)   # half-speed breakdown (2 bars)
s.place(s.pos(14), bar_of(3))
s.pat(15, [(0, K), (4, SN), (8, SN1, 0.6), (10, SN1, 0.7), (12, SN1, 0.85),
           (13, SN1, 0.9), (14, SN1), (15, SN1)])
s.place(s.pos(16) - len(CR), rev(CR), 0.9)

for b in range(16, 20):
    s.place(s.pos(b), bar_of(b % 3))
    s.place(s.pos(b, 0), wobble(49.0 if b % 2 else 55.0, 14, 3.0), 0.36)
s.place(s.pos(16), CR, 0.9)
s.place(s.pos(20), bar_of(0)); s.place(s.pos(20, 0), sub(55.0, 8), 0.34)
s.pat(21, [(0, K), (4, SN), (8, pitched(CR, 0.45), 0.9)])
s.place(s.pos(21, 0), sub(55.0, 12), 0.3)

s.render('amen_jungle_174.wav', drive=1.4)
