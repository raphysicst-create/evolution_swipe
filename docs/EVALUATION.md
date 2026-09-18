# Independent presentation evaluation

Evaluator: separate agent `/root/visual_evaluator`. This agent does not edit game code. Scores below are based on rendered evidence, source inspection, and separately produced regression evidence, not the implementer's description.

## Reference and scoring method

Reference files inspected: `EVO_SWIPE_2D_desktop.png`, `EVO_SWIPE_2D_mobile.png`, and `EVO_SWIPE_2D_mockup.html`. The reference contributes its charcoal ground, warm cream paper, muted peach/mint/teal/rose palette, softly irregular contours, creature illustration, rounded layered panels, restrained secondary text, and large readable Korean headings. Its demo mechanics and dashboard layout are not a gameplay specification.

The original `index.html` source was read before implementation. It has a centered swipe card, hidden-until-drag choices, a three-outcome environment roulette, population feedback, endings/checkpoints, tree, classroom tools, and tutorial. The reference image cannot justify replacing this structure.

| Category | Maximum | Evidence required |
| --- | ---: | --- |
| A. Gameplay preservation | 30 | Independent frozen-script/DOM/data checks and deterministic differential regression; input/modal behavior in browser |
| B. Art direction | 25 | Actual desktop/mobile rendering compared with supplied images |
| C. Visual hierarchy | 15 | Scenario, species, population, drag labels, roulette/result/continue and ancillary screens readable at relevant sizes |
| D. Game feel | 15 | Swipe/return/roulette/result states observed, with original timing and choice access retained |
| E. Performance | 15 | Self-contained loading, no external requests/dependencies, measured or observed browser operation, transform/opacity-first motion |

A score of 90 alone does not pass: A must be 30, there must be no hard fail, and at least five independent iterations must be evaluated. Lack of evidence is not a pass. A hard fail requires rollback and a revised plan.

## Baseline observations

- Original source uses three remote dependencies: Tailwind CDN, Font Awesome CDN, and Pretendard CDN. The final offline condition therefore requires self-contained equivalent styling and icon presentation while preserving the actual game script.
- Original visuals use cool slate panels and small symbolic icons. This is a substantial distance from the reference's cream illustrated story-card treatment.
- Swipe choices intentionally appear only during dragging: 12 px reveal threshold, 60 px full opacity, 80 px selection threshold. Their original DOM targets and input route must remain intact.
- Original fly/roulette/result timings are fixed by the engine and must not be changed as visual polish.

No baseline numeric score has been assigned without a rendered baseline.

## Iteration 1 — 74/100, continue

| A /30 | B /25 | C /15 | D /15 | E /15 | Hard fails |
| ---: | ---: | ---: | ---: | ---: | --- |
| 30 | 12 | 10 | 9 | 13 | 0 detected |

Evidence inspected: `qa/captures/iteration-1/` game, drag, result, tutorial, tree and data desktop PNGs; mobile game/drag and 320 px game/result/tutorial PNGs; saved iteration HTML; `qa/results-iteration-1.json`. Frozen game-script hash is unchanged (`9c3811e53c153c817b7398d8bdf26b62053e8b17adb402fcdc4149c1c0d72107`); differential states match across 360 transactions and 64 seeded routes. The auditor's actual pointer/touch tests pass. Candidate loads offline with no network request or JS error.

The charcoal/cream/peach/mint palette and layered paper border now resemble the reference. However, the card still contains a small generic worm symbol surrounded by a large blank region; there is not yet a creature illustration, scene or strong art identity. The desktop header and card are separated by a large empty gap. At 320 px the logo subtitle and tree control wrap awkwardly; the mobile drag label splits a Korean final syllable onto its own line. Tutorial copy is readable but the game card's underlying text remains visible behind it. Roulette/results lack a cohesive enclosing surface.

The result screenshots have full-page widths larger than the viewport after card fly-out (desktop 2725 px and small 763 px); this is a visual overflow issue to investigate, not evidence of broken gameplay. No new operational hard fail has been detected in the supplied interaction evidence. Game-feel score is limited because this iteration largely changes surfaces and the evaluator has reviewed static interaction-state captures. The capture script uses ordinary motion and waits for the actual final reveal; the first regression harness separately uses reduced motion. Performance earns 13: self-contained 103,052-byte HTML, no dependencies, successful input, and measured 70.9 ms candidate load; a normal-motion frame trace remains pending. These timing samples are not a controlled device benchmark.

Decision: quality threshold not met. Next iteration should introduce distinctive lightweight creature/landscape art, strengthen desktop composition, prevent awkward Korean wrapping, and then address modal readability and normal-motion evidence.

## Iteration 2 — 84/100, continue

| A /30 | B /25 | C /15 | D /15 | E /15 | Hard fails |
| ---: | ---: | ---: | ---: | ---: | --- |
| 30 | 20 | 12 | 10 | 12 | 0 detected |

