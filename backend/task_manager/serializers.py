from django.core.validators import MinValueValidator
from rest_framework import serializers
from django_celery_results.models import TaskResult


class TasksListSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source="id")
    name = serializers.CharField(source="task_name")
    created_at = serializers.CharField(source="date_created")

    class Meta:
        model = TaskResult
        fields = ['uuid', 'name', 'created_at']


class OptionsSerializer(serializers.Serializer):
    retry = serializers.IntegerField(validators=[MinValueValidator(0)])
    delay = serializers.IntegerField(validators=[MinValueValidator(0)])


class CreateTaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='task_name', max_length=255)
    params = serializers.JSONField(source='task_kwargs', required=False)
    options = OptionsSerializer(source='meta', required=False)

    class Meta:
        model = TaskResult
        fields = ['name', 'params', 'options']
