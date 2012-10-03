from collections import defaultdict

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.db.models.signals import class_prepared
from django.db.models import get_model

DEFAULT_SETTINGS = {
    'RESOURCE_TYPE_CHOICES': None,
    'IMAGE_STORAGE': settings.DEFAULT_FILE_STORAGE,
    'KEY_IMAGE_MODEL': None,
    'SETUP_RESOURCES': [],
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'SUPPLYCLOSET_SETTINGS', {}))

USER_SETTINGS['IMAGE_STORAGE'] = get_storage_class(USER_SETTINGS['IMAGE_STORAGE'])

SETUP_MODELS = defaultdict(list)
if USER_SETTINGS['SETUP_RESOURCES']:
    for item in USER_SETTINGS['SETUP_RESOURCES']:
        bits = item.split('.')
        if len(bits) == 2:
            field_name = 'related'
        else:
            field_name = bits[2]
        model = get_model(*bits[:2])
        SETUP_MODELS[model].append(field_name)


globals().update(USER_SETTINGS)

# from .registration import handle_prepared_model
# class_prepared.connect(handle_prepared_model)