Evidence inspected: iteration-2 saved HTML and actual desktop/mobile/320 px game, mobile drag, desktop/320 px result and 320 px tutorial screenshots; `qa/results-iteration-2.json`; `qa/overflow-iteration-2.json`. The saved HTML hash matches the audited candidate (`b86e1a7cf8a16b4ec351e9fcc0eeeaf51c0a0db4de1779cae0a1ecf1a28597b7`). All original-versus-candidate checks pass, including normal roulette event order/alignment and real mobile input. No runtime requests or errors.

The supplied logo, scenic side vignette, spacious centered paper card, hand-drawn creature and quieter field-guide panel now establish a coherent reference-derived identity. The mobile order of scenario → creature → possible environments is clear. The small header and choice-label wrapping from iteration 1 are improved. However, an inherited opaque pale oval covers most of the new landscape, visibly separating the creature from its environment. Tutorial and result overlays still show distracting game content underneath; result surfaces remain less developed than the main card.

The result capture remains wider than its viewport (desktop 2785 px); the separate overflow probe shows the document itself is viewport-wide and controls are usable, but `body.scrollWidth` still includes the flying card. Therefore this is not a mobile-operation hard fail, but it is unfinished presentation containment. Short-screen continue is below the initial viewport but scrolls into view and remains clickable.

The 177,378-byte standalone page has no extra runtime dependency. Normal-motion p95 is 16.8 ms, matching the baseline sample, but one 81 ms long task produced an 83.3 ms maximum frame versus 33.3 ms original. This is insufficient to infer a systemic regression, yet prevents a strong performance score until an isolated follow-up measurement. Static state screenshots plus preserved normal-motion timing support the game-feel score; a full smoothness judgment is still limited.

Decision: quality threshold not met. Remove the pale oval; integrate creature and habitat; strengthen result, ending and tutorial surfaces; contain fly-out overflow; then collect another normal-motion trace. Do not alter the frozen roulette times.

## Iteration 3 — 90/100, continue to required iteration count

| A /30 | B /25 | C /15 | D /15 | E /15 | Hard fails |
| ---: | ---: | ---: | ---: | ---: | --- |
| 30 | 21 | 13 | 12 | 14 | 0 detected |

Evidence inspected: iteration-3 desktop/mobile/320 px game, mobile drag, desktop/320 px result, 320 px tutorial; saved HTML matches audited SHA `31067ff5e2b3aeb58f5debd87e838698d1753bebc1bdf1501e2ce72b437a5953`; `qa/results-iteration-3.json` and new presentation rules. The frozen script, original DOM, gameplay differentials, offline execution and actual mouse/touch progression pass. Both document and body widths now equal the viewport after fly-out; the rendered result images confirm the fix.

The creature now sits directly within the landscape. Paper inset lines and slightly irregular edges support the field-journal style. The framed roulette/result panel establishes a clear trait → environment → outcome → continue sequence, including at 320 px. The opaque tutorial treatment eliminates text showing through. Direction arrows make the swipe badges clearer without changing their reveal thresholds. The illustrated landscape remains more geometrically flat than the supplied painterly reference, limiting art score; ancillary controls and later tutorial screens still need the same careful review as the main card.

Three isolated normal-motion traces report p95 16.7–16.8 ms, with no recurring frame gap during the 2.5-second spin. Two runs contain a 56 ms initialization task just after opening the overlay; one does not. This supports smooth ongoing animation but leaves minor first-paint headroom. The page is 185,037 bytes, uses no new library, loads with zero network requests, and keeps the original motion schedule. Tests describe this machine rather than every low-end tablet.

Decision: numeric threshold reached, but only three iterations have been completed. Continue with touch targets/accessibility, full tutorial and ancillary-screen readability, and actual rendered coverage of every icon-driven creature plus long titles, endings and checkpoints. The initial overlay paint should also be simplified where possible.

## Iteration 4 — 91/100, continue to final polish

| A /30 | B /25 | C /15 | D /15 | E /15 | Hard fails |
| ---: | ---: | ---: | ---: | ---: | --- |
| 30 | 22 | 13 | 12 | 14 | 0 detected |

Evidence inspected: iteration-4 normal captures, actual 10-stage gallery, unknown-icon fallback, all five 320×568 tutorial steps, short-screen long title/ending/tools/tree, landscape practice/ending, tablet tutorial/ending, `extended.json`, presentation selectors, and `qa/results-iteration-4.json`. Saved candidate hash equals the audited hash `fb29ee6bea8219f951dc406ce27d58b498f3ad0506c51a96d6cd77c57ef07680`. The full gameplay/DOM/offline regression suite passes again. Extended execution also completes tutorial practice and checkpoint continuation.

All ten existing stage icons produce distinct, consistently drawn creatures. Terrestrial icon metadata selects a land scene, while aquatic forms retain water; the generic future-icon fallback visibly renders. No individual stage-name branch was added to presentation. Main long titles remain readable. Tools, tree and result panels now share the same visual family and larger controls. The fully opaque result backdrop further improves focus.

