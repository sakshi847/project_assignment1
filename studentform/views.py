import uuid
from django.shortcuts import render, redirect
from studentform.forms import StudentForm, ParentForm
from .models import Registration
from django.contrib import messages
from datetime import datetime

def initiate_payment(request):
    fee = request.session.get('fee_details')
    if not fee:
        messages.error(request, "No fee data. Please complete review.")
        return redirect('studentform:review_fee')

    registration_id = str(uuid.uuid4())
    request.session['registration_id'] = registration_id

    total = fee['total_fee']
    return redirect(f"/payment/pay/{registration_id}/?amount={total}")

def parent_form_view(request):
    for key in ['parent_data', 'student_data_list', 'fee_details', 'registration_id']:
        request.session.pop(key, None)
    request.session.pop('payment_done', None)  
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            request.session['parent_data'] = form.cleaned_data
            return redirect('studentform:student_form')
    else:
        form = ParentForm()
    return render(request, 'studentform/parent_form.html', {'form': form})


def student_form_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student_data = form.cleaned_data
            student_data['dob'] = student_data['dob'].isoformat() 

            student_list = request.session.get('student_data_list', [])

            
            for existing_student in student_list:
                if (existing_student['student_name'].strip().lower() == student_data['student_name'].strip().lower() and
                    existing_student['dob'] == student_data['dob'] and
                    existing_student['exam'] == student_data['exam']):
                    from django.contrib import messages
                    messages.error(request, "This student has already been registered for the same exam.")
                    return redirect('studentform:student_form')

            # If not duplicate, add
            student_list.append(student_data)
            request.session['student_data_list'] = student_list

            if 'add_another' in request.POST:
                messages.success(request, "Student added successfully. You can add another.")
                return redirect('studentform:student_form')
            else:
                return redirect('studentform:review_fee')
    else:
        form = StudentForm()
    return render(request, 'studentform/student_form.html', {'form': form})


def review_fee_view(request):
    if request.session.get('payment_done'):
        messages.info(request, "Payment has already been completed.")
        return redirect('payment:payment_success')

    parent_data = request.session.get('parent_data')
    student_list = request.session.get('student_data_list', [])

    if not parent_data or not student_list:
        messages.error(request, "Session expired or no student added.")
        return redirect('studentform:parent_form')
    
    if request.session.get('payment_done'):
        messages.success(request, "You have already completed payment.")


    exam_fees = {
    'Unit Test 1': 200,
    'Unit Test 2': 200,
    'Periodic Test 1': 250,
    'Periodic Test 2': 250,
    'Mid-Term Exam': 500,
    'Half-Yearly Exam': 600,
    'Pre-Mid Term Exam': 550,
    'Pre-Board Exam 1': 700,
    'Pre-Board Exam 2': 700,
    'Final Exam': 800,
    'Annual Exam': 800,
    'Board Practice Exam': 900,
    'Board Final Exam': 1000,
    'Practical Exam': 300,
    'Olympiad Exam': 500,
    'NTSE Level 1': 400,
    'Science Talent Exam': 350,
    'Math Olympiad': 350,
    'Foundation Exam (NEET/JEE)': 1200,
    'Competitive Exam Mock Test': 600,
    'JEE': 1200,
    'NEET': 1300,
    'CUET': 1000,
    'Olympiad': 500
}
    fee_details = []
    total_fee = 0
    total_tax = 0

    for student in student_list:
        base = exam_fees.get(student['exam'], 1000)
        tax = round(base * 0.18, 2)
        total = round(base + tax, 2)
        total_fee += total
        total_tax += tax

        fee_details.append({
            'student': student,
            'base': base,
            'tax': tax,
            'total': total
        })

    request.session['fee_details'] = {
        'all_students': fee_details,
        'total_fee': round(total_fee, 2),
        'total_tax': round(total_tax, 2)
    }

    context = {
        'parent': parent_data,
        'students': fee_details,
        'total_fee': round(total_fee, 2),
        'total_tax': round(total_tax, 2)
    }

    return render(request, 'studentform/review_fee.html', context)

