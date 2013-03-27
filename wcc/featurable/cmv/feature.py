from collective.portlet.collectionmultiview import BaseRenderer
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from wcc.featurable import MessageFactory as _
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter, getUtility
from wcc.featurable.interfaces import (IFeaturableProvider,
                                     IFeaturableSettings,
                                     IFeaturable)
from zope.interface import Interface
from zope import schema

class IFeatureRendererSchema(Interface):
    columns = schema.Choice(
        title=_(u"Columns"),
        description=_(u"Number of columns to render"),
        values=[2,3,4]
    )

    more_link = schema.TextLine(
        title=_(u'More Link'),
        description=_(u'URL to link to on the "More News" link'),
        default=u''
    )

class FeatureRenderer(BaseRenderer):
    title=_("WCC Feature Renderer")
    template = ViewPageTemplateFile('templates/feature.pt')
    schema = IFeatureRendererSchema

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

    def get_class(self, idx):
        columns = self.data.columns
        if idx == 0:
            return 'cell width-1:%s position-0' % columns
        return 'cell width-1:%(columns)s position-%(pos)s:%(columns)s' % {
                'pos':idx,'columns':columns
        }

    def items(self):
        columns = self.data.columns
        return [i.getObject() for i in self.results()[:columns]]

    def more_link(self):
        collection_url = self.collection().absolute_url()
        return getattr(self.data, 'more_link', None) or collection_url
