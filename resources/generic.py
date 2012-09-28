from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
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
        for value in value:
            if not value:
                return None
        try:
            if len(value) == 2 and \
                int(value[0]) == self.content_type.pk and \
                int(value[1]) == self.object_id:
                return self.compress(value)
            else:
                raise ValidationError(self.error_messages['invalid'])
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
        super(GenericM2MInlineFormSet, self).__init__(data, files, prefix=prefix,
                                                queryset=qs, **kwargs)

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
        obj.object = form.cleaned_data['object_type'].get_object_for_this_type(id=form.cleaned_data['object_id'])
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
        """Saves model instances for every form, adding and changing instances
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
        kwargs = {
            'label': getattr(form.fields.get(name), 'label', capfirst(self.fk.verbose_name))
        }

        form.fields[name] = InlineGenericForeignKeyField(self.instance, **kwargs)
        # # Add the generated field to form._meta.fields if it's defined to make
        # # sure validation isn't skipped on that field.
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
                          extra=3, can_order=False, can_delete=True, max_num=None,
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
