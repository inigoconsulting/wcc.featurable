from zope import schema
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey
from plone.registry.interfaces import IRegistry

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wcc.featurable import MessageFactory as _
from wcc.featurable.interfaces import (IFeaturableProvider, 
                                        IFeaturableSettings,
                                        IFeaturable)
from AccessControl import getSecurityManager
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

import dateutil

class IFeaturedContent(IPortletDataProvider):
    """
    Define your portlet schema here
    """
    item = schema.Choice(
        title=_(u'Featured content'),
        source=SearchableTextSourceBinder(
            {'object_provides': IFeaturable.__identifier__},
            default_query='path:'
        )
    )

class Assignment(base.Assignment):
    implements(IFeaturedContent)

    item = None
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def title(self):
        return _('Featured Content')

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/featuredcontent.pt')

    @property
    def available(self):
        return True if self.item() else False

    def item(self):
        return self._get_item(self.data.item)

    def _get_item(self, path):
        if not path:
            return None

        if path.startswith('/'):
            path = path[1:]

        portal_state = getMultiAdapter((self.context, self.request),
                name=u'plone_portal_state')

        portal = portal_state.portal()

        if isinstance(path, unicode):
            path = str(path)

        result = portal.unrestrictedTraverse(path, default=None)

        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None

        return result


    def get_date(self, obj):
        date = obj.Date()
        if isinstance(date, str):
            return dateutil.parser.parse(date).strftime('%d.%m.%Y')
        return date.strftime('%d.%m.%Y')

    def get_feature_image(self, obj):
        featureimages = obj.restrictedTraverse('@@featureimages')
        return featureimages.tag()

    def get_featureimage_width(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        return proxy.feature_image_width


    def getstyle(self):
        return 'width:%spx;margin:0 auto;' % (self.get_featureimage_width())

class AddForm(base.AddForm):
    form_fields = form.Fields(IFeaturedContent)
    form_fields['item'].custom_widget = UberSelectionWidget
    label = _(u"Add Featured Content")
    description = _(u"List featured contents")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IFeaturedContent)
    form_fields['item'].custom_widget = UberSelectionWidget
    label = _(u"Add Featured Content")
    label = _(u"Edit Featured Content")
    description = _(u"List featured contents")
