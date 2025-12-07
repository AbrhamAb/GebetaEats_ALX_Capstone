from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
        path('admin/', admin.site.urls),

            # auth
                path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

                        # app endpoints
                            path('api/auth/', include('users.urls')), 
                                path('api/vendors/', include('vendors.urls')), 
                                    path('api/menu/', include('menu.urls')),  
]
