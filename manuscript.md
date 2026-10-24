# Travel mode and street geometry shape modelled melanopic daylight exposure on a tropical urban route

## Abstract

Daylight exposure during travel depends on street geometry, enclosure and journey duration, while the interpretation of dose differences also depends on the attribution convention. This computational study integrates these questions in a spectral model of a 4.97 km, five-section route inspired by Dhaka. Seven travel modes and six independent street interventions were evaluated for an 08:00 departure on 15 March 2026, using official CIE photopic and melanopic functions on a 5 nm grid. Mean travel-facing melanopic equivalent daylight illuminance ranged from 332.4 lx for a bus window seat to 8769.5 lx for walking; integrated doses ranged from 94.1 lx h for a car with aftermarket film to 9685.5 lx h for walking. Relative to the filmed car, walking had an exposure-rate ratio of 23.16 and a dose ratio of 102.95. For the filmed car, sequential decompositions assigned either 78.3% or 3.4% of the dose deficit to duration, depending on factor order; the symmetric two-factor Shapley share was 40.8%. Whitewashed façades increased walking dose by 65.9%, an 18 m height cap by 62.4%, a minimum street width of 18 m by 10.4%, and pale paving replacing asphalt by 5.1%. Foliage cover of 40% and 70% reduced dose by 34.5% and 60.0%. These deterministic comparisons use assumed geometry, materials and weather; direct beam reached the eye in 9 of 67 baseline walking steps. Reporting exposure rate, duration, viewing direction, decomposition convention and spectral provenance makes their interpretation explicit. The results do not establish physiological effects or measured inequalities among commuters.

Keywords: melanopic EDI; urban daylight; street canyon; travel mode; Shapley decomposition; spectral provenance

## Introduction

The light reaching a person’s eyes is a property of the whole optical path. A bright outdoor environment can be screened by a vehicle roof, filtered by glazing, or viewed through a narrow opening. Buildings and trees also change which parts of the sky and surrounding surfaces are visible. These relationships are familiar in architectural daylight design, but a journey adds a second dimension: travellers move through several environments and spend different amounts of time in each.

CIE S 026 provides a spectral metrology for describing optical radiation relevant to ipRGC-influenced responses, including melanopic equivalent daylight illuminance, abbreviated here as mEDI (CIE 2018a). It provides a common measurement language; an mEDI value by itself is not a prediction of a person’s biological response. Brown et al. (2022) recommend a daytime indoor light level expressed in this metric for healthy adults. In this study, their 250 lx value is used only as an exploratory reporting threshold. It is not converted into a daily dose requirement or a transport safety criterion.

Commuting has already been examined as a source of incidental daylight exposure (Lu, Hu and Davis 2021). We examine how a travel-mode comparison changes when the mean light level at the eye is separated from the duration over which exposure accumulates, and how independently defined street interventions affect the same route. The contribution is a reproducible computational comparison with explicit attribution rules, rather than a field estimate of commuters’ exposure.

A further issue concerns the comparison itself. Separating a dose gap into duration and exposure-rate components by changing one factor at a time gives different answers for the two possible orders. An undeclared order can therefore make a reporting convention appear to be a finding about transport or enclosure design. We apply the established Shapley averaging principle (Shapley 1952) to this two-factor product, report both sequential alternatives, and disclose the spectral inputs used for the final calculation. The decomposition is an accounting convention, not a new model of biological response.

The study has three questions. First, how do mean mEDI and integrated dose differ across seven assumed travel modes? Second, how much of each dose deficit relative to walking is assigned to duration and exposure rate, and how does that assignment depend on factor order? Third, what happens when building height, façade reflectance, street width, paving or foliage cover is changed individually? The StreetLux implementation, parameter files, complete result tables and plotting scripts are supplied so that these questions can be checked without access to a remote service.

## Methods

### Route and environmental inputs

The model contains five successive street types: a residential lane, a mixed-use collector, a wide arterial, an underpass and an office canyon. Their total length is 4970 m. The route is Dhaka-inspired rather than a surveyed reconstruction of the complete Mirpur–Motijheel journey. The place names in the input file are scenario labels; no GPS trace, measured building survey, traffic record or on-route light measurement accompanies the dataset.

