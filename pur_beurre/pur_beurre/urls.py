from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("www.urls", namespace="www")),
    path("", include("product.urls", namespace="product")),
    path("mon-compte/", include("account.urls", namespace="account")),
    path("becomeachef/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
