from django.db import models
from property.constants import SUPPORTED_LANGUAGES, PRIMARY_LANGUAGE
from django.utils import translation


# Create your models here.
class HomePageContent(models.Model):
    """Model to store content for the home page"""

    company_name = models.CharField(max_length=200, help_text="Company name")

    # Hero section
    hero_title = models.CharField(
        max_length=200,
        help_text=f"Main headline in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    hero_subtitle = models.TextField(
        blank=True,
        help_text=f"Subtitle text in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    hero_image = models.ImageField(upload_to="homepage/", help_text="Main banner image")

    # properties for sale section
    properties_for_sale_title = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"Properties for sale section title in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    properties_for_sale_subtitle = models.TextField(
        blank=True,
        help_text=f"Properties for sale section subtitle in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )

    # middle section
    middle_section_title = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"Middle section title in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    middle_section_content = models.TextField(
        blank=True,
        help_text=f"Middle section content in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )

    # properties for rent section
    properties_for_rent_title = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"Properties for rent section title in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    properties_for_rent_subtitle = models.TextField(
        blank=True,
        help_text=f"Properties for rent section subtitle in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )

    # Contact information
    contact_phone = models.CharField(
        max_length=50, blank=True, help_text="Contact phone number"
    )
    contact_email = models.EmailField(blank=True, help_text="Contact email address")
    contact_address = models.TextField(blank=True, help_text="Physical address")

    # Social media links
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")

    # Statistics to display
    properties_count = models.PositiveIntegerField(
        default=0, help_text="Number of properties to display"
    )
    years_experience = models.PositiveIntegerField(
        default=0, help_text="Years of experience to display"
    )
    happy_customers = models.PositiveIntegerField(
        default=0, help_text="Number of happy customers to display"
    )

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        return "Home Page Content"

    def save(self, *args, **kwargs):
        # Only allow one instance
        if not self.pk and HomePageContent.objects.exists():
            # If you try to create a second instance, get the first one
            return HomePageContent.objects.first()
        return super().save(*args, **kwargs)

    def get_translation(self, field, language=None):
        if language is None:
            language = translation.get_language()
        try:
            translation_obj = self.translations.get(language=language)
            return getattr(translation_obj, field)
        except HomePageContentTranslation.DoesNotExist:
            # fallback to default language
            try:
                translation_obj = self.translations.get(language=PRIMARY_LANGUAGE)
                return getattr(translation_obj, field)
            except HomePageContentTranslation.DoesNotExist:
                return getattr(self, field, "")


class HomePageContentTranslation(models.Model):
    """Translations for the Home Page Content"""

    LANGUAGE_CHOICES = [(key, value) for key, value in SUPPORTED_LANGUAGES.items()]

    home_page = models.ForeignKey(
        HomePageContent, related_name="translations", on_delete=models.CASCADE
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)

    # Hero section translations
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField(blank=True)

    # About section translations
    middle_section_title = models.CharField(max_length=200, blank=True)
    middle_section_content = models.TextField(blank=True)

    # properties for sale section translations
    properties_for_sale_title = models.CharField(max_length=200, blank=True)
    properties_for_sale_subtitle = models.TextField(blank=True)

    # properties for rent section translations
    properties_for_rent_title = models.CharField(max_length=200, blank=True)
    properties_for_rent_subtitle = models.TextField(blank=True)

    class Meta:
        unique_together = ("home_page", "language")
        verbose_name = "Home Page Translation"
        verbose_name_plural = "Home Page Translations"

    def __str__(self):
        return f"Home Page Content - {self.get_language_display()}"


class AboutUsContent(models.Model):
    """Model to store content for the about us page"""

    # Hero section
    hero_title = models.CharField(
        max_length=200,
        help_text=f"Main headline in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    hero_image = models.ImageField(upload_to="homepage/", help_text="Main banner image")

    # properties for sale section
    main_subtitle = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"Main subtitle in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    main_title = models.TextField(
        blank=True,
        help_text=f"Main title in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    main_content = models.TextField(
        blank=True,
        help_text=f"Main content in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )

    # our services section
    our_services_title = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"Our services title in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    our_services_content = models.TextField(
        blank=True,
        help_text=f"Our services content in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )

    office_location_address = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"Office location address in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    office_coordinates = models.JSONField(
        null=True,
        blank=True,
        help_text="Office coordinates in format {'lat': float, 'lng': float}",
    )

    # bottom section
    bottom_section_title = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"Bottom section title in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    bottom_section_content = models.TextField(
        blank=True,
        help_text=f"Bottom section content in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Us Content"
        verbose_name_plural = "About Us Content"

    def __str__(self):
        return "About Us Content"

    def save(self, *args, **kwargs):
        # Only allow one instance
        if not self.pk and AboutUsContent.objects.exists():
            # If you try to create a second instance, get the first one
            return AboutUsContent.objects.first()
        return super().save(*args, **kwargs)

    def get_translation(self, field, language=None):
        if language is None:
            language = translation.get_language()
        try:
            translation_obj = self.translations.get(language=language)
            return getattr(translation_obj, field)
        except AboutUsContentTranslation.DoesNotExist:
            # fallback to default language
            try:
                translation_obj = self.translations.get(language=PRIMARY_LANGUAGE)
                return getattr(translation_obj, field)
            except AboutUsContentTranslation.DoesNotExist:
                return getattr(self, field, "")


class AboutUsContentTranslation(models.Model):
    """Translations for the About Us Content"""

    LANGUAGE_CHOICES = [(key, value) for key, value in SUPPORTED_LANGUAGES.items()]

    about_us = models.ForeignKey(
        AboutUsContent, related_name="translations", on_delete=models.CASCADE
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)

    # Hero section translations
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField(blank=True)

    # main section translations
    main_subtitle = models.CharField(max_length=200, blank=True)
    main_title = models.TextField(blank=True)
    main_content = models.TextField(blank=True)

    # our services section translations
    our_services_title = models.CharField(max_length=200, blank=True)
    our_services_content = models.TextField(blank=True)

    # bottom section translations
    bottom_section_title = models.CharField(max_length=200, blank=True)
    bottom_section_content = models.TextField(blank=True)

    class Meta:
        unique_together = ("about_us", "language")
        verbose_name = "About Us Translation"
        verbose_name_plural = "About Us Translations"

    def __str__(self):
        return f"About Us Content - {self.get_language_display()}"
