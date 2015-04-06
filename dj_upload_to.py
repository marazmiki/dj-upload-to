# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import uuid
import os


__version__ = '1.0.0'


class UploadTo(object):
    def __init__(self, prefix=None, num_seg=2, seg_size=2, hash_name=True,
                 save_name=False):
        self.num_seg = num_seg
        self.seg_size = seg_size
        self.prefix = prefix
        self.hash_name = hash_name
        self.save_name = save_name

    def __call__(self, model_instance, filename):
        bits = self.get_filename(model_instance, filename)
        prefix = self.get_prefix(model_instance, filename)
        bits.insert(0, prefix)

        return os.path.join(*bits)

    def get_filename(self, model_instance, filename):
        if self.save_name:
            return [filename]

        extension = os.path.splitext(filename)[1].lower().strip('.')
        fname = '{}.{}'.format(uuid.uuid4(), extension)

        bits = []
        if self.num_seg and self.seg_size:
            bits.extend(self.get_segments(model_instance, fname))
        bits.append(fname)
        return bits

    def get_prefix(self, model_instance, filename):
        """
        Returns prefix (namespace) for saved file

        :param model_instance: models.Model
        :param filename: str
        :return: str
        """
        return self.prefix or model_instance.__class__.__name__.lower()

    def get_segments(self, model_instance, filename):
        return [filename[i * self.seg_size:(i + 1) * self.seg_size]
                for i in range(self.num_seg)]
