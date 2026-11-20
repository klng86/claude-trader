"""Rotation check: hold the current call spread vs exit (at natural) and re-deploy into
the best Dec-31 SPY call spread sized so a win lands at >= $120k.

Usage: python3 sim/rotation_check.py data/quotes/<snapshot>.json
Snapshot JSON: {"spot", "days", "cur": {long, short, qty, cash}, "q": {strike: [bid, ask]}}
Only liquid $5 strikes; fills assumed at the natural price (buy at ask, sell at bid).
Two models: block bootstrap of SPY 2021-26 daily returns, and lognormal at 18% and 21% vol.
"""
import csv, json, sys
import numpy as np
from math import log, sqrt
from statistics import NormalDist

snap = json.load(open(sys.argv[1]))
S, d = snap["spot"], snap["days"]
q = {int(k): v for k, v in snap["q"].items()}
cur = snap["cur"]
GOAL = 120_000
T = d / 252

c = np.array([float(r["close"]) for r in csv.DictReader(open("data/spy_daily.csv"))])
r = c[1:] / c[:-1] - 1
rng = np.random.default_rng(1); n = 200_000; b = 10; nb = -(-d // b)
st = rng.integers(0, len(r) - b, (n, nb))
ST = S * np.prod(1 + r[(st[..., None] + np.arange(b)).reshape(n, -1)[:, :d]], axis=1)

def p_boot(k): return float(np.mean(ST >= k))
def p_ln(k, v): return 1 - NormalDist().cdf(log(k / S) / (v * sqrt(T)))

exit_cash = cur["qty"] * 100 * (q[cur["long"]][0] - q[cur["short"]][1]) + cur["cash"]
print(f"SPY {S}  days {d}  exit value (natural) ${exit_cash:,.0f}  fair ceiling {exit_cash/GOAL:.1%}")
hold = (p_boot(cur["short"]), p_ln(cur["short"], .18), p_ln(cur["short"], .21))
print(f"HOLD {cur['long']}/{cur['short']}: boot {hold[0]:.1%}  ln18 {hold[1]:.1%}  ln21 {hold[2]:.1%}")

rows = []
for k1 in q:
    for k2 in q:
        w = k2 - k1
        if w < 5 or w > 30: continue
        deb = q[k1][1] - q[k2][0]
        if deb <= 0 or w - deb <= 0: continue
        nmin = int(np.ceil((GOAL - exit_cash) / (100 * (w - deb))))
        if nmin * deb * 100 > exit_cash: continue
        rows.append((p_boot(k2), p_ln(k2, .18), p_ln(k2, .21), k1, k2, deb, nmin))
rows.sort(key=lambda x: -min(x[0], x[1]))
print("Best alternatives (rotate only if >= +5pp on BOTH boot and ln18):")
for x in rows[:8]:
    ok = x[0] - hold[0] >= .05 and x[1] - hold[1] >= .05
    print(f"  {x[3]}/{x[4]} debit {x[5]:.2f} x{x[6]}: boot {x[0]:.1%} ln18 {x[1]:.1%} ln21 {x[2]:.1%}  {'ROTATE' if ok else '-'}")
