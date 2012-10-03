from .related import RelatedResource

from contentrelations import autodiscover
autodiscover()

from contentrelations.settings import SETUP_MODELS
from contentrelations.registration import monkey_patch
for model, fields in SETUP_MODELS.items():
    for field in fields:
        monkey_patch(model, field)
