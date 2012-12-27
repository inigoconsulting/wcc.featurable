from zope.interface import Interface
from zope import schema

class IProductSpecific(Interface):
    pass

class IFeaturable(Interface):
    pass

class IFeaturableSettings(Interface):

    feature_image_height = schema.Int(
        title=u'Feature Image Height (in pixels)',
        default=200
    )

    feature_image_width = schema.Int(
        title=u'Feature Image Width (in pixels)',
        default=600
    )

class IFeaturableProvider(Interface):
    pass
