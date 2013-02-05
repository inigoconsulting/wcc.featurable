from wcc.featurable.interfaces import IFeaturableProvider, IFeaturable
from five import grok
from zope.component.hooks import getSite

class FeaturableProvider(grok.GlobalUtility):
    grok.implements(IFeaturableProvider)

    def query(self, **params):
        site = getSite()
        brains = site.portal_catalog(
            object_provides=IFeaturable.__identifier__,
            is_featured=True,
            sort_on='Date',
            sort_order='descending',
            **params
        )
        return brains
