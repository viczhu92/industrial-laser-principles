---
name: laser-doe-ablation
description: Build a 3-step ablation-recipe DOE (surface threshold → depth line matrix → volume hatched / multi-pass) with the operator, gated at each step. Use when the user says "DOE for ablation", "ablation recipe", "I need to mark/scribe/drill X material", "set up a marking parameter sweep", or otherwise wants to develop an ablation recipe.
---

# Laser Ablation DOE

> Operates under the rules in `../../INSTRUCTIONS.md` (reference-first, reference-only, interactive mode).

## When to use this skill

When the operator needs to develop a new ablation recipe — for a new material, new wavelength, or new geometric target. This skill enforces the **surface → depth → volume** progression from `laser_ablation.md` §12. Each stage has a defined experiment, and each experiment pauses for the operator to run it and report results before the next stage begins.

## What this skill is NOT

- Not for cutting all the way through (use `laser-doe-dicing`).
- Not for joining (welding skill not built — yet).
- Not for diagnosing an existing recipe gone wrong (use `laser-defect-diagnose`).

## References to load at start

- `references/laser_ablation.md` §4 (threshold), §9 (multi-pulse), §12 (workflow) — primary
- `references/laser_process_calculations.md` — fluence, peak intensity, focal spot
- `references/gaussian_beam_theory.md` — M², spot size derivation
- `references/laser_optics_selection.md` §5 — damage-threshold sanity check on chosen fluence

## Inputs to gather first

Ask the operator:

1. **Material** — composition, surface state.
2. **Goal** — surface mark / shallow scribe / depth groove / drilled hole / area cleaning?
3. **Tolerance constraints** — kerf width, depth target, HAZ tolerance, throughput target.
4. **Available laser** — wavelength, max power, PRF range, pulse-width range, M².
5. **Optical chain** — focus-lens focal length, beam expander mag, focal-spot diameter (or input beam diameter so we can compute it via `laser_process_calculations.md`).
6. **Throughput requirement** — parts per hour or scan-speed target.

**Compute and show derived values to the operator:**
- Focal-spot diameter (from `gaussian_beam_theory.md` formula).
- Maximum single-pulse fluence at full power.
- Average fluence at mid-PRF.
- Whether any of these exceeds optic damage thresholds (per `laser_optics_selection.md` §5).

→ **Pause:** confirm all inputs and derived values. Address any damage-threshold flags before proceeding.

---

## Workflow — 3 gated stages

### Stage 1 — SURFACE: single-shot threshold

Per `laser_ablation.md` §12 Step 1.

#### What to do

1. Set parameters for **non-overlapping single shots**:
   - **Low PRF** (e.g., 1 kHz).
   - **High scan speed** so pulse-to-pulse spacing >> focal-spot diameter (e.g., 100 mm/s).
   - This keeps rise-time tail effects (`scanner_optimization.md` §6) out of the threshold reading.
2. Run a **fluence sweep** — typically 5–7 shots at logarithmically-spaced energies, bracketing the literature/estimated threshold.
3. Inspect the resulting craters under microscopy.

#### What the skill computes

- Required pulse-spacing for true non-overlap.
- Suggested fluence sweep range:
  - From any literature value the operator has (cite source explicitly — note that **literature values are outside the reference docs** and must be flagged as such).
  - From general material-class anchors when literature isn't available.
- Test-pattern parameter list (PRF, speed, pulse energies for each shot).

#### After running — Liu plot threshold extraction

Per `laser_ablation.md` §12:

- Operator measures **crater diameter** at each above-threshold fluence.
- Compute **(crater diameter)² vs. log(fluence)**.
- Linear extrapolation crosses the x-axis at the **ablation threshold fluence**.
- Cross-check against any literature value.

The Liu plot can be built in the user's existing `Process Parameters Calculator` Liu Plot sheet, or computed by hand here.

→ **Pause:** confirm threshold value. Sanity-check against literature if available. Confirm to proceed to Stage 2.

