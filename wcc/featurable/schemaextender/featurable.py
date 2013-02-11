from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes import atapi
from plone.app.blob.field import ImageField
from Products.ATContentTypes.interfaces import IATContentType
from zope.interface import Interface
from five import grok
from wcc.featurable.interfaces import (IProductSpecific, IFeaturable,
                                        IFeaturableSettings)
from wcc.featurable import MessageFactory as _
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from wcc.featurable.validators import ArchetypeImageSizeValidator
# Visit http://pypi.python.org/pypi/archetypes.schemaextender for full 
# documentation on writing extenders

class ExtensionImageField(ExtensionField, atapi.ImageField):
    pass    

class ExtensionBooleanField(ExtensionField, atapi.BooleanField):
    pass

class ImageWidget(atapi.ImageWidget):

    def Description(self, instance, **kwargs):
        registry = getUtility(IRegistry)
        proxy = registry.forInterface(IFeaturableSettings)
        return u"Upload feature image. Required size is %sx%s" % (
                proxy.feature_image_width,
                proxy.feature_image_height
        )


class Featurable(grok.Adapter):

    # This applies to all AT Content Types, change this to
    # the specific content type interface you want to extend
    grok.context(IFeaturable)
    grok.name('wcc.featurable.featurable')
    grok.implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    grok.provides(IOrderableSchemaExtender)

    layer = IProductSpecific

    fields = [
        # add your extension fields here
        ExtensionImageField('feature_image',
            required = 0,
            languageIndependent = 1,
            pil_quality =100,
            validators = (ArchetypeImageSizeValidator(),),
            storage = atapi.AttributeStorage(),
            schemata='settings',
            widget = ImageWidget(
                label= _("Feature Image"),
            )
        ),

        ExtensionBooleanField('is_featured',
            schemata='settings',
            widget=atapi.BooleanField._properties['widget'](
                label=_('Is Featured'),
                description=_(u'Feature this item')
            )
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        # you may reorder the fields in the schemata here
        return schematas
