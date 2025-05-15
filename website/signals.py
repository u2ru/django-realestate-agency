from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import HomePageContent, AboutUsContent


@receiver(pre_save, sender=HomePageContent)
def delete_old_hero_image(sender, instance, **kwargs):
    """Delete the old hero image when a new one is uploaded"""
    if not instance.pk:  # Skip for new instances
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.hero_image and old_instance.hero_image != instance.hero_image:
            # Delete the old image file
            default_storage.delete(old_instance.hero_image.path)
    except sender.DoesNotExist:
        pass


@receiver(pre_save, sender=AboutUsContent)
def delete_old_about_hero_image(sender, instance, **kwargs):
    """Delete the old hero image when a new one is uploaded for AboutUsContent"""
    if not instance.pk:  # Skip for new instances
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.hero_image and old_instance.hero_image != instance.hero_image:
            # Delete the old image file
            default_storage.delete(old_instance.hero_image.path)
    except sender.DoesNotExist:
        pass
