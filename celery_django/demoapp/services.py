from demoapp.models import Member


def count_agreements():
    return Member.objects.filter(is_member_withdrawn=False).count()
