=====================
Serializing Resources
=====================

Many times resources are used in another context, such as an Adobe Flash application. Serialization is the process of converting a set of resources into another format such as XML or JSON. Supply Closet's serialization framework provides a mechanism for "translating" ``Resource``\ s into other formats. Usually these other formats will be text-based and used for sending ``Resource``\ s over a wire, but it'’'s possible for a serializer to handle any format (text-based or not).

Supply Closet's serializization framework is closely based on `Django's serialization framework`_. But there is one fundamental difference. Since the nature of a ``Resource`` is flexible, there is no way to determine the fields or attributes of a ``Resource``. Therefore it is difficult to write a completely generic serializer for a given format.

.. _Django's serialization framework: https://docs.djangoproject.com/en/1.4/topics/serialization/#serializing-django-objects

How to serialize a list of resources
====================================

#. Load your serializer (see :ref:`writing_a_serializer`)
#. Instantiate your serializer
#. Call its :py:meth:`Serializer.serialize()` method with your list of objects. These objects should have a ``Resource`` class registered.

It could look like this::

    >>> from myresources.resources import MySerializer
    >>> myserializer = MySerializer()
    >>> output = myserializer.serialize(object_list)


In this example, ``object_list`` is simply an iterable of Django ``Model`` instances with registered ``Resource``\ s. Internally the serializer wraps the ``object_list`` in a :py:class:`ResourceIterator`

.. _writing_a_serializer:

Writing a serializer
====================

Your serializer should subclass :py:class:`Serializer`. Creating a functioning serializer requires only implementing one of two methods: either :py:meth:`Serializer.serialize_object` or :py:meth:`Serializer.handle_field`\ . You can only use ``handle_field`` if you pass a ``selected_fields`` parameter to the :py:meth:`Serializer.serialize` method.

Basic serialization
-------------------

Here is a very simplistic CSV serializer for a ``Resource``:

.. literalinclude:: examples/basic_csv_serializer.py

This only implements the ``serialize_object`` method. For more complex formats, you will probably need to do more.

Advanced serialization
----------------------

The :py:class:`Serializer` object has several event methods that you can use to help with the out put.

* **start serialization()** Called at the start of the process
* **end serialization()** Called at the end of the process
* **start object(obj)** Called before serializing of the passed object
* **end object(obj)** Called after serializing of the passed object

Here is an example of a very simple JSON serializer:

.. literalinclude:: examples/basic_json_serializer.py

This serializer uses the ``start_serialization`` and ``end_serialization`` methods to add the enclosing brackets ``[]`` around the objects.
