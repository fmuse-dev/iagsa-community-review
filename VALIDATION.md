# Companion preparation checks

Checked on 23 October 2026 before transfer to an external repository:

- Ten standard-library unit tests passed, including checksum/length mismatch, unsafe paths, duplicate members, symlinks, file/directory collisions, existing-output preservation, expansion limits and optimized-Python rejection.
- The preparation tool verified and extracted the exact 55,475,922-byte technical archive identified in the reviewer guide.
- The freshly extracted package's `run_review.py --mode recorded` returned `verified`: 329 inventory entries, 12 record sets, nine source profiles and 12 archives.
- The companion allowlist scan found no matching API-key/private-key patterns, preview tokens or lab project identifiers. This is a scoped scan of the companion files, not a claim about every historical artifact.

These checks validate companion packaging and recorded evidence consistency. They are not new scientific experiments or independent peer replication. No managed-cloud API, VM or hosted model was used by these local checks. The manuscript, evaluated source and frozen technical ZIP were not edited.

Run the companion checks with:

```bash
python3 -B -m unittest discover -s tests -v
```

The external repository's ordinary CI runs only these companion-tool tests. Scientific execution remains an explicit reviewer choice through the frozen technical package's instructions.
