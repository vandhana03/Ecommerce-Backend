from django.urls import path

from .import views
# from .views import View

urlpatterns = [
    path('cart/',views.CartView.as_view()),
]