### Stage 2 — DEPTH: single line, log-spaced matrix

Per `laser_ablation.md` §12 Step 2.

#### What to do

1. Use the Stage 1 threshold as the lower-bound fluence anchor.
2. Build a **Power × Scan Speed log-spaced matrix.**
3. Mark the matrix as a grid of **single lines** on the same coupon.

#### Log-spaced series

> Per `laser_ablation.md` §12 — use logarithmic spacing because the eye easily distinguishes 0.5 m/s from 1 m/s, but cannot reliably distinguish 4.5 m/s from 5 m/s.

The **1.6× series**:
```
0.1, 0.16, 0.26, 0.41, 0.65, 1, 1.6, 2.6, 4.1, 6.5, 10, ...
```

- **Power axis:** span ~ 1× to ~ 5× threshold fluence (typically 4–6 levels).
- **Scan-speed axis:** span useful range (typically 4–6 levels).

#### What the skill computes per cell

- Fluence (J/cm²).
- Pulse-to-pulse pitch in µm.
- Multiple of ablation threshold.
- **Optic damage check** — flag any cell that exceeds the lens damage-threshold limit (with `laser_optics_selection.md` §5 + 2–10× safety factor).

#### Output

Generate the matrix as:
- **CSV** for now (simple, clean).
- Or markdown table for quick review.
- Excel output via shared library when `lib/ppc_writer.py` is built — eventually matching the `Process Parameters Calculator` column layout.

→ **Pause:** review the matrix before committing. Operator can edit cells, drop ones flagged as out-of-envelope, or expand the range.

#### After running

Operator inspects each line for cut quality, kerf, HAZ.

→ **Pause:** ask the operator to identify the **best-quality cell at the highest scan speed** that meets the requirements. That cell becomes the **unit recipe** for Stage 3.

### Stage 3 — VOLUME: hatched area / multi-pass

Per `laser_ablation.md` §12 Step 3.

#### What to do

1. Take the unit recipe from Stage 2.
2. Apply across an area by **stacking parallel lines at hatch distance** (typically 0.5× to 1× spot diameter — same overlap math as `laser_ablation.md` §9).
3. For depth targets exceeding what one sweep clears, **stack passes**: 2× / 4× / 8× repeats.

#### What the skill computes

- Hatch overlap factor at the chosen hatch distance.
- Estimated depth per pass (calibrated from Stage 2 line cross-section).
- Estimated cycle time per area for each repeat count.

#### After running — the heat-accumulation diagnostic

Per `laser_ablation.md` §12 — Diagnostic.

Plot **achieved depth vs. (number of repeats × inverse scan speed)**:

| Relationship | Meaning | Action |
|---|---|---|
| **Linear** | Heat-tolerant process — doubling repeats halves speed-to-target | Use the highest-throughput cell. **Done.** |
| **Non-linear** (diminishing returns) | Strong thermal accumulation | One of: **add Pause between passes** (test 0.5 s, 1 s, 2 s); or **lower per-pass power** (drop one cell on the matrix). |

→ **Pause:** operator reports which case it is. Loop with adjustment, or finalize.

---

## Final output

The skill produces:

1. **DOE matrix file** — Stages 1, 2, 3 each as a sheet (CSV with stage labels for now; xlsx when ppc_writer is available).
2. **Recipe summary** (markdown) — final selected cell with all derived parameters, threshold value, validation samples, reference citations.
3. **Reference index** — which reference section drove each decision.

Save to `outputs/laser-doe-ablation/<YYYY-MM-DD>-<material>/`.

---

## Cross-skill links

- If a defect appears in Stage 2 or 3 that the matrix can't explain → `laser-defect-diagnose`.
- If power readings drift during the experiment → `laser-power-measurement` (sanity check).
- If an optic damage check fires in Stage 2 → stop and warn (a `laser-damage-sizer` skill is planned but not built; for now, hand back to the operator with the warning).
- If position-specific defects appear (corner burn-in, line-end short) → `laser-delay-tuner`.
