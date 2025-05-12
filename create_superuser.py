from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import IntegrityError

def create_superuser():
    try:
        # Replace with your preferred superuser credentials
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        print("Superuser created successfully.")
    except IntegrityError:
        print("Superuser already exists.")

if __name__ == "__main__":
    create_superuser()

