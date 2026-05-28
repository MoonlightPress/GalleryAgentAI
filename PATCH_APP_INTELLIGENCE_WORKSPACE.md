# Patch app.py with intelligence workspace

## 1. Add this import near the top of app.py

```python
from mochi_dashboard_components import render_intelligence_workspace
```

## 2. Replace your tabs line

Find:

```python
tabs = st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])
```

Replace with:

```python
tabs = st.tabs(["Mochi Atelier", "Intelligence", "Mousehole", "Observatory", "Archive"])
```

## 3. Add this new tab block after the Mochi Atelier block

Because the new tab order is:

```python
tabs[0] = Mochi Atelier
tabs[1] = Intelligence
tabs[2] = Mousehole
tabs[3] = Observatory
tabs[4] = Archive
```

Add:

```python
with tabs[1]:
    render_intelligence_workspace()
```

## 4. Update your existing lower tabs

Change:

```python
with tabs[1]:
```

to:

```python
with tabs[2]:
```

Change:

```python
with tabs[2]:
```

to:

```python
with tabs[3]:
```

Change:

```python
with tabs[3]:
```

to:

```python
with tabs[4]:
```

## 5. Run

```powershell
python run_intelligence_pipeline.py
python -m streamlit run app.py
```

## 6. Deploy

```powershell
git add app.py mochi_dashboard_components.py deploy_data memory reports *.py
git commit -m "add intelligence workspace"
git push
```
