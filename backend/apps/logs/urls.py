from django.urls import path
from .views import LogUploadView

urlpatterns = [
    path("upload/", LogUploadView.as_view(), name="log-upload"),
]