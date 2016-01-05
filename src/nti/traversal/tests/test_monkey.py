#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from nose.tools import assert_raises

from zope import interface

from zope.traversing import api as trv_api
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError

import nti.traversal.monkey

from nti.traversal.tests import TraversalLayerTest

class TestMonkey(TraversalLayerTest):

	def test_patched_traversal_api(self):
		assert nti.traversal.monkey._patched_traversing, "No fixed version exists"

		@interface.implementer(ITraversable)
		class BrokenTraversable(object):
			def traverse(self, name, furtherPath):
				getattr(self, u'\u2019', None)  # Raise unicode error

		with assert_raises(TraversalError):
			# Not a unicode error
			trv_api.traverseName(BrokenTraversable(), '')

		assert_that(trv_api.traverseName(BrokenTraversable(), '', default=1), is_(1))

		with assert_raises(TraversalError):
			# Not a unicode error
			trv_api.traverseName(object(), u'\u2019')

		assert_that(trv_api.traverseName(object(), u'\u2019', default=1), is_(1))

		with assert_raises(TraversalError):
			# Not a unicode error
			trv_api.traverseName({}, u'\u2019')

		assert_that(trv_api.traverseName({}, u'\u2019', default=1), is_(1))

		# Namespacing works. Note that namespace traversal ignores default values
		with assert_raises(TraversalError):
			assert_that(trv_api.traverseName({}, u'++foo++bar', default=1), is_(1))
