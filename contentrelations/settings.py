from collections import defaultdict

from django.conf import settings
from django.db.models import get_model

DEFAULT_SETTINGS = {
    'SETUP_RESOURCES': [],
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'SUPPLYCLOSET_SETTINGS', {}))

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
