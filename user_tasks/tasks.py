from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(email, username):
    subject = "Welcome to Our Platform!"
    message = f"Hello {username},\n\nThank you for joining us!"
    from_email = "noreply@example.com"
    
    send_mail(subject, message, from_email, [email])
    print("Mail Sent Successfully using celery")
    return f"Email sent to {email}"
