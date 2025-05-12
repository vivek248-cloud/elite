
#!/bin/bash

# Install required dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run the server (optional for local development, but for deployment, you may use a production server like gunicorn)
python manage.py runserver 0.0.0.0:8000