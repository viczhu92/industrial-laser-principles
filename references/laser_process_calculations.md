# Laser Process Calculations Reference

## When to use this file

For practical calculations in laser manufacturing process design — pulse energy, spot size, fluence, scan parameters, accumulated energy, ablation threshold extraction. Companion to `gaussian_beam_theory.md` which explains the underlying physics.

All calculations assume Gaussian beam profile (M² near 1) with **1/e² beam diameter convention**. See theory file for corrections to other conventions.

## Reference setup for worked examples

Worked examples below use a representative ns fiber-laser ablation setup at industrial scan speeds. The numbers are illustrative — substitute your own parameters as needed.

| Parameter | Value | Symbol |
|---|---|---|
| Wavelength | 1064 nm | λ |
| Average power | 200 W | P |
| Pulse repetition frequency | 200 kHz | PRF |
| Pulse width | 58 ns | PW |
| Beam diameter at laser exit | 9.5 mm | D_exit |
| Beam expander magnification | 1× | BE |
| M² | 1.3 | M² |
| Focal length | 160 mm | F |
| Mark speed | 4 m/s | v |
| Hatch distance | 20 µm | H |

---

## 1. Pulse Energy

```
E_pulse = P_avg / PRF
```

**Worked example**: 200 W / 200 kHz = 200 / 200,000 = **1 mJ per pulse**

**Pitfalls**:
- PRF must be in Hz, not kHz. Forgetting the 1000x converts gives 1 J pulses (1000x too big).
- This formula assumes 100% duty in pulse generation. For laser systems with simmer/idle current, peak power per pulse may be slightly lower than calculated.

---

## 2. Focused Spot Diameter

```
D_focus = 4 · M² · λ · F / (π · D_input)
```

**Practical mixed-units form** (λ in nm, F and D_input in mm, result in µm):

```
D_focus(µm) = 4 · M² · λ(nm) · F(mm) / (π · D_input(mm)) / 1000
```

**Worked example**:
```
D_input = BE × D_exit = 1 × 9.5 = 9.5 mm
D_focus = 4 × 1.3 × 1064 × 160 / (π × 9.5) / 1000
       = 885,248 / 29.845 / 1000
       = 29.66 µm
```

**Pitfalls**:
- `D_input` is the beam diameter **AT THE FOCUSING LENS**, not at the laser exit. If a beam expander is in the path, D_input = BE_magnification × D_exit.
- Verify whether your reference formula uses radius (ω) or diameter (D). The constant differs (2 vs. 4).
- For very high-NA focusing (low F-number), aberrations and finite NA effects make this Gaussian formula approximate.

---

## 3. Average Fluence

Energy per unit area, treating the beam as if uniformly distributed within the 1/e² radius:

```
F_avg = E_pulse / (π · r²) = E_pulse / (π · (D/2)²)
```

**Worked example**:
```
r = D_focus / 2 = 14.83 µm = 14.83 × 10⁻⁴ cm
Spot area = π × (14.83 × 10⁻⁴)² = 6.91 × 10⁻⁶ cm²
F_avg = 1 × 10⁻³ J / 6.91 × 10⁻⁶ cm² = 144.7 J/cm²
```

**Pitfall**: Unit mixing is the most common error. Stay in SI (J and cm) and convert at the end.

---

## 4. Peak Fluence

The peak (center) fluence is what you compare against material thresholds, not the average:

```
F_peak = 2 · F_avg          (M² < 2, well-behaved Gaussian)
F_peak = 1.5–1.8 · F_avg    (high M² beams, more spread out)
F_peak = 1.0 · F_avg        (flat-top beams)
```

**Worked example**: 2 × 144.7 = **289.4 J/cm²**

**Pitfall**: Quoting average fluence when comparing against published ablation thresholds (which are typically peak fluence) underestimates real fluence by 2x — leading to either overshoot or under-spec processes.

---

## 5. Peak Power

Power during the pulse itself (not the time-averaged power):

```
P_peak = E_pulse / PW
```

**Worked example**: 1 mJ / 58 ns = 10⁻³ / 58 × 10⁻⁹ = **17,241 W ≈ 17.2 kW ≈ 0.0172 MW**

**Unit hack**: mJ / ns = MW directly (because 10⁻³ / 10⁻⁹ = 10⁶ = M).

**Sanity check**: P_peak / P_avg = 1 / (PW × PRF) = 1 / (58e-9 × 200e3) = 1 / 0.0116 = 86. So peak power is ~86x average for this setup. This ratio = 1/duty cycle is a useful gut check.

---

## 6. Peak Intensity (Power Density)

Peak power per unit area at the beam center:

```
I_peak = P_peak / (π · r²)
```

**Worked example**:
```
I_peak = 17,241 W / 6.91 × 10⁻⁶ cm² = 2.50 × 10⁹ W/cm² = 2.50 GW/cm²
```

**Sanity-check magnitudes for laser-material interaction regimes**:

