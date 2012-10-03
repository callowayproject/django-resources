from contentrelations import BaseResource, resource_list
from imageapp.models import Image

class ImageResource(BaseResource):
    def get_title(self):
        return self.instance.name

    def get_description(self):
        return self.instance.caption

    def get_key_image(self):
        return self.instance.image


resource_list.register(Image, ImageResource)