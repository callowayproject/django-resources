import json

from contentrelations import BaseResource, resource_list
from contentrelations.serializer import Serializer

from .models import Food, Beverage, Person


class ExampleResource(BaseResource):
    def get_title(self):
        return self.instance.name

    def get_short_desc(self):
        return self.instance.description[:10]

resource_list.register((Food, Beverage, Person), ExampleResource)


class SimpleJSONSerializer(Serializer):
    """
    This will serialize resources with name and description attributes
    """

    def start_serialization(self):
        self.stream.write("[")

    def end_serialization(self):
        self.stream.write("]")

    def serialize_object(self, obj):
        out = {'name': obj.name, 'description': obj.description}
        if not self.first:
            self.stream.write(",")
        self.stream.write(json.dumps(out))
