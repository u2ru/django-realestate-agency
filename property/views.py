from django.shortcuts import render
from django.db.models import Q

from .models import Property


def index(request):
    properties = Property.objects.all()

    # Get search parameters from request
    search_query = request.GET.get("q", "")
    property_type = request.GET.get("property_type", "")
    deal_type = request.GET.get("deal_type", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    city = request.GET.get("city", "")
    region = request.GET.get("region", "")
    min_area = request.GET.get("min_area")
    max_area = request.GET.get("max_area")
    rooms = request.GET.get("rooms")

    # Apply filters based on provided parameters
    if search_query:
        properties = properties.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(location__icontains=search_query)
        )

    if property_type:
        properties = properties.filter(property_type=property_type)

    if deal_type:
        properties = properties.filter(deal_type=deal_type)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    if city:
        properties = properties.filter(city__icontains=city)

    if region:
        properties = properties.filter(region__icontains=region)

    if min_area:
        properties = properties.filter(area__gte=min_area)

    if max_area:
        properties = properties.filter(area__lte=max_area)

    if rooms:
        properties = properties.filter(rooms=rooms)

    # Add search parameters to context to maintain them in the form
    context = {
        "properties": properties,
        "search_params": {
            "q": search_query,
            "property_type": property_type,
            "deal_type": deal_type,
            "min_price": min_price,
            "max_price": max_price,
            "city": city,
            "region": region,
            "min_area": min_area,
            "max_area": max_area,
            "rooms": rooms,
        },
    }

    return render(request, "homeid/listing-full-width-grid-1.html", context)


def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    return render(request, "homeid/single-property-6.html", {"property": property})
