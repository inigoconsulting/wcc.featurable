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

from plone.registry.interfaces import IRegistry
from zope.component import ComponentLookupError, getUtility

class FeatureImage(namedfile.NamedBlobImage):

    def __init__(self, *args, **kwargs):
        super(FeatureImage, self).__init__(*args, **kwargs)

    @property
    def description(self):
        try:
            registry = getUtility(IRegistry)
        except ComponentLookupError:
            return u''
        proxy = registry.forInterface(IFeaturableSettings)
        return u"Upload feature image. Required size is %sx%s" % (
                proxy.feature_image_width,
                proxy.feature_image_height
        )

    @description.setter
    def description(self, value):
        pass

class IFeaturable(form.Schema, IBaseFeaturable):
    """
       Marker/Form interface for Featurable
    """

    # -*- Your Zope schema definitions here ... -*-

    form.fieldset('settings',
        label=_(u'Settings'),
        fields=['feature_image']
    )

    feature_image = FeatureImage(
        title=_(u'Feature Image'),
        required=False,
    )

#    is_featured = schema.Bool(
#        title=_(u'Is Featured'),
#        description=_(u'Feature this item'),
#    )

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
        'feature_image'
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
