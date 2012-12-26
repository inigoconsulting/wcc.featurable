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
from wcc.featurable.validators import DexterityImageSizeValidator

class IFeaturable(form.Schema, IBaseFeaturable):
    """
       Marker/Form interface for Featurable
    """

    # -*- Your Zope schema definitions here ... -*-

    feature_image = namedfile.NamedBlobImage(
        title=_(u'Feature Image'),
        required=False,
    )

    is_featured = schema.Bool(
        title=u'Featured',
    )

@form.validator(field=IFeaturable['feature_image'])
def validateFeatureImage(value):
    validator = DexterityImageSizeValidator()
    validator.validate(value)
    return True

alsoProvides(IFeaturable,IFormFieldProvider)

class Featurable(object):
    """
       Adapter for Featurable
    """
    implements(IFeaturable)
    adapts(IDexterityContent)

    _delegated_attributes = [
        'feature_image', 'is_featured',
    ]

    def __init__(self, context):
        self.context = context

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
