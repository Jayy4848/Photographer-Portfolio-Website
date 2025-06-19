"""
WSGI config for photography_site project.
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography_site.settings')

# Initialize Django first to set up the environment
application = get_wsgi_application()

# Run initialization for Vercel BEFORE serving requests
if 'VERCEL' in os.environ:
    try:
        # Run migrations first
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Migrations completed")
        
        # Then create basic site settings
        from photographer.models import SiteSettings
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'photographer_name': 'Professional Photography Studio',
                'tagline': 'Capturing Life\'s Beautiful Moments',
                'about_text': 'Welcome to our photography portfolio. We specialize in creating beautiful, timeless images that tell your story.',
                'hero_title': 'Professional Photography Studio',
                'hero_subtitle': 'Creating timeless memories through the art of photography',
                'email': 'contact@studio.com',
                'phone': '+1 (555) 123-4567',
                'address': '123 Photography Lane, Creative City',
            }
        )
        if created:
            print("✅ Basic site settings created")
        else:
            print("✅ Site settings already exist")
        
    except Exception as e:
        print(f"⚠️ Initialization error: {e}")

# Export the app for Vercel
app = application
