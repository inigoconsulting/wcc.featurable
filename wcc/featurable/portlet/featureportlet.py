from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form

from z3c.form import field

from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationList, RelationChoice

from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wcc.featurable import MessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from AccessControl import getSecurityManager

class IFeaturePortlet(IPortletDataProvider):
    """
    Define your portlet schema here
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    target_collection = schema.Choice(
        title=_(u"Target collection"),
        description=_(u"Find the collection which provides the items to display"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))


class Assignment(base.Assignment):
    implements(IFeaturePortlet)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def title(self):
        return getattr(self, 'header', _('Featured Content from Collection'))

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/featureportlet.pt')

    @property
    def available(self):
        return True

    @memoize
    def collection(self):
        collection_path = self.data.target_collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]

        if not collection_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(collection_path, unicode):
            # restrictedTraverse accepts only strings
            collection_path = str(collection_path)

        result = portal.unrestrictedTraverse(collection_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result


    def item(self):
        collection = self.collection()
        brains = collection.queryCatalog(batch=False)

        if brains:
            return brains[0].getObject()
        return None


class AddForm(base.AddForm):
    form_fields = form.Fields(IFeaturePortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Add Feature Portlet")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IFeaturePortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Edit Feature Portlet")
    description = _(u"")
