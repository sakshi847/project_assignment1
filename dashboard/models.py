from django.shortcuts import render
from payment.models import PaymentDetail
from studentform.models import Registration

def payment_dashboard(request):
    payments = PaymentDetail.objects.all().order_by('-payment_time')

    data = []
    for payment in payments:
        students = Registration.objects.filter(registration_id=payment.registration_id)
        if students.exists():
            parent = students.first()
            for student in students:
                data.append({
                    'parent_name': parent.parent_name,
                    'student_name': student.student_name,
                    'amount_paid': payment.amount_paid,
                    'transaction_id': payment.transaction_id,
                    'payment_time': payment.payment_time,
                })

    return render(request, 'dashboard/payment_dashboard.html', {'data': data})

