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

      :py:class:`ForeignKey` ``(`` :ref:`key_image_model` ``)``

      An override of the key image of the ``content_object`` using a related model as defined in :ref:`key_image_model`. It will use the ``content_object``'s mapped key image if blank.

   .. py:attribute:: credit

      :py:class:`CharField` ``(255)``

      An override of the credit of the ``content_object``. It will use the ``content_object``'s mapped credit if blank.

   .. py:attribute:: url

      :py:class:`CharField` ``(255)``

      An override of the URL of the ``content_object``. It will use the ``content_object``'s mapped URL if blank.



ModelName
=========

.. py:class:: ModelName

   .. py:attribute:: parent

      :py:class:`TreeForeignKey` ``(self)``

      The category's parent category. Leave this blank for an root category.

   .. py:attribute:: name

      **Required** ``CharField(100)``

      The name of the category.

   .. py:attribute:: slug

      **Required** ``SlugField``

      URL-friendly title. It is automatically generated from the title.

   .. py:attribute:: active

      **Required** ``BooleanField`` *default:* ``True``

      Is this item active. If it is inactive, all children are set to inactive as well.

