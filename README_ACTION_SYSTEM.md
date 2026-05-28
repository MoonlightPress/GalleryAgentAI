# Mochi Action System

This adds a lightweight CRM/action layer.

## New files

- `opportunity_status_engine.py`
- `mochi_action_components.py`
- `run_full_mochi_pipeline.py`

## What it creates

- `memory/opportunity_status.json`
- `memory/action_queue.json`

## Statuses

- new
- saved
- contacted
- response_received
- rejected

## Run

```powershell
python run_full_mochi_pipeline.py
python -m streamlit run app.py
```

## Purpose

This turns opportunities into a workflow:
- save
- reject
- mark contacted
- mark response received
- track follow-up dates
- show action queue
