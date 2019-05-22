from django.urls import path

from acm_placement_app.placements.views import PlacementsRequestWizard

app_name = 'placements'

urlpatterns = [
    path("request/", PlacementsRequestWizard.as_view(), name='request-placements'),
]
