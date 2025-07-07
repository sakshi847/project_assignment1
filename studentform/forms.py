# studentform/forms.py

from django import forms
from django.core.exceptions import ValidationError
import re

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
            'pattern': r'\d{10}',
            'title': 'Enter a 10-digit number',
            'placeholder': 'e.g., 9876543210'
        })
    )

    alt_mobile = forms.CharField(
        max_length=10,
        required=False,
        label="Alternate Mobile Number (Optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': r'\d{10}',
            'title': 'Enter a 10-digit number if provided'
        })
    )

    address = forms.CharField(
        label="Residential Address",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Street, City, State, ZIP'
        })
    )

    def clean_parent_mobile(self):
        number = self.cleaned_data.get('parent_mobile')
        if not re.match(r'^\d{10}$', number):
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return number

    def clean_alt_mobile(self):
        alt_number = self.cleaned_data.get('alt_mobile')
        if alt_number and not re.match(r'^\d{10}$', alt_number):
            raise forms.ValidationError("Alternate number must be 10 digits.")
        return alt_number



class StudentForm(forms.Form):
    student_name = forms.CharField(label="Student Name", max_length=100)
    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(label="Gender", choices=[('', '-- Select Gender --'),('Male', 'Male'), ('Female', 'Female')])
    standard = forms.ChoiceField(label="Current Standard", choices=[('', '-- Select Standard --')] + [(str(i), f"Std {i}") for i in range(1, 13)])
    exam = forms.ChoiceField(label="Exam Applying For", choices=[
        ('', '-- Select Exam --'),
        ('Unit Test 1', 'Unit Test 1'),
        ('Unit Test 2', 'Unit Test 2'),
        ('Periodic Test 1', 'Periodic Test 1'),
        ('Periodic Test 2', 'Periodic Test 2'),
        ('Mid-Term Exam', 'Mid-Term Exam'),
        ('Half-Yearly Exam', 'Half-Yearly Exam'),
        ('Pre-Mid Term Exam', 'Pre-Mid Term Exam'),
        ('Pre-Board Exam 1', 'Pre-Board Exam 1'),
        ('Pre-Board Exam 2', 'Pre-Board Exam 2'),
        ('Final Exam', 'Final Exam'),
        ('Annual Exam', 'Annual Exam'),
        ('Board Practice Exam', 'Board Practice Exam'),
        ('Board Final Exam', 'Board Final Exam'),
        ('Practical Exam', 'Practical Exam'),
        ('Olympiad Exam', 'Olympiad Exam'),
        ('NTSE Level 1', 'NTSE Level 1'),
        ('Science Talent Exam', 'Science Talent Exam'),
        ('Math Olympiad', 'Math Olympiad'),
        ('Foundation Exam (NEET/JEE)', 'Foundation Exam (NEET/JEE)'),
        ('Competitive Exam Mock Test', 'Competitive Exam Mock Test'),

    ])
