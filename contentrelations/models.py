from .related import RelatedResource

from supplycloset import autodiscover
autodiscover()

from supplycloset.settings import SETUP_MODELS
from supplycloset.registration import monkey_patch
for model, fields in SETUP_MODELS.items():
    for field in fields:
        monkey_patch(model, field)
