# Limitations

## Overview

This project successfully produced two working prototype directions, but it also involved several limitations that influenced both the physical fabrication process and the technical scope of the final result. These limitations are important not only as constraints, but also as part of the design process itself: the project evolved under real prototyping conditions rather than in a fully controlled development environment.

---

## 1. Fabrication constraints

### Laser cutter unavailability
One of the most significant practical limitations was the lack of reliable access to the laser cutter during the expected fabrication window. The shelf design for the retail prototype had already been planned digitally, but machine errors and prolonged unavailability delayed the transition from design to physical realization.

This affected:
- the final shelf fabrication timeline,
- fit testing of structural parts,
- and the ability to validate tolerances physically.

### Incomplete enclosure iterations
Several enclosure ideas were developed conceptually, but not all of them were fully fabricated or tested in final form. This was particularly true for:
- the retail tag enclosure,
- the sensor support mechanism,
- and some later wireless layout concepts.

As a result, some parts of the system remain validated mainly at the conceptual or prototype logic level rather than as completely finished physical products.

### Dependency on teammate fabrication progress
Because the work was distributed, some aspects of the final integration depend on the availability and timing of 3D printed or laser-cut parts produced by other team members.

---

## 2. Hardware and integration limitations

### Late or missing components
Some practical delays were caused by missing or late-arriving components, which reduced the available time for final integration and testing.

### Cable and connector availability
At several points, integration was slowed down by the lack of:
- specific cables,
- soldered headers,
- or connector compatibility.

A good example was the difficulty of integrating the NeoPixel ring cleanly before proper contact and connection were established.

### Battery integration not finalized
Battery-powered operation was considered, especially for the educational prototype, but the main development path focused first on achieving stable functionality through USB power. As a result, portable power remains more of an extension than a fully integrated feature.

---

## 3. Sensor and measurement limitations

### Sensor warm-up and drift
The BME680/BME688 requires warm-up and stabilization. Early measurements showed that if the baseline is taken too early, gas resistance values may still be drifting, which reduces the reliability of the computed baseline-relative metrics.

### Product-specific calibration
The threshold logic used in the current firmware versions is calibrated specifically using the orange experiment and should not be treated as a general freshness model for all fruits.

### Limited experimental scope
The current experiments:
- are exploratory,
- include a limited number of fruit conditions,
- and should be interpreted as proof of feasibility rather than statistical validation.

### Overripe sample severity
The overripe oranges tested were strongly degraded. This is useful because it produces a strong detectable signal, but it also means that the “very ripe” class is currently anchored to a rather extreme condition.

---

## 4. Networking limitations

### Wi-Fi and hotspot instability
The retail prototype depends on networking between:
- the ESP32,
- the Raspberry Pi,
- and in some cases a mobile hotspot or Raspberry Pi-hosted hotspot.

This produced several practical issues during development, including:
- failure to join some hotspot configurations,
- IP changes after reboot,
- and manual recovery after Raspberry Pi restarts.

These issues do not invalidate the prototype, but they do reduce smoothness during deployment and demo preparation.

---

## 5. Scope limitations

### Prototype, not finished product
Both versions of the system should be understood as prototypes:
- useful,
- functional,
- and demonstrative,
but not final commercial devices.

### No universal freshness claim
The system does not identify a chemical species directly, nor does it provide a universal freshness score. Its strength lies in relative detection within a specific setup.

### Limited enclosure control
The fruit experiments were done in a semi-enclosed environment rather than in a fully sealed and repeatable chamber. Therefore, air circulation and diffusion effects likely influence the measurements.

---

## 6. Documentation and research limitations

### Limited paper length
Because the final paper is constrained in length, not every design iteration, technical detail, or fabrication issue can be described in full. This makes the repository and supporting documentation especially important.

### State-of-the-art depth
A short course paper can only include a focused and concise review of related work, so the literature discussion will necessarily be limited compared to a larger research article.

---

## 7. Positive interpretation of limitations

These limitations are not simply failures or missing parts. They are also representative of real digital fabrication workflows, where:
- machines fail,
- materials arrive late,
- components do not fit perfectly,
- and systems must be rethought iteratively.

In this sense, the project is also an example of adaptive design under realistic fabrication constraints.
