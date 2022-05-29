from django.contrib import admin
from .models import Review
from .models import Feature
from .models import Customer
from django.utils.html import format_html

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))
        
    thumbnail.short_description = 'Photo'

    list_display = ('id', 'thumbnail', 'first_name', 'designation', 'created_date')
    list_display_links = ('id', 'thumbnail', 'first_name',)
    search_fields = ('first_name', 'last_name', 'designation')

admin.site.register(Review, ReviewAdmin)

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_date',)
    list_display_links = ('id','name',)
    search_fields = ('name', 'id',)

admin.site.register(Feature, FeatureAdmin)

class CustomerAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))

    thumbnail.short_description = 'Photo'

    list_display = ('id', 'thumbnail', 'name', 'created_date')
    list_display_links = ('id', 'thumbnail', 'name')
    search_fields = ('name', 'id')

admin.site.register(Customer, CustomerAdmin)