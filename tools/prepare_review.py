"""Verify and extract the frozen IAGSA technical ZIP; never execute its contents."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import zipfile

EXPECTED_SHA256 = '4cff58336a0a2c01eb5be1dbf69ca393e0b790609099dcdaad9a06e8fc54db48'
EXPECTED_BYTES = 55_475_922
MAX_MEMBERS = 10_000
MAX_EXPANDED = 800_000_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_members(archive):
    members = archive.infolist()
    require(0 < len(members) <= MAX_MEMBERS, 'Invalid ZIP member count')
    require(sum(m.file_size for m in members) <= MAX_EXPANDED, 'ZIP expands beyond limit')
    seen = set()
    files = set()
    for member in members:
        name = member.filename
        path = PurePosixPath(name)
        require(name and not path.is_absolute() and '..' not in path.parts
                and '\\' not in name and ':' not in name and path.parts
                and name.rstrip('/') == path.as_posix(), 'Unsafe ZIP member path')
        normalized = path.as_posix()
        require(normalized not in seen, 'Duplicate ZIP member')
        seen.add(normalized)
        mode = member.external_attr >> 16
        require(stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR), 'Special ZIP member')
        require(not (member.flag_bits & 1), 'Encrypted ZIP member')
        if not member.is_dir():
            files.add(normalized)
    for name in seen:
        require(all(p.as_posix() not in files for p in PurePosixPath(name).parents
                    if p.as_posix() != '.'), 'File/directory collision')
    require(archive.testzip() is None, 'ZIP CRC failure')


def prepare(source, target, expected_sha256=EXPECTED_SHA256, expected_bytes=EXPECTED_BYTES):
    require(not target.exists() and not target.is_symlink(), 'Output must not already exist')
    # Hold one file descriptor through verification and extraction.
    with source.open('rb') as stream:
        digest = hashlib.sha256()
        length = 0
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            length += len(chunk)
            digest.update(chunk)
        require(length == expected_bytes, 'Archive length mismatch')
        require(digest.hexdigest() == expected_sha256, 'Archive SHA-256 mismatch')
        stream.seek(0)
        with zipfile.ZipFile(stream) as archive:
            validate_members(archive)
            target.mkdir(parents=True, exist_ok=False)
            try:
                archive.extractall(target)
            except BaseException:
                shutil.rmtree(target)
                raise
    return length


def main():
    require(__debug__ and not sys.flags.optimize, 'Optimized Python is not supported')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    length = prepare(args.archive, args.output)
    print(f'Archive verified and extracted: {length} bytes. No experiment was executed.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('REJECTED:', error, file=sys.stderr)
        sys.exit(1)
