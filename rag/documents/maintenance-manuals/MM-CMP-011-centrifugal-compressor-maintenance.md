# MM-CMP-011 — Centrifugal Compressor Maintenance Manual

**Document ID:** MM-CMP-011  
**Revision:** 2.5  
**Effective Date:** 20 October 2025  
**Site:** EastRefinery  
**Assets:** Compressor C-201, Compressor C-202  
**Owner:** Rotating Equipment / Process Area Maintenance  

---

## 1. Purpose

Maintenance guidance for C-201 and C-202, especially where discharge pressure alarms, surge-margin problems, and cooler fouling show up together. Operations run the machine with OP-CMP-002. This manual is for the people who open, calibrate, stroke, and overhaul the supporting gear.

## 2. What fails first on this site

From the last two years of work orders:

1. Discharge cooler fouling in dusty / high ambient periods
2. Anti-surge positioner sticking after long periods near one position
3. Impulse-line condensate after poorly drained steam-trace work
4. Transmitters left with old calibration after range changes
5. Recurring near-surge operation wearing seals and bearings faster than the plan assumed

## 3. Predictive and routine monitoring support

Help operations by making these checks real, not paperwork:

1. Review discharge and suction pressure with recycle valve position, not as separate trends.
2. Track cooler approach temperature. Rising approach with steady duty usually means fouling.
3. Look at vibration and thrust weekly, and after any surge event.
4. Confirm anti-surge transmitter and valve feedback monthly.
5. After any “nuisance high discharge pressure” claim, prove whether the process gauge and DCS agree.

## 4. Maintenance response to discharge pressure alarms

Work the likely causes in this order unless evidence points elsewhere:

1. Prove the instrument. Compare DCS to a trusted local gauge. Check impulse lines for condensate or blockage.
2. Inspect discharge cooler condition and fan operation.
3. Stroke the anti-surge valve. Check for stick-slip and wrong position feedback.
4. Look downstream for a control valve or process restriction.
5. Only after the above, talk about alarm rationalisation with the alarm philosophy owner.

If discharge temperature is high at the same time, cooler and load issues jump ahead of “maybe the transmitter is wrong.”

## 5. Surge-related findings

- Long periods with low surge margin age seals and bearings.
- Low suction plus a busy recycle valve often means the problem is upstream, not “bad compressor guts.”
- Raising discharge setpoint to escape a nuisance alarm is a bad trade if surge margin is already thin.

After a real surge event, schedule at least a vibration review and a seal leak check before calling the job closed.

## 6. Alignment with operator recommendations from the alarm system

Treat API or copilot recommendations as advisory text.

Cross-check against:

- This manual
- OP-CMP-002
- SI-CMP-032

Reject recommendations that say, in effect, keep running while discharge temperature stays high and pressure is already in alarm. On this plant, load reduction and cooling recovery come first.

## 7. Typical maintenance work packages

### Cooler clean

Include fan checks, bundle condition, and a post-clean approach-temperature comparison against the last clean baseline.

### Anti-surge valve service

Include stroking, positioner calibration, air supply quality, and a functional check with operations watching surge margin.

### Transmitter / impulse work

Include drain/vent discipline, leak check, and a two-point comparison before handover.

## 8. Related documents

- OP-CMP-002
- TG-CMP-021
- SI-CMP-032
- AP-ER-040
