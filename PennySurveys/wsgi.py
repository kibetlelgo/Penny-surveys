"""
WSGI config for PennySurveys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PennySurveys.settings')

application = get_wsgi_application()

if (
    os.environ.get('VERCEL')
    and settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'
):
    call_command('migrate', interactive=False, verbosity=0)
