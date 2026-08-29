from django.db import models
from django.utils.translation import gettext_lazy


class Label(models.Model):
    name = models.CharField(gettext_lazy('Name'), max_length=100, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
