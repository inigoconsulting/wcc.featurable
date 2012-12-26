README for wcc.featurable
==========================================

Hooking to content types
-------------------------

To mark an Archetype content types as Featurable, add this into configure.zcml
if your policy product::

  <class class="Products.ATContentTypes.content.document.ATDocument"> 
     <implements interface="wcc.featurable.interfaces.IFeaturable"/> 
  </class>


For Dexterity content types, just apply the Featurable behavior to the content
type

Configuration
--------------

Configuration is managed using plone.registry. To configure, check out the
"Configuration Registry" control panel and configure these keys:

* wcc.featurable.interfaces.IFeaturableSettings.feature_image_height

* wcc.featurable.interfaces.IFeaturableSettings.feature_image_width
