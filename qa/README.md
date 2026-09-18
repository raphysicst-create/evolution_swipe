# Presentation regression audit

Run from the project directory with the already installed Python and Playwright:

```powershell
python qa/regression.py --label iteration-5
```

This audit does not install packages or alter any game file. The game still ships and runs as a single HTML file. Playwright is development QA tooling already available on this computer, not a game dependency. Results are recorded as `qa/results-<label>.json`.

The original files are pinned by SHA-256 and stored outside the repository at `%TEMP%\evo-swipe-presentation-baseline-20260919`. A successful audit also saves `verified-<label>.html` there, supporting exact rollback and independent review. Each report pins the candidate file hash and fails if the candidate changes while the audit is running. The baseline archive is local QA evidence; it is not required to play the game.

The audit checks:

- The entire 46,376-byte game script remains byte-identical, including data, algorithms, generated markup, timers, listeners and exports. The separate legacy `evolution_swipe.html` is byte-identical in its entirety.
- All 71 original HTML IDs retain their element tags; there are no duplicates. Original data attributes and the five tutorial sections retain their values and order.
- Original and candidate execute offline in real Chromium. The original's unavailable Tailwind config global is stubbed only in the original test context, without changing its game script. Original missing CDN resources are recorded as a baseline limitation. The candidate must make zero external requests and produce zero JavaScript errors.
- Every one of 60 trait/environment payoff cells runs at starting populations 1, 20, 45, 50, 100 and 120: 360 transactions cover cap, decline, both -45 overrides, population collapse, survival and direct extinction. Eight real seeds and eight side sequences add 64 deterministic routes; 2,048 raw RNG values are also compared.
- State snapshots compare pending data, node, population, seed, locks, path, logs, discovered/reached/current-run sets, endings and rendered game text. Restart, checkpoint, seed application, tutorial isolation, diagram graph/zoom and JSON/CSV export behavior are compared.
- Browser pointer events cover -81/-80/+80/+81 thresholds, cancel and non-primary-button rejection, with immediate and post-260ms state snapshots. These are separate from actual desktop mouse and mobile Chromium touch swipes.
- The candidate's actual hit targets, tutorial skip, desktop/mobile swipes, continue, diagram controls, seed input and keyboard progression are tested at 1280×900 and 390×844. Every mode runs with external requests blocked.
- Normal-motion roulette is checked separately from reduced-motion test contexts. Chosen → spin → environment → verdict ordering, exact wheel alignment and unchanged pre-continue population/log behavior are compared. Observed timing, frame intervals and long tasks are reported.
- Final short-screen checks at 320×568 and 844×390 click through all five tutorial pages and the practice gate, then select and click an ending checkpoint inside the scrollable modal. The resulting node and population are verified after the actual click.

`--skip-ui` is only for developing the harness against the untouched baseline; it is not an acceptance run. `results-harness-baseline.json` intentionally records the preexisting offline `tailwind is not defined` error while all original-versus-original gameplay comparisons passed.

Performance samples describe this machine's headless Chromium run, not a certification for every low-end device. The original offline load includes blocked CDN attempts, so it is not a fair comparison to a fully cached original online page. Use dependency size, actual zero-request execution, animation inspection, frame samples and independent visual testing together. QA has not modified baseline gameplay bugs or added save behavior that the current game does not possess.

For the separate fair performance comparison, `python qa/performance.py --capture` collects the original HTML's public CDN responses into the TEMP baseline directory. It validates actual Tailwind styling and the original Font Awesome font. The captured nine resources total 3,798,955 decoded bytes; none is added as a candidate dependency. `python qa/performance.py --label final --trials 5` then replays the exact cached original resources with no live networking and compares them to the standalone candidate. It runs five trials per page at normal CPU speed and 4× CPU throttling, measuring ready time, first overlay callbacks/tasks, steady roulette frames, and 120-frame pointer drags. CPU throttling is a controlled simulation on this computer, not a claim about every physical low-end device. Run it without concurrent captures or browser tests.
