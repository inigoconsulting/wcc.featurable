from collective.grok import gs
from wcc.featurable import MessageFactory as _
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from wcc.featurable.interfaces import IFeaturableSettings

@gs.importstep(
    name=u'wcc.featurable', 
    title=_('wcc.featurable import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.featurable.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
    registry = getUtility(IRegistry)
    registry.registerInterface(IFeaturableSettings)
