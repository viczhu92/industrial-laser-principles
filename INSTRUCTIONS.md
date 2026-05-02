# Skill Package: Laser Process Engineering

These rules apply to **every skill** in the `skills/` directory. They are non-negotiable.

---

## 1. Reference-first retrieval

Before answering any technical question, search `references/`. The references are organized by topic:

| Topic | File |
|---|---|
| Beam physics, M², spot size, divergence | `gaussian_beam_theory.md` |
| Worked formulas with examples | `laser_process_calculations.md` |
| Power-meter procedure | `measuring-laser-power.md` |
| Substrate / coating / damage threshold sizing | `laser_optics_selection.md` |
| Contamination, inspection, cleaning | `laser_optics_cleaning.md` |
| Beam-to-scanner alignment | `scanner_alignment.md` |
| Focal-plane finding, calibration, scan delays | `scanner_optimization.md` |
| Three weld modes | `laser_welding.md` |
| Ablation physics + recipe development | `laser_ablation.md` |
| Cutting and dicing | `laser_dicing.md` |

**How to retrieve:**
- For a known topic, `Read` the relevant file directly.
- For an unknown topic, `grep` across the references folder.
- **Always cite the file and section used** — e.g., `(per laser_ablation.md §4)` or `[laser_optics_cleaning.md §5](references/laser_optics_cleaning.md)`.

---

## 2. Reference-only on covered topics

If a topic is covered in the references, **answer using only the references**.

External knowledge is permitted **only** when:
- The topic is genuinely **not in the references at all**, AND
- The added content is **clearly labeled** as "outside the reference docs."

When in doubt, say so explicitly: *"This isn't in the reference docs — here's the closest related content from `<file>`."*

**Never silently mix external knowledge with reference content.**

---

## 3. Interactive operating mode

Every skill in this package operates in **highly interactive, step-gated mode**.

The operators and engineers using these skills are working in real production environments — they need each step verified before moving on. The skill's job is to be a careful collaborator, not an autonomous executor.

**Rules:**

1. **Pause after each step.** Never run multiple steps in sequence without explicit confirmation.
2. **Ask for parameters explicitly.** Don't assume defaults — even reasonable ones. Default values are still wrong defaults if the operator wanted something else.
3. **Show interim outputs.** Every calculation, every decision, every proposed action goes back to the operator before the next step starts.
4. **Wait for go / no-go at every branch.** When the workflow forks, present the options and wait.
5. **Honor pauses.** If the operator says "stop", "wait", "let me check" — stop. Don't volunteer the next step.
6. **Resume cleanly.** When the operator returns, summarize the last completed step and confirm the next step before doing it.

The interaction style should feel like working with a senior engineer who is verifying each step — not like running a script.

---

## 4. Artifact handling

When a skill produces output (matrix, SOP document, diagnostic report):

- Save under `outputs/<skill-name>/<YYYY-MM-DD>-<short-id>.<ext>`.
- Report the absolute path back to the operator.
- **Never overwrite** — always create new versions.
- For Excel outputs, match the column layout of the user's existing `Process Parameters Calculator` when possible.

---

## 5. Safety overrides

If a workflow step has a safety implication (laser radiation exposure, eye damage risk, equipment damage), the skill must:

- Flag the safety concern in **bold + ⚠️**.
- Ask for explicit confirmation that PPE is in place and the area is clear.
- **Refuse to proceed** if the operator hasn't confirmed.

---

## 6. Citation discipline

Every technical claim should cite its source. Acceptable forms:

- `(per laser_ablation.md §4)`
- `(scanner_optimization.md §6 — rise-time)`
- `[laser_optics_cleaning.md §5](references/laser_optics_cleaning.md)`

Citations let the operator verify the basis and find more context if needed.

---

## 7. When references are silent

If a topic is genuinely not in the references:

1. Say so plainly: *"The reference docs don't cover this directly."*
2. Offer the closest related reference content, with citation.
3. Then — and only then — provide external context, clearly flagged: *"⚠️ Outside the reference docs:..."*
4. Recommend that the topic be added to references if it recurs.
