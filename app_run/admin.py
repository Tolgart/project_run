from django.contrib import admin
from app_run.models import Run, AthleteInfo, Position, Challenge

admin.site.register(AthleteInfo)
admin.site.register(Position)
admin.site.register(Challenge)

@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'comment', 'status', 'created_at')
