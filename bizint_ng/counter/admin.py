from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Action, Count


class CountInline(admin.TabularInline):
    fields = ['action', 'count', 'update_date']
    model = Count
    extra = 0


# class ActionAdmin(admin.ModelAdmin):
class ActionAdmin(GuardedModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date information', {'fields': ['creation_date']}),
    ]
    inlines = [CountInline]
    list_display = ('name', 'creation_date', 'get_count', 'latest_date')

    def get_count(self, obj):
        return obj.get_count()

    get_count.short_description = "Count"

    def latest_date(self, obj):
        try:
            latest_date = obj.get_latest().update_date
        except AttributeError:
            latest_date = None
        return latest_date


admin.site.register(Action, ActionAdmin)
