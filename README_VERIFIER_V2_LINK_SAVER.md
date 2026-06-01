
# Verifier V2 Link Saver

This fixes the bug where `verified_opportunities.json` had no `relevant_links`.

## Run

```powershell
python run_verifier_v2_link_saver.py
```

## Check

```powershell
python -c "import json,pprint;pprint.pp(json.load(open('memory/verified_opportunities.json',encoding='utf-8'))[0].keys())"
notepad reports\link_audit_report.md
notepad reports\submission_link_report.md
notepad reports\actionable_opportunities.md
```

You should now see `relevant_links` in the first record keys.

The important metric is whether `Submission links found` is no longer zero for every item.
