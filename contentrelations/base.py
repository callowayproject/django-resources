from collections import defaultdict


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
        if hasattr(self.instance, '_meta'):
            return self.instance._meta.verbose_name
        else:
            return self.instance.__class__.__name__

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

    def group_by(self, attrname):
        """
        Return a dictionary where the keys are distinct values of attrname and
        the values are a list of Resources
        """
        from django.template.defaultfilters import slugify
        groups = defaultdict(list)
        for item in self.__iter__():
            val = slugify(getattr(item, attrname, 'unknown')).replace('-', '_')
            groups[val].append(item)
        return dict(groups)


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
            if hasattr(i, '_meta'):
                relations.append(
                    Q(app_label=i._meta.app_label, model=i._meta.object_name.lower())
                )
        if relations:
            return reduce(lambda x, y: x | y, relations)
        else:
            return relations

    def register(self, model_or_iterable, resource_class=None):
        from .settings import SETUP_MODELS
        from .registration import monkey_patch
        from .related import ReverseRelatedObjectsDescriptor
        from django.core.exceptions import ImproperlyConfigured

        if resource_class is None:
            resource_class = BaseResource
        if not isinstance(model_or_iterable, (list, tuple)):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if hasattr(model, '_meta') and model._meta.abstract:
                raise ImproperlyConfigured('The model %s is abstract, so it '
                      'cannot be registered with admin.' % model.__name__)

            if model in self._registry:
                return
            self._registry[model] = resource_class
            monkey_patch(model, 'related_from', ReverseRelatedObjectsDescriptor())
            if hasattr(model, '_meta'):
                model_str = "%s.%s" % (model._meta.app_label, model.__name__)
                if model_str in SETUP_MODELS:
                    for field in SETUP_MODELS[model_str]:
                        monkey_patch(model, field)

    def get_for_instance(self, instance):
        """
        Return the registered resource instance for the instance passed
        """
        from .related import RelatedResource
        try:
            if isinstance(instance, RelatedResource):
                instance = instance.object
            resource_class = self._registry[instance.__class__]
            return resource_class(instance)
        except KeyError:
            return None

    def __getitem__(self, key):
        """
        mapping for _registry
        """
        return self._registry[key]

resource_list = ResourceList()

try:
    from django.core.paginator import Paginator, Page

    class ResourcePage(Page):
        def __getitem__(self, index):
            from django.utils import six
            if not isinstance(index, (slice,) + six.integer_types):
                raise TypeError
            # The object_list is converted to a list so that if it was a QuerySet
            # it won't be a database hit per __getitem__.
            if not isinstance(self.object_list, list):
                self.object_list = list(self.object_list)
            return resource_list.get_for_instance(self.object_list[index])

    class ResourcePaginator(Paginator):
        def _get_page(self, *args, **kwargs):
            """
            Returns an instance of a single page.

            This hook can be used by subclasses to use an alternative to the
            standard :cls:`Page` object.
            """
            return ResourcePage(*args, **kwargs)
except ImportError:
    pass
