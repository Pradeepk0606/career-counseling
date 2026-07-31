import logging
import os
from django.contrib.auth import get_user_model
from django.core.management import call_command

logger = logging.getLogger(__name__)
_serverless_initialized = False


def ensure_serverless_db():
    """
    Ensures migrations are run and default admin/student credentials exist.
    """
    global _serverless_initialized
    if _serverless_initialized:
        return
    _serverless_initialized = True

    # 1. Run migrations to ensure all tables exist
    try:
        call_command("migrate", verbosity=0, interactive=False)
    except Exception as e:
        logger.error("Migration error on serverless boot: %s", e)

    # 2. Ensure default admin superuser exists with known credentials
    try:
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@careercompass.com",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        user.set_password("admin123")
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
    except Exception as e:
        logger.error("Superuser setup error: %s", e)

    # 3. Ensure sample student data exists
    try:
        from career.models import Student

        if not Student.objects.filter(entry_code="1234567").exists():
            call_command("populate_db", 3, verbosity=0)
    except Exception as e:
        logger.error("Populate DB error: %s", e)


class ServerlessInitMiddleware:
    """
    Middleware that performs zero-config database setup on Vercel/serverless environments.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ensure_serverless_db()
        return self.get_response(request)
