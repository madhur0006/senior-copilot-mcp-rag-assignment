# OP-MTR-003 — Critical Motor Start and Trip Response Procedure

**Document ID:** OP-MTR-003  
**Revision:** 1.4  
**Effective Date:** 10 January 2026  
**Site:** EastRefinery  
**Assets:** Motor M-501, Motor M-502, Boiler Feed Pump motors, other critical service motors listed on the Unit 5 critical motor register  
**Units:** Unit 5 primarily; same rules apply to BFP motors in Unit 2 and Unit 3  
**Owner:** Electrical Operations / Area Operations  
**Audience:** Board operators, field operators, electrical technicians, shift supervisors  

---

## 1. Purpose

This procedure is for the first minutes after a critical motor trip, and for deciding when a restart is allowed. A motor trip is not only an electrical event. The driven pump or compressor is usually part of the story.

## 2. Golden rule

Do not restart a critical motor just because the process is hurting. Find out why it tripped, protect people, start approved standby equipment if you have it, then investigate.

## 3. Immediate response after a motor trip alarm

1. Leave the motor stopped.
2. Read the trip reason from DCS, MCC, or relay display. Write it down before someone resets it.
3. Check what the driven equipment is doing and what the process lost.
4. Start the approved standby machine if the lineup allows it and it is healthy.
5. Call electrical maintenance and the shift supervisor for critical service.
6. Keep the area clear if there was smoke, a bang, or a burning smell.

Useful radio language:

- “M-501 tripped on overcurrent at 14:12. Standby not yet started. No smoke reported.”
- Better than: “Motor tripped, we are looking into it.”

## 4. Common trip causes and first checks

| What the relay / DCS says | Check first | Restart now? |
|---|---|---|
| Overcurrent / overload | Locked rotor, jammed driven machine, process overload, phase imbalance | No |
| Ground fault | Cable damage, water in terminal box, wet insulation | No |
| High winding temperature | Lost cooling fan, dirty filters, long overload | No, cool down and fix cause |
| Bearing temperature high | Grease, alignment, coupling, bearing damage | No |
| Undervoltage / bus event | Upstream feeder or plant power quality | Only after power is stable |
| Manual stop / interlock | Confirm whether someone stopped it for a reason | Only if the stop reason is cleared |

## 5. Related assets you should inspect

A motor trip investigation that only looks at the motor is incomplete.

Always look at:

1. Driven pump, compressor, or fan
2. Coupling and coupling guard
3. Motor bearings and driven-equipment bearings
4. Local valves that can put a heavy start load on the motor
5. MCC feeder, contactor, overload, and protection relay
6. Whether other motors on the same bus saw a dip

If the motor belongs to a boiler feed pump, also check:

- Suction strainer DP at the time of trip
- Minimum-flow valve position
- Discharge valve position during the start attempt
- Seal flush running state
- Any active BFP pressure or vibration alarms just before the trip

## 6. Field checks before maintenance arrives

From a safe position:

1. Smell and look for smoke at the motor and terminal box.
2. Check whether the coupling guard is hot or discoloured.
3. Listen only if the machine is still coasting and it is safe. Do not remove guards.
4. Confirm the local isolator state and whether emergency stop was pressed.
5. Do not open the terminal box until electrical has it under LOTO.

## 7. Restart criteria

Restart is allowed only when all of these are true:

1. Trip cause is identified and corrected, or a competent person has cleared the machine in writing.
2. Electrical insulation checks are acceptable where required.
3. The train turns freely if there was any suspicion of seizure.
4. Process conditions are inside the start envelope for the driven equipment.
5. Standby strategy is understood if this start fails again.
6. Supervisor approval is recorded for critical service motors.

If any item is missing, keep the motor locked out and use standby or reduce rate.

## 8. After a successful restart

1. Stay on the board for the first 15 to 30 minutes.
2. Watch amps, winding or bearing temperature if available, and driven-equipment alarms.
3. Ask the field for one confirmation walkdown.
4. Write the restart time and remaining follow-up work in the log.
5. Do not close the work order just because the motor is turning again.

## 9. Recurring trips

If the same motor trips more than once in a short period:

1. Stop the restart cycle.
2. Treat it as a reliability event, not bad luck.
3. Pull trends for amps, temperature, and driven-equipment load.
4. Use TG-MTR-022 and MM-MTR-012.
5. Hand the issue to electrical and rotating together, not one team in isolation.

## 10. Related documents

- MM-MTR-012 Critical Motor Maintenance Manual
- TG-MTR-022 Motor Trip Alarm Troubleshooting Guide
- SI-GEN-030 Alarm Response Safety Instructions
- OP-BFP-001 when the motor drives a boiler feed pump
