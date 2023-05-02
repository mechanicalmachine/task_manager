from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from django_celery_results.models import TaskResult
from rest_framework.viewsets import GenericViewSet

from task_manager.serializers import TasksListSerializer, CreateTaskSerializer, TaskRetrieveSerializer


class TaskViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    lookup_field = "task_id"
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return TasksListSerializer
        elif self.action == "create":
            return CreateTaskSerializer
        elif self.action == "retrieve":
            return TaskRetrieveSerializer

    def get_queryset(self):
        queryset = TaskResult.objects.all()
        task_name = self.request.query_params.get('name')
        if task_name is not None:
            queryset = queryset.filter(task_name=task_name)
        return queryset

