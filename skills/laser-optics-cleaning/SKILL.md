---
name: laser-optics-cleaning
description: Guide an operator through the diagnostic and cleaning of a laser optic, gated at each decision and each cleaning level. Use when the user says "clean a lens", "clean an optic", "lens contamination", "F-theta got dirty", or otherwise asks for guided cleaning.
---

# Laser Optics Cleaning

> Operates under the rules in `../../INSTRUCTIONS.md` (reference-first, reference-only, interactive mode).

## When to use this skill

When an operator suspects optic contamination (power loss, visible mark on the surface, or routine inspection finding) and is preparing to clean. This skill enforces the **"don't clean it if it's not dirty"** rule, walks through diagnostic inspection first, and only then escalates through the cleaning levels — always pausing for confirmation.

## References to load at start

- `references/laser_optics_cleaning.md` — primary
- `references/laser_optics_selection.md` — for damage-vs-cleanable judgment

## The three hard rules — apply throughout

Per `laser_optics_cleaning.md` §4:

> **Rule 1 — Don't clean optics that aren't dirty.** Every clean is a chance to introduce a scratch.
>
> **Rule 2 — Never use unknown CDA.** Use only an optic bulb blower or a canister labeled "clean air."
>
> **Rule 3 — One stroke, one tissue.** Never re-use a tissue on an optic.

The skill must enforce these at the relevant gates.

## Inputs to gather first

Ask the operator:

1. **Which optic** is suspected (focus lens, beam expander lens, F-θ, mirror, ...)?
2. **Why is it suspected** — power loss, visual indication, scheduled inspection?
3. **Mounted or unmounted** — is it accessible without breaking alignment?
4. **PPE / cleanroom level** in place.
5. **Available cleaning supplies** —
   - IPA grade (must be 99.99%-pure / laser- or spectroscopic-grade per `laser_optics_cleaning.md` §6)
   - When was the IPA bottle last replaced? (Open: today / Spill-prevention: last few days / Sealed: last week — per §6)
   - Lens tissues (clean, new pack)
   - Hemostats or tweezers
   - Optic bulb blower or canister labeled "clean air"

> ⚠️ **The laser must be off, mechanically blocked, and the key removed** before any optic is touched. Confirm explicitly.

→ **Pause:** confirm all inputs received and laser is safed. Then proceed.

---

## Workflow

### Step 1 — Diagnostic inspection FIRST (Rule 1)

Per `laser_optics_cleaning.md` §2.

Before touching anything, do a visual inspection:
- Reflect a ceiling light off the coating at a **45°–85°** angle.
- Position so the **background behind the optic is dark**.
- Look for:
  1. Discontinuities, spots, scratches.
  2. Color changes at the **beam-entry footprint** (suggests coating change or sub-surface damage).

**Three possible verdicts:**

| Verdict | Action |
|---|---|
| **Looks clean** | **STOP. Don't clean.** Re-measure power; if still down, look elsewhere (`laser-troubleshoot`). |
| **Particles or film visible** | Contamination. Proceed to Step 2. |
| **Sub-surface damage / fracture / delamination** | **STOP. Replace the optic.** Cleaning won't help. |

> Discoloration with no other defect is **suspicious but not definitive** — try cleaning, but be ready to replace if performance doesn't recover (per `laser_optics_cleaning.md` §1).

→ **Pause:** ask the operator which verdict applies. Branch accordingly.

### Step 2 — Classify contamination type

Per `laser_optics_cleaning.md` §1.

| Contamination | Cleaning levels |
|---|---|
| **Particles only** (dust, debris) | Levels 1–2: Air → Drop and Drag |
| **Film / smoke residue** | Level 3: Wipe |
| **Mixed** | Start at lowest level that addresses both, escalate as needed |

→ **Pause:** confirm contamination type. Confirm cleaning supplies are present and ready.

### Step 3 — Solvent freshness check (Rule 2 + §6 of cleaning ref)

> **A surface can never end up cleaner than the solvent used to clean it.** (per `laser_optics_cleaning.md` §6)

