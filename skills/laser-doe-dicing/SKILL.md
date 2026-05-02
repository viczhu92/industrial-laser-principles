---
name: laser-doe-dicing
description: Build a dicing/cutting recipe — start with stealth-vs-ablative-vs-fusion decision, then geometric depth feasibility, polarization choice, and multi-pass parameter matrix. Use when the user says "DOE for dicing", "wafer dicing recipe", "PCB cutting recipe", "set up cutting parameter sweep", or "I need to cut/dice X".
---

# Laser Dicing / Cutting DOE

> Operates under the rules in `../../INSTRUCTIONS.md` (reference-first, reference-only, interactive mode).

## When to use this skill

When developing a recipe for **separating** material — full-thickness cutting, wafer dicing, PCB routing, or stealth dicing. The decisions here are different from ablation (surface removal): there's a path-selection step at the top, a geometric feasibility limit, polarization considerations, and dissimilar-material trade-offs.

## What this skill is NOT

- Not for surface marking / shallow scribing (use `laser-doe-ablation`).
- Not for diagnosing an existing recipe gone wrong (use `laser-defect-diagnose`).

## References to load at start

- `references/laser_dicing.md` — primary, full document
- `references/laser_ablation.md` — for the ablative-cutting branch (overlap, thermal accumulation)
- `references/laser_process_calculations.md` — fluence, peak intensity
- `references/gaussian_beam_theory.md` — M², spot size, depth of focus
- `references/laser_optics_selection.md` §5 — damage threshold check on chosen fluence

## Inputs to gather first

Ask the operator:

1. **Material** + **thickness**.
2. **Through-cut, or partial-cut + cleave?** (Dicing-style is partial + cleave — `laser_dicing.md` §1.)
3. **Is the material transparent at the operating wavelength?** (Critical for stealth-dicing decision.)
4. **Edge-quality requirements** — chip-out tolerance, wall-angle requirement, recast tolerance.
5. **Throughput target.**
6. **Available laser** — wavelength, max power, pulse-width regime (UFL? ns? CW?), polarization (linear / circular / unpolarized).
7. **Optics + scanner** — focal-spot diameter, beam expander, working distance.
8. **Heterogeneous stack?** (e.g., PCB with epoxy + glass fiber + copper.)

→ **Pause:** confirm inputs.

---

## Workflow — staged decisions

### Stage 0 — DECISION: which cutting path?

Per `laser_dicing.md` §1–§2.

| Path | When to use |
|---|---|
| **Stealth dicing** | Material is transparent at λ; brittle (Si at appropriate λ, sapphire, glass); partial-cut + cleave acceptable |
| **Ablative cutting (UFL or ns)** | Standard opaque material; micrometer-level accuracy needed |
| **Fusion cutting** | Thick metal; high-power CW available; sub-mm tolerance acceptable |

→ **Pause:** present the three with rationales. Confirm the path. Branch:
- **Stealth** → jump to **Stage 4-S**.
- **Ablative or Fusion** → continue to **Stage 1**.

### Stage 1 — Geometric feasibility check (ablative / fusion path)

Per `laser_dicing.md` §3.

The wall-angle limit is a right-triangle problem:

```
max_single_column_depth ≈ focal_spot_diameter / tan(min_wall_angle)
```

Where `min_wall_angle` is the steepest slope at which the wall still couples enough laser energy to ablate.

#### Compute and report

