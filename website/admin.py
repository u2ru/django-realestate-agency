from django.contrib import admin
from unfold.admin import ModelAdmin
from django.forms import ModelForm, TextInput, Textarea, forms, JSONField
from django.utils.html import format_html
from .models import (
    HomePageContent,
    HomePageContentTranslation,
    AboutUsContent,
    AboutUsContentTranslation,
)
from property.constants import SUPPORTED_LANGUAGES, PRIMARY_LANGUAGE
from property.admin import CoordinatesWidget

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
                    not in [
                        "middle_section_content",
                        "properties_for_sale_subtitle",
                        "properties_for_rent_subtitle",
                        "main_content",
                        "our_services_content",
                        "bottom_section_content",
                        "meta_description",
                        "content",
                        "subtitle",
                    ]
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
        ordering_field = "language"

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
            # separate section for middle section
            "middle_section_title",
            "middle_section_content",
            # separate section for properties for sale
            "properties_for_sale_title",
            "properties_for_sale_subtitle",
            # separate section for properties for rent
            "properties_for_rent_title",
            "properties_for_rent_subtitle",
        ],
    )
    for lang in SECONDARY_LANGUAGES
]


@admin.register(HomePageContent)
class HomePageContentAdmin(ModelAdmin):
    inlines = homepage_translation_inlines
    readonly_fields = ("logo_preview", "logo_white_preview")
    fieldsets = (
        ("Company Information", {"fields": ("company_name",)}),
        (
            "Logo",
            {
                "fields": ("logo", "logo_preview", "logo_white", "logo_white_preview"),
                "classes": ("wide",),
            },
        ),
        ("Hero Section", {"fields": ("hero_title", "hero_subtitle", "hero_image")}),
        (
            "Properties for Sale Section",
            {"fields": ("properties_for_sale_title", "properties_for_sale_subtitle")},
        ),
        (
            "Middle Section",
            {"fields": ("middle_section_title", "middle_section_content")},
        ),
        (
            "Properties for Rent Section",
            {"fields": ("properties_for_rent_title", "properties_for_rent_subtitle")},
        ),
        (
            "Contact Information",
            {"fields": ("contact_phone", "contact_email", "contact_address")},
        ),
        ("Social Media", {"fields": ("facebook_url", "instagram_url")}),
        (
            "Statistics",
            {"fields": ("properties_count", "years_experience", "happy_customers")},
        ),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;"/>',
                obj.logo.url,
            )
        return "No logo uploaded"

    logo_preview.short_description = "Logo Preview"

    def logo_white_preview(self, obj):
        if obj.logo_white:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;"/>',
                obj.logo_white.url,
            )
        return "No white logo uploaded"

    logo_white_preview.short_description = "White Logo Preview"

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


class AboutUsContentAdminForm(ModelForm):
    office_coordinates = JSONField(
        required=False,
        widget=CoordinatesWidget,
        help_text="Click on the map to set coordinates",
    )

    class Meta:
        model = AboutUsContent
        fields = "__all__"


@admin.register(AboutUsContent)
class AboutUsContentAdmin(ModelAdmin):
    form = AboutUsContentAdminForm
    inlines = [
        create_translation_inline_class(
            AboutUsContentTranslation,
            "about_us",
            lang,
            [
                "hero_title",
                "hero_subtitle",
                #
                "main_subtitle",
                "main_title",
                "main_content",
                #
                "our_services_title",
                "our_services_content",
                #
                "bottom_section_title",
                "bottom_section_content",
            ],
        )
        for lang in SECONDARY_LANGUAGES
    ]
    fieldsets = (
        ("Hero Section", {"fields": ("hero_title", "hero_image")}),
        ("Main Content", {"fields": ("main_subtitle", "main_title", "main_content")}),
        (
            "Our Services Section",
            {"fields": ("our_services_title", "our_services_content")},
        ),
        (
            "Office Location",
            {"fields": ("office_location_address", "office_coordinates")},
        ),
        (
            "Bottom Section",
            {"fields": ("bottom_section_title", "bottom_section_content")},
        ),
    )

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
