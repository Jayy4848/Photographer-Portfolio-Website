"""
WSGI config for photography_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography_site.settings')

# Initialize Django application
application = get_wsgi_application()

# Vercel serverless function handlers
app = application
handler = application

def migrate_on_vercel():
    """Run migrations on Vercel deployment"""
    if 'VERCEL' in os.environ:
        try:
            from django.core.management import execute_from_command_line
            execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
            print("✅ Database migrations completed successfully")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")

# Run migrations if on Vercel
migrate_on_vercel()
