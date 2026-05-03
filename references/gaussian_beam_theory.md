# Gaussian Beam Theory Reference

## When to use this file

For conceptual questions about laser beam physics — propagation, focusing, units, what symbols mean, why formulas have the constants they do. Companion to `laser_process_calculations.md` which covers practical formulas with worked examples.

This file is structured around the conceptual stumbling points engineers hit when they first work with Gaussian beam optics. Each section ends with the "engineer's intuition" — the takeaway that matters in practice.

---

## 1. Gaussian Beam Intensity Distribution

A laser beam from a real laser has an approximately Gaussian intensity profile in the radial direction:

```
I(r) = I₀ · exp(-2r² / ω²)
```

Where:
- `I(r)` = irradiance at radial distance r [W/cm²]
- `I₀` = peak irradiance at beam center [W/cm²]
- `r` = radial distance from beam axis [cm]
- `ω` = beam radius at the 1/e² intensity point [cm]

### Beam diameter convention

Industry standard defines beam diameter as `D = 2ω`, where ω is the radius at which intensity drops to **1/e² ≈ 13.5%** of peak. This is NOT the FWHM (full width at half maximum).

Conversion: `D_FWHM = D_1/e² · √(ln(2)/2) ≈ 0.589 · D_1/e²`

If a vendor specs a beam diameter, always verify which convention they use. Mixing the two introduces a ~1.7x error.

---

## 2. Why the "2" in I₀ = 2P/(πω²)

The peak intensity of a Gaussian beam is:

```
I₀ = 2P / (πω²)
```

The factor of 2 is not arbitrary — it falls out of integrating the Gaussian profile over the entire beam cross-section to recover total power P:

```
P = ∫₀^∞ I(r) · 2πr dr = I₀ · πω²/2
```

Solving for I₀ gives `2P/(πω²)`.

### Intuition

If the beam were a flat-top with uniform intensity inside radius ω, then `I = P/(πω²)` (no factor of 2). Gaussian beams concentrate energy at the center, so peak intensity is 2× the would-be flat-top average. The "effective area" of a Gaussian is `πω²/2`, not `πω²`.

### Important consequence: 1/e² radius doesn't contain all the power

The 1/e² radius contains **86.5% of total power**, not 100%. The remaining 13.5% lies outside in the Gaussian tail.

### Engineering implication

When calculating fluence thresholds (ablation, damage), always use **peak fluence**, not average:

```
F_peak = 2 · F_avg = 2E / (πω²)
```

Using F_avg underestimates the actual fluence at beam center by 2x — leading to missed ablation thresholds, surprise damage, or process drift.

For high-M² beams (M² > 2), the peak factor drops to ~1.5–1.8 (energy is more spread out). For pure flat-top beams, the factor is 1.

---

## 3. Units: Irradiance vs Fluence

These two quantities are commonly confused but mean different things:

| Quantity | Symbol | Unit | When to use |
|---|---|---|---|
| Irradiance / Power density | I | W/cm² | CW lasers, instantaneous power per area |
| Fluence / Energy density | F | J/cm² | Pulsed lasers, single-pulse energy per area |
| Power | P | W | Continuous power |
| Pulse energy | E | J | Per-pulse energy |

### Conversion

```
F = I · t_pulse                    (for rectangular pulse shape)
E = P_avg / f_rep                  (pulse energy from avg power and rep rate)
```

### Engineer's intuition

For pulsed lasers (most laser manufacturing), **fluence is the dominant parameter** — it determines whether you ablate, melt, or pass through unchanged. Material thresholds are typically published as J/cm².

For CW lasers, **irradiance is the dominant parameter** — it sets steady-state heating rate.

If you mix them up in a calculation, you'll be off by a factor of pulse_width × rep_rate (the "duty cycle"), which for ns pulses at kHz rates is ~10⁻⁵ — five orders of magnitude.

---

## 4. Beam Propagation: ω(z)

A focused or diverging Gaussian beam has a hyperbolic envelope. The beam radius at axial position z is:

```
ω(z) = ω₀ · √(1 + (z/z_R)²)
```

Where:
- `ω₀` = waist radius (minimum beam radius) [m]
- `z` = axial distance FROM the waist [m]
- `z_R` = Rayleigh range [m]

### What is z?

`z` is position along the propagation axis, with **z = 0 at the beam waist** (focal point). It is positive after the waist (downstream) and negative before (upstream). The geometry is symmetric around z = 0 — the beam contracts to ω₀ at the waist, then expands again.

