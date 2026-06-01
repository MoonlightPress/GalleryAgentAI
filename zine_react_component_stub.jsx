
/*
Optional React component stub.

Expected data:
deploy_data/zine_website_top_section.json
deploy_data/zine_category_targets.json

Drop this into your dashboard where the Zine category should appear.
*/

export default function ZineTopSection({ section }) {
  if (!section) return null;

  const targets = section.top_samples || [];
  const phase1 = section.practical_solution?.phase_1_targets || [];

  return (
    <section className="rounded-2xl border p-6 shadow-sm space-y-6">
      <div>
        <p className="text-sm uppercase tracking-wide opacity-70">Career Category</p>
        <h2 className="text-3xl font-semibold">{section.title}</h2>
        <p className="mt-2 text-base opacity-80">{section.subtitle}</p>
      </div>

      <div className="rounded-xl p-4 bg-neutral-50">
        <p className="text-lg">{section.positioning}</p>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div className="rounded-xl border p-4">
          <p className="text-sm opacity-70">Known Targets</p>
          <p className="text-2xl font-semibold">{section.known_target_count}</p>
        </div>
        <div className="rounded-xl border p-4">
          <p className="text-sm opacity-70">High Priority</p>
          <p className="text-2xl font-semibold">{section.high_priority_count}</p>
        </div>
        <div className="rounded-xl border p-4">
          <p className="text-sm opacity-70">Koenji + Nakano</p>
          <p className="text-2xl font-semibold">{section.koenji_nakano_count}</p>
        </div>
      </div>

      <div>
        <h3 className="text-xl font-semibold">Practical Solution</h3>
        <p className="mt-1">{section.practical_solution?.goal}</p>
        <ul className="mt-3 list-disc pl-5">
          {(section.practical_solution?.make || []).map((item, i) => <li key={i}>{item}</li>)}
          <li>{section.practical_solution?.monthly_habit}</li>
        </ul>
      </div>

      <div>
        <h3 className="text-xl font-semibold">Phase 1 Targets</h3>
        <div className="mt-3 grid gap-3">
          {phase1.map((t) => (
            <div key={t.display_name} className="rounded-xl border p-4">
              <div className="font-medium">{t.display_name}</div>
              <div className="text-sm opacity-70">{t.neighborhood} · {t.opportunity_type}</div>
              <p className="mt-2 text-sm">{t.why_it_matters}</p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-xl font-semibold">Good Samples</h3>
        <div className="mt-3 grid md:grid-cols-2 gap-3">
          {targets.map((t) => (
            <div key={t.display_name} className="rounded-xl border p-4">
              <div className="font-medium">{t.display_name}</div>
              <div className="text-sm opacity-70">{t.neighborhood} · {t.opportunity_type}</div>
              <p className="mt-2 text-sm">{t.first_action}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
