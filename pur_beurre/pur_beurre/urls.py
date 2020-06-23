from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("www.urls")),
    path("", include("product.urls")),
    path("mon-compte/", include("account.urls")),
    path("becomeachef/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
