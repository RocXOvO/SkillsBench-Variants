"""Read-only source verification and descriptive summary of the complete variant ledger.

This is a summary of recorded historical/recovery observations, not a pooled
uniform-protocol causal estimate. No experiment is launched or modified.
"""
from pathlib import Path
from collections import Counter, defaultdict
from itertools import product
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / 'paper/audits/variant-maintext-20260921'
EXP = ROOT / 'experiments/skillsbench-transfer/dev-v0.7'
METHODS = ['skillevolver', 'spark', 'coevoskills']
STATUS = {'valid', 'valid_budget_exhaustion', 'scientific_failure', 'passed'}

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

ledger = read(EXP / 'reviewed-recovery-coverage-20260920-user-exclusions-r2.json')
r3 = read(EXP / 'reviewed-recovery-coverage-20260920-final-r3.json')
r5 = read(EXP / 'reviewed-recovery-coverage-20260920-final-r5.json')
assert digest(EXP / 'reviewed-recovery-coverage-20260920-user-exclusions-r2.json') == r3['parent_ledger']['sha256']
assert digest(EXP / r5['parent_ledger']['name']) == r5['parent_ledger']['sha256']
inventory = read(OLD / 'formal-attempt-inventory-main-r33-20260920.json')
identities = {(x['variant_id'], x['condition']) for x in ledger['historical_pairs']}
candidates = defaultdict(dict)

def add(x, variant=None, condition=None):
    key = (x.get('variant_id', variant), x.get('condition', condition))
    if key in identities and x.get('status') in STATUS and isinstance(x.get('reward'), (int, float)):
        candidates[key][x['path']] = {
            'variant_id': key[0], 'condition': key[1], 'path': x['path'],
            'status': x['status'], 'reward': x['reward'],
            'grader_finished_at': x.get('grader_finished_at')}

for row in inventory['rows']:
    for x in [row['parent']] + row['sidecars']:
        if x:
            add(x, row['variant_id'], row['condition'])
for x in inventory['indexed_results'] + inventory['audited_reevaluation_results']:
    add(x)
assert len(candidates) == 838

# Extend the existing literal-valid / lexicographic-path tie breaker to all
# historical cells. This is a post-collection deterministic source resolution,
# not a preregistered rule and not a claim that one conflicting score is truer.
# Keep every conflicting candidate and quantify its influence below.
selected = {}
conflicts = []
for key, by_path in sorted(candidates.items()):
    xs = list(by_path.values())
    chosen = min(xs, key=lambda x: (x['status'] != 'valid', x['path']))
    selected[key] = dict(chosen, category='historical')
    if len({x['reward'] for x in xs}) > 1:
        conflicts.append({'variant_id': key[0], 'condition': key[1],
                          'selected_path': chosen['path'], 'selected_reward': chosen['reward'],
                          'candidates': xs})

recoveries = ledger['separate_recoveries'] + r3['added_separate_recoveries']
assert len(recoveries) == 48
for x in recoveries:
    key = x['variant_id'], x['condition']
    assert key not in selected
    selected[key] = {**x, 'path': x['result_path'], 'category': 'recovery',
                     'expected_sha256': x['result_sha256']}

checks = read(OLD / 'coverage.json')['separate_file_read_checks']['cells']
superseded = []
for x in checks:
    key = x['variant_id'], x['condition']
    superseded.append({'variant_id': key[0], 'condition': key[1],
                       'old': selected[key], 'replacement': x,
                       'reason': 'Use the completed file-reading repair in place of inline skill delivery for the full descriptive summary.'})
    selected[key] = {**x, 'path': x['evidence'], 'category': 'file_read_repair'}

assert len(selected) == 886
assert dict(Counter(c for v, c in selected)) == {'coevoskills': 221, 'no_skill': 222, 'skillevolver': 222, 'spark': 221}
assert len({v for v, c in selected}) == 222
requests = {x['path']: x for x in selected.values()}
for conflict in conflicts:
    for x in conflict['candidates']:
        requests.setdefault(x['path'], x)
