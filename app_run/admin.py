from django.contrib import admin
from app_run.models import Run, AthleteInfo, Position, Challenge, CollectibleItem

admin.site.register(AthleteInfo)
admin.site.register(Position)
admin.site.register(Challenge)
admin.site.register(CollectibleItem)

@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'comment', 'status', 'created_at')
