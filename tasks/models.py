from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy

from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(gettext_lazy('Name'), max_length=100, unique=True)
    description = models.TextField(gettext_lazy('Description'), blank=True)
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
    labels = models.ManyToManyField(
        Label, verbose_name=gettext_lazy('Labels'), through='LabelTask', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LabelTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
