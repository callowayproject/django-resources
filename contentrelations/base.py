from django.core.exceptions import ImproperlyConfigured


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class BaseResource(object):
    """
    Base class that allows for mapping of a model to resource information
    """
    missing_attribute_value = ''
    raise_error_on_missing = False

    def __init__(self, instance):
        self.instance = instance

    def get_resource_name(self):
        return self.instance._meta.verbose_name

    def get_url(self):
        gau = getattr(self.instance, 'get_absolute_url', '')
        if gau:
            return gau()
        return ''

    def __getattr__(self, name):
        """
        Try to get ``name`` from a get_FOO method or the original object

        Remember: __getattr__ is only called when ``name`` is not found.

        This method could get recursively called twice, the first time, it will
        add ``get_`` to the beginning at try again. Then it tries the self.instance
        """
        if name.startswith("get_"):
            try:
                import re
                original_name = re.sub(r"^get_", "", name)
                return getattr(self.instance, original_name)
            except AttributeError:
                if self.raise_error_on_missing:
                    raise
                else:
                    return self.missing_attribute_value
        else:
            accessor_name = "get_%s" % name
            get_value = getattr(self, accessor_name, False)
            if callable(get_value):
                return get_value()
            else:
                return get_value

    def __str__(self):
        return "%s Resource" % self.get_resource_name().capitalize()


class ResourceIterator(list):
    """
    Takes a sequence of objects, and returns the resource class registered for it
    when iterated against
    """
    def __getitem__(self, key):
        val = super(ResourceIterator, self).__getitem__(key)
        return resource_list.get_for_instance(val)

    def __iter__(self):
        for item in super(ResourceIterator, self).__iter__():
            yield resource_list.get_for_instance(item)


class ResourceList(object):
    """
    A ResourceList object encapsulates an group of Resources. Models are
    registered with the ResourceList using the register() method.
    """
    def __init__(self):
        self._registry = {}

    def content_types_lookup(self):
        """
        Return the a query lookup for ContentType models registered.
        """
        from django.db.models import Q
        relations = []
        for i in self._registry.keys():
            relations.append(
                Q(app_label=i._meta.app_label, model=i._meta.object_name.lower())
            )
        if relations:
            return reduce(lambda x, y: x | y, relations)
        else:
            return relations

    def register(self, model_or_iterable, resource_class=None):
        from django.db.models.base import ModelBase
        from .settings import SETUP_MODELS
        from .registration import monkey_patch

        if resource_class is None:
            resource_class = BaseResource
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured('The model %s is abstract, so it '
                      'cannot be registered with admin.' % model.__name__)

            if model in self._registry:
                #raise AlreadyRegistered('The model %s is already registered' % model.__name__)
                return
            self._registry[model] = resource_class
            model_str = "%s.%s" % (model._meta.app_label, model.__name__)
            if model_str in SETUP_MODELS:
                for field in SETUP_MODELS[model_str]:
                    monkey_patch(model, field)

    def get_for_instance(self, instance):
        """
        Return the registered resource instance for the instance passed
        """
        resource_class = self._registry[instance.__class__]
        return resource_class(instance)

    def __getitem__(self, key):
        """
        mapping for _registry
        """
        return self._registry[key]

resource_list = ResourceList()
