import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.conf.update(
    accept_content=["json"],
    result_serializer="json",
    send_events=False,
    task_serializer="json",
    task_acks_late=True,
    task_default_queue="celery",
    task_default_exchange="celery",
    task_default_routing_key="celery",
    task_create_missing_queues=False,
    broker_heartbeat=10,
    broker_connection_max_retries=10,
    broker_heartbeat_checkrate=2,
    broker_transport_options={"confirm_publish": True, "connect_timeout": 10, "read_timeout": 30, "write_timeout": 30},
    worker_max_tasks_per_child=300,
    worker_prefetch_multiplier=1,
    worker_direct=False,  # create queue for each worker
    worker_hijack_root_logger=False,
    result_expires=3600,
    result_extended=True,
)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
