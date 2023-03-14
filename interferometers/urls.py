from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # Main paths
    path('', views.home_page),
    path('admin/', admin.site.urls),
    path('team/', views.team_page),
    # Applications
    path('accounts/', include('accounts.urls')),
    path('fabry-perot/', include('fabry_perot.urls')),
    path('michelson/', include('michelson.urls')),
]
