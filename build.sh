#!/bin/bash
# Force Python 3.11 installation
export PATH=/opt/render/project/python/Python-3.11.9/bin:$PATH

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
