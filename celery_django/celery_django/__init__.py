# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import demo_app, account_app

__all__ = ('demo_app', 'account_app')
