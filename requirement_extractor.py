
import json
from pathlib import Path

src='memory/submission_targets.json'
out='memory/submission_requirements.json'

data=json.load(open(src,encoding='utf-8'))

for item in data:
    item['estimated_requirements']=[
        'portfolio',
        'artist statement',
        'images of work'
    ]

json.dump(data,open(out,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
print('Wrote',out)
