# Trading Journal

Rules for this account:
- **Paper trading only, on Alpaca.** Never place, modify or cancel orders on IBKR (read-only at most).
- The Alpaca paper account starts at $100,000. The plan trades only a **$50,000 sleeve** of it, as the base portfolio.
- Each entry records date (NZ/US), what happened, the numbers, and the decisions made.

---

## 2026-11-17 — Kick-off

**Goals set by the user**
- $50k → **$120k USD by 31 Dec 2026** (+140% in 31 trading days).
- → **NZD 5M by 31 Dec 2031**, which is about USD 2.75M at USD/NZD 1.817 (the rate on 17 Nov 2026).
- No new cash added; growth must come from trading.

**Market snapshot (16 Nov close)**
- SPY 739.95 (fell 1.9% on the day from 754.27)
- QQQ 661.80
- VIX 19.3 (it spiked to 28 on 5 Nov)
- SPY Dec-31 options: implied volatility around 15% near the money

**Feasibility analysis** (`sim/goal_odds.py`, results in `sim/goal_odds_output.txt`)
- Leverage alone (1–5× SPY) has a ~0% chance of +140% in 6 weeks.
- The best trade found is an all-in SPY 31-Dec 750/770 bull call spread: **32.8% chance of hitting $120k, 51% chance of ending below $25k.**
- The ceiling for a fairly priced bet is start ÷ goal = 41.7%.
- Goal 2 from $120k with 4× leverage: ~4%. Both goals combined: ~1–1.5%.
- I told the user plainly that the goals cannot be guaranteed. The user chose to proceed with the paper trade.

**Phase 1 trade plan**
- BUY 60 × (SPY261231C00750000 / SPY261231C00770000) bull call spread, limit net debit $8.33, total $49,980.
- Quotes on 16 Nov: 750C ask 13.38, 770C bid 5.05; mids 13.345 and 5.105, so mid debit ≈ 8.24.
- Maximum value 60 × $2,000 = **$120,000** if SPY ≥ 770 at expiry. Maximum loss is the debit paid.
- Management rules (see STRATEGY.md):
  - Hold to expiry.
  - Close early only if the spread is worth ≥ $19.50.
  - Close before the 31 Dec close if SPY is between 750 and 770 (assignment risk).
  - No averaging down and no rolling.

**Execution log**
- 2026-11-16 19:50 ET (market closed):
  - Submitted the multi-leg limit order (client id `phase1-spy-750-770-cs-20261117`). **Rejected: HTTP 403 "request is forbidden" (code 40310000).**
  - A 1-contract single-leg diagnostic order at $0.05 was rejected the same way.
  - Read-only API calls work, and the account shows `trading_blocked: false`, options level 3.
  - The cause is either the market being closed or the connector's API key lacking trading permission.
  - Next step: retry after the 17 Nov open.

## 2026-11-17 — Standing mandate

- **The user granted ongoing authority:** Claude may run any analysis needed and adjust the strategy as conditions change.
- **Hard limit, repeated by the user:** **no trading in the live IBKR account.**
- **Recorded in:** `CLAUDE.md` (standing instructions).
- **Monitoring:** a weekday check-in at 1:13 pm US Eastern was planned, but creating the recurring schedule was **denied by a permission check**. It is pending the user's approval. The one-off order retry at 9:45 am US Eastern on 17 Nov is still scheduled.
- **Update:** the user approved the daily check-in. It is now **active** every weekday at 1:13 pm US Eastern; the first run is 17 Nov 2026.
- **Update:** the check-in moved to **10:45 pm SGT, Mon–Fri** (the user is based in Singapore).
  - That is 9:45 am US Eastern now, 15 minutes after the US open. From 8 Mar 2027 (US daylight saving) it becomes 10:45 am US Eastern, still within US trading hours.
  - The separate one-off retry was removed, because the daily check-in fires at the same moment and now handles the order entry.
  - On 31 Dec the check-in runs at 9:45 am US Eastern, leaving about 6 hours before the close to apply the 750–770 exit rule.

## 2026-11-17 — Clarification: several trades allowed

