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
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from plone.app.blob.field import ImageField as BlobImageField
from Products.ATContentTypes.interfaces import IATNewsItem

from redturtle.video.interfaces import IRTVideo

# Visit http://pypi.python.org/pypi/archetypes.schemaextender for full 
# documentation on writing extenders

class ExtensionBooleanField(ExtensionField, atapi.BooleanField):
    pass

class ExtensionReferenceField(ExtensionField, atapi.ReferenceField):
    pass

class ExtensionStringField(ExtensionField, atapi.StringField):
    pass

class ExtensionBlobImageField(ExtensionField, BlobImageField):
    pass


class Featurable(grok.Adapter):

    # This applies to all AT Content Types, change this to
    # the specific content type interface you want to extend
    grok.context(IFeaturable)
    grok.name('wcc.featurable.featurable')
    grok.implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    grok.provides(IOrderableSchemaExtender)

    layer = IProductSpecific

    @property
    def fields(self):
        image_field = [
            # add your extension fields here
            ExtensionBlobImageField('image',
                required = 0,
                languageIndependent = True,
                storage = atapi.AttributeStorage(),
                widget=ExtensionBlobImageField._properties['widget'](
                    label=_('Image'),
                )
            ),
        ]

        image_caption_field = [

            ExtensionStringField('imageCaption',
                required = 0,
                languageIndependent = False,
                storage = atapi.AttributeStorage(),
                widget=atapi.StringField._properties['widget'](
                    label=_('Image Caption')
                )
            ),
        ]

        fields = [

            ExtensionStringField('imageCopyright',
                required = 0,
                languageIndependent = False,
                storage = atapi.AttributeStorage(),
                widget=atapi.StringField._properties['widget'](
                    label=_('Image Copyright')
                )
            ),

            ExtensionBooleanField('is_featured',
                schemata='settings',
                languageIndependent = 1,
                widget=atapi.BooleanField._properties['widget'](
                    label=_('Is Featured'),
                    description=_(u'Feature this item')
                )
            ),
            ExtensionBooleanField('feature_hide_image',
                schemata='settings',
                languageIndependent = 1,
                widget=atapi.BooleanField._properties['widget'](
                    label=_('Hide image from displaying in feature listings'),
                )
            )
        ]

        
        if IATNewsItem.providedBy(self.context):
            return fields

        if IRTVideo.providedBy(self.context):
            return image_caption_field + fields

        return image_field + image_caption_field + fields

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        # you may reorder the fields in the schemata here
        return schematas
