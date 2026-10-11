#!/usr/bin/env python3
"""Freeze a stopped TF-IDF actor and invoke its host grader within one 900s budget."""
import argparse
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import time

from grade_tfidf import IMAGES

QUEUE = Path('/home/amax/spark-native-work/self-evo-skillsbench-20260926-r1/server_queue')
sys.dont_write_bytecode = True

FROZEN = Path('/data/amax/spark-repro/transfer-frozen-sources-V6dLhH')
SNAPSHOT_SHA = 'b97b19ec5271580ff9098b84808aeedf9c6007801b47109a2b596c28675ae671'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started = time.monotonic()
    end = started + 900
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=list(IMAGES), required=True)
    parser.add_argument('--solver-container', required=True)
    parser.add_argument('--mounts', type=Path, required=True, help='Trusted generation bind mounts: [[host_path, container_path], ...]')
    parser.add_argument('--provider-env', type=Path, required=True, help='Private 0600 scan input; see host protocol')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--exclusive-lock', type=Path, required=True)
    parser.add_argument('--condition', choices=['no_skill', 'skillrevise', 'spark', 'skillevolver', 'coevoskills'], default='no_skill')
    parser.add_argument('--agent-timeout', action='store_true')
    args = parser.parse_args()
    if Path('/.dockerenv').exists():
        raise RuntimeError('This entry requires a Linux host and its native Docker engine')
    output = args.output_dir.absolute()
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    task = Path('/home/amax/spark-native-work/skillrevise-variant-extension-20260924-r1/preflight/tfidf-integration-r6/staged') / args.variant / 'task-root'
    snapshot_path = QUEUE / 'tfidf_added_p1_snapshot_PREPARE_20261003_r1.py'
    if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != SNAPSHOT_SHA:
        raise ValueError('Original stopped-snapshot helper changed')
    sys.path[:0] = [str(task / 'private/grader/legacy'), str(FROZEN)]
    helper = load('original_tfidf_snapshot', snapshot_path)
    capture = load('original_bounded_capture', QUEUE / 'native_offer_capture_r4.py')

    def remaining():
        value = end - time.monotonic()
        if value <= 0:
            raise TimeoutError('The shared 900s verifier budget is exhausted')
        return value

    original_command = helper.command

    def command(argv, timeout=30):
        result = original_command(argv, timeout=min(timeout, remaining()))
        remaining()
        return result

    def bounded_export(name, archive):
        rc = capture.copy_stream(['docker', 'export', name], archive, Path(str(archive) + '.stderr'),
                                 helper.safe_docker_env(), end, cap=remaining(),
                                 stdout_limit=10240 * 1024 * 1024 + 65536, stderr_limit=65536)
        if rc != 0:
            raise RuntimeError('Bounded rootfs capture failed')
        remaining()

    helper.command = command
    helper.bounded_export = bounded_export
    try:
        receipt = output / 'snapshot.json'
        helper.freeze_stopped(args.solver_container,
                              {'runtime_image_id': IMAGES[args.variant], 'cpus': 8, 'memory_mb': 4096},
                              [(Path(p), target) for p, target in json.loads(args.mounts.read_text())],
                              receipt, args.provider_env)
        remaining()
        deployment = {'variant_id': args.variant, 'condition': args.condition, 'agent_timeout': args.agent_timeout,
                      'runtime_image_id': IMAGES[args.variant], 'snapshot_receipt': str(receipt),
                      'snapshot_sha256': hashlib.sha256(receipt.read_bytes()).hexdigest()}
        config = output / 'deployment.json'
        config.write_text(json.dumps(deployment, indent=2) + '\n')
        exit_code = capture.copy_stream(['bash', str(task / 'private/grader/test.sh'), '--deployment', str(config),
                                        '--run-dir', str(output / 'native'), '--exclusive-lock', str(args.exclusive_lock)],
                                       output / 'native.stdout', output / 'native.stderr', helper.safe_docker_env(),
                                       end, cap=remaining(), stdout_limit=16 * 1024 * 1024, stderr_limit=65536)
        remaining()
        status = json.loads((output / 'native/status.json').read_text())
        if exit_code == 0 and status['status'] == 'completed' and status['grader_completed'] is True:
            if type(status['reward']) is not int or status['reward'] not in (0, 1):
                raise ValueError('Invalid completed reward')
            if (output / 'native/reward.txt').read_text() != str(status['reward']) + '\n':
                raise ValueError('Reward publication mismatch')
        elif exit_code != 75 or status['reward'] is not None:
            raise RuntimeError('Host grader returned an unrecognized status')
        summary = {**status, 'whole_verifier_elapsed_seconds': time.monotonic() - started,
                   'whole_verifier_budget_seconds': 900, 'model_calls': 0,
                   'solver_cleanup_policy': 'caller retains its stopped solver and snapshot for audit'}
        (output / 'grade-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        print(json.dumps(summary))
        return exit_code
    except Exception as error:
        # Extra cleanup time cannot publish a score. Only this fresh run's
        # trusted probe receipts identify containers; never scan other runs.
        cleanup_errors = []
        for evidence in (output / 'native').glob('tasks/*/*/graded-artifacts/call-*/evidence.json'):
            try:
                value = json.loads(evidence.read_text())
                name = value['container_name']
                if not re.fullmatch(r'transfer-tfidf-probe-[0-9a-f]{16}', name):
                    raise ValueError('Unrecognized owned probe name')
                probe = subprocess.run(['docker', 'inspect', name], capture_output=True, text=True,
                                       timeout=10, env=helper.safe_docker_env())
                if probe.returncode == 0:
                    observed = json.loads(probe.stdout)[0]
                    if observed['Name'] != '/' + name or observed['Image'] != value['image_id']:
                        raise ValueError('Probe receipt and physical identity differ')
                    subprocess.run(['docker', 'rm', '-f', name], check=True, timeout=20,
                                   stdout=subprocess.DEVNULL, env=helper.safe_docker_env())
            except Exception as cleanup_error:
                cleanup_errors.append(type(cleanup_error).__name__)
        status = {'status': 'engineering_pending', 'reward': None, 'grader_completed': False,
                  'error': type(error).__name__ + ': ' + str(error), 'model_calls': 0,
                  'cleanup_errors': cleanup_errors}
        (output / 'grade-summary.json').write_text(json.dumps(status, indent=2) + '\n')
        print(json.dumps(status))
        return 75


if __name__ == '__main__':
    sys.exit(main())
