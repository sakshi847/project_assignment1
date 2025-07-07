from django.db import models
from django.utils import timezone

class OTPModel(models.Model):
    mobile = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    resend_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.mobile} - {self.otp}"
