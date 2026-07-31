import os
import shutil
from pathlib import Path
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Auto-migrate database tables on serverless boot if needed
try:
    call_command("migrate", interactive=False)
except Exception:
    pass

from config.wsgi import app
