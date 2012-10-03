from django.db import models
from contentrelations.related import RelatedObjectsDescriptor


class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    related = RelatedObjectsDescriptor()

    def __unicode__(self):
        return self.name


class Beverage(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    # related = RelatedObjectsDescriptor()

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    # related = RelatedObjectsDescriptor()

    def __unicode__(self):
        return self.name


class KeyImageShim(models.Model):
    image_file = models.FileField(upload_to='keyimageshim')

    def __unicode__(self):
        return self.image_file
