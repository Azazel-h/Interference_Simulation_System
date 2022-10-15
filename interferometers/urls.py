from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index_page),  # Main page
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('fpi/', include('fpi.urls')),  # Fabry-Perot interferometer
]
