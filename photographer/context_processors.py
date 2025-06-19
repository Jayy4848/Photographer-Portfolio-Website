from django.db import OperationalError
from .models import Category

def featured_categories(request):
    """
    Context processor to provide featured categories to all templates
    """
    try:
        categories = Category.objects.filter(is_featured=True)[:6]
        return {'featured_categories': categories}
    except (OperationalError, Exception):
        # Return empty queryset if database isn't ready or tables don't exist
        return {'featured_categories': Category.objects.none() if 'Category' in globals() else []} 