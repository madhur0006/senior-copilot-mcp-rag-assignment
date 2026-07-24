# AP-ER-040 — EastRefinery Alarm Management Philosophy

**Document ID:** AP-ER-040  
**Revision:** 3.0  
**Effective Date:** 1 July 2025  
**Site:** EastRefinery  
**Owner:** Alarm Management Team  
**Approved by:** Operations Manager, Process Safety  

---

## 1. Purpose

This philosophy explains how alarms are supposed to behave at EastRefinery: which ones deserve to exist, how they are prioritised, when they get rationalised, and what good alarm response looks like. It is not a substitute for equipment procedures. It is the shared rulebook above them.

## 2. What an alarm is for

An alarm should tell an operator that a process or equipment condition needs attention in time to prevent a worse consequence. If nobody can do anything useful with it, it should not be an alarm.

Good alarms are:

- Relevant
- Unique for a consequence where practical
- Prioritised honestly
- Documented with a response
- Tested after changes

Bad alarms are:

- Noise that people learn to ignore
- Duplicates of the same problem
- Stale conditions with no action path
- Standing alarms that stay in for days without ownership

## 3. Priority definitions

| Priority | Meaning | Target first response |
|---|---|---|
| Critical | Immediate threat to safety, environment, or major equipment damage | Immediate |
| High | Significant upset likely if not corrected soon | Within about 5 minutes |
| Medium | Degraded condition needing planned action | Within about 30 minutes |
| Low | Advisory / informational | By end of shift or by work order process |

Priority is about consequence and urgency, not about how annoyed the shift is by the sound.

## 4. Priority scoring used in investigations

When tools calculate a priority score, the useful drivers on this site are:

1. Configured severity
2. Asset criticality
3. Potential consequence if ignored
4. Time already spent in alarm
5. Related consequential alarms
6. Whether the alarm is actionable now

If someone asks which alarm is highest priority in EastRefinery, the answer should name the drivers, not only print a number.

## 5. Rationalisation rules

An alarm may become a rationalisation candidate when:

1. It repeats often with little or no useful consequence
2. It stays stale for long periods without a real action path
3. Better instrumentation or logic can replace it
4. Several alarms are telling the same story badly

Important limits:

- Rationalisation needs Management of Change.
- Copilot systems may identify candidates.
- Copilot systems must not auto-suppress or delete alarms.

## 6. Expected evidence for recurring high-severity investigations

For jobs such as investigating recurring high-severity alarms on Boiler Feed Pump 101 over 90 days, the investigation pack should include:

1. Correct asset identification
2. Alarm history for the chosen window
3. Correlation or contributing factors
4. Applicable operating procedure and safety citations
5. Recommended actions with owners
6. A clear note when API recommendations and written procedures disagree

## 7. Roles

| Role | Alarm duty |
|---|---|
| Board operator | First response, logging, escalation |
| Shift supervisor | Priority calls during floods, inhibits approval |
| Alarm owner / engineer | Design quality, rationalisation, MOC |
| Reliability | Recurring bad actors and equipment follow-up |
| Process safety | Consequence judgements on critical alarms |

## 8. Performance ideas the site watches

These are not vanity metrics. They tell us whether the alarm system is helping or shouting:

- Number of standing alarms
- Frequent bad actors
- Time to acknowledge critical alarms
- Flood events per month
- Recurring critical alarms on the same asset

## 9. Related documents

- SI-GEN-030
- TG-PRI-023
- Unit operating procedures
- Site MOC procedure
- ISA-18.2 / IEC 62682 aligned practices adapted for this site
