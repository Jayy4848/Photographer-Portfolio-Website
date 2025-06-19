from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core.validators import MinLengthValidator, RegexValidator
from datetime import datetime

class Category(models.Model):
    """Model for photo categories like Wedding, Birthday, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    cover_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    # Image specs for different sizes
    cover_thumbnail = ImageSpecField(
        source='cover_image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 85}
    )
    
    cover_large = ImageSpecField(
        source='cover_image',
        processors=[ResizeToFit(1200, 800)],
        format='JPEG',
        options={'quality': 90}
    )
    
    order = models.PositiveIntegerField(default=0, help_text="Order of appearance on the website")
    is_featured = models.BooleanField(default=False, help_text="Display in featured section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gallery_detail', kwargs={'slug': self.slug})

    @property
    def image_count(self):
        return self.images.count()


class GalleryImage(models.Model):
    """Model for individual gallery images"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='galleries/')
    
    # Multiple image sizes for responsive design
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80}
    )
    
    medium = ImageSpecField(
        source='image',
        processors=[ResizeToFit(800, 600)],
        format='JPEG',
        options={'quality': 85}
    )
    
    large = ImageSpecField(
        source='image',
        processors=[ResizeToFit(1920, 1080)],
        format='JPEG',
        options={'quality': 90}
    )
    
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False, help_text="Display in hero section or featured galleries")
    date_taken = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.category.name} - {self.title or f'Image {self.id}'}"


class Testimonial(models.Model):
    """Model for client testimonials"""
    client_name = models.CharField(max_length=100)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    
    client_photo_thumbnail = ImageSpecField(
        source='client_photo',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 85}
    )
    
    testimonial_text = models.TextField()
    event_type = models.CharField(max_length=100, blank=True, help_text="e.g., Wedding, Birthday")
    event_date = models.DateField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.event_type}"

    @property
    def star_range(self):
        return range(self.rating)

    @property
    def empty_star_range(self):
        return range(5 - self.rating)


class ContactSubmission(models.Model):
    """Model for contact form submissions and booking requests"""
    INQUIRY_TYPES = [
        ('wedding', 'Wedding Photography'),
        ('reception', 'Reception Photography'),
        ('birthday', 'Birthday Party'),
        ('corporate', 'Corporate Event'),
        ('baby_shower', 'Baby Shower'),
        ('pre_wedding', 'Pre-wedding Shoot'),
        ('other', 'Other Event'),
        ('general', 'General Inquiry'),
    ]
    
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    event_date = models.DateField(blank=True, null=True)
    event_location = models.CharField(max_length=200, blank=True)
    guest_count = models.PositiveIntegerField(blank=True, null=True, help_text="Approximate number of guests")
    budget_range = models.CharField(max_length=50, blank=True, help_text="Your budget range")
    message = models.TextField()
    
    # Admin fields
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()}"

    @property
    def is_booking_request(self):
        return self.event_date is not None


class SiteSettings(models.Model):
    """Model for site-wide settings"""
    photographer_name = models.CharField(max_length=100, default="Professional Photographer")
    tagline = models.CharField(max_length=200, default="Capturing Life's Beautiful Moments")
    about_text = models.TextField(default="Professional photographer with years of experience...")
    
    # Contact Information
    email = models.EmailField(default="contact@photographer.com")
    phone = models.CharField(max_length=20, default="+1234567890")
    address = models.TextField(default="123 Photography St, City, State 12345")
    working_hours = models.CharField(max_length=100, default="Mon-Sat: 9AM-6PM")
    
    # Social Media
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # Hero Section
    hero_video = models.FileField(upload_to='hero/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_title = models.CharField(max_length=200, default="Professional Photography")
    hero_subtitle = models.CharField(max_length=300, default="Creating timeless memories through the lens")
    
    # SEO
    meta_title = models.CharField(max_length=60, default="Professional Photography Services")
    meta_description = models.CharField(max_length=160, default="Professional photography for weddings, events, and special occasions.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('There can be only one SiteSettings instance')
        return super().save(*args, **kwargs)


class Award(models.Model):
    """Model for photographer awards and achievements"""
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='awards/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-year', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.year}"
