from django.urls import path

from acm_placement_app.placements.views import PlacementsRequestWizard, RunView

app_name = 'placements'

urlpatterns = [
    path("request/", PlacementsRequestWizard.as_view(), name='request-placements'),
    path("run/<int:id>", RunView.as_view(), name='run'),
]
