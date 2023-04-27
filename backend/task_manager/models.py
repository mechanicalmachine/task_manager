import uuid

from django.db import models


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
        COMPLETED = "COMPLETED", "COMPLETED"
        FAILED = "FAILED", "FAILED"
        RETRY_PENDING = "RETRY_PENDING", "RETRY_PENDING"
        CANCELLED = "CANCELLED", "CANCELLED"

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id"
    )
    created_at = models.DateTimeField(verbose_name="Created", auto_now_add=True, editable=False)
    name = models.CharField(max_length=255, verbose_name="Name")
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING,
        verbose_name="Status",
    )
