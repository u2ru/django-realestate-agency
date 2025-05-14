from .models import HomePageContent


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