Confirm:
- IPA is **99.99%-pure** (laser- or spectroscopic-grade).
- IPA bottle is **fresh enough**:
  - Open-top bottle → must be replaced **today**.
  - Spill-prevention dispenser → within last **few days**.
  - Sealed bottle → within last **week**.

→ **Pause:** if solvent is older than the threshold for its container type, **stop** and request fresh solvent before cleaning.

### Step 4 — Cleaning, escalating only as needed

Start with the gentlest method that has a chance of working.

#### Level 1 — Air

Per `laser_optics_cleaning.md` §5 Level 1.

Bulb blower or clean-air canister, **upright**.

> ⚠️ **Never tilt the canister** — tilting releases liquid propellant onto the optic.
> ⚠️ **Never let frozen propellant land on the coating** — thermal shock cracks coatings.

→ **Pause:** confirm Level 1 done. Did it resolve? If yes → Step 5. If no → Level 2.

#### Level 2 — Drop and Drag (flat surfaces only)

Per `laser_optics_cleaning.md` §5 Level 2.

For particles air can't dislodge, on flat surfaces. (Curved surfaces don't work well.)

1. Place optic on a clean surface, or hold it stable.
2. Lay a single lens tissue across the coating.
3. Apply **1–2 drops** of IPA, let it spread through the tissue.
4. Drag the tissue with the **wet edge trailing** away from the optic.

The wet front lifts particles without the downward pressure that would otherwise grind them across the coating.

→ **Pause:** confirm Level 2 done. Resolved? If yes → Step 5. If no → Level 3.

#### Level 3 — Wipe (curved surfaces or stuck contamination)

Per `laser_optics_cleaning.md` §5 Level 3.

1. Fold a lens tissue to roughly the optic's width.
2. Grip near the fold with clean hemostats or tweezers, **parallel to the fold**.
3. Apply **1–3 drops** of IPA on the fold, shake off the excess.
4. Drag slowly across the surface with **light pressure**.
5. **As you drag, rotate the hemostat along the beak axis** — this lifts particles up off the surface rather than smearing them across.
6. **One stroke per tissue.** Discard, refold, start fresh. (Rule 3.)
7. For multiple passes: **always wipe in the same direction.** Never reverse.

→ **Pause:** confirm Level 3 done. Resolved? If yes → Step 5. If no, evaluate:
- Small-aperture optic (micro-lens, fiber tip)? → Level 4.
- Full-aperture optic? → consider replacement.

#### Level 4 — Cleaning swabs (small areas only)

Per `laser_optics_cleaning.md` §5 Level 4.

Only for **micro-lenses, fiber tips, ferrules**. Small contact patch concentrates pressure — **never use on full-aperture optics.**

→ **Pause:** confirm.

#### What you must NOT use

Per `laser_optics_cleaning.md` §5 — "What you must not use":

- **Eyewear or imaging-optics cleaning supplies** — leave residues that survive at GW/cm² peak intensity.
- **Microfiber cloths** — shed fibers.
- **Consumer "lens cleaner" formulations** — contain detergent residue or polymer binders.

If the operator only has these available, **stop the cleaning procedure** and source proper supplies.

### Step 5 — Verify

Per `laser_optics_cleaning.md` §2 + §7 (Decision Flow).

Repeat the inspection at 45°–85° in a dark background.

- Clean? → re-measure power if power loss was the original symptom. Compare to baseline.
- Still contaminated? → escalate one level, or scrap if approaching the swab/replace boundary.

→ **Pause:** report final verdict. Done.

---

## Output

A cleaning record (markdown):

- Optic ID + position in the system
- Inspection verdict (Step 1)
- Contamination classification (Step 2)
- Solvent freshness confirmed (Step 3)
- Levels attempted: each one's result
- Final inspection result (Step 5)
- Power baseline comparison (if applicable)
- Operator notes

Save to `outputs/laser-optics-cleaning/<YYYY-MM-DD>-<optic-id>.md`.

---

## Cross-skill links

- If contamination is found and the operator wants to verify the impact: hand to `laser-power-measurement` for a before/after reading.
- If contamination is suspected but inspection looks clean: hand to `laser-troubleshoot` — the issue may be elsewhere.
- If a sub-surface defect is found and replacement is required: refer to `laser_optics_selection.md` for spec verification of the replacement.
