from contentrelations import BaseResource, resource_list
from articleapp.models import Article

class ArticleResource(BaseResource):
    def get_title(self):
        return self.instance.headline

    def get_description(self):
        return self.instance.summary

    def get_key_image(self):
        return self.instance.primary_image

    def get_resource_name(self):
        return u'%s Article' % self.instance.primary_category

resource_list.register(Article, ArticleResource)