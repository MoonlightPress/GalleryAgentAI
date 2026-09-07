# Out of season, not out of use

Art that is good but wrong for the current month. Nothing here is in rotation:
`heroImages.js` globs `heroes/mochi`, `heroes/peppercorn` and `heroes/saffron`
only, so a file sitting here is simply not in any pool.

| file | was | why it is here |
|---|---|---|
| `mochi_winter_01.webp` | `mochi/mochi_day_06.webp` | Snow on the roofs and the balustrade, and a note reading "Rainy days, cosy ways" — a winter scene surfacing in September (Scott, 2026-09-07). The skyline is also European rather than Tokyo. |

## The eventual home for this

Bible11 specifies season tags in the filename — `mochi_winter_overcast_01.webp`
— with the selection algorithm weighting toward images whose tags match the
current month, and untagged images eligible year-round. That system does not
exist yet; `heroImages.js` still picks by day/night only.

Files here are named to that convention already, so when seasonal weighting is
built the fix is to move them back into their companion folder and let the
weighting do the work. Until then, moving a file in or out of this directory is
the whole of taking it out of, or putting it back into, rotation.
