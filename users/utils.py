from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created

import variables


def save_refresh(refresh, response):
    response.set_cookie(
        key='refresh',
        value=str(refresh),
        max_age=60 * 60 * 24 * 30,
        expires=refresh.current_time + timedelta(days=30),
        httponly=True,
    )
    return response


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "https://{client_url}/new_password/{token}".format(
            client_url=variables.CLIENT_URL,
            token=reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()