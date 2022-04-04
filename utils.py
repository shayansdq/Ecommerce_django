from django.core.mail import send_mail
from kavenegar import *
from django.conf import settings


def send_otp_code(phone, code):
    try:
        api = KavenegarAPI('706E46774F736F4E5A4967457675656E5349366167336E5A6F7655414A78476438304845775743655441553D')
        params = {
            'sender': '10008663',  # optional
            'receptor': phone,  # multiple mobile number, split by comma
            'message': f'Welcome to ShopiHi: \n\n code: {code}',
        }
        response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_register_email(email, code):
    subject = 'Welcome to ShopiHi World'
    message = f'Hi dear\nWelcome to our shop.\nYou registered successfully with Phone: {customer.user.phone}\n' \
              f'Your code: {code}\n\nBest regards.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)