- The triangle's height for the operator's focal-spot diameter at typical wall angles.
- A typical focused beam reaches **~ 200 µm in average materials** (per `laser_dicing.md` §3 — engineer's intuition).
- **If material thickness exceeds that limit:**
  - Single-column cut **will not get through.**
  - Plan a **multi-pass parallel widening** strategy.
  - **Number of passes scales with depth².** Doubling cut depth quadruples cut time.

→ **Pause:** present the geometric feasibility report. If multi-pass is needed, confirm the depth-to-passes estimate is acceptable to the throughput budget. If not, recommend a different focal-spot configuration (smaller focus + more passes vs. larger focus + fewer but wider passes).

### Stage 2 — Polarization decision

Per `laser_dicing.md` §4.

| Situation | Polarization |
|---|---|
| **First-pass-only on flat surface** | Linear is OK |
| **Multi-pass with formed walls** | **Circular polarization** strongly recommended — X and Y cuts then behave identically |

If the operator's laser outputs linear polarization and circular is needed, recommend inserting a quarter-wave plate.

→ **Pause:** confirm polarization configuration. Verify hardware can deliver it.

### Stage 3 — Material-class warnings

Per `laser_dicing.md` §5–§6.

Check the operator's material against known problem classes:

| Material class | Specific warnings |
|---|---|
| **Glass / Si at melt** | Self-healing reflective surface; **UV or mid-IR strongly preferred** |
| **Plastics / polymers** | Molten material reflows back into kerf; **UFL strongly preferred** |
| **PCB stack (epoxy + fiber)** | Recipe compromise: **high speed + cooling gas** for epoxy, **high pulse energy + correct λ** for fiber |
| **Metal-on-plastic stack (blind via)** | Shock-delamination regime — pulse-width and PRF tuning is critical |
| **Self-funneling cuts** | Some configurations form waveguide-like walls — high aspect ratio possible (`§5`) |

→ **Pause:** flag any applicable warnings. Operator confirms they understand and how they'll address them.

### Stage 4-A — Multi-pass parameter matrix (ablative)

For ablative cutting:

#### Build the matrix

Three axes:

- **Pass count:** 1, 2, 4, 8, 16 (logarithmic).
- **Power:** log-spaced 4–6 levels (1.6× steps from `laser_ablation.md` §12).
- **Scan speed:** log-spaced 4–6 levels.

Total cells: typically 5 × 5 × 3 = 75 if all three are explored. **Pin one variable** (usually pass-count) to a reasonable starting estimate from Stage 1's geometric calculation, to keep the matrix tractable.

#### What the skill computes per cell

- Fluence (J/cm²).
- Multiple of ablation threshold (if known from a prior `laser-doe-ablation` run on the same material).
- Pulse-to-pulse pitch.
- Estimated cycle time per cut.
- **Optic damage check** (`laser_optics_selection.md` §5).

→ **Pause:** review the matrix. Operator can edit, drop flagged cells, or restart.

#### After running

Operator inspects each cell for:
- Did it cut through?
- Wall quality (taper, recast).
- HAZ at edges.
- Re-deposited material.

→ **Pause:** identify the best cell (cut-through + clean walls + acceptable cycle time). Confirm.

### Stage 4-S — Stealth dicing parameter sweep

Per `laser_dicing.md` §2.

Goal: **internal modification only, no surface ablation.**

#### Build the matrix

Three axes:

- **Focal Z (in-bulk depth):** 4–5 levels stepping into the bulk.
- **Pulse energy:** 4–5 log-spaced levels.
- **Pulse spacing:** 3 levels (close, medium, sparse) — defines modification line continuity.

#### Critical constraint

- Pulse energy must be **above the in-bulk modification threshold** (non-linear absorption regime).
- Pulse energy must be **below the surface-ablation threshold** at the entry surface.
- The skill computes both thresholds and flags cells outside this window.

→ **Pause:** review. Operator commits.

#### After running

Cleave the wafer along the modification line. Inspect:
- Did it cleave cleanly?
- Edge quality.
- **Surface damage on the entry side** (must be none — that's the entire point of stealth).

→ **Pause:** identify the best cell.

### Stage 5 — Validate at production scan speed

The matrix was tuned at characterization speed; production speed may differ.

Run the chosen recipe at **production scan speed** on a real coupon. Iterate if needed.

→ **Pause:** confirm production run is acceptable.

---

## Final output

1. **Decision log** (markdown) — path-choice rationale, polarization choice, geometric pass count, material warnings.
2. **DOE matrix** (CSV / xlsx).
3. **Final recipe summary** (markdown) with reference citations for every decision.

Save to `outputs/laser-doe-dicing/<YYYY-MM-DD>-<material>/`.

---

## Cross-skill links

- Position-specific defects (corners, line ends) during validation → `laser-delay-tuner`.
- Cell can't cut through but the geometry math says it should → re-check Stage 1, or hand to `laser-troubleshoot`.
- Power drifts during the experiment → `laser-power-measurement`.
- General defect classification mid-run → `laser-defect-diagnose`.
