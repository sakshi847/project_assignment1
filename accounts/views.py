from django.shortcuts import render, redirect
from django.contrib import messages
import random
import datetime
from django.contrib.messages import get_messages
from .models import OTPModel

def otp_login(request):
    mobile = ""  
    now = datetime.datetime.now()

    if request.method == 'GET':
        _ = list(get_messages(request))  # Clear old messages

    if request.method == 'POST':
        mobile_input = request.POST.get('mobile', '').strip()
        request.session['otp_mobile'] = mobile_input
        mobile = mobile_input

        if not mobile_input.isdigit() or len(mobile_input) != 10 or mobile_input[0] not in "6789":
            messages.error(request, "Enter a valid Indian 10-digit mobile number starting with 6, 7, 8, or 9.")
            return redirect('accounts:otp_login')

        entered_otp = request.POST.get('otp')
        generate = 'generate' in request.POST
        resend = 'resend' in request.POST

        block_dict = request.session.get('block_dict', {})
        if mobile_input in block_dict:
            block_time = datetime.datetime.fromisoformat(block_dict[mobile_input])
            if now < block_time:
                mins = int((block_time - now).total_seconds() // 60)
                messages.error(request, f"{mobile_input} is blocked. Try again after {mins} minutes.")
                return redirect('accounts:otp_login')

        
        if generate or resend:
            rd = request.session.get('resend_dict', {})
            rc = rd.get(mobile_input, 0)
            if rc < 3:
                otp = str(random.randint(100000, 999999))
                request.session['otp'] = otp
                request.session['mobile_session'] = mobile_input
                request.session['otp_generated_at'] = now.isoformat()
                rd[mobile_input] = rc + 1
                request.session['resend_dict'] = rd
                left = 3 - rd[mobile_input]

                OTPModel.objects.update_or_create(
                    mobile=mobile_input,
                    defaults={'otp': otp, 'resend_count': rd[mobile_input]}
                )

                messages.success(request, f"(Test) OTP sent to {mobile_input}. {left} resend(s) left.")
                print(f"OTP for {mobile_input} = {otp}")
            else:
                block_until = now + datetime.timedelta(hours=24)
                block_dict[mobile_input] = block_until.isoformat()
                request.session['block_dict'] = block_dict
                messages.error(request, "Max 3 resends used. Blocked for 24 hours.")
            return redirect('accounts:otp_login')

        if entered_otp:
            sess_otp = request.session.get('otp')
            sess_mob = request.session.get('mobile_session')
            attempts_dict = request.session.get('attempts_dict', {})
            attempts = attempts_dict.get(mobile_input, 0)
            
            otp_generated_at = request.session.get('otp_generated_at')
            if otp_generated_at:
                otp_time = datetime.datetime.fromisoformat(otp_generated_at)
                if (now - otp_time).total_seconds() > 45:
                    messages.error(request, "OTP expired. Please generate a new one.")
                    return redirect('accounts:otp_login')    
            

            if entered_otp == sess_otp and mobile_input == sess_mob:
                
                messages.success(request, "OTP verified successfully.")
                for key in ['attempts_dict', 'resend_dict', 'block_dict', 'otp_mobile', 'otp', 'mobile_session', 'otp_generated_at']:
                    request.session.pop(key, None)
                request.session['mobile'] = mobile_input  # required for dashboard
                return redirect('studentform:parent_form')
            else:
                attempts += 1
                attempts_dict[mobile_input] = attempts
                request.session['attempts_dict'] = attempts_dict
                left = 3 - attempts
                if attempts >= 3:
                    block_until = now + datetime.timedelta(hours=24)
                    block_dict[mobile_input] = block_until.isoformat()
                    request.session['block_dict'] = block_dict
                    messages.error(request, "Too many invalid OTPs. Blocked for 24 hours.")
                else:
                    messages.error(request, f"Invalid OTP. {left} attempt(s) left.")
                return redirect('accounts:otp_login')

    mobile = request.session.get('otp_mobile', '')
    rd = request.session.get('resend_dict', {})
    rc = rd.get(mobile, 0)
    remaining = max(0, 3 - rc)

    otp_generated_at = request.session.get('otp_generated_at')
    otp_generated = bool(otp_generated_at)

    return render(request, 'accounts/otp_login.html', {
        'mobile': mobile,
        'resend_count': rc,
        'remaining_resends': remaining,
        'otp_generated': otp_generated,
        'otp_generated_at': otp_generated_at
    })

