
# Category Context Engine v1

Turns the 230 raw multi-ingress candidates into advisor-style context blocks.

Input:

```text
memory/multi_ingress_raw_candidates.json
```

Output:

```text
memory/category_context.json
deploy_data/category_context.json
reports/category_context.md
```

It also patches Streamlit to show an **Opportunity Context** section.

## Run

```powershell
python run_category_context_v1.py
```

## Check

```powershell
notepad reports\category_context.md
```

## Launch

```powershell
python -m streamlit run app.py
```

## Git

```powershell
git add .
git commit -m "add category context engine and advisor summaries"
git push
```
