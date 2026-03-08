from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import SignupForm


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
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('login')}?created=1")
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})
