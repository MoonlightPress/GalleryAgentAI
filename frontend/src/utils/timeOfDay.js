// Is it "night" on the viewer's clock? Used to swap the companions' hero art to
// their night-time illustrations in the evening. 18:00–05:59 local counts as
// night — late enough that daytime work has wound down, warm enough to feel like
// the atelier at dusk. Computed once when the hero mounts (a page open across the
// 6pm/6am boundary picks up the new art on the next load), so no timer is needed.
export function isNightNow(date = new Date()) {
  const h = date.getHours()
  return h >= 18 || h < 6
}
