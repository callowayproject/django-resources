"""
Allows connecting any object to any other object and unifying the interface
between all the objects.
"""
__version_info__ = {
    'major': 1,
    'minor': 1,
    'micro': 1,
    'releaselevel': 'final',
    'serial': 1
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0], __version_info__['serial']))
    return ''.join(vers)

__version__ = get_version()


try:
    import django
    from .base import resource_list, BaseResource  # NOQA

    if django.VERSION[1] > 3:
        def discover(app):
            import copy
            from django.utils.importlib import import_module
            from django.utils.module_loading import module_has_submodule

            mod = import_module(app)
            # Attempt to import the app's resources module.
            try:
                before_import_registry = copy.copy(resource_list._registry)
                import_module('%s.resources' % app)
            except:
                # Reset the model registry to the state before the last import as
                # this import will have to reoccur on the next request and this
                # could raise NotRegistered and AlreadyRegistered exceptions
                # (see #8245).
                resource_list._registry = before_import_registry

                # Decide whether to bubble up this error. If the app just
                # doesn't have an admin module, we can ignore the error
                # attempting to import it, otherwise we want it to bubble up.
                if module_has_submodule(mod, 'resources'):
                    raise
    else:
        def discover(app):
            import imp
            from django.utils.importlib import import_module

            # For each app, we need to look for an admin.py inside that app's
            # package. We can't use os.path here -- recall that modules may be
            # imported different ways (think zip files) -- so we need to get
            # the app's __path__ and look for admin.py on that path.

            # Step 1: find out the app's __path__ Import errors here will (and
            # should) bubble up, but a missing __path__ (which is legal, but weird)
            # fails silently -- apps that do weird things with __path__ might
            # need to roll their own admin registration.
            try:
                app_path = import_module(app).__path__
            except AttributeError:
                return

            # Step 2: use imp.find_module to find the app's admin.py. For some
            # reason imp.find_module raises ImportError if the app can't be found
            # but doesn't actually try to import the module. So skip this app if
            # its admin.py doesn't exist
            try:
                imp.find_module('resources', app_path)
            except ImportError:
                return

            # Step 3: import the app's admin file. If this has errors we want them
            # to bubble up.
            import_module("%s.resources" % app)

    def autodiscover():
        """
        Auto-discover INSTALLED_APPS resources.py modules and fail silently when
        not present. This forces an import on them to register any resource bits
        they may want.

        Copied from django.contrib.admin
        """
        from .settings import SKIP_APPS
        from django.conf import settings

        for app in settings.INSTALLED_APPS:
            if app != 'contentrelations' and app not in SKIP_APPS:
                discover(app)

except ImportError:
    pass
