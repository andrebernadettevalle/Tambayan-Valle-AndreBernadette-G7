from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing-list'),
    path('mine/', views.my_listings, name='my-listings'),
    path('new/', views.listing_create, name='listing-create'),
    path('<int:pk>/', views.listing_detail, name='listing-detail'),
    path('<int:pk>/edit/', views.listing_update, name='listing-update'),
    path('<int:pk>/delete/', views.listing_delete, name='listing-delete'),
]