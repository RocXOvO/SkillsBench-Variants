# Two SkillsBench variant source archives

The 233-variant batch used by Generic, SkillLearn, Trace, and SkillRevise and the historical 222-variant batch used by CoEvoSkills, SPARK, and SkillEvolver were exported to the local machine on 2026-10-11.

| Batch | Source tasks | P1 / P2 / P3 | Task files | Compressed bytes |
|---|---:|---|---:|---:|
| Four methods: 233 variants | 81 | 81 / 71 / 81 | 13,088 | 6,064,275,010 |
| Historical three methods: 222 variants | 77 | 77 / 68 / 77 | 12,086 | 5,487,309,013 |

Every logical task file in each archive was checked against the manifest's SHA256, size, and mode. The complete compressed archive hashes match the server receipts. Credential filename and high-confidence credential-pattern checks returned no matches.

The private repository's [dataset release](https://github.com/RocXOvO/ICLR-paper/releases/tag/variant-datasets-20261011) holds 46 and 41 binary volumes, respectively and their manifests, SHA256 checksums, validation reports, and Chinese download/extraction instructions. Each volume is at most 128 MiB. Binary archives and raw experiment workspaces remain outside Git history; this directory holds derived provenance records only.

The complete local archives are under `output/variant-packages-20261011/`. To reconstruct downloaded release volumes:

```sh
cat variant-tasks-233-20261010.tar.gz.chunk-* > variant-tasks-233-20261010.tar.gz
cat variant-tasks-222-20261011.tar.gz.chunk-* > variant-tasks-222-20261011.tar.gz
shasum -a 256 -c SHA256SUMS
tar -xzf variant-tasks-233-20261010.tar.gz
tar -xzf variant-tasks-222-20261011.tar.gz
```

The sets share 213 variant IDs; their ID-only differences are recorded in `batches.json`. Shared IDs do not certify identical package versions. Historical constructor packages and located public/grader stages are recorded separately in the 222 archive; this is a source export and does not establish one uniform historical evaluation protocol. Its SPARK and CoEvoSkills result inventories have 221 selected results each because audiobook P3 was excluded for those methods; SkillEvolver and no-skill inventories have 222.

The 233 archive preserves the previously corrected TF-IDF P3 test.sh source pin. Its per-variant provenance amendment was explicitly bound to the external manifest during verification. Five extension variants (edit-pdf P1/P2/P3 and radar-vital-signs P1/P3) place their build context under `public/Dockerfile` and `public/root/` rather than `environment/`.

Both complete archives were downloaded and validated locally before the final transfer. After slow local uplink transfers, identical source-side volumes were used for upload. Each server-side volume was independently matched to the local SHA256 before uploading.

No task/model evaluation, skill evolution, manuscript edit, or online Overleaf modification occurred.
