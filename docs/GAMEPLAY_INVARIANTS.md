# GAMEPLAY INVARIANTS

Recorded from the unedited `index.html` and `evolution_swipe.html` on 2026-09-19, before presentation implementation. These are regression requirements, not proposals to redesign the game.

## Baseline and file roles

- `index.html` is the current, complete, single-file environment-roulette game: seeded trait × environment outcomes, population, discovered-branch diagram, checkpoints, lesson-data exports, and five-step tutorial.
- `evolution_swipe.html` is a distinct older deterministic branch game, not an interchangeable entry point. It uses `EVOLUTION_TREE`, left/right destination IDs and the persistent `evo_unlocked_endings` key. Preserve this file byte for byte; do not transplant its game into `index.html`.
- Byte-exact originals are preserved outside the repository at `C:\Users\22\AppData\Local\Temp\evo-swipe-presentation-baseline-20260919`.
- Original SHA-256: index `f7b9e3ff9b8d23ef5b1ed9cb04894076e47a6359800e29b942fca2dc161ce921`; legacy `66fd0cc18f56f43934da83d9a8da30dab8766d77d5d9b8cf53cfbfeb7de273ec`.
- Freeze the entire final inline game script of index byte for byte, including rendering, data, event wiring, timers and functions. Presentation belongs in inline CSS, decorative markup and separate read-only presentation script if required. Keep the document runnable as one file with no build step.
- Original index loads Tailwind, Font Awesome and Pretendard through three network dependencies. They are baseline limitations, not new hard failures caused by this work. Final offline support must embed replacements in index without changing the frozen game script or creating new runtime dependencies.

## State, data and RNG

- Initial state: `node='pikaia'`, `pending=null`, empty `path` and `log`, `locked=false`, `pop=100`, `MAXPOP=120`, reached contains only pikaia, and `seen`/`runEdges` are empty.
- Data is the unmodified `ENV`, `END`, `TREE`, `VERDICT`, `HEX`, `POPD`. Keep every key, label, icon, era, scenario, environment list and its order, trait, payoff verdict/destination/note, and optional population delta.
- Ten playable nodes: pikaia, placoderm, jawed_fish, tiktaalik, amphibian, amniote, synapsid, mammal, diapsid, dinosaur. Fifteen environments; seventeen endings (six extinction, eleven survival). These counts describe the baseline, not constants for presentation logic.
- RNG is exact Mulberry32. URL seed parsing is `parseInt(params.get('seed')) || Math.floor(Math.random()*100000)`; URL zero and invalid seed therefore use a random initial seed. Preserve this existing behavior.
- Each choice calls RNG exactly once: `envs[Math.floor(rng()*envs.length)]`. Wheel animation consumes no randomness. Presentation must neither call the game RNG nor reset/advance seed state.
- Seed application accepts all parseable integers, including zero/negative; rejects NaN with existing message. It resets rng from seed and starts pikaia at 100 with empty path/runEdges. It does not clear log, seen or reached. It closes endModal, not dataModal.

## Turn order and outcomes

1. Accepted left/right input enters `fly(side)`, checks locked, sets locked, clears gesture state/badges, applies fly-out transform and opacity.
2. After exactly 260 ms it invokes `choose(side)`. L selects TREE[node].L; other side selects R.
3. Choose draws environment, resolves that trait's payoff, assigns pending; records seen (`node|trait|environment`) and current-run edge (`node|trait|destination`); appends one log row; calls showEvent. A missing payoff preserves the existing console error and same-node render path.
4. Population and next node do not change until `proceed()`. The continue control and Enter/Space invoke the same handler. Preserve the ability to continue before the visual reveal completes.
5. Proceed clears roulette timers, closes eventModal, appends exactly one path description. `perish` sets population to zero and immediately shows the payoff ending. Otherwise update `Math.min(120, pop + (cell.dp !== undefined ? cell.dp : POPD[cell.v]))`.
6. Default deltas: thrive +25, survive -20, perish -999 (perish has its dedicated zero path). Pikaia's armor/anoxia and agility/sea_level_drop override survive to -45. Do not add a zero lower clamp to internal population.
7. After non-perish update, `pop<=0` selects ext_collapse before normal destination routing. Otherwise TREE destination renders the next node; END destination shows that ending. Existing updateEdgeCount call ordering remains unchanged.
- Render updates existing era/title/scenario/icon/choice badges/environment previews, records reached node, resets card and unlocks input, then renders population and edge count.
- Population display rounds and clamps below zero. Bar clamps into [0,100%] relative to MAXPOP. Existing colors have thresholds >60, >30, otherwise red.

