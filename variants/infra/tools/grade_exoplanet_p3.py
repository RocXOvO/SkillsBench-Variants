#!/usr/bin/env python3
"""Call the recovered official Exoplanet P3 stopped-output grader exactly once."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

FROZEN = Path('/data/amax/spark-repro/transfer-frozen-sources-V6dLhH')
PLAN = Path('/home/amax/spark-native-work/self-evo-skillsbench-20260926-r1/server_queue/ordinary-skill-233-20261009-r1/input-plan-r2.json')
VARIANT = 'exoplanet-detection-period--p3--dev-401'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solver-container', required=True)
    parser.add_argument('--output-dir', type=Path, required=True, help='New directory under /data/amax/skillsbench-variants/runs')
    parser.add_argument('--condition', default='external')
    args = parser.parse_args()
    output = args.output_dir.absolute()
    if not output.is_relative_to('/data/amax/skillsbench-variants/runs'):
        raise ValueError('Use the mounted fresh run directory')
    state = json.loads(subprocess.check_output(['docker', 'inspect', args.solver_container]))[0]
    if state['State']['Running'] or state['State']['Pid'] or state['State']['OOMKilled'] or state['State']['Error']:
        raise ValueError('A stopped, healthy solver is required')
    if state['Config'].get('Labels', {}).get('skillsbench-variants.variant') != VARIANT:
        raise ValueError('Solver variant label mismatch')
    output.mkdir(parents=True, exist_ok=False)
    row = next(x for x in json.loads(PLAN.read_text())['rows'] if x['variant_id'] == VARIANT)
    if state['Image'] != row['source_record']['cell']['solver_image']:
        raise ValueError('Solver image differs from the frozen deployment binding')
    cell = {**row['source_record']['cell'], 'condition': args.condition}
    # This receipt identifies a newly supplied stopped solver. No historical
    # model result, prediction, answer or reward is used by this entry point.
    receipt = output / 'solver-receipt.json'
    receipt.write_text(json.dumps({'solver_container': args.solver_container}) + '\n')
    sys.path.insert(0, str(FROZEN))
    spec = importlib.util.spec_from_file_location('official_exoplanet_p3', FROZEN / 'grade_ready_exoplanet_p3.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.one((cell, receipt))
    print(json.dumps(result))
    return 0 if result.get('status') == 'valid' else 75


if __name__ == '__main__':
    sys.exit(main())
