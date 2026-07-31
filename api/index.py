import os
import shutil
from pathlib import Path
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Auto-migrate database tables on serverless boot
try:
    call_command("migrate", interactive=False)
except Exception:
    pass

# Ensure default admin user and demo student data exist on boot
try:
    from django.contrib.auth.models import User
    from career.models import Student

    if not User.objects.filter(username="admin").exists():
        u = User(username="admin", email="admin@careercompass.com", is_staff=True, is_superuser=True)
        u.set_password("admin123")
        u.save()

    if not Student.objects.filter(entry_code="1234567").exists():
        try:
            call_command("populate_db", 3)
        except Exception:
            Student.objects.create(name="Demo Student", email="student@example.com", entry_code="1234567")
except Exception:
    pass

from config.wsgi import app