- **User:** the strategy doesn't have to be a single trade; it can use several to reach the goal. If the current strategy is suitable, proceed as-is.
- **Assessment:** the single 750/770 spread stays as the opening trade.
  - With fair pricing, nothing beats the 41.7% ceiling, and splitting into smaller bets only adds costs and time decay.
  - Several trades help in two cases: if the market moves sharply, and in Phase 2.
- **Added to STRATEGY.md:** rules for using several trades during Phase 1:
  - take profit at ≥ $19.50
  - rotate into a new trade if the spread falls below $3 with at least 8 trading days left and a better option exists
  - put any spare cash into further defined-risk trades
  - no undefined risk
  - carry any remaining value into Phase 2
- **Decision:** proceed as-is. The order goes in at tonight's 10:45 pm SGT check-in.

## 2026-11-17 — Check-in #1 (10:45 pm SGT / 9:46 am US Eastern)

**Snapshot**
- SPY 738.3 (16 Nov close 740.04).
- 750C: bid 12.53, ask 12.60. 770C: bid 4.53, ask 4.59.
- 750/770 spread: mid ≈ $8.01, natural $8.07. Cheaper than yesterday's $8.33.
- Payout ratio at mid is about 2.5×, so 60 spreads still pay $120k for about $48.3k.
- 31 trading days to expiry (expiry 31 Dec). Implied volatility: 750C 15.9%, 770C 13.9%.

**Odds**
- Unchanged in substance. SPY needs ≥ 770, +4.3% from here.
- The risk-neutral probability implied by the spread price is about 40%. The simulation estimate is about 32–33%.

**Execution**
- Market OPEN. Placed BUY 60 × 750/770 spread, limit $8.05 (client id `phase1-spy-750-770-cs-20261117-r1`). **Rejected: HTTP 403 "request is forbidden" (40310000).**
- Diagnostic: a 1-share SPY stock limit order at $500 was **also rejected with 403**.
- The account config is normal: `suspend_trade: false`, `closing_transactions_only: false`, options level 3, $100k buying power.
- **Conclusion:** the cause is not market hours, options approval or the account's state. The Alpaca connector's credentials can read but cannot place orders, so every write call is forbidden. **The user needs to fix this** by reconnecting the Alpaca paper connector, or re-issuing its API key, with trading permission.

**Decision**
- No position yet. The strategy is unchanged.
- The daily check-in will retry each day. If entry is delayed, re-size so that payout ≈ $120k and total cost ≤ $50k.
- If entry slips past about 1 Dec, re-run the odds: with less time, the same strike needs a bigger move per day.

## 2026-11-17 — ✅ Phase 1 position OPENED (10:48 pm SGT / 9:48 am US Eastern)

- **Fix:** the user reconnected the Alpaca MCP connector. Orders are now accepted.
- **Order:** BUY 60 × SPY 31-Dec-2026 750/770 bull call spread, limit $8.05. Client id `phase1-spy-750-770-cs-20261117-r2`, order id `fb6dfbea-dba9-4127-b783-de46cc1bb0f9`.
- **Fill:** about 1 second after submission, at a **net debit of $7.91** (below the $8.05 limit):
  - Long 60 × SPY261231C00750000 @ $12.53
  - Short 60 × SPY261231C00770000 @ $4.62
- **Cost:** 60 × $791 = **$47,460**. The rest of the $50k sleeve, **$2,540**, stays in cash.
- **SPY at entry:** about 738.6.
- **Payoff at 31 Dec expiry:**

| SPY at expiry | Spread value | Sleeve total (incl. $2,540 cash) |
|---|---|---|
| ≤ 750 | $0 | $2,540 |
| 757.91 (breakeven) | $47,460 | $50,000 |
| 760 | $60,000 | $62,540 |
| ≥ 770 | **$120,000** | **$122,540** ✅ goal |

