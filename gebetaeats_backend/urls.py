from django.contrib import admin
from django.urls import include, path

from users.views import LoginView, RefreshTokenView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/",
         RefreshTokenView.as_view(), name="token_refresh"),
    path("api/auth/", include("users.urls")),
    path("api/vendors/", include("vendors.urls")),
    path("api/vendors/", include("menu.urls")),
    path("api/orders/", include("orders.urls")),
    path("", include("web.urls")),
]
