.. _creating_a_resource:

===================
Creating a Resource
===================

.. contents::
   :local:

Establishing the interface
==========================

Before you do anything, plan out which attributes you want to unify. For out example, we'll say we want ``title``, ``description``, ``key_image`` and ``url``.

With that in mind, we'll create our Resource models. Let's start with the ``Image`` model:

.. literalinclude:: examples/imageresource.py

Our ``ImageResource`` class subclasses ``BaseResource``, which provides a bunch of helpful features. We created three methods ``get_title()``, ``get_description()``, and ``get_key_image()``, and in each of these methods, we simply returned the equivalent attribute for that model using the ``instance`` attribute.

Aren't we missing something? What about the URL? Well, that leads us to discuss some features of :py:class:`BaseResource`.

Special Attributes of BaseResource
==================================

For the most part :py:class:`BaseResource` resolves requests for attributes in a specific and predictable way (see :ref:`accessing_resource_attributes`). There are two special attributes that it handles differently: ``resource_type`` and ``url``.

.. _resource_name_attr:

Resource Name
-------------

By default :py:class:`BaseResource` returns the model's verbose name. This attribute becomes a standard way to refer to the type of resource. You can override the default value by defining a ``get_resource_name`` method in your sub-class.


.. _url_attr:

URL
---

By default :py:class:`BaseResource` calls the instance's ``get_absolute_url`` method and returns the result. In some cases, you may want to return a different value, as we will when we define the Resource class for ``DownloadableFile``.


Customizing the special attributes
==================================

Let's define our interface for our ``DownloadableFile`` model.

.. literalinclude:: examples/downloadablefileresource.py

You'll notice that we defined four ``get_`` methods, and the ``get_url`` method returns the URL for the file instead of the model.

Finally, let's define the interface for our ``Article`` model.

.. literalinclude:: examples/articleresource.py

In this case, we defined a ``get_resource_name``. The version for our ``Article`` returns a different name depending on each instance's ``primary_category``.

Where do I put these definitions?
=================================

Good question! Django Supply Closet attempts to import the ``resources`` module of every installed app package. So define these in a ``resource.py`` file.