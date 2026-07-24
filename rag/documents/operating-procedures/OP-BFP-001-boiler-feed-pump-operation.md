# OP-BFP-001 — Boiler Feed Pump 101/102 Operating Procedure

**Document ID:** OP-BFP-001  
**Revision:** 3.2  
**Effective Date:** 1 November 2025  
**Site:** EastRefinery  
**Assets:** Boiler Feed Pump 101 (BFP-101), Boiler Feed Pump 102 (BFP-102)  
**Units:** Unit 2, Unit 3  
**Owner:** Utilities Operations  
**Reviewed by:** Reliability Engineering, Process Safety  
**Audience:** Control room operators, field operators, shift supervisors, reliability engineers  

---

## 1. Purpose

This procedure tells the shift how to start, run, respond to alarms, and shut down Boiler Feed Pumps 101 and 102. These pumps feed the boilers. If either pump is mishandled, you can lose boiler level, damage seals and bearings, or put people next to a hot high-pressure leak.

Use this document together with SI-BFP-031 for safety rules and MM-BFP-010 when maintenance work is needed.

## 2. Scope

Covers:

- BFP-101 and BFP-102 pump casings, couplings, and baseplates
- Drive motors and local start stations
- Suction and discharge isolation valves
- Minimum-flow recirculation valve and bypass
- Mechanical seals and seal flush / cooler
- Local gauges and DCS transmitters for pressure, vibration, bearing temperature, and seal leak detection

Does not cover boiler drum level control strategy details. Those stay in the boiler operating procedure.

## 3. Roles

| Role | Responsibility |
|---|---|
| Board operator | Watches DCS alarms, trends, and setpoints; coordinates switchover |
| Field operator | Does local valve checks, listens for cavitation, reports leaks and smell/noise changes |
| Shift supervisor | Approves abnormal running, standby unavailability, and restart after trip |
| Reliability / rotating | Owns vibration diagnosis and longer-term fixes |

## 4. Prerequisites before startup

Do not start a pump until all of the following are true:

1. No open permit that blocks starting the selected pump.
2. Deaerator / suction tank level is above the low-low interlock and stable.
3. Cooling water to the seal cooler is open and returning warm (not dead cold with no flow).
4. Seal flush pressure is in the normal band marked on the local board.
5. DCS communication to the pump tags is healthy. Bad quality tags are not “good enough to start.”
6. The standby pump is available, or the supervisor has recorded why it is not.
7. Suction strainer differential pressure is not already in alarm.
8. Field walkdown complete: no open flanges, no oil under the coupling, guards in place.

## 5. Normal operating envelope

These numbers are the day-to-day guide. If your local nameplate or latest MOC differs, follow the approved local values and note the difference in the shift log.

| Parameter | Normal | Alarm | Trip / forced action |
|---|---|---|---|
| Discharge pressure | 85 to 95 barg | High at 100 barg | High-High at 105 barg |
| Suction pressure | 2.5 to 4.0 barg | Low at 1.8 barg | Low-Low at 1.2 barg |
| Vibration (DE / NDE) | under 4.5 mm/s | High at 7.1 mm/s | High-High at 11.2 mm/s |
| Bearing temperature | under 75 C | High at 85 C | High-High at 95 C |
| Motor amps | near nameplate after settle | High / overload | Trip per motor protection |
| Seal leakage | damp / trace | visible drip | Isolate if spraying |

Notes from experience on this site:

- BFP-101 tends to run a little noisier than BFP-102 after the 2024 coupling change. Noise alone is not a trip, but rising vibration with noise is.
- During hard boiler load ramps, discharge pressure can spike briefly if the recirculation valve is slow. Watch the valve position trend, not only the pressure number.

## 6. Startup sequence

1. Tell the field operator which pump you are starting and confirm standby status.
2. Open the suction isolation valve fully. Leave no “almost open” positions.
3. Set the minimum-flow recirculation valve to the start position used for that pump (see local start card on the panel).
4. Crack open the discharge isolation so the check valve can seat properly once flow starts.
5. Start the motor from DCS. Watch starting amps and listen on radio for unusual noise from the field.
6. After the motor settles, raise discharge pressure in a controlled way using discharge valve and recirculation. Do not slam the discharge open.
7. Confirm seal flush and bearing temperatures are moving in the right direction within the first 10 minutes.
8. Put the pump on automatic control only after it has been stable for about 10 minutes.
9. Write the start time, vibration baseline, and any odd observations in the shift log.

If the pump does not build pressure, trips on start, or sounds like gravel (cavitation), stop. Do not keep restarting hoping it will “come good.”

## 7. Normal running checks

Every shift, at least once while the pump is in service:

