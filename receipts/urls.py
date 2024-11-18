from django.urls import path

from .views import ProcessReceiptView, GetPointsView

urlpatterns = [
    path("process", ProcessReceiptView.as_view(), name="process"),
    path("<str:receipt_id>/points", GetPointsView.as_view(), name="points"),
]
