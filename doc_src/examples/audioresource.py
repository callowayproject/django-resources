import contentrelations
from .models import AudioModel

class AudioResource(contentrelations.BaseResource):
    def get_resource_type(self):
        return "Audio & Video"

    def get_title(self):
        return self.model.name

    def get_description(self):
        return self.model.summary

    def get_key_image(self):
        return self.model.image

    def get_url(self):
        return self.model.audio_file.url

contentrelations.resource_list.register(AudioModel, AudioResource)