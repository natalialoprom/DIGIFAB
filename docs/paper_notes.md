# Paper Notes

## Context

The final paper will be written in a short ACM-style format, with limited length. Because of that, the paper will need to be selective and focused. It cannot include every implementation detail, so the repository and supporting documentation should carry much of the technical depth that does not fit into the paper.

The paper belongs to a **Digital Fabrication** course, so it should not be framed only as an embedded-systems or sensing paper. It should reflect the broader making process:
- product design,
- fabrication iterations,
- electronics,
- prototyping constraints,
- and experimental validation.

---

## Suggested Paper Focus

The paper should present the project as a **digital fabrication process resulting in two complementary smart-freshness prototypes**:
- a connected retail prototype,
- and an educational light-based prototype.

The contribution is not only the final code or sensing logic, but also:
- the design evolution,
- the fabrication decisions,
- the handling of practical constraints,
- and the validation of the sensing approach through experiments.

---

## Suggested Structure

### 1. Introduction
Explain:
- the food-waste problem,
- the motivation for freshness-aware systems,
- and the relevance to SDG 12.

Briefly introduce the two prototypes and their intended contexts:
- supermarket,
- school cafeteria / classroom.

### 2. Related work / state of the art
Keep this short and targeted.

Possible angles:
- smart food monitoring systems,
- gas sensing or low-cost environmental sensing for food condition,
- electronic shelf labels / smart retail systems,
- educational interactive devices for sustainability awareness.

This section should be concise due to space limits.

### 3. Design and fabrication process
This section is especially important for the course context.

Include:
- shelf concept,
- tag evolution,
- sensor-mount evolution,
- educational box concept,
- fabrication methods considered,
- digital fabrication constraints,
- iterative redesign decisions.

### 4. System implementation
Explain the two architectures briefly:

- **Retail prototype**
  - ESP32 + sensor
  - Raspberry Pi + e-ink + dashboard

- **Educational prototype**
  - ESP32-C3 + sensor + NeoPixel ring

Keep the implementation description practical and readable.

### 5. Experimental methodology
Describe:
- sensor warm-up,
- baseline calibration,
- comparison between ambient, fresh oranges, and overripe oranges,
- use of baseline-relative gas and humidity changes.

### 6. Results and discussion
Use a small number of clear figures and summarize:
- fresh oranges caused moderate changes,
- overripe oranges caused strong humidity rise and strong gas resistance drop,
- threshold logic was then derived from these results.

Also discuss limitations briefly.

### 7. Conclusion
Conclude with:
- feasibility of the approach,
- relevance of dual prototype strategy,
- future work such as more repeated trials and improved enclosures.

---

## Main Messages to Preserve

Even if the paper is short, these ideas should survive:

1. **The project is about digital fabrication as much as sensing.**
2. **Two prototypes emerged from the same concept but serve different contexts.**
3. **The system works comparatively relative to a baseline, not through an absolute freshness index.**
4. **The orange experiment supports the design of the prototype logic.**
5. **Constraints and iteration were an essential part of the process.**

---

## Material That Can Be Left to the Repository

Because space is limited, these can be expanded in GitHub/Notion instead of in the paper:

- full wiring details,
- dashboard route descriptions,
- long code explanations,
- full experiment logs,
- all fabrication notes,
- complete version history,
- implementation quirks and debugging details.

---

## Figures Worth Prioritizing

With only a few figures possible, prioritize those that communicate the most:

1. **One image showing both prototype directions**
   - retail setup and educational light box
   - or a combined figure of the two concepts

2. **One design/fabrication figure**
   - shelf/tag iteration or enclosure evolution

3. **One experiment figure**
   - the most informative plot from the orange study
   - probably gas resistance/humidity comparison or the boxplots

If needed, combine subfigures into one compact multi-panel figure.

---

## Writing Tone

Use a tone that is:
- technical,
- clear,
- concise,
- grounded,
- and not exaggerated.

Avoid claiming:
- universal freshness detection,
- scientific-grade spoilage prediction,
- or product-ready deployment.

Prefer language such as:
- “baseline-relative indication,”
- “exploratory experiment,”
- “prototype logic,”
- “feasibility demonstration,”
- “digital fabrication iteration.”

---

## Key Phrases That May Be Useful

- baseline-relative freshness assessment
- local microenvironment sensing
- dual-prototype design
- smart shelf concept
- educational sustainability artifact
- low-cost embedded sensing
- iterative digital fabrication workflow
- practical prototyping constraints

---

## Immediate Next Writing Tasks

When paper writing starts, the first useful outputs to prepare are:
1. a short abstract,
2. a one-paragraph introduction,
3. a compact related-work shortlist,
4. a figure selection decision,
5. a compressed methodology subsection based on the orange experiment.
