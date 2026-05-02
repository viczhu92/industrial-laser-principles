# Scanner Process Optimization

## When to use this file

Once the beam is mechanically aligned through the scanner (see `scanner_alignment.md`), the next layer of work is process-level tuning: locating the focal plane on the actual material, calibrating the scan field so commanded coordinates equal marked coordinates, and dialing in the timing delays that coordinate the laser with the galvo. This file covers all of that.

---

## 1. Locating the Focal Plane

By definition, the focal plane is the Z position where the spot is smallest and the peak fluence is highest. In practice it can be surprisingly hard to read off a marked sample.

Common visualization options include burn paper (Zap-It), anodized aluminum, and oxidized or coloured metal surfaces. Bare metals like copper and bare aluminum have a high ablation threshold — the bare surface is a poor diagnostic. A coloured anodize or oxide layer drops the threshold and makes a focus ladder readable at sane pulse energies.

> **Burn paper caveat.** Zap-It is fast and convenient, but the paper changes colour at very low fluence — meaning the visible "mark" can be much wider than the focused spot. Use it as a coarse first cut, not as the calibration reference.

### Two effects that confound visual sizing

1. **Threshold non-linearity.** Below the material's ablation threshold there is no mark; far above it, the mark saturates the visual signal. In the saturated regime the mark *width* no longer tracks the beam diameter — it tracks how much energy is poured in. A saturated mark cannot locate the focus.

2. **Beam diameter vs. Z.** The 1/e² diameter has a minimum at the focal plane and widens above and below it. Fluence drops as it widens because the same pulse energy spreads over more area. The mark gets visibly fuzzier and eventually disappears as defocus grows.

### Three practical tricks for finding focus on a focus ladder

The classical test is a row of short marked lines at evenly stepped Z heights:

1. **Reduce energy until only one line survives.** Drop the pulse energy step by step. The lines farthest from focus drop below threshold first. The last surviving line marks the position closest to the focal plane.

2. **Match the fuzziness on both sides.** Translate the entire ladder up or down until the leftmost and rightmost still-visible lines look *equally fuzzy* — both near threshold. The midpoint of that symmetric bracket is much better defined than trying to read focus off the brightest central line.

3. **Maximize pulse separation.** Set the scan speed so adjacent pulses *barely* touch on each line. The Z position where the gap between consecutive pulses is *largest* is the position with the smallest spot — i.e. the focal plane.

> **Side observation:** outer lines on a focus ladder also expose the laser's rise-time tail. The first few pulses on every line are weaker than the steady-state train, so each line shows a softer leading edge. (Order-of-magnitude reference: 50 kHz PRF, 4 m/s scan speed, dZ/z_R ≈ 1.4 between rungs, 200 µJ pulses in a ~50 µm waist.)

---

## 2. Astigmatism Across the Focal Plane

Astigmatism in the optical train means horizontal and vertical features can have **different best-focus Z positions**. Optimize for horizontal lines and the vertical lines go off-focus, and vice versa.

For applications that mark in both axes — which is most of them — set the calibration test pattern at **45°** so the focus search averages across both orientations rather than favouring one. The compromise focus this finds is acceptable for nearly all marking processes and is easier to find consistently than chasing the two extremes separately.

---

## 3. Edge-of-Field Correction

Field curvature is residual on most focusing optics, even telecentric (F-θ) lenses. If you set Z to optimize the centre of the FoV, the *edges* will sit slightly off-focus.

The fix is geometric: don't centre Z on the centre of the FoV. Set focus at a position **between the centre and the edge**, so the focus error spreads across the field rather than concentrating on the perimeter. This is the right move when edge quality matters more than dead-centre quality — which is usually the case for any feature that crosses a large fraction of the FoV.

---

## 4. Scaling Calibration (X / Y / Rotation)

A commanded distance does not yet equal the marked distance until you calibrate the scanner. Procedure:

