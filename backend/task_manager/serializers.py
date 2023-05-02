from rest_framework import serializers
from django_celery_results.models import TaskResult


class TasksListSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source="id")
    name = serializers.CharField(source="task_name")
    created_at = serializers.CharField(source="date_created")

    class Meta:
        model = TaskResult
        fields = ['uuid', 'name', 'created_at']
