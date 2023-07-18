from apps.users.api.v1.serializers import UserDetailSerializer
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserDetailSerializer(instance=user, context={'request': request}).data
    }


def generate_random_digits(length):
    # Generate a secure random number
    secure_random = random.SystemRandom()
    random_number = secure_random.randint(10 ** (length - 1), (10 ** length) - 1)
    return random_number


def send_verification_email(user_email, pin_code):
    subject = 'Verify Your Email'
    template = 'activation.html'
    context = {'pincode': f'{pin_code}'}
    from_email = 'info@inventoryplus.com'
    recipient_list = [user_email]

    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_forgor_password_email(user_email, pin_code):
    subject = 'Forgot Password'
    template = 'forgot_password.html'
    context = {'pincode': f'{pin_code}'}
    from_email = 'info@inventoryplus.com'
    recipient_list = [user_email]

    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
