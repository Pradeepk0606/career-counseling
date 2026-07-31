import os
import shutil
from pathlib import Path
from django.core.management import call_command
from django.contrib.auth import get_user_model

_serverless_initialized = False


class ServerlessInitMiddleware:
    """
    Middleware that performs zero-config lazy database setup on Vercel/serverless environments.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _serverless_initialized

        if not _serverless_initialized:
            _serverless_initialized = True
            is_vercel = "VERCEL" in os.environ or "AWS_LAMBDA_FUNCTION_NAME" in os.environ

            if is_vercel:
                try:
                    call_command("migrate", interactive=False)
                except Exception:
                    pass

                try:
                    User = get_user_model()
                    if not User.objects.filter(username="admin").exists():
                        u = User(
                            username="admin",
                            email="admin@careercompass.com",
                            is_staff=True,
                            is_superuser=True,
                        )
                        u.set_password("admin123")
                        u.save()
                except Exception:
                    pass

                try:
                    from career.models import Student
                    if not Student.objects.filter(entry_code="1234567").exists():
                        call_command("populate_db", 3)
                except Exception:
                    pass

        response = self.get_response(request)
        return response
