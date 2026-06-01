
import React from "react";

/*
Publishing page.

Expected data:
- deploy_data/publishing_website_section.json
*/

function StatCard({ label, value }) {
  return (
    <div className="rounded-2xl border p-4 bg-white shadow-sm">
      <p className="text-sm opacity-60">{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
    </div>
  );
}

function TargetCard({ target }) {
  return (
    <article className="rounded-2xl border p-5 bg-white shadow-sm space-y-3">
      <div>
        <h3 className="text-lg font-semibold">{target.display_name}</h3>
        <p className="text-sm opacity-65">{target.neighborhood} · {target.opportunity_type}</p>
      </div>
      <p className="text-sm opacity-80">{target.why_it_matters}</p>
      <div className="rounded-xl bg-neutral-50 p-3 text-sm">
        <p className="font-medium">First action</p>
        <p className="opacity-75">{target.first_action}</p>
      </div>
    </article>
  );
}

export default function PublishingCategoryPage({ section }) {
  if (!section) return null;

  const statCards = section.top_stat_cards || [];
  const plan = section.battle_plan || {};
  const phase1 = plan.phase_1_targets || [];
  const samples = section.top_samples || [];

  return (
    <main className="space-y-8">
      <section className="rounded-3xl border p-7 bg-white shadow-sm">
        <p className="text-sm uppercase tracking-wide opacity-60">Career Category</p>
        <h1 className="mt-1 text-4xl font-semibold">{section.title}</h1>
        <p className="mt-3 max-w-3xl text-lg opacity-80">{section.positioning}</p>

        <div className="mt-6 grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
          {statCards.map((card) => (
            <StatCard key={card.label} label={card.label} value={card.value} />
          ))}
        </div>
      </section>

      <section className="grid lg:grid-cols-2 gap-5">
        <div className="rounded-2xl border p-6 bg-white shadow-sm">
          <h2 className="text-2xl font-semibold">Why this path</h2>
          <p className="mt-3 opacity-80">{section.metrics?.why_this_path}</p>
        </div>

        <div className="rounded-2xl border p-6 bg-white shadow-sm">
          <h2 className="text-2xl font-semibold">Success condition</h2>
          <p className="mt-3 opacity-80">{plan.success_condition}</p>
          <p className="mt-3 text-sm opacity-70">
            Estimated cost: {plan.estimated_cost} · Timeline: {plan.expected_timeline}
          </p>
        </div>
      </section>

      <section className="rounded-2xl border p-6 bg-white shadow-sm">
        <h2 className="text-2xl font-semibold">Battle Plan</h2>
        <ol className="mt-4 space-y-2 list-decimal pl-5">
          {(plan.steps || []).map((step, index) => (
            <li key={index} className="opacity-80">{step}</li>
          ))}
        </ol>
      </section>

      <section>
        <h2 className="text-2xl font-semibold">Phase 1 Targets</h2>
        <div className="mt-4 grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          {phase1.map((target) => (
            <TargetCard key={target.display_name} target={target} />
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold">Good Samples</h2>
        <div className="mt-4 grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          {samples.map((target) => (
            <TargetCard key={target.display_name} target={target} />
          ))}
        </div>
      </section>
    </main>
  );
}
