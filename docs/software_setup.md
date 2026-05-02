# Software Setup

## Overview

This project contains two software stacks:
1. a **networked retail stack** with an ESP32 Feather and a Raspberry Pi,
2. a **local educational firmware** running entirely on an ESP32-C3.

Both depend on Arduino-based firmware for sensor acquisition, while the retail prototype additionally includes a Python/Flask application on the Raspberry Pi.

---

## 1. Retail Prototype Software

### Components
- Arduino firmware for **ESP32 Feather**
- Python Flask server for **Raspberry Pi**
- e-ink rendering logic
- dashboard routes for browser access

### ESP32 Feather firmware
The ESP32 firmware is responsible for:
- reading the BME680/BME688 sensor,
- creating or using a baseline,
- computing baseline-relative metrics,
- assigning a freshness status,
- sending the data to the Raspberry Pi over Wi-Fi.

Typical outputs sent to the server include:
- product name,
- status,
- price,
- temperature,
- humidity,
- gas resistance.

### Raspberry Pi software
The Raspberry Pi runs a Flask app that:
- listens for updates on `/update`,
- stores the current state,
- renders the e-ink price tag,
- serves pages such as:
  - `/store`
  - `/dashboard`
  - `/offers`
  - `/history`

### Python environment
A Python virtual environment is recommended.

Example setup:

```bash
python3 -m venv env
source env/bin/activate
pip install flask pillow adafruit-blinka adafruit-circuitpython-epd
```

### Running the Flask server

```bash
cd ~
source env/bin/activate
python3 server.py
```

### Accessing the dashboard
Once the Raspberry Pi is running and connected to the local network, the pages can be accessed from another device using:

```text
http://<raspberry-pi-ip>:5000/store
http://<raspberry-pi-ip>:5000/dashboard
http://<raspberry-pi-ip>:5000/offers
http://<raspberry-pi-ip>:5000/history
```

---

## 2. Educational Prototype Software

### ESP32-C3 firmware
The educational firmware runs locally on the ESP32-C3 and performs:
- sensor warm-up,
- baseline calibration,
- repeated sampling,
- baseline-relative classification,
- NeoPixel color output.

No server, Wi-Fi, or external dashboard is required for this version.

### Main logic
The firmware:
1. warms up the sensor,
2. computes a baseline in ambient air,
3. smooths gas-drop and humidity-rise values,
4. classifies the current state,
5. updates the NeoPixel ring.

Typical educational states:
- `Fresh`
- `Ripe`
- `Very ripe`

These are mapped to:
- green,
- yellow,
- red.

---

## 3. Arduino IDE Setup

### Required libraries
Install the following libraries through the Arduino IDE Library Manager:

- **Adafruit BME680 Library**
- **Adafruit NeoPixel**
- dependencies required by the Adafruit sensor stack

### Boards
Install ESP32 board support and select:
- the appropriate ESP32 Feather-compatible target for the retail prototype,
- the appropriate ESP32-C3 target for the educational prototype.

### Serial monitor
Use the serial monitor at:

```text
115200 baud
```

This is used for:
- debugging,
- baseline verification,
- experiment logging,
- live inspection of sensor behavior.

---

## 4. Wi-Fi and networking notes

The retail prototype depends on:
- the ESP32 being able to connect to the same network as the Raspberry Pi,
- the Raspberry Pi Flask server being reachable from the ESP32.

During development, both:
- mobile hotspots,
- and Raspberry Pi-hosted hotspots

were tested.

Because Wi-Fi configuration was one of the main practical friction points, the educational prototype was intentionally designed as a fully local system.

---

## 5. Repository Organization

Suggested locations in the repository:

- `retail_prototype/esp32_feather/`  
  for supermarket firmware

- `retail_prototype/raspberry_pi/`  
  for Flask server and e-ink logic

- `educational_prototype/esp32_c3/`  
  for classroom light-box firmware

- `experiments/`  
  for CSVs, scripts, and analysis artifacts

---

## 6. Future software improvements

Potential next steps include:
- CSV logging on the Raspberry Pi,
- manual override from the dashboard,
- support for multiple products,
- recalibration button for the educational version,
- more explicit product-specific calibration profiles.
