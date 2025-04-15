from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Report, validate_email
import datetime

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
            
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        return email

class ReportForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('flood', 'Flood'),
        ('earthquake', 'Earthquake'),
        ('fire', 'Fire'),
        ('hurricane', 'Hurricane'),
        ('tornado', 'Tornado'),
        ('landslide', 'Landslide'),
        ('other', 'Other')
    ]
    
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    date_time = forms.DateTimeField(
        initial=datetime.datetime.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    location = forms.CharField(max_length=200, required=False)
    location_landmark = forms.CharField(max_length=200, required=False)
    full_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20, required=False)
    news_link = forms.URLField(max_length=500, required=False)
    media_url = forms.URLField(max_length=500, required=False)
    
    class Meta:
        model = Report
        fields = [
            'title', 'description', 'date_time', 'categories',
            'location', 'location_landmark', 'full_name', 'email',
            'phone', 'news_link', 'media_url'
        ]
    
    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories:
            return None  # Return None instead of a default value
        return ','.join(categories)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not validate_email(email):
            raise ValidationError("Invalid email format")
        return email