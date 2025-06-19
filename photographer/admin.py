from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, GalleryImage, Testimonial, ContactSubmission, SiteSettings, Award


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_count', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_featured']
    ordering = ['order', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'cover_image')
        }),
        ('Display Options', {
            'fields': ('order', 'is_featured'),
            'classes': ('collapse',)
        }),
    )
    
    def image_count(self, obj):
        return obj.image_count
    image_count.short_description = 'Images'


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'title', 'order', 'is_featured', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.thumbnail.url if hasattr(obj, 'thumbnail') else obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'category', 'is_featured', 'order', 'date_taken']
    list_filter = ['category', 'is_featured', 'date_taken', 'created_at']
    search_fields = ['title', 'description', 'location', 'category__name']
    list_editable = ['order', 'is_featured']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('category', 'image', 'title', 'description')
        }),
        ('Details', {
            'fields': ('date_taken', 'location'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('order', 'is_featured'),
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px;" />',
                obj.thumbnail.url if hasattr(obj, 'thumbnail') else obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'event_type', 'rating', 'is_featured', 'event_date']
    list_filter = ['rating', 'is_featured', 'event_type', 'event_date']
    search_fields = ['client_name', 'testimonial_text', 'event_type']
    list_editable = ['is_featured']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_photo', 'event_type', 'event_date')
        }),
        ('Testimonial', {
            'fields': ('testimonial_text', 'rating')
        }),
        ('Display Options', {
            'fields': ('is_featured',),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'event_date', 'is_read', 'is_responded', 'created_at']
    list_filter = ['inquiry_type', 'is_read', 'is_responded', 'event_date', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message', 'event_location']
    list_editable = ['is_read', 'is_responded']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('inquiry_type', 'event_date', 'event_location', 'guest_count', 'budget_range')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Admin Section', {
            'fields': ('is_read', 'is_responded', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_responded']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} submissions marked as read.')
    mark_as_read.short_description = 'Mark selected submissions as read'
    
    def mark_as_responded(self, request, queryset):
        queryset.update(is_responded=True)
        self.message_user(request, f'{queryset.count()} submissions marked as responded.')
    mark_as_responded.short_description = 'Mark selected submissions as responded'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('photographer_name', 'tagline', 'about_text')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'working_hours')
        }),
        ('Social Media', {
            'fields': ('instagram_url', 'facebook_url', 'twitter_url', 'whatsapp_number'),
            'classes': ('collapse',)
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image', 'hero_video'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent adding multiple instances
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the settings
        return False


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'year', 'order']
    list_filter = ['year', 'organization']
    search_fields = ['title', 'organization', 'description']
    list_editable = ['order']
    ordering = ['-year', 'order']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'organization', 'year', 'description', 'image')
        }),
        ('Display Options', {
            'fields': ('order',),
        }),
    )


# Enhanced Admin Site Configuration
admin.site.site_header = "Photography Portfolio Admin"
admin.site.site_title = "Photo Admin"
admin.site.index_title = "Welcome to Photography Portfolio Administration"

# Custom admin views for better dashboard
class PhotographyAdminSite(admin.AdminSite):
    site_header = 'Photography Portfolio Admin'
    site_title = 'Photo Admin'
    index_title = 'Portfolio Management Dashboard'
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Add dashboard statistics
        extra_context.update({
            'total_categories': Category.objects.count(),
            'total_images': GalleryImage.objects.count(),
            'featured_images': GalleryImage.objects.filter(is_featured=True).count(),
            'total_testimonials': Testimonial.objects.count(),
            'unread_contacts': ContactSubmission.objects.filter(is_read=False).count(),
            'recent_contacts': ContactSubmission.objects.filter(is_read=False)[:5],
        })
        
        return super().index(request, extra_context)
