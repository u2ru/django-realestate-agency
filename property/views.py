from django.shortcuts import render
from django.db.models import Q
from django.db.models import Max
from django.forms.models import model_to_dict
from .models import (
    Property,
    PROPERTY_TYPE_CHOICES,
    PRICE_TYPE_CHOICES,
    DEAL_TYPE_CHOICES,
    FEATURE_CHOICES,
)
from .constants import CITY_CHOICES


def index(request):
    properties = Property.objects.all()

    # Get search parameters from request
    deal_type = request.GET.get("deal_type", "")
    type = request.GET.get("type", "")
    search = request.GET.get("search", "")
    bedrooms = request.GET.get("bedrooms", "")
    if bedrooms:
        bedrooms = int(bedrooms)
    city = request.GET.get("city", "")
    price_type = request.GET.get("price_type", "")
    # price = request.GET.get("price", "")
    # area = request.GET.get("area", "")
    property_id = request.GET.get("property_id", "")
    features = set(request.GET.getlist("features"))

    if features:
        all_properties = list(properties)
        properties = [
            p for p in all_properties if features.intersection(set(p.features))
        ]

    # Apply filters based on provided parameters
    if search:
        filtered_properties = properties.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(address__icontains=search)
        )
        if filtered_properties.count() != 0:
            properties = filtered_properties

    if deal_type:
        deal_type_formatted = [
            choice[0]
            for choice in DEAL_TYPE_CHOICES
            if choice[1].lower().replace(" ", "-") == deal_type
        ]
        if deal_type_formatted:
            properties = properties.filter(deal_type=deal_type_formatted[0])

    if type:
        properties = properties.filter(property_type=type)

    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    if city:
        properties = properties.filter(city=city)

    # if price:
    #     properties = properties.filter(price__range=price)

    if price_type:
        properties = properties.filter(price_type=price_type)

    # if area:
    #     properties = properties.filter(area__range=area)

    if property_id:
        properties = properties.filter(property_id=property_id)

    # filter properties
    city_list = CITY_CHOICES
    home_types = PROPERTY_TYPE_CHOICES
    max_bedrooms = (
        Property.objects.aggregate(Max("bedrooms"))["bedrooms__max"]
        if Property.objects.aggregate(Max("bedrooms"))["bedrooms__max"] > 6
        else 6
    )
    bedroom_list = [(i, str(i)) for i in range(1, max_bedrooms + 1)]
    area_range_max = Property.objects.aggregate(Max("area"))["area__max"]
    price_range_max = Property.objects.aggregate(Max("price"))["price__max"]
    status_list = DEAL_TYPE_CHOICES
    features_list = FEATURE_CHOICES

    # Add search parameters to context to maintain them in the form
    context = {
        "properties": properties,
        "search_params": {
            "deal_type": deal_type,
            "type": type,
            "search": search,
            "bedrooms": bedrooms,
            "city": city,
            "price_type": price_type,
            # "price": price,
            # "area": area,
            "property_id": property_id,
        },
        "filter_properties": {
            "city_list": city_list,
            "home_types": home_types,
            "bedroom_list": bedroom_list,
            "area_range_max": area_range_max,
            "price_range_max": price_range_max,
            "price_type_list": PRICE_TYPE_CHOICES,
            "status_list": status_list,
            "features_list": features_list,
        },
        "values_from_search": {
            "city": city,
            "price_type": price_type,
            "type": type,
            "deal_type": [
                choice[0] for choice in DEAL_TYPE_CHOICES if choice[0] == deal_type
            ],
            "bedrooms": bedrooms,
            "features": features,
        },
    }

    return render(request, "homeid/listing-full-width-grid-1.html", context)


def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    similar_properties = Property.objects.filter(property_type=property.property_type)[
        :4
    ]

    city_list = CITY_CHOICES
    home_types = PROPERTY_TYPE_CHOICES

    # Convert model to dict and add translations
    property_dict = model_to_dict(property)
    property_dict.update(
        {
            "name": property.get_translation("name"),
            "description": property.get_translation("description"),
            "price_per_area": property.price_per_area,  # Add the property
            "get_youtube_url": property.get_youtube_url(),  # Add the method
            "get_main_image": property.get_main_image(),  # Add the method
            "get_images": list(property.get_images()),  # Add the method
            "coordinates": (
                {
                    "lng": (str(property.coordinates.get("lng", "")).replace(",", ".")),
                    "lat": (str(property.coordinates.get("lat", "")).replace(",", ".")),
                }
                if property.coordinates
                else None
            ),
        }
    )

    return render(
        request,
        "homeid/single-property-6.html",
        {
            "property": property_dict,
            "similar_properties": similar_properties,
            "filter_properties": {
                "city_list": city_list,
                "home_types": home_types,
            },
        },
    )
