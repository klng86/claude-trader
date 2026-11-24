# claude-trader

A trading log and research repo for one goal: grow a **$50,000 USD** base portfolio with no extra cash added:

| Milestone | Target | Deadline | What it takes |
|---|---|---|---|
| Phase 1 | **$120,000 USD** | 31 Dec 2026 | +140% in 31 trading days |
| Phase 2 | **NZD 5,000,000** (≈ USD 2.75M at 1.817 USD/NZD on 17 Nov 2026) | 31 Dec 2031 | 22.9× from $120k, about 87% a year |

> ⚠️ **Paper trading only, on Alpaca.** No orders are placed, changed or cancelled on Interactive Brokers (IBKR) or any live-money account. The Alpaca paper account holds $100,000; the plan trades only a $50,000 sleeve of it.

## Status (updated 24 Nov 2026, 11:15 pm SGT)

- **Phase 1 position: OPEN ✅**
  - Long 60 × SPY 31-Dec-2026 750/770 bull call spreads, **filled at $7.91** ($47,460).
  - $2,540 of the sleeve is in cash.
- **Payoff:** if SPY ≥ 770 on 31 Dec (+4.3% from 738.6 at entry), the sleeve is worth **$122,540**.
  - Breakeven: SPY 757.91.
  - Maximum loss: $47,460.
- **24 Nov main check:** SPY 718.9. Spread worth $4.17 at exit; sleeve **≈ $27.6k (−45%)**.
  - Odds of reaching the goal: about 11–15%.
  - Rotation test: the best alternative was only +2–3 points better, so **hold**.
- **Account:** Alpaca paper, opened 17 Nov after the connector was reconnected (earlier attempts were rejected with HTTP 403). See the [journal](journal/JOURNAL.md).

## Monitoring

- **Phase 1 (until 31 Dec 2026):** two weekday check-ins (times while US clocks are on standard time):
  - **9:40 pm SGT (8:40 am US Eastern), pre-market prep:**
    - Read-only. Covers the 8:30 am US economic data, the news and SPY's pre-market price.
    - Writes "Today's plan" with price triggers.
  - **11:15 pm SGT (10:15 am US Eastern), main check:**
    - Uses live option prices after the opening swings settle.
    - Carries out the plan and the risk rules, then journals and pushes.
- **Phase 2:** the check-in moves to weekly or monthly, set when Phase 1 ends.
- The standing rules in [CLAUDE.md](CLAUDE.md) apply to every check-in. Above all: **no trading on IBKR.**

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
