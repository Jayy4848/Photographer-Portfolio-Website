"""
WSGI config for photography_site project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography_site.settings')

application = get_wsgi_application()

# For Vercel
app = application
