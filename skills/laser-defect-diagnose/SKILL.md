---
name: laser-defect-diagnose
description: Classify a specific laser-process defect (recast lip, charred edge, incomplete cut, taper, HAZ darkening, etc.) into root cause and corrective action. Use when the user says "I'm seeing X defect", "kerf has Y", "what causes Z", or has a specific defect to classify.
---

# Laser Defect Diagnosis

> Operates under the rules in `../../INSTRUCTIONS.md` (reference-first, reference-only, interactive mode).

## When to use this skill

When the operator has already identified a specific defect on a marked or cut sample and wants to know:

- What's causing it?
- Which parameter to change?
- Whether it's a process problem or an alignment / contamination problem.

This skill is **more specific than `laser-troubleshoot`** — assume general triage has been done, or skip it if the defect points clearly at a process cause.

## References to load at start

- `references/laser_ablation.md` — HAZ, plume, threshold, multi-pulse, recipe (§4, §10–§12)
- `references/laser_dicing.md` — cutting-specific defects, polarization, dissimilar materials
- `references/laser_welding.md` — mode collapse, weld defects
- `references/scanner_optimization.md` — scan-delay-related defects (cross-reference)

## Inputs to gather first

Ask the operator:

1. **Process type** — ablation / dicing / cutting / welding?
2. **Material** + thickness if relevant.
3. **Visible defect** — describe in plain words. Photo helpful.
4. **Where on the feature** — start of line, end, corner, edge, throughout?
5. **Current parameters** — power, PRF, pulse width, scan speed, hatch, repeats, polarization.
6. **What changed** — same recipe used to work, or new recipe?

→ **Pause:** confirm inputs.

---

## Workflow

### Step 1 — Localize the defect

The same word ("burn", "rough edge", "incomplete") can mean very different things. Resolve ambiguity first.

Match against this triage:

| Defect location | Likely category | Branch |
|---|---|---|
| **Position-specific** — at line start / line end / specific corner | **Scan delay** | Hand to `laser-delay-tuner` |
| **Distributed across the cut / mark** | **Process parameter** | Continue to Step 2 |
| **Edge or wall only** | **Polarization, wall-angle, or material-class issue** (dicing) | Continue to Step 2 (dicing branch) |
| **Surface marks away from cut, or beam-path issue** | **Contamination or stray reflection** | Hand to `laser-troubleshoot` |
| **Random / intermittent** | **Drift or alignment** | Hand to `laser-troubleshoot` |

→ **Pause:** confirm classification before continuing.

### Step 2 — Process-specific defect mapping

Branch by process. **Cite the reference for every fix proposed.**

#### Ablation defects

Per `laser_ablation.md` §4, §10, §11, §12.

| Defect | Likely root cause | Fix |
|---|---|---|
| **Excessive HAZ around the mark** | Fluence too far above threshold (`§4`) | Lower power or increase scan speed |
| **Mark width grows but depth doesn't** | Saturation — past optimum fluence (`§4`) | Lower power |
| **Inconsistent depth along a single line** | Plume shielding (`§10`) | Cross-flow gas; or vacuum/inert atmosphere |
| **No mark at all** | Below ablation threshold (`§4`) | Increase fluence — more power, slower speed, or smaller spot |
| **Mark fades after first pass** | Heat-tolerant process needing more passes (`§9`) | Add repeats |
| **Diminishing returns from added passes** | Strong thermal accumulation (`§12`) | Add a Pause between passes, or lower per-pass power |
| **Recast / re-deposited debris in kerf** | Plume not clearing (`§10`) | Cross-flow gas; lower repeat rate; vacuum |
| **Wider HAZ than expected for cold ablation** | Pushed beyond cold-ablation regime into "warm" ablation (`§7`) | Drop fluence closer to threshold — lower power, longer process time |

#### Dicing / cutting defects

Per `laser_dicing.md` §3–§6.

| Defect | Likely root cause | Fix |
|---|---|---|
| **Cut won't go all the way through** | Wall-angle / depth limit reached (`§3`) | Add parallel passes (depth² scaling); or change focal-spot width |
| **Different quality in X vs Y** | Linear polarization with asymmetric coupling (`§4`) | Switch to circular polarization |
| **Charred epoxy on PCB cut** | Heat too high for the matrix (`§6`) | Increase scan speed; add cooling gas |
| **Glass fiber not fully cut** | Pulse energy insufficient for fiber (`§6`) | Increase pulse energy; or change wavelength |
| **Through-cut into substrate on blind via** | Pulse parameters wrong for shock-delamination regime (`§6`) | Adjust pulse width and PRF for delamination; reduce per-pulse energy |
| **Recast on Si dicing edge** | Ablative path on transparent material (`§2`) | Switch to stealth dicing if material allows |
| **Tapered kerf walls** | Wall-angle approaching the geometric limit (`§3`) | Widen entry with parallel passes; or use larger focal spot |

#### Welding defects

Per `laser_welding.md`.

| Defect | Likely root cause | Fix |
|---|---|---|
| **Weld much shallower than expected** | Peak intensity dropped below keyhole threshold (`§4`) | Increase power; decrease spot; or shorten pulse to raise peak |
| **Spatter, porosity, or humping** | Operating in keyhole near the collapse boundary (`§4`) | Stabilize keyhole — adjust intensity, add shield gas, slow scan slightly |
| **Wide shallow nugget when keyhole was intended** | In conduction or transition mode unintentionally (`§2`–§3) | Increase peak intensity to clear ~1.5 MW/cm² (`§4`) |
| **Weld appearance OK but no bond** | Insufficient energy coupling | Check material absorption at wavelength; check surface state |

→ **Pause:** ask which row matches. Confirm before proposing the fix.

### Step 3 — Validate the proposed fix is reachable

Before changing the recipe:

- **Compute the new peak intensity / fluence** (per `laser_process_calculations.md`).
- **Check it stays within optic damage thresholds** (per `laser_optics_selection.md` §5 — apply the 2×–10× safety factor).
- **Confirm the laser, scanner, and stage envelope can deliver** the new parameters (PRF range, max power, scan-speed limit).

If any of these fails, **the proposed fix is not feasible**. Either:
- Find an alternative parameter knob.
- Recommend a hardware change (different optic, different focus lens, beam expander adjustment).
- Stop and report the constraint.

→ **Pause:** present the proposed change + validation. Wait for go.

### Step 4 — Test and report

Operator runs a test sample with the proposed change. Compare to baseline.

- Defect resolved → done.
- Defect partially resolved → loop back to Step 2 with updated symptom.
- Defect unchanged → re-classify; the original root-cause hypothesis was wrong.

→ **Pause:** loop until clean.

---

## Output

A defect-diagnosis record (markdown):

- Defect description (with photo if provided)
- Process type, material, parameters
- Localization verdict (Step 1)
- Root cause identified (Step 2) **with reference citation**
- Proposed fix + feasibility check (Step 3)
- Test result (Step 4)
- Final recipe delta

Save to `outputs/laser-defect-diagnose/<YYYY-MM-DD>-<defect-id>.md`.

---

## Cross-skill links

- Position-specific corner / line-end defects → `laser-delay-tuner`
- General performance drop without a clear defect → `laser-troubleshoot`
- Optic damage suspected → `laser-optics-cleaning` (for inspection)
- Recipe rebuild needed → `laser-doe-ablation` or `laser-doe-dicing`
