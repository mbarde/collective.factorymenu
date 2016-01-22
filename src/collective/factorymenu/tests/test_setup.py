# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.factorymenu.testing import COLLECTIVE_FACTORYMENU_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.factorymenu is properly installed."""

    layer = COLLECTIVE_FACTORYMENU_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.factorymenu is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.factorymenu'))

    def test_browserlayer(self):
        """Test that ICollectiveFactorymenuLayer is registered."""
        from collective.factorymenu.interfaces import (
            ICollectiveFactorymenuLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveFactorymenuLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_FACTORYMENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.factorymenu'])

    def test_product_uninstalled(self):
        """Test if collective.factorymenu is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.factorymenu'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveFactorymenuLayer is removed."""
        from collective.factorymenu.interfaces import ICollectiveFactorymenuLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveFactorymenuLayer, utils.registered_layers())
