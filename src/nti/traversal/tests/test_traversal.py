#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import contains_string

from nose.tools import assert_raises

from zope import interface

from zope.location.interfaces import IRoot
from zope.location.interfaces import ILocation

from nti.traversal.traversal import resource_path

import zope.testing.loghandler

from nti.traversal.tests import TraversalLayerTest

class TestTraversal(TraversalLayerTest):

	def test_unicode_resource_path(self):

		@interface.implementer(IRoot)
		class Root(object):
			__parent__ = None
			__name__ = None

		@interface.implementer(ILocation)
		class Middle(object):
			__parent__ = Root()
			__name__ = u'Middle'

		@interface.implementer(ILocation)
		class Leaf(object):
			__parent__ = Middle()
			__name__ = u'\u2019'

		assert_that(resource_path(Leaf()),
					is_('/Middle/%E2%80%99'))

	def test_traversal_no_root(self):

		@interface.implementer(ILocation)
		class Middle(object):
			__parent__ = None
			__name__ = u'Middle'

		@interface.implementer(ILocation)
		class Leaf(object):
			__parent__ = Middle()
			__name__ = u'\u2019'

		log_handler = zope.testing.loghandler.Handler(None)
		log_handler.add('nti.traversal.traversal')
		try:
			with assert_raises(TypeError):
				resource_path(Leaf())
			record, = log_handler.records
			assert_that(record.getMessage(), contains_string("test_traversal.Middle"))
		finally:
			log_handler.close()
