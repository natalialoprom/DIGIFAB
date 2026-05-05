# Retail Prototype Usage Instructions

## 1. What this prototype is

This prototype simulates a **smart supermarket shelf** for fruit. It uses:

* an **ESP32 Feather** with a **BME680/BME688** sensor to monitor the local environment around the fruit
* a **Raspberry Pi** with an **e-ink display** to show a shelf label
* a **Flask web dashboard** to display the current product state, offers, and update history

The current calibration is based on **oranges**, so the most meaningful tests should be done with oranges.

The system does **not** measure freshness as an absolute scientific value. Instead, it compares the current sensor readings to a **baseline** and interprets the changes relatively.

---

## 2. Main parts of the system

### Sensing node

* **ESP32 Feather**
* **BME680/BME688**
* powered by USB

This part reads:

* temperature
* humidity
* gas resistance

and sends the processed result to the Raspberry Pi over Wi-Fi.

### Server/display node

* **Raspberry Pi**
* **2.13" e-ink display**
* powered separately

This part:

* receives the ESP32 updates
* updates the e-ink shelf tag
* hosts the dashboard pages

---

## 3. Before starting

Make sure you have:

* the **ESP32 Feather** connected to the **BME680/BME688**
* the **Raspberry Pi** connected to the **e-ink display**
* both devices powered
* both devices on the **same Wi-Fi network with a 2.4Ghz band**
* the correct IP address of the Raspberry Pi

If the Raspberry Pi IP changes, the ESP32 code must be updated accordingly.

---

## 4. Raspberry Pi setup and launch

### Step 1 — turn on the Raspberry Pi

Power the Raspberry Pi and wait until it has fully booted.

### Step 2 — connect it to the network

Make sure the Raspberry Pi is connected to the same Wi-Fi network that the ESP32 will use. By default, a wifi hotspot with the name "prueba" and password "12341234" will work with both the Raspberry Pi and ESP32.

### Step 3 — find its IP address

On the Raspberry Pi, run:

```bash
hostname -I
```

This will return the local IP address, for example:

```bash
192.168.137.76
```

### Step 4 — start the Flask server

In the Raspberry Pi terminal:

```bash
cd ~
source env/bin/activate
python3 server.py
```

If everything is working, the terminal should show something like:

```bash
Running on http://127.0.0.1:5000
Running on http://192.168.x.x:5000
```

Leave this terminal open while using the prototype.

---

## 5. Dashboard access

From a phone or laptop connected to the **same network**, open a browser and use the Raspberry Pi IP.

Available pages:

* Storefront:
  `http://<RASPBERRY_PI_IP>:5000/store`

* Dashboard:
  `http://<RASPBERRY_PI_IP>:5000/dashboard`

* Offers:
  `http://<RASPBERRY_PI_IP>:5000/offers`

* History:
  `http://<RASPBERRY_PI_IP>:5000/history`

Example:

```text
http://192.168.137.76:5000/dashboard
```

If the page does not open:

* check that the Flask server is still running
* check that the phone/laptop is on the same network
* check that the Raspberry Pi IP has not changed

---

## 6. ESP32 setup

The ESP32 Feather must be programmed with the retail firmware. 

In the firmware, the following values must match the current setup:

* Wi-Fi name (`ssid`)
* Wi-Fi password
* Raspberry Pi update URL (`serverBase`)

Example:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverBase = "http://192.168.137.76:5000/update";
```

### Important

The `serverBase` must use the current Raspberry Pi IP.

If the Raspberry Pi IP changes, update this line and upload the code again.

---

## 7. Starting the prototype

### Step 1 — power the ESP32

Connect the ESP32 Feather by USB.

### Step 2 — let the sensor warm up

After starting, the firmware performs:

* a warm-up period
* a baseline calibration in ambient air

During this stage:

* keep the fruit away from the sensor
* do not breathe directly on the sensor
* avoid moving it too much

This step is important because the prototype compares later measurements against this initial baseline.

### Step 3 — wait for calibration to complete

The ESP32 serial monitor will show baseline messages. Once calibration is complete, it starts monitoring normally.

### Step 4 — place the oranges near the sensor

After calibration, place the oranges in the intended monitoring position near the sensor.

---

## 8. Expected behavior

The system classifies the product into one of three states:

* **Fresh**
* **Use soon**
* **Discount**

These states are based on relative changes in:

* humidity
* gas resistance

### In practice

* **ambient / no fruit nearby** should usually stay near `Fresh`
* **fresh oranges** may produce small or moderate changes
* **very overripe oranges** should produce stronger changes and are more likely to move toward `Discount`

Because the current prototype is orange-calibrated, oranges are the recommended product for testing.

---

## 9. Outputs to observe

### E-ink shelf display

The e-ink display should update to show:

* product name
* state
* price
* compact sensor footer

### Web dashboard

The dashboard shows:

* product cards
* current state
* latest readings
* offers page
* update history

### ESP32 serial monitor

For debugging, the ESP32 serial monitor at **115200 baud** shows:

* current readings
* baseline-relative values
* intermediate classification
* stable classification

---

## 10. Recommended demo procedure

A simple demonstration flow is:

### Demo A — system startup

1. Power Raspberry Pi
2. Start Flask server
3. Open dashboard in browser
4. Power ESP32
5. Let sensor warm up and calibrate

### Demo B — ambient condition

1. Leave the sensor in normal air
2. Observe the dashboard and e-ink display
3. Confirm the system is stable

### Demo C — fresh fruit

1. Place fresh oranges near the sensor
2. Wait for several update cycles
3. Observe whether humidity and gas values change slightly

### Demo D — overripe fruit

1. Replace the fresh oranges with overripe oranges
2. Wait for the system to respond
3. Observe stronger changes in the dashboard and, if thresholds are reached, the transition toward `Discount`

---

## 11. Important practical notes

### The prototype is baseline-relative

This means:

* it is sensitive to the starting conditions
* results depend on the local environment
* it should be interpreted as a relative monitoring system, not as a universal freshness meter

### The current thresholds are calibrated for oranges

The teachers should preferably test:

* oranges
* ideally including clearly fresh and clearly overripe samples

### Sensor response is not always instantaneous

Changes may take some time depending on:

* fruit condition
* distance to sensor
* enclosure geometry
* airflow
* room humidity

### E-ink updates are slow by nature

This is normal. E-ink is not a fast-refresh display.

---

## 12. Troubleshooting

### Dashboard does not open

* make sure `server.py` is still running
* check the Raspberry Pi IP again with `hostname -I`
* make sure the phone/laptop is on the same Wi-Fi network

### ESP32 does not send updates

* check Wi-Fi credentials in the Arduino code
* check that `serverBase` uses the correct Raspberry Pi IP
* check the serial monitor for Wi-Fi or HTTP errors

### E-ink does not update

* check Raspberry Pi wiring to the display
* confirm SPI is enabled
* confirm the Flask server is actually receiving `/update` requests

### Readings look wrong or unstable

* repeat the startup and let the sensor calibrate again
* avoid touching or breathing near the sensor during baseline
* test in a more stable environment
