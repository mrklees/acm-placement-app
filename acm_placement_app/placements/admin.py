from django.contrib import admin

from acm_placement_app.placements.models import PlacementRequest, PlacementResult


@admin.register(PlacementRequest)
class PlacementRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'requested_by', 'created', 'is_completed',)


@admin.register(PlacementResult)
class PlacementResultAdmin(admin.ModelAdmin):
    list_display = ('placementrequest', 'created',)
