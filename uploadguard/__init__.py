# -*- coding: utf-8 -*-
"""
Plupload and Resumable.js plugin.
"""
from __future__ import unicode_literals

VERSION = (0, 1, 0, 'dev')

__version__ = '.'.join((str(each) for each in VERSION[:4]))

def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    return '.'.join((str(each) for each in VERSION[:4]))
