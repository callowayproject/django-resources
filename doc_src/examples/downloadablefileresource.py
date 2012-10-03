from contentrelations import BaseResource, resource_list
from downloads.models import DownloadableFile

class DownloadableFileResource(BaseResource):
    def get_title(self):
        return self.instance.file_name

    def get_description(self):
        return self.instance.notes

    def get_key_image(self):
        return self.instance.preview_image

    def get_url(self):
        return self.instance.downloadablefile.url


resource_list.register(DownloadableFile, DownloadableFileResource)