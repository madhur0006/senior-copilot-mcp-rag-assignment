# TG-MTR-022 — Motor Trip Alarm Troubleshooting Guide

**Document ID:** TG-MTR-022  
**Revision:** 1.6  
**Effective Date:** 1 March 2026  
**Site:** EastRefinery  
**Assets:** Motor M-501, Motor M-502, Boiler Feed Pump motors  
**Owner:** Electrical Reliability / Area Operations  

---

## 1. Objective

Help the shift work a motor trip without guessing, and without restarting into a damaged machine. Also make clear which related assets belong in the same investigation.

## 2. First 15 minutes

1. No restart.
2. Capture the trip reason before reset.
3. Understand process impact.
4. Start standby if available and approved.
5. Call electrical and the supervisor for critical service.
6. Ask the field whether there was noise, smoke, or a smell.

If several motors on one bus tripped together, think upstream power first.

## 3. Related assets to inspect

For any critical motor trip, look beyond the motor nameplate:

1. Driven pump, compressor, or fan
2. Coupling and guard
3. Motor bearings and driven-equipment bearings
4. Local suction and discharge valves that change start load
5. MCC feeder, contactor, and protection relay
6. Power quality or feeder events on the same board

For a boiler feed pump motor trip, add:

- Suction strainer DP
- Minimum-flow valve position at trip time
- Seal flush status
- Discharge valve position during the start attempt
- Any BFP pressure or vibration alarms just before the trip

## 4. Clues from combinations

- Trip + rising amps + low suction: process/cavitation load issue is likely in play
- Trip + bearing temperature already high: mechanical problem may have come first
- Trip + clean process trends + bus dip: look at electrical supply
- Trip during start only: lineup and start method deserve as much attention as the motor windings

## 5. Restart gate

Use OP-MTR-003. If the paperwork and checks are not done, the answer is not “just bump it.”

## 6. What to hand to maintenance

Give them:

- Exact trip text and time
- Whether standby was started
- Process conditions
- Any recent work on the motor or driven machine
- Whether this has happened before recently

## 7. Related documents

- OP-MTR-003
- MM-MTR-012
- SI-GEN-030
- OP-BFP-001 / MM-BFP-010 when relevant
