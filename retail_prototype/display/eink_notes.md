# E-ink Notes

## Overview

The retail prototype uses an **Adafruit ThinkInk 2.13" e-ink display** connected to a **Raspberry Pi**. The purpose of this display is to emulate a supermarket electronic shelf label and provide a physically grounded output device for the smart shelf concept.

The e-ink display is updated by the Flask server running on the Raspberry Pi whenever new data is received from the ESP32 sensing node.

---

## Role in the prototype

The e-ink display is used to show:
- product name,
- freshness-related state,
- current price,
- compact sensor information if desired.

It acts as the physical output corresponding to the dashboard, making the system feel closer to a real retail smart-tag deployment.

---

## Why e-ink was chosen

The display was chosen because it fits the supermarket use case well:

- it resembles electronic shelf labels used in retail,
- it is visually clean and easy to read,
- it consumes little power compared to always-on displays,
- and it adds a strong product-design component to the prototype.

Even if the full system remains a prototype, the e-ink output helps communicate the intended application clearly.

---

## Software control

The display is controlled from the Raspberry Pi using:
- **Python**
- **Adafruit Blinka**
- **Adafruit CircuitPython EPD libraries**
- **Pillow (PIL)** for image and text rendering

The Flask server typically:
1. receives a product update from the ESP32,
2. updates the current internal state,
3. generates a new image buffer,
4. sends the rendered image to the e-ink display.

---

## Display rendering strategy

The display content is kept intentionally simple.

Typical information shown:
- uppercase product name
- current state (`Fresh`, `Use soon`, `Discount`)
- current price
- optional compact footer with:
  - temperature
  - humidity
  - gas value

This is designed to mimic a supermarket price label rather than a full dashboard.

---

## Typical Python rendering flow

The display update logic follows this pattern:

1. create a blank image canvas
2. draw text onto the canvas with PIL
3. send the image to the e-ink driver
4. trigger a display refresh

A simplified structure looks like this:

```python
image = Image.new("L", (250, 122), 255)
draw = ImageDraw.Draw(image)

draw.text((10, 8), product.upper(), font=font_medium, fill=0)
draw.text((10, 35), status.upper(), font=font_medium, fill=0)
draw.text((10, 68), price, font=font_large, fill=0)

footer = f"T:{temp}  H:{hum}  G:{gas}"
draw.text((10, 102), footer, font=font_small, fill=0)

display.image(image)
display.display()