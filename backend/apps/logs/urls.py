from django.urls import path
from .views import LogUploadView, LogFileStatusView

urlpatterns = [
    path("upload/", LogUploadView.as_view(), name="log-upload"),
    path("<uuid:log_file_id>/status/", LogFileStatusView.as_view(), name="log-status"),
]