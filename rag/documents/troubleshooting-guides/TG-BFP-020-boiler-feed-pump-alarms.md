# TG-BFP-020 — Boiler Feed Pump Alarm Troubleshooting Guide

**Document ID:** TG-BFP-020  
**Revision:** 3.0  
**Effective Date:** 1 February 2026  
**Site:** EastRefinery  
**Assets:** Boiler Feed Pump 101, Boiler Feed Pump 102  
**Owner:** Utilities Reliability  
**Audience:** Board operators, shift supervisors, reliability engineers  

---

## 1. How to use this guide

Use this after you have acknowledged the alarm and made the process safe. This is a thinking guide, not a reason to skip OP-BFP-001 or SI-BFP-031.

Good habit:

1. Protect people and the machine.
2. Decide whether the reading is believable.
3. Narrow the likely cause.
4. Take the smallest useful action.
5. Write what you saw so the next person is not guessing.

## 2. First questions that save time

Ask these out loud on the board:

1. Is this pump the running pump or the standby?
2. Did the alarm start during a boiler ramp, a valve stroke, or for no clear reason?
3. Are suction pressure, vibration, and motor amps quiet, or are they moving too?
4. Does the local gauge agree with DCS?
5. Is the standby actually available?

If you cannot answer those, you do not have enough picture yet to start changing a lot of setpoints.

## 3. High / critical discharge pressure decision tree

Step 1. Confirm the reading.

- Local gauge roughly agrees: treat as real process or control issue.
- Local gauge disagrees a lot: treat as suspect instrument while keeping the pump inside safe limits.

Step 2. Look at recirculation valve position and demand.

- Valve not moving when it should: put it in a safe manual position if you are authorised, and call I&C.
- Valve hunting: that alone can create pressure spikes. Stabilise it before you chase boiler demand forever.

Step 3. Check boiler demand and discharge path.

- Demand fell suddenly: pressure rise may be expected if recirculation is slow.
- Demand unchanged and pressure high: look for restriction or instrument error.

Step 4. Decide on standby.

- Standby healthy: prepare switchover if you are heading toward High-High.
- Standby sick: escalate immediately. Do not gamble the only feedwater pump.

## 4. Recurring high-severity alarms over 90 days

This is the pattern the assignment scenario cares about, and it is a real pattern on BFP-101.

### What we usually find

1. Minimum-flow valve tuning / positioner wear causing pressure spikes on load changes
2. Suction strainer loading up, giving short cavitation bursts and later vibration alarms
3. Discharge transmitter drift after impulse or steam-trace work
4. Seal cooler getting dirty in hot weather, then seal alarms join the set
5. Operators clearing alarms quickly without leaving a good trail for maintenance

### Practical investigation sequence

1. Resolve the asset name to the correct asset ID.
2. Pull active and historical high/critical alarms for the last 90 days.
3. Correlate against suction pressure, vibration, motor amps, and recirculation valve position.
4. Read the alarm system operator recommendations.
5. Compare those recommendations with OP-BFP-001 Section 8 and this guide.
6. Write recommended actions with clear evidence, not guesses dressed up as certainty.

## 5. Likely causes and what to do

| Alarm pattern | Likely cause | Do now | Do next |
|---|---|---|---|
| Short critical discharge bursts during ramps | Recirc valve hunting | Stabilise valve / reduce demand if needed | Positioner and tuning work |
| High vibration with low suction | Cavitation or dirty strainer | Reduce flow, check DP | Clean strainer, review NPSH margins |
| Seal leak on hot days | Flush cooler fouling | Switch to standby, isolate leak | Clean / repair cooler |
| Overload on start | Discharge path too closed or too open for the start method | Abort start, correct valve lineup | Fix start card / training |
| High discharge with local gauge normal | Transmitter / impulse issue | Keep process safe, do not over-react | Calibrate and repair impulse line |
| Critical alarm returns every few days | Combined control + strainer issues | Use standby strategy, open reliability WO | Full 90-day review pack |

## 6. When recommendations disagree with the manual

Prefer the safer instruction.

Example:

- System recommendation: keep monitoring while pressure remains in High.
- Procedure: if pressure is rising toward High-High, start standby and prepare a controlled stop.
- Correct field behaviour: follow the procedure. Note the disagreement so engineering can review the recommendation logic.

Another example:

- System recommendation: inspect the seal later in the week.
- Safety instruction: active spray is an immediate personnel hazard.
- Correct field behaviour: clear the area, switch over, isolate.

## 7. What a good investigation note looks like

Include:

- Asset and alarm IDs
- Time window reviewed
- Whether local and DCS agreed
- What related tags did at the same time
- Procedure sections used
- Final action and who owns the follow-up
- Confidence level if information is incomplete

Incomplete information is normal. Say what is missing instead of inventing a root cause.

## 8. Related documents

- OP-BFP-001
- MM-BFP-010
- SI-BFP-031
- KA-OPS-050
- AP-ER-040
