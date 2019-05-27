from django.urls import path

from acm_placement_app.placements.views import PlacementRequestWizard, RunView

app_name = 'placements'

urlpatterns = [
    path("request/", PlacementRequestWizard.as_view(), name='request-placements'),
    path("run/<int:id>", RunView.as_view(), name='run'),
]
