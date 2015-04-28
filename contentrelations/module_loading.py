import copy
from importlib import import_module
from django.utils.module_loading import module_has_submodule


def autodiscover_modules(*args, **kwargs):
    """
    Copied from django.utils.module_loading in Django 1.7

    Modified to allow skippable apps.

    Auto-discover INSTALLED_APPS modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.

    You may provide a register_to keyword parameter as a way to access a
    registry. This register_to object must have a _registry instance variable
    to access it.
    """
    from django.apps import apps

    register_to = kwargs.get('register_to')
    skip_apps = kwargs.get('skip_apps', [])
    for app_config in apps.get_app_configs():
        if app_config.name in skip_apps:
            continue
        for module_to_search in args:
            # Attempt to import the app's module.
            try:
                if register_to:
                    before_import_registry = copy.copy(register_to._registry)

                import_module('%s.%s' % (app_config.name, module_to_search))
            except:
                # Reset the registry to the state before the last import
                # as this import will have to reoccur on the next request and
                # this could raise NotRegistered and AlreadyRegistered
                # exceptions (see #8245).
                if register_to:
                    register_to._registry = before_import_registry

                # Decide whether to bubble up this error. If the app just
                # doesn't have the module in question, we can ignore the error
                # attempting to import it, otherwise we want it to bubble up.
                if module_has_submodule(app_config.module, module_to_search):
                    raise
