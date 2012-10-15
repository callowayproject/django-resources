# from django.db.models.loading import get_model
# from contentrelations.settings import SETUP_MODELS
# from contentrelations.registration import monkey_patch


# for model_str, fields in SETUP_MODELS.items():
#     model = get_model(*model_str.split('.'))
#     if model is None:
#         print "Can't load model: %s" % model_str
#         continue
#     for field in fields:
#         monkey_patch(model, field)
