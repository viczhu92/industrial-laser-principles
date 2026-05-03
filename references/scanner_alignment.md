# Galvo Scanner Alignment

## When to use this file

For the practical mechanics of **steering a laser beam through a galvo scanner onto a focused work surface** — beam-path geometry, the four alignment degrees of freedom, picking reference targets, beam-visualization tools, and where the beam expander fits in. For the process-tuning that happens *after* alignment is done (focal-plane finding, scan delays, field calibration), see `scanner_optimization.md`. For beam physics, see `gaussian_beam_theory.md`. For optic care that often masquerades as alignment, see `laser_optics_cleaning.md`.

---

## 1. The Beam Path as Geometry

A laser beam between source and target is, geometrically, a line in 3-space. Two points define it:

- **Target** — fixed. The work surface, the focal plane, or whatever reference you've nominated.
- **Source** — adjustable. Where the laser comes out is what you actually move during alignment.

### Four degrees of freedom

Pick a Cartesian frame with Z along the beam, X horizontal, Y vertical (both transverse). Any deviation from the designed beam path is described by:

| Symbol | Meaning |
|---|---|
| `dX` | Lateral offset along X |
| `dY` | Lateral offset along Y |
| `Yaw` | Angular tilt about Y (beam rotation in the XZ plane) |
| `Pitch` | Angular tilt about X (beam rotation in the YZ plane) |

To put the source on the target you have to adjust **two translations and two angles**. They are independent and need independent reference points.

> **Engineer's intuition:** "Centered" and "aligned" are not synonyms. Translation and angle are independent — any procedure that mixes them up will cycle endlessly without converging.

---

## 2. Beam Profile Basics

Most laser beams have a Gaussian or near-Gaussian intensity distribution: a soft peak with no hard edge. The conventional "diameter" is the **1/e² diameter**, which contains **86.5% of the total power**.

### Roundness and orientation

A perfectly circular beam has equal X and Y diameters. When unequal, the beam is **elliptical**:

```
Roundness = Minor diameter / Major diameter   (in %)
```

An ellipse also has an **orientation** — the angle of its major axis in the X-Y plane.

> ⚠️ **Trap:** an elliptical beam whose major axis sits at exactly **45°** in the XY frame *measures* as roundness = 1 in those coordinates, even though it isn't circular. Roundness without an orientation reading is meaningless.

---

## 3. Why a Focusing Lens Amplifies Sensitivity

Inserting a lens between source and target concentrates the beam into a focus, raising energy density at the work surface. The geometry only works perfectly when the beam enters the lens **centered and perpendicular**. Any deviation produces:

- a larger focal diameter,
- a lower peak energy density (which scales as **1/diameter² → quadratic in the alignment error**),
- asymmetric X/Y at the focus.

When you stack a galvo scanner on top of the lens, every alignment error is multiplied by the angular leverage of the steering mirrors. Sensitivity goes up by an order of magnitude.

---

## 4. Motion Control — Stages, Galvos, and Combinations

Two fundamentally different mechanisms move a focused beam to where it needs to be on the workpiece. The choice between them — and the way they're combined — drives most of the system architecture.

### Translation stages
Stacked XY (and sometimes Z) stages physically move the part:
- **Strengths:** unlimited working area (just stack longer stages), micron-scale resolution, well-understood metrology.
- **Limits:** real mass requires high-current motors, and acceleration and top speed are bounded by the mechanics. **Typical top speed ~ 200 mm/s.**

### Galvo scanners
A galvo is a small mirror on a torque-spring-loaded shaft driven by a servo motor. The "moving mass" is a few grams of mirror — orders of magnitude less than a stage carriage:
- **Strengths:** much higher scan speed — **typical top speed ~ 5 m/s**. The beam is the only thing that moves once it leaves the galvo, so cycle time per feature is minutes faster than equivalent stage motion would be.
- **Limits:** **field of view is small** — bounded by the scan-angle range of the mirrors and the geometry of the focusing optics downstream.

### Polygon / raster scanners
A rotating multi-faceted mirror replaces the galvo on the fast axis. Each facet sweeps across the field as it rotates past the beam:
- **Top scan speed reaches ~ 100 m/s** — an order of magnitude faster than galvos.
- Only practical for **raster-type processing** (uniform line-by-line patterns). They can't vector-address arbitrary geometry.

