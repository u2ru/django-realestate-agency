from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from .constants import SUPPORTED_LANGUAGES, PRIMARY_LANGUAGE, CITY_CHOICES
from django.utils import translation

# Property specifications
PROPERTY_TYPE_CHOICES = [
    ("APARTMENT", "Apartment"),
    ("HOUSE", "House"),
    ("COMMERCIAL", "Commercial"),
    ("LAND", "Land"),
]

PRICE_TYPE_CHOICES = [
    ("HIGH", "High"),
    ("LOW", "Low"),
    ("MEDIUM", "Medium"),
]

DEAL_TYPE_CHOICES = [
    ("SALE", "For Sale"),
    ("RENT", "For Rent"),
]

FEATURE_CHOICES = [
    ("balcony", "Balcony"),
    ("parking", "Parking"),
    ("elevator", "Elevator"),
    ("furniture", "Furniture"),
    ("central_heating", "Central Heating"),
]


# Create your models here.
class PropertyFeature(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)

    def __str__(self):
        return self.display_name

    class Meta:
        ordering = ["display_name"]


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
    price_type = models.CharField(
        max_length=10, choices=PRICE_TYPE_CHOICES, default="LOW"
    )
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

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)

    deal_type = models.CharField(max_length=10, choices=DEAL_TYPE_CHOICES)

    RENT_PERIOD_CHOICES = [
        ("month", "Month"),
        ("week", "Week"),
        ("day", "Day"),
    ]
    rent_period = models.CharField(
        max_length=10,
        choices=RENT_PERIOD_CHOICES,
        blank=True,
        null=True,
        default="month",
        help_text="Applicable only if deal type is RENT",
    )

    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    total_rooms = models.PositiveIntegerField(null=True, blank=True)
    area = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Area in square meters"
    )
    floor = models.PositiveIntegerField(null=True, blank=True)
    coordinates = models.JSONField(
        null=True,
        blank=True,
        help_text="Property coordinates in format {'lat': float, 'lng': float}",
    )

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
    features = models.JSONField(
        default=list,
        blank=True,
        help_text="List of features that apply to the property (e.g., ['balcony', 'parking', 'elevator'])",
    )

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

    def get_youtube_url(self):
        if self.youtube_url:
            get_id = self.youtube_url.split("=")[1][:11]
            return f"https://www.youtube.com/embed/{get_id}?autoplay=1&mute=1"
        return None

    def get_main_image(self):
        """Returns the main image URL or None if no images exist"""
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image.url
        # If no main image is set, return the first image
        first_image = self.images.first()
        return first_image.image.url if first_image else None

    def get_images(self):
        return self.images.all()

    def __str__(self):
        return self.name

    def get_translation(self, field, language=None):
        if language is None:
            language = translation.get_language()
        try:
            translation_obj = self.translations.get(language=language)
            return getattr(translation_obj, field)
        except PropertyTranslation.DoesNotExist:
            # fallback to default language
            try:
                translation_obj = self.translations.get(language=PRIMARY_LANGUAGE)
                return getattr(translation_obj, field)
            except PropertyTranslation.DoesNotExist:
                return getattr(self, field, "")

    @property
    def price_per_area(self):
        if self.area:
            return f"{round(self.price / self.area, 2)} {self.currency}/m²"
        return None


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
