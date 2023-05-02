from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from django_celery_results.models import TaskResult
from task_manager.serializers import TasksListSerializer


class TaskViewSet(ListAPIView, viewsets.ModelViewSet):
    serializer_class = TasksListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TaskResult.objects.all()
        task_name = self.request.query_params.get('name')
        if task_name is not None:
            queryset = queryset.filter(task_name=task_name)
        return queryset

