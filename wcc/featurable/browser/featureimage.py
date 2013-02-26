from five import grok
from wcc.featurable.interfaces import IFeaturable, IFeaturableSettings
from wcc.featurable.behavior.featurable import IFeaturable as IDexterityFeaturable
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from AccessControl import getSecurityManager

class FeatureImageUtilView(grok.View):
    grok.context(IFeaturable)
    grok.name('featureimages')

    def render(self):
        return str(self)

    def tag(self):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        scales = self.context.restrictedTraverse('@@images')
        result = scales.scale('feature_image', 
                width=proxy.feature_image_width,
                height=999, direction='keep')
        return result.tag() if result else ''
