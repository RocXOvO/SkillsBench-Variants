#!/usr/bin/env python3
"""Show the authoritative deployment binding for one exported task."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('variant_id')
    parser.add_argument('--metadata', type=Path, default=Path(__file__).resolve().parents[1] / 'metadata/DEPLOYMENT-233.json')
    args = parser.parse_args()
    manifest = json.loads(args.metadata.read_text())
    matches = [x for x in manifest['rows'] if x['variant_id'] == args.variant_id]
    if len(matches) != 1:
        raise ValueError('Task ID is not in the 233 batch')
    print(json.dumps(matches[0], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
