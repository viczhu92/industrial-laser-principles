---
name: laser-delay-tuner
description: Diagnose and tune scan-delay parameters (LaserOn, LaserOff, Jump, Mark, Polygon) by interpreting corner / line-end defects. Use when the user says "corner is rounded", "burn-in at line start/end", "line ends short", "scan delays", or has any scan-delay tuning question.
---

# Laser Scan-Delay Tuner

> Operates under the rules in `../../INSTRUCTIONS.md` (reference-first, reference-only, interactive mode).

## When to use this skill

When marks or cuts show defects at **line starts, line ends, or corners** — and the suspected cause is a mistuned scan delay. This skill reads the symptom, identifies the offending delay, and proposes a specific adjustment anchored to the laser's pulse-to-pulse interval.

## References to load at start

- `references/scanner_optimization.md` §8–§10 — primary

## The fundamental constraint

Per `scanner_optimization.md` §10:

> Adjustments **smaller than one pulse interval may produce no observable change** — between pulses the beam is off anyway, so a sub-interval shift is invisible.
> Coarse-tune in 1–2 pulse intervals; fine-tune within that.

This drives every step-size recommendation in this skill.

## Inputs to gather first

Ask the operator:

1. **Symptom description** — what does the defect look like, and where on the line/shape?
   - Burn-in (large dot) at line start?
   - Line start missing — mark begins late?
   - Line end short?
   - Burn-in at line end?
   - Curve / oscillation at start of mark?
   - Small curve at end of mark?
2. **Test pattern used** — square / rectangle / triangle? **Are direction arrows shown?**
3. **Material** (anodized aluminum is recommended per `scanner_optimization.md` §9).
4. **Current settings** — scan speed, PRF, current LaserOn / LaserOff / Jump / Mark / Polygon delays.

> ⚠️ **If the test pattern has no direction arrows**, ask the operator to **re-run with arrows**. Per `scanner_optimization.md` §9, without arrows you cannot tell whether a corner defect is at the *start* (LaserOn) or *end* (LaserOff) of the line. **Stop here** until arrows are included.

→ **Pause:** confirm inputs and test-pattern direction is known.

---

## Workflow

### Step 1 — Match symptom to root cause

Per the symptom table in `scanner_optimization.md` §9:

| Symptom | Root cause | Fix direction |
|---|---|---|
| **Burn-in (large dot) at line start** | LaserOn too short — laser fires before mirror at start | **Increase LaserOn** |
| **Line start missing — mark begins late** | LaserOn too long — mirror has moved past start | **Decrease LaserOn** |
| **Line ends short of endpoint** | LaserOff too short — laser cuts off before mirror arrives | **Increase LaserOff** |
| **Burn-in (dot) at line end** | LaserOff too long — laser stays on past mirror endpoint | **Decrease LaserOff** |
| **Curve / oscillation at start of mark** | Jump too short — mirrors hadn't settled before mark started | **Increase Jump** |
| **Total scan time longer than necessary** | Jump or Mark too long | **Decrease the offender** |
| **Small curve at end of mark** | Mark too short — mirrors hadn't reached endpoint before next jump | **Increase Mark** |

→ **Pause:** confirm symptom match. Show the candidate delay + fix direction. Wait for operator to confirm before proceeding to step size.

### Step 2 — Compute step size

Per `scanner_optimization.md` §10:

```
Pulse interval = 1 / PRF
```

Common values:

| PRF | Pulse interval |
|---|---|
| 20 kHz | 50 µs |
| 50 kHz | 20 µs |
| 100 kHz | 10 µs |
| 200 kHz | 5 µs |
| 500 kHz | 2 µs |

**Recommended adjustments:**
- **Coarse step:** 2 × pulse interval. Use this to find the right neighborhood.
- **Fine step:** 0.5 × pulse interval. Use this only after coarse-tuning has the symptom roughly correct.

Compute the recommended initial change for this operator's specific PRF and present:

> "Increase LaserOn from <current> by 2 × pulse interval = <X µs>, giving <new value>."

→ **Pause:** wait for operator to confirm the proposed step.

### Step 3 — Validate

Per `scanner_optimization.md` §9:

Recommend re-running the **same test pattern at the same scan speed and material**.

| Re-run result | Action |
|---|---|
| Symptom went away | **Done** with this delay. Go to Step 4 to optimize Jump/Mark. |
| Symptom **changed** (e.g., fixed one defect, exposed a different one) | Loop back to Step 1 with the new symptom. |
| Symptom is the **same magnitude** | Step size was too small — increase by another 1–2 pulse intervals. |
| Symptom is **inverted** (now over-corrected) | Reduce step. Try 0.5 × pulse interval in the opposite direction. |

→ **Pause:** ask the operator to report the new pattern result. Loop.

### Step 4 — Optimize the slow delays

Per `scanner_optimization.md` §8 — Throughput note:

After **LaserOn / LaserOff are correct**, reduce **Jump and Mark** down to the smallest values that still give clean corners. Jump and Mark each extend cycle time; LaserOn / LaserOff do not.

The order matters:

1. During LaserOn / LaserOff tuning (Steps 1–3), **Jump and Mark were deliberately long** so they didn't mask other defects.
2. Now reduce them in **1–2 pulse-interval increments** until corner quality starts to degrade.
3. **Back off one step** to the last clean setting.

→ **Pause:** present each Jump / Mark adjustment for confirmation. Loop until both are at minimum-clean.

---

## Boundary call-outs

If the operator reports defects that do **not** match the §9 table, this is **not** a scan-delay problem. Examples:

- Edge of mark is wavy → likely galvo dynamic-response issue or feedforward misconfiguration (`scanner_optimization.md` §7).
- Depth varies along the line → laser power instability or rise-time effect (`scanner_optimization.md` §6).
- Pattern is shifted from commanded location → field calibration or scaling (`scanner_optimization.md` §4–§5).

In any of these cases, hand off to `laser-troubleshoot` (general triage) or `laser-defect-diagnose` (defect classification).

---

## Output

A delay-tuning record (markdown):

- Symptom history (each iteration)
- For each iteration: which delay, before / after value, observed result
- Final settings (LaserOn / LaserOff / Jump / Mark / Polygon)
- Speed / power / PRF point at which they were validated
- Notes for any speed-power point variations the operator anticipates

Save to `outputs/laser-delay-tuner/<YYYY-MM-DD>-<machine>.md`.

> **Reminder:** Settings tuned at one scan speed will likely **not** be correct at another. Per `scanner_optimization.md` §9, delays scale with speed.
