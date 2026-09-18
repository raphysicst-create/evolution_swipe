# Presentation iterations

The gameplay baseline and regression contract were recorded first in GAMEPLAY_INVARIANTS.md. The implementer does not score their own work; independent scores and evidence are recorded in EVALUATION.md.

## Iteration 1

- PLAN: Embed replacements for the three existing CDN presentation resources, introduce the reference charcoal/cream/mint/peach palette and a layered paper card. Preserve every game script byte and DOM target.
- IMPLEMENT: Inline utility rules and small SVG icon masks, system Korean font stack, paper/card/panel CSS. No game code changed and no new runtime dependency.
- EVALUATE: Independent score 74/100 (30/12/10/9/13); no hard fail. Script/DOM/seed/offline/touch regressions pass.
- DECISION: Proceed with dominant creature art and a composed desktop layout. Address small screen wrapping and sparse card interior.

## Iteration 2

- PLAN: Add icon-driven creature art, reference wordmark/scenic vignette, scenario-first paper composition and clear noninteractive desktop field guide.
- IMPLEMENT: Eleven lightweight SVG creatures including a generic fallback; original mockup embedded logo and scenic image; CSS/markup only. Retain original drag badges and controls.
- EVALUATE: Independent score 84/100 (30/20/12/10/12); hard fails 0. Normal roulette order/angle/timing and offline regression pass. One noisy 81 ms startup sample requires isolated follow-up.
- DECISION: Revise the leftover opaque habitat oval, result/tutorial surfaces and fly-out overflow.

## Iteration 3

- PLAN: Uncover the illustrated habitat, contain fly-out paint, and unify roulette, result, ending and tutorial surfaces. Keep existing timers/inputs unchanged.
- IMPLEMENT: CSS-only scene correction, container clipping, direction stamps, journal modal/ring/CTA treatments, opaque tutorial stage and matching wordmark.
- EVALUATE: Independent 90/100 (30/21/13/12/14), hard fails 0. All regressions pass. Both body/document overflow corrected. Isolated roulette p95 16.7–16.8 ms; small first-overlay paint tasks remain for follow-up.
- DECISION: Continue to satisfy five iterations and cover the complete tutorial/tree/tools/stage/ending presentation.

## Iteration 4

- PLAN: Improve touch targets, names for icon-only controls, short-screen tutorial scrolling, diagram/tool readability, and icon-driven terrestrial habitats. Review every stage and ending/checkpoint presentation.
- IMPLEMENT: Inline CSS, accessible markup, larger existing controls, flex-safe scroll area for tutorial, field grid diagram, foliage scene selected only by existing icon classes; opaque modal backdrop to reduce blending cost.
- EVALUATE: Independent 91/100 (30/22/13/12/14), hard fails 0. All ten icon-driven creatures and generic fallback render; offline/gameplay/touch checks pass.
- DECISION: Fix 320 px tutorial strip wrapping, practice illustration contrast and flex-compressed ending badge; verify modal scrolling and controlled performance comparison.

## Iteration 5

- PLAN: Address the evaluator's remaining small-screen defects, add restrained static paper texture, and complete standalone/performance/regression acceptance.
- IMPLEMENT: Two-line small tutorial strip, illustrated practice card, non-shrinking ending/result content, CSS-only background scroll containment, consistent wheel font and tiny static SVG paper grain. No production JavaScript was added or modified.
- EVALUATE: Independent final 93/100 (30/23/14/12/14), hard fails 0. Fresh full screenshots, final gameplay/offline/short-screen audit and twenty-sample styled-original comparison accepted. Final source is 196,086 bytes, SHA-256 86f4edbae14dd729ec7b6c8be8abfa7f7845ef24f3d33edd320001f8d952c026.
- DECISION: Complete. All five independent iterations are recorded, gameplay is 30/30 and no hard fail occurred. Performance improved overall; the small simulated 4× CPU first-overlay cost and occasional throttled spikes remain explicitly documented.
