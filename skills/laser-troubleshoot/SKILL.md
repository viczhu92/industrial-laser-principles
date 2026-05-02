---
name: laser-troubleshoot
description: General laser-system troubleshooting walkthrough — orders the diagnostics correctly so alignment isn't blamed for a power, optic, or focus problem. Use when the user says "cut quality dropped", "marks aren't right", "system isn't performing", "what should I check first", or has an open-ended performance complaint.
---

# Laser System Troubleshooting

> Operates under the rules in `../../INSTRUCTIONS.md` (reference-first, reference-only, interactive mode).

## When to use this skill

When system performance has dropped (cut quality degraded, mark contrast lowered, weld depth inadequate, ablation rate down) and the operator doesn't yet know what's at fault. This skill enforces the **correct triage order** so alignment isn't pulled apart unnecessarily for a power or contamination problem.

## References to load at start

- `references/scanner_alignment.md` §11 — primary triage order
- `references/laser_optics_cleaning.md` — Step 2 of the triage
- `references/measuring-laser-power.md` — Step 1 of the triage
- `references/scanner_optimization.md` §1, §6, §7 — Step 3 (focal plane) and laser-output sanity

## The triage order is non-negotiable

Per `scanner_alignment.md` §11:

1. **Power at the laser output**
2. **Optic cleanliness**
3. **Focus-plane parallelism**
4. **Then** alignment checks

> ⚠️ **Don't skip ahead.** Most "alignment" complaints are actually one of Steps 1–3. Fixing them in order is faster than guessing.

## Inputs to gather first

Ask the operator:

1. **What is the symptom — quantitatively?** (e.g., "cut depth dropped from 80 µm to 50 µm at the same recipe", "kerf is wider than yesterday".)
2. **What changed recently?** Laser swap, optic change, recipe update, environment change?
3. **When did it start?** Abrupt or gradual?
4. **Any safety concerns or alarms** that came up?

If the answer to #2 is "we just installed a new laser", the path is **laser-replacement workflow** — go to Step 4 directly with that branch in mind. Otherwise, run the full triage.

→ **Pause:** confirm inputs and triage path before starting Step 1.

---

## Workflow — 4 ordered steps

### Step 1 — Verify laser output power

Per `scanner_alignment.md` §11 + `measuring-laser-power.md`.

**Measure directly at the laser output**, before any downstream optic. This isolates the source from the rest of the system.

Two options:
- Hand off to `laser-power-measurement` for a fully guided 7-step routine.
- Do a quick check inline if the operator has a recent baseline reading.

**Outcome paths:**

| Result | Next |
|---|---|
| Power is in spec | Go to Step 2 |
| Power is low | **Stop the alignment hunt.** Source is the issue — engage laser vendor support, check chiller, fiber, pump diodes (laser-type-specific). |
| Power readings inconsistent | Repeat 3× to rule out warm-up or detector issue, then decide. |

→ **Pause:** confirm Step 1 result before moving on.

### Step 2 — Check every transmissive optic in the beam path

Per `scanner_alignment.md` §11 + `laser_optics_cleaning.md`.

Walk the operator through each optic, in order from source to work surface:

1. Beam expander input window.
2. Beam expander internal optics (if accessible).
3. Beam expander output window.
4. Scanner input window (if any).
5. Galvo mirrors.
6. Focus lens (F-θ or basic).
7. Any protective window above the work surface.

For each: visual inspection at 45°–85° per `laser_optics_cleaning.md` §2.

If contamination is found, hand off to `laser-optics-cleaning` for the cleaning workflow. Return here when complete.

> ⚠️ If power at the laser output (Step 1) was in spec but power at the work surface is low, **the loss is in the optic chain.** Find it before continuing. Don't proceed to Step 3 with a known optic loss unfixed.

→ **Pause:** confirm each optic checked. Confirm any cleaning was done and re-verified. Confirm power at the work surface is now in spec.

### Step 3 — Verify focal plane is parallel to the work surface

Per `scanner_alignment.md` §11 + `scanner_optimization.md` §1.

Quick test:
1. Mark a small pattern at multiple points across the FoV (corners + center).
2. Compare mark width / quality at center vs. edges.
3. Equal quality across FoV → focal plane parallel to work surface.
4. Edge variation that the center doesn't show → **not parallel**.

If not parallel, possible causes:
- Work surface mechanically tilted.
- Z-stage motion axis non-parallel to focus-lens normal.
- Wrong working distance — could be a **beam-expander divergence problem** (per `scanner_alignment.md` §9 diagnostic).

→ **Pause:** confirm Step 3 result before moving to Step 4.

### Step 4 — Now alignment

Only reached if Steps 1–3 all confirm OK.

Per `scanner_alignment.md` §11:

| Situation | Procedure |
|---|---|
| Laser was just swapped | **Laser-replacement procedure** (per §11 — remove BEx and focus lens, align source to scanner aperture / focal plane, then reinstall) |
| First-time installation | **First-time installation procedure** — requires metrology for scanner perpendicularity / centering relative to work surface |
| Drift from working baseline | **Generic alignment iteration** — two-target principle (`scanner_alignment.md` §5) |

> **Reality check** (per `scanner_alignment.md` §11): Most production systems lack the metrology and access for a textbook alignment. If tool-specific work instructions exist, follow those. The triage order above is universal; the alignment procedure beyond is system-specific.

→ **Pause:** confirm operator wants to proceed to alignment, or whether to bring in service / vendor support.

---

## Output

A triage report (markdown):

- Symptom + quantification + when it started
- What changed recently
- **Step 1 (power):** result, action taken
- **Step 2 (optics):** each optic checked, any cleaning done
- **Step 3 (focus):** parallelism verdict
- **Step 4 (alignment):** if reached, what was adjusted
- Where the issue was found
- Final verification (re-measure or re-cut sample)

Save to `outputs/laser-troubleshoot/<YYYY-MM-DD>-<machine>.md`.

---

## Cross-skill links

- Step 1 → `laser-power-measurement`
- Step 2 → `laser-optics-cleaning`
- If a specific defect is observed (corner burn-in, recast, charred edges) instead of a generic performance drop, branch to `laser-defect-diagnose` first.
- If position-specific defects (line starts/ends, corners) → `laser-delay-tuner` directly.
