from celery import signature
from guardian.shortcuts import get_objects_for_user, assign_perm
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import DjangoObjectPermissions

from django_celery_results.models import TaskResult
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from backend.celery import app
from task_manager.serializers import TasksListSerializer, CreateTaskSerializer, TaskRetrieveSerializer


class TaskViewSet(DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    lookup_field = "task_id"
    permission_classes = [DjangoObjectPermissions]

    def get_serializer_class(self):
        if self.action == "list":
            return TasksListSerializer
        elif self.action == "create":
            return CreateTaskSerializer
        elif self.action == "retrieve":
            return TaskRetrieveSerializer

    def get_queryset(self):
        queryset = get_objects_for_user(self.request.user, 'view_object', klass=TaskResult)
        task_name = self.request.query_params.get('name')
        if task_name is not None:
            queryset = queryset.filter(task_name=task_name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"task_id": instance.task_id}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        data = serializer.data
        task_signature = signature(data.pop("name"))
        result = task_signature.apply_async(**data)
        instance = TaskResult.objects.store_result(
            'application/json', 'utf-8', result.id, result, result.status, task_name=serializer.data["name"]
        )
        assign_perm("view_taskresult", self.request.user, instance)
        assign_perm("delete_taskresult", self.request.user, instance)
        return instance

    def perform_destroy(self, instance):
        app.control.revoke(instance.task_id, terminate=True)
