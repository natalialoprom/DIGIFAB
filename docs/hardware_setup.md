# Hardware Setup

## Overview

This project includes two hardware configurations:
1. a **retail prototype** built around an ESP32 Feather and a Raspberry Pi,
2. an **educational prototype** built around an ESP32-C3 and a NeoPixel-based light box.

Both rely on the same sensing element: the **Adafruit BME680/BME688** environmental sensor.

---

## 1. Retail Prototype Hardware

### Main components
- **ESP32 Feather**
- **Adafruit BME680/BME688**
- **Raspberry Pi**
- **Adafruit ThinkInk 2.13" e-ink display**
- jumper wires / USB cables
- optional battery or portable power source

### Sensor wiring to ESP32 Feather
The sensor was connected over I2C as follows:

- `VIN` -> `3V`
- `GND` -> `GND`
- `SDI` -> `SDA` / `GPIO 23`
- `SCK` -> `SCL` / `GPIO 22`

This configuration was used during the orange comparison experiment and in the supermarket firmware.

### Raspberry Pi role
The Raspberry Pi is used as:
- local web server,
- e-ink controller,
- dashboard host,
- price-tag update node.

### E-ink display
The e-ink screen is connected directly to the Raspberry Pi and is updated from the Flask server application.

The display is intended to emulate a supermarket electronic shelf label.

---

## 2. Educational Prototype Hardware

### Main components
- **ESP32-C3 DevKitM-1**
- **Adafruit BME680/BME688**
- **Adafruit NeoPixel Ring 16x RGBW**
- translucent enclosure
- USB power

### Sensor wiring to ESP32-C3
For the educational prototype, the BME680/BME688 is connected via I2C using software-defined pins:

- `VIN` -> `3V3`
- `GND` -> `GND`
- `SDI` -> `GPIO 5` (used as SDA)
- `SCK` -> `GPIO 6` (used as SCL)

### NeoPixel ring wiring
The NeoPixel ring is connected as follows:

- `Power 5V` -> `5V`
- `Ground` -> `GND`
- `Data In` -> `GPIO 4`

A **330 Ω resistor** is placed in series with the data line between the microcontroller and the ring.

Important notes:
- use **Data In**, not Data Out
- share the same ground between ESP32 and ring
- power is supplied through USB during current development
- battery integration is planned as a later step

### Translucent enclosure
The ring is intended to illuminate a translucent body so that the box itself changes visible color according to fruit state.

---

## 3. Fabrication-related Hardware Considerations

Because the project is part of a Digital Fabrication course, the hardware setup is closely linked to physical design constraints.

### Retail physical setup
The retail prototype includes:
- a miniature supermarket shelf concept,
- a smart tag enclosure,
- a sensor mounting mechanism designed to position the sensor close to the fruit while protecting it physically.

The design evolved through several iterations:
1. front-facing tag with cable,
2. cable routed under the produce box to a clamp and sensor arm,
3. wireless separation between sensing node and display/tag.

### Educational physical setup
The educational prototype is intended to be fully contained in a single light-diffusing box that can be used in:
- school cafeterias,
- classroom demos,
- awareness activities around food waste.

---

## 4. Practical Setup Notes

### Power
At the current stage:
- the retail ESP32 is typically powered through USB,
- the Raspberry Pi is powered independently,
- the educational ESP32-C3 is also powered through USB.

Battery operation is possible, especially for the educational version, but was not the main integration path during initial testing.

### Sensors and calibration
The BME680/BME688 requires:
- warm-up,
- stabilization,
- baseline calibration in ambient air.

For that reason, all final firmware versions use a **per-session baseline** rather than fixed absolute values.

### Reliability notes
The most common hardware issues encountered were:
- unstable temporary wiring,
- Wi-Fi/hotspot problems in the connected prototype,
- missing cables or connectors,
- fabrication delays affecting enclosure integration.

---

## 5. Recommended Documentation to Add Later

This file can be extended with:
- wiring photos,
- pinout diagrams,
- enclosure photos,
- 3D print screenshots,
- laser-cut shelf assembly images.
