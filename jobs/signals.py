from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ApplicantProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_applicant_profile(sender, instance, created, **kwargs):
    """Auto-create ApplicantProfile when a non-staff user registers."""
    if created and not instance.is_staff and not hasattr(instance, 'applicant_profile'):
        ApplicantProfile.objects.create(user=instance)