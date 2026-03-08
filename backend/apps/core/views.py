from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/home.html")


def product_overview(request):
    return render(request, "core/product_overview.html")


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


def signup(request):
    return render(request, "registration/signup.html")
