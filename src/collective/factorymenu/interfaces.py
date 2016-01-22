# -*- coding: utf-8 -*-

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class ICollectiveFactorymenuLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICustomMenuEnabled(Interface):
    """Marker interface for content that use custom menu"""


class ICustomFactoryMenuProvider(Interface):
    """Interface for adapters that provide customization for factory menu"""
