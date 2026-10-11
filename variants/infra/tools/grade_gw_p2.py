#!/usr/bin/env python3
"""Grade frozen GW P2 CSV output with the recovered historical-context environment."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode = True

FROZEN = Path('/data/amax/spark-repro/transfer-frozen-sources-V6dLhH')
PLAN = Path('/home/amax/spark-native-work/self-evo-skillsbench-20260926-r1/server_queue/ordinary-skill-233-20261009-r1/input-plan-r2.json')
VARIANT = 'gravitational-wave-detection--p2--dev-401'
IMAGE = 'sha256:3b50e63f024f63379f64ae274c4441931c3e452b998f7ac9774dbcaacf3606eb'


def main():
    end = time.monotonic() + 240
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solver-container', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.absolute()
    if not output.is_relative_to('/data/amax/skillsbench-variants/runs'):
        raise ValueError('Use the mounted fresh run directory')
    cell = next(r for r in json.loads(PLAN.read_text())['rows'] if r['variant_id'] == VARIANT)['source_record']['cell']
    state = json.loads(subprocess.check_output(['docker', 'inspect', args.solver_container], timeout=max(.01, end - time.monotonic())))[0]
    if state['Image'] != cell['solver_image'] or state['Config'].get('Labels', {}).get('skillsbench-variants.variant') != VARIANT:
        raise ValueError('Solver image or variant label mismatch')
    if state['State']['Running'] or state['State']['Pid'] or state['State']['OOMKilled'] or state['State']['Error']:
        raise ValueError('A stopped, healthy solver is required')
    private = Path(cell['grader_path'])
    for name, digest in cell['grader_files'].items():
        if hashlib.sha256((private / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Frozen grader file changed')
    output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(FROZEN))
    spec = importlib.util.spec_from_file_location('original_gw_capture', FROZEN / 'transfer_quantum_capture.py')
    capture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(capture)
    _, receipt = capture.capture_stopped_outputs(args.solver_container, output / 'capture', end,
                                                 filenames=('detection_results.csv',), locations=('root',))
    (output / 'capture-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    logs = output / 'logs'
    logs.mkdir()
    logs.chmod(0o777)
    name = 'sbv-gw-grader-' + uuid.uuid4().hex[:16]
    argv = ['docker', 'create', '--name', name, '--label', 'skillsbench-variants.grader=' + VARIANT,
            '--network', 'none', '--read-only', '--cpus', '8', '--memory', '8192m', '--pids-limit', '512',
            '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges', '--tmpfs', '/tmp:rw,nosuid,size=128m', '--workdir', '/root']
    for source, target, readonly in [(private, '/opt/grader', True), (output / 'capture/root', '/capture', True), (logs, '/logs/verifier', False)]:
        argv += ['--mount', 'type=bind,src=' + str(source) + ',dst=' + target + (',readonly' if readonly else '')]
    subprocess.run(argv + [IMAGE, 'python', '-I', '/opt/grader/run.py'], check=True, stdout=subprocess.DEVNULL,
                   timeout=max(.01, end - time.monotonic()))
    try:
        subprocess.run(['docker', 'start', '-a', name], timeout=max(.01, end - time.monotonic()), check=True)
        if time.monotonic() >= end:
            raise TimeoutError('The shared 240s verifier budget is exhausted')
        result = json.loads((logs / 'committed.json').read_text())
        if result['status'] == 'completed' and type(result['reward']) is int and result['reward'] in (0, 1):
            if (logs / 'reward.txt').read_text() != str(result['reward']) + '\n':
                raise ValueError('Reward publication mismatch')
            exit_code = 0
        else:
            if result.get('reward') is not None:
                raise ValueError('Unrecognized grader result')
            exit_code = 75
    finally:
        try:
            subprocess.run(['docker', 'rm', '-f', name], check=True, stdout=subprocess.DEVNULL,
                           timeout=max(.01, min(30, end - time.monotonic())))
        except Exception:
            # Emergency cleanup does not turn a verifier timeout into a valid score.
            subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            raise
        if time.monotonic() >= end:
            raise TimeoutError('Cleanup exceeded the shared 240s verifier budget')
    print(json.dumps(result))
    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({'status': 'engineering_invalid', 'reward': None,
                          'grader_completed': False, 'error': type(error).__name__ + ': ' + str(error)}))
        sys.exit(75)
