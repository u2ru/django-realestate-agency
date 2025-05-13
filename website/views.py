from django.shortcuts import render
from .models import HomePageContent
from property.models import Property, PROPERTY_TYPE_CHOICES
from property.constants import CITY_CHOICES
from django.db.models import Max


# Create your views here.
def index(request):
    home_page_content = HomePageContent.objects.first()
    featured_properties_for_sale = Property.objects.filter(
        featured=True, deal_type="SALE"
    )[:5]
    featured_properties_for_rent = Property.objects.filter(
        featured=True, deal_type="RENT"
    )[:5]
    # filter properties
    city_list = CITY_CHOICES
    home_types = PROPERTY_TYPE_CHOICES
    max_bedrooms = Property.objects.aggregate(Max("bedrooms"))["bedrooms__max"]
    bedroom_list = [(i, str(i)) for i in range(1, max_bedrooms + 1)]
    area_range_max = Property.objects.aggregate(Max("area"))["area__max"]
    price_range_max = Property.objects.aggregate(Max("price"))["price__max"]
    print("area_range_max", area_range_max)
    print("price_range_max", price_range_max)
    return render(
        request,
        "homeid/home-01.html",
        {
            "home_page_content": {
                "hero_title": home_page_content.get_translation("hero_title"),
                "hero_subtitle": home_page_content.get_translation("hero_subtitle"),
                "hero_image": home_page_content.hero_image,
            },
            "featured_properties_for_sale": featured_properties_for_sale,
            "featured_properties_for_rent": featured_properties_for_rent,
            "filter_properties": {
                "city_list": city_list,
                "home_types": home_types,
                "bedroom_list": bedroom_list,
                "area_range_max": area_range_max,
                "price_range_max": price_range_max,
            },
        },
    )


def about(request):
    return render(request, "homeid/about-us.html")


def contact(request):
    return render(request, "homeid/contact-us-1.html")


def error_404(request):
    return render(request, "homeid/404.html")
