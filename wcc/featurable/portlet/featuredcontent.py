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
from wcc.featurable.interfaces import IFeaturableProvider, IFeaturableSettings
import dateutil

class IFeaturedContent(IPortletDataProvider):
    """
    Define your portlet schema here
    """
    count = schema.Int(
        title=_(u'Number of items to list'),
        default=3
    )

    content_types = schema.List(
        title=_(u'Content types'),
        value_type=schema.Choice(vocabulary='plone.app.vocabularies.PortalTypes')
    )

class Assignment(base.Assignment):
    implements(IFeaturedContent)

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
        return True

    def items(self):
        provider = getUtility(IFeaturableProvider)
        brains = provider.query(portal_type=self.data.content_types)
        return brains[:self.data.count]

    def get_date(self, brain):
        date = brain.Date
        if isinstance(date, str):
            return dateutil.parser.parse(date).strftime('%d.%m.%Y')
        return date.strftime('%d.%m.%Y')

    def get_feature_image(self, brain):
        obj = brain.getObject()
        scales = obj.restrictedTraverse('@@images')
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        return scales.scale('feature_image', width=proxy.feature_image_width,
                height=proxy.feature_image_height)

class AddForm(base.AddForm):
    form_fields = form.Fields(IFeaturedContent)
    label = _(u"Add Featured Content")
    description = _(u"List featured contents")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IFeaturedContent)
    label = _(u"Edit Featured Content")
    description = _(u"List featured contents")
