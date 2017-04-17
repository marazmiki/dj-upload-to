# coding: utf-8

from __future__ import unicode_literals
import uuid
import os


__version__ = '2.0.0'
__all__ = ['UploadTo', 'upload']


not_provided = object()


class UploadTo:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, model_instance, filename):
        bits = self.get_filename(model_instance, filename)
        prefix = self.get_prefix(model_instance, filename)
        bits.insert(0, prefix)

        return os.path.join(*bits)

    @property
    def save_name(self):
        """
        Don't generate filename, keep original one
        """
        return self.kwargs.get('save_name', False)

    @save_name.setter
    def save_name(self, new_value):
        """
        Don't generate filename, keep original one
        """
        self.kwargs['save_name'] = new_value

    @property
    def num_seg(self):
        """
        Number of segments to be used
        """
        return self.kwargs.get('num_seg', 2)

    @num_seg.setter
    def num_seg(self, new_value):
        """
        Number of segments to be used
        """
        self.kwargs['num_seg'] = new_value

    @property
    def seg_size(self):
        """
        Length of each of segment, in chars
        """
        return self.kwargs.get('seg_size', 2)

    @seg_size.setter
    def seg_size(self, new_value):
        """
        Length of each of segment, in chars
        """
        self.kwargs['seg_size'] = new_value

    @property
    def prefix(self):
        """
        In what directory do you plan upload files?
        """
        return self.kwargs.get('prefix', not_provided)

    @prefix.setter
    def prefix(self, new_value):
        self.kwargs['prefix'] = new_value

    def deconstruct(self):
        """
        Makes django to able to use that function for migrations creation.

        According documentation (please see https://goo.gl/uAri6l) it should
        return tuple of:

        - full function name,
        - a list of all numeral arguments,
        - a dictionary of all keyword arguments.

        :return: tuple
        """
        return 'dj_upload_to.UploadTo', self.args, self.kwargs

    def get_extension(self, model_instance, filename):
        """
        Returns an extension from given `filename`

        This made as class method to make user able to override
        extension obtaining logic. In most cases there isn't required
        although.

        :param model_instance:
        :type model_instance: django.db.models.base.ModelBase:
        :param filename:
        :type filename: str
        :return: str
        """
        return os.path.splitext(filename)[1].lower().strip('.')

    def get_trusted_filename(self, model_instance, filename):
        """
        Returns a generated filename (exclude extension) generated
        by ourselves and thus trusted.

        At the default implementation it's not depends from some field in
        model instance, but you're free to use, let's say file content
        checksum taken from `model_instance` as trusted filename.

        :param model_instance:
        :type model_instance: django.db.models.base.ModelBase
        :param filename:
        :type filename: str
        :return:
        """
        return '{}'.format(uuid.uuid4())

    def get_filename(self, model_instance, filename):
        """
        Returns list of all bits of generated filename

        :param model_instance:
        :type model_instance: django.db.models.base.ModelBase
        :param filename:
        :type filename: str
        :return:
        """
        if self.save_name:
            return [filename]
        basename = '{name}.{extension}'.format(
            name=self.get_trusted_filename(model_instance, filename),
            extension=self.get_extension(model_instance, filename),
        )
        bits = []
        if self.num_seg and self.seg_size:
            bits.extend(self.get_segments(model_instance, basename))
        bits.append(basename)
        return bits

    def get_prefix(self, model_instance, filename):
        """
        Returns prefix (namespace) for saved file

        :param model_instance:
        :type model_instance: django.db.models.base.ModelBase
        :param filename:
        :type filename: str
        :return: str
        """
        return {
            not_provided: model_instance.__class__.__name__.lower(),
            None: '',
        }.get(self.prefix, self.prefix)

    def get_segments(self, model_instance, filename):
        """
        Returns list of segments based on settings.
        Generates list of `num_seg` strings length of `seg_size`.

        :param model_instance:
        :type model_instance: django.db.models.base.ModelBase
        :param filename:
        :type filename: str
        :return:
        """
        return [filename[i * self.seg_size:(i + 1) * self.seg_size]
                for i in range(self.num_seg)]


upload = UploadTo(save_name=False, num_seg=2, seg_size=2)
