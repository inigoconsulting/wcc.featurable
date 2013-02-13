from five import grok
from wcc.featurable.interfaces import IFeaturable, IFeaturableSettings
from wcc.featurable.behavior.featurable import IFeaturable as IDexterityFeaturable
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

class FeatureImageUtilView(grok.View):
    grok.context(IFeaturable)
    grok.name('featureimages')

    def render(self):
        return str(self)

    def get_image(self):
        obj = self.context
        return obj.getField('feature_image').get(obj)

    def tag(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        imgobj = self.get_image()
        if not imgobj:
            return ''

        scales = imgobj.restrictedTraverse('@@images')
        result = scales.scale('image', width=proxy.feature_image_width,
                height=proxy.feature_image_height)
        return result.tag() if result else ''

class DexterityFeatureImageUtilView(FeatureImageUtilView):
    grok.context(IDexterityFeaturable)

    def get_image(self):
        if getattr(self.context, 'feature_image', None):
            return self.context.feature_image.to_object
        return None
