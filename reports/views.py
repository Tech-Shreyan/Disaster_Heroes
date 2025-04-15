from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Report, sanitize_input
from .forms import UserRegistrationForm, LoginForm, ReportForm
import json

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Form validation already takes care of sanitizing
            user = form.save()
            login(request, user)
            messages.success(request, "Registered successfully")
            return redirect('report_list')
        else:
            # Form is not valid, render the form with errors
            return render(request, 'reports/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'reports/register.html', {'form': form})

def register_api(request):
    """API endpoint for user registration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create a user form from the data
            form = UserRegistrationForm({
                'username': data.get('username', ''),
                'email': data.get('email', ''),
                'password1': data.get('password', ''),
                'password2': data.get('password', ''),  # Assuming same password
                'phone': data.get('phone', '')
            })
            
            if form.is_valid():
                user = form.save()
                return JsonResponse({"message": "Registered successfully"}, status=201)
            else:
                # Return form errors
                return JsonResponse({"error": form.errors}, status=400)
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Get user by email
            try:
                user = User.objects.get(email=email)
                # Authenticate with username (Django's default)
                user = authenticate(username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, "Login successful")
                    return redirect('report_list')
                else:
                    messages.error(request, "Invalid credentials")
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials")
                
        return render(request, 'reports/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'reports/login.html', {'form': form})

def login_api(request):
    """API endpoint for user login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            password = data.get('password', '')
            
            try:
                user = User.objects.get(email=email)
                # Authenticate with username (Django's default)
                user = authenticate(username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        "message": "Login successful",
                        "user": user.to_dict()
                    }, status=200)
                else:
                    return JsonResponse({"error": "Invalid credentials"}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

def report_list(request):
    """View to display all reports"""
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})

def report_api(request):
    """API endpoint to get all reports"""
    if request.method == 'GET':
        try:
            reports = Report.objects.all().order_by('-created_at')
            return JsonResponse([report.to_dict() for report in reports], safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def report_form_view(request):
    """View to display and handle the report submission form"""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            
            # If user is logged in, associate report with user
            if request.user.is_authenticated:
                report.user = request.user
                
            report.save()
            messages.success(request, "Report submitted successfully")
            return redirect('report_list')
        else:
            return render(request, 'reports/report_form.html', {'form': form})
    else:
        form = ReportForm()
        return render(request, 'reports/report_form.html', {'form': form})

def submit_report_api(request):
    """API endpoint for report submission"""
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()
            
            # Make a copy of data to avoid modifying the original
            form_data = data.copy()
            
            # Handle categories
            if 'categories' in data:
                if data['categories'] is None:
                    # Handle null categories
                    form_data['categories'] = []
                elif isinstance(data['categories'], list):
                    # Keep as list for the form to process
                    form_data['categories'] = data['categories']
                elif isinstance(data['categories'], str):
                    # Handle comma-separated string
                    if data['categories']:
                        form_data['categories'] = [c.strip() for c in data['categories'].split(',')]
                    else:
                        form_data['categories'] = []
            
            form = ReportForm(form_data)
            if form.is_valid():
                report = form.save(commit=False)
                
                # If user is logged in, associate report with user
                if request.user.is_authenticated:
                    report.user = request.user
                    
                report.save()
                return JsonResponse({"message": "Report submitted successfully"}, status=201)
            else:
                return JsonResponse({"error": form.errors}, status=400)
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

# Create your views here.
