from celery import Celery

from app.config import settings

celery_app = Celery(
    "worldcup_scout",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.autodiscover_tasks(["app.tasks"])
