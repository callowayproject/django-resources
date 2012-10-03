=========
Resources
=========

BaseResource
============

.. py:class:: BaseResource

   This class provides an abstraction for unifying access to different resources under a common interface. If a resource doesn't have a ``FOO`` attribute, the subclass should defined a ``get_FOO`` method that returns the appropriate value.

   .. py:attribute:: missing_attribute_value

      :py:class:`str` *Default:* ``''``

      The value returned when all methods of retrieving it has failed. Only used if :py:attr:`BaseResource.raise_error_on_missing` is ``False``

   .. py:attribute:: raise_error_on_missing

      :py:class:`bool` *Default:* ``False``

      An :py:class:`AttributeError` should be raised when all methods of retrieving it has failed.

   .. py:attribute:: instance

      :py:class:`object`

      Set during instantiation, this is the instance used to resolve all attribute requests.

   .. py:method:: get_resource_type()

      This is the ``get_FOO`` method used when attempting to resolve the ``resource_type`` attribute. By default it returns the ``verbose_name`` of the ``instance``.

   .. py:method:: get_url()

      This is the ``get_FOO`` method used when attempting to resolve the ``url`` attribute. by default it returns the value from ``instance.get_absolute_url()``

ResourceList
============

.. py:class:: ResourceList

   This class provides the registry of models to their sub-classed :py:class:`BaseResource` models. It is instantiated for use in :ref:`resource_list`.

   .. py:method:: content_types_lookup() -> Q object

      Returns a :py:class:`Q` object used for limiting :py:class:`ContentType` objects for selection to only those registered.

   .. py:method:: get_for_instance(instance) -> BaseResource

      :param instance: An instance of a ``Model``

      Returns the registered resource for the passed instance instantiated with that instance.

   .. py:method:: register(model_or_iterable, resource_class)

      :param model_or_iterable: The :py:class:`Model` or an iterable of :py:class:`Model` to link with a resource class.
      :type model_or_iterable: ``Model``, ``tuple`` or ``list``
      :param BaseResource resource_class: The :py:class:`BaseResource` subclass to link with the model or models given.

.. _resource_list:

resource_list
=============

**from contentrelations import resource_list**

The instantiated :py:class:`ResourceList` used for registering :py:class:`Model`\ s with their :py:class:`BaseResource` sub-classes.


ResourceIterator
================

.. py:class:: ResourceIterator

   This class wraps any iterator or sequence and returns each item's registered Resource class.
