"""
WSGI config for photography_site project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography_site.settings')

# This is what Vercel needs
app = get_wsgi_application()

def handler(request):
    return app(request.environ, request.start_response)