1. Compare DCS discharge pressure with the local gauge. A growing gap usually means instrument drift or impulse-line trouble.
2. Look at suction pressure and strainer DP together. Low suction with rising DP points to the strainer first.
3. Check recirculation valve is not hunting. Continuous hunting wears the positioner and spikes discharge pressure.
4. Walk the seal area from a safe distance. A new drip pattern matters even if the alarm has not come in yet.
5. Confirm standby pump readiness: power available, valves in standby lineup, no active critical alarms on the spare.

## 8. Alarm response

### 8.1 High or critical discharge pressure

1. Acknowledge the alarm and note the time.
2. Check a second reading (local gauge or redundant transmitter) before you change a lot of process.
3. If the reading is real:
   - Reduce boiler demand only if the board strategy allows it.
   - Open recirculation to relieve the discharge.
   - Check whether the discharge valve or check valve is behaving oddly.
4. If pressure keeps climbing toward High-High, start the standby pump and prepare a controlled stop of the affected pump.
5. Do not bypass the pressure interlock to keep the boiler comfortable.

Common real causes on BFP-101/102:

- Recirculation valve stuck or hunting
- Sudden loss of boiler demand with slow control response
- Downstream restriction
- Transmitter reading high while the local gauge is normal (instrument issue)

### 8.2 Low suction pressure

1. Check suction tank / deaerator level.
2. Check strainer DP and upstream feed.
3. If the pump starts to sound like cavitation, reduce flow.
4. At Low-Low, expect the trip. Bring the standby across and leave the tripped pump for investigation.

### 8.3 High vibration

1. Compare against the last good baseline, not against memory.
2. Ask the field for noise, smell of hot oil, and whether the base feels unusual.
3. Check for cavitation symptoms, loose bolts, and coupling condition.
4. At High-High, trip the pump and start standby. Do not “ride it” because the boiler needs water.
5. Keep the pump tagged out for rotating equipment until they clear it.

### 8.4 Seal leak high

1. Treat spray as a personnel hazard, not a housekeeping issue.
2. Keep people out of the line of fire.
3. Switch to standby from the board if you can.
4. Isolate and depressurise under LOTO before anyone works on the seal.
5. Call maintenance and safety. Record photos if it is safe to take them from a distance.

### 8.5 Motor overload or motor-related alarms

1. Do not keep starting into an overload.
2. Check discharge valve position and whether the pump is trying to push against a closed or near-closed path.
3. Follow OP-MTR-003 if the motor trips.

## 9. Recurring high-severity alarms (what the shift should do)

If BFP-101 or BFP-102 keeps throwing high or critical alarms over days or weeks:

1. Pull 90-day trends for discharge pressure, suction pressure, vibration, motor amps, and recirculation valve position.
2. Write down whether the alarms line up with boiler load changes.
3. Check strainer history and cooler performance.
4. Compare any computer-generated operator recommendations with Section 8 of this procedure and with MM-BFP-010.
5. If the same critical alarm comes back more than five times in 30 days, raise it to reliability and open a proper work order. Do not keep clearing and hoping.

This is the pattern we have already seen on BFP-101: recirculation hunting plus a dirty suction strainer during load swings.

## 10. Related equipment to look at

When the alarm is on the pump, still check:

- Pump motor and coupling
- Suction strainer and suction isolation valve
- Minimum-flow recirculation valve and positioner
- Discharge check valve and isolation valve
- Seal flush cooler and orifice
- Pressure transmitters PT-BFP-101 / PT-BFP-102 and their impulse lines
- Local seal leak detector and junction box

## 11. Controlled shutdown

1. Confirm standby is running and stable if the unit still needs feedwater.
2. Reduce load on the pump being stopped.
3. Stop the motor from DCS.
4. Close discharge isolation as required by the local lineup.
5. Leave suction and auxiliary systems in the state required for standby or maintenance.
6. If handing to maintenance, apply LOTO and complete the permit.

## 12. Restart after trip or maintenance

Do not restart until:

1. The trip cause is known, or maintenance has cleared the machine.
2. Free rotation has been checked if the pump was opened or seized.
3. Instruments that contributed to the event have been checked or calibrated if they were suspect.
4. Supervisor approval is recorded for critical service.

## 13. Records

In the shift log, write:

- Alarm times and IDs
- What you changed (valves, setpoints, which pump is running)
- Standby status
- Who you called
- Whether the condition cleared or was handed over

## 14. Related documents

- MM-BFP-010 Boiler Feed Pump Maintenance Manual
- TG-BFP-020 Boiler Feed Pump Alarm Troubleshooting Guide
- SI-BFP-031 Boiler Feed Pump Safety Instructions
- OP-MTR-003 Critical Motor Start and Trip Response
- AP-ER-040 EastRefinery Alarm Management Philosophy
- KA-OPS-050 Recurring BFP high-severity alarms (service notes)
