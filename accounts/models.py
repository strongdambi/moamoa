from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    parents = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                                help_text='부모님 기본 0 | 아이들은 부모님 번호')
    birthday = models.DateField(null=True, blank=True, help_text='생년월일')
    images = models.TextField(blank=True, null=True, help_text='프로필 이미지')