1. Mark a square or rectangle with known commanded dimensions.
2. Measure the actual marked dimensions to whatever precision the application demands (a measurement microscope or vision system is typical).
3. Compute the X and Y scale errors and enter them as **global correction factors** in the scanner software, so every subsequent file scales identically.

If the scanner is paired with motion stages, also calibrate the **rotational alignment** between the scanner XY and the stage XY. Without this, the part picked up by the stage will not register correctly under the scanner — and any feature placed by both systems will be offset.

---

## 5. Field Calibration (Pincushion and Higher-Order Distortion)

Even after global scaling, the scan field will show distortion. Pincushion is the most common name, but the residual is often a higher-order surface that no single scale factor can flatten. Most scanner software supports a **field correction table** to handle this:

1. Mark a raster of points across the full FoV at known commanded coordinates.
2. Measure the actual marked positions.
3. Compute the per-node residual error (commanded minus actual).
4. Load the table back into the scanner software as a field correction.

The software then applies a per-region correction during scanning. Done well, this brings edge accuracy into the same range as centre accuracy — important for any feature that spans a large fraction of the FoV.

---

## 6. Laser Rise-Time

A common implicit assumption is that the laser turns on instantly. It does not.

- The **first pulse** can range from **0% to 200%** of the steady-state amplitude. Many lasers therefore implement **first-pulse suppression** — the controller deliberately holds the first pulse at zero, since it is the least repeatable pulse in the train and the most likely to deposit a burn-in spot.
- The next several pulses ramp toward steady-state along a thermal envelope, often with ringing. The amplitude transient typically runs over **5–500 µs** depending on laser type and PRF.
- Full stabilization of the pulse train — including any longer-timescale thermal settling inside the gain medium — can take **milliseconds to seconds** after turn-on.
- The vendor spec that summarizes all of this is **rise time** — usually defined as the time from the first pulse to **80%** of the long-train steady-state amplitude.

### Why this matters at the work surface

A 50 µs rise time at 5 m/s scan speed corresponds to about **250 µm** of travel during which the energy is below specification. That distance shows up at every line start as poor marking or incomplete cutting. As scan speed goes up, the affected distance scales linearly — fast scanning makes the rise-time penalty worse, not better.

### Knobs to tune

- **Pulse waveform** (when the laser supports multiple shapes).
- **PRF.**
- **Simmer** — idle pumping that pre-loads the gain medium and shortens rise time.
- **Power %.**

Each combination has different rise-time and pulse-jitter behaviour. Characterize on the actual material, not on a single benchtop test, before committing to production settings.

---

## 7. Galvo Motion vs. Trigger Timing

Equally common is the assumption that the galvo is at exactly the commanded speed at the programmed mark coordinates. It is not — the mirrors are accelerating into the line and decelerating out.

The fundamental issue is that conventional **reactive (PID-style) feedback** reads the present position, compares it to the demand, and adjusts the motor drive. Accuracy is therefore bounded by the loop's response delay — and gets *worse* as scan speed increases. Three tools exist to push past that limit:

1. **Pre-acceleration.** Begin the acceleration phase *before* the laser turn-on so the mirror is already at speed by the time the laser fires.
2. **Encoder-position triggering** (also called **fixed-distance triggering**). High-end motion controllers can fire a laser pulse after the stage or galvo has actually moved a programmed distance, instead of after a programmed time has elapsed. This eliminates start/stop burns and improves edge quality on cuts.

   > ⚠️ Not every laser can be triggered this way. Many have a fixed PRF range, an external-trigger response delay, or simply no external-trigger input at all. Verify the laser's external-trigger spec before designing a recipe around fixed-distance firing.

3. **Feedforward scan controllers.** Instead of reacting to position error after it appears, a feedforward controller computes the full galvo trajectory in advance from the mirror's known dynamic-response constants, and pre-compensates for that response inside the command stream. The result is **no acceleration burns and roughly an order-of-magnitude speed improvement** on intricate patterns versus reactive controllers.

