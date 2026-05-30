# Patch app.py to use richer report engine

At the top of `app.py`, after imports, add:

```python
from opportunity_report_engine import opportunity_report_markdown
```

Inside `render_detail`, replace:

```python
st.markdown(report_markdown(opp))
```

with:

```python
st.markdown(opportunity_report_markdown(opp))
```
