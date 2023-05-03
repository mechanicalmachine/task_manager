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


class TaskRetrieveSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source="task_id")
    status = serializers.SerializerMethodField()

    class Meta:
        model = TaskResult
        fields = ['uuid', 'status', "result", "traceback", "date_done"]

    def get_status(self, obj: TaskResult) -> str:
        status_mapping = {
            "PENDING": "PENDING",
            "RECEIVED": "PENDING",
            "STARTED": "IN_PROGRESS",
            "SUCCESS": "COMPLETED",
            "FAILURE": "FAILED",
            "RETRY": "RETRY_PENDING",
            "REVOKED": "CANCELLED"
        }
        return status_mapping.get(obj.status)

    def to_representation(self, instance: TaskResult):
        data = super().to_representation(instance)

        if instance.status in ("PENDING", "RECEIVED", "STARTED"):
            data.pop("date_done")
        if instance.status != "SUCCESS":
            data.pop("result")
        if instance.status not in ("FAILURE", "RETRY"):
            data.pop("traceback")

        return data


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
