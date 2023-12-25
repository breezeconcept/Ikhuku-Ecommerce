from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created:  # Only send email on user creation
        verification_link = reverse('confirm-email', kwargs={'token': instance.id})
        verification_url = settings.BASE_URL + verification_link  # Replace BASE_URL with your URL

        send_mail(
            'Verify your email',
            f'Please click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