### Marking on the Fly (MoF / MOtF)
Putting a galvo on top of a moving stage gives **fast scan over a large area** without forcing either mechanism to do something it's bad at. The galvo handles fast scanning inside a tile; the stage either steps to the next tile or moves continuously while the galvo compensates in real time. Almost all production marking and dicing systems on large parts work this way.

### A third axis (Z)

3D laser machining needs Z motion. Two common implementations:
- **Z-stage on the sample** — moves the workpiece up and down. Mechanically simple, but inherits the mass problem.
- **Moving focus lens** — adjusts the focal plane inside the optical column. Used when the application needs **high-speed Z adjustment**, e.g. correcting field curvature dynamically as the galvo sweeps.

### More degrees of freedom

Adding **rotational stages, piezo stages, or hexapod platforms** opens up multi-dimensional micromachining — angled cuts, conformal patterning, beveled edges, etc.

> ⚠️ **Robot arms are tempting** because of their reach and dexterity, but they don't carry the **micron-scale accuracy** that micromachining requires. Use a robot for part handling and gross positioning, not for the actual laser process.

---

## 5. The Two-Reference Principle

A positive lens converges parallel input rays to a single point at the focal plane. That has a useful consequence for alignment: **lateral translation of the input beam doesn't change where the focus lands on the focal plane** — it only changes the angle of arrival. Two reference points are needed, one for angle and one for translation.

### Sequence

1. Adjust **angle** so the beam reaches the **far-target** at the focal plane.
2. Adjust **translation** so the beam passes through the **near-target** at the scanner input aperture.
3. Iterate — in practice the two adjustments couple slightly because of mount asymmetries.

### The two targets

- **Near-target** — the scanner input aperture itself. A crosshair or iris dropped into the aperture provides a mechanically registered, unambiguous center.
- **Far-target** — the projection of the focus-lens center, perpendicular to the lens, onto the work surface. This has no obvious physical fiducial.

### Four ways to materialize the far-target

1. **Purpose-built tooling** — designed for the specific machine.
2. **Mechanical metrology before the scanner aperture.** The two reference points need at least **300 mm** of separation for useful precision.
3. **Mirror retro-reflection.** Only valid when the scanner-lens centerline is parallel to the work-surface centerline within **< 0.1°**. Place a flat mirror on the work surface — the beam reflecting back into itself confirms perpendicularity.
4. **Z-axis single-shot pattern.** Only valid when the Z-stage axis is parallel to the focus-lens normal within **< 0.1°**. Fire single laser shots at progressively different Z heights — the resulting pattern walks laterally if there's residual angular error.

Methods 3 and 4 are good **verifications**. They are not practical when the alignment loop runs many iterations.

---

## 6. Tools for Locating the Beam Center

Four ways to read out where the beam center actually is:

### CCD-based beam profiler
A CCD camera plus fitting software returns a Gaussian fit, center, and diameter. **The most informative tool by a wide margin** — but very sensitive to background light. Block room lights and use ND filters with OD > 1 to keep the camera out of saturation. Common software is **Ophir BeamGage** (`ophiropt.com/laser--measurement/software-download`).

### Knife-edge method
A razor blade translated tangentially into the beam, with the un-blocked portion captured on a power meter. The center is where the meter reads 50% of full power; diameter follows from a few sample points and an erf fit. Slow, manual, **rarely worth the time** for routine alignment.

### Crosshair targets
Two thin wires across an aperture, mechanically registered to the optic mount. The shadow appears in any beam detector. On a CCD, the diffraction fringes around the wires are symmetric *only* when the beam is centered on the crosshair — making them a precise visual reference.

### Aperture targets
An aperture casts a similar shadow visible in any detector. Coarse alignment by judging beam-edge symmetry by eye; fine alignment by reading the symmetric fringe pattern around the edge on a CCD. Works only when the **beam diameter is between roughly 0.25× and 1×** the aperture diameter.

---

## 7. Visualizing an Invisible Beam

