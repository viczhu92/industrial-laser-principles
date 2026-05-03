---
name: laser-power-measurement
description: Walk an operator through a laser-power measurement, gated step-by-step. Use when the user says "measure laser power", "power meter routine", "verify laser output", or asks for guided supervision of a power measurement.
---

# Laser Power Measurement

> Operates under the rules in `../../INSTRUCTIONS.md` (reference-first, reference-only, interactive mode).

## When to use this skill

When an operator or engineer needs to make a laser-power measurement — for incoming inspection, after a laser swap, as part of routine maintenance, or to validate a recipe. This skill walks the **7-step procedure** from `measuring-laser-power.md` with a pause for confirmation at each step.

## References to load at start

- `references/measuring-laser-power.md` — primary
- `references/laser_process_calculations.md` — for any spot-size or fluence sanity checks during configuration

## Inputs to gather BEFORE Step 1

Ask the operator, one at a time or in a single block:

1. **Laser model and nominal output power** (e.g., "an industrial 200W ns fiber laser, set to 100W").
2. **Wavelength** (1064 nm? 532 nm? UV?). Required for the wavelength correction step.
3. **Detector model** in use, and whether **anticipation** is enabled.
4. **Where in the beam path** the measurement is being made (after focus lens? Before scanner? At laser output?).
5. **PPE in place** — laser-safety glasses for the wavelength, beam tube, beam stop.

> ⚠️ **Do not proceed past this point until PPE confirmation is received.**
> ⚠️ The eye's blink reflex provides no protection at IR wavelengths — confirm explicitly.

→ **Pause:** confirm all inputs received, then proceed to Step 1.

---

## Workflow — 7 gated steps

Per `measuring-laser-power.md`. Run in order. **Pause after each step.** Confirm completion (or surface anomaly) before moving on.

### Step 1 — Warm-up

Per `measuring-laser-power.md` Step 1.

Ask the operator to fire the laser and let it stabilize:
- **5 minutes** for ns and CW fiber lasers
- **10–20 minutes** for ps lasers

Reason: optical components shift while the laser reaches thermal equilibrium with its environment.

→ **Pause:** "Has the laser been on for the warm-up time? Ready to proceed?"

### Step 2 — Verify detector specs match laser

Per `measuring-laser-power.md` Step 2.

Walk through each spec check:
- Average power within detector range?
- Power density within range?
- Pulse energy within range (for pulsed lasers)?
- Energy density within range?
- PRF within range?

→ **Pause:** confirm each is in spec. **Stop the procedure** if any are out of spec — request a different detector before going on.

### Step 3 — Beam size on detector

Per `measuring-laser-power.md` Step 3.

Target: **40%–60% of the optical aperture.**

Ask the operator:
- What is the detector aperture diameter?
- What is the current beam diameter at the detector position?

If not in 40–60% range:
- Without F-θ in path: enlarge the beam.
- With F-θ in path: maximize as space allows, or use a diffuser.

> ⚠️ A focused beam (after F-θ) on the detector creates very high power density — **risk of damaging the detector**. Limit exposure time.

→ **Pause:** confirm beam size, or report inability to reach target.

### Step 4 — Heat up detector (laser ON, 2 min)

Per `measuring-laser-power.md` Step 4.

The detector head is constantly exchanging heat with its surroundings. Heating it up first eliminates that offset from the measurement.

→ **Pause:** confirm 2 minutes elapsed. Confirm operator is ready to block beam for Step 5.

### Step 5 — Block beam (laser OFF or blocked, 2 min)

Per `measuring-laser-power.md` Step 5.

Block the beam, allow head to reach thermal equilibrium. **For heads ≤ 30 W rated**, 1 minute is sufficient.

→ **Pause:** confirm 2 minutes elapsed.

### Step 6 — Zero

Per `measuring-laser-power.md` Step 6.

Operator zeros the monitor. Laser must be off and environment thermally stable.

→ **Pause:** confirm zero captured. Read the displayed zero value back to the operator and log it.

### Step 7 — Take the reading (laser ON, 1 min)

Per `measuring-laser-power.md` Step 7.

- If anticipation is **enabled**: reading available in ≤ 1 second.
- If anticipation is **disabled**: wait 1 minute for stabilization.

Record:
- Average power reading.
- Time when reading was taken.
- Wavelength correction factor applied (Y/N — see post-checks below).

→ **Pause:** confirm reading captured.

---

## Post-measurement checks

Per `measuring-laser-power.md` — Additional Notes.

### Wavelength correction

If the laser wavelength is **not 1064 nm**, confirm:
- The per-detector correction factor was applied (auto-applied if the monitor knows the operating wavelength).
- The correction value used.

If the operator is uncertain, the reading is **not valid** until this is sorted.

### Zero check

Did room temperature drift during warm-up? If yes, re-zero before trusting the reading.

### Repeatability

Compare to the previous reading on the same laser/detector pair:
- Power-meter repeatability: **±0.5%**.
- Differences larger than 0.5% are real and worth investigating:
  - Laser drift / warm-up not complete?
  - Optic contamination on the path?
  - Alignment shift?

→ **Pause:** ask the operator to log the reading and any notes. Skill complete.

---

## Output

A measurement record (markdown):

- Date / time
- Laser ID, detector ID, configuration
- All 7 step confirmations
- Final reading + wavelength correction status
- Any anomalies flagged
- Comparison to last known reading if available

Save to `outputs/laser-power-measurement/<YYYY-MM-DD>-<laser-id>.md`.

---

## Cross-skill links

- If the reading is unexpectedly low: hand to `laser-troubleshoot` (Steps 2–4 there cover optic contamination and alignment).
- If repeated readings differ by more than 0.5% with no obvious cause: also `laser-troubleshoot`.
