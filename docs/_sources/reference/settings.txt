========
Settings
========

.. _resource_type_choices_setting:

RESOURCE_TYPE_CHOICES
=====================

**Default:** ``None``

A list of labels used for Slide and Resource. If left empty, a plain character field is displayed

.. _image_storage_setting:

IMAGE_STORAGE
=============

**Default:** ``settings.DEFAULT_FILE_STORAGE``

The file storage class to use for image storage.

.. _key_image_model_setting:

KEY_IMAGE_MODEL
===============

**Default:** ``None``

If specified, a :py:class:`ForeignKeyField` is created and linked to that model to provide images for :py:class:`Slide`\ s and :py:class:`Resource`\ s.

.. _setup_resources_setting:

SETUP_RESOURCES
===============

**Default:** ``[]``

This takes a list of strings in the format ``'appname.Model.fieldname'`` like ``'auth.User.related'`` and adds the :py:class:`RelatedResource` generic many-to-many relation to the ``fieldname`` of ``appname.Model``.