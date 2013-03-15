from Acquisition import aq_inner
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wcc.featurable.interfaces import IFeaturableSettings, IFeaturable
from Products.ATContentTypes.interfaces import IATNewsItem

class FeatureImageViewlet(ViewletBase):
    
    index = ViewPageTemplateFile('templates/featureimage_viewlet.pt')

    def enabled(self):
        if IATNewsItem.providedBy(self.context):
            return False
        if IFeaturable.providedBy(self.context):
            return True
        return False

    def get_feature_image(self):
        obj = self.context
        featureimages = obj.restrictedTraverse('@@featureimages')
        result = featureimages.tag()
        return result if result else ''

