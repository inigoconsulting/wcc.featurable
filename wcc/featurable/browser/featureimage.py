from five import grok
from wcc.featurable.interfaces import IFeaturable, IFeaturableSettings
from wcc.featurable.behavior.featurable import IFeaturable as IDexterityFeaturable
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from AccessControl import getSecurityManager
from logging import getLogger
logger = getLogger('wcc.featurable')

class FeatureImageUtilView(grok.View):
    grok.context(IFeaturable)
    grok.name('featureimages')

    def render(self):
        return str(self)

    def tag(self, scale=None, css_class=None, width=None, height=None):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        scales = self.context.restrictedTraverse('@@images')
        if getattr(self.context, 'feature_hide_image', False):
            return ''


        scale_width = width or proxy.feature_image_width
        scale_height = height or 999
        if scale is None:
            result = scales.scale('image', 
                width=scale_width,
                height=scale_height, direction='keep')
        else:
            result = scales.scale('image', scale=scale)
        try:
            return result.tag(css_class=css_class) if result else ''
        except IOError:
            logger.error(
                'Broken Feature Image : %s' % (
                    self.context.absolute_url()
                )
            )
            return ''
