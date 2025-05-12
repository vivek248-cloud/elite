import os
import django

# Set the default settings module for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elite.settings")

# Setup Django
django.setup()

from django.contrib.auth.models import User
from django.db import IntegrityError

def create_superuser():
    try:
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        print("Superuser created successfully.")
    except IntegrityError:
        print("Superuser already exists.")

if __name__ == "__main__":
    create_superuser()
