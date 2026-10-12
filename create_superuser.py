import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinic.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()
username = os.environ.get("ADMIN_USERNAME", "admin")
password = os.environ.get("ADMIN_PASSWORD")

if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email="", password=password)
    print(f"Created superuser '{username}'.")
else:
    print("Superuser skipped (already exists or ADMIN_PASSWORD not set).")
