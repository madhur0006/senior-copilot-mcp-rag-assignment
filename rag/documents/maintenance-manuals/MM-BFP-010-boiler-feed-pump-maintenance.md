# MM-BFP-010 — Boiler Feed Pump Maintenance Manual

**Document ID:** MM-BFP-010  
**Revision:** 4.0  
**Effective Date:** 1 August 2025  
**Site:** EastRefinery  
**Assets:** Boiler Feed Pump 101, Boiler Feed Pump 102  
**Owner:** Rotating Equipment / Utilities Maintenance  

---

## 1. Overview

This manual is for mechanics, rotating engineers, and planners working on BFP-101 and BFP-102. Operators should use OP-BFP-001 for running the pumps. This document covers what to inspect, what to change, and how to judge whether an alarm is a process problem, an instrument problem, or real machine wear.

## 2. Machine summary

Both pumps are boiler feed service, high discharge pressure, with mechanical seals and a minimum-flow recirculation line. They sit on critical service. A messy repair on one pump is not “just a pump job” if the standby is weak.

Known site notes:

- BFP-101 has a history of recirculation valve positioner wear.
- BFP-102 seal cooler fouled badly in summer 2025 during high cooling-water temperature.
- Both pumps show false discharge pressure scares when impulse lines are not drained after steam-trace work.

## 3. Preventive maintenance

| Task | Interval | What “acceptable” means |
|---|---|---|
| Vibration survey | Monthly | Overall usually under 4.5 mm/s; no new high peak at running speed or blade pass without explanation |
| Bearing temperature review | Weekly | Stable trend, normally under 75 C |
| Seal flush and cooler check | Monthly | Correct pressure/flow; cooler not plugged |
| Suction strainer clean | Quarterly, or earlier on high DP | DP back in normal band |
| Coupling alignment | Semi-annual, and after intrusive work | Within current OEM / site tolerance sheet |
| Oil / grease condition | Per lube route | No burnt smell, correct level, no water |
| Motor insulation tests | Annual or after trip/moisture event | Per electrical standard |

If the pump has been alarming a lot, do not wait for the calendar. Bring the checks forward.

## 4. Corrective guidance by symptom

### 4.1 High vibration

Work through it in order:

1. Collect overall vibration and, if possible, spectrum / phase.
2. Check soft foot, base bolts, and foundation condition.
3. Check coupling alignment and insert condition.
4. Rule out cavitation using suction pressure, strainer DP, and sound reports from operations.
5. Look at impeller balance and wear-ring clearances if the pump is opened.
6. If bearings are noisy or hot, plan replacement rather than greasing forever.

Do not hand the pump back with “vibration acceptable after reset” if you never found a cause.

### 4.2 Seal leak

1. Confirm flush pressure and cooler outlet temperature before blaming the seal faces alone.
2. Isolate, LOTO, and depressurise fully before breaking containment.
3. Inspect seal faces, O-rings, and whether pipe strain is twisting the seal chamber.
4. Replace the cartridge if leakage is above the operating limit or if faces are damaged.
5. After return to service, watch the seal for the first hours with operations.

### 4.3 Recurring high discharge pressure

Operations often ask maintenance whether the pump is “blocking” discharge. On these machines, the more common maintenance finds are:

1. Discharge transmitter out of calibration
2. Impulse line partially blocked or full of condensate
3. Discharge check valve sticky
4. Minimum-flow valve positioner worn or calibrated badly
5. Control loop tuned so the valve hunts during boiler ramps

Suggested shop / field actions:

1. Calibrate or compare the discharge transmitter against a known gauge.
2. Stroke the recirculation valve and look at actual vs demanded position.
3. Inspect the check valve if operations report chatter or reverse flow signs.
4. Sit with process / I&C on tuning if the valve is healthy but still hunting.

### 4.4 Low flow / poor feed to boiler

Check wear rings, impeller condition, suction path, and whether recirculation is stuck open more than it should be. A pump can look “fine” electrically and still fail to make flow if internals are worn.

## 5. How to treat Alarm API / copilot recommendations

Computer recommendations are useful starting points. They are not a work instruction.

Before acting on them:

1. Read the matching section in OP-BFP-001 and SI-BFP-031.
2. Reject anything that implies bypassing interlocks or running through High-High pressure.
3. Prefer switchover to standby and a controlled isolation when the machine is in real danger.
4. Write in the work order whether you agreed with the recommendation or why you did not.

Example of a healthy disagreement:

- Recommendation: continue monitoring while pressure stays in High.
- Manual / procedure expectation: if pressure is climbing toward High-High, start standby and take the pump off carefully.
- What to do: follow the procedure, then note the conflict so the recommendation logic can be improved later.

## 6. Spares that should not run out

Keep these available or on a short lead-time agreement:

- Mechanical seal cartridge
- DE and NDE bearings
- Coupling inserts
- Wear rings
- Recirculation valve positioner soft parts
- Transmitter impulse fittings and block/bleed valves

## 7. Return-to-service checks

After maintenance:

1. Confirm lineup with operations.
2. Confirm guards fitted.
3. Confirm instruments returned to service, not left in bypass.
4. Start per OP-BFP-001.
5. Take a fresh vibration and temperature baseline and store it.

## 8. Related documents

- OP-BFP-001
- TG-BFP-020
- SI-BFP-031
- KA-OPS-050
- OP-MTR-003 for motor work
