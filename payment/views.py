from django.shortcuts import render, redirect
from django.contrib import messages
from studentform.models import Registration
from .models import PaymentDetail  
from datetime import datetime
import uuid

def pay(request, registration_id):
    amount = request.GET.get('amount')
    return render(request, 'payment/pay.html', {
        'registration_id': registration_id,
        'amount': amount
    })

def success(request, registration_id):
    return redirect('payment:finalize', registration_id=registration_id)

def cancel(request, registration_id):
    messages.warning(request, "Payment canceled.")
    return redirect('studentform:review_fee')

def finalize(request, registration_id):
    parent = request.session.get('parent_data')
    students = request.session.get('student_data_list', [])
    fee = request.session.get('fee_details')

    if not parent or not students or not fee:
        messages.error(request, "Session expired. Please restart registration.")
        return redirect('studentform:parent_form')

    total_amount = 0
    duplicate_students = []
    registered_count = 0

    for entry in fee['all_students']:
        st = entry['student']
        already_registered = Registration.objects.filter(
            student_name=st['student_name'],
            exam=st['exam'],
            parent_mobile=parent['parent_mobile']
        ).exists()

        if already_registered:
            duplicate_students.append(f"{st['student_name']} - {st['exam']}")
            continue

        # Registration.objects.create(
        #     parent_name     = parent['parent_name'],
        #     parent_email    = parent['parent_email'],
        #     parent_mobile   = parent['parent_mobile'],
        #     relation        = parent['relation'],
        #     address         = parent['address'],
        #     student_name    = st['student_name'],
        #     dob             = datetime.strptime(st['dob'], '%Y-%m-%d').date(),
        #     gender          = st['gender'],
        #     standard        = st['standard'],
        #     exam            = st['exam'],
        #     base_fee        = entry['base'],
        #     tax             = entry['tax'],
        #     total_fee       = entry['total'],
        #     payment_status  = True,
        #     registration_id = registration_id
        # )

        address = f"{parent.get('address_line1', '')}, {parent.get('address_line2', '')}, {parent.get('city', '')}, {parent.get('state', '')} - {parent.get('pincode', '')}"

        Registration.objects.create(
            parent_name     = parent['parent_name'],
            parent_email    = parent['parent_email'],
            parent_mobile   = parent['parent_mobile'],
            relation        = parent['relation'],
            address         = address,
            student_name    = st['student_name'],
            dob             = datetime.strptime(st['dob'], '%Y-%m-%d').date(),
            gender          = st['gender'],
            standard        = st['standard'],
            exam            = st['exam'],
            base_fee        = entry['base'],
            tax             = entry['tax'],
            total_fee       = entry['total'],
            payment_status  = True,
            registration_id = registration_id
        )


        total_amount += entry['total']
        registered_count += 1

    if registered_count > 0:
        reg_obj = Registration.objects.filter(registration_id=registration_id).first()
        if reg_obj:
            PaymentDetail.objects.create(
                registration   = reg_obj,
                amount_paid    = total_amount,
                transaction_id = str(uuid.uuid4())[:12],
                status         = "Success"
            )
            request.session['mobile'] = parent['parent_mobile']


        for key in ['parent_data', 'student_data_list', 'fee_details', 'registration_id']:
            request.session.pop(key, None)

        if duplicate_students:
            messages.warning(request,
                "Some students were already registered and skipped: " +
                ", ".join(duplicate_students)
            )

        messages.success(request, f"Payment successful! {registered_count} student(s) registered.")
        return render(request, 'payment/success.html', {
            'registration_id': registration_id,
            'total': total_amount
        })
      
        

    else:
        messages.warning(request, "Entered student is already registered.")
        return redirect('studentform:review_fee')