===============
Model Reference
===============

Slide
=====

.. py:class:: Slide

   .. py:attribute:: object_id

      :py:class:`IntegerField`

      Part of the generic relation for the resource this slide is augmenting.

   .. py:attribute:: content_type

      :py:class:`ForeignKey` ``(django.contrib.contenttypes.models.ContentType)``

      Part of the generic relation for the resource this slide is augmenting.

   .. py:attribute:: content_object

      :py:class:`GenericForeginKey`

      Part of the generic relation for the resource this slide is augmenting.

   .. py:attribute:: resource_type

      :py:class:`CharField` ``(50)``

      An override of the ``content_object``'s resource type. Choices are displayed if specified in RESOURCE_TYPE_CHOICES. It will use the ``content_object``'s mapped resource type if blank.

   .. py:attribute:: title

      :py:class:`CharField` ``(100)``

      An override of the title of the ``content_object``. It will use the ``content_object``'s mapped title if blank.

   .. py:attribute:: description

      :py:class:`TextField`

      An override of the description of the ``content_object``. It will use the ``content_object``'s mapped description if blank.

   .. py:attribute:: key_image_custom

      :py:class:`FileField`

      An override of the key image of the ``content_object``. It will use the ``content_object``'s mapped key image if blank.

   .. py:attribute:: key_image_width

      **Read only** :py:class:`IntegerField`

      Automatically set to the width of ``key_image_custom`` image when uploaded.

   .. py:attribute:: key_image_height

      **Read only** :py:class:`IntegerField`

      Automatically set to the height of ``key_image_custom`` image when uploaded.

   .. py:attribute:: key_image_related

      :py:class:`ForeignKey` ``(`` :ref:`key_image_model_setting` ``)``

      An override of the key image of the ``content_object`` using a related model as defined in :ref:`key_image_model_setting`. It will use the ``content_object``'s mapped key image if blank.

   .. py:attribute:: credit

      :py:class:`CharField` ``(255)``

      An override of the credit of the ``content_object``. It will use the ``content_object``'s mapped credit if blank.

   .. py:attribute:: url

      :py:class:`CharField` ``(255)``

      An override of the URL of the ``content_object``. It will use the ``content_object``'s mapped URL if blank.

   .. py:attribute:: citation

      :py:class:`CharField` ``(255)``

      An override of the citation of the ``content_object``. It will use the ``content_object``'s mapped citation if blank.

   .. py:attribute:: notes

      :py:class:`TextField`

      An override of the notes of the ``content_object``. It will use the ``content_object``'s mapped notes if blank.

   .. py:attribute:: internal_ref

      :py:class:`CharField` ``(255)``

      An override of the internal_ref of the ``content_object``. It will use the ``content_object``'s mapped internal_ref if blank.


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

