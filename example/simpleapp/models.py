from django.db import models
from genericm2m.models import RelatedObjectsDescriptor
from resources.models import RelatedResource


class Food(models.Model):
    name = models.CharField(max_length=255)

    related = RelatedObjectsDescriptor(RelatedResource)

    def __unicode__(self):
        return self.name


class Beverage(models.Model):
    name = models.CharField(max_length=255)

    related = RelatedObjectsDescriptor(RelatedResource)

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=255)

    related = RelatedObjectsDescriptor(RelatedResource)

    def __unicode__(self):
        return self.name
