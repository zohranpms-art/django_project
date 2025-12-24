from django.contrib import admin
from django.utils.html import format_html
from .models import Property, VisitorEntry

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'property_type', 'owner', 'subscription_active', 'qr_preview')
    list_filter = ('property_type', 'subscription_active')

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="100"/>', obj.qr_code.url)
        return "No QR"
    qr_preview.short_description = 'QR Code'

@admin.register(VisitorEntry)
class VisitorEntryAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'property', 'reason', 'status', 'request_time', 'photo_preview')
    list_filter = ('status', 'reason')

    def photo_preview(self, obj):
        if obj.visitor_photo:
            return format_html('<img src="{}" width="80" height="80" style="border-radius:50%;"/>', obj.visitor_photo.url)
        return "No photo"
    photo_preview.short_description = 'Photo'