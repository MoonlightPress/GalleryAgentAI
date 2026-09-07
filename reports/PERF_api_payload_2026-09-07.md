# Why the site loads slowly — measured 2026-09-07

Not a regression from that day's work. It has been this size all along, and it
is not a caching or gzip problem: both are configured correctly.

## The measurement

Against production, `https://twilightdreamworks.com`:

| endpoint | raw | gzipped | time |
|---|---:|---:|---:|
| `/api/opportunities` | **7.26 MB** | 744 KB | **4.0 s** |
| `/api/saffron` | 1.51 MB | 471 KB | 2.2 s |
| `/api/today` | 26 KB | 7 KB | 0.8 s |

Server throughput measures ~250–370 KB/s, so roughly 1.2 MB of compressed JSON
lands before the page can paint. She reads this on a phone in Tokyo.

## Where the 7.26 MB goes

By section:

| section | items | bytes | share |
|---|---:|---:|---:|
| **watch_list** | **828** | **4.31 MB** | **59%** |
| competitions_awards | 100 | 493 KB | 7% |
| zines_and_print | 30 | 184 KB | 3% |
| relationship_targets | 27 | 153 KB | 2% |
| open_calls | 21 | 114 KB | 2% |
| publication_editorial | 12 | 61 KB | 1% |
| immediate_best_moves | 0 | 2 B | — |

By field, across all 1,018 cards:

| field | bytes | share |
|---|---:|---:|
| `checklist` | 1,065,518 | 26.0% |
| `email_en` | 674,308 | 16.5% |
| `email_ja` | 378,908 | 9.3% |
| `email_zh` | 295,776 | 7.2% |
| `why_it_fits` | 143,519 | 3.5% |
| `overview` | 126,201 | 3.1% |
| `summary` | 124,620 | 3.0% |

**A third of the payload is full email drafts, in three languages, for every one
of 1,018 cards.** Another quarter is checklists. Both are read only inside
`OppDetailPanel` — she downloads 1,018 cards' worth of drafts in order to open
at most one.

## The one complication

`checklist` is not purely detail-panel. `frontend/src/utils/recommendationQuality.js`
(`checklistMap` / `applyChecklistSignal`) reads `item.label` and `item.status`
to compute the readiness signal that ORDERS the list. So it can be slimmed to
those two keys — it cannot simply be dropped.

## Proposed fix, in order of value against risk

1. **Strip `email_en` / `email_ja` / `email_zh` from the list payload** and fetch
   them from a per-opportunity detail endpoint on card open. −1.35 MB (~19%).
   Needs the endpoint plus a fetch in `OppDetailPanel`.
2. **Slim `checklist` to `{label, status}`** on the list surface, full object on
   detail. Keeps the ordering signal, sheds most of 1.07 MB.
3. **Cap `watch_list`.** 828 items is more than she would ever scroll and it is
   over half the response on its own.

Together: roughly 7.26 MB → under 2 MB.

## Why it was not done on the day

API surgery on the endpoint that feeds her main page, at the end of a long
session, with three mistakes already made that day by moving quickly. It is not
urgent — it is not new — and it wants tests.
