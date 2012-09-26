===============
Getting Started
===============

Install
=======

#. Use ``pip`` to install the package::

       pip install django-resources

#. Add ``resources`` to your ``INSTALLED_APPS``:

   .. code-block:: python

      INSTALLED_APPS = (
          # ...
          'resources',
      )

What is a Resource?
===================

You have a bunch of models that store data. You want to relate these other models together, showing them as helpers to each other. Excellent! One problem: they all have differently named fields. One model's ``name`` is another model's ``title``.

Django Resource provides a wrapper around models to provide a consistent interface. It defaults to several attributes that you can use, augment, or ignore entirely and use ones of your creation. The bottom line is that you don't have to make all your apps' models the same.

Create and register a Resource
==============================

see :ref:`creating_a_resource`

Serializing Resources
=====================

Getting the serialized resources for a model
============================================