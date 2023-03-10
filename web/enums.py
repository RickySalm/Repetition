from django.db import models


class Role(models.TextChoices):
    admin = 'admin', 'Администратор'
    user = 'user', 'Пользователь'
    staff = 'staff', 'Сотрудник'
