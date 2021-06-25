from django.db import models


class Member(models.Model):
    is_member_withdrawn = models.BooleanField('is_member_withdrawn', help_text="동의한 멤버 탈퇴 여부", default=False)
