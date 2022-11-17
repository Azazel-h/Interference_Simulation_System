from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('update-graph/', views.update_graph),
    path('update-history/', views.update_history),
    path('update-preset/', views.update_preset)
]
