"""
Allows connecting any object to any other object and unifying the interface
between all the objects.
"""
__version_info__ = {
    'major': 1,
    'minor': 3,
    'micro': 5,
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

from .base import resource_list, BaseResource  # NOQA


def autodiscover():
    """
    Auto-discover INSTALLED_APPS resources.py modules and fail silently when
    not present. This forces an import on them to register any resource bits
    they may want.

    Copied from django.contrib.admin
    """
    from .settings import SKIP_APPS
    from .module_loading import autodiscover_modules

    autodiscover_modules('resources', register_to=resource_list, skip_apps=SKIP_APPS)

default_app_config = 'contentrelations.apps.ContentRelationsAppConfig'
