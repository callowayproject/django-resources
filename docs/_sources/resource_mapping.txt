.. _creating_a_resource:

===================
Creating a Resource
===================

Common Attributes
=================

You convert one of your Django models into a Resource by creating and registering a Resource class. The :py:class:`BaseResource` class defines common attributes for a resource. Since these attributes may go by different names in different objects, you will create a custom Resource for each model to extract the information.

.. _resource_type_attr:

**Resource Type**
    A brief label for the type of resource, like "Image" or "Multimedia". Resource Types do not have to be unique. Different objects with the same Resource Type are grouped together when listing by Resource Type.

.. _title_attr:

**Title**
    The title of the object.

.. _description_attr:

**Description**
    Descriptive text of the object.

.. _key_image_attr:

**Key Image**
    An image for display.

.. _credit_attr:

**Credit**
    Credit line for the object.

.. _url_attr:

**URL**
    The URL for this object.

.. _citation_attr:

**Citation**
    A non-Internet citation of the resource, like a book.

.. _notes_attr:

**Notes**
    Any notes regarding this resource.

.. _internal_ref_attr:

**Internal Reference**
    An arbitrary reference for your internal use.

Django Resources attempts to import ``resources`` from every entry in ``INSTALLED_APPS``.

Here is an example of making an audio resource:

.. literalinclude:: examples/audioresource.py
   :linenos:

I left lines 20-30 in but commented out to show that this resource isn't going to implement those items. There might be two reasons for this:

#. The model does not have any equivalent fields with this information. The default implementation will simply return ``''``.
#. The model has fields with those default names (``credit``, ``citation``, ``notes``, ``internal_ref``)


Specialized Resources
=====================

Slide
-----

A Slide typically wraps another object, allowing one-time overriding of the object's attributes. For example, if you wanted to provide a different caption for a photo object, you would create a slide, link the photo object and provide a new caption. Then the slide is added to the resource listing instead of the original object.

Resource
--------

A Resource is an external object. While it is a link outside of the web site, a Resource doesn't have to be the entire external web site. It could refer to an external image or video or downloadable item. Basically a Resource is a proxy object for anything that we don't have on our site.