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
from plone.app.blob.subtypes.image import ExtensionBlobField
# Visit http://pypi.python.org/pypi/archetypes.schemaextender for full 
# documentation on writing extenders

class ExtensionBooleanField(ExtensionField, atapi.BooleanField):
    pass

class ExtensionReferenceField(ExtensionField, atapi.ReferenceField):
    pass

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
        ExtensionBlobField('feature_image',
            required = 0,
            languageIndependent = 1,
            storage = atapi.AttributeStorage(),
            widget=ExtensionBlobField._properties['widget'](
                label=_('Feature image'),
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
