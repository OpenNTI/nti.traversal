#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Code taken from https://github.com/Pylons/pyramid

@see: https://github.com/Pylons/pyramid/blob/1.8-branch/pyramid/location.py

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

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
        def test(arg): 
            return isinstance(arg, class_or_interface)
    for location in lineage(resource):
        if test(location):
            return location