Most industrial fiber lasers operate at **1064 nm** — invisible to the eye and dangerous at any meaningful power. The eye's blink reflex provides no protection against IR radiation.

> ⚠️ **Safety:** alignment exposes operators to laser energy. Don't attempt alignment without laser-safety training and the right PPE. Verify no bystander is in the beam path or any reflected path.

Five visualization tools, ordered roughly by power capacity:

| Tool | Power range | Stationary use? | Center? | Diameter? |
|---|---|---|---|---|
| **Red IR card** (phosphor) | mW | No — wave only | No | No |
| **White card** (frequency-conversion crystal — glows green) | < 5 W | Yes | Edge / circumference | No |
| **Burn paper / Zap-It** | mW (or large-diameter beams) | Single shot | Edge / circumference | No |
| **IR viewer** (photomultiplier-based) | W | Yes | Edge / circumference | No |
| **CCD beam profiler** | mW–W | Yes | **Yes** | **Yes** |

### Practical notes
- **Red IR cards** are extremely sensitive — single-digit mW lights them up; a few hundred mW will burn them. Use only for *presence detection* by waving the card through the beam. Direct any reflection away from any face. Recharge by exposing the card to room light afterward.
- **White cards** glow green via wavelength conversion. They tolerate higher power, which makes them stationary-usable but also more dangerous. Unlike red cards, they give a rough impression of beam roundness.
- **Burn paper** is single-shot — the beam discolors the paper from black to whitish. Use only at low power or with a deliberately enlarged beam, typically through a crosshair with a single laser pulse.
- **IR viewer** converts the invisible beam into a visible image when it lands on a target. Use a power meter as a safe terminating target. Adjust the front iris for brightness, focus the front lens onto the photomultiplier, then iterate front-and-back focus for sharpness in the field center. Edges will always be soft — these are not high-end optics.

> ⚠️ **Never** put a detection card or an IR viewer **at the focal point**. The card will burn through; the viewer will saturate or be damaged.
>
> ⚠️ Cards and IR viewers can show beam *position* but **not beam diameter**. Only a beam profiler can.

---

## 8. Aligning the Galvo Scanner Itself

In most production setups the scanner is bolted to a fixed bracket and **pre-aligned by the integrator**, so the relationship between scanner and work surface is known. In that case the alignment problem reduces to:

- **Near-target:** scanner input aperture.
- **Far-target:** focus-lens center, perpendicular to the lens, projected to the work surface.

Adjust `dX`, `dY`, `Yaw`, `Pitch` by steering the laser source until both targets are hit.

### Tolerance rule of thumb

| Spec | Typical |
|---|---|
| Position into scanner aperture | **< 0.3 mm** |
| Angle into scanner aperture | **< 5 mrad** (≈ 0.29°) |

**Concrete example:** a typical industrial 200W-class ns fiber laser may have an exit-beam tolerance of **~ 1 mm and ~ 2 mrad (0.1°)** — *larger* than the scanner's input tolerance. The optical path between laser and scanner therefore has to *correct*, not just preserve, the laser's exit pointing. External alignment has to be precise; "good enough" is genuinely not good enough.

### Astigmatism and polarization

Both are properties controlled by **optical-system design** and incoming beam quality, not by the field alignment process. Don't try to compensate them with aperture adjustments — verify them as part of incoming inspection on the laser source instead.

---

## 9. The Focusing Lens: Basic vs. F-Theta (Telecentric)

The focusing lens is part of the scanner — it is designed for a specific separation from the galvo mirrors and cannot be casually swapped without re-engineering.

| Lens type | Field of view | Beam angles in field | Focal surface |
|---|---|---|---|
| **Single-element basic lens** | Large | Large at edges | **Curved** — focus drifts off-plane toward the FoV edges |
| **F-θ (telecentric) lens** | Engineered for the scanner | Telecentric — beam exits perpendicular to the work surface | **Flat** across the FoV |

A telecentric lens is a multi-element design and demands a well-centered, well-angled input. It also has a defined **Working Distance (WD)**, listed in the spec sheet — the work surface must sit at exactly that distance from the lens.

