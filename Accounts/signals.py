from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.urls import reverse
# from django.conf import settings
# from .models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def send_verification_email(sender, instance, created, **kwargs):
#     if created:  # Only send email on user creation
#         # verification_link = reverse('confirm-email', kwargs={'token': instance.id})
#         verification_link = reverse('account/verify', kwargs={'id': str(instance.id)})
#         verification_url = settings.BASE_URL + verification_link  # Replace BASE_URL with your URL

#         send_mail(
#             'Verify your email',
#             f'Please click the link to verify your email: {verification_url}\n\nNote: Upon clicking the link, You will be redirected to our temporary verification page.\nThen click the PUT button at the bottom right of the page\n\nAfter that, you can now visit https://ikhuku.com/login to sign in.',
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.email],
#             fail_silently=False,
#         )






from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.conf import settings
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created:  # Only send email on user creation
        verification_link = reverse('account_verify', kwargs={'id': str(instance.id)})
        verification_url = settings.BASE_URL + verification_link  # Replace BASE_URL with your URL

        # Rendering the HTML email template
        html_content = render_to_string('Accounts/email_verify.html', {'verification_url': verification_url})
        
        # Sending the HTML email
        subject = 'Verify your email'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.email

        msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
