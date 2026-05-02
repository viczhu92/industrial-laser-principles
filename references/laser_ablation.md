# Laser Ablation Process

## When to use this file

For the physics and process knobs of **laser material removal** — what governs ablation rate and quality, why pulse width and wavelength change everything, how multi-pulse overlap and plume management drive real-world recipes. For weld-mode selection, see `laser_welding.md`. For cutting and dicing specifically, see `laser_dicing.md`. For computing fluence and intensity, see `laser_process_calculations.md`.

---

## 1. What Ablation Is

The word *ablation* means "carried away." In laser context it refers to material removal driven by photon-deposited energy. The mechanisms vary with material and pulse regime, but the end state is the same — material that was on the workpiece is now somewhere else.

---

## 2. Material Categories

Ablation behavior depends strongly on what's being processed. Four broad classes cover most industrial work:

1. **Single elements** — metals, diamond, etc. Behavior dominated by thermal and electronic properties.
2. **Molecular structures**
   - **Hard:** ceramics like Al₂O₃ — strong bonds, high ablation thresholds.
   - **Soft:** plastics and polymers — low bond energies, but heat-flow problems.
3. **Composites** — PCB stack-ups (epoxy + glass fibre), populated semiconductor packages — adjacent components within the same beam path can have *opposite* ablation requirements.
4. **Biological** — soft, water-rich, regulated; outside the scope of most industrial laser work.

---

## 3. Four Mechanisms of Material Departure

At the point of ablation, material leaves the surface through one or more of four physical pathways:

1. **Evaporation** — solid → liquid → vapor.
2. **Sublimation** — solid → vapor directly, skipping the liquid phase.
3. **Plasma formation** — ionized state, energetic enough to break molecular bonds outright.
4. **Mechanical ejection** — sudden subsurface heating produces micro-explosions that throw out solid debris.

The first three eject material as gas; the fourth ejects solid particles. Real processes usually involve more than one mechanism in sequence.

### Photon-induced chemistry

Some materials decompose chemically under photon exposure, releasing energy that then accelerates the ablation process:
- **Titanium** oxidizes to titanium-oxide dust, releasing chemical energy that mixes back into the ablation event.
- **AlN** decomposes into Al₂O₃ and nitrogen.

These reactions are part of why "the same laser" can give very different results on different materials.

---

## 4. The Ablation Threshold

Below a critical fluence — the **ablation threshold** — nothing happens. Above it, removal begins. The rate above threshold is decidedly non-linear:

- Doubling the fluence does **not** halve the process time.
- Excess energy beyond the optimum ends up heating the bulk rather than removing more material — which **enlarges the heat-affected zone (HAZ)** and degrades quality.
- Threshold curves vary by material; for some metals, fluence well above the optimum eventually reaches a different physical regime that does increase removal rate, but with a step change in HAZ.

### Materials that don't fit the standard curve

- **Crystalline silicon** actually benefits from some inefficiency — the bulk heating it produces lowers the threshold for subsequent pulses, raising the steady-state removal rate.
- **Transparent materials** (glass, sapphire, some polymers) cannot be ablated at all below the non-linear threshold — the energy passes through. Only when fluence reaches the level where multi-photon and plasma processes kick in does anything happen.

> **Engineer's intuition:** Every ablation process has an optimum fluence, usually a small multiplier above threshold (~ 2–5×). Pushing harder past that point trades quality for speed. Characterizing the curve for the specific material is non-negotiable.

---

## 5. The Process Parameter Map

Ablation outcomes depend on a long list of variables. Useful to organize them by where in the system they originate:

### Laser source
- Wavelength
- Waveform / pulse shape
- Average power
- PRF (pulse repetition frequency)
- Pulse width
- Rise time
- Simmer level
- Peak power
- M² (beam quality)

### Optics
- Aperture diameter
- Beam-expander magnification
- Focus lens (focal length, F-number)
- Focal depth (Rayleigh range)
- Aberrations
- Field of view
- Alignment (see `scanner_alignment.md`)

### Motion
- Scan speed
- Trigger accuracy (see `scanner_optimization.md`)
- Pitch (pulse-to-pulse spacing)
- Hatch (line-to-line spacing)
- Delay times
- Position accuracy
- Number of repeats / passes

### Target material
- Absorption (function of wavelength × material spectral response)
- Thickness
- Thermal conductivity
- Surface state
- Melting / evaporation point
- Volume of material to remove

### Work surface and environment
- Size, flatness
- Vacuum / clamping
- Gas type, pressure, flow speed
- Exhaust / fume extraction
- Plume deflection management

### Output / quality metrics
- Cycle / takt time
- Heat-affected zone (HAZ)
- Final temperature

---

## 6. Absorption Physics

Absorption is the **energy-coupling** parameter — how much of the incident photon energy actually deposits in the material. It is governed by **wavelength × material spectral response** and is the single most important consideration when choosing a wavelength.

### Absorption depth

The penetration depth of the light into the material determines where the energy actually deposits:

