from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML, Div
from crispy_forms.bootstrap import PrependedText, AppendedText
from django.core.validators import RegexValidator
from datetime import date, timedelta
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    """Enhanced contact form with crispy forms styling and validation"""
    
    # Override fields for better validation and widgets
    phone = forms.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Please enter a valid phone number (e.g., +1234567890 or 1234567890)"
        )],
        widget=forms.TextInput(attrs={
            'placeholder': '+1234567890',
            'class': 'form-control'
        })
    )
    
    event_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': date.today().isoformat(),
            'max': (date.today() + timedelta(days=365*2)).isoformat()  # 2 years ahead
        }),
        help_text="Select your event date (optional)"
    )
    
    guest_count = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 50'
        }),
        help_text="Approximate number of guests"
    )
    
    budget_range = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., $2000-$5000',
            'class': 'form-control'
        }),
        help_text="Your budget range (optional)"
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Tell us about your event, photography style preferences, and any special requirements...',
            'class': 'form-control'
        }),
        help_text="Please provide details about your photography needs"
    )

    class Meta:
        model = ContactSubmission
        fields = [
            'name', 'email', 'phone', 'inquiry_type', 'event_date',
            'event_location', 'guest_count', 'budget_range', 'message'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com',
                'class': 'form-control'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'event_location': forms.TextInput(attrs={
                'placeholder': 'Event venue or location',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'contact-form'
        self.helper.attrs = {'novalidate': ''}
        
        self.helper.layout = Layout(
            HTML('<div class="form-section">'),
            HTML('<h4 class="form-section-title"><i class="fas fa-user"></i> Contact Information</h4>'),
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-3'),
                Column('inquiry_type', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            HTML('</div>'),
            
            HTML('<div class="form-section">'),
            HTML('<h4 class="form-section-title"><i class="fas fa-calendar-alt"></i> Event Details</h4>'),
            Row(
                Column('event_date', css_class='form-group col-md-6 mb-3'),
                Column('event_location', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('guest_count', css_class='form-group col-md-6 mb-3'),
                Column('budget_range', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            HTML('</div>'),
            
            HTML('<div class="form-section">'),
            HTML('<h4 class="form-section-title"><i class="fas fa-comment"></i> Your Message</h4>'),
            Field('message', css_class='mb-3'),
            HTML('</div>'),
            
            Div(
                Submit('submit', 'Send Message', css_class='btn btn-primary btn-lg btn-block'),
                css_class='text-center mt-4'
            )
        )

    def clean_event_date(self):
        """Validate event date is not in the past"""
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < date.today():
            raise forms.ValidationError("Event date cannot be in the past.")
        return event_date

    def clean_phone(self):
        """Clean and validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove spaces, dashes, and parentheses
            phone = ''.join(char for char in phone if char.isdigit() or char == '+')
        return phone

    def clean(self):
        """Additional form validation"""
        cleaned_data = super().clean()
        inquiry_type = cleaned_data.get('inquiry_type')
        event_date = cleaned_data.get('event_date')
        
        # If it's an event inquiry, suggest providing event date
        if inquiry_type and inquiry_type != 'general' and not event_date:
            self.add_error(
                'event_date',
                "For event inquiries, please provide an event date to help us check availability."
            )
        
        return cleaned_data


class QuickContactForm(forms.Form):
    """Simplified contact form for quick inquiries (e.g., in modals)"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your name',
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email',
            'class': 'form-control'
        })
    )
    
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your phone (optional)',
            'class': 'form-control'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Quick message or question...',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'quick-contact-form'
        
        self.helper.layout = Layout(
            Field('name', css_class='mb-3'),
            Field('email', css_class='mb-3'),
            Field('phone', css_class='mb-3'),
            Field('message', css_class='mb-3'),
            Submit('submit', 'Send Quick Message', css_class='btn btn-primary btn-block')
        )


class NewsletterForm(forms.Form):
    """Newsletter subscription form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email for updates',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'newsletter-form d-flex'
        self.helper.form_show_labels = False
        
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-8'),
                Column(
                    Submit('subscribe', 'Subscribe', css_class='btn btn-outline-light'),
                    css_class='col-4'
                ),
                css_class='g-0'
            )
        )


class SearchForm(forms.Form):
    """Search form for galleries and images"""
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search photos, categories, locations...',
            'class': 'form-control'
        })
    )
    
    category = forms.CharField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'search-form'
        
        # Populate category choices
        from .models import Category
        categories = Category.objects.all()
        category_choices = [('', 'All Categories')] + [(cat.slug, cat.name) for cat in categories]
        self.fields['category'].widget.choices = category_choices
        
        self.helper.layout = Layout(
            Row(
                Column('query', css_class='col-8'),
                Column('category', css_class='col-4'),
                css_class='g-2'
            ),
            Submit('search', 'Search', css_class='btn btn-primary mt-2')
        ) 