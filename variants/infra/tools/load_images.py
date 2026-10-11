#!/usr/bin/env python3
"""Load the supplied exports and restore only their recorded image aliases."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def call(argv):
    return subprocess.check_output(argv, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--archive', type=Path, action='append', required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true', help='Images were already loaded with host-side decompression')
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text())
    info = json.loads(call(['docker', 'info', '--format', '{{json .}}']))
    if not any('containerd' in str(row) for row in info.get('DriverStatus', [])):
        raise RuntimeError('Use Docker 29 with the containerd image store; see README')
    verified = []
    for archive in args.archive:
        expected = catalog['archives'][archive.name]
        digest = hashlib.sha256()
        with archive.open('rb') as stream:
            for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                digest.update(block)
        if archive.stat().st_size != expected['bytes'] or digest.hexdigest() != expected['sha256']:
            raise ValueError('Image export checksum mismatch: ' + archive.name)
        if not args.verify_only:
            if archive.suffix == '.zst':
                decompress = subprocess.Popen(['zstd', '--long=31', '--decompress', '--stdout', str(archive)], stdout=subprocess.PIPE)
                try:
                    subprocess.run(['docker', 'image', 'load', '--platform', 'linux/amd64'], stdin=decompress.stdout, check=True)
                    decompress.stdout.close()
                    if decompress.wait() != 0:
                        raise RuntimeError('Image transport decompression failed')
                finally:
                    if decompress.poll() is None:
                        decompress.terminate()
                        decompress.wait()
            else:
                subprocess.run(['docker', 'image', 'load', '--platform', 'linux/amd64', '--input', str(archive)], check=True)
        verified.append(archive.name)
    ids = catalog['required_delivered_image_ids']
    rows = json.loads(call(['docker', 'image', 'inspect', *ids]))
    if {x['Id'] for x in rows} != set(ids):
        raise RuntimeError('Loaded image IDs differ from the recorded exports')
    if any(x['Architecture'] != 'amd64' or x['Os'] != 'linux' for x in rows):
        raise RuntimeError('The original deployment targets Linux/amd64')
    for tag, image in catalog['aliases'].items():
        if image not in ids or tag.startswith('sha256:'):
            raise ValueError('Invalid delivered image alias')
        subprocess.run(['docker', 'image', 'tag', image, tag], check=True)
    receipt = {'schema': 'skillsbench-variants-image-load.v1', 'docker_version': info['ServerVersion'],
               'loaded_archives': verified, 'verified_image_ids': sorted(ids),
               'aliases_restored': len(catalog['aliases']), 'model_calls': 0, 'grader_calls': 0}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'verified_image_ids'}))


if __name__ == '__main__':
    main()
