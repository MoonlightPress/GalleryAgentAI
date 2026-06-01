import './StatusBar.css'

const JUNE_2026 = {
  month: 'June 2026',
  days: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
  // June 1, 2026 is a Monday
  dates: [
    [1, 2, 3, 4, 5, 6, 7],
    [8, 9, 10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19, 20, 21],
    [22, 23, 24, 25, 26, 27, 28],
    [29, 30, null, null, null, null, null],
  ],
  today: 2,
}

export default function StatusBar() {
  return (
    <div className="status-bar">
      {/* Left: Mochi identity + mood */}
      <div className="status-left">
        <div className="status-cat-thumb" />
        <div className="status-info">
          <div className="status-name">
            Mochi <span className="status-heart">♡</span>
          </div>
          <div className="status-mood-pills">
            <span className="mood-pill mood-happy">Happy</span>
            <span className="mood-sep">•</span>
            <span className="mood-pill mood-full">Full</span>
            <span className="mood-sep">•</span>
            <span className="mood-pill mood-content">Content</span>
          </div>
          <div className="status-bar-track">
            <div className="status-bar-fill" />
          </div>
        </div>
      </div>

      {/* Center: status message */}
      <div className="status-center">
        <div className="status-message">Mochi is happily napping in the sun.</div>
        <div className="status-sub">Come back later to feed and play!</div>
        <div className="status-sprig">🌿</div>
      </div>

      {/* Right: mini calendar + sticky note */}
      <div className="status-right">
        <div className="mini-calendar">
          <div className="mini-cal-month">{JUNE_2026.month}</div>
          <div className="mini-cal-grid">
            {JUNE_2026.days.map((d, i) => (
              <div key={i} className="mini-cal-header">{d}</div>
            ))}
            {JUNE_2026.dates.flat().map((d, i) => (
              <div
                key={i}
                className={`mini-cal-day${d === JUNE_2026.today ? ' today' : ''}${!d ? ' empty' : ''}`}
              >
                {d || ''}
              </div>
            ))}
          </div>
        </div>
        <div className="sticky-note">
          You've got beautiful things to make.
        </div>
      </div>
    </div>
  )
}
