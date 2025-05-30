"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.views.static import serve

admin.site.site_title = "Real Estate Admin"
admin.site.site_header = "Real Estate Admin"


def redirect_root(request):
    return redirect(f"/{settings.LANGUAGE_CODE}/")


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # for set_language
    path("", redirect_root),  # Redirect / to /en/ or your default language
    #
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += i18n_patterns(
    path("", include("website.urls"), name="home"),
    path("property/", include("property.urls", namespace="property")),
    path("admin/", admin.site.urls),
    prefix_default_language=False,
)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
