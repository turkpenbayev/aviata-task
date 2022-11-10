import json

from celery.result import AsyncResult
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Search, Currency
from .tasks import get_data_from_provider
from .serializers import ResultSerializer
from .services import get_currencies


provider_urls = ['http://127.0.0.1:8001/search', 'http://127.0.0.1:8002/search']


@api_view(['GET'])
def results(request, search_id = None, currency = None, *args, **kwargs):
    try:
        search = Search.objects.get(pk=search_id)
    except Search.DoesNotExist:
        return Response({'error': 'search not found'}, status=status.HTTP_404_NOT_FOUND)

    if search.status != "COMPLETED":
        is_finished = True
        for task_id in search.tasks_list:
            if AsyncResult(task_id).state != "SUCCESS":
                is_finished = False
                break

        if is_finished:
            search.status = "COMPLETED"
            search.save()

    currencies = get_currencies(timezone.now().date())
    if currency.lower() not in currencies.keys():
        return Response({'error': 'currency does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'search_id': search.pk,
        'status': search.status
    }
    items = search.items_dict
    for item in items:
        pricing = item['pricing']
        if pricing['currency'].lower() == currency.lower():
            amount = pricing['total']
        else:
            currency_kzt = currencies[pricing['currency'].lower()]
            currency_req = currencies[currency.lower()]
            total = float(pricing['total'])
            kzt_d = float(currency_kzt['description'])
            kzt_q = float(currency_kzt['quant'])
            req_d = float(currency_req['description'])
            req_q = float(currency_req['quant'])
            amount = "{:.2f}".format(total*kzt_d*req_q/(req_d*kzt_q))

        item['price'] = {
            'amount': amount,
            'currency': currency.upper()
        }
    data['itemes'] = items
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def search(request, *args, **kwargs):
    search = Search.objects.create(status='PENDING')
    tasks=[]
    for provider_url in provider_urls:
        task = get_data_from_provider.apply_async(
            args=(search.pk, provider_url)
        )
        tasks.append(task.id)
    search.tasks = ','.join(tasks)
    search.save()
    return Response({'search_id': search.pk}, status=status.HTTP_200_OK)
