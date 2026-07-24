from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy


class Status(models.Model):
    name = models.CharField(gettext_lazy('Name'), max_length=100, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(gettext_lazy('Name'), max_length=100, unique=True)
    description = models.TextField(gettext_lazy('Description'), null=True, blank=True)
    status = models.ForeignKey(
        Status, verbose_name=gettext_lazy('Status'), on_delete=models.PROTECT
    )
    assignee = models.ForeignKey(
        User,
        verbose_name=gettext_lazy('Assignee'),
        related_name='assigned_tasks',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name=gettext_lazy('Author'),
        related_name='created_tasks',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
