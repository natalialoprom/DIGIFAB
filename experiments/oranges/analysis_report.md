# BME680 Orange-Freshness Experiment: Analysis Report

## 1. Overview

This report analyzes a controlled sampling experiment performed with an Adafruit BME680/BME688 environmental sensor wired to an ESP32 Feather over I²C (`VIN→3V`, `GND→GND`, `SDI→SDA / GPIO 23`, `SCK→SCL / GPIO 22`). The sensor was used to compare three conditions inside a semi-enclosed setup: ambient air, freshly purchased oranges, and overripe oranges. The Arduino sketch streamed measurements over the serial monitor as CSV with columns `ms,phase,tempC,humPct,pressHpa,gasKOhms,deltaGasKOhms,gasDropPct,deltaHumPct`. After warm-up and a 20-sample baseline calibration, the experiment moved through three labelled phases. The goal was not to derive an absolute "freshness index" but to compare the local microenvironment around the sensor across conditions, using humidity and gas resistance as the main observables.

## 2. Data preparation

The raw serial dump contained both data rows and command-echo lines beginning with `#`. Only labelled data rows (`ambient`, `fresh_oranges`, `old_oranges`) were retained. Because the firmware's delta columns are zero until the baseline is established, the `ambient` rows were further split into two sub-segments for analysis:

- **`ambient_pre_baseline`** — long warm-up window during which `deltaGasKOhms = 0`. Used only to confirm that the sensor stabilized before calibration.
- **`ambient_ref`** — short ambient window between "Baseline ready" and the start of the fresh-oranges phase. This is the meaningful ambient reference for comparison with the fruit phases.

Sample counts and durations of the comparable segments:

| Segment | n | Duration (s) |
|---|---|---|
| `ambient_ref` | 22 | 49.7 |
| `fresh_oranges` | 294 | 694.1 |
| `old_oranges` | 73 | 170.6 |

Sampling cadence was approximately one row every 2.37 s.

## 3. Baseline calibration

The firmware's 20-sample baseline calibration produced the following reference values, used internally to compute `deltaGasKOhms`, `gasDropPct`, and `deltaHumPct`:

| Quantity | Baseline |
|---|---|
| Temperature | 26.04 °C |
| Relative humidity | 26.49 % |
| Gas resistance | 32.20 kΩ |

The pre-baseline warm-up showed the typical BME680 trajectory: temperature decreasing from ~27.8 °C toward room temperature as the package self-heating equilibrates, while gas resistance climbed steadily from ~19.8 kΩ to ~33 kΩ over roughly 23 minutes. This drift is expected for a metal-oxide gas sensor reaching steady state and is the reason the firmware enforces a warm-up period before calibration.

## 4. Per-phase results

### 4.1 Ambient reference (post-baseline)

In the 50-second window before fruit was introduced, the sensor reported very stable readings: temperature 26.01 ± 0.01 °C, humidity 26.57 ± 0.16 %, and gas resistance 32.46 ± 0.31 kΩ. The baseline-relative gas drop hovered around −0.8 % (i.e. resistance was actually slightly higher than the baseline mean, within noise) and Δhumidity was +0.08 percentage points. The last two samples of this segment already show the leading edge of a humidity rise (+0.27 pp, then +0.77 pp), indicating that the oranges were brought close to the sensor immediately before the official phase change.

### 4.2 Fresh oranges

Across the 11.6-minute fresh-orange phase, mean humidity rose to 30.84 ± 1.05 % (Δ = +4.34 pp vs. baseline) and mean gas resistance dropped modestly to 30.92 ± 0.88 kΩ (mean gas drop of ~4.0 %, peak ~9.6 %). Temperature drifted down to 24.27 ± 0.52 °C, consistent with the fruit acting as a small thermal mass that cooled the local air slightly and reduced the BME680 hotplate's downstream warming. The gas trace shows oscillations on the scale of 1–2 kΩ overlaid on a slow drift, but it never deviates dramatically from the ambient level. In other words, fresh oranges produce a clear and consistent humidity rise (the peel transpires water vapour) and only a small VOC-related response.

### 4.3 Overripe oranges

The overripe phase was qualitatively different. Within ~26 seconds of the phase change, gas resistance had already collapsed by more than 50 % relative to baseline; mean gas resistance over the whole segment was 15.45 ± 6.06 kΩ — less than half of the ambient reference. The mean baseline-relative gas drop was 52.0 % and the maximum was 75.0 % (gas = 8.04 kΩ at t ≈ 2328.7 s). Humidity simultaneously climbed to a mean of 34.9 ± 3.1 %, with a peak of 43.9 % (Δ = +17.4 pp). Temperature stabilized slightly higher than during the fresh phase (24.64 ± 0.24 °C), which is consistent with longer settling and possibly with slight metabolic warming from microbial activity, although the temperature difference is small enough that thermal mass and timing alone could explain it.

