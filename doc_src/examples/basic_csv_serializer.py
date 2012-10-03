from contentrelations.serializer import Serializer
import csv

class SimpleCSVSerializer(Serializer):
    """
    This will serialize resources with name and description attributes
    """

    def serialize_object(self, obj):
        csv_writer = csv.writer(self.stream)
        csv_writer.writerow([obj.name, obj.description])