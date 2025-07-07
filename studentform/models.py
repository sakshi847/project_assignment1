from django.db import models

class Registration(models.Model):
    parent_name     = models.CharField(max_length=100)
    parent_email    = models.EmailField()
    parent_mobile   = models.CharField(max_length=15)
    relation        = models.CharField(max_length=50)
    address         = models.TextField()

    student_name    = models.CharField(max_length=100)
    dob             = models.DateField()
    gender          = models.CharField(max_length=10)
    standard        = models.CharField(max_length=10)
    exam            = models.CharField(max_length=50)

    base_fee        = models.FloatField()
    tax             = models.FloatField()
    total_fee       = models.FloatField()
    payment_status  = models.BooleanField(default=False)

    registration_id = models.CharField(max_length=36, null=True, blank=True)

    submitted_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.exam}"
