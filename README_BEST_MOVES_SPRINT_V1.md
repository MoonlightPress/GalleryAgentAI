# Best Moves Sprint v1

Compresses all current opportunity research into one small homepage section.

It creates:

```text
memory/best_moves.json
deploy_data/best_moves.json
reports/best_moves.md
```

Then patches Streamlit to show:

- Best Next Moves
- 3 overall cards
- more overall moves collapsed
- category summaries collapsed

## Run

```powershell
python run_best_moves_sprint_v1.py
```

## Check

```powershell
notepad reports\best_moves.md
```

## Launch

```powershell
python -m streamlit run app.py
```

## Git

```powershell
git add .
git commit -m "add compressed best next moves section"
git push
```
