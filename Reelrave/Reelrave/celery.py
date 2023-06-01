import os
from datetime import timedelta
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Reelrave.settings')
app = Celery('Reelrave')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_expired_records': {
        'task': 'ReelRave.tasks.delete_expired_records',
        'schedule': timedelta(hours=1),
    },
}