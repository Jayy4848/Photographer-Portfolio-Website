"""
WSGI config for photography_site project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography_site.settings')

# This is what Vercel needs
app = get_wsgi_application()

# Initialize basic data for Vercel
if 'VERCEL' in os.environ:
    try:
        from django.core.management import execute_from_command_line
        from photographer.models import SiteSettings
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create basic site settings if they don't exist
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'photographer_name': 'Professional Photography Studio',
                'tagline': 'Capturing Life\'s Beautiful Moments',
                'about_text': 'Welcome to our photography portfolio. We specialize in creating beautiful, timeless images that tell your story.',
                'hero_title': 'Professional Photography Studio',
                'hero_subtitle': 'Creating timeless memories through the art of photography',
            }
        )
        print("✅ Basic site data initialized")
        
    except Exception as e:
        print(f"⚠️ Initialization warning: {e}")
