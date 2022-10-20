from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('visualization.urls')),
    path('michelson/', include('michelson.urls')),
    path('accounts/', include('accounts.urls')),
]
