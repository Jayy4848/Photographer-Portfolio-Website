"""
WSGI config for photography_site project.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography_site.settings')

# Initialize Django first to set up the environment
application = get_wsgi_application()

# Enhanced initialization for Vercel
if 'VERCEL' in os.environ:
    try:
        print("🚀 Starting Vercel initialization...")
        
        # Run migrations with more verbose output
        print("📋 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ Database migrations completed successfully")
        
        # Import models after migrations are complete
        from django.apps import apps
        from photographer.models import SiteSettings
        
        # Ensure all models are loaded
        apps.populate()
        
        # Create basic site settings
        print("🏗️ Creating site settings...")
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
                'working_hours': 'Mon-Fri: 9AM-6PM, Sat-Sun: 10AM-4PM',
                'meta_title': 'Professional Photography Studio',
                'meta_description': 'Professional photography services for all your special moments.',
            }
        )
        
        if created:
            print("✅ Site settings created successfully")
        else:
            print("✅ Site settings already exist")
        
        print("🎉 Vercel initialization completed successfully!")
        
    except Exception as e:
        print(f"⚠️ Initialization error: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        # Continue anyway - the app should still work with error handling in views

# Export the app for Vercel
app = application
