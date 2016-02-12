from django.db.models import Q
from django.db import models
from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from .generic import GFKOptimizedQuerySet


class RelatedResourceManager(models.Manager):
    def get_content_type(self, content_type, **kwargs):
        """
        Get all the items of the given content type related to this item.
        """
        qs = self.get_queryset()
        return qs.filter(content_type__name=content_type, **kwargs)

    def get_relation_source(self, relation_source, **kwargs):
        """
        Get all the items of the given relation source to this item
        """
        qs = self.get_queryset()
        return qs.filter(relation_source=relation_source, **kwargs)


class RelatedResource(models.Model):
    """
    A resource related to another object
    """
    # SOURCE OBJECT
    source_type = models.ForeignKey(ContentType,
        related_name="child_relatedobjects")
    source_id = models.IntegerField(db_index=True)
    source = GenericForeignKey(
        ct_field="source_type",
        fk_field="source_id")

    # ACTUAL RELATED OBJECT:
    object_type = models.ForeignKey(ContentType,
        related_name="related_objects",)
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
        ordering = ('order', )

    def __unicode__(self):
        out = u'%s related to %s' % (self.source, self.object)
        if self.relation_type:
            return "%s (%s)" % (out, self.relation_type)
        else:
            return out


class RelatedObjectsDescriptor(object):
    def __init__(self, model=None, from_field='source', to_field='object'):
        self.related_model = model or RelatedResource
        self.from_field = self.get_related_model_field(from_field)
        self.to_field = self.get_related_model_field(to_field)

    def get_related_model_field(self, field_name):
        opts = self.related_model._meta
        for virtual_field in opts.virtual_fields:
            if virtual_field.name == field_name:
                return virtual_field
        return opts.get_field(field_name)

    def is_gfk(self, field):
        return isinstance(field, GenericForeignKey)

    def get_query_for_field(self, instance, field):
        if self.is_gfk(field):
            ctype = ContentType.objects.get_for_model(instance)
            return {
                field.ct_field: ctype,
                field.fk_field: instance.pk
            }
        elif isinstance(instance, field.rel.to):
            return {field.name: instance}

        raise TypeError('Unable to query %s with %s' % (field, instance))

    def get_query_from(self, instance):
        return self.get_query_for_field(instance, self.from_field)

    def get_query_to(self, instance):
        return self.get_query_for_field(instance, self.to_field)

    def set_attributes_from_name(self, name):
        self.name = name
        self.concrete = False
        self.verbose_name = self.name.replace('_', ' ')

    def contribute_to_class(self, cls, name, virtual_only=False):
        self.set_attributes_from_name(name)
        self.model = cls
        # if virtual_only:
        #     cls._meta.add_virtual_field(self)
        # else:
        #     cls._meta.add_field(self)
        setattr(cls, self.name, self)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        ManagerClass = type(self.related_model._default_manager)  # NOQA
        return self.create_manager(instance, ManagerClass)

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("Manager must be accessed via instance")

        manager = self.__get__(instance)
        manager.add(*value)

    def delete_manager(self, instance):
        return self.create_manager(instance,
                self.related_model._base_manager.__class__)

    def create_manager(self, instance, superclass, cf_from=True):
        rel_obj = self
        if cf_from:
            core_filters = self.get_query_from(instance)
            rel_field = self.to_field
        else:
            core_filters = self.get_query_to(instance)
            rel_field = self.from_field
        uses_gfk = self.is_gfk(rel_field)

        class RelatedManager(superclass):
            def get_queryset(self):
                if uses_gfk:
                    qs = GFKOptimizedQuerySet(self.model, gfk_field=rel_field)
                    return qs.filter(**(core_filters))
                else:
                    return superclass.get_queryset(self).filter(**(core_filters))

            def add(self, *objs):
                for obj in objs:
                    if not isinstance(obj, self.model):
                        raise TypeError("'%s' instance expected" % self.model._meta.object_name)
                    for (k, v) in core_filters.iteritems():
                        setattr(obj, k, v)
                    obj.save()
            add.alters_data = True

            def create(self, **kwargs):
                kwargs.update(core_filters)
                return super(RelatedManager, self).create(**kwargs)
            create.alters_data = True

            def get_or_create(self, **kwargs):
                kwargs.update(core_filters)
                return super(RelatedManager, self).get_or_create(**kwargs)
            get_or_create.alters_data = True

            def remove(self, *objs):
                for obj in objs:
                    # Is obj actually part of this descriptor set?
                    if obj in self.all():
                        obj.delete()
                    else:
                        raise rel_obj.related_model.DoesNotExist, \
                            "%r is not related to %r." % (obj, instance)
            remove.alters_data = True

            def clear(self):
                self.all().delete()
            clear.alters_data = True

            def connect(self, obj, **kwargs):
                kwargs.update(rel_obj.get_query_to(obj))
                connection, created = self.get_or_create(**kwargs)
                return connection

            def related_to(self):
                mgr = rel_obj.create_manager(instance, superclass, False)
                return mgr.filter(
                    **rel_obj.get_query_to(instance)
                )

            def symmetrical(self):
                return superclass.get_queryset(self).filter(
                    Q(**rel_obj.get_query_from(instance)) |
                    Q(**rel_obj.get_query_to(instance))
                ).distinct()

        manager = RelatedManager()
        manager.core_filters = core_filters
        manager.model = self.related_model

        return manager

    def all(self):
        if self.is_gfk(self.from_field):
            ctype = ContentType.objects.get_for_model(self.model)
            query = {self.from_field.ct_field: ctype}
        else:
            query = {}
        return self.related_model._default_manager.filter(**query)


class ReverseRelatedObjectsDescriptor(RelatedObjectsDescriptor):
    def __init__(self, model=None, from_field='object', to_field='source'):
        super(ReverseRelatedObjectsDescriptor, self).__init__(model, from_field, to_field)
