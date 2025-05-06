from django.urls import path
from . import views
app_name = 'bob'
urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('graph', views.graph, name='graph'),
    path('questions/', views.questions, name='questions'),
    path('answers/', views.answers, name='answers'),
]