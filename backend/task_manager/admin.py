from django.contrib import admin
from django_celery_results.admin import TaskResultAdmin
from django_celery_results.models import TaskResult

from backend.celery import app


@admin.action(description='Cancel selected tasks')
def cancel_tasks(modeladmin, request, queryset):
    tasks_id_to_cancel = list(queryset.values_list("task_id", flat=True))
    app.control.revoke(tasks_id_to_cancel, terminate=True)


class ArticleAdmin(TaskResultAdmin):
    actions = [cancel_tasks]


admin.site.unregister(TaskResult)
admin.site.register(TaskResult, ArticleAdmin)
