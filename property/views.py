from django.shortcuts import render

from .models import Property


def index(request):
    properties = Property.objects.all()
    return render(request, "index.html", {"properties": properties})
