========
Settings
========

.. _setup_resources_setting:

SETUP_RESOURCES
===============

**Default:** ``[]``

This takes a list of strings in the format ``'appname.Model.fieldname'`` like ``'auth.User.related'`` and adds the :py:class:`RelatedResource` generic many-to-many relation to the ``fieldname`` of ``appname.Model``.