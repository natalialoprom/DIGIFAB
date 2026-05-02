# Project Overview

## Smart Freshness Monitoring System

This project develops a smart freshness monitoring system aimed at reducing food waste and supporting more responsible food consumption, aligned with **UN Sustainable Development Goal 12: Responsible Consumption and Production**.

The work was developed in the context of a **Digital Fabrication** course and combines physical prototyping, embedded electronics, sensing, digital fabrication methods, and simple data-driven decision logic. The project evolved into **two complementary prototype versions**, each targeting a different use case while sharing the same sensing foundation.

## Main Motivation

Fresh produce deteriorates over time and often shows environmental changes before it is visually discarded. In retail environments, this can lead to avoidable waste if products are not identified and discounted in time. In educational environments, food waste is often discussed conceptually but not experienced through interactive systems.

The project therefore explores whether a low-cost environmental sensor can be used to detect relative changes around fruit and translate them into understandable outputs for two contexts:

1. **Retail / supermarket prototype**  
   A connected smart shelf that updates a price tag and dashboard based on freshness-related changes.

2. **Educational / school cafeteria prototype**  
   A local light-based device that changes color depending on the relative ripeness state of fruit, designed for classroom or cafeteria awareness activities.

## Prototype Versions

### 1. Retail / Supermarket Prototype

This version uses:
- **ESP32 Feather**
- **Adafruit BME680/BME688** gas, humidity, temperature, and pressure sensor
- **Raspberry Pi**
- **Adafruit ThinkInk 2.13" e-ink display**
- **Flask-based local web dashboard**

The ESP32 reads the sensor data and sends it over Wi-Fi to the Raspberry Pi. The Raspberry Pi updates both:
- an **e-ink shelf tag**
- a **retail-style web interface**

The purpose of this prototype is to simulate a smart supermarket shelf capable of:
- monitoring the local microenvironment around fruit,
- identifying relative freshness changes,
- and reflecting these changes as dynamic discount suggestions.

### 2. Educational / School Cafeteria Prototype

This version uses:
- **ESP32-C3 DevKitM-1**
- **Adafruit BME680/BME688**
- **Adafruit NeoPixel Ring 16x RGBW**
- a **translucent enclosure**

Unlike the retail version, this prototype is fully local and does not require Wi-Fi or a server. It uses a simplified output model:
- **green** = fresh
- **yellow** = ripening / use soon
- **red** = very ripe

This version is intended as a tangible educational tool for:
- schools,
- cafeterias,
- workshops,
- and classroom activities related to food waste and sensing.

## Design Rationale

The final project architecture was shaped by both conceptual choices and practical fabrication constraints. Initially, the system was conceived as a single retail-focused prototype, but over time it became clear that the sensor-and-feedback concept also had value in a more accessible and educational form.

This led to the development of two versions:
- one more connected and “product-like,”
- and one simpler, more interactive, and suitable for public demonstration or classroom use.

## Fabrication Context

Because this was a Digital Fabrication project, the work includes more than electronics and code. It also involved:
- physical shelf design,
- enclosure concepts,
- laser-cut structure planning,
- 3D printed mounting solutions,
- and iterative design changes driven by testing and practical constraints.

An important part of the project was not only what was built, but **how the design evolved** in response to:
- machine availability,
- component delays,
- integration issues,
- and limited time for fabrication.

## Current Outcome

At the current stage, both prototypes are functional at the system level:

- the **retail prototype** supports sensor reading, network communication, e-ink updates, and a dashboard;
- the **educational prototype** supports local sensing and color-based feedback using a NeoPixel ring.

Sensor experiments with oranges were also carried out to validate whether the chosen sensing approach could distinguish between:
- ambient air,
- fresh oranges,
- and overripe oranges.

These experiments support the use of **baseline-relative environmental changes** as a practical proxy for freshness state.

## Repository Purpose

This repository is intended to gather:
- firmware,
- Raspberry Pi code,
- experimental data,
- fabrication assets,
- documentation,
- and paper-related notes

in a single organized structure, making the project easier to reproduce, document, and extend.
