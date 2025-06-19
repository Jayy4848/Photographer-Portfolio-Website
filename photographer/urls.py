from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'photographer'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery_detail'),
    path('about/', views.about, name='about'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    
    # Individual image detail (for lightbox or dedicated pages)
    path('image/<int:pk>/', views.ImageDetailView.as_view(), name='image_detail'),
    
    # API endpoints for AJAX requests
    path('api/gallery/<slug:category_slug>/images/', views.api_gallery_images, name='api_gallery_images'),
    path('api/featured-images/', views.api_featured_images, name='api_featured_images'),
    
    # Class-based views (alternative implementations)
    path('galleries/', views.GalleryListView.as_view(), name='gallery_list_cbv'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 