import contextlib
import os
from pathlib import Path

import pytest

import readdbc

BLAST_FOLDER = Path('readdbc/blast')


@pytest.fixture(autouse=True)
def _remove_blastpy():
    def _remove():
        files = os.listdir(BLAST_FOLDER)
        for file in filter(lambda f: f.startswith('blastpy'), files):
            with contextlib.suppress(FileNotFoundError):
                (BLAST_FOLDER / file).unlink()
        with contextlib.suppress(FileNotFoundError):
            (BLAST_FOLDER / 'blast.o').unlink()

    _remove()
    yield
    _remove()


def test_fixture_blast_folder_starts_with_no_blastpy_files():
    files = os.listdir(BLAST_FOLDER)
    for file in files:
        assert not file.startswith('blastpy')


def test_build_returns_none():
    r = readdbc._build_blast()
    assert r is None


def test_build_creates_blastpy_lib():
    readdbc._build_blast()
    files = [f for f in os.listdir(BLAST_FOLDER) if f.startswith('blastpy')]
    assert len(files) > 0


def test_before_build_cant_import_blastpy():
    with pytest.raises(ModuleNotFoundError):
        __import__('readdbc.blast.blastpy')


def test_after_build_can_import_blastpy():
    readdbc._build_blast()
    __import__('readdbc.blast.blastpy')


def test_blastpy_has_dbc2dbf_function():
    readdbc._build_blast()
    assert hasattr(readdbc.blast.blastpy.lib, 'dbc2dbf')
