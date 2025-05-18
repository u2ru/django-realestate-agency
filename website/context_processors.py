from .models import HomePageContent
from django.conf import settings
from django.utils.translation import get_language


def common_context(request):
    """Context processor to add common data to all templates"""
    home_page_content = HomePageContent.objects.first()
    return {
        "logo": (
            home_page_content.logo.url
            if home_page_content and home_page_content.logo
            else None
        ),
        "logo_white": (
            home_page_content.logo_white.url
            if home_page_content and home_page_content.logo_white
            else None
        ),
        "footer_content": {
            "company_name": home_page_content.company_name if home_page_content else "",
            "contact_phone": (
                home_page_content.contact_phone if home_page_content else ""
            ),
            "contact_email": (
                home_page_content.contact_email if home_page_content else ""
            ),
            "contact_address": (
                home_page_content.contact_address if home_page_content else ""
            ),
            "facebook_url": home_page_content.facebook_url if home_page_content else "",
            "instagram_url": (
                home_page_content.instagram_url if home_page_content else ""
            ),
        },
    }


def currency(request):
    """
    Context processor that provides currency information to all templates.
    Returns the current currency and available currencies.
    """
    current_currency = request.session.get("currency", settings.CURRENCY)
    currencies = []
    for code, symbol in settings.CURRENCIES:
        currencies.append(
            {"code": code, "symbol": symbol, "is_active": code == current_currency}
        )

    return {"CURRENCY": current_currency, "CURRENCIES": currencies}


def language(request):
    """
    Context processor that provides language information to all templates.
    """
    current_language = get_language() or settings.LANGUAGE_CODE
    return {"LANGUAGE": current_language}
