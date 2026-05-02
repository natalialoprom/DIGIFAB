# Calibration Notes

## Scope

These calibration notes apply to the **retail / supermarket prototype** based on:
- **ESP32 Feather**
- **Adafruit BME680/BME688**
- **Raspberry Pi + e-ink display**
- **Flask dashboard**

At the current stage, the prototype logic is **calibrated specifically for oranges**, and especially informed by the controlled comparison between:
- ambient air,
- fresh oranges,
- overripe oranges.

This calibration should therefore be understood as:
- **product-specific**
- **prototype-specific**
- **baseline-relative**
- and **preliminary**

It should **not** be interpreted as a universal freshness calibration for all fruits.

---

## Why baseline-relative calibration is used

The BME680/BME688 is a metal-oxide environmental sensor that does not directly output a freshness score. Instead, it provides:
- temperature,
- relative humidity,
- pressure,
- gas resistance.

In practice, the most useful variables for this project are:
- **relative humidity**
- **gas resistance**

However, absolute gas-resistance values are strongly affected by:
- warm-up time,
- environmental conditions,
- airflow,
- local humidity,
- sensor drift,
- and session-to-session variation.

Because of this, the final firmware does not rely on fixed absolute gas-resistance values alone. Instead, it uses:
- a **warm-up phase**
- a **session baseline**
- and **relative changes** compared to that baseline.

---

## Experimental basis

A controlled experiment was performed with oranges in three conditions:
- **ambient air**
- **fresh oranges**
- **overripe oranges**

The sensor was connected to the ESP32 Feather over I2C and logged values over time as CSV. After warm-up and calibration in ambient air, the experiment compared how humidity and gas resistance changed when fresh and overripe oranges were placed near the sensor in a semi-enclosed setup.

### Baseline used in the most stable run
The most useful baseline obtained during the orange comparison experiment was approximately:

- **Temperature:** 26.04 °C
- **Relative humidity:** 26.49 %
- **Gas resistance:** 32.20 kΩ

### Main observed trends
The experiment showed the following pattern:

#### Ambient reference
- humidity around **26–27 %**
- gas resistance around **32 kΩ**

#### Fresh oranges
- moderate humidity increase
- small-to-moderate gas resistance drop

Typical observed behavior:
- humidity around **30–32 %**
- gas drop typically around **2–9 %**

#### Overripe oranges
- strong humidity increase
- very large gas resistance drop

Typical observed behavior:
- humidity around **34–39 %**
- gas drop commonly above **50 %**
- strong transient peaks also observed

These results support the idea that:
- **fresh oranges** change the local microenvironment moderately,
- while **overripe oranges** produce a much stronger environmental shift.

---

## Current classification strategy

The current retail firmware uses two derived metrics:

- **deltaHumPct**  
  Difference between current humidity and baseline humidity

- **gasDropPct**  
  Percentage drop in gas resistance relative to baseline

These are used after:
- a warm-up period,
- baseline calibration,
- short-term smoothing,
- and temporal confirmation of the predicted state.

---

## Current orange-calibrated thresholds

The following thresholds are currently used as practical prototype logic:

### Fresh
- `gasDropPct < 10`
- and `deltaHumPct < 6`

### Use soon
- `10 <= gasDropPct < 30`
- or `6 <= deltaHumPct < 10`

### Discount
- `gasDropPct >= 30`
- or `deltaHumPct >= 10`

These thresholds were chosen conservatively so that:
- fresh oranges remain close to the `Fresh` / `Use soon` boundary,
- strongly degraded oranges are clearly pushed into `Discount`.

---

## Why smoothing and confirmation are used

Short-term fluctuations are expected in the BME680/BME688 output, especially in:
- gas resistance,
- partially enclosed spaces,
- and transient fruit exposure.

For that reason, the firmware includes:
- a **short moving average**
- and a **confirmation requirement** before changing the displayed state

This is important in the supermarket version because:
- the e-ink display should not flicker between states,
- the price tag should feel stable,
- and users should not see rapid oscillations caused by noise or brief disturbances.

---

## Practical interpretation in the retail prototype

The resulting logic should be interpreted as:

- **Fresh**  
  Conditions close to ambient baseline, with only minor local changes around the fruit.

- **Use soon**  
  Noticeable environmental change suggesting progression in ripening, but not a severe spoilage-like state.

- **Discount**  
  Strong humidity increase and/or strong gas-resistance drop, consistent with a much more advanced state of degradation.

This is intended as a **relative freshness-aware decision support system**, not as a chemically specific spoilage detector.

---

## Important limitations

### Product specificity
The thresholds in the current firmware are informed by **oranges**, not by all fruits.

### Severity of the overripe sample
The overripe oranges used in the experiment were **very far past their optimal state**, which makes the `Discount` class correspond to a rather strong condition.

### Enclosure dependence
The magnitude of the response depends on:
- enclosure size,
- airflow,
- fruit distance to sensor,
- number of fruits,
- and exposure time.

### Environmental dependence
Different rooms, ventilation conditions, and temperatures may shift the effective thresholds.

---

## How to recalibrate for another session

Recommended procedure:

1. Power the system on.
2. Let the sensor warm up in ambient air.
3. Keep the fruit away during warm-up.
4. Run the baseline calibration routine.
5. Confirm that humidity and gas resistance are reasonably stable.
6. Start monitoring fruit relative to that session baseline.

---

## How to recalibrate for another product

To recalibrate for a different fruit or produce category:

1. Repeat the experiment with:
   - ambient air,
   - fresh sample,
   - overripe sample
2. Collect CSV logs.
3. Compare:
   - mean humidity rise,
   - mean gas-resistance drop,
   - transient behavior
4. Adjust the thresholds for:
   - `Fresh`
   - `Use soon`
   - `Discount`
5. Validate by repeating the measurement over several specimens and sessions.

---

## Future calibration improvements

Possible future improvements include:
- repeating the orange experiment with multiple specimens,
- balancing phase durations,
- using more controlled enclosures,
- product-specific profiles,
- adaptive baselines,
- and per-product calibration tables stored in firmware or selected through the dashboard.

---

## Summary

The current retail prototype is calibrated as an **orange-aware baseline-relative system**. Its logic is based on the observation that:
- fresh oranges cause moderate local environmental changes,
- overripe oranges cause a much stronger humidity increase and gas-resistance drop.

The result is a simple, practical classification scheme suitable for the prototype:
- `Fresh`
- `Use soon`
- `Discount`

This calibration is sufficient for demonstration and prototype validation, but should be treated as exploratory and product-specific.