from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('visitor-entry/<int:property_id>/', views.visitor_entry, name='visitor_entry'),
    path('approve/<int:entry_id>/', views.approve_entry, name='approve_entry'),
    path('check-status/<int:entry_id>/', views.check_status, name='check_status'),
    path('request-approved/', render, {'template_name': 'request_approved.html'}, name='request_approved'),
    path('request-rejected/', render, {'template_name': 'request_rejected.html'}, name='request_rejected'),
]