from django.urls import path
from .views import OperationView

urlpatterns = [
    path("operation/", OperationView.as_view(), name="operation"),
]