> ⚠️ **Risk of accidental cancellation.** Acceleration and rise-time errors can cancel each other at one specific speed/power combination — making the result *look* correct at that one operating point. The combination falls apart at any other speed or power. Always validate across the full operating range you actually use, not at a single recipe.

---

## 8. Scan Delays — the Five Standard Knobs

Most laser-scanner software exposes **five timing delays** that coordinate the laser turn-on/off with the galvo motion. They split into two groups.

### Laser delays — when the beam fires

| Delay | When it acts | What it controls |
|---|---|---|
| **LaserOn** | Just before a scan line begins | Holds the laser off until the mirrors are positioned at the correct line start. Prevents a burn-in dot at the start. |
| **LaserOff** | Just after a scan line ends | Keeps the laser on until the mirrors actually reach the line endpoint. Prevents the line from being cut short. |

### Scanner delays — mirror settle time

| Delay | When it acts | What it controls |
|---|---|---|
| **Jump** | Before a scan line begins | Allows the mirrors to physically settle after a fast jump between lines. |
| **Mark** | After a scan line ends | Allows the mirrors to actually finish the line before the next jump or stop. |
| **Polygon** | At a vector angle change *inside* a connected polyline | Replaces Mark delay when the line continues — no full stop, just a smaller settle window. |

> **Throughput note.** With most controllers, **LaserOn and LaserOff do not extend total scan time** — they shift when the laser fires within an already-running motion. **Jump and Mark do extend scan time** — every additional millisecond there is added to the cycle. Optimize Jump and Mark down to the minimum that still gives clean corners.

---

## 9. Diagnosing Delay Misadjustment

The standard test marks a square or rectangle and looks at what happens at the corners.

| What you see | Root cause | Fix |
|---|---|---|
| **Burn-in (large dot) at line start** | LaserOn too short — laser fires before mirror reaches start | Increase LaserOn |
| **Line start is missing — mark begins late** | LaserOn too long — mirror has already moved past start | Decrease LaserOn |
| **Line ends short of endpoint** | LaserOff too short — laser cuts off before mirror arrives | Increase LaserOff |
| **Burn-in (dot) at line end** | LaserOff too long — laser stays on past mirror endpoint | Decrease LaserOff |
| **Curve / oscillation at start of mark** | Jump too short — mirrors hadn't settled before mark started | Increase Jump |
| **Total scan time longer than needed** | Jump or Mark too long | Decrease the offender |
| **Small curve at end of mark** | Mark too short — mirrors hadn't reached endpoint before next jump | Increase Mark |

### Recommended tuning order

1. Set **Jump and Mark to deliberately long values** so they aren't masking other defects.
2. Tune **LaserOn and LaserOff** to perfection on a square test pattern.
3. Then reduce Jump and Mark down to the smallest values that still give clean corners.

### Designing the test pattern

Use a triangular pattern with **arrows showing vector direction** — without the direction indicators you can't tell whether a corner defect is at the *start* (LaserOn problem) or *end* (LaserOff problem) of a line. **Number each test triangle** so you can correlate iterations against the delay setting that produced them — finding the right values is repetitive and back-tracking matters.

Run the test on the **production scan speed and material** you'll actually use. Anodized aluminum is convenient — predictable absorption and high contrast. Settings tuned at 1 m/s will not be correct at 5 m/s; delays scale with speed.

---

## 10. Step-Size for Delay Adjustments

When stepping a delay value, anchor your increments to the laser's **pulse-to-pulse interval**:

```
Pulse interval = 1 / PRF
```

At 20 kHz PRF the interval is **50 µs**. Adjusting any delay by an amount **smaller than one pulse interval may produce no observable change** — between pulses the beam is off anyway, so a sub-interval shift is invisible.

> **Engineer's intuition:** Coarse-tune in increments of 1–2 pulse intervals to find the right neighbourhood; fine-tune within that window. Trying to bisect 5 µs differences at 20 kHz is wasted effort.
