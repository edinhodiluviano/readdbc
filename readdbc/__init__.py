import os
import subprocess
from pathlib import Path


def to_dbf(src: [str, Path], dest: [str, Path] = None, /):
    src = Path(src)
    _check_file(name=src, extension='dbc')

    if dest is None:
        dest = str(src).replace('.dbc', '.dbf')
    dest = Path(dest)

    this_folder = Path(os.path.dirname(os.path.realpath(__file__)))
    blast_cmd = this_folder / 'blast-dbf'
    cmd = [
        blast_cmd,
        src,
        dest,
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode == 0:
        return None


def _check_file(*, name: Path, extension: str):
    expected_end = '.' + extension.lower()
    if not str(name).lower().endswith(expected_end):
        raise ValueError(f'file "{name}" is expected to have {extension=}')
