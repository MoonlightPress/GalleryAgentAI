# Remove Review Intelligence Patch v1

This removes the oversized Review Intelligence report dump from the Streamlit homepage.

It does not delete your reports.

It only removes:

```python
from ui.opportunity_review_sections import render_opportunity_review_sections
```

and:

```python
render_opportunity_review_sections()
```

from `app.py`.

## Run

```powershell
python remove_review_intelligence_patch_v1.py
```

## Launch

```powershell
python -m streamlit run app.py
```

## Git

```powershell
git add .
git commit -m "remove oversized review intelligence section from homepage"
git push
```