### Engineer's intuition for z

When you focus a laser onto a workpiece, the design intent is z = 0 at the workpiece surface — that's where the spot is smallest and fluence is highest. Surface flatness deviations (web flutter, roll eccentricity, surface roughness) push the workpiece to non-zero z, growing the actual beam radius hitting the surface.

---

## 5. Rayleigh Range z_R

```
z_R = π · ω₀² · n / λ              (idealized, M² = 1)
z_R = π · ω₀² / (M² · λ)           (real beams, M² > 1)
```

Where:
- `n` = refractive index of the medium (≈1 for air, 1.5 for glass, 1.33 for water)
- `λ` = vacuum wavelength

### What z_R physically means

z_R is the distance from the waist at which:

| Property | Value at z = z_R |
|---|---|
| Beam radius ω | √2 · ω₀ |
| Beam area πω² | 2 · πω₀² (doubles) |
| Peak intensity | I₀ / 2 (halves) |
| Fluence | F₀ / 2 (halves) |

### Common confusion: "where r doubles?"

**No — z_R is where the AREA doubles** (radius × √2 ≈ 1.41).

The position where ω(z) = 2·ω₀ (radius literally doubles) is at `z = √3 · z_R ≈ 1.73 z_R`. There, area = 4× and intensity = 1/4. This point doesn't have a special name and isn't commonly used.

### Why z_R matters in engineering

z_R defines the **process window** along the optical axis. For |z| < z_R, beam properties don't change much. For |z| >> z_R, the beam is in the far field and has clearly diverged.

Depth of focus is typically defined as `DoF = 2·z_R` (the full ±z_R range).

### The role of n (refractive index)

The refractive index n appears because the beam's *actual wavelength* in a medium is `λ_medium = λ_vacuum / n`. The strict formula uses λ_medium; using λ_vacuum requires multiplying by n.

In laser manufacturing in air, n ≈ 1.0003 → just use n = 1 and ignore. n only matters when:
- Focusing inside transparent solids (laser glass welding)
- Fiber optics
- Immersion lithography
- Laser processing inside electrolytes or other liquids

---

## 6. The M² Factor

M² is the beam quality factor — the ratio between the actual beam's `ω·θ` product (waist × divergence) and that of a perfect Gaussian:

```
M² = (ω₀ · θ)_actual / (ω₀ · θ)_perfect_gaussian
```

| M² value | Beam quality | Typical source |
|---|---|---|
| 1.0 | Theoretical perfect Gaussian | None (idealization) |
| 1.05–1.2 | Excellent | Single-mode fiber laser |
| 1.2–1.5 | Good | Solid-state, well-aligned |
| 1.5–3 | Mediocre | Multimode fiber, poorly aligned |
| 3+ | Poor | Multimode bulk, fiber-coupled diodes |

### Where M² shows up (at fixed focusing geometry: same ω_f, F, λ)

```
ω₀ ∝ M²              (focused waist grows linearly with M²)
θ_far = ω_f / F      (far-field divergence is set by geometry, NOT by M²)
z_R ∝ M²             (Rayleigh range GROWS with M²)
DoF = 2·z_R ∝ M²     (depth of focus grows proportionally)
F_peak ∝ 1/(M²)²     (peak fluence drops quadratically — spot area grows ∝ (M²)²)
I_peak ∝ 1/(M²)²     (same reason as F_peak)
```

### Pitfall: reading z_R = πω₀²/(M²λ) without substituting ω₀

The z_R formula has M² in the denominator, which makes it look like z_R ∝ 1/M². That conclusion is only valid if you hold ω₀ fixed (e.g., comparing two beams pre-shaped to the same waist size). **At fixed focusing geometry**, ω₀ itself scales as M², so substituting back:

```
z_R = π · (M²·λF/(π·ω_f))² / (M²·λ) = M² · λ · F² / (π · ω_f²)
```

Net effect: z_R ∝ M². The bigger focused spot diverges more slowly, so the Rayleigh range grows. Two competing M² factors (one from ω₀², one from the explicit denominator) leave a net linear M² in the numerator.

### Engineer's intuition

A beam with M² = 2 vs. M² = 1 at the same focusing geometry has:
- 2× the waist radius (ω₀ ∝ M²)
- 4× the focused spot area
- 2× the Rayleigh range and depth of focus (bigger spot diverges more slowly)
- 1/4 the peak fluence and peak intensity (energy spread over 4× the area)

