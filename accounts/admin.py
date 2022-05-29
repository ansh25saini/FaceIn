from django.contrib import admin
from .models import Time, Present

# Register your models here.
class TimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'time','out')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'date', 'out')

admin.site.register(Time, TimeAdmin)


class PresentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'present')
    list_display_links = ('id', 'user',)
    search_fields = ('user', 'date', 'present')

admin.site.register(Present, PresentAdmin)

