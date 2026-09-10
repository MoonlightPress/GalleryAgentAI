import fs from 'node:fs';
import {STATES,GOALS} from '../../frontend/src/data/strategy_ladders.js';
import {GRANT_LANDSCAPE} from '../../frontend/src/data/saffron_insights.js';
const dir=new URL('./',import.meta.url);
for(const [name,obj] of [['ladders',{STATES,GOALS}],['grants',GRANT_LANDSCAPE]]) {
  const rows=[];
  function walk(v,p='') {
    if(!v||typeof v!=='object')return;
    if('zh' in v && 'en' in v){rows.push({path:p,zh:v.zh,en:v.en});return;}
    for(const [k,x] of Object.entries(v)){
      const q=p?`${p}.${k}`:k;
      if(k.endsWith('_zh'))rows.push({path:q,zh:x}); else walk(x,q);
    }
  }
  walk(obj);
  fs.writeFileSync(new URL(name+'_inventory.json',dir),JSON.stringify(rows,null,2));
  fs.writeFileSync(new URL(name+'_zh.txt',dir),rows.map(r=>`[${r.path}] ${r.zh}`).join('\n\n'));
  process.stdout.write(`${name}: ${rows.length} Chinese fields\n`);
}
