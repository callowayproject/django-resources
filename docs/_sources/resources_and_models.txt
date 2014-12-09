=================================
Linking Resources to other models
=================================

.. contents::
   :local:

Overview
========

Having a unified interface for different models is wonderful, but how do we make these relationships of ``Resource``\ s?

Borrowing some chops from Charles Leifer's django-genericm2m_, Django Supply Closet provides helpful utilities.

#. All querying and connecting logic is in a single attribute that acts on both model instances and the model class
#. Any model to be used as the intermediary "through" model and a default model is already available
#. Uses an optimized lookup for ``GenericForeignKeys``
#. Provides a ``InlineModelAdmin`` class for use in the Django admin
#. You can dynamically set up the relationship in your ``settings.py``

.. _django-genericm2m: https://github.com/coleifer/django-generic-m2m

Adding to a model
=================

Before you start creating relationships, you'll need to add a ``RelatedObjectsDescriptor``
to any model you plan on relating to other models.

Here's a quick example:

.. code-block:: python

    from django.db import models

    from contentrelations.related import RelatedObjectsDescriptor


    class Food(models.Model):
        name = models.CharField(max_length=255)

        related = RelatedObjectsDescriptor()

        def __unicode__(self):
            return self.name


    class Beverage(models.Model):
        name = models.CharField(max_length=255)

        related = RelatedObjectsDescriptor()

        def __unicode__(self):
            return self.name


If you'd like to add relationships to a model that you don't control (for example
the ``User`` model from ``django.contrib.auth``), you can use the :ref:`setup_resources_setting`
setting:

.. code-block:: python

    SUPPLYCLOSET_SETTINGS = {
        'SETUP_RESOURCES': ['auth.User.related']
    }


What is the RelatedResource class?
==================================

The "related" attribute from the previous examples is the way the generic many-to-many
is exposed for each model. Behind-the-scenes it is using :py:class:`RelatedResource`.


There's not really too much that should be weird about this model. It contains
two ``GenericForeignKeys``, one to represent the "from" object, the source of the
connection, and another to represent to "to" object (what "from" is being connected
with).


Creating relationships
======================

A custom model manager is exposed on each model via the ``RelatedObjectsDescriptor``.
The API for creating and querying relationships is exposed via this descriptor.

Here is a sample interactive terminal session::

    >>> # create a handful of objects to use in our demo
    >>> pizza = Food.objects.create(name='pizza')
    >>> cereal = Food.objects.create(name='cereal')
    >>> beer = Beverage.objects.create(name='beer')
    >>> soda = Beverage.objects.create(name='soda')
    >>> milk = Beverage.objects.create(name='milk')
    >>> healthy_eater = User.objects.create_user('healthy_eater', 'healthy@health.com', 'secret')
    >>> chocula = User.objects.create_user('chocula', 'chocula@postcereal.com', 'garlic')

Now that we have some Food, Beverage and User objects, create some connections between them::

    >>> rel_obj = pizza.related.connect(beer, relation_type='goes well with')
    >>> type(rel_obj) # what did we just create?
    <class 'contentrelations.related.RelatedResource'>

The object that represents the connection is an instance of whatever is passed to the :py:class:`RelatedObjectDescriptor` when it is added to a model. The default is :py:class:`RelatedResource`. Here are the interesting properties of the new related object::

    >>> rel_obj.source
    <Food: pizza>
    >>> rel_obj.object
    <Beverage: beer>
    >>> rel_obj.relation_type
    'goes well with'


Querying relationships
======================

These relationships can be queried::

    >>> pizza.related.all() # find all objects that pizza has been related to
    [<RelatedResource: pizza related to beer (goes well with)>]


Retrieving the objects instead of the RelatedResource objects
-------------------------------------------------------------

When the relationship is defined with a :py:class:`GenericForeignKey`, as is the case here, the :py:class`RelatedObjectsDescriptor` (here defined as ``related``) will return a special Django :py:class:`QuerySet` class that provides an optimized lookup of any ``GenericForeignKey``-ed objects::

    >>> type(pizza.related.all())
    <class 'contentrelations.generic.GFKOptimizedQuerySet'>
    >>> pizza.related.all().generic_objects() # traverse the GFK relationships
    [<Beverage: beer>]

If the object on the back-side of the relationship also has a ``RelatedObjectsDescriptor`` with the same intermediary model, reverse lookups are possible:

    >>> beer.related.related_to() # query the back-side of the relationship
    [<RelatedResource: pizza related to beer (goes well with)>]

