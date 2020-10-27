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
    list_display = ('name', 'creation_date', 'get_count', 'get_latest')

#admin.site.register(Action)
#admin.site.register(Count)
admin.site.register(Action, ActionAdmin)
