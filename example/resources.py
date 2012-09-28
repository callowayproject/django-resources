from resources import BaseResource, resource_list
from .models import Food, Beverage, Person


class ExampleResource(BaseResource):
    def get_title(self):
        return self.name

resource_list.register((Food, Beverage, Person), BaseResource)