| Regime | Peak intensity | Mechanism |
|---|---|---|
| Photothermal | < 10⁸ W/cm² (< 100 MW/cm²) | Heating, melting, evaporation |
| Photoablation | 10⁸ – 10¹¹ W/cm² (0.1 – 100 GW/cm²) | Ablation with controlled HAZ |
| Plasma generation | > 10¹¹ W/cm² (> 100 GW/cm²) | Cold ablation, plasma plume |

For ns fiber-laser ablation at industrial scan speeds, typical peak intensity is in the **1–10 GW/cm²** range — solidly in the ablation regime.

---

## 7. Rayleigh Range and Depth of Focus

```
z_R = π · ω₀² / (M² · λ)        (single-sided "Rayleigh range")
DoF = 2 · z_R                    (two-sided "Depth of Focus")
```

**Worked example**:
```
ω₀ = D_focus / 2 = 14.83 µm = 14.83 × 10⁻⁶ m
ω₀² = 2.20 × 10⁻¹⁰ m²
z_R = π × 2.20 × 10⁻¹⁰ / (1.3 × 1064 × 10⁻⁹)
    = 6.91 × 10⁻¹⁰ / 1.38 × 10⁻⁶
    = 5.00 × 10⁻⁴ m = 0.50 mm
DoF = 1.00 mm
```

**Engineering rule**: Worst-case workpiece Z-axis flatness deviation must be much less than z_R for stable processing.

**Common terminology confusion**: Some references define DoF = z_R (one-sided), others = 2·z_R (two-sided). When specifying a tolerance, always state which convention is being used.

---

## 8. Defocused Spot Size and Fluence

If the workpiece is at axial offset Δz from focus:

```
D(Δz) = D₀ · √(1 + (Δz / z_R)²)
F(Δz) = F₀ / (D(Δz) / D₀)²       (fluence drops as area grows)
I(Δz) = I₀ / (D(Δz) / D₀)²
```

**Worked example** at Δz = 0.25 mm (= 0.5 z_R):
```
ratio = √(1 + 0.5²) = √1.25 = 1.118
D(Δz) = 29.66 × 1.118 = 33.17 µm
F(Δz) = 144.7 / 1.118² = 144.7 / 1.25 = 115.7 J/cm²  (~80% of focal plane)
I(Δz) = 2.50 / 1.25 = 2.00 GW/cm²
```

**Useful rules of thumb**:

| Δz | Fluence ratio |
|---|---|
| 0 | 100% |
| 0.5 z_R | 80% |
| 1.0 z_R | 50% |
| 2.0 z_R | 20% |

---

## 9. Aperture Truncation Loss

Power transmitted by a Gaussian beam (1/e² diameter D) through a circular aperture (diameter A):

```
P_transmitted = P · (1 - exp(-2 · (A/D)²))
```

**Worked example**: 200 W beam (D = 9.5 mm) through 14 mm aperture:
```
(A/D)² = (14/9.5)² = 2.17
1 - exp(-2 × 2.17) = 1 - exp(-4.34) = 1 - 0.013 = 0.987
P_transmitted = 200 × 0.987 = 197.4 W   (1.3% loss)
```

**Quick reference**:

| A/D | Power transmitted |
|---|---|
| 0.5 | 39% |
| 1.0 | 86% |
| 1.5 | 99% |
| 2.0 | 99.97% |

**Pitfall**: Both A and D must be diameters (or both radii) using the **same convention** (1/e² is standard). The factor of 2 in the exponent is specific to 1/e² diameter.

---

## 10. Pace (Pulse-to-Pulse Distance)

Distance between adjacent pulse centers along the scan direction:

```
Pace = v / PRF
```

**Worked example**: 4 m/s / 200 kHz = 4 / 200,000 = 20 × 10⁻⁶ m = **20 µm**

---

## 11. Overlap

Two equivalent forms — pick whichever makes the conversation clearer:

```
Overlap (%)         = (D - Pace) / D
Overlap (dia/pace)  = D / Pace
```

**Worked example**: D = 29.66 µm, Pace = 20 µm:
- (29.66 - 20) / 29.66 = 32.6%
- 29.66 / 20 = 1.48 dia/pace

**Engineering ranges**:

| Process type | Typical overlap |
|---|---|
| Drilling, perforating | 0% (discrete spots) |
| Line cutting, scribing | 50–70% |
| Surface texturing, marking | 80–95% |
| Polishing, thermal smoothing | > 95% (thermal accumulation regime) |

For thin-substrate ablation cuts, overlap is typically in the 50–80% range — enough to ensure a clean cut without entering thermal accumulation that could damage temperature-sensitive material below the surface.

---

## 12. Hatch Distance and Areal Coverage

For 2D area exposure (surface texturing, area ablation), parallel scan lines spaced by `hatch distance H`:

```
Hatch overlap (dia/hatch) = D / H
```

For uniform area coverage, both `D/Pace > 1` AND `D/Hatch > 1` are typically required. Process designers often set H ≈ Pace for isotropic coverage.

---

## 13. Accumulated Energy (Pulse Train Effect)

