from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from .constants import SUPPORTED_LANGUAGES, PRIMARY_LANGUAGE, CITY_CHOICES


# Create your models here.
class Property(models.Model):
    name = models.CharField(
        max_length=200,
        help_text=f"Name in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    description = models.TextField(
        help_text=f"Description in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}"
    )

    # Price and currency
    CURRENCY_CHOICES = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GEL", "Georgian Lari"),
    ]
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")

    # Location details
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    property_id = models.CharField(max_length=100)

    # Media
    youtube_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="YouTube video URL for property showcase",
    )

    # Property specifications
    PROPERTY_TYPE_CHOICES = [
        ("APARTMENT", "Apartment"),
        ("HOUSE", "House"),
        ("COMMERCIAL", "Commercial"),
        ("LAND", "Land"),
    ]
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)

    DEAL_TYPE_CHOICES = [
        ("SALE", "For Sale"),
        ("RENT", "For Rent"),
    ]
    deal_type = models.CharField(max_length=10, choices=DEAL_TYPE_CHOICES)

    rooms = models.PositiveIntegerField(null=True, blank=True)
    area = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Area in square meters"
    )
    floor = models.PositiveIntegerField(null=True, blank=True)
    total_floors = models.PositiveIntegerField(null=True, blank=True)

    STATE_CHOICES = [
        ("NEW", "New"),
        ("RENOVATED", "Renovated"),
        ("REQUIRES_RENOVATION", "Requires Renovation"),
        ("UNDER_CONSTRUCTION", "Under Construction"),
    ]
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, null=True, blank=True
    )

    # Additional features as checkboxes
    has_balcony = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_furniture = models.BooleanField(default=False)
    has_central_heating = models.BooleanField(default=False)

    # Agent information
    agent_name = models.CharField(
        max_length=100, blank=True, null=True, help_text="Name of the responsible agent"
    )
    agent_phone = models.CharField(
        max_length=50, blank=True, null=True, help_text="Contact number of the agent"
    )

    # Display and status fields
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="properties/%Y/%m/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.name}"

    def get_thumbnail(self, width=150):
        """Get HTML for a thumbnail of specified width"""
        return f'<img src="{self.image.url}" width="{width}" height="auto" />'


class PropertyTranslation(models.Model):
    LANGUAGE_CHOICES = [(key, value) for key, value in SUPPORTED_LANGUAGES.items()]

    property = models.ForeignKey(
        Property, related_name="translations", on_delete=models.CASCADE
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        unique_together = ("property", "language")
        verbose_name = "Property Translation"
        verbose_name_plural = "Property Translations"

    def __str__(self):
        return f"{self.property.name} - {self.get_language_display()}"


# Signal to delete image file when PropertyImage instance is deleted
@receiver(post_delete, sender=PropertyImage)
def auto_delete_image_file_on_delete(sender, instance, **kwargs):
    """Delete the image file when the PropertyImage instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


# Signal to delete old image file when PropertyImage instance is updated with a new image
@receiver(pre_save, sender=PropertyImage)
def auto_delete_image_file_on_change(sender, instance, **kwargs):
    """Delete the old image file when the PropertyImage instance is updated with a new image."""
    if not instance.pk:  # Skip if this is a new instance
        return

    try:
        old_instance = PropertyImage.objects.get(pk=instance.pk)
    except PropertyImage.DoesNotExist:
        return

    # Check if the image has been changed
    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)
