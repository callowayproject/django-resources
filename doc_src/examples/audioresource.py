import resources
from .models import AudioModel

class AudioResource(resources.BaseResource):
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

    # def get_credit(self):
    #     pass

    # def get_citation(self):
    #     pass

    # def get_notes(self):
    #     pass

    # def get_internal_ref(self):
    #     pass

resources.resource_list.register(AudioModel, AudioResource)