from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from wcc.featurable import MessageFactory as _
from wcc.featurable.interfaces import IFeaturable as IBaseFeaturable
from wcc.featurable.interfaces import IFeaturableSettings
from wcc.featurable.validators import DexterityImageSizeValidator
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.ATContentTypes.interfaces.image import IATImage

from plone.registry.interfaces import IRegistry
from zope.component import ComponentLookupError, getUtility
from plone.multilingualbehavior import directives as pam
from Acquisition import aq_base

class IFeaturable(form.Schema, IBaseFeaturable):
    """
       Marker/Form interface for Featurable
    """

    # -*- Your Zope schema definitions here ... -*-

    form.fieldset('settings',
        label=_(u'Settings'),
        fields=['is_featured', 'feature_hide_image']
    )

    pam.languageindependent('image')
    image = namedfile.NamedBlobImage(
        title=_(u'Image'),
        required=False,
    )

    imageCaption = schema.TextLine(
        title=_(u'Image Caption'),
        required=False,
        default=u''
    )

    imageCopyright = schema.TextLine(
        title=_(u'Image Copyright'),
        required=False,
        default=u'',
    )

    pam.languageindependent('is_featured')
    is_featured = schema.Bool(
        title=_(u'Is Featured'),
        description=_(u'Feature this item'),
    )

    pam.languageindependent('feature_hide_image')
    feature_hide_image = schema.Bool(
        title=_(u'Hide image from displaying in feature listings'),
    )


alsoProvides(IFeaturable,IFormFieldProvider)

class Featurable(object):
    """
       Adapter for Featurable
    """
    implements(IFeaturable)
    adapts(IDexterityContent)

    _delegated_attributes = [
        'image',
        'imageCaption',
        'is_featured',
        'feature_hide_image'
    ]

    def __init__(self, context):
        self.context = aq_inner(context)

    def __getattr__(self, key):
        if key in self._delegated_attributes:
            return getattr(self.context, key)
        raise AttributeError(key)

    def __setattr__(self, key, value):
        if key in self._delegated_attributes:
            setattr(self.context, key, value)
        self.__dict__[key] = value

    def __delattr__(self, key):
        if key in self._delegated_attributes:
            delattr(self.context, key)
        del self.__dict__[key]
