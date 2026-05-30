# Patch app.py with action workflow

## 1. Add import near top of app.py

```python
from mochi_action_components import render_action_workspace, render_status_controls
```

## 2. Change tabs

Find:

```python
tabs = st.tabs(["Mochi Atelier", "Intelligence", "Mousehole", "Observatory", "Archive"])
```

Replace with:

```python
tabs = st.tabs(["Mochi Atelier", "Actions", "Intelligence", "Mousehole", "Observatory", "Archive"])
```

## 3. Add new Actions tab after Mochi Atelier tab

```python
with tabs[1]:
    render_action_workspace()
```

## 4. Shift later tab indexes

If you already had:

```python
with tabs[1]:
    render_intelligence_workspace()
```

Change it to:

```python
with tabs[2]:
    render_intelligence_workspace()
```

Then Mousehole becomes `tabs[3]`, Observatory becomes `tabs[4]`, Archive becomes `tabs[5]`.

## 5. Optional: add action buttons inside detail report

Inside `render_detail(opp)`, before the Close button, add:

```python
render_status_controls(opp, key_prefix="detail")
```

## 6. Run

```powershell
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## 7. Deploy

```powershell
git add app.py deploy_data memory reports *.py
git commit -m "add action workflow"
git push
```
