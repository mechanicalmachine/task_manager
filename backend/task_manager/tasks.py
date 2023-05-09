import time

from backend.celery import app


@app.task(bind=True, autoretry_for=(Exception,))
def task_one(self, param1=None, param2=None, retry=5, delay=30):
    try:
        1 / 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=delay, max_retries=retry)


@app.task
def task_two(*args, **kwargs):
    time.sleep(100)
