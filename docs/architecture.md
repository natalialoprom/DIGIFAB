# Architecture

## System-Level Architecture

The project is organized around **two related but distinct prototypes** built on top of the same sensing principle: environmental changes near fruit can be captured through a low-cost gas and humidity sensor and then mapped to an output that is understandable to users.

Both prototypes use a **BME680/BME688** as the main sensing element, but differ in how they process and communicate the result.

## 1. Retail / Supermarket Architecture

### High-level structure

```text
ESP32 Feather + BME680  --->  Wi-Fi  --->  Raspberry Pi + Flask
                                           |-> E-ink shelf tag
                                           |-> Web dashboard
```

### Components

#### ESP32 Feather sensing node
The ESP32 Feather is responsible for:
- reading the BME680/BME688 sensor,
- computing freshness-related indicators relative to a baseline,
- assigning a state such as `Fresh`, `Use soon`, or `Discount`,
- sending the readings and state to the Raspberry Pi over Wi-Fi.

#### BME680/BME688 sensor
The sensor provides:
- temperature,
- relative humidity,
- pressure,
- gas resistance.

In this project, the most relevant variables are:
- **humidity**
- **gas resistance**

The system does not attempt to identify a specific gas. Instead, it relies on **relative changes** in the local environment.

#### Raspberry Pi server node
The Raspberry Pi runs a Flask application that:
- exposes an `/update` endpoint for incoming ESP32 readings,
- updates the e-ink display content,
- stores or displays the latest product state,
- serves a local dashboard with pages such as:
  - `/store`
  - `/dashboard`
  - `/offers`
  - `/history`

#### E-ink shelf display
The e-ink display acts as a smart shelf tag and shows:
- product name,
- freshness state,
- price,
- optionally some compact sensor information.

This matches the intended supermarket use case more closely than a standard LCD because it resembles real electronic price labels.

### Data flow

1. The ESP32 reads the sensor.
2. It compares current values to a session baseline.
3. It computes a simple classification.
4. It sends an HTTP GET request to the Raspberry Pi.
5. The Raspberry Pi updates:
   - the e-ink screen,
   - the internal product state,
   - the dashboard pages.

## 2. Educational Prototype Architecture

### High-level structure

```text
ESP32-C3 + BME680 ---> local processing ---> NeoPixel ring / translucent box
```

### Components

#### ESP32-C3 controller
The ESP32-C3 reads the sensor locally and performs all decision logic on-board. No networking or server is required.

#### BME680/BME688 sensor
The same sensing principle is used as in the retail prototype:
- baseline acquisition,
- comparison against current readings,
- emphasis on relative humidity increase and gas resistance drop.

#### NeoPixel ring
The NeoPixel ring provides a highly visible and intuitive output:
- green,
- yellow,
- red.

It is intended to illuminate a translucent enclosure so that the whole box appears to change color.

### Data flow

1. The ESP32-C3 warms up the sensor.
2. A baseline is measured in ambient conditions.
3. The current environment is sampled repeatedly.
4. Baseline-relative changes are smoothed.
5. The system assigns one of three states:
   - `Fresh`
   - `Ripe`
   - `Very ripe`
6. The NeoPixel ring updates the enclosure color.

## Shared Design Logic

Although the output mechanisms are different, both prototypes share the same design logic:

- use a **session baseline**
- work with **relative changes**
- combine **humidity** and **gas resistance**
- avoid claiming a universal absolute freshness index

This was an intentional choice based on the experimental results and on the known behavior of MOX gas sensors such as the BME680.

## Why Baseline-Relative Logic Was Chosen

The experiments showed that:
- absolute gas resistance values can drift significantly with warm-up and environment,
- humidity changes are often easier to interpret than gas values alone,
- relative comparison against a baseline is more robust than fixed absolute thresholds.

For that reason, both firmwares are built around:
- baseline calibration,
- baseline-relative metrics,
- simple threshold-based classification.

## Architectural Trade-offs

### Retail prototype
**Advantages**
- richer user-facing interface
- realistic supermarket framing
- networked and extensible
- supports dashboards and multiple views

**Limitations**
- more complex to deploy
- depends on Wi-Fi and Raspberry Pi stability
- more points of failure

### Educational prototype
**Advantages**
- simple and robust
- self-contained
- easy to demonstrate
- suitable for classrooms and public engagement

**Limitations**
- no history or dashboard by default
- less detailed feedback
- less realistic as a retail deployment

## Future Architectural Extensions

Possible future improvements include:
- CSV logging in the retail prototype,
- manual override in the dashboard,
- support for multiple live products,
- recalibration button for the educational prototype,
- product-specific profiles beyond oranges,
- better enclosure control for more repeatable experiments.
