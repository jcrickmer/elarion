import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger("apps.core.auth")


def _get_ip(request):
    if not request:
        return "unknown"
    return request.META.get("REMOTE_ADDR", "unknown")


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request, **kwargs):
    username = credentials.get("username", "unknown")
    logger.warning("login_failed username=%s ip=%s", username, _get_ip(request))


@receiver(user_logged_in)
def on_login_success(sender, request, user, **kwargs):
    logger.info("login_success username=%s ip=%s", user.get_username(), _get_ip(request))


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    username = user.get_username() if user else "anonymous"
    logger.info("logout username=%s ip=%s", username, _get_ip(request))
