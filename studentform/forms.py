from django import forms
from django.core.exceptions import ValidationError
import re
import datetime

class ParentForm(forms.Form):
    RELATIONSHIP_CHOICES = [
        ('', '-- Select Relation --'),
        ('Parent', 'Parent'),
        ('Guardian', 'Guardian'),
        ('Other', 'Other')
    ]

    parent_name = forms.CharField(
        max_length=100,
        label="Parent/Guardian Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    relation = forms.ChoiceField(
        choices=RELATIONSHIP_CHOICES,
        label="Relation to Student",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    parent_email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    parent_mobile = forms.CharField(
        max_length=10,
        label="Mobile Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': r'[6-9]\d{9}',
            'title': 'Enter a valid 10-digit Indian mobile number',
            'placeholder': 'e.g., 9876543210'
        })
    )

    alt_mobile = forms.CharField(
        max_length=10,
        required=False,
        label="Alternate Mobile Number (Optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': r'[6-9]\d{9}',
            'title': 'Enter a valid 10-digit Indian mobile number if provided'
        })
    )

    address_line1 = forms.CharField(
        label="Address Line 1 (House No, Street)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address_line2 = forms.CharField(
        label="Address Line 2 (Locality/Area)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    state = forms.CharField(
        label="State",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    pincode = forms.CharField(
        label="Pincode",
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': r'\d{6}'})
    )

    def clean_parent_mobile(self):
        number = self.cleaned_data.get('parent_mobile')
        if not re.match(r'^[6-9]\d{9}$', number):
            raise forms.ValidationError("Enter a valid 10-digit Indian mobile number.")
        return number

    def clean_alt_mobile(self):
        alt_number = self.cleaned_data.get('alt_mobile')
        if alt_number and not re.match(r'^[6-9]\d{9}$', alt_number):
            raise forms.ValidationError("Alternate number must be a valid 10-digit Indian number.")
        return alt_number

class StudentForm(forms.Form):
    student_name = forms.CharField(label="Student Name", max_length=100)
    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(
        label="Gender",
        choices=[('', '-- Select Gender --'), ('Male', 'Male'), ('Female', 'Female')]
    )
    standard = forms.ChoiceField(
        label="Current Standard",
        choices=[('', '-- Select Standard --')] + [(str(i), f"Std {i}") for i in range(1, 13)]
    )

    exam = forms.ChoiceField(
        label="Exam Applying For",
        choices=[
            ('', '-- Select Exam --'),
            ('Unit Test 1', 'Unit Test 1'),
            ('Unit Test 2', 'Unit Test 2'),
            ('Mid-Term Exam', 'Mid-Term Exam'),
            ('Final Exam', 'Final Exam'),
            ('Board Practice Exam', 'Board Practice Exam'),
            ('Board Final Exam', 'Board Final Exam'),
            ('Practical Exam', 'Practical Exam'),
            ('Olympiad Exam', 'Olympiad Exam'),
            ('Science Talent Exam', 'Science Talent Exam'),
            ('Math Olympiad', 'Math Olympiad'),
            ('Competitive Exam Mock Test', 'Competitive Exam Mock Test'),
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        standard = cleaned_data.get('standard')

        if dob and standard:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            try:
                std = int(standard)
                expected_age = std + 4
                if age < expected_age:
                    raise ValidationError(f"The age ({age}) is too low for Std {std}. Minimum expected age: {expected_age} years.")
            except ValueError:
                pass  
