from django.urls import re_path

from task_manager.views import TaskVieSet

app_name = "task"
urlpatterns = [
    re_path(r"^task/?$", TaskVieSet.as_view({"post": "create"})),
]
