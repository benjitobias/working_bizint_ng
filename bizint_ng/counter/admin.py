from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from django.utils.html import format_html

from .models import Action, Count, Location


class CountInline(admin.TabularInline):
    fields = ['action', 'count', 'update_date', 'note', 'longitude', 'latitude']
    model = Count
    extra = 0
    max_num = 3


# class ActionAdmin(admin.ModelAdmin):
class ActionAdmin(GuardedModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['owner']}),
        ('Date information', {'fields': ['creation_date']}),
    ]
    inlines = [CountInline]
    list_display = ('name', 'creation_date', 'get_count', 'latest_date', 'owner')

    def get_count(self, obj):
        return obj.get_count()

    get_count.short_description = "Count"

    def latest_date(self, obj):
        try:
            latest_date = obj.get_latest().update_date
        except AttributeError:
            latest_date = None
        return latest_date

    def get_note(self, obj):
        return "Note"


class LocationAdmin(GuardedModelAdmin):
    list_display = ['name', 'owner', 'get_coordinates_with_link']

    def get_coordinates_with_link(self, location):
        return format_html("<a  href='{link}'>{coordinates}</a>", link=location.link, coordinates=location.coordinates)

    get_coordinates_with_link.short_description = 'Coordinates'

admin.site.register(Action, ActionAdmin)
admin.site.register(Location, LocationAdmin)
