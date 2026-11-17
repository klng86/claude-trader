# Trading plan: $50k → $120k (31 Dec 2026) → NZD 5M (31 Dec 2031)

Plan date: 17 Nov 2026. Market data as of the 16 Nov close: SPY 739.95, QQQ 661.80, VIX 19.3, USD/NZD 1.817.

## No strategy can promise these targets

| Target | Required | Annualised |
|---|---|---|
| $120k by 31 Dec 2026 | +140% in 31 trading days | far beyond any repeatable edge |
| NZD 5M by 31 Dec 2031 (≈ USD 2.75M) | 22.9× from $120k, or 55× from $50k | 87% a year from $120k, 123% a year from $50k |

If you bet on outcomes the market prices fairly, you cannot reach a 2.4× target with a probability higher than start ÷ goal = **41.7%**. Commissions, bid/ask spreads and option premium only lower that ceiling. To have even a ~33% chance of reaching $120k, you have to accept a roughly 50% chance of losing most of the money. Results from `sim/goal_odds.py` (200k simulated paths, resampled from SPY's 2021–26 returns, which flatter long positions):

**Goal 1 (31 Dec 2026)**

| Strategy | P(reach $120k) | Median result | P(end below $25k) |
|---|---|---|---|
| SPY, 1× to 5× daily leverage | 0.0% | about $51k | 0–1.5% |
| **All-in SPY Dec-31 750/770 call spread** | **32.8%** | $17k | 51% |
| Half in the spread, half in cash | 0.0% | $34k | 0% |

Leverage alone cannot get there in time. A 5× leveraged SPY position needs about a +19% move in six weeks. Concentrated, defined-risk options are the only route with real odds, and those odds are about one in three.

**Goal 2 (31 Dec 2031)**: even starting from $120k, a 4× leveraged S&P position reaches USD 2.75M in only **~4%** of paths. It wipes out 90%+ of the account in about 2% of paths. That uses an optimistic 15%-a-year market history. Combined, the chance of hitting both goals is about **1–1.5%**.

## The plan for the highest probability of hitting the goals

### Phase 1: 17 Nov to 31 Dec 2026, one concentrated, defined-risk bet

The probability-maximising approach is "bold play": make a single bet sized so that a win lands exactly on the target. Smaller repeated bets lose to costs, and bigger bets waste upside.

- **Trade:** buy about 60 SPY 31-Dec-2026 750/770 bull call spreads at a net debit of about $8.33 or better ($49,980 total).
- **Payoff:** if SPY is at or above 770 at expiry (+4.1%), the account is worth 60 × $2,000 = **$120,000**. The maximum loss is the debit paid.
- **Why SPY rather than single stocks or meme options:** the target needs only a +4% index move, and implied volatility is a fairly low 15%. Spreads are tight (about $0.05–0.10 a leg) and there is no gap risk from single-stock earnings. A trade with the same odds on a single stock carries more friction.
- **Management rules:**
  - Enter as one combo limit order at mid (≤ $8.40). Do not leg in.
  - Hold to expiry. Taking profit early gives up the 2.4× payoff that the target needs. Exit early only if the spread is worth $19.50 or more (≥ 97.5% of the maximum value) to remove pin risk.
  - Close before the 31 Dec close if SPY is between 750 and 770, so the short leg isn't assigned against a long leg that is only partly in the money.
  - No averaging down and no rolling. If the trade loses, Phase 1 has failed and the plan resets with whatever is left.

### Phase 2: 2027–2031, compounding (only if Phase 1 succeeds)

The target needs 87% a year. No index product delivers that. The best available odds come from:
1. **Core holding (about 70%):** 2.5–3× leveraged broad equity, through UPRO/TQQQ or deep-in-the-money LEAPS calls on SPY or QQQ, rebalanced quarterly.
2. **Convexity sleeve (about 30%):** catalyst-driven option spreads, sized at no more than 5% of the account per trade, aiming for 3–5× payoffs.
3. **Drawdown circuit-breaker:** cut leverage to 1× after a 35% peak-to-trough drop, and add it back only when SPY is above its 200-day moving average.
4. **Checkpoints:** about $225k by end-2027, $420k by end-2028, $790k by end-2029, $1.47M by end-2030 and $2.75M by end-2031. These are the 87% compounding path at today's FX rate. Missing two checkpoints in a row means the target is statistically out of reach. Moving to a de-risked plan at that point is better than taking ever-larger bets to catch up.

## A recommended alternative

If losing about half the capital in six weeks is not acceptable, a 1.5–2× leveraged S&P allocation has a median outcome of roughly $200–260k by 2031 with small ruin risk. That is a realistic plan, but it will not meet the stated targets.

## Files
- `sim/goal_odds.py`: the Monte Carlo simulation (`python3 sim/goal_odds.py`)
- `sim/goal_odds_output.txt`: the latest run
- `data/spy_daily.csv`: SPY daily closes from Sep 2021 to Nov 2026 (Alpaca)

*This is analysis, not personalised financial advice. Options can expire worthless.*
