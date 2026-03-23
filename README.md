# Dominion Citadel Schools Backend (Django API)

## Overview
This repository contains the backend API for Dominion Citadel Schools, built with Django and Django REST Framework.  
It provides endpoints for campuses, academic programs, admissions, testimonials, and other backend services.  
The API is designed for multiple environments (development, staging, production) and integrates with MySQL databases.

---

## Features
- Django REST Framework for API endpoints
- MySQL database integration
- Environment-specific settings (dev, staging, prod)
- Role-based authentication (planned)
- Deployed via Namecheap cPanel Python App

---

## Project Structure

v1/
├── manage.py
├── about/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── academics/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── admission/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── config/                # Project settings
│   ├── settings/               # Base, dev, staging, prod configs
│   ├── urls.py
│   └── wsgi.py
├── contact/                    
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── gallery/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── media_config/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── statics/
├── templates/
├── testimonials/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── users/
│   ├──models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── requirements.txt
└── passenger_wsgi.py            # Required for cPanel deployment


---

## Installation (Development)
1. Clone the repo:
   ```bash
   git clone https://github.com/dominion-citadel-schools/backend.git
   cd backend
   
## Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

## Install dependencies:
pip install -r requirements.txt

## python manage.py migrate
python manage.py migrate

## Start development server:
python manage.py runserver

## Environment Setup
Development: Local machine (settings/development.py)

Staging: staging.dominioncitadelschools.com (settings/staging.py)

Production: api.dominioncitadelschool.com (settings/production.py)

Set environment variable in passenger_wsgi.py:
os.environ['DJANGO_SETTINGS_MODULE'] = 'dominion_schools_backend_api.settings.staging'

## Deployment (cPanel)
Upload project to /home/username/staging_api or /home/username/prod_api

Configure Python App in cPanel

Install dependencies:
pip install -r requirements.txt

Collect static files:
python manage.py collectstatic

Restart app in cPanel

## Contribution Guidelines
Branches:

development → local dev

staging → staging server

production → production server

Always create feature branches from development.

Submit pull requests for review before merging.
