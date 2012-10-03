===============
Using Resources
===============

Using a resource requires instantiating the registered resource class with an instance of the appropriate class. In short::

    ExampleResource(Example.objects.get(id=1))

But since you probably are missing key information about which resource goes with with object, there are some easier ways to do this.

Getting the Resource class from a model
=======================================

If you have the model, you can get the resource class from the :ref:`resource_list`.

.. code-block:: python

    from contentrelations import resource_list
    from simpleapp.models import Food
    FoodResourceClass = resource_list[Food]

Then you can instantiate the class with any :py:class:`Food` object.

.. code-block:: python

    food_item = Food.objects.get(id=1)
    resource = FoodResourceClass(food_item)

Getting the Resource from a model instance
==========================================

An even simpler way to get a Resource is to use the :py:meth:`ResourceList.get_for_instance` method on the :ref:`resource_list` object. This method takes an instance, and does the lookup and instantiation for you.

.. code-block:: python

    from contentrelations import resource_list
    from simpleapp.models import Food
    food_item = Food.objects.get(id=1)
    resource = resource_list.get_for_instance(food_item)

.. _accessing_resource_attributes:

Accessing resource attributes
=============================

A Resource class attempts to get an attribute several ways:

#. An attempt to access ``resource.FOO`` attempts to call the ``resource.get_FOO()`` method.
#. If a subclass has defined the ``get_FOO()`` method, then that result is returned.
#. If there is not a ``get_FOO()`` method defined, the resource attempts to get the ``FOO`` attribute from the original instance.
#. If that fails, it will either raise an :py:class:`AttributeError` if the resource's :py:attr:`BaseResource.raise_error_on_missing` is ``True`` (its default value is ``False``) or return the :py:attr`BaseResource.missing_attribute_value` value, which is ``''`` by default.

.. _getting_the_resources_list_objects:

Getting the Resources of a list of objects
==========================================

What if you have a list of items and you want to use them as Resources? That's where the :py:class:`ResourceIterator` comes in. the ResourceIterator wraps any iterator or sequence and returns each item's registered Resource class. Here is a simple example::

    >>> from articleapp.models import Article
    >>> from imageapp.models import Image
    >>> from downloads.models import DownloadableFile
    >>> from contentrelations.resources import ResourceIterator
    >>> a = Article.objects.all()[0]
    >>> i = Image.objects.all()[0]
    >>> d = DownloadableFile.objects.all()[0]
    >>> items = [a, i, d]
    >>> for i in ResourceIterator(items):
    ...     print i
    ...
    Article Resource
    Image Resource
    Downloadablefile Resource

When we passed a list of an Article, Image and Downloadable File to :py:class:`ResourceIterator` we got back an iterator of their corresponding resources.

