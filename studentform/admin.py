from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'exam', 'parent_name', 'parent_mobile', 'payment_status', 'submitted_at')
    search_fields = ('student_name', 'parent_name', 'exam')
    list_filter = ('exam', 'payment_status')

