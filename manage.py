# #!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys


# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elite.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def create_superuser():
    import django
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()
    username = "root"
    email = "admin@example.com"
    password = "Admin123"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superuser created successfully.")
    else:
        print("⚠️ Superuser already exists.")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check if this is a migrate/makemigrations call, then create superuser
    if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
        # Delay creation until after Django is set up
        try:
            execute_from_command_line(sys.argv)
        finally:
            create_superuser()
        return

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
