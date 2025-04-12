from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import re
import html

class User(AbstractUser):
    """Extended user model with additional fields"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.username
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone
        }

class Report(models.Model):
    """Model for disaster reports"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    categories = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    location_landmark = models.CharField(max_length=200, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    news_link = models.URLField(max_length=500, blank=True, null=True)
    media_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Optional: Add a foreign key to link reports to users
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    
    def __str__(self):
        return self.title
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_time': self.date_time.isoformat(),
            'categories': self.categories,
            'location': self.location,
            'location_landmark': self.location_landmark,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'news_link': self.news_link,
            'media_url': self.media_url,
            'created_at': self.created_at.isoformat()
        }

# Helper functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(input_data):
    """Sanitize input to prevent XSS attacks"""
    if isinstance(input_data, str):
        return html.escape(input_data.strip())
    return input_data

