
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import resolve_url


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=5)
    website_url = models.URLField(blank=True)
    hint1 = models.TextField(blank=True)
    hint2 = models.TextField(blank=True)
    nickname = models.CharField(max_length=20)
    avatar = models.ImageField(
        blank=True,
        upload_to="accounts/avatar/%Y/%m/%d",
        help_text="48px * 48px 크기의 png/jpg 파일을 업로드해주세요.",
    )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)

