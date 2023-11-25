import os
import subprocess
from pathlib import Path


class BlastError(Exception):
    """Exception raised for errors raised by blast lib.

    Attributes:
        code: int
        message: str
    """

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f'{code=}    {message=}')


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
    elif proc.returncode == 2:
        os.remove(dest)
        raise BlastError(
            code=proc.returncode, message=proc.stderr.decode('utf8')
        )
    raise NotImplementedError()


def _check_file(*, name: Path, extension: str):
    expected_end = '.' + extension.lower()
    if not str(name).lower().endswith(expected_end):
        raise ValueError(f'file "{name}" is expected to have {extension=}')
