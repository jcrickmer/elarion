from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def product_overview(request):
    return render(request, "core/product_overview.html")


def signup(request):
    return render(request, "registration/signup.html")
