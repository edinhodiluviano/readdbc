import filecmp
import shutil
from pathlib import Path

import pytest

import readdbc


def test_when_convert_colebr15_dbc_returns_none(tmpdir):
    given = readdbc.dbc2csv('tests/COLEBR15.dbc', tmpdir / 'aaa')
    assert given is None


def test_convert_doesnt_accept_named_args():
    with pytest.raises(TypeError):
        readdbc.dbc2csv(src='', dest='')


def test_convert_with_invalid_dbc_file_raises_error(tmpdir):
    source = tmpdir / 'aaa.dbc'
    dest = tmpdir / 'aaa.csv'
    with open(source, 'wb') as f:
        f.write(b'abc')
    with pytest.raises(readdbc.BlastError):
        readdbc.dbc2csv(source, dest)


def test_convert_with_invalid_dbc_create_no_dest_file(tmpdir):
    source = tmpdir / 'aaa.dbc'
    dest = tmpdir / 'aaa.csv'
    with open(source, 'wb') as f:
        f.write(b'abc')
    with pytest.raises(readdbc.BlastError):
        readdbc.dbc2csv(source, dest)
    assert not dest.exists()



def test_convert_doesnt_accept_non_dbc_extension_input_file(tmpdir):
    original_source = 'tests/COLEBR15.csv'
    source = tmpdir / 'COLEBR15.csv'
    shutil.copyfile(original_source, source)
    with pytest.raises(ValueError):
        readdbc.dbc2csv(source, tmpdir / 'aaa')


files = ['COLEBR15', 'DIFTBR20', 'PAIRBR06']


@pytest.mark.parametrize('file', files)
def test_when_convert_file_dbc_contents_matches_file_csv(file, tmpdir):
    source = f'tests/{file}.dbc'
    dest = tmpdir / 'bbb'
    compare = f'tests/{file}.csv'
    readdbc.dbc2csv(source, dest)
    assert filecmp.cmp(dest, compare)


@pytest.mark.parametrize('file', files)
def test_convert_behave_the_same_with_path(file, tmpdir):
    source = f'tests/{file}.dbc'
    dest = tmpdir / 'bbb'
    compare = f'tests/{file}.csv'
    readdbc.dbc2csv(Path(source), Path(dest))
    assert filecmp.cmp(dest, compare)


@pytest.mark.parametrize('file', files)
def test_when_convert_without_dest_infer_by_source(file, tmpdir):
    original_source = f'tests/{file}.dbc'
    source = tmpdir / f'{file}.dbc'
    shutil.copyfile(original_source, source)
    readdbc.dbc2csv(source)
    expected_dest_file = tmpdir / f'{file}.csv'
    compare = f'tests/{file}.csv'
    assert filecmp.cmp(expected_dest_file, compare)
