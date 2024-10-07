from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('document/<str:title>/', views.view_document, name='view_document'),
]