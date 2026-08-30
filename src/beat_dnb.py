"""Classic DnB: filtered intro -> two drops with sub bass -> chop fills -> outro."""
from amenlib import *

s = Session(22)

# intro: filtered break opening up
s.place(s.pos(0), lp(bar_of(0), 500), 0.9)
s.place(s.pos(1), lp(bar_of(1), 2200), 0.95)
s.place(s.pos(2), bar_of(0))
s.place(s.pos(3), bar_of(1)[:int(12 * STEP)])
for i, st in enumerate([12, 13, 14, 15]):
    s.place(s.pos(3, st), SN1, 0.65 + i * 0.12)
s.place(s.pos(4) - len(CR), rev(CR), 0.9)

# drop 1
s.place(s.pos(4), bar_of(0)); s.place(s.pos(4), CR, 0.9)
s.place(s.pos(5), bar_of(1))
s.place(s.pos(6), bar_of(2))
s.pat(7, [(0, K), (2, K2), (4, SN), (6, G, 0.8), (7, SN1, 0.7), (8, K),
          (10, SN1), (11, SN1, 0.8), (12, S2), (14, rev(SN1))])
s.place(s.pos(8), bar_of(0))
s.place(s.pos(9), bar_of(3))
s.place(s.pos(10), bar_of(2))
s.pat(11, [(0, K), (2, K2), (4, SN), (8, SN1, 0.6), (10, SN1, 0.7),
           (12, SN1, 0.8), (13, SN1, 0.85), (14, SN1, 0.9),
           (14.5, SN1, 0.95), (15, SN1), (15.5, SN1)])
s.place(s.pos(12) - len(CR), rev(CR), 0.8)

# section 2: heavier chopping
s.place(s.pos(12), CR, 0.9)
s.pat(12, [(0, K), (1, K2, 0.85), (4, SN), (7, SN1, 0.6), (9, K2),
           (10, K), (12, S2), (15, G, 0.8)])
s.place(s.pos(13), bar_of(1))
s.pat(14, [(0, K), (2, SN1, 0.55), (3, SN1, 0.7), (4, SN), (8, K2),
           (10, K), (11, SN1, 0.6), (12, S2), (14, K2, 0.9)])
s.pat(15, [(0, K), (2, K2), (4, SN), (8, G, 0.9), (8.5, G, 0.75), (9, G, 0.6),
           (10, SN1, 0.8), (12, S2), (14, rev(SN), 0.9)])
s.place(s.pos(16), bar_of(0))
s.place(s.pos(17), bar_of(2))
s.place(s.pos(18), bar_of(3))
s.pat(19, [(0, K), (2, K2), (4, SN), (6, SN1, 0.5), (8, SN1, 0.6),
           (10, SN1, 0.7), (12, SN1, 0.85), (13, SN1, 0.9),
           (14, SN1), (15, pitched(SN, 0.7))])
s.place(s.pos(20) - len(CR), rev(CR), 0.85)

# outro
s.place(s.pos(20), bar_of(0)); s.place(s.pos(20), CR, 0.9)
s.pat(21, [(0, K), (4, SN), (8, pitched(CR, 0.5), 0.9)])

# sub bass, A minor
N = {'A1': 55.0, 'C2': 65.41, 'G1': 49.0, 'E1': 41.2, 'D2': 73.42, 'F1': 43.65}
def bassline(b, notes):
    for st, name, ln in notes:
        s.place(s.pos(b, st), sub(N[name], ln), 0.34)

for b in range(4, 12):
    if b % 2 == 0:
        bassline(b, [(0, 'A1', 3), (6, 'A1', 2), (10, 'C2', 2), (12, 'G1', 3)])
    else:
        bassline(b, [(0, 'A1', 3), (8, 'E1', 3), (12, 'G1', 2), (14, 'A1', 2)])
for b in range(12, 20):
    if b % 2 == 0:
        bassline(b, [(0, 'A1', 3), (6, 'D2', 2), (10, 'C2', 2), (12, 'A1', 3)])
    else:
        bassline(b, [(0, 'F1', 3), (6, 'F1', 2), (8, 'G1', 3), (12, 'E1', 4)])
bassline(20, [(0, 'A1', 8)])
bassline(21, [(0, 'A1', 12)])

s.render('amen_dnb_174.wav')
