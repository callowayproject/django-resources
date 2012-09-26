from django.core.exceptions import ImproperlyConfigured


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class BaseResource(object):
    """
    Base class that allows for mapping of a model to resource information
    """
    def __init__(self, model):
        self.model = model

    def resource_name(self):
        return self.model._meta.verbose_name

    def get_resource_type(self):
        return getattr(self.model, 'resource_type', '')

    def get_title(self):
        return getattr(self.model, 'title', '')

    def get_description(self):
        return getattr(self.model, 'description', '')

    def get_key_image(self):
        return getattr(self.model, 'key_image', '')

    def get_credit(self):
        return getattr(self.model, 'credit', '')

    def get_url(self):
        gau = getattr(self.model, 'get_absolute_url', '')
        if gau:
            return gau()

    def get_citation(self):
        return getattr(self.model, 'citation', '')

    def get_notes(self):
        return getattr(self.model, 'notes', '')

    def get_internal_ref(self):
        return getattr(self.model, 'internal_ref', '')

    @property
    def resource_type(self):
        return self.get_resource_type()

    @property
    def title(self):
        return self.get_title()

    @property
    def description(self):
        return self.get_description()

    @property
    def key_image(self):
        return self.get_key_image()

    @property
    def credit(self):
        return self.get_credit()

    @property
    def notes(self):
        return self.get_notes()

    @property
    def citation(self):
        return self.get_citation()

    @property
    def internal_ref(self):
        return self.get_internal_ref()


class ResourceList(object):
    """
    A ResourceList object encapsulates an group of Resources. Models are
    registered with the ResourceList using the register() method.
    """
    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, resource_class=None):
        from django.db.models.base import ModelBase

        if resource_class is None:
            resource_class = BaseResource
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured('The model %s is abstract, so it '
                      'cannot be registered with admin.' % model.__name__)

            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            self._registry[model] = resource_class(model)

resource_list = ResourceList()