The cost of bad beam quality is **peak fluence**, not depth of focus. M² is one of the dominant levers in process performance — pay for low M² when you need high fluence and small features.

For TRUMPF-class fiber lasers, M² ≈ 1.1–1.3 is typical and basically at the practical ceiling.

---

## 7. Focusing a Gaussian Beam

Standard focusing equation (focused spot DIAMETER from a collimated input):

```
D_focus = 4 · M² · λ · F / (π · D_input)
```

Where:
- `D_focus` = focused spot diameter at 1/e² [same units as λ × F / D_input]
- `D_input` = collimated beam diameter at the lens [m]
- `F` = focal length of the focusing optic [m]
- `M²` = beam quality factor

### Symbol convention warning

Many references write this in equivalent radius form:

```
ω₀ = M² · λ · F / (π · ω_input)         (radii)
ω₀ = 2 · M² · λ · F / (π · D_input)     (radius from input diameter)
```

These all represent the same physics, but the constant changes (2, 4) depending on whether ω or D appears in the formula. **Always verify whether a formula uses radius or diameter** before plugging in numbers.

### Counterintuitive: bigger input → smaller spot

To make `D_focus` smaller, you want `D_input` larger. This is why beam expanders (Galilean, Keplerian) are placed BEFORE focusing optics — expanding the input beam shrinks the focus.

### The fundamental tradeoff: spot size vs. depth of focus

Depth of focus scales as:

```
DoF ≈ 2 · z_R = 2π · ω₀² / (M² · λ)
```

So `DoF ∝ ω₀²`. **Halving the spot size quarters the depth of focus**:

```
ω₀ ↓ 1/2  →  DoF ↓ 1/4
```

This forces an engineering tradeoff:
- **Short focal length, large input → small spot, shallow DoF** (precise but unforgiving)
- **Long focal length, small input → large spot, deep DoF** (tolerant but lower energy density)

### Engineering rule for picking F-number

Set DoF/2 (= z_R) larger than your worst-case workpiece flatness deviation:

```
z_R ≥ max axial workpiece deviation (web flutter, roughness, alignment error)
```

Then accept whatever spot size that gives. The DoF is a hard floor; spot size is a soft ceiling.

---

## 8. Common Conceptual Traps

| Trap | Reality |
|---|---|
| "Beam diameter is FWHM" | Industry standard is 1/e² = 13.5% of peak. FWHM ≈ 0.59 × 1/e² diameter |
| "Peak fluence equals average fluence" | Peak = 2× average for Gaussian. Use peak vs. material thresholds |
| "z_R is where the radius doubles" | z_R is where the AREA doubles (radius × √2 ≈ 1.41) |
| "Bigger input beam → bigger focused spot" | Opposite — bigger input → smaller focused spot |
| "M² is just a number" | M² acts linearly on spot size and quadratically on peak fluence |
| "ω in the formula means radius" | Symbol conventions vary — always verify radius vs. diameter |
| "Ignore n (refractive index) in air" | Correct for air. Don't ignore for in-glass focusing or immersion |
| "Pulsed laser intensity = power/area" | For pulsed, use peak power = E/PW. Avg power gives a number ~10⁵ too small |
| "Higher overlap = better processing" | Up to a point. Past ~95% you're in thermal accumulation regime, may not be desired |

---

## 9. Symbol Glossary

| Symbol | Meaning | Units (typical) |
|---|---|---|
| `λ` | Wavelength (vacuum) | nm |
| `n` | Refractive index of medium | dimensionless |
| `ω` | Beam radius (1/e² intensity) | µm or mm |
| `ω₀` | Waist radius (at focus) | µm |
| `D` | Beam diameter (= 2ω) | µm or mm |
| `r` | Radial distance from beam axis | µm |
| `z` | Axial distance from waist | mm |
| `z_R` | Rayleigh range | mm |
| `θ` | Far-field divergence half-angle | mrad |
| `M²` | Beam quality factor | dimensionless |
| `F` | Focal length | mm |
| `P` | Power (avg, for pulsed) | W |
| `P_peak` | Peak power during pulse | kW or MW |
| `E` | Pulse energy | mJ or µJ |
| `PW` | Pulse width (FWHM) | ns |
| `PRF` | Pulse repetition frequency | kHz |
| `I` | Irradiance / intensity | W/cm² or MW/cm² |
| `F_fluence` | Fluence | J/cm² |
| `DoF` | Depth of focus | mm |
