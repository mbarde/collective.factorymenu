# -*- coding: utf-8 -*-

from Acquisition import aq_inner, aq_parent
from OFS.interfaces import IFolder
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as pmf
from plone.app.contentmenu.interfaces import IFactoriesMenu
from plone.app.contentmenu.interfaces import IFactoriesSubMenuItem
from plone.app.contentmenu.menu import FactoriesMenu as PloneFactoriesMenu
from plone.app.contentmenu.menu import FactoriesSubMenuItem as PFSubMenuItem
from plone.memoize.instance import memoize
from . import _
from .interfaces import ICustomFactoryMenuProvider, ICollectiveFactorymenuLayer
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import queryAdapter
from zope.i18n import translate
from zope.interface import implements


def _safe_unicode(text):
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8', 'ignore')
    return text


# Stolen from ploneview
def isFolderOrFolderDefaultPage(context, request):
    context_state = getMultiAdapter(
        (aq_inner(context), request), name=u'plone_context_state')
    return context_state.is_structural_folder() or\
        context_state.is_default_page()


class FactoriesSubMenuItem(PFSubMenuItem):
    implements(IFactoriesSubMenuItem)

    @memoize
    def _get_data(self):
        # First of all, get the real context of the menu
        context = self.context
        request = self.request
        if IFolder.providedBy(context):
            folder = context
        elif isFolderOrFolderDefaultPage(context, request):
            folder = aq_parent(aq_inner(context))
        else:
            # don't know how to handle this
            folder = context

        portal_url = getToolByName(context, 'portal_url')
        data = {'context': context,
                'portal_url': portal_url, 'container': folder}
        return data

    @memoize
    def getCustomMenuResults(self):
        data = self._get_data()

        try:
            m_provider = ICustomFactoryMenuProvider(data['container'])
        except TypeError:
            # For any adaptation problem
            return None

        itemsToAdd = self._itemsToAdd()
        if len(itemsToAdd) == 1:
            fti = itemsToAdd[0][1]
            return m_provider.getSingleEntryMenuCustomization(data, fti)
        return None

    @property
    def title(self):
        itemsToAdd = self._itemsToAdd()
        showConstrainOptions = self._showConstrainOptions()
        custom_menu_results = self.getCustomMenuResults()
        if custom_menu_results:
            if not showConstrainOptions and len(itemsToAdd) == 1:
                title = custom_menu_results.get('title')
                title = translate(_safe_unicode(title),
                                  domain='plone',
                                  context=self.request)
                return pmf(u'label_add_type', default='Add ${type}',
                           mapping={'type': title})
        title = super(FactoriesSubMenuItem, self).title
        return title

    @property
    def description(self):
        itemsToAdd = self._itemsToAdd()
        showConstrainOptions = self._showConstrainOptions()
        custom_menu_results = self.getCustomMenuResults()
        if custom_menu_results:
            if not showConstrainOptions and len(itemsToAdd) == 1:
                return custom_menu_results.get('description')
        description = super(FactoriesSubMenuItem, self).description
        return description

    @property
    def action(self):
        custom_menu_results = self.getCustomMenuResults()
        if custom_menu_results:
            return custom_menu_results.get('action')
        action = super(FactoriesSubMenuItem, self).action
        return action

    @property
    def icon(self):
        # BBB: deprecated from Plone 4.0
        custom_menu_results = self.getCustomMenuResults()
        if custom_menu_results:
            return custom_menu_results.get('icon')
        icon = super(FactoriesSubMenuItem, self).icon
        return icon


class FactoriesMenu(PloneFactoriesMenu):
    implements(IFactoriesMenu)

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = PloneFactoriesMenu.getMenuItems(self, context, request)

        # No menu customization if the product is not installed
        if not ICollectiveFactorymenuLayer.providedBy(request):
            return results

        portal_url = getToolByName(context, 'portal_url')

        # First of all, get the real context of the menu
        if IFolder.providedBy(context):
            folder = context
        elif isFolderOrFolderDefaultPage(context, request):
            folder = aq_parent(aq_inner(context))
        else:
            # don't know how to handle this
            folder = context

        data = {'context': context,
                'portal_url': portal_url, 'container': folder}

        try:
            m_provider = ICustomFactoryMenuProvider(folder)
        except TypeError:
            # For any adaptation problem
            return results

        results = m_provider.getMenuCustomization(data, results)

        # Re-sort
        results.sort(lambda x, y: cmp(x['title'], y['title']))

        mtool = getToolByName(context, 'portal_membership')
        if not mtool.isAnonymousUser() and\
            mtool.getAuthenticatedMember().has_permission(
                'Customize menu: factories', folder
        ):
            context_url = folder.absolute_url()
            results.append(
                {'title': _(u'custommenu_manage_title',
                            default=u'Customize menu\u2026'),
                 'description': _(u'custommenu_manage_description',
                                  default=u'Manage custom elements '
                                          u'of this menu'),
                 'action': context_url + '/@@customize-factoriesmenu',
                 'selected': False,
                 'icon': None,
                 'submenu': None,
                 'extra': {'separator': 'actionSeparator',
                           'id': 'customize-factoriesmenu',
                           'class': 'customize-menu'},
                 }
            )
        return results
