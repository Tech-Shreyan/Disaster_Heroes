from django.urls import path
from . import views

urlpatterns = [
    # Web views
    path('', views.report_list, name='report_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('report/new/', views.report_form_view, name='report_form'),
    
    # API endpoints
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/reports/', views.report_api, name='report_api'),
    path('api/report/submit/', views.submit_report_api, name='submit_report_api'),
]