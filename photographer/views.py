from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.core.mail import send_mail
from django.conf import settings

from .models import Category, GalleryImage, Testimonial, ContactSubmission, SiteSettings, Award
from .forms import ContactForm


def get_site_settings():
    """Helper function to get or create site settings"""
    settings, created = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'photographer_name': 'Professional Photographer',
            'tagline': 'Capturing Life\'s Beautiful Moments',
            'about_text': 'Professional photographer with years of experience capturing precious moments.',
        }
    )
    return settings


def home(request):
    """Homepage with hero section and featured content"""
    site_settings = get_site_settings()
    featured_categories = Category.objects.filter(is_featured=True)[:6]
    featured_images = GalleryImage.objects.filter(is_featured=True)[:8]
    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    recent_awards = Award.objects.all()[:4]
    
    # Get random images for hero carousel if no featured images
    if not featured_images.exists():
        featured_images = GalleryImage.objects.order_by('?')[:8]
    
    context = {
        'site_settings': site_settings,
        'featured_categories': featured_categories,
        'featured_images': featured_images,
        'featured_testimonials': featured_testimonials,
        'recent_awards': recent_awards,
        'page_title': 'Home',
    }
    
    return render(request, 'photographer/home.html', context)


def gallery_list(request):
    """Gallery categories listing page"""
    categories = Category.objects.all()
    site_settings = get_site_settings()
    
    context = {
        'categories': categories,
        'site_settings': site_settings,
        'page_title': 'Gallery',
    }
    
    return render(request, 'photographer/gallery_list.html', context)


def gallery_detail(request, slug):
    """Individual gallery category page with images"""
    category = get_object_or_404(Category, slug=slug)
    images = category.images.all()
    
    # Pagination
    paginator = Paginator(images, 12)  # Show 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    site_settings = get_site_settings()
    all_categories = Category.objects.all()[:8]  # Limit to 8 related categories
    
    context = {
        'category': category,
        'images': page_obj,
        'all_categories': all_categories,
        'site_settings': site_settings,
        'page_title': f'{category.name} Gallery',
    }
    
    return render(request, 'photographer/gallery_detail.html', context)


def about(request):
    """About page with photographer information"""
    site_settings = get_site_settings()
    awards = Award.objects.all()
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    
    context = {
        'site_settings': site_settings,
        'awards': awards,
        'testimonials': testimonials,
        'page_title': 'About',
    }
    
    return render(request, 'photographer/about.html', context)


def testimonials(request):
    """Testimonials page"""
    testimonials_list = Testimonial.objects.all()
    
    # Pagination
    paginator = Paginator(testimonials_list, 6)  # Show 6 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    site_settings = get_site_settings()
    
    context = {
        'testimonials': page_obj,
        'site_settings': site_settings,
        'page_title': 'Testimonials',
    }
    
    return render(request, 'photographer/testimonials.html', context)


def contact(request):
    """Contact page with form"""
    site_settings = get_site_settings()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_submission = form.save()
            
            # Send email notifications
            try:
                # Email to photographer
                photographer_subject = f'New Booking Request from {contact_submission.name}'
                photographer_message = f"""
New booking request received:

Name: {contact_submission.name}
Email: {contact_submission.email}
Phone: {contact_submission.phone}
Event Type: {contact_submission.event_type}
Event Date: {contact_submission.event_date}
Event Location: {contact_submission.event_location}
Budget: {contact_submission.budget}

Message:
{contact_submission.message}

Submitted on: {contact_submission.created_at.strftime('%B %d, %Y at %I:%M %p')}

Please contact the client to confirm the booking.
                """
                
                send_mail(
                    photographer_subject,
                    photographer_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [site_settings.email],
                    fail_silently=False,
                )
                
                # Email to client
                client_subject = f'Booking Request Confirmation - {site_settings.photographer_name}'
                client_message = f"""
Dear {contact_submission.name},

Thank you for your interest in our photography services! We have received your booking request for {contact_submission.event_type}.

Booking Details:
- Event Type: {contact_submission.event_type}
- Event Date: {contact_submission.event_date}
- Location: {contact_submission.event_location}
- Budget: {contact_submission.budget}

We will review your request and get back to you within 24 hours to discuss the details and confirm your booking.

If you have any urgent questions, please feel free to contact us:
- Phone: {site_settings.phone}
- Email: {site_settings.email}
- WhatsApp: {site_settings.whatsapp_number}

Best regards,
{site_settings.photographer_name}
{site_settings.tagline}
                """
                
                send_mail(
                    client_subject,
                    client_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_submission.email],
                    fail_silently=False,
                )
                
                success_message = 'Thank you for your booking request! Confirmation emails have been sent to both you and our photographer. We will contact you within 24 hours.'
                
            except Exception as e:
                # Log the error but don't fail the form submission
                print(f"Email sending failed: {e}")
                success_message = 'Thank you for your booking request! We have received your information and will contact you soon.'
            
            messages.success(request, success_message)
            
            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': success_message
                })
            
            return redirect('photographer:contact')
        else:
            # If it's an AJAX request, return JSON with errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'site_settings': site_settings,
        'page_title': 'Contact',
    }
    
    return render(request, 'photographer/contact.html', context)


