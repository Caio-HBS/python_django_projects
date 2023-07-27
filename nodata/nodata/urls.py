from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include("dorin.urls")),
    path('dorin/', include("dorin.urls")),
    path('dorinsocialapi/', include('dorinsocialapi.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('admin/', admin.site.urls),
]
