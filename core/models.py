from django.db import models
from django.conf import settings

class Property(models.Model):
    TYPE_CHOICES = (
        ('bungalow', 'Bungalow/Independent'),
        ('building', 'Apartment Building'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.TextField()
    building_name = models.CharField(max_length=255, blank=True, null=True)
    flat_no = models.CharField(max_length=50, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    subscription_active = models.BooleanField(default=False)

class VisitorEntry(models.Model):
    REASON_CHOICES = (
        ('delivery', 'Delivery'), ('guest', 'Guest'), ('service', 'Service'),
        ('family', 'Family'), ('meeting', 'Meeting'), ('other', 'Other')
    )
    STATUS_CHOICES = (('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'))
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=255)
    visitor_phone = models.CharField(max_length=20)
    visitor_photo = models.ImageField(upload_to='visitors/')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    other_reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_time = models.DateTimeField(auto_now_add=True)