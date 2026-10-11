#!/usr/bin/env python3
"""Restore hash-pinned deployment paths inside a private reproduction workspace."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def relative(path):
    parsed = PurePosixPath(path)
    if not parsed.is_absolute() or '..' in parsed.parts:
        raise ValueError('Invalid original deployment path')
    if not path.startswith(('/data/amax/', '/home/amax/')):
        raise ValueError('Deployment path outside the documented namespace')
    return Path(*parsed.parts[1:])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--tasks', type=Path, required=True, help='233 batch tasks directory')
    parser.add_argument('--materials', type=Path, required=True, help='Extracted deployment supplement')
    parser.add_argument('--actor-runtime', type=Path, required=True)
    parser.add_argument('--workspace', type=Path, required=True, help='New empty workspace')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    if manifest['variant_count'] != 233 or len(manifest['rows']) != 233:
        raise ValueError('Use MANIFEST-233.json with the 233 task archive')
    destination = args.workspace.absolute()
    destination.mkdir(parents=True, exist_ok=False)
    destination.chmod(0o700)
    (destination / 'engine-socket').mkdir(mode=0o700)
    rootfs = destination / 'rootfs'
    rootfs.mkdir()
    written = {}
    content = {}

    def install(source, original, expected, mode):
        target = rootfs / relative(original)
        if source.is_symlink() or not source.is_file():
            raise ValueError('Missing regular source: ' + str(source))
        if digest(source) != expected:
            raise ValueError('Source hash mismatch: ' + str(source))
        if original in written:
            if written[original] != (expected, mode):
                raise ValueError('Conflicting deployment aliases: ' + original)
            return
        if target.exists():
            raise ValueError('Unexpected existing deployment file: ' + original)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Copy, rather than link to input archives: consumers cannot mutate originals.
        shutil.copyfile(source, target)
        target.chmod(int(mode, 8))
        written[original] = (expected, mode)
        content.setdefault(expected, (source, mode))

    for row in manifest['rows']:
        task = args.tasks / row['variant_id']
        for item in row['files']:
            source = task / item['path']
            install(source, item['source'], item['sha256'], item['mode'])
            # A frozen historical file can have a different live source location.
            # Restore the archived bytes to that alias, never substitute live bytes.
            if item.get('live_source_snapshot_path'):
                install(source, item['live_source_snapshot_path'], item['sha256'], item['mode'])
        for prefix, original in [('public/', row['exact_public_source']),
                                 ('private/grader/', row['exact_grader_source'])]:
            for item in row['files']:
                if item['path'].startswith(prefix):
                    install(task / item['path'], original + '/' + item['path'][len(prefix):],
                            item['sha256'], item['mode'])

    source_index = json.loads((args.materials / 'metadata/SOURCE-FILES.json').read_text())
    for item in source_index['files']:
        install(args.materials / item['package_path'], item['original_path'],
                item['sha256'], item['mode'])
    actor = json.loads((args.materials / 'metadata/ACTOR-RUNTIME.json').read_text())
    for item in actor['files']:
        install(args.actor_runtime / item['relative_path'], item['source'],
                item['sha256'], item['mode'])

    aliases = json.loads((args.materials / 'metadata/DEPENDENCY-ALIASES.json').read_text())
    for original, expected in aliases.items():
        if original in written and written[original][0] == expected:
            continue
        if expected not in content:
            raise ValueError('Unresolved pinned deployment dependency: ' + original)
        source, mode = content[expected]
        install(source, original, expected, mode)

    (rootfs / 'data/amax/skillsbench-variants/runs').mkdir(parents=True, exist_ok=True)
    (rootfs / 'home/amax').mkdir(parents=True, exist_ok=True)
    result = {'schema': 'skillsbench-variants-workspace.v1', 'task_count': 233,
              'files_restored': len(written), 'input_manifest_sha256': digest(args.manifest),
              'workspace': str(destination), 'source_hashes_verified': True,
              'model_calls': 0, 'grader_calls': 0}
    (destination / 'prepared.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
