"""
WSGI config for homepage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

path = '/data/sheptunov.info'
if path not in sys.path:
    sys.path.append(path)

os.environ['LANG']='ru_RU.UTF-8'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homepage.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
