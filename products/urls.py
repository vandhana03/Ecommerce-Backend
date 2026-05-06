from django.urls import path

from .import views
# from .views import View

urlpatterns = [
    path('products/',views.ProductListCreateView.as_view()),
    path('products/<int:product_id>/',views.ProductDetailView.as_view()),
]