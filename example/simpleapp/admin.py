from django.contrib import admin

from .models import Food, Beverage, Person

from contentrelations.admin import RelatedInline

class AlternateInline(RelatedInline):
    rel_name = 'resources'
    verbose_name_plural = "Resource Carousel"
    exclude = ('source_type', 'source_id', 'relation_type')

class SimpleAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    inlines = [RelatedInline]

class AnotherAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    inlines = [AlternateInline]

admin.site.register((Food, Beverage), SimpleAdmin)
admin.site.register(Person, AnotherAdmin)
