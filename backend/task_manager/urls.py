from django.urls import re_path

from task_manager.views import TaskViewSet

app_name = "task"
urlpatterns = [
    re_path(r"^task/?$", TaskViewSet.as_view({"post": "create"})),
    re_path(r"^task/?$", TaskViewSet.as_view({"get": "list"})),
]
