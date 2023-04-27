from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from task_manager.models import Task
from task_manager.serializers import TaskSerializer


class TaskVieSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
