from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.admin.utils import flatten_fieldsets
except ImportError:
    from django.contrib.admin.util import flatten_fieldsets
from functools import partial

from .related import RelatedResource
from .generic import genericm2m_inlineformset_factory


class GenericCollectionInlineModelAdmin(GenericInlineModelAdmin):
    ct_field = "content_type"
    ct_fk_field = "object_id"

    def __init__(self, parent_model, admin_site):
        super(GenericCollectionInlineModelAdmin, self).__init__(parent_model, admin_site)
        from django.core.urlresolvers import reverse, NoReverseMatch
        ctypes = ContentType.objects.all().order_by('id').values_list('id', 'app_label', 'model')
        elements = {}
        for x, y, z in ctypes:
            try:
                elements[x] = reverse("admin:%s_%s_changelist" % (y, z))
            except NoReverseMatch:
                continue
        self.content_types = "{%s}" % ",".join(["'%s': '%s'" % (k, v) for k, v in elements.items()])

    def get_formset(self, request, obj=None, **kwargs):
        """
        Returns a BaseInlineFormSet class for use in admin add/change views.
        """
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        # exclude.extend(self.get_readonly_fields(request, obj))
        if self.exclude is None and hasattr(self.form, '_meta') and self.form._meta.exclude:
            # Take the custom ModelForm's Meta.exclude into account only if the
            # InlineModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)
        # if exclude is an empty list we use None, since that's the actual
        # default
        exclude = exclude or None
        # can_delete = self.can_delete and self.has_delete_permission(request, obj)
        defaults = {
            "form": self.form,
            "formset": self.formset,
            "fk_name": self.fk_name,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": partial(self.formfield_for_dbfield, request=request),
            "extra": self.extra,
            "max_num": self.max_num,
            # "can_delete": can_delete,
        }
        defaults.update(kwargs)
        result = genericm2m_inlineformset_factory(self.parent_model, self.model, **defaults)
        result.content_types = self.content_types
        result.ct_fk_field = self.ct_fk_field
        return result


class GenericCollectionTabularInline(GenericCollectionInlineModelAdmin):
    template = 'admin/edit_inline/related_resource_inline.html'


class RelatedInline(GenericCollectionTabularInline):
    model = RelatedResource
    exclude = ('source_type', 'source_id')

    def get_formset(self, request, obj=None, **kwargs):
        """
        Adds a rel_name attribute to the formset for reverse lookups
        """
        result = super(RelatedInline, self).get_formset(request, obj, **kwargs)
        result.rel_name = getattr(self, 'rel_name', 'related')
        name = getattr(self, 'verbose_name_plural', result.model._meta.verbose_name_plural)
        result.verbose_name_plural = name
        return result

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        from .base import resource_list
        if db_field.name == "object_type":
            db_field.rel.limit_choices_to = resource_list.content_types_lookup()
        return super(RelatedInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, *args, **kwargs):
        return True

    class Media:
        js = ("contentrelations/js/genericlookup.js",)
