from django.contrib import admin
from .models import Location, Event

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ['name']

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    fieldsets = [
        ('Event Details', {'fields': ['location', 'creator', 'voters', 'note']})
    ]
    list_display = ('location', 'created_date', 'creator', 'get_voters')
    list_filter = ['created_date']

admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)