> **Diagnostic:** if the actual best-focus distance is significantly different from the specified WD, the most likely cause is a **beam-expander problem** — usually the divergence setting is off, so the beam reaching the scanner isn't collimated.

---

## 10. The Beam Expander

A beam expander is an optional fourth optical element placed between the laser source and the scanner. Its purpose is to set the beam diameter that enters the scanner.

### Why beam diameter at the scanner matters

Focal-spot diameter is *inversely* proportional to the input beam diameter:

```
D_focus = 4 · M² · λ · f / (π · D_input)
```

| Symbol | Meaning |
|---|---|
| `M²` | Beam quality factor [—] |
| `λ` | Wavelength [µm] |
| `f` | Focal length of the focus lens [mm] |
| `D_input` | Beam diameter at the focus lens [mm] |
| `D_focus` | Focal-spot diameter [µm] |

So a **1.5× beam expander** delivers a **1.5× smaller focal spot**. A **variable beam expander** lets you tune both magnification *and* divergence — which gives independent control over spot size and focal-plane position.

### Sizing rule of thumb

Set the beam expander so the beam fills **50–60% of the scanner aperture diameter** for optimum focal spot. Smaller and you waste the lens's resolving power; larger and you start clipping and adding aberrations.

> ⚠️ A beam too small *or* too large into the scanner aperture cuts process quality. As an order-of-magnitude example: replacing a laser with one whose beam diameter is **10% smaller** can yield about a **21% loss in cutting efficiency** (energy density scales as diameter², so 1.1² ≈ 1.21).

### Inside a beam expander

A beam expander is conceptually a **diverging lens followed by a converging lens** (Galilean topology). The first lens expands the beam, the second re-collimates it at the new diameter. A lens centered on the beam axis preserves angle while changing diameter — exactly what's needed.

### Aligning *with* a beam expander

A misaligned beam expander steers the beam off-path. The procedure has to respect that:

1. **Do primary alignment without the beam expander.** Source → scanner aperture → focal plane.
2. Insert the beam expander only after primary alignment is locked in.
3. If the expander is variable, **set its magnification first**, then align.
4. Ideally the expander has 4 axes of fine adjustment: 2 translation + 2 angular.

### Adjustment workflow

- Use the **far-target (focal plane)** for the expander's **angular** adjustment only.
- Use the **near-target (scanner aperture)** for the expander's **translation** adjustment.
- Iterate.

### Profiler-based alternative

1. Place a beam profiler somewhere between the focus lens and the focal plane.
2. **Remove** the beam expander. Record the location of the beam center on the profiler.
3. **Reinstall** the beam expander. Adjust its angular axes until the beam center returns to the recorded location.
4. The scanner input aperture imprints fringes on the beam profile. Translate (X, Y) the expander until those fringes form a symmetric, circular pattern.
5. Iterate angle and translation as needed.

---

## 11. Alignment Troubleshooting

Production samples are the only definitive answer on whether alignment is good. The single most common alignment-related defect is **cut-quality degradation from fluence loss** — and fluence depends on both pulse energy and spot size, which means it can be misdiagnosed as either an alignment issue or a laser issue.

### Verify in this order before assuming alignment is at fault

1. **Power at the laser output** — measured directly, before any downstream optic. Confirms the source is actually delivering spec.
2. **Optic cleanliness** — every transmissive surface in the beam path. (See `laser_optics_cleaning.md`.)
3. **Focus-plane parallelism** — confirm that the focal plane is parallel to the work surface.
4. **Then** start alignment checks.

### Procedure for a laser replacement

1. Remove the **beam expander** and the **focus lens**.
2. Align the new source through the **scanner input aperture** (near-target) to the **focal-plane reference** (far-target).
3. Reinstall the **focus lens**, maintaining alignment.
4. Reinstall the **beam expander**, in that order, maintaining alignment.

### Procedure for first-time installation

Metrology is required to align the **perpendicularity and centering of the scanner relative to the work surface**. This part can't be done with the laser alone.

### Reality check

Most production systems don't have the access, space, or rigid reference points that a textbook procedure assumes. Every system therefore involves **some assumptions and improvisation** — typically captured in tool-specific work instructions rather than in a generic alignment doc.
