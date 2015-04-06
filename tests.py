#!/usr/bin/env python
# coding: utf-8

import dj_upload_to
import unittest
import re


UUID_RE = re.compile(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', re.I)


def up(filename, **options):
    return dj_upload_to.UploadTo(**options)(ExampleModel(), filename)


class ExampleModel(object):
    pass


class Test(unittest.TestCase):
    def test_1(self):
        self.assertEquals('examplemodel/file.txt', up('file.txt',
                                                      prefix=None,
                                                      save_name=True))

    def test_2(self):
        self.assertEquals('spam/file.exe', up('file.exe',
                                              prefix='spam',
                                              save_name=True))

    def test_3(self):
        self.assertTrue(up('File.PnG', save_name=True).endswith('.PnG'))

    def test_4(self):
        self.assertTrue(up('File.PnG', save_name=False).endswith('.png'))

    def test_5(self):
        filename = up('file.zip', save_name=False, num_seg=3)
        self.assertEquals(4, filename.count('/'))

    def test_6(self):
        filename = up('file.zip', save_name=False, seg_size=4).split('/')
        self.assertEquals(4, len(filename))
        self.assertEquals(4, len(filename[1]))
        self.assertEquals(4, len(filename[2]))


def main():
    """
    Main test module, used as entry point from setup.py
    """
    unittest.main(exit=True)


if __name__ == '__main__':
    main()
