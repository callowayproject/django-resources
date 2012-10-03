from django.contrib import admin

from .models import Food, Beverage, Person

from contentrelations.admin import RelatedInline


class SimpleAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    inlines = [RelatedInline]

admin.site.register((Food, Beverage, Person), SimpleAdmin)
