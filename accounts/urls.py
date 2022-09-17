import django_cas_ng.views

from django.urls import path

urlpatterns = [
    path('login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
]
