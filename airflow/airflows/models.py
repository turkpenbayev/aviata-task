import uuid
import json

from django.db import models


class Search(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=256)
    tasks = models.TextField(null=True, blank=True)
    items = models.TextField(null=True, blank=True)

    @property
    def tasks_list(self):
        return self.tasks.split(',') if self.tasks else []

    @property
    def items_dict(self):
        return json.loads(self.items) if self.items else []


class Currency(models.Model):
    date = models.DateField()
    currencies = models.TextField()

    @property
    def currencies_dict(self):
        return json.loads(self.currencies) if self.currencies else None
