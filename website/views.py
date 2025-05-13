from django.shortcuts import render, redirect
from django.utils import translation
from django.conf import settings
from .models import HomePageContent


# Create your views here.
def index(request):
    home_page_content = HomePageContent.objects.first()
    return render(
        request, "homeid/home-01.html", {"home_page_content": home_page_content}
    )


def about(request):
    return render(request, "homeid/about-us.html")


def contact(request):
    return render(request, "homeid/contact-us-1.html")


def error_404(request):
    return render(request, "homeid/404.html")
