from __future__ import unicode_literals
import dj_upload_to
import re
import pytest
import sys


@pytest.fixture
def ExampleModel():
    return type(
        'ExampleModel' if sys.version.startswith('3') else b'ExampleModel',
        (), {}
    )


@pytest.fixture
def up(ExampleModel):
    def inner(filename, **options):
        return dj_upload_to.UploadTo(**options)(ExampleModel(), filename)
    return inner


@pytest.mark.parametrize('option_name, value', [
    ('save_name', True),
    ('seg_size', 15),
    ('num_seg', 22),
    ('prefix', 'just-prefix')
])
def test_setter_test(option_name, value):
    upload_to_obj = dj_upload_to.UploadTo()
    setattr(upload_to_obj, option_name, value)
    assert value == getattr(upload_to_obj, option_name)


def test_autoprefix(up):
    assert 'examplemodel/file.txt' == up('file.txt', save_name=True)


def test_explicit_prefix(up):
    assert 'spam/file.exe' == up('file.exe', prefix='spam', save_name=True)


def test_no_prefix(up):
    assert 'file.exe' == up('file.exe', prefix=None, save_name=True)


def test_save_name(up):
    assert up('File.PnG', save_name=True).endswith('File.PnG')


def test_generate_name(up):
    assert up('File.PnG', save_name=False).endswith('.png')


def test_generate_name_with_custom_segment_numbers(up):
    filename = up('file.zip', save_name=False, num_seg=3)

    assert re.match(
        'examplemodel/[a-f0-9]{2}/[a-f0-9]{2}/[a-f0-9]{2}/[\-a-f0-9]{36}.zip',
        filename
    )


def test_generate_name_with_custom_segment_size(up):
    filename = up('file.zip', save_name=False, seg_size=4)

    assert re.match(
        'examplemodel/[a-f0-9]{4}/[a-f0-9]{4}/[\-a-f0-9]{36}.zip',
        filename
    )


def test_generate_name_without_segments(up):
    filename = up('file.zip', save_name=False, seg_size=0)
    assert re.match('examplemodel/[\-a-f0-9]{36}.zip', filename)


def test_deconstruct():
    upt = dj_upload_to.UploadTo(1, 2, 3, spam='egg')
    name, args, kwargs = upt.deconstruct()

    assert 'dj_upload_to.UploadTo' == name
    assert (1, 2, 3) == args
    assert {'spam': 'egg'} == kwargs
