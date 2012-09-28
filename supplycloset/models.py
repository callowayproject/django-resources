from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from .resources import BaseResource, resource_list
from .settings import RESOURCE_TYPE_CHOICES, IMAGE_STORAGE, KEY_IMAGE_MODEL


class ExternalResource(models.Model):
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

resource_list.register(ExternalResource, BaseResource)


class Slide(models.Model):
    """
    An wrapper around another model
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
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


class RelatedResourceManager(models.Manager):
    def get_content_type(self, content_type, **kwargs):
        """
        Get all the items of the given content type related to this item.
        """
        qs = self.get_query_set()
        return qs.filter(content_type__name=content_type, **kwargs)

    def get_relation_source(self, relation_source, **kwargs):
        """
        Get all the items of the given relation source to this item
        """
        qs = self.get_query_set()
        return qs.filter(relation_source=relation_source, **kwargs)


class RelatedResource(models.Model):
    """
    A resource related to another object
    """
    # SOURCE OBJECT
    parent_type = models.ForeignKey(ContentType,
        related_name="child_relatedobjects")
    parent_id = models.IntegerField(db_index=True)
    parent = GenericForeignKey(
        ct_field="parent_type",
        fk_field="parent_id")

    # ACTUAL RELATED OBJECT:
    object_type = models.ForeignKey(ContentType,
        related_name="related_objects",
        limit_choices_to=resource_list.content_types_lookup())
    object_id = models.IntegerField(db_index=True)
    object = GenericForeignKey(
        ct_field="object_type",
        fk_field="object_id")

    # METADATA
    relation_source = models.IntegerField(
        editable=False,
        blank=True, null=True)
    relation_type = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    order = models.IntegerField(
        blank=True, null=True)

    objects = RelatedResourceManager()

    class Meta:
        ordering = ('relation_source', 'parent_type', 'parent_id', 'order', )

    def __unicode__(self):
        return u'%s related to %s' % (self.parent, self.object)
