from django.urls import path

from . import views


app_name = 'michelson'

urlpatterns = [
    path('', views.index_page, name='index'),
    path('update_graph/', views.update_graph),
    path('update_history/', views.update_history),
    path('update_preset/', views.update_preset)
]
