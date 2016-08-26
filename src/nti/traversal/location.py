#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

try:
	from pyramid.location import lineage
	from pyramid.traversal import find_interface

	lineage = lineage
	find_interface = find_interface
except ImportError:

	from zope.interface.interfaces import IInterface

	def lineage(resource):
		while resource is not None:
			yield resource
			try:
				resource = resource.__parent__
			except AttributeError:
				resource = None

	def find_interface(resource, class_or_interface):
		if IInterface.providedBy(class_or_interface):
			test = class_or_interface.providedBy
		else:
			test = lambda arg: isinstance(arg, class_or_interface)
		for location in lineage(resource):
			if test(location):
				return location
