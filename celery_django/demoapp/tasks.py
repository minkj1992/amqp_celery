# Create your tasks here

from celery import shared_task
from demoapp.models import Member

@shared_task(ignore_result=True)
def create_member(account_id: int):
    print("hereeeeeee")
    Member.objects.create(account_id=account_id)


@shared_task
def rejoin_member(member_id):
    m = Member.objects.get(id=member_id)
    m.is_member_withdrawn = False
    m.save()


@shared_task
def withdrawn_member(member_id):
    m = Member.objects.get(id=member_id)
    m.is_member_withdrawn = True
    m.save()
