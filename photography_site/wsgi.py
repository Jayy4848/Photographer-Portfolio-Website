"""
WSGI config for photography_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography_site.settings')

# Initialize Django
application = get_wsgi_application()

# For Vercel deployment - run migrations and setup
if 'VERCEL' in os.environ:
    try:
        from django.core.management import execute_from_command_line
        from django.db import connection
        from django.contrib.auth import get_user_model
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        
        # Create sample data if needed
        try:
            from photographer.management.commands.populate_sample_data import Command
            command = Command()
            command.handle()
        except Exception as e:
            print(f"Sample data creation failed: {e}")
            
    except Exception as e:
        print(f"Database initialization failed: {e}")
        # Continue anyway to avoid blocking the app