The site coordinates are 23.8103° N and 90.4125° E, with local time UTC+6. All modes depart at 08:00 on 15 March 2026. Atmospheric assumptions are turbidity beta 0.34, turbidity alpha 1.2, ozone 0.26 cm, precipitable water 4.5 cm, pressure 1010 mb, cloud cover 0.15 and ground albedo 0.12. These define one synthetic morning, not a sampled climatic distribution. Each segment has an azimuth, two building heights, a street width, a lateral eye position and material spectra. Table 1 and Figure 1 describe the geometry.

{{fig:figure_1_street_sections|Figure 1. Architectural sections of the five modelled street types. Building heights and street widths are labelled explicitly; horizontal drawing scales vary between panels. The green band represents a probabilistic foliage layer, not resolved crowns. The grey band is the opaque underpass. Red points identify lateral eye locations. Arrows illustrate diffuse sky access, not simulated beam trajectories.}}

{{table:street_route}}

### Spectral and directional calculation

The model evaluates wavelengths from 380 to 780 nm at 5 nm intervals. The supplied official CIE photopic luminous-efficiency and α-opic action-spectrum tables are interpolated onto that grid (CIE 2018b; CIE 2019). The supplied extraterrestrial solar spectrum, labelled ASTM E490-00a in the archive, is used by the atmospheric model (ASTM International 2019). Its bundled conversion from micrometre to nanometre units is reproducible and its file digest is recorded, but this study does not independently authenticate that solar dataset against a new external download.

The calculation combines a spectral sky, canyon surface exchange and a directional enclosure filter. Each section is represented by parallel façades extending indefinitely along the street, with homogeneous surface properties within that section. A Fibonacci sphere samples 768 directions. Rays are classified as sky, left façade, right façade or ground, and the canyon solver estimates spectral reflected radiance. The eye-level quantity is irradiance on a vertical plane facing the declared heading. Foliage is represented by a horizontal statistical interception layer; the underpass uses the same layer mechanism with an opaque transmission spectrum and 85% cover. Vehicle bodies block directions outside their apertures; glazing filters the radiance admitted through each aperture. The material and glazing spectra are model assumptions, not laboratory measurements of vehicles or finishes sampled in Dhaka.

Solar position follows the NOAA algorithm. At the site and date, solar altitude rises from 24.6° (azimuth 104.3°, south-east) at 08:00 to 38.9° (azimuth 114.2°) at 09:06, the end of the walking trip. The direct beam enters the eye-level irradiance on a vertical plane through the cosine of its incidence angle. A step is counted as having a visible beam when the sun direction is unobstructed by the façades from the eye position; canopy attenuation is then applied to that beam. Solar altitude and azimuth were checked against an independent implementation (astral 3.2) for ten cases in both hemispheres, with azimuth agreeing to within 0.01°.

Melanopic irradiance is the wavelength integral of spectral irradiance at the eye multiplied by the melanopic action spectrum. Division by the fixed D65 conversion factor K = 0.0013262 W/lm produces mEDI. The time integral then gives the accumulated exposure:

{{eq:metrology}}

In Equation 1, Eλ is spectral irradiance at the eye, sₘₑₗ is the melanopic weighting function and K is the fixed D65 conversion factor. The time integral D is reported in lx h with time measured in hours. The term “dose” therefore denotes integrated modelled mEDI, without an assumed dose–response relationship. Photopic illuminance and the melanopic daylight efficacy ratio (DER), mEDI divided by photopic illuminance, are also retained. A lower DER means less melanopic-weighted exposure for a given photopic illuminance; it does not directly quantify a physiological response. Reported mean DER values are duration-weighted averages of the instantaneous ratios, not ratios of the two reported means. Mean mEDI is the integrated dose divided by total trip duration.

### Travel modes and timing

Walking is modelled at 4.5 km/h with an eye height of 1.55 m. A cycle rickshaw with its hood down travels at 9 km/h with an eye height of 1.35 m. The CNG auto-rickshaw uses 16 km/h and 1.25 m; the bus window seat uses 14 km/h and 1.60 m. The three car configurations use 20 km/h and 1.20 m. They differ in their window spectra: clear side and rear glazing, bronze side and rear glazing, or aftermarket film with a bronze windscreen. The first two car cases retain a laminated windscreen. Aperture azimuths and elevations are declared in the supplied enclosure module.

Each section’s traversal time follows from length and speed. Its number of samples is the nearest integer to traversal time divided by a nominal 60 s step, with at least one sample. The section duration is then divided evenly among those samples and evaluated at temporal midpoints. Thus, 60 s is a nominal resolution, not a claim that every integration interval is exactly one minute. Walking has 67 samples and a duration of 66.27 min. No congestion, acceleration, stops or dwell times are included.

