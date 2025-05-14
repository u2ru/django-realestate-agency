from django.shortcuts import render
from .models import HomePageContent, AboutUsContent
from property.models import Property, PROPERTY_TYPE_CHOICES, DEAL_TYPE_CHOICES
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
    status_list = DEAL_TYPE_CHOICES

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
                "status_list": status_list,
            },
        },
    )


def about(request):
    about_us_content = AboutUsContent.objects.first()
    return render(
        request,
        "homeid/about-us.html",
        {
            "about_us_content": {
                "hero_title": about_us_content.get_translation("hero_title"),
                "hero_image": about_us_content.hero_image,
                "main_subtitle": about_us_content.get_translation("main_subtitle"),
                "main_title": about_us_content.get_translation("main_title"),
                "main_content": about_us_content.get_translation("main_content"),
                "our_services_title": about_us_content.get_translation(
                    "our_services_title"
                ),
                "our_services_content": about_us_content.get_translation(
                    "our_services_content"
                ),
                "office_location_address": about_us_content.office_location_address,
                "office_coordinates": {
                    "lat": str(about_us_content.office_coordinates["lat"]).replace(
                        ",", "."
                    ),
                    "lng": str(about_us_content.office_coordinates["lng"]).replace(
                        ",", "."
                    ),
                },
                "bottom_section_title": about_us_content.get_translation(
                    "bottom_section_title"
                ),
                "bottom_section_content": about_us_content.get_translation(
                    "bottom_section_content"
                ),
            }
        },
    )


def error_404(request):
    return render(request, "homeid/404.html")
