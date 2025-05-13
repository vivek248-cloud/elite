#!/bin/bash

cd $RENDER_PROJECT_ROOT

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py shell < create_superuser.py
