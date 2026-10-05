from __future__ import annotations
from collections import Counter,defaultdict
def build_requirement_matrix(requirements,closures,reconciliation):
 states={r['id']:r['state'] for r in requirements}; sources={r['id']:['M22'] for r in requirements}
 for milestone,data in closures.items():
  rows=data.get('closed_by_m23',[])+data.get('closures',[])
  if data.get('requirement_id'): rows.append(data)
  for x in rows:
   rid=x.get('requirement_id'); new=x.get('m23_state') or x.get('m24_state') or x.get('m25_state') or x.get('m26_state') or x.get('m27_state') or x.get('new_state')
   if rid and new: states[rid]=new;sources[rid].append(milestone)
 for x in reconciliation.get('rules',[]): states[x['requirement_id']]=x['reconciled_state'];sources[x['requirement_id']].append('M29-reconciliation')
 rows=[];bydom=defaultdict(list)
 for r in requirements:
  row={'requirement_id':r['id'],'domain':r['domain'],'objective':r['objective'],'state':states[r['id']],'evidence_sources':sources[r['id']]};rows.append(row);bydom[r['domain']].append(row)
 domains=[]
 for d in range(1,9):
  rr=bydom[d];domains.append({'domain':d,'state':'EVIDENCED' if all(x['state']=='EVIDENCED' for x in rr) else 'PARTIAL','requirements_total':len(rr),'requirements_evidenced':sum(x['state']=='EVIDENCED' for x in rr),'open_requirements':[x['requirement_id'] for x in rr if x['state']!='EVIDENCED']})
 c=Counter(states.values())
 return {'requirements':rows,'domains':domains,'state_counts':dict(c),'all_requirements_evidenced':all(x['state']=='EVIDENCED' for x in rows),'open_requirements':[x['requirement_id'] for x in rows if x['state']!='EVIDENCED']}
