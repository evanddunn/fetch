"""Define Urls for app Receipts"""

from django.urls import path

from .views import GetPointsView, ProcessReceiptView

urlpatterns = [
    path("process", ProcessReceiptView.as_view(), name="process"),  # API endpoint to process receipt
    path("<str:receipt_id>/points", GetPointsView.as_view(), name="points"),  # API endpoint to calculate receipt points
]
