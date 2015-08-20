import os
import sys	
sys.path.append('/data/sheptunov.info/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'homepage.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
