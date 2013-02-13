from collective.grok import gs
from Products.CMFCore.utils import getToolByName
from wcc.featurable.interfaces import IFeaturable
from zope.component import getUtility
from zope.component.hooks import getSite
from plone.app.layout.navigation.root import getNavigationRoot
from logging import getLogger
logger = getLogger('wcc.featurable.upgrade')

# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade wcc.featurable to 1004',
                description=u'Upgrade wcc.featurable to 1004',
                source='1003', destination='1004',
                sortkey=1, profile='wcc.featurable:default')
def to1004(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.featurable.upgrades:to1004')

    catalog = getToolByName(context, 'portal_catalog')

    # create portal/<lang>/featureimages/
    portal = getSite()
    for lang, langtitle in portal.portal_languages.listSupportedLanguages():
        langsite = portal[lang]
        if not langsite.has_key('featureimages'):
            langsite.invokeFactory('Folder','featureimages')
            featureimages = langsite['featureimages']
            langval = langsite.getField('language').get(langsite)
            featureimages.getField('language').set(featureimages, langval)
            featureimages.reindexObject()

    for brain in catalog({'object_provides': IFeaturable.__identifier__,
                        'Language':'all'}):
        obj = brain.getObject()
        # blank featureImage
        if getattr(obj, 'feature_image', None):
            navroot = portal.restrictedTraverse(getNavigationRoot(obj))
            # create if  portal/featureimages/

            image = obj.feature_image
            name = '_'.join(obj.getPhysicalPath()[1:])

            logger.info('Migrating image for %s',
                    '/'.join(obj.getPhysicalPath()))

            if name not in navroot.featureimages.keys():
                navroot.featureimages.invokeFactory('Image', name)

            newimage = navroot.featureimages[name]
            newimage.getField('image').set(newimage, image)
            lang = obj.getField('language').get(obj)
            newimage.getField('language').set(newimage, lang)
            obj.feature_image = None
            obj.getField('feature_image').set(obj, newimage)
            obj.reindexObject()
            newimage.reindexObject()


@gs.upgradestep(title=u'Upgrade wcc.featurable to 1003',
                description=u'Upgrade wcc.featurable to 1003',
                source='1002', destination='1003',
                sortkey=1, profile='wcc.featurable:default')
def to1003(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.featurable.upgrades:to1003')


@gs.upgradestep(title=u'Upgrade wcc.featurable to 1002',
                description=u'Upgrade wcc.featurable to 1002',
                source='1001', destination='1002',
                sortkey=1, profile='wcc.featurable:default')
def to1002(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.featurable.upgrades:to1002')


@gs.upgradestep(title=u'Upgrade wcc.featurable to 1001',
                description=u'Upgrade wcc.featurable to 1001',
                source='1', destination='1001',
                sortkey=1, profile='wcc.featurable:default')
def to1001(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.featurable.upgrades:to1001')
