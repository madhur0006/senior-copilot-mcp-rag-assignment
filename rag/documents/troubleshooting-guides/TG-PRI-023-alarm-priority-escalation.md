# TG-PRI-023 — Alarm Priority and Escalation Troubleshooting Guide

**Document ID:** TG-PRI-023  
**Revision:** 1.2  
**Effective Date:** 15 November 2025  
**Site:** EastRefinery  
**Owner:** Alarm Management Team / Operations Excellence  

---

## 1. Purpose

Help operators and engineers answer questions like “which alarm matters most right now, and why?” without sorting only by colour on the screen.

## 2. How priority is judged on this site

Priority goes up when more of these are true:

1. Severity is Critical or High
2. The asset is critical service (boiler feed, compressor anti-surge path, safety-related motors, and similar)
3. The alarm is active and not acknowledged
4. Related consequential alarms are present
5. Time in alarm has passed the response target in AP-ER-040
6. Standing still will likely damage equipment, hurt people, or force a unit upset

A Medium alarm on a critical path can outrank a High alarm on a spare with no consequence. Read the whole picture.

## 3. Working method for “highest priority in EastRefinery”

1. Get the active alarm list for the site or unit.
2. Pull priority scores for the top candidates.
3. Check asset criticality and what else is alarming around them.
4. Explain the winner using the score drivers, not only the word Critical.
5. Point to AP-ER-040 and the equipment procedure that applies.

Example of a useful answer:

“Alarm A on BFP-101 scores highest because it is Critical, the pump is in critical service, it has been active for 12 minutes, and vibration is rising with it. Alarm B is also High, but it sits on a spare machine with no process consequence right now.”

## 4. Escalation expectations

| Condition | Who to call |
|---|---|
| Critical unacknowledged more than about 5 minutes | Shift supervisor |
| Several critical alarms in one unit (flood) | Shift supervisor and process support |
| Safety interlock or leak / fire / toxic concern | Follow SI-GEN-030 and emergency response |
| Same critical alarm recurring more than five times in 30 days | Reliability work order and supervisor |

## 5. Alarm floods

When the screen is noisy:

1. Protect safety and stabilise the unit first.
2. Work consequential alarms linked to trips and interlocks.
3. Use only approved shelving rules. Do not invent your own suppress list.
4. After the dust settles, capture which alarms were noise so rationalisation can be considered later.

## 6. Copilot / investigation output expectations

If a tool answers a priority question, it should show:

- The selected alarm
- Score or ranking basis
- Related alarms considered
- Procedure or philosophy citations
- Any uncertainty if the priority service was unavailable

## 7. Related documents

- AP-ER-040
- SI-GEN-030
- Equipment-specific OP / TG documents
