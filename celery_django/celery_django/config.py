import os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_django.settings')

result_backend = 'rpc://'
result_serializer = 'json'
accept_content = ['application/json']
task_always_eager = False
task_acks_late = True
worker_prefetch_multiplier = 1
broker_url = settings.CRUX_BILLING_RABBITMQ_URL
task_queues = None