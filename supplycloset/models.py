from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from .base import BaseResource, resource_list
from .settings import RESOURCE_TYPE_CHOICES, IMAGE_STORAGE, KEY_IMAGE_MODEL

# So this model gets created
from .related import RelatedResource


class ExternalResource(models.Model):
    """
    An external resource
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
        upload_to='supplycloset/externalresources',
        storage=IMAGE_STORAGE(),
        blank=True, null=True)
    key_image_width = models.IntegerField(blank=True, null=True)
    key_image_height = models.IntegerField(blank=True, null=True)
    if KEY_IMAGE_MODEL:
        key_image_related = models.ForeignKey(KEY_IMAGE_MODEL, blank=True, null=True)
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
    overrides = ['resource_type', 'title', 'description', 'key_image',
                 'credit', 'url', 'citation', 'notes', 'internal_ref']
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    resource_type_ovr = models.CharField("resource type",
        max_length=50,
        choices=RESOURCE_TYPE_CHOICES,
        db_index=True)
    title_ovr = models.CharField("title",
        max_length=255,
        null=True, blank=True)
    description_ovr = models.TextField("description", null=True, blank=True)
    key_image_custom = models.FileField(
        upload_to='supplycloset/slides',
        storage=IMAGE_STORAGE(),
        blank=True, null=True)
    key_image_width = models.IntegerField(blank=True, null=True)
    key_image_height = models.IntegerField(blank=True, null=True)
    if KEY_IMAGE_MODEL:
        key_image_related = models.ForeignKey(KEY_IMAGE_MODEL, blank=True, null=True)
    credit_ovr = models.CharField("credit",
        max_length=255,
        blank=True, null=True)
    url_ovr = models.CharField("URL",
        max_length=255,
        blank=True, null=True)
    citation_ovr = models.CharField("citation",
        max_length=255,
        blank=True, null=True)
    notes_ovr = models.TextField("notes",
        blank=True, null=True)
    internal_ref_ovr = models.CharField("internal ref",
        max_length=255,
        blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Slide, self).__init__(*args, **kwargs)
        self._resource = None

    @property
    def key_image_ovr(self):
        """
        Return the key_image_related or key_image_custom
        """
        if self.key_image_custom:
            return self.key_image_custom
        return getattr(self, 'key_image_related', None)

    @property
    def resource(self):
        if self._resource is None and self.content_object:
            self._resource = resource_list.get_for_instance(self.content_object)

        return self._resource

    def __getattr__(self, name):
        """
        Return either the overriddden value, or the original value, or raise
        and AttributeError.
        """
        if name in self.overrides:
            value = getattr(self, "%s_ovr" % name)
            if value:
                return value
            if self.content_object:
                return getattr(self.resource, name)
        raise AttributeError("'Slide' object has no attribute '%s'" % name)


resource_list.register(Slide, BaseResource)

from supplycloset import autodiscover
autodiscover()

from supplycloset.settings import SETUP_MODELS
from supplycloset.registration import monkey_patch
for model, fields in SETUP_MODELS.items():
    for field in fields:
        monkey_patch(model, field)