The primary gaze follows each section’s travel azimuth. A separate sweep evaluates 24 fixed world headings, spaced by 15°. The heading spread is the ratio of the largest to the smallest trip-mean value among those fixed headings. It should not be confused with the ratio obtained by choosing a new best direction at every time step. Because the modes differ in speed and eye height as well as enclosure, their exposure-rate contrast does not isolate a causal glazing effect.

### Dose decomposition and the role of factor order

Let R and T denote a mode’s mean travel-facing mEDI and trip duration in hours, and let R₀ and T₀ denote the walking reference. Dose is RT. All six non-walking modes have lower R and shorter T, so their positive dose deficit is G = R₀T₀ − RT. Two exact sequential allocations are possible. In ordering A, duration changes first at the walking rate, then rate changes at the mode’s duration. In ordering B, rate changes first at the walking duration, then duration changes at the mode’s rate:

{{eq:sequential}}

Both pairs sum to G. Their duration contributions differ by (R₀ − R)(T₀ − T). This interaction is generally nonzero; neither sequence is established as a causal ordering by these data. The symmetric two-factor Shapley allocation averages the two sequences:

{{eq:symmetric}}

Each share is its symmetric contribution divided by G and expressed as a percentage; the two shares sum to 100%. This presentation uses positive deficit contributions; the numerical outputs record the equivalent signed differences from walking. Averaging removes dependence on which factor is changed first, but the attribution still depends on the selected reference and on representing dose as the product of these two factors. In particular, mean exposure rate includes enclosure, eye height and the clock times at which sections are reached. These are algebraic allocations, not experimentally identified effects of changing travel time or glazing.

### Independent street interventions

Six independent interventions are evaluated for walking. The minimum-width scenario sets each width to the larger of its original value and 18 m, retaining the original lateral eye offset from the centreline. It therefore leaves the 30 m arterial and 22 m underpass unchanged. The height scenario caps each façade height at 18 m. The façade scenario applies the whitewash spectrum to both canyon sides. Pale paving replaces asphalt only; the residential brick paving and existing concrete are retained. The two foliage scenarios set cover to 40% or 70% only on non-opaque sections, preserving canopy heights, materials and the concrete underpass. These definitions prevent interventions from accidentally changing unrelated features.

The comparisons are ranked by travel-facing dose. Since all street interventions retain walking speed and route length, their percentage dose changes equal their percentage changes in mean mEDI. The interventions are evaluated separately; the results do not describe combinations or interactions between design changes. The auxiliary Pareto set in the machine-readable output is not used to claim an urban planning optimum.

### Spectral provenance and calibration checks

The publication runner explicitly loads the bundled CIE photopic and α-opic tables and the supplied solar spectrum, checks the CIE file digests, and records the active data paths. It does not use the analytic action-spectrum fallback retained in the source for exploratory operation. The CIE files match the checksums in their official dataset metadata. The provenance record separately shows that no external daylight-basis component table was loaded; the D65 check uses the built-in daylight reconstruction. Thus, use of official action spectra should not be read as authentication of every spectral or optical assumption.

The numerically derived D65 conversion factor on the implemented grid is 0.0013264190 W/lm, differing from the fixed factor by 0.0165%; the computed D65 DER is 1.000165. The derived value is a diagnostic and does not replace K in Equation 1. This check establishes internal metrological consistency, not accuracy of the canyon optics against measurements or a reference renderer.

### Numerical verification and reporting

A fresh execution of the bundled reproduction workflow matched all 3367 numerical fields checked in the principal archived JSON outputs, using relative tolerance 10⁻⁹ and absolute tolerance 10⁻⁸. Runtime and local path fields were excluded by the supplied comparison routine. All eleven regression checks passed, including solar-position checks against an independent implementation and canyon-geometry checks (sun-side beam visibility, open-sky limit, monotonic occlusion and mirrored-street invariance). The sequential shares were computed from the saved mean rates and durations using Equations 2 and 3; their symmetric averages agree with the signed contributions in the numerical outputs. Reproduction is a check of the supplied numerical experiment, not external validation. No population sampling, confidence intervals or significance tests are implied by these deterministic scenario results.

## Results

### Exposure levels and accumulated dose

