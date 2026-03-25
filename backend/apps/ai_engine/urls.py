from django.urls import path
from .views import AnalyzeLogsView

urlpatterns = [
    path("analyze/<uuid:log_file_id>/", AnalyzeLogsView.as_view(), name="analyze-logs"),
]