# Laser Dicing and Cutting

## When to use this file

For understanding **how laser cutting actually works** at the depth and quality level that matters in semiconductor and PCB processing — the difference between fusion cutting, micromachining, and dicing; what limits maximum cut depth; how polarization, material class, and stack-up govern recipe choice. For ablation fundamentals, see `laser_ablation.md`. For weld modes, see `laser_welding.md`. For computing fluence and pulse parameters, see `laser_process_calculations.md`.

---

## 1. Cutting vs. Dicing — The Distinction

Heavy-industrial laser cutting is dominated by **fusion cutting**: a high-power CW or quasi-CW laser melts a kerf and a high-velocity assist gas blows the molten material out. One pass per cut, kerf widths and tolerances in the **hundreds of micrometers**.

**Micromachining** uses ultrafast lasers (UFL) — high peak power, clean Gaussian profiles, lower average power. Throughput strategy is **many fast passes** rather than one slow pass. Accuracy is in the micrometer range.

**Dicing** is something different again — historical term originally borrowed from the dice cube of gambling, later adopted for the operation of separating a wafer into individual chips.

| Operation | What happens |
|---|---|
| **Cutting** | Kerf goes all the way through. Material separates in one step. |
| **Dicing** | Kerf stops at a defined depth. Separation is a second step (mechanical cleavage). |

The two-step approach has practical advantages:

- **Faster overall.** The combined process is much faster than cutting all the way through.
- **Less debris.** Less material is ablated, so less plume to manage.
- **Backside protection.** The exit side of the wafer (and any dicing tape) never sees direct laser radiation.
- **Cleaner edges.** Mechanical cleavage of brittle material along a pre-scribed groove gives sharper edges than full-depth cutting.

---

## 2. Stealth Dicing — A Special Case

When the material is **transparent at the laser wavelength** (silicon at certain wavelengths, sapphire, glass), a focused beam delivers low fluence at the entry surface but high fluence inside the bulk. With pulse parameters tuned correctly, the in-bulk fluence reaches a threshold for either:

- localized fracture nucleation,
- localized internal stress modification.

Brittle material can then be cleaved along the modified line — either mechanically or with a localized heat source. The result: **very fast, debris-free, no surface damage**.

This is the dominant approach for high-volume Si and SiC dicing in semiconductor manufacturing.

---

## 3. Phases of Multi-Sweep Cutting

For non-stealth, ablative cutting the kerf deepens over multiple sweeps and the physics changes from sweep to sweep:

### Sweep 1 — pristine surface
The first pass meets a flat surface perpendicular to the beam. Removal rate is high, geometry is simple.

### Sweep N — cumulative effects
Subsequent sweeps face a surface modified by previous passes:
- **Elevated temperature** near the cut.
- **Different reflectance** at the now-roughened surface.
- **Effective absorption depth** changes as the surface profile evolves.

Removal rate typically stays high for the first few sweeps and **then tapers as geometry changes**.

### Why removal eventually stops

As the groove deepens, the **angle between the beam and the cut wall approaches parallel**. A glancing-incidence beam reflects more than it absorbs, scattering its energy down the groove without coupling into the wall material. This wall-angle limit defines the **maximum cut depth** for a given focused beam.

The geometry is just a right triangle:
- the **focal-spot diameter** sets the kerf width at the top,
- the **minimum stable wall angle** (the steepest slope where wall absorption still couples) sets the side,
- the **height of that triangle** is the maximum cut depth before wall geometry collapses the process.

Once the workpiece is thicker than that triangle, no single-column cut will get through. You either widen the entry with parallel passes (the 200 µm rule below), or accept that this focal-spot/wall-angle combination is fundamentally outside its range.

> **Engineer's intuition:** A typical focused beam reaches a maximum cut depth of about **200 µm** in average materials. Deeper cuts require widening the groove with parallel passes — and the number of passes scales with the **square of the depth**. Doubling the cut depth quadruples the cut time.

The **aspect ratio** is the cut depth divided by the entry width. Most ablative cutting sits in the 1–3 range; specialized geometries with self-funneling wall reflectivity (see §5) can reach 50:1 or higher.

---

## 4. Polarization Matters Once There's a Wall

The first sweep over a flat, pristine surface is **symmetric** — the surface is perpendicular to the beam, polarization is largely irrelevant.

Once a steep wall has formed in the cut direction, the **absorption-vs-reflection ratio at the wall depends strongly on the polarization state** relative to the wall geometry. With a **linearly polarized** beam:
- The cut behaves *very* differently in X versus Y if linear polarization is fixed in machine frame.
- "Following the cut direction" with a polarization rotator is technically possible but mechanically awkward.

The standard solution is to convert the laser output to **circular polarization**. X and Y cuts then behave identically, at the cost of slightly reduced single-direction efficiency.

---

## 5. Material Class Behavior

Cuttability varies dramatically by material class:

### Hard, high-melt materials (ceramics, diamond, Al₂O₃)
Ablate cleanly — high binding energy means sharp threshold transitions and clean geometry. **Behave well under laser shaping.**

### Soft, low-melt, low-thermal-conductivity materials
**Significantly harder to cut cleanly.** Specific failure modes:
- **Glass and silicon at melt** — reflectivity skyrockets due to a self-healing molten surface; the process becomes inefficient. The melt also sloshes around under nearby shockwaves.
- **Plastics and polymers** — molten material flows back into the groove. They are also semi-transparent at IR wavelengths, so applied energy spreads over long absorption lengths inside the material at low fluence — and there's nowhere for the heat to escape.

UFL helps with all of the above by providing some "cold" ablation behavior (see `laser_ablation.md` §7). **UV and mid-IR wavelengths** also help by keeping energy localized near the surface where it's wanted.

### Self-funneling cuts (the special case)

There are configurations where the **wall surface forms a film with the right thickness and reflectivity** to act as a waveguide, channeling laser energy down into the cut. Wall angles approach parallel to the beam direction, generating very high aspect-ratio holes and cuts. This is exploited in deep-via drilling.

---

## 6. Dissimilar Materials in One Cut

Real-world cutting often crosses heterogeneous stacks where adjacent materials have **opposite** laser requirements.

### Example 1 — PCB (epoxy + glass fibre)
- **Glass fibres** need high peak power. The fibre's circular cross-section acts as a small lens, focusing the beam onto itself; cut quickly before the fibre forms a molten glob.
- **Epoxy** can't tolerate heat at all — charred edges show up immediately if the recipe runs hot.

The recipe compromise: **high scan speed + cooling gas** to keep the epoxy cool, **high pulse energy + correct wavelength** to ablate the fibres efficiently.

### Example 2 — blind-via drilling (PCB stack)
A drill through several epoxy layers reinforced by fibre and copper layers, **stopping cleanly at a specific copper layer** without damaging the underlying material.

The trick: a metal film **shocked** by an appropriate laser pulse can **delaminate** from its plastic carrier — leaving the carrier intact below it. Cutting through metal but not the substrate beneath sounds impossible at first reading; in practice, the differential coupling between metal and plastic at the right pulse parameters makes it routine.

---

## 7. The Universal Compromise

A laser cutting recipe is fundamentally a **compromise between cut quality and cut speed**. Faster usually means hotter; hotter usually means more HAZ and more debris; more HAZ and debris usually mean worse quality. There is no recipe that maximizes both.

What changes between applications is **which corner of the trade-off matters more**:
- Wafer dicing optimizes for clean edges.
- PCB cutting optimizes for throughput per dollar of laser.
- R&D prototyping optimizes for repeatable, well-characterized parameters.

The recipe is downstream of the priority — pin the priority first, then tune around it.
