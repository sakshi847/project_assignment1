from django.contrib import admin
from .models import OTPModel

@admin.register(OTPModel)
class OTPModelAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'otp', 'created_at', 'resend_count')
    search_fields = ('mobile',)
    list_filter = ('created_at',)
