# 7 Steps for Measuring Laser Power

## STEP 1 – FIRE UP YOUR LASER AND MAKE SURE IT IS STABLE BEFORE STARTING A POWER MEASUREMENT (5 min for ns and CW fiber laser, 10–20 min for ps lasers)

Wait for the laser to reach a stable operating point before taking a power measurement. The required warm-up is typically 5 to 20 minutes depending on the laser type. The optical components shift as the laser reaches thermal equilibrium with its environment; the laser should not be used for measurements before equilibrium is reached.

## STEP 2 – MAKE SURE YOU USE THE DETECTOR WITHIN ITS SPECIFICATIONS

Not every detector works with every laser. Each detector has its own specification envelope, and the chosen detector must match the laser's parameters for the measurement to be accurate. Common specifications to check include average power, power density, energy, energy density, and repetition rate.

## STEP 3 – MAKE SURE YOUR BEAM SIZE IS 40% TO 60% OF THE OPTICAL APERTURE

This is the most reliable way to ensure heat is fully absorbed and transferred to the power meter. The sensing element behind the absorber is large and symmetrical, so the full aperture area should be used. A beam that is too small raises the risk of damaging the detector during measurement. Space constraints in the system do not always permit the 40%–60% target; in that case, maximize the beam size on the detector within the available space, or use a diffusing element to spread the beam.

Without an F-Theta lens in the beam path, the beam can be enlarged to meet the 40%–60% rule. If the measurement must be taken after an F-Theta lens — whether due to space constraints or the purpose of the test — it is naturally very difficult to reach the 40%–60% aperture coverage.

## STEP 4 – LASER ON: HEAT UP YOUR LASER POWER DETECTOR (2 MINUTES)

Power detectors measure heat transfer, so any temperature difference between the detector and the ambient environment will degrade the measurement. The detector head is constantly exchanging heat with its surroundings, and the rate of that exchange is highest when the head is at a different temperature than the surrounding environment.

Heating up the detector eliminates this offset. Two minutes is more than enough.

If the measurement is taken after an F-Theta lens, the focused spot will be very small. Avoid exposing the power detector to the beam for an extended period — the high power density can damage the detector.

## STEP 5 – LASER OFF: BLOCK THE LASER BEAM (2 MINUTES)

Blocking the beam allows the head to reach thermal equilibrium. The thermal disc transfers heat to its casing, or via the fan or water cooling, at the same natural rate it would when the beam is on. Two minutes is sufficient, or one minute for heads rated at 30 W or less.

## STEP 6 – DO A "ZERO"

Use the zeroing function on the monitor to define the zero level. This is done with the laser off and the environment thermally stable.

## STEP 7 – LASER ON: ALLOW LASER POWER DETECTOR TO STABILIZE (1 MINUTE)

Stabilization is much faster on detectors with anticipation enabled — an accurate reading is available in 1 second or less. Anticipation is an electronic tuning that predicts the steady-state measurement value; it is reliable in most circumstances and drastically reduces the detector's rise time.

Otherwise, wait at least 1 minute — by that point the reading will be stable.

## Additional Notes

A common mistake involves the wavelength correction factor when operating at wavelengths other than 1064 nm. The detector's NIST-traceable sensitivity value is valid only for a 1064 nm laser. If the laser operates elsewhere within the detector's calibrated spectral range, the per-detector wavelength correction factor stored in the detector's memory chip must be applied. When a monitor is used with the detector, selecting the operating wavelength in the interface applies this correction automatically.

It is also worth verifying that the zeroing process was performed correctly. Room temperature can rise during laser warm-up, which would shift the zero. Repeated measurements should be consistent: the repeatability of the power meter is ±0.5%, so any session-to-session difference larger than this is a signal to investigate further — including whether the laser itself is genuinely stable over time.
