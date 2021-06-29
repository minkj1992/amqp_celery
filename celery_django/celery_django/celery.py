import os
from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_django.settings')

class CeleryConfig:
    result_backend = 'rpc://'
    broker_url = 'pyamqp://admin:admin@localhost:5672'
    result_serializer = 'json'
    accept_content = ['application/json']
    timezone = settings.TIME_ZONE


class CruxCeleryConfig(CeleryConfig):
    """
    $ docker run -p 5672:5672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin rabbitmq
    """
    
    task_default_queue = 'account.idcardcenter.queue'
    task_default_exchange = 'account.idcardcenter.exchange'
    task_default_exchange_type = "topic"
    task_default_routing_key = "kakaoBusiness.route"

app = Celery('celery_django')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(CruxCeleryConfig)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

