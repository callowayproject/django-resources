from collections import defaultdict

from django.conf import settings

DEFAULT_SETTINGS = {
    'SETUP_RESOURCES': [],
    'JS_PREFIX': '',
    'SKIP_APPS': []
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'CONTENTRELATIONS_SETTINGS', {}))

SETUP_MODELS = defaultdict(list)
if USER_SETTINGS['SETUP_RESOURCES']:
    for item in USER_SETTINGS['SETUP_RESOURCES']:
        bits = item.split('.')
        if len(bits) == 2:
            field_name = 'related'
        else:
            field_name = bits[2]
        SETUP_MODELS['.'.join(bits[:2])].append(field_name)

if USER_SETTINGS['SKIP_APPS'] is None:
    USER_SETTINGS['SKIP_APPS'] = []
elif isinstance(USER_SETTINGS['SKIP_APPS'], basestring):
    USER_SETTINGS['SKIP_APPS'] = [USER_SETTINGS['SKIP_APPS']]

if 'contentrelations' not in USER_SETTINGS['SKIP_APPS']:
    previous = list(USER_SETTINGS['SKIP_APPS'])  # in case of tuple
    previous.append('contentrelations')
    USER_SETTINGS['SKIP_APPS'] = previous[:]

globals().update(USER_SETTINGS)
