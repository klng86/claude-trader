# claude-trader

A trading log and research repo for one goal: grow a **$50,000 USD** base portfolio with no extra cash added:

| Milestone | Target | Deadline | What it takes |
|---|---|---|---|
| Phase 1 | **$120,000 USD** | 31 Dec 2026 | +140% in 31 trading days |
| Phase 2 | **NZD 5,000,000** (≈ USD 2.75M at 1.817 USD/NZD on 17 Nov 2026) | 31 Dec 2031 | 22.9× from $120k, about 87% a year |

> ⚠️ **Paper trading only, on Alpaca.** No orders are placed, changed or cancelled on Interactive Brokers (IBKR) or any live-money account. The Alpaca paper account holds $100,000; the plan trades only a $50,000 sleeve of it.

## Status (updated 17 Nov 2026)

- **Phase 1 trade:** SPY 31-Dec-2026 750/770 bull call spread, 60 spreads at about $8.33 net debit (≈ $49,980).
  - If SPY ≥ 770 at expiry, the position is worth $120,000.
  - Maximum loss is the debit paid.
- **Execution:** the first order attempts on 16 Nov, while the market was closed, were rejected with HTTP 403. A retry is scheduled for 17 Nov at 9:45 am US Eastern. See the [journal](journal/JOURNAL.md).
- **Open positions:** none yet.

## Odds of hitting the targets

From `sim/goal_odds.py`: 200,000 Monte Carlo paths, block-bootstrapped from SPY daily returns for Sep 2021 to Nov 2026. That period averaged about 15% a year, so these odds lean optimistic.

| | Chance of hitting target | Chance of a big loss |
|---|---|---|
| Phase 1 with leverage only (1–5× SPY) | ~0% | low |
| **Phase 1 with the all-in 750/770 call spread** | **32.8%** | 51% chance of ending below $25k |
| Ceiling for any fairly priced bet (start ÷ goal) | 41.7% | — |
| Phase 2 from $120k, 4× leveraged S&P | ~4% | ~2% chance of losing 90%+ |
| **Both goals combined** | **~1–1.5%** | — |

No strategy can guarantee these targets. The plan aims for the highest achievable probability and states the risk of ruin openly.

## The plan, in brief

- **Phase 1 (to 31 Dec 2026):** one concentrated, defined-risk bet, sized so that a win lands exactly on $120k.
  - Hold to expiry.
  - Close early only if the spread is worth $19.50 or more.
  - Close before expiry if SPY ends between 750 and 770, to avoid assignment trouble.
  - No averaging down and no rolling.
- **Phase 2 (2027–2031):** compound the account.
  - About 70% in 2.5–3× leveraged index exposure (UPRO/TQQQ or deep-in-the-money LEAPS).
  - About 30% in catalyst-driven option spreads, with no more than 5% of the account in any one trade.
  - Cut leverage to 1× after a 35% drawdown.
- **Yearly checkpoints (USD):**

  | End of | 2027 | 2028 | 2029 | 2030 | 2031 |
  |---|---|---|---|---|---|
  | Target | $225k | $420k | $790k | $1.47M | $2.75M |

  Missing two checkpoints in a row means switching to a de-risked plan.

Full details are in [STRATEGY.md](STRATEGY.md).

## Repo layout

| Path | Contents |
|---|---|
| `STRATEGY.md` | Full plan, trade setup, risk rules and the safer alternative |
| `journal/JOURNAL.md` | Running log of every decision, order, fill and lesson |
| `sim/goal_odds.py` | Monte Carlo of the odds for both goals |
| `sim/goal_odds_output.txt` | Output of the latest simulation run |
| `data/spy_daily.csv` | SPY daily closes, Sep 2021 to Nov 2026, from Alpaca |

## Reproduce the simulation

The script needs Python 3 and numpy. Run it from the repo root:

```bash
python3 sim/goal_odds.py
```

## Data sources

- **Prices and option chains:** Alpaca market data
- **VIX history:** Equibles
- **USD/NZD rate:** Alpha Vantage

---
*Analysis and simulated trading only. This is not financial advice. Options can expire worthless.*
