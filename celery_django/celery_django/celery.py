import os
from typing import TypedDict

from celery import Celery, bootsteps

from django.conf import settings
from kombu import Queue, Consumer, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_django.settings')

account_consumer_queue_name = 'account.consumer.queue'
demo_queue = Queue(
        name='demo_celery',
        exchange=Exchange('demo.exchange', type='direct')
)


class ConsumerOnlyCeleryConfig:
    result_backend = 'rpc://'
    result_serializer = 'json'
    accept_content = ['application/json']
    timezone = settings.TIME_ZONE
    broker_url = 'pyamqp://admin:admin@localhost:5672'
    # consumer로만 활용하는 셀러리는 task_queue를 비우고 ConsumerStep에서 라우팅 처리를 해줘야한다. (wrong destination error)
    task_queues = None


class DemoCeleryConfig:
    result_backend = 'rpc://'
    result_serializer = 'json'
    accept_content = ['application/json']
    broker_url = 'pyamqp://admin:admin@localhost:5671'
    task_queues = (demo_queue,)


demo_app = Celery('demo')
demo_app.config_from_object(DemoCeleryConfig)
demo_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



class AccountEventDto(TypedDict):
    event_type: str
    account_id: str


class AccountConsumeStep(bootsteps.ConsumerStep):
    EVENT_CALLBACK_MAPPER = {
        'ACCOUNT_JOIN': 1,
        'ACCOUNT_WITHDRAWAL': 2
    }
    HANDLING_EVENTS = tuple(EVENT_CALLBACK_MAPPER.keys())

    def get_consumers(self, channel):
        consumer_queue = Queue(name=account_consumer_queue_name,
                               exchange=Exchange(name='account.consumer.exchange',
                                                 type='topic', ),
                               routing_key='account.consumer.route')
        return (Consumer(channel,
                         queues=[consumer_queue, ],
                         callbacks=[self.handle_message],
                         accept=['json'],
                         tag_prefix="consume"),)

    def handle_message(self, body, message):
        account_dto: AccountEventDto = AccountConsumeStep._parse_dsp_account_event(body)
        demo_app.send_task(name='demoapp.tasks.create_member', args=(account_dto['account_id'],), queue='demo_celery')

        # try:
        #     if event_type in AccountConsumeStep.HANDLING_EVENTS:
        #         is_success = AccountConsumeStep.handle_dsp_account_withdrawal(account_dto.account_id)
        #         if is_success:
        #             message.ack()
        #     else:
        #         logger.info("Ignored task")
        #         message.ack()
        # except Exception as err:
        #     logger.error(err)

    @classmethod
    def handle_account_withdrawal(cls, account_id):
        return True

    @classmethod
    def _parse_dsp_account_event(cls, body) -> AccountEventDto:
        return AccountEventDto(account_id='12345', event_type="ACCOUNT_WITHDRAWAL")


account_app = Celery('account')
account_app.config_from_object(ConsumerOnlyCeleryConfig)
account_app.steps['consumer'].add(AccountConsumeStep)
