from django.urls import path
from apps.catalog.views import CategoryIndexView, ProductsByCategoryView, ProductDetailView


urlpatterns = [
    path('', CategoryIndexView.as_view(), name='Catalog'),
    path('<str:slug>/', ProductsByCategoryView.as_view(), name='Categories'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product')
]