- **Payout ratio:** 2.53×, better than the 2.40× planned because the fill was cheaper.
- **Odds:** the price implies about a 40% chance of SPY ≥ 770; the simulation estimate is about 33%.
- **Risk rules now active** (STRATEGY.md):
  - take profit if the spread is worth ≥ $19.50
  - rescue-rotation review if the spread is worth < $3 with ≥ 8 trading days left
  - close before the 31 Dec bell if SPY is between 750 and 770
  - spare cash ($2,540) can go into further defined-risk trades if they add odds
- **Paper account after the trade:** about $52.5k cash plus the spread. The $50k outside the sleeve is untouched.

## 2026-11-18 — Check-in #2 (10:45 pm SGT / 9:45 am US Eastern)

**Snapshot**
- SPY 730.6. It fell 1.0% on 17 Nov (close 732.41, intraday low 727.02) and is lower again today.
- VIX 25.5 at the 17 Nov close (22.9 on the 16th). Implied volatility rose: 750C 16.9%, 770C 15.0%.
- Spread value ≈ $6.45 (750C $10.10, 770C $3.65), down 18.5% from the $7.91 entry.
- Sleeve value: 60 × $645 + $2,540 cash = **$41,240**, down 17.5%.
- Days to expiry: 30 trading days.

**Odds of SPY ≥ 770 on 31 Dec (needs +5.4%)**
- Lognormal model: 15.5% / 18.5% / 22.3% at volatilities of 15% / 17% / 20%.
- Bootstrap: 23.1%.
- The most any position could offer at this sleeve value is 41.66k ÷ 120k ≈ **34.7%**.

**Rotation analysis** (new script: `sim/rotation_check.py`)
- Exiting at the natural price would bring in about $39.1k, or $41.66k including cash.
- Best realistic re-deployment: 120 × **754/764** spreads at $3.47 natural. Odds would be 28.3% (bootstrap) or 23.6% (lognormal 18%), against 23.1% / 19.9% for holding: **+5.2 and +3.7 points.**
- Spreads only $1–3 wide looked better on paper (up to 51%), but those come from stale quotes and need more than 1,000 contracts. Excluded.

**Decision: HOLD.**
- No rule triggered: the spread is worth $6.45, well above the $3 rescue level and below the $19.50 take-profit.
- The rotation edge is under +5 points on the lognormal model and depends on noisy quotes. Moving after one day on a 1% dip would be churn.
- Added a standing rotation test to STRATEGY.md: rotate only if the improvement is ≥ 5 points on BOTH models.
- The VIX spike (25.5) makes new spreads more expensive, which is another reason not to rotate now.

## 2026-11-19 — Check-in #3 (10:45 pm SGT / 9:46 am US Eastern)

**Snapshot**
- SPY **737.3**, up 1.0% today. It closed 18 Nov at 730.33 after an intraday low of 726.90.
- VIX closed 18 Nov at 24.56, down from 25.46.
- **Data issue:** Alpaca option quotes have not updated since the 18 Nov close (timestamps 21:14 UTC), both in the chain and in the latest-quote endpoint, 16 minutes into today's session. Position marks are stale too.
- Spread at the 18 Nov close: 750C bid 9.45 / ask 9.66, 770C bid 3.38 / ask 3.45, mid ≈ $6.14.
  - Sleeve at the 18 Nov close ≈ 60 × $614 + $2,540 = **$39.4k**.
- Estimated value today: the spread's delta is about 0.21, so SPY's +7 adds about $1.5, putting the spread near **$7.6** and the sleeve near **$48k**.
- Implied volatility for the Dec-31 options fell to about 13–14% at the 18 Nov close, even with VIX in the mid-20s.

**Odds of SPY ≥ 770 on 31 Dec** (needs +4.4%, 29 trading days)
- Lognormal model: 17.2% / 21.3% / 23.9% at volatilities of 13.5% / 16% / 18%.
- Bootstrap: 28.7%.

**Rotation test:** not run, because the quotes are stale and a comparison on old prices would be meaningless. In any case, today's rally moves SPY toward the current strikes, which weakens the case for rotating.

**Decision: HOLD.** No rule triggered: the spread is about $6–7.6, between the $3 rescue level and the $19.50 take-profit. No orders placed.

**Follow-up:** if option quotes are still stale at the next check-in, treat it as a data-feed problem and tell the user.
