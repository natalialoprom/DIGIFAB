# Experiments

## Overview

A set of exploratory experiments was carried out to evaluate whether the BME680/BME688 sensor could distinguish between different fruit conditions using baseline-relative measurements. The goal was not to produce a universal freshness metric, but to determine whether a low-cost sensor could detect meaningful changes in the local microenvironment around fruit.

The main experiment focused on **oranges**, comparing:
- ambient air,
- freshly purchased oranges,
- overripe oranges.

---

## Experiment Goal

To test whether the combination of:
- **relative humidity increase**
- **gas resistance drop**

could be used as a practical indicator of fruit freshness state in the prototypes.

This question was especially relevant for:
- the classification logic in the retail prototype,
- and the color mapping in the educational prototype.

---

## Hardware Used

- **ESP32 Feather**
- **Adafruit BME680/BME688**
- Arduino-based firmware streaming data over serial

Sensor wiring:
- `VIN -> 3V`
- `GND -> GND`
- `SDI -> SDA / GPIO 23`
- `SCK -> SCL / GPIO 22`

---

## Methodology

The experiment was designed as a baseline-relative comparison.

### Procedure
1. The sensor was allowed to warm up in ambient room air.
2. A baseline was recorded in ambient conditions.
3. A short post-baseline ambient reference segment was collected.
4. Fresh oranges were placed near the sensor in a semi-enclosed setup.
5. Overripe oranges were then measured in the same general setup.
6. The firmware logged sensor data in CSV format.

### Recorded variables
The Arduino sketch output:
- elapsed time
- phase label
- temperature
- humidity
- pressure
- gas resistance
- gas-resistance variation relative to baseline
- gas-drop percentage relative to baseline
- humidity variation relative to baseline

### Important methodological note
A key lesson from early trials was that **baseline quality matters heavily**. A baseline taken while the sensor is still drifting can distort the interpretation of the gas data. For this reason, later trials used a more stable post-warm-up baseline and were treated as more reliable.

---

## Main Analysis Files

The orange experiment currently includes:
- `raw_data.csv`
- `summary_stats.csv`
- `analysis_report.md`
- `analyze.py`
- generated plots:
  - `plot_boxes.png`
  - `plot_deltas.png`
  - `plot_gas.png`
  - `plot_hum.png`
  - `plot_temp.png`

These files are intended to support both:
- firmware calibration,
- and paper writing.

---

## Main Observations

The experiment showed a clear ordering across the three conditions:

- **ambient air**
- **fresh oranges**
- **overripe oranges**

The most useful variables were:
- relative humidity,
- gas resistance relative to baseline.

### Ambient
Ambient air remained comparatively stable once the baseline had been established.

### Fresh oranges
Fresh oranges produced:
- a moderate humidity increase,
- a small-to-moderate gas resistance drop.

This suggests a detectable but limited alteration of the local microenvironment.

### Overripe oranges
Overripe oranges produced:
- a much stronger humidity increase,
- a much larger gas resistance drop.

This phase showed the clearest separation from ambient and from the fresh-orange condition.

---

## Interpretation

The experiments support the idea that the BME680/BME688 can be used as a **relative freshness proxy** when:
- properly warmed up,
- baselined per session,
- and interpreted comparatively rather than absolutely.

The project therefore does **not** claim that:
- a single gas resistance value directly corresponds to freshness.

Instead, it uses:
- **session baseline**
- **relative changes**
- **simple threshold logic**

to determine practical states such as:
- Fresh / Use soon / Discount
- Fresh / Ripe / Very ripe

---

## Current Threshold Logic

Based on the orange experiment, the project currently uses orange-calibrated logic where:

- small gas-drop and humidity-rise values correspond to **fresh**
- medium changes correspond to **use soon / ripe**
- large changes correspond to **discount / very ripe**

These thresholds should be treated as:
- **product-specific**
- **prototype-specific**
- and **preliminary**

rather than as general values for all fruits.

---

## Limitations of the Experiment

The orange experiment was useful, but several limitations apply:

- only a limited number of samples were tested,
- the overripe oranges were very strongly degraded,
- the enclosure was semi-enclosed rather than tightly controlled,
- phase durations were not perfectly balanced,
- the BME680 is a general MOX gas sensor and not a gas-specific analyzer.

For those reasons, the results are most useful for:
- guiding firmware logic,
- demonstrating feasibility,
- and motivating future repeat experiments.

---

## Recommended Future Experiments

To improve robustness, future experiments should include:
- repeated trials with multiple oranges per condition,
- time-matched segments,
- tighter enclosure control,
- comparison with additional fruit types,
- repeatability tests across different days,
- and longer observation windows.
