from django.urls import path
from . import views
from django.conf.urls.i18n import set_language
from django.shortcuts import redirect


def set_currency(request):
    currency = request.POST.get("currency")
    request.session["currency"] = currency
    return redirect(request.META.get("HTTP_REFERER", "/"))


urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    # path("contact/", views.contact, name="contact"),
    path("404", views.error_404, name="error_404"),
    path("set_language/", set_language, name="set_language"),
    path("set_currency/", set_currency, name="set_currency"),
]
