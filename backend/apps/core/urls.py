from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product-overview/", views.product_overview, name="product_overview"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("auth/signup/", views.signup, name="signup"),
]
