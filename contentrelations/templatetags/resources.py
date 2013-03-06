# This tag only work in Django 1.4+

from django import template

register = template.Library()


@register.assignment_tag
def get_resource(item):
    """
    Given a model object, return either the Resource registered to handle that
    item, or the item itself.
    """
    from contentrelations.base import resource_list
    resource = resource_list.get_for_instance(item)
    if resource is None:
        return item
    return resource
