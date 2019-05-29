from django.urls import path

from acm_placement_app.placements.views import PlacementRequestWizard, RunView, PlacementRequestList, \
    PlacementRequestDetail, download_results

app_name = 'placements'

urlpatterns = [
    path("request/", PlacementRequestWizard.as_view(), name='request-placements'),
    path("run/<int:id>/", RunView.as_view(), name='run'),
    path("list/", PlacementRequestList.as_view(), name='placementrequest-list'),
    path("<int:pk>/", PlacementRequestDetail.as_view(), name='placementrequest-details'),
    path("<int:pk>/download-results", download_results, name='placementrequest-download-results'),
]
