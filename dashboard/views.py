from django.shortcuts import render, redirect
from studentform.models import Registration

def home(request):
    mobile = request.session.get('mobile')
    if not mobile:
        return redirect('accounts:otp_login')  

    students = Registration.objects.filter(parent_mobile=mobile)
    return render(request, 'dashboard/home.html', {
        'students': students,
        'mobile': mobile
    })

def logout_view(request):
    request.session.flush()  
    return redirect('accounts:otp_login')  
