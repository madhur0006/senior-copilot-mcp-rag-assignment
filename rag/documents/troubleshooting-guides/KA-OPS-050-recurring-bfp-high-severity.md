# KA-OPS-050 — Service Knowledge Article: Recurring BFP High-Severity Alarms

**Document ID:** KA-OPS-050  
**Revision:** 1.1  
**Effective Date:** 12 April 2026  
**Site:** EastRefinery  
**Assets:** Boiler Feed Pump 101, Boiler Feed Pump 102  
**Type:** Service knowledge / closed investigation notes  
**Prepared by:** Utilities Reliability after WO-88421 and WO-89102  

---

## Summary

Over two recent quarters, Unit 2 saw repeated high and critical alarms on Boiler Feed Pump 101. The loudest ones were high discharge pressure. High vibration showed up as a second act, usually after the pressure events, especially when the suction strainer was getting dirty.

This note exists so the next shift or the next engineer does not have to rediscover the same story from scratch.

## What people saw on shift

- Clusters of high/critical alarms inside 90-day windows
- Many events during boiler load ramps
- Recirculation valve moving like it could not decide where to sit
- Operators saying “pressure jumped, then came back”
- A few seal dampness reports on warmer weeks, not always in the same hour as the pressure spikes

## What maintenance found

1. Recirculation valve positioner worn and slow to respond
2. Suction strainer DP higher than the operators had been watching day to day
3. Discharge transmitter calibration off enough to exaggerate some peaks
4. No major impeller damage on the first teardown window
5. Seal cooler starting to foul, which explained the separate seal complaints more than the pressure spikes

## What actually helped

1. Cleaned the suction strainer and put a clearer DP watch in place
2. Replaced the recirculation positioner and retuned the loop with process support
3. Recalibrated the discharge pressure transmitter and cleaned the impulse line
4. Re-briefed the shift on OP-BFP-001 Section 8 response, especially standby switchover near High-High
5. Kept BFP-101 on a reliability watch list for 60 days after the fix

After that work, the critical bursts dropped sharply. We still see ordinary High warnings on big ramps, but not the same repeated critical pattern.

## Were the computer recommendations consistent with the manuals?

Mostly yes on direction, not always on urgency.

- The alarm system often suggested checking recirculation and confirming standby readiness. That matched the manuals.
- Some recommendations were softer than SI-BFP-031 and OP-BFP-001 when pressure was climbing hard. In those moments the written procedure was stricter, and the shift was right to follow the procedure.

Lesson for anyone building or using a copilot: show both sources, and when they disagree, prefer the safety-conservative document.

## Evidence pack worth repeating on the next similar job

1. Asset search for Boiler Feed Pump 101
2. Historical high/critical alarms for the last 90 days
3. Correlation and priority information
4. Operator recommendations from the alarm platform
5. Passages from OP-BFP-001, TG-BFP-020, MM-BFP-010, and SI-BFP-031

## Open watch items

- Confirm strainer DP alarm is visible enough on the board
- Recheck recirculation tuning after the next major turnaround
- Keep an eye on BFP-102 for the same pattern if it inherits older positioner hardware

## Related documents

- OP-BFP-001
- TG-BFP-020
- MM-BFP-010
- SI-BFP-031
- AP-ER-040
