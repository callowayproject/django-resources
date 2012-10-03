from contentrelations.serializer import Serializer
import json

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