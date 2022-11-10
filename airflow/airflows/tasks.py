import json
import uuid

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Search
from .services import make_request, set_currency


@shared_task(bind=True)
def get_data_from_provider(self, search_id: uuid.uuid4, request_url: str):
    with transaction.atomic():
        response = make_request(request_url)
        try:
            search = Search.objects.get(pk=search_id)
        except Search.DoesNotExist:
            return
        items = search.items_dict
        items.extend(response)
        items.sort(key=lambda e: float(e['pricing']['total']), reverse=False)
        search.items = json.dumps(items)
        search.save()
        return 


@shared_task(bind=True)
def download_currencies(self):
    date = timezone.now().date()
    set_currency(date)
    return
