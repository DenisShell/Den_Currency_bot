import requests
import json
from config_cb import keys

class ConversionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Невозможно посчитать одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Ошибка в написании валюты {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Ошибка в написании валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Ошибка в указании количества {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base