remote = '''import json, hashlib
from pathlib import Path
out = []
for x in REQUESTS:
 p = Path(x['path']); raw = p.read_bytes(); d = json.loads(raw)
 assert d['reward'] == x['reward'], str(p)
 assert d['status'] == x['status'], str(p)
 sha = hashlib.sha256(raw).hexdigest()
 if x.get('expected_sha256'): assert sha == x['expected_sha256'], str(p)
 out.append({'path': str(p), 'sha256': sha, 'reward': d['reward'], 'status': d['status']})
print(json.dumps(out))
'''.replace('REQUESTS', repr(list(requests.values())))
verified = subprocess.run(['ssh', '-o', 'BatchMode=yes', 'amax@219.223.251.70', 'python3 -'],
                          input=remote, text=True, capture_output=True, check=True)
provenance = {x['path']: x for x in json.loads(verified.stdout)}
for x in selected.values():
    x['sha256'] = provenance[x['path']]['sha256']
for conflict in conflicts:
    for x in conflict['candidates']:
        x['sha256'] = provenance[x['path']]['sha256']

def summarize(method, data, paradigm=None):
    vs = sorted(v for v, c in data if c == method and
                (paradigm is None or v.split('--')[1] == paradigm))
    pairs = [(data[v, 'no_skill']['reward'], data[v, method]['reward']) for v in vs]
    ds = [s-b for b, s in pairs]
    return {'n': len(vs), 'baseline_mean': sum(b for b, s in pairs)/len(vs)*100,
            'skill_mean': sum(s for b, s in pairs)/len(vs)*100,
            'delta': sum(ds)/len(vs)*100, 'improved': sum(d > 0 for d in ds),
            'regressed': sum(d < 0 for d in ds), 'tied': sum(d == 0 for d in ds)}

report = {'scope': 'Full recorded-evaluation descriptive summary, including historical, recovery and file-reading repair results.',
          'unique_variants': 222, 'unique_condition_cells': 886,
          'category_counts': dict(Counter(x['category'] for x in selected.values())),
          'condition_counts': dict(Counter(c for v, c in selected)), 'methods': {},
          'verified_source_files': len(provenance), 'conflict_sensitivity': {}}
paired = []
for m in METHODS:
    report['methods'][m] = {'overall': summarize(m, selected),
        'paradigms': {p: summarize(m, selected, p) for p in ['p1', 'p2', 'p3']}}
    for v, c in sorted(selected):
        if c == m:
            b, s = selected[v, 'no_skill'], selected[v, m]
            paired.append({'method': m, 'variant_id': v, 'baseline': b, 'skill': s,
                           'delta': s['reward']-b['reward']})

# Exhaust all score combinations of the five conflict cells; do not treat
# alternative records as additional tasks. This sensitivity stays in the audit.
scenarios = []
for rewards in product(*[sorted({x['reward'] for x in c['candidates']}) for c in conflicts]):
    alternative = dict(selected)
    for c, reward in zip(conflicts, rewards):
        k = c['variant_id'], c['condition']
        alternative[k] = {**selected[k], 'reward': reward}
    scenarios.append({m: summarize(m, alternative) for m in METHODS})
for m in METHODS:
    report['conflict_sensitivity'][m] = {
        metric: [min(s[m][metric] for s in scenarios), max(s[m][metric] for s in scenarios)]
        for metric in ['baseline_mean', 'skill_mean', 'delta', 'improved', 'regressed', 'tied']}
policy = {
    'historical_selection': 'Prefer literal valid status, then lexicographically first result path; preserve every conflict and evaluate all 32 conflicting-score combinations. Post-collection deterministic rule, independent of reward.',
    'recovery_selection': 'Use the 48 fixed recovery paths in r2/r3; replace the three inline-delivery cells with the completed file-reading repairs.',
    'interpretation': 'Descriptive full-record summary across recorded settings. Does not identify a uniform-protocol causal treatment effect or create new experimental runs.',
    'user_instruction': 'Modify source now; defer compilation, bilingual translation, difference PDFs and Zotero update until explicitly requested.',
    'sources': [{'path': str(p.relative_to(ROOT)), 'sha256': digest(p)} for p in [
        EXP / 'reviewed-recovery-coverage-20260920-user-exclusions-r2.json',
        EXP / 'reviewed-recovery-coverage-20260920-final-r3.json',
        EXP / 'reviewed-recovery-coverage-20260920-final-r5.json',
        OLD / 'formal-attempt-inventory-main-r33-20260920.json', OLD / 'coverage.json']],
    'conflicts': conflicts, 'superseded_inline_records': superseded}
for name, obj in [('statistics.json', report), ('selection-policy.json', policy),
                  ('selected-records.json', list(selected.values())), ('paired-scores.json', paired)]:
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
print(json.dumps(report, indent=2))