def search(request):
    """Search functionality for images and categories"""
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # Search in categories
        categories = Category.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
        # Search in images
        images = GalleryImage.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(category__name__icontains=query)
        )
        
        results = {
            'categories': categories,
            'images': images,
            'query': query,
        }
    
    site_settings = get_site_settings()
    
    context = {
        'results': results,
        'query': query,
        'site_settings': site_settings,
        'page_title': f'Search Results for "{query}"' if query else 'Search',
    }
    
    return render(request, 'photographer/search.html', context)


# API Views for AJAX requests
@csrf_exempt
def api_gallery_images(request, category_slug):
    """API endpoint to get gallery images for a category (for AJAX loading)"""
    if request.method == 'GET':
        category = get_object_or_404(Category, slug=category_slug)
        images = category.images.all()
        
        images_data = []
        for image in images:
            images_data.append({
                'id': image.id,
                'title': image.title,
                'description': image.description,
                'thumbnail': image.thumbnail.url if hasattr(image, 'thumbnail') else image.image.url,
                'medium': image.medium.url if hasattr(image, 'medium') else image.image.url,
                'large': image.large.url if hasattr(image, 'large') else image.image.url,
                'location': image.location,
                'date_taken': image.date_taken.isoformat() if image.date_taken else None,
            })
        
        return JsonResponse({
            'success': True,
            'category': {
                'name': category.name,
                'description': category.description,
            },
            'images': images_data
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def api_featured_images(request):
    """API endpoint to get featured images"""
    if request.method == 'GET':
        featured_images = GalleryImage.objects.filter(is_featured=True)[:10]
        
        images_data = []
        for image in featured_images:
            images_data.append({
                'id': image.id,
                'title': image.title,
                'category': image.category.name,
                'thumbnail': image.thumbnail.url if hasattr(image, 'thumbnail') else image.image.url,
                'medium': image.medium.url if hasattr(image, 'medium') else image.image.url,
                'large': image.large.url if hasattr(image, 'large') else image.image.url,
            })
        
        return JsonResponse({
            'success': True,
            'images': images_data
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Custom 404 and 500 error views
def custom_404(request, exception):
    """Custom 404 error page"""
    site_settings = get_site_settings()
    return render(request, 'photographer/404.html', {
        'site_settings': site_settings,
        'page_title': 'Page Not Found'
    }, status=404)


def custom_500(request):
    """Custom 500 error page"""
    site_settings = get_site_settings()
    return render(request, 'photographer/500.html', {
        'site_settings': site_settings,
        'page_title': 'Server Error'
    }, status=500)


# Class-based views for more complex functionality
class GalleryListView(ListView):
    """Class-based view for gallery listing with filtering"""
    model = Category
    template_name = 'photographer/gallery_list.html'
    context_object_name = 'categories'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = get_site_settings()
        context['page_title'] = 'Gallery'
        return context


class ImageDetailView(DetailView):
    """Detail view for individual images (for lightbox or dedicated pages)"""
    model = GalleryImage
    template_name = 'photographer/image_detail.html'
    context_object_name = 'image'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = get_site_settings()
        context['page_title'] = self.object.title or f"{self.object.category.name} Image"
        
        # Get related images from same category
        context['related_images'] = GalleryImage.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:6]
        
        return context
