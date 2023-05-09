from django.urls import re_path

from task_manager.views import TaskViewSet

app_name = "task"
urlpatterns = [
    re_path(r"^tasks/?$", TaskViewSet.as_view({"get": "list", "post": "create"})),
    re_path(r"^tasks/(?P<task_id>[0-9a-f-]{32,36})/?$", TaskViewSet.as_view({"get": "retrieve"})),
    re_path(r"^tasks/(?P<task_id>[0-9a-f-]{32,36})/cancel/?$", TaskViewSet.as_view({"post": "destroy"})),
]
