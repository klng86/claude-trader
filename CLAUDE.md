# Standing instructions for Claude in this repo

## Hard rules
1. **Never trade on IBKR.** Do not place, modify or cancel any order, alert or watchlist on Interactive Brokers. Read-only IBKR data calls are allowed only for research.
2. **Trade only in the Alpaca paper account,** through the `mcp__Alpaca_Paper_Trading__*` tools.
3. The strategy trades a **$50,000 sleeve** of the $100k paper account. Treat the other ~$50k as untouchable.
4. Never add capital or reset the account to manufacture progress.

## Mandate (from the user)
- **Targets:** $120k USD by 31 Dec 2026, then NZD 5M by 31 Dec 2031. Convert at the USD/NZD rate on that day.
- **Analysis and adjustments:** Claude may run any analysis needed and adjust the strategy as conditions change, without asking first, as long as the hard rules above hold.
- **Record keeping:** every analysis, decision, order, fill and strategy change goes in `journal/JOURNAL.md`, newest entry at the bottom. Any change to the plan or risk rules also updates `STRATEGY.md`. The Status section of `README.md` stays current.
- **Git:** commit and push after each update, to branch `claude/happy-hopper-8qjp0n`.

## Schedule
- **9:40 pm SGT, pre-market prep (read-only):**
  - Covers news, economic data and SPY's pre-market price.
  - Writes a "Today's plan" entry in the journal.
- **11:15 pm SGT, main check:** the only check-in that may trade, on the Alpaca paper account only.
- Times assume US standard time. When US daylight saving starts on 8 Mar 2027, the pre-market check would land at the open, so review the schedule before then.

## Routine on each check-in
1. Read the market clock, the account, positions and open orders on Alpaca paper.
2. Update the market snapshot: SPY, VIX, the spread's value, days to expiry.
3. Re-check the odds of reaching the target with the latest prices. Use `sim/goal_odds.py`, or a quick analysis for the current position.
4. Apply the risk rules in `STRATEGY.md`. Act only when a rule triggers or the analysis clearly justifies a change, and log the reason.
5. Journal, update the README status, commit, push. Tell the user if anything material happened.