Remaining small-screen flaws are concrete: the tutorial's three-part left/right explanation splits Korean words into isolated syllables at 320 px; the practice worm icon is pale green against a pale green ground; the ending badge visibly compresses into an oval in short windows. Landscape panels require inner scrolling, and the tested practice/checkpoint controls remain operable. Content appearing below the 568/390-pixel viewport in full-page screenshots is outside the fixed overlay's actual viewport, not a gameplay failure.

The standalone page is 191,186 bytes. Three traces again maintain 16.7–16.8 ms p95 with no repeated gap during spin; 52/62/56 ms tasks occur only in initial overlay setup. This is acceptable observed ongoing responsiveness with a documented first-paint limitation, not evidence of equivalence on all devices. A fair fully styled original comparison remains desirable for the final performance claim.

Decision: fourth iteration is functionally sound and above the numeric threshold. Complete the fifth iteration by fixing the tutorial strip and practice contrast, preventing ending-child compression, preserving panel scrolling if background scrolling is locked, and applying restrained final paper texture. Verify these exact small-screen states and rerun independent parity/performance checks.

## Iteration 5 — 93/100, accepted

| A /30 | B /25 | C /15 | D /15 | E /15 | Hard fails |
| ---: | ---: | ---: | ---: | ---: | --- |
| 30 | 23 | 14 | 12 | 14 | 0 detected |

Evidence inspected: final iteration-5 desktop/mobile/320 px game and result captures, refreshed 320×568 tutorial explanation/practice/ending, landscape practice/ending, all-stage gallery, final saved HTML, `qa/results-iteration-5.json`, extended capture script and report, and the 20-sample `qa/performance-final.json`. Also viewed the fully styled original `qa/captures/baseline-desktop.png` for direct comparison. Final capture, production file, regression audit and performance report share SHA `86f4edbae14dd729ec7b6c8be8abfa7f7845ef24f3d33edd320001f8d952c026`.

The final small tutorial strip keeps each directional label intact and moves its explanation below them. Practice now uses a recognizable miniature creature. The ending badge retains its shape; short-panel content scrolls rather than compressing. Actual tutorial completion and checkpoint continuation still succeed at 320×568 and 844×390 after background scroll containment. Subtle paper grain adds reference character without obscuring Korean text. The visual system is consistent across gameplay, results, endings, tools and teaching screens. The artwork is intentionally simpler and more geometric than the supplied raster reference, and ancillary copy remains compact, so the art/hierarchy scores are not perfect.

Gameplay preservation remains 30: every byte of the 46,376-byte frozen game script and the complete legacy file is unchanged; all 71 original IDs/tags and data hooks survive; 360 payoff transactions, 64 seeded routes, RNG outputs, state/log/export comparisons and actual desktop/mobile input pass. No new JavaScript, framework or runtime file is required. The 196,086-byte HTML runs with zero external requests and zero JavaScript errors. Art follows existing icon metadata and has a tested unknown-icon fallback.

The fair performance comparison replays the original's complete captured CDN styling/icons/fonts from a temporary cache and measures five runs per page at ordinary and simulated 4× CPU cost. It does not compare against an unstyled original. The benchmark verified original resource completeness and stable final file bytes.

| Median metric | Styled original, 1× | Final, 1× | Styled original, 4× | Final, 4× |
| --- | ---: | ---: | ---: | ---: |
| Ready (ms) | 1767 | 315 | 4612 | 1382 |
| Steady roulette p95 frame interval (ms) | 116.7 | 16.8 | 133.4 | 16.8 |
| Drag p95 frame interval (ms) | 33.4 | 16.8 | 33.4 | 16.7 |
| First overlay frame callback (ms) | 83.5 | 56.4 | 257.8 | 277.7 |

Ongoing animation/input and loading improve materially in this measured environment. The simulated 4× first-overlay callback is about 20 ms slower in the final median, with substantial run-to-run variation; this is explicitly retained as first-paint headroom and accounts for the remaining performance point. It is not evidence of a recurring swipe/roulette stall or a perceptible loading regression. These headless Chromium results do not certify every physical low-end device. Game-feel judgment combines independently inspected interaction-state captures, unchanged event timings, actual input tests and measured animation traces; it is not a claim of manual video-playback review.

Decision: accepted. Five independent iterations are documented, the last score is 93, gameplay is 30/30, and no hard-fail condition was detected. The game remains single-file/offline and the final presentation uses the supplied reference direction without importing the reference's demo mechanics.

## Score summary

| Iteration | A | B | C | D | E | Total | Hard fails | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 30 | 12 | 10 | 9 | 13 | 74 | 0 | Revise art/composition |
| 2 | 30 | 20 | 12 | 10 | 12 | 84 | 0 | Revise habitat/modals/overflow |
| 3 | 30 | 21 | 13 | 12 | 14 | 90 | 0 | Continue required iterations and coverage |
| 4 | 30 | 22 | 13 | 12 | 14 | 91 | 0 | Fix small-screen details |
| 5 | 30 | 23 | 14 | 12 | 14 | 93 | 0 | Accepted |
