#!/bin/bash

# Set working directory to where manage.py is (change 'index' if needed)
cd "$(dirname "$0")"

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py shell < create_superuser.py