Walking produced the highest mean travel-facing mEDI (8769.5 lx) and trip dose (9685.5 lx h) (Table 2 and Figure 2). The bus window seat produced the lowest mean mEDI (332.4 lx), and the car with aftermarket film produced the lowest dose (94.1 lx h). Relative to the filmed car, mean exposure differed by a factor of 23.16 and dose by 102.95; relative to the bus window seat, the mean-exposure ratio was 26.38. The cycle rickshaw retained a relatively high mean exposure (5588.0 lx), but its shorter trip reduced accumulated dose to 3085.8 lx h. Mean exposure and dose ordered two pairs of modes differently. The bronze-glazed car had a higher mean mEDI than the CNG auto-rickshaw (1478.2 vs 1308.2 lx) but a lower dose (367.3 vs 406.4 lx h), and the car with film had a higher mean than the bus window seat (378.6 vs 332.4 lx) but a lower dose (94.1 vs 118.0 lx h). In both pairs the faster mode had the shorter trip. These changes in ordering are direct examples of why mean light level and accumulated exposure should both be reported.

{{table:street_modes}}

{{fig:figure_2_mode_exposure|Figure 2. Mean travel-facing mEDI and integrated trip dose for the same route and departure time. Bars show deterministic model outputs, not sample means from measured commuters. Different axis units distinguish exposure rate from accumulated exposure.}}

The fixed-heading spread was 2.65 for walking and 10.76 for the CNG enclosure. Bus and film-car spreads were 8.74 and 9.59, respectively. Directional apertures can therefore create large differences between the light received along different fixed views. In the walking calculation, the source accounting assigned 43.7% of travel-facing mEDI to sky, 22.4% to the two façades together, 5.2% to ground and 28.7% to direct solar irradiance at the eye. A direct beam was visible from the eye position in 9 of the 67 walking steps and in 2 of the 33 cycle-rickshaw steps, all in the final office-canyon section, whose axis (120°) lies close to the solar azimuth (about 113°). It was not visible in any motorised-vehicle run. The comparison therefore tests diffuse, reflected and filtered light for most of the route, with a direct-sun contribution that is specific to one section and to the morning geometry; the direct-sun path is not validated by these results. The bus window seat and the car with film were above 250 lx for 52.3% and 66.4% of the trip, respectively, and all other modes throughout.

### Duration attribution changes with the reporting convention

Under the symmetric allocation, duration accounted for 60.1% of the cycle-rickshaw dose deficit relative to walking, while exposure rate accounted for 39.9%. Duration shares were 49.0% for the clear-glazed car, 47.1% for the bronze-glazed car, 43.1% for the CNG, 40.8% for the filmed car and 35.6% for the bus (Table 3 and Figure 3). For the filmed car, the 9591.4 lx h deficit comprised 3915.2 lx h assigned to duration and 5676.2 lx h assigned to exposure rate. These terms were calculated before rounding; independently rounded displayed values may differ slightly from subtraction of the rounded doses in Table 2.

{{table:street_shares}}

{{fig:figure_3_dose_decomposition|Figure 3. Symmetric shares of the dose deficit relative to walking. The two shares sum to 100% for each mode. Exposure rate includes enclosure, eye height and the different clock times at which route sections are reached; the shares are not causal effects.}}

For the filmed car, changing duration first assigns 78.3% of the same deficit to duration, whereas changing rate first assigns 3.4%. The difference is 74.9 percentage points; averaging the two gives the 40.8% symmetric share. The corresponding sequential duration shares for the clear-glazed car are 81.3% and 16.8%, averaging to 49.0%. Across modes, the two orders differ by 26.6 to 74.9 percentage points. All six modes change from a majority-duration to a majority-rate account when the order is reversed; the cycle rickshaw is closest to the threshold (73.4% duration-first, 46.8% rate-first). The total dose deficit is unchanged in every case.

### Effects of individual street interventions

Whitewashed façades increased walking dose from 9685.5 to 16069.9 lx h, a 65.9% increase. Capping façade heights at 18 m increased dose by 62.4%. Enforcing a minimum street width of 18 m increased it by 10.4%, and replacing asphalt with pale concrete increased it by 5.1%. Foliage cover of 40% and 70% reduced dose by 34.5% and 60.0%, respectively. The height cap also changed solar access: it increased the number of walking steps with a visible direct beam from 9 to 42 of 67, and direct sun supplied 35.6% of its walking mEDI, compared with 28.7% at baseline. Its effect therefore combines greater sky and sun access, whereas the whitewash effect arises mainly through the reflected component. Table 4 reports the results rounded for display, and Figure 4 makes the directions of change visible.

