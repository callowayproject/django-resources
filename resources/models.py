from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from .resources import BaseResource, resource_list
from .settings import RESOURCE_TYPE_CHOICES, IMAGE_STORAGE, KEY_IMAGE_MODEL


class Resource(models.Model):
    """
    An external resources
    """
    resource_type = models.CharField(
        max_length=50,
        choices=RESOURCE_TYPE_CHOICES,
        db_index=True)
    title = models.CharField(
        max_length=255,
        null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    key_image_custom = models.FileField(
        upload_to='resources/resources',
        storage=IMAGE_STORAGE(),
        blank=True, null=True)
    key_image_width = models.IntegerField(blank=True, null=True)
    key_image_height = models.IntegerField(blank=True, null=True)
    if KEY_IMAGE_MODEL:
        key_image_related = models.ForeignKey(KEY_IMAGE_MODEL)
    credit = models.CharField(
        max_length=255,
        blank=True, null=True)
    url = models.CharField(
        max_length=255,
        blank=True, null=True)
    citation = models.CharField(
        max_length=255,
        blank=True, null=True)
    notes = models.CharField(
        max_length=255,
        blank=True, null=True)
    internal_ref = models.CharField(
        max_length=255,
        blank=True, null=True)

resource_list.register(Resource, BaseResource)


class Slide(models.Model):
    """
    An wrapper around another model
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    resource_type = models.CharField(
        max_length=50,
        choices=RESOURCE_TYPE_CHOICES,
        db_index=True)
    title = models.CharField(
        max_length=255,
        null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    key_image_custom = models.FileField(
        upload_to='resources/slides',
        storage=IMAGE_STORAGE(),
        blank=True, null=True)
    key_image_width = models.IntegerField(blank=True, null=True)
    key_image_height = models.IntegerField(blank=True, null=True)
    if KEY_IMAGE_MODEL:
        key_image_related = models.ForeignKey(KEY_IMAGE_MODEL)
    credit = models.CharField(
        max_length=255,
        blank=True, null=True)
    url = models.CharField(
        max_length=255,
        blank=True, null=True)
    citation = models.CharField(
        max_length=255,
        blank=True, null=True)
    notes = models.TextField(
        blank=True, null=True)
    internal_ref = models.CharField(
        max_length=255,
        blank=True, null=True)

resource_list.register(Slide, BaseResource)
