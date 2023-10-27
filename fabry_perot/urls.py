from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('graph/', views.ShowGraph.as_view()),
    path('graph-report/', views.GraphReport.as_view()),
    path('history/', views.HistoryTable.as_view()),
    path('preset/', views.PresetsTable.as_view())
]
