from five import grok
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.topic import IATTopic
from wcc.featurable.interfaces import IFeaturableSettings, IFeaturable
from zope.component import getMultiAdapter, getUtility
from plone.registry.interfaces import IRegistry

grok.templatedir('templates')

class FeatureImageListingView(grok.View):
    grok.baseclass()
    grok.name('featureimagelisting_view')
    grok.template('featureimagelisting_view')

    def get_featureimage_width(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        return proxy.feature_image_width

    def get_feature_image(self, obj):

        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)

        placeholder = u'<div style="height:%spx;width:%spx;"></div>' % (
            proxy.feature_image_height,
            proxy.feature_image_width,
        )
        if not IFeaturable.providedBy(obj):
            return placeholder

        featureimages = obj.restrictedTraverse('@@featureimages')
        result = featureimages.tag()
        return result if result else placeholder

class FolderFeatureImageListingView(FeatureImageListingView):
    grok.context(IATFolder)

class TopicFeatureImageListingView(FeatureImageListingView):
    grok.context(IATTopic)
