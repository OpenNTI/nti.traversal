#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

try:
	from pyramid.encode import url_quote
	url_quote = url_quote

except ImportError:

	from nti.traversal._compat import text_type
	from nti.traversal._compat import binary_type

	try:
		from urllib.parse import quote as _url_quote
	except ImportError:  # PY3
		from urllib import quote as _url_quote

	def url_quote(val, safe=''):
		cls = val.__class__
		if cls is text_type:
			val = val.encode('utf-8')
		elif cls is not binary_type:
			val = str(val).encode('utf-8')
		return _url_quote(val, safe=safe)
