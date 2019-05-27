from django.contrib import admin

from acm_placement_app.placements.models import PlacementRequest


@admin.register(PlacementRequest)
class PlacementRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'requested_by', 'created', 'is_completed',)
