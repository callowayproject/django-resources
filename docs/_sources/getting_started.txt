===============
Getting Started
===============

Install
=======

#. Use ``pip`` to install the package::

       pip install django-contentrelations

#. Add ``contentrelations`` to your ``INSTALLED_APPS``:

   .. code-block:: python

      INSTALLED_APPS = (
          # ...
          'contentrelations',
      )

What is a Resource?
===================

You have a bunch of models that store data, let's say an ``Image`` model, an ``Article`` model and ``DownloadableFile`` model. You want to use them together and in the same way, but you have a problem: none of the models' attributes are named the same! This is a nightmare! That's where a Resource comes in. A Resource is a wrapper around a model to provide a consistent interface.


Next see :ref:`creating_a_resource`
