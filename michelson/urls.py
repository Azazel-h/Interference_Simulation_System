from django.urls import path

from . import views


app_name = 'michelson'

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('update-graph/', views.Graph.as_view()),
    path('update-history/', views.HistoryTable.as_view()),
    path('update-preset/', views.PresetsTable.as_view())
]
