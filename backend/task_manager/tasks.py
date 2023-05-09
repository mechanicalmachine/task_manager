from backend.celery import app


@app.task(bind=True, autoretry_for=(Exception,))
def fake_task(self, param1=None, param2=None, retry=30, delay=10):
    try:
        1 / 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=delay, max_retries=retry)