Each point on the workpiece sees multiple pulses due to overlap. Accumulated peak fluence at a point sums contributions from all overlapping pulses.

**Linear accumulation factor** (along scan direction):

```
N_linear = 1 + Σ_N exp(-2(N · Pace / ω)²)         for N = 1, 2, 3, ...
```

The "1" represents the central pulse; the sum adds contributions from each adjacent pulse N positions away. For tight overlap, this sum can grow significantly above 1.

**Areal accumulation factor** (with hatch lines, separable Gaussian):

```
N_area = N_linear × N_hatch
```

Where `N_hatch` uses the same form but with hatch distance H instead of Pace.

**Engineering implication**: Effective fluence delivered = `N_area × F_peak_single_pulse`. Process designers can use this to back-calculate pulse parameters needed to hit a desired total fluence given a chosen overlap and hatch.

**Caveats**:
- This treats each pulse as independent — valid for fluence accumulation, but does NOT capture thermal accumulation between pulses (heat not fully dissipating before the next pulse arrives).
- Empirical factors (e.g. ~1.5x correction terms) are sometimes applied to better fit thermal effects. Calibrate against material/process when accuracy matters.

---

## 14. Liu Plot — Ablation Threshold Extraction

The Liu method (J. Liu, *Opt. Lett.* 7(5), 196–198, 1982) extracts ablation threshold fluence and effective spot size from measured ablation crater diameters at varying pulse energies.

### Theory

For a Gaussian beam, the diameter of the ablated region D_ablated relates to pulse energy E by:

```
D_ablated² = 2 · ω₀² · ln(E / E_th)
```

Where E_th is the pulse energy at which fluence at beam center exactly equals the threshold fluence F_th.

### Procedure

1. **Measure** D_ablated at multiple pulse energies (recommended: 5–10 points spanning ~2× to ~10× of estimated E_th).
2. **Plot** D_ablated² (y-axis) vs ln(E) (x-axis).
3. **Linear regression** gives slope and intercept.

### Extraction formulas

```
ω₀ = √(slope / 2)
D_gauss = 2 · ω₀ = √(2 · slope)
E_th = exp(-intercept / slope)
F_th_avg = E_th / (π · ω₀²)
F_th_peak = 2 · F_th_avg
```

### Optimum pulse energy (for cleanest ablation, minimal HAZ)

```
E_opt = (e² / 2) · E_th ≈ 3.69 · E_th
```

This is the energy at which the ablation crater has the steepest sidewall — best for high-resolution patterning and minimum heat-affected zone.

### Pitfalls

- **Always use the same data range** for SLOPE and INTERCEPT regression. Mismatched ranges produce inconsistent E_th and F_th.
- **Span enough energy range** (at least 2× to 10× of E_th) for a clean linear fit.
- **Trail-width measurements** (for line ablation) work in addition to spot-diameter measurements — both follow the same D² ∝ ln(E) relation.
- The method assumes single-pulse ablation. For multi-pulse exposures, ablation incubation effects can shift the apparent threshold downward.

---

## 15. Quick Reference Table

| Quantity | Formula | Typical units |
|---|---|---|
| Pulse energy | `P / PRF` | mJ |
| Spot diameter | `4·M²·λ·F / (π·D_in)` | µm |
| Average fluence | `E / (π·r²)` | J/cm² |
| Peak fluence | `2·F_avg` (M² < 2) | J/cm² |
| Peak power | `E / PW` | kW or MW |
| Peak intensity | `P_peak / (π·r²)` | MW/cm² or GW/cm² |
| Rayleigh range | `π·ω₀² / (M²·λ)` | mm |
| Depth of focus | `2·z_R` | mm |
| ω at offset Δz | `ω₀·√(1+(Δz/z_R)²)` | µm |
| Pace | `v / PRF` | µm |
| Overlap (%) | `(D - Pace) / D` | % |
| Aperture transmission | `1 - exp(-2(A/D)²)` | fraction |
| Liu spot diameter | `√(2·slope)` | µm |
| Liu threshold energy | `exp(-intercept/slope)` | µJ |

---

## 16. Common Process Design Workflow

When designing a new laser process or characterizing an existing one, calculations are typically performed in this order:

1. **Determine target spot size** based on feature size requirements (use eq. 2 to back-calculate F or D_input).
2. **Calculate DoF** (eq. 7) and verify it exceeds workpiece flatness deviations.
3. **Calculate fluence** (eqs. 3–4) and verify it exceeds material ablation threshold (from Liu plot, eq. 14, or literature).
4. **Calculate peak intensity** (eq. 6) and verify regime (photothermal vs. ablation vs. plasma) matches process intent.
5. **Pick scan speed and PRF** to set overlap (eqs. 10–11) appropriate for process type.
6. **Verify accumulated energy** (eq. 13) doesn't exceed desired total dose.
7. **Calculate aperture loss** (eq. 9) if scanner aperture limits beam delivery.
8. **Iterate** — these are coupled, and changing one parameter typically forces re-checks elsewhere.
