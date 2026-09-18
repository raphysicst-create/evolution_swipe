# Final QA evidence

Candidate SHA-256: `86f4edbae14dd729ec7b6c8be8abfa7f7845ef24f3d33edd320001f8d952c026`

Standalone HTML: 196,086 bytes. Frozen inline game script: 46,376 bytes, SHA-256 `9c3811e53c153c817b7398d8bdf26b62053e8b17adb402fcdc4149c1c0d72107`. Legacy HTML remains byte-identical.

## Regression

- Iterations 1–5 pass the original-versus-candidate audit. Final report: `results-iteration-5.json`.
- All 71 original IDs/tag types, original data attributes and tutorial order remain intact.
- Every one of 60 payoffs at six populations (360 transactions), 64 seeded routes, 2,048 RNG values, input boundaries/cancellation, restart/checkpoint, seed application, tutorial isolation, branch diagram, and JSON/CSV exports match.
- Zero final JavaScript errors and zero network requests. Real desktop mouse and mobile touch input work offline. Normal/reduced roulette outcomes match. At 320×568 and 844×390, tutorial navigation and ending checkpoint controls remain operable through inner scrolling.

## Controlled performance comparison

Five trials per cell in headless Chromium at 1280×900. Original public CDN resources were captured once, validated as fully styled, and replayed locally; there were no cache misses or runtime errors. Candidate uses no external resources. CPU 4× is a local throttling simulation, not a certification of specific low-end hardware.

| CPU | Metric (ms) | Original median | Candidate median |
|---|---|---:|---:|
| 1× | Page ready | 1767.3 | 314.8 |
| 1× | First overlay frame callback | 83.5 | 56.4 |
| 1× | Initial long-task maximum | 55.0 | 55.0 |
| 1× | Roulette frame interval p95 | 116.7 | 16.8 |
| 1× | Drag frame interval p95 | 33.4 | 16.8 |
| 1× | Pointer handler p95 | 0.2 | 0.2 |
| 4× | Page ready | 4612.1 | 1382.3 |
| 4× | First overlay frame callback | 257.8 | 277.7 |
| 4× | Initial long-task maximum | 238.0 | 277.0 |
| 4× | Roulette frame interval p95 | 133.4 | 16.8 |
| 4× | Drag frame interval p95 | 33.4 | 16.7 |
| 4× | Pointer handler p95 | 0.7 | 0.7 |

At 4× CPU throttling the first overlay callback is about 20 ms slower (277.7 vs 257.8 ms), and its initial long task is 277 vs 238 ms. This localized cost remains visible in the report; do not claim zero latency or improvement in every metric. Candidate startup and ongoing drag/roulette frame distributions improve in this controlled comparison. The candidate's maximum sampled roulette interval at 4× is 183.3 ms; the recorded frame data does not locate that spike precisely. Its median p95 is 16.8 ms, with one trial at 33.3 ms. Another throttled trial records a 59 ms long task at 2.608 seconds. Normal-speed candidate maximum after the initial window is 16.8 ms.

The regression harness's earlier bare-offline original timing is not the fully styled comparator and must not be used for a visual-performance claim. `performance-final.json` contains all 20 raw samples, response validation, candidate hash and stability check. Original cached dependencies total 3,798,955 decoded bytes and remain only in TEMP; they are not part of the shipped game.

The untouched baseline self-check records its preexisting offline Tailwind error. That is distinct from all edited iteration reports, which pass without external dependencies. The iteration-5 preflight is preserved separately; final acceptance uses the final hash above.
