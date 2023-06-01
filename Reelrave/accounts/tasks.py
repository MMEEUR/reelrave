from django.utils import timezone
from django.core.mail import send_mail
from celery import shared_task
from .models import EmailConfirm, PasswordReset


@shared_task
def send_welcome_email(email: str, username: str):
    "background task to send an welcome email asynchronously"
    
    subject = "Welcome to Reelrave community"
    message = f"Subject: Welcome to the Reelrave Community!\n\n\
                Dear [{username}],\n\n\
                Welcome to the Reelrave community!\
                We're excited to have you on board and can't wait to see what you bring to the table.\n\n\
                As a member of our community, you'll have access to a range of features that will help you \
                discover and share your favorite movies with other movie enthusiasts from around the world.\n\n\
                Whether you're a casual moviegoer or a serious cinephile,\
                Reelrave is the perfect place to connect with like-minded individuals\
                and discover new films that you're sure to love.\n\n\
                We encourage you to explore the site and take advantage of all the features available to you.\
                If you have any questions or need help getting started, our friendly support team is always here to help.\n\n\
                Once again, welcome to the Reelrave community. We look forward to seeing you around!\n\n\
                Best regards,\n\n\
                [Mahdyar Eatemad]\n\n\
                Reelrave Community Manager"        
                
                       
    return send_mail(
        subject,
        message,
        "a@b.com",
        [email],
        fail_silently=False
    )
    
    
@shared_task
def delete_expired_records():
    PasswordReset.objects.filter(expires__lt=timezone.now()).delete()
    EmailConfirm.objects.filter(expires__lt=timezone.now()).delete()