
from django.urls import path
from .import views




urlpatterns = [
    path('checkout/',views.CheckoutView.as_view()),
    path('',views.OrderListView.as_view()),
    path('<int:order_id>/',views.UpdateOrderStatusView.as_view()),


]