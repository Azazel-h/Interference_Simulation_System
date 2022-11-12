from django.urls import path

from . import views


app_name = 'michelson'

urlpatterns = [
    path('', views.index_page, name='index'),
]
