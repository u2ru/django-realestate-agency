from django.shortcuts import render
from .models import HomePageContent
from property.models import Property
from django.utils import translation


# Create your views here.
def index(request):
    home_page_content = HomePageContent.objects.first()
    featured_properties = Property.objects.filter(featured=True)[:5]
    return render(
        request,
        "homeid/home-01.html",
        {
            "home_page_content": {
                "hero_title": home_page_content.get_translation("hero_title"),
                "hero_subtitle": home_page_content.get_translation("hero_subtitle"),
                "hero_image": home_page_content.hero_image,
            },
            "featured_properties": featured_properties,
        },
    )


def about(request):
    return render(request, "homeid/about-us.html")


def contact(request):
    return render(request, "homeid/contact-us-1.html")


def error_404(request):
    return render(request, "homeid/404.html")