Create some more connections - any combination of models can be used. Below I'm
connectiong a Food (cereal) to both Beverage objects (milk) and User objects (Chocula)::

    >>> cereal.related.connect(milk) # connecting to a beverage
    <RelatedResource: cereal related to milk>
    >>> cereal.related.connect(chocula) # connecting to a user
    <RelatedResource: cereal related to chocula>

    >>> cereal.related.all() # show what cereal is related to
    [<RelatedResource: cereal related to chocula>,
     <RelatedResource: cereal related to milk>]

    >>> chocula.related.all() # relationships are ONE WAY
    []
    >>> chocula.related.related_to() # querying the backside shows what has been connected to chocula
    [<RelatedResource: cereal related to chocula ("")>]

Querying all relations to a Model
---------------------------------

Also worth noting is that the :py:class:`RelatedObjectsDescriptor` works on both the instance-level (``pizza``) and the class-level (``Food``), so if we wanted to see all objects related to foods::

    >>> Food.related.all() # anything that has been related to a food
    [<RelatedResource: cereal related to chocula>,
     <RelatedResource: cereal related to milk>,
     <RelatedResource: pizza related to beer (goes well with)>]


Using a custom "through" model
==============================

It's possible to use a custom "through" model in place of the default :py:class:`RelatedResource`. If you know you're only going to be using a couple models, this can be a handy way to save queries. Here's another silly example where we
have a ``RelatedBeverage`` model that our Food model will use:

.. code-block:: python

    class RelatedBeverage(models.Model):
        food = models.ForeignKey('Food')
        beverage = models.ForeignKey('Beverage')

        class Meta:
            ordering = ('-id',)

    class Food(models.Model):
        # ... same as above except for this new attribute:
        related_beverages = RelatedObjectsDescriptor(RelatedBeverage, 'food', 'beverage')

The "``related_beverages``" attribute is an instance of :py:class:`RelatedObjectsDescriptor`, but it is instantiated with a couple of arguments:

* ``RelatedBeverage``: the model to be used to hold the "connections"
* ``food``: the field name on the above model which maps to the "from" object
* ``beverage``: the field name which maps to the "to" object

Continuing the shell session from above with the same models, foods can be
connected to beverages using the new "related_beverages" attribute::

    >>> pizza.related_beverages.connect(soda)
    <RelatedBeverage: RelatedBeverage object>

Querying provides the same interface, but since the "to" object is a direct
``ForeignKey`` to Beverage, a normal Django :py:class:`QuerySet` is used::

    >>> pizza.related_beverages.all()
    [<RelatedBeverage: RelatedBeverage object>]
    >>> type(pizza.related_beverages.all())
    <class 'django.db.models.query.QuerySet'>

A ``TypeError`` will be raised if you try to connect an invalid object, such as
a Person to the "related_beverages"::

    >>> pizza.related_beverages.connect(mario)
    *** TypeError: Unable to query ...

And lastly, just like before, its possible to query on the class to get all the
``RelatedBeverage`` objects for our foods::

    >>> Food.related_beverages.all()
    [<RelatedBeverage: RelatedBeverage object>]

Adding to the admin
===================

Add :py:class:`RelatedInline` to your inlines:

.. code-block:: python

    from contentrelations.admin import RelatedInline

    class SimpleAdmin(admin.ModelAdmin):
        list_display = ('name', )
        search_fields = ('name',)
        inlines = [RelatedInline]

If you changed the name from the default ``related``, you need to give the inline a bit of help so it can find the name of the related field.

.. code-block:: python

    from contentrelations.admin import RelatedInline

        class AlternateInline(RelatedInline):
            rel_name = 'resources'

        class AnotherAdmin(admin.ModelAdmin):
            list_display = ('name', )
            search_fields = ('name',)
            inlines = [AlternateInline]

To change the name of the inline fieldset:

.. code-block:: python

    from contentrelations.admin import RelatedInline

        class AlternateInline(RelatedInline):
            verbose_name_plural = "Resource Carousel"

        class AnotherAdmin(admin.ModelAdmin):
            list_display = ('name', )
            search_fields = ('name',)
            inlines = [AlternateInline]

To exclude either the ``relation_type`` or ``order`` field you have to include the excluded fields in the parent class:

.. code-block:: python

    from contentrelations.admin import RelatedInline

        class AlternateInline(RelatedInline):
            exclude = ('source_type', 'source_id', 'relation_type')

        class AnotherAdmin(admin.ModelAdmin):
            list_display = ('name', )
            search_fields = ('name',)
            inlines = [AlternateInline]
