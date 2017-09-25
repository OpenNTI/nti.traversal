#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Code taken from https://github.com/Pylons/pyramid

@see: https://github.com/Pylons/pyramid/blob/1.8-branch/pyramid/compat.py
@see: https://github.com/Pylons/pyramid/blob/1.8-branch/pyramid/encode.py
@see: https://github.com/Pylons/pyramid/blob/1.8-branch/pyramid/traversal.py
 
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six
from six.moves import urllib_parse

from repoze.lru import lru_cache

try:
    from pyramid.traversal import _segment_cache
except ImportError:
    _segment_cache = {}

try:
    from webob.request import PATH_SAFE as PATH_SEGMENT_SAFE
except ImportError:
    PATH_SEGMENT_SAFE = "/~!$&'()*+,;=:@"

logger = __import__('logging').getLogger(__name__)


def url_quote(val, safe=''):  # bw compat api
    cls = val.__class__
    if cls is six.text_type:
        val = val.encode('utf-8')
    elif cls is not six.binary_type:
        val = str(val).encode('utf-8')
    return urllib_parse.quote(val, safe=safe)


if six.PY2:
    def native_(s, encoding='latin-1', errors='strict'):
        """ 
        If ``s`` is an instance of ``text_type``, return
        ``s.encode(encoding, errors)``, otherwise return ``str(s)``
        """
        if isinstance(s, six.text_type):
            return s.encode(encoding, errors)
        return str(s)
else:
    def native_(s, encoding='latin-1', errors='strict'):
        """ 
        If ``s`` is an instance of ``text_type``, return
        ``s``, otherwise return ``str(s, encoding, errors)``
        """
        if isinstance(s, six.text_type):
            return s
        return str(s, encoding, errors)


if six.PY2:
    def quote_path_segment(segment, safe=PATH_SEGMENT_SAFE):
        """ 
        Return a quoted representation of a 'path segment'
        """
        try:
            return _segment_cache[(segment, safe)]
        except KeyError:
            if segment.__class__ is six.text_type:
                result = url_quote(segment.encode('utf-8'), safe)
            else:
                result = url_quote(str(segment), safe)
            _segment_cache[(segment, safe)] = result
            return result
else:
    def quote_path_segment(segment, safe=PATH_SEGMENT_SAFE):
        """ 
        Return a quoted representation of a 'path segment'
        """
        try:
            return _segment_cache[(segment, safe)]
        except KeyError:
            if segment.__class__ not in (six.text_type, six.binary_type):
                segment = str(segment)
            result = url_quote(native_(segment, 'utf-8'), safe)
            # we don't need a lock to mutate _segment_cache, as the below
            # will generate exactly one Python bytecode (STORE_SUBSCR)
            _segment_cache[(segment, safe)] = result
            return result


@lru_cache(1000)
def join_path_tuple(t):
    return t and '/'.join(quote_path_segment(x) for x in t) or '/'
