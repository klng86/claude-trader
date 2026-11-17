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
