import './StatusBar.css'

// The old status panel (Mochi mood pills, mini-calendar, buddy stats, sticky note)
// was removed per Scott — it wasn't earning its space. The "Mochi found something
// new" notice moved OUT of here to a prominent top-of-page banner
// (NewOpportunitiesBanner) so it's actually seen. This is now just a quiet accent
// that closes the page; something useful can take its place later.
export default function StatusBar() {
  return <div className="status-accent" aria-hidden="true" />
}
