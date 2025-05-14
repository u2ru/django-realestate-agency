from .models import HomePageContent


def homepage_content(request):
    home_page_content = HomePageContent.objects.first()
    return {
        "footer_content": {
            "company_name": (
                home_page_content.company_name if home_page_content else None
            ),
            "address": (
                home_page_content.contact_address if home_page_content else None
            ),
            "email": (home_page_content.contact_email if home_page_content else None),
            "phone": (home_page_content.contact_phone if home_page_content else None),
            "facebook_url": (
                home_page_content.facebook_url if home_page_content else None
            ),
            "instagram_url": (
                home_page_content.instagram_url if home_page_content else None
            ),
        }
    }
