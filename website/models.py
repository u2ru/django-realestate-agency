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

    # About section
    about_title = models.CharField(
        max_length=200,
        blank=True,
        help_text=f"About section title in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    about_content = models.TextField(
        blank=True,
        help_text=f"About section content in {SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]}",
    )
    about_image = models.ImageField(
        upload_to="homepage/", blank=True, null=True, help_text="About section image"
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
    about_title = models.CharField(max_length=200, blank=True)
    about_content = models.TextField(blank=True)

    class Meta:
        unique_together = ("home_page", "language")
        verbose_name = "Home Page Translation"
        verbose_name_plural = "Home Page Translations"

    def __str__(self):
        return f"Home Page Content - {self.get_language_display()}"
