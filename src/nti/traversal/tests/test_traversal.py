#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import contains_string

import unittest

from zope import interface

from zope.location.interfaces import IRoot
from zope.location.interfaces import ILocation

from nti.traversal.traversal import resource_path
from nti.traversal.traversal import ContainerAdapterTraversable

import zope.testing.loghandler

from nti.traversal.tests import SharedConfiguringTestLayer


class TestTraversal(unittest.TestCase):

    layer = SharedConfiguringTestLayer

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
            with self.assertRaises(TypeError):
                resource_path(Leaf())
            record, = log_handler.records
            assert_that(record.getMessage(),
                        contains_string(".Middle"))
        finally:
            log_handler.close()

    def test_adapter_traversable(self):
        @interface.implementer(ILocation)
        class Middle(object):
            __parent__ = None
            __name__ = u'Middle'
        mid = Middle()
        c = ContainerAdapterTraversable(mid)
        assert_that(c, has_property('context', is_(mid)))
        assert_that(c, has_property('_container', is_(mid)))
        c.context = None
        assert_that(c, has_property('context', is_(none())))
        assert_that(c, has_property('_container', is_(none())))
