
# Mochi Feedback Learning Upgrade

This adds adaptive recommendation learning.

It watches:
- interested
- submitted
- waiting
- follow_up
- conversation_started
- soft_relationship
- strong_relationship
- rejected
- archived

Then it learns:
- what categories she likes
- what cities/countries seem useful
- what tags recur in good opportunities
- what themes appear in rejected opportunities

Then it rescoring future recommendations.

## Install

Unzip into:

```text
C:\ScottStuff\GalleryAgentAI
```

## Run

```powershell
python patch_pipeline_feedback_learning.py
python patch_app_feedback_learning.py
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Deploy

```powershell
git add .
git commit -m "add feedback learning system"
git push
```

## Notes

At first, it may say there are no learned preferences. That is normal. The system needs relationship states or saved/rejected opportunities before it can learn.
