
/*
Example integration.

Replace imports/paths to match your app.
This assumes your bundler can import JSON.
*/

import React, { useState } from "react";
import CareerPathsHome from "./components/career/CareerPathsHome";
import ZineCategoryPage from "./components/career/ZineCategoryPage";
import PublishingCategoryPage from "./components/career/PublishingCategoryPage";

import categoryMetrics from "../deploy_data/category_metrics.json";
import zineSection from "../deploy_data/zine_website_section_final.json";
import publishingSection from "../deploy_data/publishing_website_section.json";

export default function CareerAdvisorPage() {
  const [selected, setSelected] = useState("zines");

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-10">
      <CareerPathsHome metrics={categoryMetrics} onSelect={setSelected} />

      {selected === "zines" && <ZineCategoryPage section={zineSection} />}
      {selected === "publishing" && <PublishingCategoryPage section={publishingSection} />}
    </div>
  );
}
