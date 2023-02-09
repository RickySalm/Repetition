from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(BaseModels):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)


class Note(BaseModels):
    title = models.CharField(max_length=500)
    text = models.TextField()

    alert_send_at = models.DateTimeField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
