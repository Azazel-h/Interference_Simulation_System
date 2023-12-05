from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='fp-index'),
    path('graph/', views.Graph.as_view()),
    path('history/', views.HistoryTable.as_view()),
    path('preset/', views.PresetsTable.as_view())
]
