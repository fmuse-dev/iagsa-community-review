# Reviewer and reproduction guide

## 1. Obtain the frozen evidence

Open https://doi.org/10.5281/zenodo.23595879 and download the technical review ZIP. The paper PDF is separate. This companion is prepared against this exact technical archive:

- Filename: `IAGSA_Technical_Review_Package.zip`
- Size: 55,475,922 bytes
- SHA-256: `4cff58336a0a2c01eb5be1dbf69ca393e0b790609099dcdaad9a06e8fc54db48`

The digest identifies the prepared manuscript-free technical package. If the uploaded file differs, stop and report the mismatch; do not edit the expected digest to make it pass. A renamed file with identical bytes is acceptable. A recompressed ZIP is a different artifact. Publication and file availability depend on the author completing the Zenodo record.

## 2. Verify and extract without credentials

Use Python 3.12 on a disposable local workspace. From this companion's root:

```bash
python3 -B tools/prepare_review.py --archive /path/to/IAGSA_Technical_Review_Package.zip --output ../iagsa-review-input
```

The tool checks length, SHA-256, CRC, member paths, duplicates, file types and expansion limits before extraction. The output directory must not already exist. It does not execute archive code or make network requests. Keep the companion and its tests outside the extracted package.

Then run the package's recorded-data verifier:

```bash
python3 -B ../iagsa-review-input/IAGSA_Technical_Review_Package/run_review.py --mode recorded
```

Expected: `status: verified`. The verification covers the complete file inventory, source hashes, recorded case identities and specified outcome consistency. It is **not a new experiment**. Do not use Python `-O` or `-OO`.

## 3. Choose an execution route

Follow the extracted `START_HERE.md` for exact commands. Do not mix source revisions or historical and current container hashes.

| Route | Requirements | Meaning |
| --- | --- | --- |
| Recorded verification | Standard-library Python; no credentials | Integrity and consistency of retained author-produced records |
| Local T/G subset | Linux, pinned Python dependencies and hash-checked OPA download | Fresh T05, G1–G4, G5a and G6 execution |
| All nine local source profiles | Disposable Linux host with root and worker-UID switching | Adds T01, T03, T08a, full T08b1 and G7 |
| C9 reader and C10 | Historical technical package's reviewer instructions | Separate integrated-flow and contract checks; distinguish scripted calibration from actual model calls |
| Managed-cloud or hosted-model experiments | Independently provisioned resources, permissions and credentials | New external execution; may incur provider charges |

Environment setup may download dependencies; recorded verification is offline. Write environments, new outputs and reports outside the extracted package. A worker-identity preflight failure is `not_executed`, not a pass. Do not weaken identity separation to force completion.

## 4. Submit a useful result

Include source/profile identity, archive digest, Python/OS versions, exact command, privilege preflight, raw output, exit code and the independently observed resource/evidence outcome. Exclude credentials and personal data. Label an altered scenario as an extension, not an exact reproduction. Identify whether the run was author-operated or independently conducted.
