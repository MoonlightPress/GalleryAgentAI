
import json, os
from pathlib import Path
queue='memory/verification_queue.json'
if not os.path.exists(queue):
    Path('memory').mkdir(exist_ok=True)
    json.dump([], open(queue,'w',encoding='utf-8'))
print('verification queue ready')
