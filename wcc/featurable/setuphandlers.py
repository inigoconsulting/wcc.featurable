from collective.grok import gs
from wcc.featurable import MessageFactory as _

@gs.importstep(
    name=u'wcc.featurable', 
    title=_('wcc.featurable import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.featurable.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
