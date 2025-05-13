from django.contrib import admin
from django.forms import ModelForm, TextInput, Textarea
from django.utils.html import format_html
from .models import (
    HomePageContent,
    HomePageContentTranslation,
)
from property.models import SUPPORTED_LANGUAGES, PRIMARY_LANGUAGE

# Get language codes from constant
SECONDARY_LANGUAGES = [
    lang for lang in SUPPORTED_LANGUAGES.keys() if lang != PRIMARY_LANGUAGE
]


# Functions to handle translations
def create_translation_form_class(model_class, language_code, field_names):
    """Create a ModelForm class for a specific language"""
    language_name = SUPPORTED_LANGUAGES[language_code]

    class TranslationForm(ModelForm):
        class Meta:
            model = model_class
            fields = field_names
            widgets = {
                field: (
                    TextInput(
                        attrs={
                            "placeholder": f"{language_name} {field.replace('_', ' ').title()}"
                        }
                    )
                    if field
                    not in ["about_content", "meta_description", "content", "subtitle"]
                    else Textarea(
                        attrs={
                            "placeholder": f"{language_name} {field.replace('_', ' ').title()}"
                        }
                    )
                )
                for field in field_names
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if hasattr(self, "instance"):
                self.instance.language = language_code

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.language = language_code
            if commit:
                instance.save()
            return instance

    # Give the class a unique name
    TranslationForm.__name__ = f"{model_class.__name__}_{language_code}TranslationForm"
    return TranslationForm


def create_translation_inline_class(model_class, parent_field, language_code, fields):
    """Create a StackedInline class for a specific language"""
    language_name = SUPPORTED_LANGUAGES[language_code]
    form_class = create_translation_form_class(model_class, language_code, fields)

    class TranslationInline(admin.StackedInline):
        model = model_class
        form = form_class
        verbose_name = f"{language_name} Translation"
        verbose_name_plural = f"{language_name} Translation"
        extra = 1
        max_num = 1
        can_delete = False  # Prevent translation deletion

        def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs.filter(language=language_code)

        def has_add_permission(self, request, obj=None):
            if obj:
                return self.get_queryset(request).count() == 0
            return True

    # Give the class a unique name
    TranslationInline.__name__ = (
        f"{model_class.__name__}_{language_code}TranslationInline"
    )
    return TranslationInline


# Create translation inlines for HomePageContent
homepage_translation_inlines = [
    create_translation_inline_class(
        HomePageContentTranslation,
        "home_page",
        lang,
        [
            "hero_title",
            "hero_subtitle",
            "hero_cta_text",
            "about_title",
            "about_content",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ],
    )
    for lang in SECONDARY_LANGUAGES
]


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            f"Hero Section ({SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]})",
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                    "hero_image",
                    "hero_cta_text",
                    "hero_cta_link",
                ),
            },
        ),
        (
            f"About Section ({SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]})",
            {
                "fields": ("about_title", "about_content", "about_image"),
            },
        ),
        (
            "Contact Information",
            {
                "fields": ("contact_phone", "contact_email", "contact_address"),
            },
        ),
        (
            "Social Media",
            {
                "fields": ("facebook_url", "instagram_url", "twitter_url"),
            },
        ),
        (
            f"SEO Settings ({SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]})",
            {
                "fields": ("meta_title", "meta_description", "meta_keywords"),
                "classes": ("collapse",),
            },
        ),
        (
            "Statistics",
            {
                "fields": ("properties_count", "years_experience", "happy_customers"),
            },
        ),
    )
    inlines = homepage_translation_inlines

    def has_add_permission(self, request):
        # Only allow one instance
        return not HomePageContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the single instance
        return False

    def save_formset(self, request, form, formset, change):
        """Ensure translations have language set before saving"""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, HomePageContentTranslation):
                # Force set language based on formset prefix
                for lang_code in SECONDARY_LANGUAGES:
                    if lang_code.lower() in formset.prefix.lower():
                        instance.language = lang_code
            instance.save()
        formset.save_m2m()