{{table:street_designs}}

{{fig:figure_4_design_changes|Figure 4. Separate intervention effects on walking dose. The opaque underpass is preserved in both foliage scenarios. Width changes impose a minimum rather than replacing every width with 18 m. These effects describe melanopic exposure alone; they do not measure thermal comfort, visual comfort or ecological benefit.}}

## Discussion

### Exposure accounting and design interpretation

The largest practical consequence for reporting is the difference between exposure-rate and dose comparisons. A high dose ratio can arise partly because one traveller spends much longer outdoors. Dose remains useful as an accounting quantity, but interpreting it requires the trip duration and the time profile of exposure. In this route, the two metrics order two pairs of modes differently: the bronze-glazed car and the CNG auto-rickshaw, and the filmed car and the bus window seat. A design report that publishes only a single dose ranking would hide this distinction.

The sequential comparison adds a second reporting requirement. In the filmed-car example, the same data can yield either a 78.3% or a 3.4% duration share. A report could consequently direct attention towards trip duration or towards enclosure design merely by leaving its chosen order unstated. The symmetric allocation removes this avoidable order effect and, here, gives a majority exposure-rate share for the filmed car and a majority duration share for the cycle rickshaw. It does not identify the best intervention. In particular, the duration attribution is not a recommendation to lengthen a journey, and a rate attribution is not a measured effect of replacing glazing. Testing either intervention requires its own counterfactual while controlling the other relevant inputs.

Two modes are close to an even split under the symmetric convention: 49.0% duration and 51.0% rate for the clear-glazed car, and 47.1% and 52.9% for the bronze-glazed car. Such small majorities should not be turned into a categorical design priority, especially without parameter uncertainty or a full convergence analysis. The useful reporting unit is the pair of contributions alongside the underlying rates, durations and total deficit.

### Architectural interpretation of the street interventions

The street interventions also suggest an architectural reading. In the baseline walking run, façades supply 22.4% of mEDI, direct sun 28.7% and sky 43.7%, yet changing façade spectra raises walking dose by 65.9%. This result is consistent with the mechanism represented by the solver, but the magnitude is conditional on its diffuse surface assumptions and selected material curves. The whitewash result is not a proposal to treat all real façades alike. Specular reflections, maintenance, soiling, façade access and glare would need separate consideration before a material policy could follow from the model.

Likewise, a lower mEDI value under foliage is not evidence that trees are undesirable. Shade may serve thermal comfort and other objectives absent from this calculation. The useful outcome is to make the optical trade-off explicit and to identify when a broader design assessment is needed. Each intervention preserves unrelated structures and materials so that its optical effect remains interpretable; both foliage scenarios therefore retain the opaque underpass.

### Limitations and validation needs

The spectral calibration check and reproducible tables strengthen numerical traceability, but several uncertainties remain. The route and enclosure geometries are assumed. The atmospheric model is not driven by a measured weather series. All modes occupy the same lateral route positions, which is a deliberate comparison rule rather than a traffic-lane model. The foliage layer does not resolve individual crowns or scattering paths. Finite directional sampling can affect small apertures and high-contrast fields; only a limited convergence check is supplied (verification/convergence_check.py): increasing the sampled directions from 768 to 12288 changed mean travel-facing mEDI by +1.5% for walking, +1.7% for the CNG auto-rickshaw and +5.7% for the filmed car, so the reported ratios carry an angular uncertainty of that order, whereas shortening the time step from 60 s to 15 s made no measurable difference. There is no matching Radiance comparison or field measurement in this study’s source archive. A direct beam reached the eye in 9 of 67 walking steps and 2 of 33 cycle-rickshaw steps, all in the office-canyon section where the street axis lies close to the solar azimuth, and in no motorised-vehicle step. Direct sun is therefore a geometry-specific part of the baseline comparison (28.7% of walking mEDI) that depends on departure time, cloud cover and street side; the direct-sun path is not validated against a reference renderer or measurements. A finite set of idealised sections also omits junctions, street ends, detailed vehicle interiors and within-section variations in geometry. Validation obtained for another model or scene would not establish accuracy for these route calculations.

