===============
Model Reference
===============


RelatedResource
===============

.. py:class:: RelatedResource

   .. py:attribute:: source_id

      :py:class:`IntegerField`

      The ``id`` of the source object. Part of a generic relation to the source object.

   .. py:attribute:: source_type

      :py:class:`ForeignKey` ``(django.contrib.contenttypes.models.ContentType)``

      The :py:class:`ContentType` of the source object. Part of the generic relation to the source object.

   .. py:attribute:: source_object

      :py:class:`GenericForeignKey`

      The source object as defined by the ``source_id`` and ``source_type``\ .

   .. py:attribute:: object_id

      :py:class:`IntegerField`

      The ``id`` of the related object. Part of a generic relation to the related object.

   .. py:attribute:: object_type

      :py:class:`ForeignKey` ``(django.contrib.contenttypes.models.ContentType)``

      The :py:class:`ContentType` of the related object. Part of the generic relation to the related object.

   .. py:attribute:: object

      :py:class:`GenericForeignKey`

      The related object as defined by the ``object_id`` and ``object_type``\ .

   .. py:attribute:: relation_source

      :py:class:`IntegerField`

      Currently unused, but hopefully will be used to allow multiple types of resource relationships in a future version.

   .. py:attribute:: relation_type

      :py:class:`CharField` ``(255)``

      This is a free-form field for specifying how the related object is linked to the source object.

   .. py:attribute:: order

      :py:class:`IntegerField`

      Allows for establishing an order to the related objects.

