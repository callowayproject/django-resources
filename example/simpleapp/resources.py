from supplycloset import BaseResource, resource_list
from .models import Food, Beverage, Person


class ExampleResource(BaseResource):
    def get_title(self):
        return self.instance.name

    def get_short_desc(self):
        return self.instance.description[:10]

resource_list.register((Food, Beverage, Person), ExampleResource)
