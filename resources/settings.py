from django.conf import settings
from django.core.files.storage import get_storage_class
DEFAULT_SETTINGS = {
    'RESOURCE_TYPE_CHOICES': None,
    'IMAGE_STORAGE': settings.DEFAULT_FILE_STORAGE,
    'KEY_IMAGE_MODEL': None,
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'RESOURCES_SETTINGS', {}))

USER_SETTINGS['IMAGE_STORAGE'] = get_storage_class(USER_SETTINGS['IMAGE_STORAGE'])

globals().update(USER_SETTINGS)