Further work should pair time-resolved spectral measurements with surveyed sections and vehicle apertures, repeat the comparison across departure times and seasons, and test angular convergence. Validation should compare both absolute mEDI and the ordering of design effects. Physiological interpretation would additionally require a study of people with appropriate exposure history and response measurements. Those are separate questions from whether the supplied numerical experiment reproduces. Dose equivalence across repeated trips would be an arithmetic equality only: these calculations do not establish biological equivalence across times of day, repeated days or different exposure histories.

## Conclusions

For the declared tropical morning scenario, the walking-to-film-car exposure-rate ratio was 23.16 and the dose ratio was 102.95. Shorter duration contributed substantially to the larger dose contrast, but its numerical share depended on the attribution convention: the filmed-car duration share was 78.3% or 3.4% under the two sequential orders and 40.8% under their symmetric average. The comparison therefore requires both exposure accounting and disclosure of how the gap is allocated.

Street geometry and surface assumptions also produced substantial within-model differences. Façade whitewashing produced the largest increase in walking dose (65.9%), followed closely by the 18 m height cap (62.4%), which also increased direct-sun access along the route. The minimum-width intervention increased walking dose by 10.4%, and both foliage scenarios reduced the melanopic quantity evaluated here. These outcomes do not establish overall design merit, measured exposure inequalities or health effects. A reproducible report should identify the exposure rate, duration, viewing direction, intervention definition, decomposition rule and spectral calibration chain. Symmetric attribution removes factor-order dependence, not dependence on the allocation convention; transparent provenance and external validation remain necessary for interpreting the model itself.

## Data and code availability

The accompanying StreetLux reproducibility package contains the model source, input geometry, reference tables and their digests, JSON and CSV results, regression checks, plotting code and editable manuscript source. Running reproduce.py regenerates the numerical analyses, all four figures and the sequential and symmetric decomposition data used in Table 3, and compares the principal numerical outputs with the saved study results. The decomposition uses the rates and durations in modes.json and requires no additional simulations. Running authoring/build_manuscript.py rebuilds the Word manuscript from manuscript.md, the computed tables, figures and native equation source. The numerical experiments require no external account or model API. The model version is 0.2.1. A separate script, verification/convergence_check.py, repeats three baseline mode runs at higher angular resolution and a shorter time step.

## Declarations

Ethics and consent: this study uses a computational model and contains no participant measurements.

Author information and declarations: [Complete the final author list, affiliations, corresponding email, author contributions, funding and competing-interest statements before submission.]

AI assistance: OpenAI ChatGPT with Codex was used for source inspection and correction, reproducibility and arithmetic checks, manuscript drafting and editing, reference checks, formatting and figure-script preparation. The figures were produced deterministically from plotting code and model outputs. The author or authors remain responsible for verifying the analysis, interpretation, citations and final text.

## References

ASTM International. 2019. Standard Solar Constant and Zero Air Mass Solar Spectral Irradiance Tables. ASTM E490-00a(2019). West Conshohocken, PA: ASTM International. https://doi.org/10.1520/E0490-00AR19.

Brown TM, Brainard GC, Cajochen C, Czeisler CA, Hanifin JP, Lockley SW, Lucas RJ, Münch M, O’Hagan JB, Peirson SN, Price LLA, Roenneberg T, Schlangen LJM, Skene DJ, Spitschan M, Vetter C, Zee PC, Wright KP Jr. 2022. Recommendations for daytime, evening, and nighttime indoor light exposure to best support physiology, sleep, and wakefulness in healthy adults. PLOS Biology 20(3):e3001571. https://doi.org/10.1371/journal.pbio.3001571.

CIE. 2018a. CIE System for Metrology of Optical Radiation for ipRGC-Influenced Responses to Light. CIE S 026/E:2018. Vienna: International Commission on Illumination. https://doi.org/10.25039/S026.2018.

CIE. 2018b. CIE alpha-opic action spectra [dataset]. https://doi.org/10.25039/CIE.DS.vqqhzp5a.

CIE. 2019. CIE spectral luminous efficiency for photopic vision [dataset]. https://doi.org/10.25039/CIE.DS.dktna2s3.

Lu Y, Hu W, Davis W. 2021. The calculated circadian effects of light exposure from commuting. Applied Sciences 11(24):11846. https://doi.org/10.3390/app112411846.


Shapley LS. 1952. A Value for N-Person Games. RAND Paper P-295. Santa Monica, CA: RAND Corporation. https://doi.org/10.7249/P0295.
