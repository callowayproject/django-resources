from io import BytesIO

from .base import ResourceIterator


class Serializer(object):
    """
    Abstract class for serializing a sequence of Resources
    """
    def serialize(self, sequence, **options):
        """
        start the serialization process.
        """
        if isinstance(sequence, ResourceIterator):
            self.sequence = sequence
        else:
            self.sequence = ResourceIterator(sequence)
        self.options = options
        self.stream = options.pop("stream", BytesIO())
        self.selected_fields = options.pop("fields", None)

        self.start_serialization()
        self.first = True

        for obj in self.sequence:
            self.start_object(obj)
            if self.selected_fields is None:
                self.serialize_object(obj)
            else:
                for fld in self.selected_fields:
                    self.handle_field(obj, fld)
            self.end_object(obj)
            if self.first:
                self.first = False
        self.end_serialization()
        return self.getvalue()

    def start_serialization():
        """
        Event: We are starting serialization
        """
        pass

    def start_object(self, obj):
        """
        Event: We are starting to serialize this object
        """
        pass

    def serialize_object(self, obj):
        """
        Subclasses must implement this or handle_field. This does most of the work
        """
        raise NotImplementedError

    def handle_field(self, obj, field):
        """
        Subclasses must implement this or serialize_object. This does most of the work
        """
        raise NotImplementedError

    def end_object(self, obj):
        """
        Event: We have finished serializing this object
        """
        pass

    def end_serialization():
        """
        Event: We have finished serialization
        """
        pass

    def getvalue(self):
        """
        Return the fully serialized sequence (or None if the output stream is
        not seekable).
        """
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()
