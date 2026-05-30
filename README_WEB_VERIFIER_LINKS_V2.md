
# Web Verifier Links v2

This fixes the missing `relevant_links` field.

## Run

```powershell
python run_real_verification.py
python -c "import json,pprint;pprint.pp(json.load(open('memory/verified_opportunities.json',encoding='utf-8'))[0].keys())"
python run_submission_crawler.py
```

After the first check, you should see:

```text
relevant_links
```

Then open:

```powershell
notepad reports\web_verification_report.md
notepad reports\actionable_opportunities.md
```
