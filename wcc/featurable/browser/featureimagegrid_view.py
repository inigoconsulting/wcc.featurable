from five import grok
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.topic import IATTopic
from wcc.featurable.interfaces import IFeaturableSettings, IFeaturable
from zope.component import getMultiAdapter, getUtility
from plone.registry.interfaces import IRegistry

grok.templatedir('templates')

class FeatureImageGridView(grok.View):
    grok.baseclass()
    grok.name('featureimagegrid_view')
    grok.template('featureimagegrid_view')

    def get_featureimage_width(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        return proxy.feature_image_width

    def get_feature_image(self, obj):

        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)

        placeholder = '<div style="height:%spx;width:%spx;"></div>' % (
            proxy.feature_image_height,
            proxy.feature_image_width,
        )
        if not IFeaturable.providedBy(obj):
            return placeholder
        scales = obj.restrictedTraverse('@@images')
        result = scales.scale('feature_image', width=proxy.feature_image_width,
                height=proxy.feature_image_height)
        return result if result else placeholder



class FolderFeatureImageGridView(FeatureImageGridView):
    grok.context(IATFolder)

class TopicFeatureImageGridView(FeatureImageGridView):
    grok.context(IATTopic)
