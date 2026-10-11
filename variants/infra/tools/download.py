#!/usr/bin/env python3
"""Download public, hash-pinned release packages with bounded temporary space."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import urllib.request


def copy_hashed(source, target, size=None):
    h = hashlib.sha256()
    remaining = size
    total = 0
    while remaining is None or remaining:
        block = source.read(min(4 * 1024 * 1024, remaining) if remaining is not None else 4 * 1024 * 1024)
        if not block:
            break
        h.update(block)
        total += len(block)
        if target is not None:
            target.write(block)
        if remaining is not None:
            remaining -= len(block)
    return total, h.hexdigest()


def download(package, folder):
    name = package['name']
    if Path(name).name != name:
        raise ValueError('Package filename must be a basename')
    final = folder / name
    if final.exists():
        with final.open('rb') as stream:
            observed = copy_hashed(stream, None)
        if observed != (package['bytes'], package['sha256']):
            raise ValueError('Existing output has a different hash: ' + name)
        print('verified ' + name, flush=True)
        return
    pending = folder / (name + '.partial')
    parts = package['parts']
    verified = 0
    boundary = 0
    if pending.exists():
        with pending.open('rb') as stream:
            for part in parts:
                if pending.stat().st_size - boundary < part['bytes']:
                    break
                if copy_hashed(stream, None, part['bytes']) != (part['bytes'], part['sha256']):
                    raise ValueError('Resume prefix is corrupt: ' + name)
                boundary += part['bytes']
                verified += 1
        with pending.open('r+b') as stream:
            stream.truncate(boundary)
    else:
        pending.touch(exist_ok=False)
    for index, part in enumerate(parts[verified:], verified + 1):
        block_file = folder / (name + '.part-download')
        for attempt in range(3):
            try:
                request = urllib.request.Request(part['url'], headers={'User-Agent': 'SkillsBench-Variants-reproduction/1'})
                with urllib.request.urlopen(request, timeout=120) as response, block_file.open('wb') as stream:
                    observed = copy_hashed(response, stream)
                if observed != (part['bytes'], part['sha256']):
                    raise ValueError('Release part hash mismatch: ' + part['name'])
                break
            except Exception:
                block_file.unlink(missing_ok=True)
                if attempt == 2:
                    raise
                time.sleep(1 + attempt)
        with block_file.open('rb') as source, pending.open('ab') as target:
            copy_hashed(source, target)
        block_file.unlink()
        print(name + ': ' + str(index) + '/' + str(len(parts)), flush=True)
    with pending.open('rb') as stream:
        observed = copy_hashed(stream, None)
    if observed != (package['bytes'], package['sha256']):
        raise ValueError('Complete archive hash mismatch: ' + name)
    pending.rename(final)
    print('verified ' + name, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=Path(__file__).resolve().parents[1] / 'metadata/PACKAGES.json')
    parser.add_argument('--group', choices=['infra', '233', '222', 'all'], default='all')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    for package in catalog['packages']:
        if args.group == 'all' or args.group in package['groups']:
            download(package, args.output)


if __name__ == '__main__':
    main()
