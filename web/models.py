from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Note(models.Model):
    title = models.CharField(max_length=500)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    alert_send_at = models.DateTimeField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
