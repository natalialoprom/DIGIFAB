"""
BME680 orange-freshness experiment analysis.
Loads raw_data.csv, segments by phase, computes summary statistics,
and generates plots used in the markdown report.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("/sessions/funny-epic-knuth/mnt/outputs")
df = pd.read_csv(OUT / "raw_data.csv")

# Convert time to seconds for readability and zero it on the first sample.
df["t_s"] = (df["ms"] - df["ms"].iloc[0]) / 1000.0

# The phase column lumps all ambient rows together, but the deltas only
# become meaningful after the baseline calibration step finishes. Split
# ambient into "pre-baseline" (delta == 0 throughout) and "post-baseline"
# (the short reference window that immediately precedes the fresh-oranges
# phase). Use the same row labels the firmware emitted.
df["segment"] = df["phase"]
post_mask = (df["phase"] == "ambient") & (df["deltaGasKOhms"] != 0.0)
df.loc[post_mask, "segment"] = "ambient_ref"
pre_mask = (df["phase"] == "ambient") & (df["deltaGasKOhms"] == 0.0)
df.loc[pre_mask, "segment"] = "ambient_pre_baseline"

# Phase change instants (s, relative to t_s = 0).
phase_changes = {}
for seg in ["ambient_ref", "fresh_oranges", "old_oranges"]:
    sub = df[df["segment"] == seg]
    if not sub.empty:
        phase_changes[seg] = (sub["t_s"].iloc[0], sub["t_s"].iloc[-1])

print("Segment time spans (s):")
for k, v in phase_changes.items():
    print(f"  {k}: {v[0]:.1f}s to {v[1]:.1f}s  (n={len(df[df['segment'] == k])})")

# Baseline values stated by the firmware.
BASELINE_TEMP = 26.04
BASELINE_HUM = 26.49
BASELINE_GAS = 32.20

# ------------- summary stats per segment -------------
def stats(sub, col):
    return {
        "mean": sub[col].mean(),
        "std": sub[col].std(),
        "min": sub[col].min(),
        "max": sub[col].max(),
    }

segments_for_stats = ["ambient_ref", "fresh_oranges", "old_oranges"]
metrics = ["tempC", "humPct", "gasKOhms", "deltaGasKOhms", "gasDropPct", "deltaHumPct"]
rows = []
for seg in segments_for_stats:
    sub = df[df["segment"] == seg]
    n = len(sub)
    duration = sub["t_s"].iloc[-1] - sub["t_s"].iloc[0] if n else float("nan")
    for m in metrics:
        s = stats(sub, m)
        rows.append({"segment": seg, "n": n, "duration_s": duration, "metric": m, **s})

stats_df = pd.DataFrame(rows)
stats_df.to_csv(OUT / "summary_stats.csv", index=False)
print("\nSummary stats:")
print(stats_df.to_string(index=False))

# ------------- pivot for the report's main comparison table -------------
pivot = stats_df.pivot_table(index="metric", columns="segment", values="mean")
pivot = pivot[segments_for_stats]
print("\nMean values per segment:\n", pivot)

# ------------- plots -------------
plt.rcParams.update({
    "figure.figsize": (10, 5),
    "axes.grid": True,
    "grid.alpha": 0.25,
    "figure.dpi": 110,
})

color_map = {
    "ambient_pre_baseline": "#999999",
    "ambient_ref": "#1f77b4",
    "fresh_oranges": "#2ca02c",
    "old_oranges": "#d62728",
}

# Restrict the plotted window to post-baseline segments only (so the long
# warm-up doesn't dominate the x-axis). This is the part of the experiment
# where deltas are meaningful.
plot_df = df[df["segment"].isin(segments_for_stats)].copy()
plot_df["t_rel_s"] = plot_df["t_s"] - plot_df["t_s"].iloc[0]

def shade_phases(ax):
    for seg, color in color_map.items():
        if seg not in segments_for_stats:
            continue
        sub = plot_df[plot_df["segment"] == seg]
        if sub.empty:
            continue
        ax.axvspan(sub["t_rel_s"].iloc[0], sub["t_rel_s"].iloc[-1],
                   alpha=0.10, color=color, label=seg)

# 1. Gas resistance over time
fig, ax = plt.subplots()
ax.plot(plot_df["t_rel_s"], plot_df["gasKOhms"], color="black", lw=1.2)
ax.axhline(BASELINE_GAS, ls="--", color="#666", lw=1, label=f"baseline ({BASELINE_GAS} kΩ)")
shade_phases(ax)
ax.set_xlabel("Time since end of baseline (s)")
ax.set_ylabel("Gas resistance (kΩ)")
ax.set_title("Gas resistance vs. time")
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "plot_gas.png")
plt.close(fig)

# 2. Humidity over time
fig, ax = plt.subplots()
ax.plot(plot_df["t_rel_s"], plot_df["humPct"], color="black", lw=1.2)
ax.axhline(BASELINE_HUM, ls="--", color="#666", lw=1, label=f"baseline ({BASELINE_HUM}%)")
shade_phases(ax)
ax.set_xlabel("Time since end of baseline (s)")
ax.set_ylabel("Relative humidity (%)")
ax.set_title("Relative humidity vs. time")
ax.legend(loc="upper left", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "plot_hum.png")
plt.close(fig)

# 3. Temperature over time
fig, ax = plt.subplots()
ax.plot(plot_df["t_rel_s"], plot_df["tempC"], color="black", lw=1.2)
ax.axhline(BASELINE_TEMP, ls="--", color="#666", lw=1, label=f"baseline ({BASELINE_TEMP} °C)")
shade_phases(ax)
ax.set_xlabel("Time since end of baseline (s)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature vs. time")
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "plot_temp.png")
plt.close(fig)

# 4. Gas drop % vs delta humidity (the firmware-derived baseline-relative metrics)
fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
ax = axes[0]
ax.plot(plot_df["t_rel_s"], plot_df["gasDropPct"], color="black", lw=1.2)
ax.axhline(0, ls="--", color="#666", lw=1)
shade_phases(ax)
ax.set_ylabel("Gas drop vs. baseline (%)")
ax.set_title("Baseline-relative changes")

ax = axes[1]
ax.plot(plot_df["t_rel_s"], plot_df["deltaHumPct"], color="black", lw=1.2)
ax.axhline(0, ls="--", color="#666", lw=1)
shade_phases(ax)
ax.set_ylabel("Δ humidity vs. baseline (% pts)")
ax.set_xlabel("Time since end of baseline (s)")
fig.tight_layout()
fig.savefig(OUT / "plot_deltas.png")
plt.close(fig)

# 5. Boxplot comparison across segments
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
labels = ["ambient_ref", "fresh_oranges", "old_oranges"]
nice_labels = ["ambient", "fresh", "overripe"]
for ax, col, title, ylabel in zip(
    axes,
    ["gasKOhms", "humPct", "gasDropPct"],
    ["Gas resistance", "Humidity", "Gas drop %"],
    ["kΩ", "%", "% (vs. baseline)"],
):
    data = [df[df["segment"] == s][col].values for s in labels]
    bp = ax.boxplot(data, labels=nice_labels, patch_artist=True, widths=0.55)
    colors = [color_map[s] for s in labels]
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.45)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "plot_boxes.png")
plt.close(fig)

print("\nPlots saved.")

# ------------- transition spike analysis (max drop reached in old phase) -------------
old = df[df["segment"] == "old_oranges"].copy()
spike_idx = old["gasDropPct"].idxmax()
print(f"\nMax gas drop during old-orange phase: {old.loc[spike_idx,'gasDropPct']:.2f}% "
      f"(gas={old.loc[spike_idx,'gasKOhms']:.2f} kΩ, hum={old.loc[spike_idx,'humPct']:.2f}%) "
      f"at t={old.loc[spike_idx,'t_s']:.1f}s")

# Time from old-phase start until first time gasDropPct exceeds 50%
old_t0 = old["t_s"].iloc[0]
crossed = old[old["gasDropPct"] >= 50.0]
if not crossed.empty:
    rise_time = crossed["t_s"].iloc[0] - old_t0
    print(f"Time from old-phase start to first ≥50% gas drop: {rise_time:.1f}s "
          f"(sample n={crossed.index[0] - old.index[0] + 1})")
