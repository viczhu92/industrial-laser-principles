# Optics Care: Contamination, Inspection, and Cleaning

## When to use this file

For the operational side of laser optics — what contamination looks like, how to inspect for it, how to handle optics without making things worse, and how to clean safely. For substrate, coating, and damage-threshold selection, see `laser_optics_selection.md`. For power-meter routines that often catch contamination first, see `measuring-laser-power.md`.

---

## 1. Two Categories of Contamination

Anything sitting on a coating becomes a potential failure point as soon as the laser fires through it. The two regimes that matter in practice:

### Particles
Dust, abrasive debris, glove fibers — anything physically resting on the surface. Under laser flux they:
- divert a small fraction of the beam (rarely measurable photometrically),
- absorb local energy and **bake permanently into the coating** (very measurable in lifetime).

### Films
Thin chemical layers — smoke residue, outgassed organics, condensed lubricant. Under laser flux they:
- cure onto the surface,
- create an absorbing layer the coating wasn't designed for,
- shift the coating's effective reflectivity, dropping fluence at the work surface and dragging the power-meter reading down with it.

### Cleanable vs. damaged

| Where it sits | Outcome |
|---|---|
| **Above** the coating surface | Cleanable |
| **Embedded in or below** the coating | Permanent damage — replace the optic |

Discoloration at the beam-entry location is **suspicious** — it's often the leading indicator of incipient damage — but is not, on its own, a hard scrap signal. Inspect carefully before deciding.

---

## 2. Detecting Contamination

Detection works in three escalating layers:

1. **Performance loss.** A power or fluence drop is the most sensitive symptom. Build a power-meter routine that catches it (see `measuring-laser-power.md`).
2. **Visual inspection.** Catches contamination that hasn't yet shown up at the work surface.
3. **Substitution.** Swap in a known-good optic and re-test — the only way to confirm contamination subtle enough to evade direct inspection.

### Visual inspection technique

Inspection is more art than checklist, but the right setup helps a lot:
- Reflect a ceiling light off the coating at a **45°–85°** angle.
- Position so the **background behind the optic is dark** — defects are invisible against a bright background.
- Scan first for **discontinuities, spots, scratches**.
- Then look at the **beam-entry footprint** specifically — colour shifts there suggest a coating change or a sub-surface defect.
- Curvature of the optic and reflections from the second surface make this much harder than it looks. If possible, practice on optics whose state you already know.

---

## 3. Handling

Habits that prevent contamination in the first place:

- **Mounted optics** can be handled by their mount.
- Make contact only with **non-optical surfaces** — the edge or barrel, never the clear aperture.
- Wear **dust-free, clean gloves**.
- Store in a **clean optical container**. As a fallback, wrap a clean lens tissue around the optic and place it in a foam-lined plastic bag.
- **Particles fall.** When practical, hold the coated surface vertical during handling — airborne dust is less likely to settle on a vertical surface than a horizontal one.

---

## 4. Three Rules Before Cleaning

Cleaning carries real risk: a poorly executed clean does more damage than the contamination it was supposed to remove. The three rules are non-negotiable.

> **Rule 1 — Don't clean optics that aren't dirty.** Every clean is a chance to introduce a scratch.
>
> **Rule 2 — Never use unknown CDA.** Shop compressed dry air carries oil mist and water vapour from the compressor and the line. Use only an optic bulb blower or a canister explicitly labelled "clean air."
>
> **Rule 3 — One stroke, one tissue.** A used tissue is contaminated by definition — never re-use it on an optic.

---

## 5. Cleaning Techniques (Escalate Only as Needed)

Start with the gentlest method that has a chance of working. Escalate only when it's clearly insufficient.

### Level 1 — Air

Dislodge loose particles with an **optic bulb blower** or a clean-air canister.

- Hold canisters **upright**. Tilting them releases liquid propellant onto the optic.
- Never let frozen propellant land on the coating — thermal shock will crack it.

### Level 2 — Drop and Drag

For particles that air won't dislodge, on **flat surfaces**. (Curved surfaces don't work well with this method.)

1. Lay the optic on a clean surface (or hold it stable).
2. Place a single lens tissue across the coating.
3. Apply **1–2 drops** of cleaning solvent and wait for the wetness to spread through the tissue.
4. Drag the tissue across the optic with the **wet edge trailing** — pulling the wet zone away from the optic.

The wet front lifts particles off without the downward pressure that would otherwise grind them across the coating.

### Level 3 — Wipe

For curved surfaces, or when Drop and Drag isn't getting it clean:

1. Fold a lens tissue to roughly the optic's width.
2. Grip near the fold with clean **hemostats or tweezers**, parallel to the fold.
3. Apply **1–3 drops** of solvent on the fold and shake off the excess.
4. Drag slowly across the surface with **light pressure**.
   - As you drag, **rotate the hemostat along the beak axis** — this lifts particles up and away from the surface rather than smearing them across.
5. **One stroke per tissue.** Discard, refold, and start fresh.
6. If multiple passes are needed, **always wipe in the same direction** — never reverse.

### Level 4 — Cleaning swabs

Reserve swabs for **small areas** — micro-lenses, fiber tips, ferrules. Don't use swabs on full-aperture optics; the small contact patch concentrates pressure and almost always leaves a scratch.

### What you must not use

Cleaning supplies designed for **eyewear or imaging optics are not safe for laser optics.** Microfiber cloths shed fibers, consumer "lens cleaner" formulations leave detergent residue, and tissues with binders deposit polymer. Any of those survive at GW/cm² peak intensity and become permanent damage on the next pulse.

---

## 6. Cleaning Solvents

| Solvent | When and why |
|---|---|
| Acetone | Aggressive, flashes off quickly. Verify coating compatibility before use. |
| Methanol | Effective; toxicity is the main concern. |
| Ethyl alcohol | Effective and widely available. |
| **Iso-propanol (IPA)** | **Default choice** — best balance of effectiveness, low toxicity, and disposal cost. |

### Purity, freshness, and humidity

> **A surface can never end up cleaner than the solvent used to clean it.**

- Use **99.99%-purity** solvent (laser- or spectroscopic-grade).
- All four solvents are **hygroscopic** — they absorb water from the air. The water then deposits on the optic when the solvent evaporates.

**Solvent replacement schedule:**

| Container type | Replace solvent |
|---|---|
| Open-top bottle | Daily |
| Spill-prevention dispenser | Every few days |
| Sealed bottle | Weekly |

Follow your local labelling rules for any temporary or transfer container.

---

## 7. Decision Flow

```
Is the optic showing power loss or visible contamination?
├── No   → Don't touch it.
└── Yes  → Visual inspection at 45°–85° with a dark background.
          ├── Subsurface damage / fracture / delamination → Replace.
          ├── Particles only                              → Air → Drop and Drag.
          ├── Film or smoke residue                       → Wipe with IPA.
          └── Discoloration only, no other defect         → Inspect again carefully;
                                                            replace if performance
                                                            doesn't recover after cleaning.
```
