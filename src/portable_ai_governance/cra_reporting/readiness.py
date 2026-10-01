from __future__ import annotations

def readiness(pack):
    anchored=[s for s in pack['stages'] if s['readiness']!='NOT_YET_ANCHORED']
    return {
      'pack_id':pack['pack_id'],'case_id':pack['case_id'],
      'all_currently_anchored_stages_ready':all(s['readiness']=='READY' for s in anchored),
      'ready_stages':[s['stage'] for s in anchored if s['readiness']=='READY'],
      'needs_data_stages':[s['stage'] for s in anchored if s['readiness']=='NEEDS_DATA'],
      'not_yet_anchored_stages':[s['stage'] for s in pack['stages'] if s['readiness']=='NOT_YET_ANCHORED'],
      'human_submission_required':True,'srp_submission_performed':False
    }
