#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import dj_upload_to
import unittest


def up(filename, **options):
    return dj_upload_to.UploadTo(**options)(ExampleModel(), filename)


class ExampleModel(object):
    pass


class Test(unittest.TestCase):
    def test_autoprefix(self):
        self.assertEquals('examplemodel/file.txt', up('file.txt',
                                                      prefix=None,
                                                      save_name=True))

    def test_explicit_prefix(self):
        self.assertEquals('spam/file.exe', up('file.exe',
                                              prefix='spam',
                                              save_name=True))

    def test_save_name(self):
        self.assertTrue(up('File.PnG', save_name=True).endswith('.PnG'))

    def test_generate_name(self):
        self.assertTrue(up('File.PnG', save_name=False).endswith('.png'))

    def test_generate_name_with_custom_segment_numbers(self):
        filename = up('file.zip', save_name=False, num_seg=3)
        self.assertEquals(4, filename.count('/'))

    def test_generate_name_with_custom_segment_size(self):
        filename = up('file.zip', save_name=False, seg_size=4).split('/')
        self.assertEquals(4, len(filename))
        self.assertEquals(4, len(filename[1]))
        self.assertEquals(4, len(filename[2]))

    def test_generate_name_without_segments(self):
        filename = up('file.zip', save_name=False, seg_size=0).split('/')
        self.assertEquals(2, len(filename))
        self.assertEquals('examplemodel', filename[0])
        self.assertTrue(filename[1].endswith('.zip'))


def main():
    """
    Main test module, used as entry point from setup.py
    """
    unittest.main()

if __name__ == '__main__':
    main()
