from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from django_celery_results.models import TaskResult
from task_manager.serializers import TasksListSerializer, CreateTaskSerializer


class TaskViewSet(ListAPIView, viewsets.ModelViewSet):
    serializer_class = TasksListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return TasksListSerializer
        elif self.action == "create":
            return CreateTaskSerializer

    def get_queryset(self):
        queryset = TaskResult.objects.all()
        task_name = self.request.query_params.get('name')
        if task_name is not None:
            queryset = queryset.filter(task_name=task_name)
        return queryset

