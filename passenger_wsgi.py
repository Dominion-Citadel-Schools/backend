import os
import sys

# Ensure project path is available
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# OPTIONAL: only if using .env
from dotenv import load_dotenv
load_dotenv()

# Environment switching
env = os.environ.get("DJANGO_ENV", "production")

if env == "staging":
    settings_module = "config.settings.staging"
elif env == "development":
    settings_module = "config.settings.development"
else:
    settings_module = "config.settings.production"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()