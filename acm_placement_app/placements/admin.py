from django.contrib import admin

from acm_placement_app.placements.models import PlacementsRequest


@admin.register(PlacementsRequest)
class PlacementsRequestAdmin(admin.ModelAdmin):
    pass
