import os  # NOQA: D104
import subprocess
from pathlib import Path


class BlastError(Exception):
    '''
    Exception raised for errors raised by blast lib.

    Attributes
    ----------
    code: int
    message: str
    '''

    def __init__(self: 'BlastError', code: int, message: str) -> 'BlastError':
        self.code = code
        self.message = message
        super().__init__(f'{code=}    {message=}')


def to_dbf(src: [str, Path], dest: [str, Path] = None, /) -> None:
    '''
    Convert a source .dbc file to a .dbf destination file.

    Attributes
    ----------
    src: str, Path
        the file to read the .dbc from.
    dest: str, Path [optional]
        the file to write the .dbf to.
        if missing, then it will infer the same dir and filename as src

    Raises
    ------
    BlastError
        if the input file can't be processed by blast-dbf decompression tool
    '''

    src = Path(src)
    _check_file(name=src, extension='dbc')

    if dest is None:
        dest = str(src).replace('.dbc', '.dbf')
    dest = Path(dest)

    this_folder = Path(os.path.realpath(__file__)).parent
    blast_cmd = this_folder / 'blast-dbf'
    cmd = [
        blast_cmd,
        src,
        dest,
    ]
    proc = subprocess.run(cmd, capture_output=True, check=False)  # NOQA: S603
    if proc.returncode == 0:
        return None  # NOQA: RET501
    if proc.returncode > 0:
        dest.unlink()
        raise BlastError(
            code=proc.returncode, message=proc.stderr.decode('utf8'),
        )
    raise NotImplementedError


def _check_file(*, name: Path, extension: str) -> None:
    expected_end = '.' + extension.lower()
    if not str(name).lower().endswith(expected_end):
        msg =f'file "{name}" is expected to have {extension=}'
        raise ValueError(msg)
