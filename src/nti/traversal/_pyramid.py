#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import warnings

try:
	from pyramid.traversal import find_interface as p_find_interface
	from pyramid.traversal import _join_path_tuple as p_join_path_tuple

	p_find_interface = p_find_interface
	p_join_path_tuple = p_join_path_tuple

except ImportError:
	warnings.warn('pyramid not available')

	from nti.traversal._compat import PY3
	from nti.traversal._compat import native_
	from nti.traversal._compat import text_type
	from nti.traversal._compat import binary_type

	from .encode import url_quote

	from .location import find_interface as p_find_interface

	_segment_cache = {}

	if PY3:  # pragma: no cover
		def quote_path_segment(segment, safe=''):
			try:
				return _segment_cache[(segment, safe)]
			except KeyError:
				if segment.__class__ not in (text_type, binary_type):
					segment = str(segment)
				result = url_quote(native_(segment, 'utf-8'), safe)

				_segment_cache[(segment, safe)] = result
				return result
	else:
		def quote_path_segment(segment, safe=''):
			try:
				return _segment_cache[(segment, safe)]
			except KeyError:
				if segment.__class__ is text_type:
					result = url_quote(segment.encode('utf-8'), safe)
				else:
					result = url_quote(str(segment), safe)

				_segment_cache[(segment, safe)] = result
			return result

	def p_join_path_tuple(t):
		return t and '/'.join([quote_path_segment(x) for x in t]) or '/'
