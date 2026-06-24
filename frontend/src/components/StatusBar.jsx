import './StatusBar.css'

// The old status panel (Mochi mood pills, mini-calendar, buddy stats, sticky note)
// was removed per Scott — it wasn't earning its space. For now this is just a quiet
// colored accent to close the page; something useful can take its place later.
export default function StatusBar() {
  return <div className="status-accent" aria-hidden="true" />
}
