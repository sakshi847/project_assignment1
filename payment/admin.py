from django.contrib import admin
from .models import PaymentDetail

@admin.register(PaymentDetail)
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'amount_paid',
        'status',
        'get_parent_name',
        'get_student_name',
    )
    
    readonly_fields = (
        'registration',
        'amount_paid',
        'transaction_id',
        'status',
        'get_parent_name',
        'get_student_name',
    )

    def get_parent_name(self, obj):
        return obj.registration.parent_name if obj.registration else "—"

    def get_student_name(self, obj):
        return obj.registration.student_name if obj.registration else "—"

    get_parent_name.short_description = "Parent Name"
    get_student_name.short_description = "Student Name"
