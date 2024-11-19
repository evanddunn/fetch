"""Define Urls for project Fetch"""

from django.urls import include, path

urlpatterns = [
    path("receipts/", include("receipts.urls")), # Include urls in the 'receipts' path of the API
]
