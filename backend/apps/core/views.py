from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.contrib import messages
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


class RateLimitedLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm

    def _attempt_key(self, username):
        ip = self.request.META.get("REMOTE_ADDR", "unknown")
        return f"login_attempts:{ip}:{(username or '').strip().lower()}"

    def dispatch(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        limit = self._limit()
        if request.method == "POST" and cache.get(self._attempt_key(username), 0) >= limit:
            form = self.get_form()
            form.add_error(None, "Too many failed login attempts. Please try again later.")
            return self.render_to_response(self.get_context_data(form=form), status=429)
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        key = self._attempt_key(self.request.POST.get("username", ""))
        timeout = self._window_seconds()
        current = cache.get(key, 0)
        cache.set(key, current + 1, timeout=timeout)
        return super().form_invalid(form)

    def form_valid(self, form):
        key = self._attempt_key(self.request.POST.get("username", ""))
        cache.delete(key)
        return super().form_valid(form)

    def _limit(self):
        from django.conf import settings

        return settings.LOGIN_RATE_LIMIT_ATTEMPTS

    def _window_seconds(self):
        from django.conf import settings

        return settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS


class RedirectingLogoutView(LogoutView):
    next_page = "home"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, "You are now logged out.")
        return response


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
