# Optics Selection for High-Power Laser Systems

## When to use this file

Reach for this file when **specifying optics** — picking a substrate, reading a coating datasheet, or sizing a lens against the laser's pulse energy and fluence. For day-to-day operational care, see `laser_optics_cleaning.md`. For Gaussian beam physics, see `gaussian_beam_theory.md`. For worked process formulas, see `laser_process_calculations.md`.

---

## 1. Choosing the Substrate

Glass dominates laser optics for three converging reasons: it transmits the working wavelength, it stays mechanically rigid under load, and its surface can be polished to fractions of a wavelength. The honest tradeoff is that no glass is perfectly transparent — at high average power, even a "lossless" lens absorbs enough light to become a thermal element in the system.

**Working number for BK7:** about **0.04% absorption per pass.**

| Average laser power | Power absorbed in a BK7 lens |
|---|---|
| 100 W | ~40 mW |
| 1 kW | ~400 mW |

At the kilowatt scale that absorbed power is no longer trivial. Local heating warps the glass surface, the surface curvature bends the wavefront, and the focal plane drifts during a job — the canonical **thermal lensing** failure mode. Fused silica has lower absorption and better thermal stability, which is why the standard answer for high-power systems is "switch to fused silica."

**Other substrate properties worth checking up front:**
- **Chemical stability** — does it react with ambient humidity? Some specialty glasses fog without sealed storage.
- **Hardness** — softer glasses scratch more readily during routine cleaning.
- **Long-term creep** — high-index or low-Tg glasses can sag noticeably over years.

For typical IR fiber-laser work, **BK7** is the everyday choice and **fused silica** is the upgrade tier. Both are chemically stable and tolerate the standard solvent set.

> **Engineer's intuition:** BK7 is fine up to around 100 W average. From 200 W into the kW range, switch to fused silica — not because BK7 fails outright, but because thermal lensing slowly degrades focal-spot quality long before the lens shows any visible damage.

---

## 2. Why Molded Glass Doesn't Make the Cut

Glass molding is cheap and good enough for general illumination optics. It is not good enough for laser optics. Two recurring failure modes:

- The molded surface deviates from the target curvature by enough to noticeably aberrate a focused spot.
- Surface defects — both scratches and digs — at molded-grade quality are large enough to act as local absorbers under laser flux.

Polished, ground optics are the floor for any laser-grade application.

---

## 3. Scratch-Dig Specification

Scratch-dig is a two-number quality grade for surface defects, used by every laser-optics vendor:

- **Scratch number** — graded on a 10–80 scale (lower = cleaner) by how brightly a defect reflects under standardized inspection lighting. Length and clear-aperture position both contribute to the grade.
- **Dig number** — graded on the size and density of pit-like surface holes, scaled to the optic's diameter.

| Grade | Where it fits |
|---|---|
| 60-40 | Commercial / illumination optics |
| **40-20** | **Standard for general-purpose laser optics** |
| **20-10** | **Precision laser applications** |
| **10-5** | **Most demanding — e.g. intra-cavity optics** |

> **Engineer's intuition:** A 20-10 surface isn't just "prettier" than a 40-20 — at GW/cm² peak intensities, every scratch and every dig is a candidate damage initiation site. Match the grade to your fluence, not to your purchase order.

---

## 4. Optical Coatings: AR and HR

Without a coating, every glass-air interface reflects roughly **4%** by Fresnel reflection alone. A laser-grade dielectric coating changes that by orders of magnitude.

- **Anti-reflection (AR) coatings** — quarter-wavelength dielectric stacks tuned to the operating wavelength. Reflection drops from ~4% to as low as **0.01%** per surface.
- **High-reflection (HR) coatings / dichroic mirrors** — same architecture but with half-wavelength stacks, designed to reflect rather than transmit.

Single-metal-layer coatings (bare aluminum, gold, etc.) cannot survive high-power laser flux and should not be used in the beam path. The cleaning techniques in the companion file still apply to them, but the coating itself will fail before contamination matters.

### How to read a transmission spec

A transmission spec like **T = 99.8%** typically implies about **0.1% reflection per uncoated glass-air interface** (or ~0.2% per coated surface — the convention varies between vendors, so always read the datasheet carefully). Reflection is also a function of:
- **Angle of incidence (AOI)** — coatings are designed for a specific AOI; deviating shifts the entire reflection curve.
- **Polarization state** — at off-normal AOI, s- and p-polarized light see different reflection coefficients.

### Why absorption deserves its own paragraph

Reflection numbers are easy to spec. Absorption numbers are easy to underestimate. Run the arithmetic:

> **0.01% absorption × 100 W = 10 mW.** That 10 mW is dissipated in roughly 10 µm of coating sitting on a glass with low thermal conductivity. The local temperature can climb enough to:
> - bow the surface (shifting the focal plane in real time),
> - shift the coating's spectral response,
> - delaminate or crack the coating outright.

The takeaway: for high-power sizing, **damage threshold** is a more honest design number than transmission and absorption alone.

---

## 5. Damage Threshold and Sizing

Damage threshold is published as a fluence (J/cm²) at a specific wavelength and pulse width. To size pulse energy against it:

```
Max pulse energy ≈ Damage_threshold [J/cm²] × Beam_area [cm²] / 2
```

The factor of 2 accounts for the Gaussian profile — **peak fluence at the beam center is twice the average over the spot.** (Derivation in `gaussian_beam_theory.md` §2.)

### Scaling damage threshold to a different pulse width

The published threshold is conditioned on a particular pulse width. To estimate it at a different pulse width, scale by the inverse square root of the pulse-width ratio:

```
F_th(τ) ≈ F_th(τ_ref) × √(τ / τ_ref)
```

This is approximate and breaks down between thermal and non-thermal regimes (ns ↔ fs are not exchangeable). Always verify against vendor data when crossing regimes.

### Derate before you commit

Apply a **2× to 10× safety factor** between calculated maximum and operating fluence. Reasons:
- Damage-threshold tests report **50% damage probability** statistically — half the test sites fail at the published number.
- Real-world contamination, alignment drift, and beam-quality degradation all eat margin.

> **External reference:** Edmund Optics' tech-tools page on laser damage threshold scaling has a fuller treatment if you need the full statistical and pulse-width-scaling math.
