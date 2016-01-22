# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.factorymenu


class CollectiveFactorymenuLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.factorymenu)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.factorymenu:default')


COLLECTIVE_FACTORYMENU_FIXTURE = CollectiveFactorymenuLayer()


COLLECTIVE_FACTORYMENU_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FACTORYMENU_FIXTURE,),
    name='CollectiveFactorymenuLayer:IntegrationTesting'
)


COLLECTIVE_FACTORYMENU_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FACTORYMENU_FIXTURE,),
    name='CollectiveFactorymenuLayer:FunctionalTesting'
)


COLLECTIVE_FACTORYMENU_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_FACTORYMENU_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveFactorymenuLayer:AcceptanceTesting'
)
