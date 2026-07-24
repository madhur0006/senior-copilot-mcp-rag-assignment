# TG-CMP-021 — Compressor Discharge Pressure Alarm Troubleshooting Guide

**Document ID:** TG-CMP-021  
**Revision:** 2.3  
**Effective Date:** 20 January 2026  
**Site:** EastRefinery  
**Assets:** Compressor C-201, Compressor C-202  
**Owner:** Process Reliability  

---

## 1. Problem in plain language

Repeated compressor discharge pressure alarms are common on Unit 2 and Unit 5. Sometimes the machine is genuinely pushing against a restriction. Sometimes the cooler is dirty. Sometimes the anti-surge valve is late. Sometimes the transmitter is lying. The job is to tell those apart without making the machine surge or sending people into a bad area.

## 2. Quick picture in the first 10 minutes

Pull these on one screen if you can:

1. Discharge pressure
2. Suction pressure
3. Anti-surge / recycle valve position
4. Discharge temperature
5. Process downstream flow or valve position

Then ask:

- Did recycle open?
- Did temperature rise with pressure?
- Did suction fall first?
- Did the alarm start right after a setpoint change?

## 3. Why the alarm keeps coming back

Common contributors on this site:

1. Fouled discharge cooler raising backpressure
2. Sticky anti-surge valve causing overshoot
3. Downstream rate cut while the compressor stays high
4. Impulse-line condensate and false highs
5. Operating too close to the surge limit for long periods
6. Old transmitter calibration after a range or service change

## 4. Immediate actions

1. Confirm the alarm is still active and how far above the limit you are.
2. Let anti-surge do its job. Open recycle further if needed and authorised.
3. Cut load if temperature is rising or surge margin is thin.
4. Check whether the reading looks false before you tear the process apart.
5. Keep the field out of the cooler bay while the machine is swinging.

## 5. Short-term follow-up

1. Ask I&C to compare transmitters and check impulse lines.
2. Stroke-test the anti-surge valve on a planned window.
3. Inspect cooler fans and approach temperature.
4. Review recent setpoint and mode changes with process engineering.
5. If alarms are frequent but consequence is low and instruments are healthy, only then discuss rationalisation under AP-ER-040.

## 6. Consistency check against the maintenance manual

If a recommendation says ignore rising discharge temperature while pressure is high, that recommendation is out of line with MM-CMP-011 and SI-CMP-032. Prefer cooling recovery and load reduction. Write the conflict down.

## 7. Example shift note

“C-201 high discharge pressure three times after 11:00. Recycle opened late on first event. Discharge temperature up 8 C. Local gauge agreed with DCS. Cooler fan B looks slow. Held rate down 5%. Called maintenance for cooler and anti-surge checks. No inhibit used.”

That note is more useful than “compressor alarming, monitored.”

## 8. Related documents

- OP-CMP-002
- MM-CMP-011
- SI-CMP-032
- AP-ER-040