| Absorption depth | Effect |
|---|---|
| **Very shallow** (high absorption) | Energy concentrates near the surface — efficient surface scribing / scrapping behavior |
| **Some depth** | Subsurface accumulation drives micro-explosions that eject larger particles — high removal rate |
| **Too deep** | Energy spreads through bulk, fluence drops below threshold — nothing useful happens |

For **transmissive materials**, none of this applies — energy passes through until non-linear effects at the focus alter the absorption.

---

## 7. Pulse Width and "Cold" Ablation

Real laser pulses have a sharp **rise time**, a peak that rolls over, and a slower decay tail. **Pulse width is the FWHM** — full width at half maximum.

### The pulse-width gradient

Compare 10 ps and 40 ns: a factor of **4000** in time. At the same pulse energy, the picosecond peak power must be 4000× higher than the nanosecond peak. To survive that internal flux, ps lasers run at higher PRF and lower pulse energy — so in practice the peak-power difference between a typical ps and ns laser is closer to **400×–1000×**, not 4000×.

### Why ultrafast matters

At ~ ps and below, photon energy deposits faster than thermal diffusion can carry it away. Bonds break before the lattice has time to heat. The label is **"cold ablation"** — minimal HAZ, sharp edges, high quality.

### The catch with cold ablation

- The ablation threshold drops with pulse width — by roughly **√(τ)**, so a 10 ps pulse has ~ 30–40× lower threshold than a 40 ns pulse.
- The available peak power (1000× higher than ns) must therefore be brought back down by a similar factor to stay in the few-times-threshold zone.
- Net result: removal rate at true cold-ablation conditions is *much slower* than warm ablation.
- In production, the standard compromise is to push fluence well past the cold-ablation optimum — accepting some HAZ in exchange for usable throughput. This is sometimes called **"warm ablation"**: better quality than ns processes, slower than ns processes at the same average power, with a quality/speed dial that an engineer actually controls.

---

## 8. Beam Quality (M²)

Most laser beams have a Gaussian profile in the transverse plane. Beam diameter is defined as the diameter of the circle containing **86.4%** of the energy.

The **M² number** (also called **Beam Parameter Product** or BPP) measures how close the actual beam is to a pure Gaussian:

| M² | Profile | Implication |
|---|---|---|
| 1 | Pure Gaussian | Smallest possible focal spot, highest fluence |
| 1.1–1.3 | "Gaussian" laser | Real-world high-quality beams |
| > 1.6 | Super- / hyper-Gaussian | Flattened-top profile |
| > 2 | Flattop | Lower peak fluence over a larger area |

**What M² is good for:**
- **M² ≈ 1** is preferred for **cutting and milling** — every photon counts, peak fluence drives the process.
- **M² > 2** is preferred for **area treatments** like cleaning — uniform coverage matters more than peak intensity.

---

## 9. Multi-Pulse Ablation

Single-shot ablation is the simplest case. Most real processes use many pulses, and the overlap geometry then dominates outcomes.

### Three motion regimes

- **Percussion drilling** — beam stationary, repeated pulses on the same spot.
- **Cutting** — beam moves linearly while pulsing.
- **Trepanning** — beam follows a circular path to make a hole *larger* than the focal spot.

### Pulse overlap math

Define the spacing between consecutive pulse centers as a fraction of the focal spot:

- **Spacing > spot diameter** — no overlap. Each pulse interacts with virgin material — equivalent to a row of single shots.
- **Spacing = spot diameter** — overlap = 1. Three pulses interact with each other at any point.
- **General case** — at overlap O, **(2·O + 1)** pulses interact with each other at any point.

Heat is the dominant cross-pulse mechanism in nearly all cases. A useful test pattern: vary scan speed against an inverse number of repeats so total energy delivered is constant — the only varying parameter is **how heat accumulates between pulses**.

The same overlap concept applies to the **hatch distance** between parallel scan lines.

### Wobble

Wobble adds a fast circular motion on top of the linear scan. The circle frequency must be much higher than the linear scan rate, otherwise the pattern degenerates into a stretched spiral. Wobble is used for marking and for fusion cutting.

> ⚠️ Wobble is unusable with **ultrafast lasers** that already operate near galvo speed limits — there's no headroom for the additional wobble motion.

---

## 10. Plume and Gas Management

Ablated material exits the surface in a roughly **180° radial pattern**. Once a groove or trench has been cut into the material, the geometry funnels the debris **upward in a narrow V-shape** along the beam axis — directly into the incoming laser path.

This is **plume shielding** (or plasma shielding): the upward jet of debris and ionized gas scatters and absorbs the incoming beam, dropping fluence at the work surface.

### Standard mitigation

- **Cross-flow gas** — a transverse air stream that pushes the plume sideways out of the beam path. Side benefit: the airflow cools the workpiece.
- **Vacuum / inert atmosphere** — the gold standard. Particles fly out unimpeded; no chemistry with the ambient gas. **Helium** is the practical alternative when vacuum isn't possible.

