from django.conf import settings


def currencies(request):
    """
    Context processor that provides currency information to all templates.
    """
    return {
        "CURRENCIES": [
            {"symbol": "$", "code": "USD", "is_active": True},
            {"symbol": "€", "code": "EUR", "is_active": False},
            {"symbol": "₾", "code": "GEL", "is_active": False},
        ]
    }
