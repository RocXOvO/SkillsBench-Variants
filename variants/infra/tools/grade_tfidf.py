#!/usr/bin/env python3
"""Invoke the original TF-IDF P1/P2 host grader with a trusted snapshot receipt."""
import argparse
import json
import os
from pathlib import Path
import sys

IMAGES = {
    'parallel-tfidf-search--p1--dev-401': 'sha256:f807d85f5de5b182990065f80974ef51d57c0e8f2f9be5b0391b0ba307a0f9c3',
    'parallel-tfidf-search--p2--dev-401': 'sha256:0eaefb647eb7d40945a81b41862314f39a614d34f55b8b51f13782f4339a57ff',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-root', type=Path, required=True)
    parser.add_argument('--deployment', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--exclusive-lock', type=Path, required=True)
    args = parser.parse_args()
    if Path('/.dockerenv').exists():
        raise RuntimeError('Run this on the Linux host. The original TF-IDF grader rejects container controllers.')
    deployment = json.loads(args.deployment.read_text())
    variant = deployment['variant_id']
    if variant not in IMAGES or deployment['runtime_image_id'] != IMAGES[variant]:
        raise ValueError('TF-IDF variant and clean measurement environment do not match')
    entry = args.task_root / 'private/grader/test.sh'
    if not entry.is_file() or entry.is_symlink():
        raise ValueError('The original host entry is missing')
    # The original entry validates every science pin, the stopped snapshot,
    # its clean parent, all measurements, the exclusive lock and typed reward.
    # Its exit 75 / reward null is preserved without translating it into zero.
    os.execvp('bash', ['bash', str(entry), '--deployment', str(args.deployment),
                     '--run-dir', str(args.run_dir), '--exclusive-lock', str(args.exclusive_lock)])


if __name__ == '__main__':
    main()
