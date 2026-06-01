
import React from "react";

/*
Homepage section.

Expected data:
- deploy_data/category_metrics.json

Usage:
import CareerPathsHome from "./CareerPathsHome";

<CareerPathsHome metrics={categoryMetrics} onSelect={(id) => ...} />
*/

export default function CareerPathsHome({ metrics, onSelect }) {
  const categories = metrics?.categories || [];

  return (
    <section className="space-y-6">
      <div>
        <p className="text-sm uppercase tracking-wide opacity-60">Career Advisor</p>
        <h1 className="text-3xl font-semibold">Career Paths</h1>
        <p className="mt-2 max-w-2xl opacity-75">
          Compare the strongest paths by speed, cost, difficulty, and current opportunity coverage.
        </p>
      </div>

      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
        {categories.map((cat) => (
          <button
            key={cat.category_id}
            onClick={() => onSelect?.(cat.category_id)}
            className="text-left rounded-2xl border p-5 shadow-sm hover:shadow-md transition bg-white"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold">{cat.title}</h2>
                <p className="mt-1 text-sm opacity-70">
                  {cat.difficulty} · {cat.cost} cost · {cat.speed}
                </p>
              </div>
              <div className="rounded-xl border px-3 py-2 text-center">
                <p className="text-xs opacity-60">Score</p>
                <p className="text-2xl font-semibold">{cat.path_score}</p>
              </div>
            </div>

            <div className="mt-5 grid grid-cols-3 gap-2 text-sm">
              <div className="rounded-xl bg-neutral-50 p-3">
                <p className="opacity-60">Targets</p>
                <p className="font-semibold">{cat.known_targets}</p>
              </div>
              <div className="rounded-xl bg-neutral-50 p-3">
                <p className="opacity-60">Priority</p>
                <p className="font-semibold">{cat.high_priority_targets}</p>
              </div>
              <div className="rounded-xl bg-neutral-50 p-3">
                <p className="opacity-60">Local</p>
                <p className="font-semibold">{cat.local_targets}</p>
              </div>
            </div>

            <p className="mt-4 text-sm opacity-75 line-clamp-3">{cat.why_this_path}</p>
          </button>
        ))}
      </div>
    </section>
  );
}
