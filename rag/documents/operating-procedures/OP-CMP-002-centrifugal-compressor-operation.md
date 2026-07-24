# OP-CMP-002 — Centrifugal Compressor Operating Procedure

**Document ID:** OP-CMP-002  
**Revision:** 2.1  
**Effective Date:** 15 September 2025  
**Site:** EastRefinery  
**Assets:** Compressor C-201, Compressor C-202  
**Units:** Unit 2, Unit 5  
**Owner:** Process Operations  
**Audience:** Board operators, field operators, process engineers, reliability  

---

## 1. Purpose

This procedure covers normal running and alarm handling for centrifugal compressors C-201 and C-202. The focus on this site is discharge pressure trouble, anti-surge behaviour, and keeping people away from bad decisions when the machine is unstable.

## 2. Scope

Includes the compressor, driver interface signals used by operations, suction scrubber / knockout drum, discharge cooler, anti-surge / recycle valve, and the main pressure and temperature instruments used by the board.

Does not replace the vendor start-up manual for major overhaul recommissioning. For that work, use the vendor pack plus the turnaround procedure.

## 3. What “normal” looks like

Exact setpoints change with the process mode. Use the current approved operating window on the board. As a practical guide:

| Parameter | What good looks like | Alarm behaviour | Protective expectation |
|---|---|---|---|
| Discharge pressure | Near the process target | High around +8% above setpoint | Open recycle / cut load |
| Suction pressure | Stable in approved band | Low around -10% | Cut rate, check upstream |
| Discharge temperature | Usually under 140 C | High near 155 C | Trip near 170 C High-High |
| Vibration | under about 5.0 mm/s | High near 7.5 mm/s | Trip at High-High |
| Surge margin | Comfortably above 10% | Low near 5% | Anti-surge valve opens |

If surge margin is thin, do not “push discharge” to clear a pressure complaint from downstream.

## 4. Before you raise rate

1. Confirm suction drum level is under control and not carrying liquid.
2. Confirm discharge cooler fans / water side look healthy.
3. Confirm anti-surge is in automatic and not forced closed.
4. Confirm no active High vibration or High discharge temperature already hanging around.
5. Tell the field if you are about to make a large rate change.

## 5. High discharge pressure response

This is the alarm that comes back again and again on these machines.

### Immediate board actions

1. Acknowledge and check whether suction pressure, recycle position, and discharge temperature moved at the same time.
2. Confirm the reading. If the local / spare transmitter disagrees a lot, treat it as suspect instrumentation while you keep the machine safe.
3. Open recycle toward a safer margin if automatic has not already done it.
4. Reduce compressor setpoint if the process still allows production at a lower rate.
5. If discharge temperature is also climbing, stop thinking about production targets and protect the machine.

### Things that commonly cause it here

1. Fouled discharge cooler putting backpressure on the machine
2. Sticky anti-surge valve that opens late and then overshoots
3. Downstream unit cutting rate while the compressor stays wound up
4. Condensate in impulse lines making a false high reading
5. Setpoint changes made without checking the surge map

### What not to do

1. Do not inhibit anti-surge to quiet the alarm list.
2. Do not force the recycle valve shut because someone wants more discharge pressure.
3. Do not send the field into the cooler bay while the machine is surging or swinging hard.

## 6. Low suction pressure

1. Check upstream feed and suction drum.
2. Cut throughput before the machine walks into surge.
3. Look for blocked strainers, cold condensate problems, or an upstream unit upset.
4. If low suction and high recycle activity show up together, say so in the log. That pairing matters for maintenance.

## 7. Surge or near-surge

Operators on this plant have learned the hard way that “near surge all shift” is not a stable way to run.

1. Open anti-surge.
2. Reduce rate.
3. Stabilize suction.
4. Call process engineering if you cannot find a stable point.
5. After the event, ask rotating to review vibration and seal condition if the machine spent a long time near the surge line.

## 8. Recurring discharge pressure alarms

When the same discharge pressure alarm keeps returning over days:

1. Trend discharge pressure, suction pressure, recycle valve, and discharge temperature for 30 to 90 days.
2. Check cooler approach temperature and fan status history.
3. Ask I&C to look at transmitter health and impulse lines.
4. Stroke-test the anti-surge valve on a planned window.
5. Read TG-CMP-021 and MM-CMP-011 before you accept any auto-generated recommendation that says “keep monitoring” while temperature is also high.

## 9. Related equipment

- Anti-surge valve and positioner
- Discharge cooler and fans
- Suction scrubber / knockout drum
- Discharge check valve
- Vibration and thrust probes
- Suction and discharge transmitters

## 10. Handover notes that help the next shift

Write plain facts:

- Which compressor is loaded
- Whether recycle is open more than usual
- Any cooler abnormality
- Whether the pressure alarm is real process or suspected instrument
- Who was called and what is still open

## 11. Related documents

- MM-CMP-011 Centrifugal Compressor Maintenance Manual
- TG-CMP-021 Compressor Discharge Pressure Alarm Troubleshooting Guide
- SI-CMP-032 Compressor System Safety Instructions
- AP-ER-040 EastRefinery Alarm Management Philosophy
