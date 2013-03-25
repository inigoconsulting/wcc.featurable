from collective.grok import gs
from Products.CMFCore.utils import getToolByName
from wcc.featurable.interfaces import IFeaturable
from zope.component import getUtility
from zope.component.hooks import getSite
from plone.app.layout.navigation.root import getNavigationRoot
from logging import getLogger
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
import sys
from plone.app.blob.field import ImageField as BlobImageField
logger = getLogger('wcc.featurable.upgrade')

# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade wcc.featurable to 1006',
                description=u'Upgrade wcc.featurable to 1006',
                source='1005', destination='1006',
                sortkey=1, profile='wcc.featurable:default')
def to1006(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.featurable.upgrades:to1006')


@gs.upgradestep(title=u'Upgrade wcc.featurable to 1005',
                description=u'Upgrade wcc.featurable to 1005',
                source='1004', destination='1005',
                sortkey=1, profile='wcc.featurable:default')
def to1005(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.featurable.upgrades:to1005')

    class ExtensionReferenceField(ExtensionField, atapi.ReferenceField):
        pass

    class ExtensionBlobImageField(ExtensionField, BlobImageField):
        pass

    class ExtensionStringField(ExtensionField, atapi.StringField):
        pass

    catalog = getToolByName(context, 'portal_catalog')

    portal = getSite()
    field = ExtensionReferenceField('feature_image',
        required = 0,
        languageIndependent = 1,
        relationship = 'featureImageRelatedImage',
        allowed_types=('Image', 'TranslatableImage'),
        storage = atapi.AttributeStorage(),
    )

    leadimagefield = ExtensionBlobImageField('leadImage',
        required = 0,
        languageIndependent = 1,
        storage = atapi.AnnotationStorage(migrate=True),
    )

    leadimagecaptionfield = ExtensionStringField('leadImage_caption',
        storage = atapi.AnnotationStorage()
    )

    catalog.manage_reindexIndex(ids=['object_provides'])

    for brain in catalog({'object_provides': IFeaturable.__identifier__,
                        'Language':'all'}):
        obj = brain.getObject()
        leadimage = leadimagefield.get(obj)
        if leadimage and leadimage.data:
            existing = obj.getField('image').get(obj)
            if not (existing and existing.data):
                obj.getField('image').set(obj, leadimage)
                obj.getField('imageCaption').set(obj,
                        leadimagecaptionfield.get(obj))
                obj.reindexObject()
                continue

        rel = field.get(obj)
        if rel is not None:
            val = rel.getField('image').get(rel)
            obj.getField('image').set(obj, val.data)
        obj.reindexObject()
    

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
            if not obj.getField('feature_image'):
                continue
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
