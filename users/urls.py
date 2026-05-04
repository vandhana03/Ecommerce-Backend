from django.urls import path

from .import views
# from .views import View

urlpatterns = [
    path('register/',views.RegisterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('products/',views.ProductListCreateView.as_view()),
    path('products/<int:product_id>/',views.ProductDetailView.as_view()),

    # path('me/', views.MeView.as_view()),
]
