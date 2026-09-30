import json
from pathlib import Path
from portable_ai_governance.cra_incident_clock.classifier import classify_severe_incident
from portable_ai_governance.cra_incident_clock.clock import build_case,evaluate_deadlines
from portable_ai_governance.cra_incident_clock.engine import evaluate_fixture_set
from portable_ai_governance.cra_incident_clock.journal import build_awareness_journal,verify_awareness_journal
ROOT=Path(__file__).resolve().parents[2]

def policy():return json.loads((ROOT/'governance/cra/m13/incident-classification-policy.json').read_text())
def load(name):return json.loads((ROOT/'tests/fixtures/m13/incidents'/name).read_text())

def test_article_14_5_a():
 r=classify_severe_incident(load('severe-14-5-a.json'),policy());assert r['decision']=='SEVERE_INCIDENT' and r['article_14_5_a'] and not r['article_14_5_b']
def test_article_14_5_b():
 r=classify_severe_incident(load('severe-14-5-b.json'),policy());assert r['decision']=='SEVERE_INCIDENT' and r['article_14_5_b']
def test_not_severe(): assert classify_severe_incident(load('not-severe.json'),policy())['decision']=='NOT_SEVERE'
def test_incomplete(): assert classify_severe_incident(load('incomplete.json'),policy())['decision']=='INCOMPLETE'
def test_aev_deadlines():
 c=build_case('AEV','p','a','2026-09-30T12:00:00Z',policy(),'2026-10-02T12:00:00Z');assert c['deadlines']['early_warning_at']=='2026-10-01T12:00:00Z';assert c['deadlines']['notification_at']=='2026-10-03T12:00:00Z';assert c['deadlines']['final_report_at']=='2026-10-16T12:00:00Z'
def test_incident_deadlines_calendar_month():
 c=build_case('SEVERE_INCIDENT','p','e','2026-09-30T10:00:00Z',policy(),notification_submitted_at='2026-10-31T08:00:00Z');assert c['deadlines']['final_report_at']=='2026-11-30T08:00:00Z'
def test_breach_detection():
 c=build_case('AEV','p','a','2026-09-30T12:00:00Z',policy(),'2026-10-02T12:00:00Z');s=evaluate_deadlines(c,'2026-10-04T12:00:00Z');assert s['stages'][0]['status']=='BREACHED' and s['stages'][1]['status']=='BREACHED'
def test_awareness_chain_and_immutability():
 c=build_case('AEV','p','a','2026-09-30T12:00:00Z',policy());rows=build_awareness_journal([c]);assert verify_awareness_journal(rows);bad=dict(c);bad['manufacturer_awareness_at']='2026-09-30T13:00:00Z';
 try: build_awareness_journal([c,bad]);assert False
 except ValueError: pass
def test_fixture_coverage():
 _,a,c,s,j=evaluate_fixture_set(ROOT);assert {x['decision'] for x in a}=={'SEVERE_INCIDENT','NOT_SEVERE','INCOMPLETE'};assert {x['case_type'] for x in c}=={'AEV','SEVERE_INCIDENT'};assert verify_awareness_journal(j)
