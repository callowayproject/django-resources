from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.models import BaseModelFormSet
from django.utils.text import capfirst


class InlineGenericForeignKeyHiddenInput(forms.MultiWidget):
    def _has_changed(self, initial, data):
        return False

    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
        )
        super(InlineGenericForeignKeyHiddenInput, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            try:
                decompressed = [int(x) for x in value.split('-')]
                return decompressed
            except ValueError:
                pass
        return [None, None]


class InlineGenericForeignKeyField(forms.MultiValueField):
    """
    A basic integer field that deals with validating the given value to a
    given parent instance in an inline.
    """
    widget = InlineGenericForeignKeyHiddenInput
    hidden_widget = InlineGenericForeignKeyHiddenInput

    default_error_messages = {
        'invalid_choice': _('The inline generic foreign key did not match the ' \
                            'parent instance.'),
        'invalid_type': _('The inline generic foregin key did not get a list of' \
                          ' values.')
    }

    def __init__(self, parent_instance, *args, **kwargs):
        self.parent_instance = parent_instance
        self.content_type = ContentType.objects.get_for_model(parent_instance)
        self.object_id = parent_instance.pk
        fields = (
            forms.models.InlineForeignKeyField(parent_instance, required=False),
            forms.IntegerField(widget=forms.HiddenInput, required=False),
        )
        kwargs['initial'] = "%s-%s" % (self.content_type.pk, self.object_id)
        super(InlineGenericForeignKeyField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            self.content_type = ContentType.objects.get(id=data_list[0])
            self.object_id = data_list[1]
            compressed = "-".join(data_list)
            return compressed
        return None

    def clean(self, value):
        for i in value:
            if not i:
                return None
        try:
            if not isinstance(value, (tuple, list)):
                raise ValidationError(self.error_messages['invalid_type'])
            if len(value) == 2 and \
                int(value[0]) == self.content_type.pk and \
                int(value[1]) == self.object_id:
                return self.compress(value)
            else:
                raise ValidationError(self.error_messages['invalid_choice'])
        except Exception:
            raise


class GenericM2MInlineFormSet(BaseModelFormSet):
    """
    Basic implementation of a formset with no ForeignKey
    """
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        if instance is None:
            self.instance = self.fk.rel.to()
        else:
            self.instance = instance
        self.save_as_new = save_as_new
        self.rel_name = 'related'
        if queryset is None:
            queryset = self.model._default_manager
        qs = self.instance.related.all()
        super(GenericM2MInlineFormSet, self).__init__(data, files,
                                          prefix=prefix, queryset=qs, **kwargs)

    @classmethod
    def get_default_prefix(cls):
        return 'genericm2mform'

    def initial_form_count(self):
        if self.save_as_new:
            return 0
        return super(GenericM2MInlineFormSet, self).initial_form_count()

    def _construct_form(self, i, **kwargs):
        form = super(GenericM2MInlineFormSet, self)._construct_form(i, **kwargs)
        if self.save_as_new:
            # Remove the primary key from the form's data, we are only
            # creating new instances
            form.data[form.add_prefix(self._pk_field.name)] = None

            # Remove the foreign key from the form's data
            form.data[form.add_prefix(self.fk.name)] = None

        # Set the fk value here so that the form can do it's validation.
        #setattr(form.instance, self.fk.get_attname(), self.instance.pk)
        return form

    def save_new(self, form, commit=True):
        # Use commit=False so we can assign the parent key afterwards, then
        # save the object.
        obj = form.save(commit=False)
        obj.parent = form.fields['parent'].parent_instance
        obj.object = form.cleaned_data['object_type'].get_object_for_this_type(
            id=form.cleaned_data['object_id']
        )
        if commit:
            obj.save()
        # form.save_m2m() can be called via the formset later on if commit=False
        if commit and hasattr(form, 'save_m2m'):
            form.save_m2m()
        return obj

    def save_new_objects(self, commit=True):
        self.new_objects = []
        for form in self.extra_forms:
            if not form.has_changed():
                continue
            # If someone has marked an add form for deletion, don't save the
            # object.
            # if self.can_delete and self._should_delete_form(form):
            #     continue
            self.new_objects.append(self.save_new(form, commit=commit))
            if not commit:
                self.saved_forms.append(form)
        return self.new_objects

    def save(self, commit=True):
        """
        Saves model instances for every form, adding and changing instances
        as necessary, and returns the list of instances.
        """
        if not commit:
            self.saved_forms = []

            def save_m2m():
                for form in self.saved_forms:
                    form.save_m2m()
            self.save_m2m = save_m2m
        return self.save_existing_objects(commit) + self.save_new_objects(commit)

    def add_fields(self, form, index):
        super(GenericM2MInlineFormSet, self).add_fields(form, index)
        # The foreign key field might not be on the form, so we poke at the
        # Model field to get the label, since we need that for error messages.
        name = self.fk.name
        default_label = capfirst(self.fk.verbose_name)
        kwargs = {
            'label': getattr(form.fields.get(name), 'label', default_label)
        }

        form.fields[name] = InlineGenericForeignKeyField(self.instance, **kwargs)
        # Add the generated field to form._meta.fields if it's defined to make
        # sure validation isn't skipped on that field.
        if form._meta.fields:
            if isinstance(form._meta.fields, tuple):
                form._meta.fields = list(form._meta.fields)
            form._meta.fields.append(self.fk.name)

    def get_unique_error_message(self, unique_check):
        unique_check = [field for field in unique_check if field != self.fk.name]
        return super(GenericM2MInlineFormSet, self).get_unique_error_message(unique_check)


def genericm2m_inlineformset_factory(parent_model, model, form=forms.ModelForm,
                          formset=GenericM2MInlineFormSet, fk_name=None,
                          fields=None, exclude=None,
                          extra=3, can_order=True, can_delete=True, max_num=None,
                          formfield_callback=None):
    """
    Returns an ``InlineFormSet`` for the given kwargs.

    You must provide ``fk_name`` if ``model`` has more than one ``ForeignKey``
    to ``parent_model``.
    """
    fk = generic.GenericRelation(parent_model, verbose_name='parent', related_name='related')
    fk.name = 'parent'
    kwargs = {
        'form': form,
        'formfield_callback': formfield_callback,
        'formset': GenericM2MInlineFormSet,
        'extra': extra,
        'can_delete': can_delete,
        'can_order': can_order,
        'fields': fields,
        'exclude': exclude,
        'max_num': max_num,
    }
    FormSet = forms.models.modelformset_factory(model, **kwargs)
    FormSet.fk = fk
    FormSet.parent_type_field = 'parent_type'
    return FormSet


class GFKOptimizedQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        # pop the gfk_field from the kwargs if its passed in explicitly
        self._gfk_field = kwargs.pop('gfk_field', None)

        # call the parent class' initializer
        super(GFKOptimizedQuerySet, self).__init__(*args, **kwargs)

    def _clone(self, *args, **kwargs):
        clone = super(GFKOptimizedQuerySet, self)._clone(*args, **kwargs)
        clone._gfk_field = self._gfk_field
        return clone

    def get_gfk(self):
        if not self._gfk_field:
            for field in self.model._meta.virtual_fields:
                if isinstance(field, GenericForeignKey):
                    self._gfk_field = field
                    break

        return self._gfk_field

    def generic_objects(self):
        clone = self._clone()

        ctypes_and_fks = {}

        gfk_field = self.get_gfk()
        ctype_field = '%s_id' % gfk_field.ct_field
        fk_field = gfk_field.fk_field

        for obj in clone:
            ctype = ContentType.objects.get_for_id(getattr(obj, ctype_field))
            obj_id = getattr(obj, fk_field)

            ctypes_and_fks.setdefault(ctype, [])
            ctypes_and_fks[ctype].append(obj_id)

        gfk_objects = {}
        for ctype, obj_ids in ctypes_and_fks.items():
            gfk_objects[ctype.pk] = ctype.model_class()._default_manager.in_bulk(obj_ids)

        obj_list = []
        for obj in clone:
            obj_list.append(gfk_objects[getattr(obj, ctype_field)][getattr(obj, fk_field)])

        return obj_list


class RelatedObjectsDescriptor(object):
    def __init__(self, model=None, from_field='parent', to_field='object'):
        from .models import RelatedResource
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

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model_class = cls
        setattr(cls, self.name, self)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        ManagerClass = type(self.related_model._default_manager)
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
            def get_query_set(self):
                if uses_gfk:
                    qs = GFKOptimizedQuerySet(self.model, gfk_field=rel_field)
                    return qs.filter(**(core_filters))
                else:
                    return superclass.get_query_set(self).filter(**(core_filters))

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
                return superclass.get_query_set(self).filter(
                    Q(**rel_obj.get_query_from(instance)) |
                    Q(**rel_obj.get_query_to(instance))
                ).distinct()

        manager = RelatedManager()
        manager.core_filters = core_filters
        manager.model = self.related_model

        return manager

    def all(self):
        if self.is_gfk(self.from_field):
            ctype = ContentType.objects.get_for_model(self.model_class)
            query = {self.from_field.ct_field: ctype}
        else:
            query = {}
        return self.related_model._default_manager.filter(**query)
