from __future__ import annotations
from .common import sha256_bytes
class BackupPolicyError(RuntimeError): pass
def validate_backup_policy(p):
 if p.get('copies_required',0)<3: raise BackupPolicyError('3-copy minimum required')
 if p.get('offsite_copies_required',0)<1: raise BackupPolicyError('offsite copy required')
 if p.get('immutable_copies_required',0)<1: raise BackupPolicyError('immutable copy required')
 if not p.get('encryption_required'): raise BackupPolicyError('backup encryption required')
 if p.get('rpo_hours',0)<=0 or p.get('rto_hours',0)<=0: raise BackupPolicyError('RPO/RTO required')
 return True
def make_backup_record(dataset_id,data,policy,created_at):
 digest=sha256_bytes(data)
 return {'backup_id':'backup-'+digest[:16],'dataset_id':dataset_id,'created_at':created_at,'sha256':digest,'encrypted':True,'immutable':True,'object_lock':'compliance','offsite':True,'retention_days':policy['retention_days']}
def verify_restore(record,restored,restore_started,restore_finished,policy,last_source_change):
 digest=sha256_bytes(restored);duration=max(0,(restore_finished-restore_started)/3600);age=max(0,(restore_started-last_source_change)/3600)
 return {'backup_id':record['backup_id'],'digest_match':digest==record['sha256'],'restore_duration_hours':duration,'rto_met':duration<=policy['rto_hours'],'recovery_point_age_hours':age,'rpo_met':age<=policy['rpo_hours'],'immutable_source':record.get('immutable') is True,'object_lock':record.get('object_lock'),'ok':digest==record['sha256'] and duration<=policy['rto_hours'] and age<=policy['rpo_hours'] and record.get('immutable') is True}
