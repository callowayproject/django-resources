from .related import RelatedObjectsDescriptor
from .settings import SETUP_MODELS


def monkey_patch(model_class, name='related', descriptor=None):
    if getattr(model_class, name, False):
        print "%s already has an attribute named %s" % (model_class.__name__, name)
        return False
    rel_obj = descriptor or RelatedObjectsDescriptor()
    rel_obj.contribute_to_class(model_class, name)
    setattr(model_class, name, rel_obj)
    return True


def handle_prepared_model(sender, *args, **kwargs):
    """
    Listens to django.db.models.signals.class_prepared and checks to see if the
    class is configured to insert related models
    """
    if sender not in SETUP_MODELS.keys():
        return
    for model, fields in SETUP_MODELS.items():
        for field in fields:
            monkey_patch(model, field)
