from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home_page),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('fabry-perot/', include('fabry_perot.urls')),
    path('michelson/', include('michelson.urls')),
]
