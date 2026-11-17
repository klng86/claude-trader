"""Monte Carlo odds for the two goals.

Goal 1: $50k -> $120k USD by 2026-12-31 (from 2026-11-17).
Goal 2: -> NZD 5,000,000 by 2031-12-31 (~USD 2.75M at USD/NZD 1.817).

Returns are block-bootstrapped from SPY daily closes 2021-09 .. 2026-11
(data/spy_daily.csv). That window averaged roughly +15%/yr, which flatters every
long-equity strategy, so treat these odds as an optimistic upper end.

Run: python3 sim/goal_odds.py
"""
import csv
import numpy as np

rng = np.random.default_rng(7)
N = 200_000
START, G1 = 50_000, 120_000
USDNZD = 1.817
G2 = 5_000_000 / USDNZD          # ~USD 2.75M
FIN_RATE = 0.045                  # yearly cost of borrowing for leverage
DAYS_G1 = int(np.busday_count("2026-11-17", "2027-01-01",
                              holidays=["2026-11-26", "2026-12-25"]))
DAYS_G2 = 252 * 5

closes = np.array([float(r["close"]) for r in csv.DictReader(open("data/spy_daily.csv"))])
rets = closes[1:] / closes[:-1] - 1


def boot(n_paths, n_days, block=10):
    """Block bootstrap of daily returns, shape (n_paths, n_days)."""
    nb = -(-n_days // block)
    starts = rng.integers(0, len(rets) - block, size=(n_paths, nb))
    idx = (starts[..., None] + np.arange(block)).reshape(n_paths, -1)[:, :n_days]
    return rets[idx]


def daily_lev(r, L):
    """Daily-rebalanced leverage L (like UPRO for L=3), wiped out at 0."""
    daily = 1 + L * r - (L - 1) * FIN_RATE / 252
    return np.clip(np.cumprod(np.clip(daily, 0, None), axis=1)[:, -1], 0, None)


# ---------- Goal 1 ----------
r1 = boot(N, DAYS_G1)
spy_T = 739.95 * np.prod(1 + r1, axis=1)
out = {}
for L in (1, 2, 3, 5):
    out[f"{L}x SPY, daily rebalanced"] = START * daily_lev(r1, L)

# SPY Dec-31 750/770 call spread, debit $8.33 (ask 750 13.38 - bid 770 5.05),
# quoted 2026-11-16. Pays 2.40x at SPY >= 770 (+4.1%).
debit, k1, k2 = 8.33, 750, 770
spread_mult = np.clip(spy_T - k1, 0, k2 - k1) / debit
out["All-in SPY 750/770 call spread"] = START * spread_mult
out["50% spread, 50% cash"] = START * (0.5 + 0.5 * spread_mult)

print(f"Goal 1: ${START:,} -> ${G1:,} in {DAYS_G1} trading days (+{G1/START-1:.0%})")
print(f"{'strategy':36s} {'P(hit)':>7s} {'median':>10s} {'P(<$25k)':>9s}")
for k, v in out.items():
    print(f"{k:36s} {np.mean(v >= G1):7.1%} {np.median(v):10,.0f} {np.mean(v < 25_000):9.1%}")
print(f"Upper bound for a fair bet (start/goal): {START/G1:.1%}\n")

# ---------- Goal 2 ----------
n2 = 50_000
r2 = boot(n2, DAYS_G2)
print(f"Goal 2: USD {G2:,.0f} (NZD 5M at {USDNZD}) by 2031-12-31")
print(f"Needs {G2/G1:.1f}x from $120k (CAGR {(G2/G1)**(1/5)-1:.0%}) "
      f"or {G2/START:.0f}x from $50k (CAGR {(G2/START)**(1/5)-1:.0%})")
print(f"{'leverage':>8s} {'P(hit) from 120k':>17s} {'P(hit) from 50k':>16s} "
      f"{'median from 120k':>17s} {'P(lose 90%)':>12s}")
for L in (1, 1.5, 2, 3, 4):
    m = daily_lev(r2, L)
    print(f"{L:8.1f} {np.mean(G1*m >= G2):17.2%} {np.mean(START*m >= G2):16.2%} "
          f"{np.median(G1*m):17,.0f} {np.mean(m < 0.1):12.1%}")
print("\nCaveat: leverage odds here use 2021-26 SPY returns (~15%/yr). "
      "At a long-run ~9%/yr these odds shrink a lot.")
