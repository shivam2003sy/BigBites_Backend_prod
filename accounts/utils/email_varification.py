import logging
from celery import shared_task
from accounts.firebaseauth.firebase_authentication import auth as firebase_admin_auth
from django.core.mail import send_mail
from django.conf import settings

# Create a logger
logger = logging.getLogger(__name__)

# @shared_task()
def generate_custom_email_from_firebase(user_email, display_name):
    try:
        action_code_settings = firebase_admin_auth.ActionCodeSettings(
            url='http://bigbites-87cdf.web.app',
            handle_code_in_app=True,
        )
        custom_verification_link = firebase_admin_auth.generate_email_verification_link(user_email, action_code_settings)
        subject = 'Verify your email address'
        message = f'Hello {display_name},\n\nPlease verify your email address by clicking on the link below:\n\n{custom_verification_link}\n\nThanks,\nYour website team'
        send_email(subject, message, user_email)
        logger.info("Email sent successfully")
        return "Email sent successfully"
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise

# send email using django send_mail
def send_email(subject, message, user_email):
    logger.info('Sending email to %s from %s', user_email, settings.EMAIL_HOST_USER)
    from_email = settings.EMAIL_HOST_USER
    recipient = user_email
    send_mail(subject, message, from_email, [recipient], fail_silently=False)
