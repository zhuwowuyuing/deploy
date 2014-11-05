"""
WSGI config for Deploy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

# import os, sys
#
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# sys.path.append(BASE_DIR)
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deploy.settings")
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

import os, sys, site

# Add the virtual Python environment site-packages directory to the path
# ../../lib/python2.6/site-packages/
ve_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..", "lib/python2.6/site-packages/"))
site.addsitedir(ve_path)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deploy.settings")

# Activate your virtual env
activate_env=os.path.expanduser("/data/website/deploy_web/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()