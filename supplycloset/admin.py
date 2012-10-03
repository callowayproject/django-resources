from django.contrib import admin

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.util import flatten_fieldsets
from functools import partial

from .models import RelatedResource
from .generic import genericm2m_inlineformset_factory


class GenericCollectionInlineModelAdmin(admin.options.InlineModelAdmin):
    ct_field = "content_type"
    ct_fk_field = "object_id"

    def __init__(self, parent_model, admin_site):
        super(GenericCollectionInlineModelAdmin, self).__init__(parent_model, admin_site)
        ctypes = ContentType.objects.all().order_by('id').values_list('id', 'app_label', 'model')
        elements = ["%s: '%s/%s'" % (x, y, z) for x, y, z in ctypes]
        self.content_types = "{%s}" % ",".join(elements)

    def get_formset(self, request, obj=None, **kwargs):
        """Returns a BaseInlineFormSet class for use in admin add/change views."""
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

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        from .base import resource_list
        if db_field.name == "object_type":
            db_field.rel.limit_choices_to = resource_list.content_types_lookup()
        return super(RelatedInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, *args, **kwargs):
        return True

    class Media:
        js = ("supplycloset/js/genericlookup.js",)
