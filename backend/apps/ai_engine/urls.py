from django.urls import path
from .views import AnalyzeLogsView, AnalysisStatusView, SemanticSearchView

urlpatterns = [
    path("analyze/<uuid:log_file_id>/", AnalyzeLogsView.as_view(), name="analyze-logs"),
    path("analyze/<uuid:log_file_id>/status/", AnalysisStatusView.as_view(), name="analysis-status"),
    path("search/<uuid:log_file_id>/", SemanticSearchView.as_view(), name="semantic-search"),
]