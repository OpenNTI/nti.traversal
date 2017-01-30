#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import sys
import types

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    text_type = str
    class_types = type,
    string_types = str,
    integer_types = int,
    binary_type = bytes
else:
    binary_type = str
    text_type = unicode
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)

if PY3:  # pragma: no cover
    def native_(s, encoding='latin-1', errors='strict'):
        """
        If ``s`` is an instance of ``text_type``, return
        ``s``, otherwise return ``str(s, encoding, errors)``
        """
        if isinstance(s, text_type):
            return s
        return str(s, encoding, errors)
else:
    def native_(s, encoding='latin-1', errors='strict'):
        """
        If ``s`` is an instance of ``text_type``, return
        ``s.encode(encoding, errors)``, otherwise return ``str(s)``
        """
        if isinstance(s, text_type):
            return s.encode(encoding, errors)
        return str(s)