## Input and modal contract

- Single pointer event path on `swipeCard`: pointerdown requires primary button and unlocked state; captures one pointer. Moves from the matching pointer apply translateX and rotation d*0.07 degrees. Cancel resets without choosing.
- Badges appear beyond 12 pixels and reach full opacity at 60. A completed move must be strictly less than -80 for L or strictly greater than +80 for R. Exactly +/-80 cancels. This applies identically to tutorial practice.
- ArrowLeft/ArrowRight call fly while the game is available. Modal priority is tutorial, event, ending, tree/data, game. Tutorial blocks game shortcuts. Event Enter/Space proceeds; ending Enter restarts; tree/data Escape closes the open diagram/data dialog.
- Keep all existing IDs, data-step values 0 through 4, `.tut-step` nodes and their order, `.wtxt` wheel-label hooks, generated diagram markup, button/input/select tags and targets. Original listeners and onclick assignments remain in the frozen script.
- `hidden`/`flex` classes and explicit inline style display must continue controlling overlays/tutorial screens. Decorative layers cannot intercept pointer input. Card animation must respect the script's inline transform and opacity.

## Roulette

- The environment is selected before roulette opens. Wheel shows every `envs` entry in order, with payoff-specific verdict colors.
- Constants remain WH_C=120, WH_R=104, WH_SPIN=2500 and cubic-bezier(.22,1,.36,1). Rotation accumulates four full turns plus deterministic alignment and +/-16%-segment drift; selected wedge stops at the pointer. Counterrotation keeps label text upright.
- Normal timing: spin at 220 ms; winning environment at 2780 ms; verdict at 3240 ms. Existing reduced-motion branch uses 0, 160, 360 ms. A later presentation style may reduce visual motion but cannot alter these timer/state transitions.
- Existing timers clear before a new wheel and on proceed. Preserve generated `wseg{index}`/`wlab{index}` IDs and all labels.

## Endings, checkpoints, diagram

- Ending metadata/tag comes from END. Ending path retains turn order and final displayed population. Checkpoint menu follows reached-set insertion order, excluding pikaia, with existing title/era labels.
- Full restart: 100 population, clear path and current-run edges, render pikaia. Checkpoint restart: selected reached node and 50 population, same clears. Neither resets RNG nor clears log/reached/seen. Preserve this distinction from applying a seed.
- `ALL_EDGES` deduplicates node|trait|destination from all payoffs. `foundEdges` derives discovered edges from seen node|trait|environment tuples. Multiple environments sharing destination collapse into one branch; current-run edges receive separate visual emphasis.
- Diagram only lays out discovered reachable branches, with original node/ending vertex IDs, title, icon, tags, focus and captions. Preserve pan, wheel zoom, pinch zoom, +/- zoom and fit controls and bounds .15 to 3. Presentation must not create additional discoveries.

## Tutorial, persistence and data exports

- Index initializes by `render('pikaia')` then `tutOpen()`. Five tutorial sections retain existing navigation order and final practice gate; a successful practice unlocks final next button. Skip/Escape closes without requiring practice.
- Tutorial uses separate gesture state and DOM and must never change game pop/path/log/seen/reached/rng. Reopening starts at tutorial step zero; existing tutPassed behavior is preserved.
- Current index has NO localStorage read/write or save/load schema. Do not invent persistence. All current run/discovery/log state is session memory. The legacy file alone persists unlocked ending IDs as a JSON array at `evo_unlocked_endings`.
- Log row fields/order/content remain `{node: title, trait: choice label, env: environment name, verdict: localized verdict, seed}` and rows accumulate across restarts/seed changes.
- Copy exports `JSON.stringify(log,null,1)` with existing success/failure messages. CSV retains BOM, Korean header, quoted field order node/trait/env/verdict/seed, newline behavior and `evo_swipe_${seed}.csv` filename. Clear log affects log plus data-panel labels only.

## Required verification

- Compare original and final game-script bytes and legacy-file bytes, static IDs/tag types/data hooks, generated hooks and listener code.
- Run identical fixed seeds and side sequences against original and final; compare chosen environment, payoff, population, next stage/ending, path, logs, reached/seen/run edges and seed evolution. Cover every payoff, both overrides, cap/collapse/perish, restarts, checkpoint, tutorial and exports.
- Browser-check pointer thresholds/cancel/lock, keyboard/modal priority, roulette/reduced motion, tutorial, tree pan/zoom, data controls and mobile touch availability. Report browser errors and resource requests. Run edited single HTML with network unavailable.
- No gameplay edits to fix baseline bugs are authorized. Record potential gameplay improvements separately; never implement them in this task.