### Process gas selection

Different gases participate in the ablation chemistry differently:

| Gas | Effect |
|---|---|
| **Oxygen** | Adds heat through oxidation reactions — helpful for some metals, problematic when it triggers unwanted micro-explosions |
| **Argon** | Inert — disables gas-phase chemistry |
| **Helium** | Inert and light — good plume clearance, almost as effective as vacuum |
| **Vacuum** | No interaction at all — ideal but rarely practical in production |
| **Air** | Default; mixed effects |

---

## 11. The Heat-Affected Zone (HAZ)

Every ablation process produces side effects, and the dominant one is the **heat-affected zone** — material near the cut that received heat without being removed.

**HAZ is a qualitative spec.** Its definition has to be re-established for each application:

- Visual discoloration from elevated temperature.
- Surface change from melt-and-resolidify.
- A boundary where ejected debris re-deposited.
- Microcrack extent.
- Invisible material restructuring (grain change, phase change).
- Specific molecular depletion or chemical change.

> **Engineer's intuition:** If two HAZ specs differ by 10× across vendors, the difference is almost always definitional, not real. Always ask which HAZ measurement criterion the spec uses before comparing.

---

## 12. Recipe Development Workflow

Translating the physics in §1–§11 into a working ablation recipe is a structured process. The most effective approach is a three-step progression — **surface → depth → volume** — where each step builds on what the previous one revealed.

### Step 1 — Surface: single-shot threshold

The goal is to pin down the ablation threshold for the specific material at the wavelength being used.

**Method:**
- Fire **non-overlapping** single shots by combining a **low PRF with a high scan speed**, so pulse-to-pulse spacing is much greater than the focal spot. This keeps the rise-time tail (§7) out of the threshold reading — the first pulse on each spot is the only pulse on that spot.
- Step fluence through a series of single shots on a clean coupon.
- Threshold is the fluence at which the surface is **visibly altered with minimal change** — the just-noticeable-difference between an untouched spot and a marked one.

That endpoint is hard to call by eye, so the practical refinement is the **Liu plot method**:

- Measure the **crater diameter** at each above-threshold fluence.
- Plot **(crater diameter)² vs. log(fluence)**.
- The linear extrapolation crosses the x-axis at the ablation threshold fluence.

If literature values exist for the material at the working wavelength, use them as a sanity check or a starting seed before committing coupon time.

### Step 2 — Depth: a single line, with overlap

The goal is to see how **cumulative heating and plume shading** change behavior versus a single shot.

**Method:**
- Use the Step 1 threshold as the seed of the fluence range.
- Build a **matrix of lines** varying **Power** and **Scan Speed** — the two most consequential knobs at this stage.
- Inspect each line for cut quality, kerf geometry, and HAZ scale.

> ⚠️ **Use a logarithmic axis for both Power and Scan Speed.** The eye easily distinguishes 0.5 m/s from 1 m/s, but cannot reliably tell 4.5 m/s from 5 m/s. A linearly-spaced sweep wastes most of its data points in regions where the difference is invisible.
>
> A convenient logarithmic series with rounded numbers:
>
> ```
> 0.1, 0.16, 0.26, 0.41, 0.65, 1, 1.6, 2.6, 4.1, 6.5, 10, ...
> ```
>
> Each step is approximately **1.6× the previous** (one-fifth of a decade). This grid covers two or three orders of magnitude with a manageable number of cells and meaningful contrast between adjacent settings.

Pick the cell that gives the best quality at the fastest speed — that becomes the unit recipe for Step 3.

### Step 3 — Volume: hatched area or deep cut

The goal is to extend the line recipe across an area, or down through depth, by stacking lines.

**Method:**
- Take the best line from Step 2 as the unit operation.
- Set the **hatch distance** between parallel lines (the line-to-line overlap concept from §9).
- For depth that exceeds what one sweep can clear, **stack passes**: repeat the matrix 2×, 4×, 8× until the depth or volume target is reached.

### Diagnostic: when more passes stop helping

The relationship between **number of repeats** and **inverse scan speed** tells you whether thermal accumulation is in play:

| Relationship | What it means | Implication |
|---|---|---|
| **Linear** | Heat-tolerant process — doubling repeats halves speed-to-target | Process scales well; throughput is the only knob |
| **Non-linear** (diminishing returns) | Strong thermal accumulation | Cooling between passes is dominating |

When the relationship is non-linear, two responses are available:

1. **Add a Pause between repeats** so the bulk has time to cool between passes.
2. **Lower the per-pass power** to reduce heat input per pass.

Both reduce thermal accumulation at the cost of overall process time. Which one is the right answer depends on the application's HAZ tolerance and throughput target.

> **Engineer's intuition:** When a recipe works on a small coupon and then falls apart at full production scale, this diagnostic is the first place to look. Heat accumulation effects scale with feature density and total run time — what looks like a stable process on a 25 mm coupon can be thermally unstable on a 200 mm panel.
