import requests
import xmltodict
import json
from functools import lru_cache

from django.utils import timezone
from .models import Currency


def make_request(url: str):
    with requests.Session() as session:
        try:
            response = session.post(url=url, timeout=100)
            if response.status_code == 404:
                return None
            response.raise_for_status()
        except requests.RequestException as e:
            raise e
        return response.json()


def set_currency(date):
    with requests.Session() as session:
        response = session.get(
            url=f"https://www.nationalbank.kz/rss/get_rates.cfm?fdate={date.strftime('%d.%m.%Y')}", timeout=100)
    my_xml = xmltodict.parse(response.text)
    currency_dict = {'kzt': {'quant': 1, 'description': 1}}
    for item in my_xml['rates']['item']:
        currency_dict[str(item['title']).lower()] = {
            'quant': item['quant'],
            'description': item['description']
        }

    currency, created = Currency.objects.get_or_create(
        date=date,
        defaults={
            'currencies': json.dumps(currency_dict)
        }
    )
    return currency


@lru_cache(maxsize=2)
def get_currencies(date) -> dict:
    try:
        currency = Currency.objects.get(date=date)
    except Currency.DoesNotExist:
        currency = set_currency(date)
    return currency.currencies_dict
