===================================
django-contentrelations v |version|
===================================

About
=====

Django Content Relations is designed to allow an object to specify an ordered collection of other objects as resources.

Two models are defined to help with this: Resource, which defines an external resource, and Slide which allows for customization of the attributes of the original object.

There are also utility functions to serialize the collection into forms suitable for a variety of displays, such as a carousel.

Contents
========

.. toctree::
   :maxdepth: 2
   :glob:

   getting_started
   resource_mapping
   using_resources
   serializing_resources
   resources_and_models
   reference/index
