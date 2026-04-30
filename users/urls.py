from django.urls import path

from .import views
# from .views import View

urlpatterns = [
    path('register/',views.RegisterView.as_view()),

]
