# Laser Welding: Conduction, Transition, Keyhole

## When to use this file

For deciding **which weld mode you're operating in** based on peak power density at the focus, and for understanding the geometry and trade-offs that come with each. For material removal (rather than joining), see `laser_ablation.md`. For cutting and dicing, see `laser_dicing.md`. For computing peak intensity from average power, PRF, pulse width, and focal-spot diameter, see `laser_process_calculations.md`.

---

## 1. Three Modes, Driven by Peak Intensity

A focused laser delivers fundamentally different welding behaviour as peak intensity climbs. The transition from one mode to the next is not gradual — there is a sharp crossover where the physics of energy coupling changes from surface conduction to keyhole formation.

| Mode | Peak intensity | Geometry | Aspect ratio (depth/width) |
|---|---|---|---|
| **Conduction** | ~ 0.5 MW/cm² | Shallow, wide nugget | < 1 |
| **Transition** | ~ 1 MW/cm² | Shallow keyhole | ~ 1 |
| **Keyhole / penetration** | > 1.5 MW/cm² | Deep, narrow keyhole | > 1.5 |

> **Engineer's intuition:** Three orders of magnitude in intensity span the whole map — from cosmetic surface joining to deep-section penetration welding. Knowing where on the map your process sits is half of the recipe selection.

---

## 2. Conduction Mode

At the low end (~ 0.5 MW/cm²), incident energy is absorbed at the surface and then **conducts** into the bulk. The result is a shallow, wide weld nugget — the opposite of a keyhole geometry.

**Where conduction welding is the right choice:**
- **Aesthetic welds** where surface appearance matters.
- Applications where **particulate ejection must be avoided** — for example, hermetic seam-sealing of sensor packages or sealed enclosures where any ejected debris would land back inside.
- **Thin-gauge joining** where a deep keyhole is overkill and would risk burn-through.

The mode is forgiving on alignment and focus, but slow per unit penetration.

---

## 3. Transition Mode

At medium intensity (~ 1 MW/cm²), a partial keyhole begins to form. The vapor channel is shallow and doesn't extend the full weld depth, so the aspect ratio sits near 1 (depth ≈ width).

This is historically the dominant mode for **pulsed Nd:YAG spot and seam welding** — enough penetration to make a structural joint, without the alignment sensitivity of full keyhole work.

---

## 4. Keyhole / Penetration Mode

Above ~ 1.5 MW/cm², the focus produces a **self-sustaining vapor channel** driven into the material. Vapor pressure inside the channel holds the walls open against surface tension; the laser couples efficiently into the channel walls; depth/width ratios above 1.5 are routine, and ratios above 10 are reachable with tight beam quality.

**Why keyhole is the high-throughput choice:**
- Deep penetration with a narrow weld bead — heat input per unit depth is minimized.
- HAZ is small relative to weld depth.
- Suitable for thick sections that conduction mode cannot reach at any reasonable speed.

**Trade-offs:**
- More sensitive to alignment, focal-plane drift, and beam quality.
- Spatter, porosity, and humping become possible defect modes that don't exist in conduction welding.
- Process windows are narrower — small drift in fluence can collapse the keyhole back to transition mode.

---

## 5. Driving the Mode in Practice

A given laser system can be parked anywhere on the intensity map by adjusting:

- **Pulse energy or average power** — direct control of intensity at fixed spot size.
- **Spot size** — smaller spot = higher intensity at the same power. Tuned via beam-expander setting or focus-lens choice.
- **Pulse width** — for pulsed lasers, a shorter pulse at the same pulse energy gives higher peak power.

> **Diagnostic intuition:** If you're getting a much shallower weld than expected, check whether peak intensity has fallen back below the keyhole threshold. The collapse from keyhole to transition mode isn't smooth — drop below ~ 1.5 MW/cm² and weld depth falls off a cliff. Confirm the math with the peak-intensity formula in `laser_process_calculations.md` §6.