A noteworthy feature of the overripe trace is its strong oscillatory behaviour: the gas signal rises and falls several times between roughly 8 kΩ and 33 kΩ. Two non-exclusive explanations fit the pattern: (i) the rotting fruit emits VOCs in pulses that diffuse unevenly through the semi-enclosed space, and (ii) the BME680's gas-sensor heater duty-cycling and surface re-oxidation produce intrinsic recovery ramps when concentrations change rapidly. Either way, the magnitude of the excursions is far outside what was observed for fresh fruit.

## 5. Quantitative comparison

Mean values per metric and segment:

| Metric | Ambient ref | Fresh oranges | Overripe oranges |
|---|---|---|---|
| Temperature (°C) | 26.01 | 24.27 | 24.64 |
| Relative humidity (%) | 26.57 | 30.84 | 34.89 |
| Gas resistance (kΩ) | 32.46 | 30.92 | 15.45 |
| Δ gas (kΩ vs. baseline) | +0.26 | −1.28 | **−16.75** |
| Gas drop (% vs. baseline) | −0.82 | 3.98 | **52.01** |
| Δ humidity (pp vs. baseline) | +0.08 | 4.34 | **8.40** |

The two fruit conditions both raise local humidity and lower gas resistance relative to ambient, but the magnitudes are roughly an order of magnitude apart. In particular the gas-resistance signal is an effective discriminator: a drop on the order of a few percent indicates fresh fruit, while drops above ~30 % cleanly identify the overripe condition. Humidity by itself is a weaker discriminator because the absolute scale of the rise overlaps between the two fruit conditions during transient parts of each phase.

## 6. Figures

The following plots accompany this report (referenced filenames are saved alongside this Markdown):

- `plot_gas.png` — gas resistance vs. time, with the baseline level shown as a dashed line and phase windows shaded.
- `plot_hum.png` — relative humidity vs. time on the same time axis.
- `plot_temp.png` — temperature vs. time.
- `plot_deltas.png` — firmware-derived `gasDropPct` (top) and `deltaHumPct` (bottom), the two baseline-relative metrics most useful for distinguishing conditions.
- `plot_boxes.png` — boxplots of gas resistance, humidity, and gas drop % across the three segments.

## 7. Limitations and caveats

Several caveats apply to interpreting these numbers:

The three phases differ in duration (≈50 s, ≈694 s, ≈171 s) and in number of samples, so per-segment means are not comparable as if they were balanced trials; statistics over the overripe phase in particular include the rapid initial transient and may not represent a steady state. Because only one sample of each fruit type was tested, the experiment cannot distinguish "overripe vs. fresh" from "this particular overripe batch vs. this particular fresh batch". The semi-enclosed setup is not gas-tight and was not actively ventilated, so VOCs and water vapour accumulate over time and confound a direct comparison between phases. The BME680 metal-oxide gas element responds to total reducing-gas load rather than to a specific molecule, so the gas-resistance drop in the overripe phase cannot be attributed to ethanol, ethylene, or any single VOC without auxiliary instrumentation. Temperature decreased during the fruit phases, which itself shifts the gas sensor's baseline; some of the apparent gas drop is thus attributable to temperature change rather than purely to VOC emission. Finally, the firmware-reported baseline (Temp 26.04 °C, Hum 26.49 %, Gas 32.20 kΩ) was averaged over a 20-sample window during which gas resistance was still drifting upward, so the baseline gas value is slightly under-estimated relative to the true post-warm-up level — this would slightly understate the true gas-drop percentages.

## 8. Conclusion

The experiment shows a clear, monotonic ordering of the three conditions in the two main observables: humidity (ambient < fresh < overripe) and gas resistance (ambient > fresh > overripe). The contrast between fresh and overripe is large — roughly a factor of ten in baseline-relative gas drop and a factor of two in baseline-relative humidity rise — and emerges within ~30 seconds of placing the overripe fruit near the sensor. This supports the project's underlying premise that a low-cost BME680 deployment, used comparatively against a per-session baseline, can distinguish fresh from spoiling citrus at the level of the local microenvironment. For a defensible quantitative claim in your paper, the next step would be repeating the run with several specimens per condition and with longer, time-matched phases under more tightly controlled enclosure conditions.

## 9. Files generated alongside this report

- `raw_data.csv` — the cleaned CSV with only labelled rows (header + 530 data rows).
- `summary_stats.csv` — per-segment summary statistics (n, duration, mean, std, min, max for each metric).
- `analyze.py` — the Python script that produced the statistics and plots, included for reproducibility.
- `plot_gas.png`, `plot_hum.png`, `plot_temp.png`, `plot_deltas.png`, `plot_boxes.png` — figures.
