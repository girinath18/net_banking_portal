import requests as req
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import ExchangeRate as er
from datetime import datetime

def index(request):
    # Proper response with a JSON object
    return JsonResponse({"message": "Welcome to the Exchange Rate App!"})

class ExchangeRateView(View):
    # List of currencies supported
    supported_currencies = ["CHF", "EUR", "USD", "CAD", "AUD", "GBP", "HRK", "HKD", "ISK",
                            "PHP", "DKK", "HUF", "CZK", "RON", "SEK", "IDR", "INR", "BRL",
                            "RUB", "JPY", "THB", "MYR", "BGN", "TRY", "CNY", "NOK", "NZD",
                            "ZAR", "MXN", "SGD", "ILS", "KRW", "PLN"]

    def get_exchange_rate_data(self, base_currency):
        """Fetch exchange rate data from the external API."""
        URL = "https://api.exchangeratesapi.io/latest"
        try:
            # API call with the base currency
            response = req.get(url=URL, params={"base": base_currency})
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except req.RequestException as e:
            return {"error": str(e)}

    def update_rates(self, current_date, rates):
        """Update database with the latest exchange rates."""
        try:
            currencies = ["RUB", "CNY", "USD", "GBP", "JPY"]
            for idx, currency in enumerate(currencies):
                rate = rates.get(currency)
                if rate:
                    query = er.objects.get(id=idx + 1)
                    query.update_exchange_rate(current_date, rate)
                    query.save()
        except Exception as e:
            return {"error": str(e)}

    def get(self, request, *args, **kwargs):
        """GET request handler for fetching exchange rates."""
        base_currency = "EUR"
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fetch rates from the database
        try:
            query = er.objects.all()
            last_update = query[0].get_exchange_rate()['updated']
            rates = {query[i].currency: query[i].get_exchange_rate()['rate'] for i in range(len(query))}

            # Check if update is needed
            last = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
            current = datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S")
            if (current - last).total_seconds() / 3600 > 24:
                api_data = self.get_exchange_rate_data(base_currency)
                if "error" not in api_data:
                    self.update_rates(current_date, api_data['rates'])
                else:
                    return JsonResponse(api_data, status=500)

            return JsonResponse({"source": "db", **rates})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class ExchangeRateRawView(View):
    def get(self, request, *args, **kwargs):
        """GET request handler for fetching raw exchange rate data."""
        base_currency = "EUR"
        api_data = ExchangeRateView().get_exchange_rate_data(base_currency)

        if "error" in api_data:
            return JsonResponse(api_data, status=500)

        # Extract required rates
        rates = {key: api_data["rates"].get(key) for key in ["RUB", "CNY", "USD", "GBP", "JPY"]}
        return JsonResponse({"source": "api", **rates})
