from decimal import Decimal
from typing import Dict, Any

# Exchange rates (you can move these to settings.py or fetch from an API)
EXCHANGE_RATES = {
    "USD": {
        "GEL": Decimal("2.7"),
        "EUR": Decimal("0.92"),
    },
    "EUR": {
        "USD": Decimal("1.09"),
        "GEL": Decimal("2.93"),
    },
    "GEL": {
        "USD": Decimal("0.37"),
        "EUR": Decimal("0.34"),
    },
}


def convert_currency(amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
    """
    Convert amount from one currency to another.

    Args:
        amount (Decimal): The amount to convert
        from_currency (str): Source currency code
        to_currency (str): Target currency code

    Returns:
        Decimal: Converted amount
    """
    if from_currency == to_currency:
        return amount

    try:
        rate = EXCHANGE_RATES[from_currency][to_currency]
        return amount * rate
    except KeyError:
        # If conversion rate not found, return original amount
        return amount
