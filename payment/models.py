import uuid
from django.db import models
from studentform.models import Registration

class PaymentDetail(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE) 

    amount_paid = models.FloatField()
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

    def __str__(self):
        if self.registration:
            return f"{self.registration.parent_name} - {self.registration.student_name} - ₹{self.amount_paid}"
        return f"Payment ID: {self.id} (No registration linked)"
