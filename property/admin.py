from django.contrib import admin
from django.forms import ModelForm, TextInput, Textarea
from django.utils.html import format_html

from .models import (
    Property,
    PropertyImage,
    PropertyTranslation,
    SUPPORTED_LANGUAGES,
    PRIMARY_LANGUAGE,
    CITY_CHOICES,
)

# Get language codes from constant
SECONDARY_LANGUAGES = [
    lang for lang in SUPPORTED_LANGUAGES.keys() if lang != PRIMARY_LANGUAGE
]


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ("image_preview",)
    fields = ("image", "image_preview", "is_main")

    def image_preview(self, obj):
        """Generate a thumbnail preview for the admin"""
        if obj.image and obj.pk:
            return format_html(
                '<img src="{}" width="100" height="auto" />', obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


# Function to create a translation form class for a specific language
def create_translation_form_class(language_code):
    """Create a ModelForm class for a specific language"""
    language_name = SUPPORTED_LANGUAGES[language_code]

    class TranslationForm(ModelForm):
        class Meta:
            model = PropertyTranslation
            fields = ("name", "description")
            widgets = {
                "name": TextInput(attrs={"placeholder": f"{language_name} Name"}),
                "description": Textarea(
                    attrs={"placeholder": f"{language_name} Description"}
                ),
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
    TranslationForm.__name__ = f"{language_code}TranslationForm"
    return TranslationForm


# Function to create a translation inline class for a specific language
def create_translation_inline_class(language_code):
    """Create a StackedInline class for a specific language"""
    language_name = SUPPORTED_LANGUAGES[language_code]
    form_class = create_translation_form_class(language_code)

    class TranslationInline(admin.StackedInline):
        model = PropertyTranslation
        form = form_class
        verbose_name = f"{language_name} Translation"
        verbose_name_plural = f"{language_name} Translation"
        extra = 1
        max_num = 1
        min_num = 1
        can_delete = False  # Prevent translation deletion

        def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs.filter(language=language_code)

        def has_add_permission(self, request, obj=None):
            if obj:
                return self.get_queryset(request).count() == 0
            return True

    # Give the class a unique name
    TranslationInline.__name__ = f"{language_code}TranslationInline"
    return TranslationInline


# Dynamically create translation inlines for each language
language_inlines = [
    create_translation_inline_class(lang) for lang in SECONDARY_LANGUAGES
]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "currency",
        "property_type",
        "deal_type",
        "agent_name",
        "featured",
        "published",
        "image_preview",
    )
    search_fields = ("name", "description", "address", "property_id", "agent_name")
    inlines = [PropertyImageInline] + language_inlines
    readonly_fields = ("image_gallery",)

    fieldsets = (
        (
            f"Basic Information ({SUPPORTED_LANGUAGES[PRIMARY_LANGUAGE]})",
            {"fields": ("name", "description", "featured", "published")},
        ),
        ("Price Information", {"fields": ("price", "currency")}),
        ("Location", {"fields": ("address", "city", "property_id")}),
        ("Media", {"fields": ("youtube_url",)}),
        (
            "Property Details",
            {
                "fields": (
                    "property_type",
                    "deal_type",
                    "rooms",
                    "area",
                    "floor",
                    "total_floors",
                    "state",
                )
            },
        ),
        (
            "Additional Features",
            {
                "fields": (
                    "has_balcony",
                    "has_parking",
                    "has_elevator",
                    "has_furniture",
                    "has_central_heating",
                ),
            },
        ),
        (
            "Agent Information",
            {
                "fields": (
                    "agent_name",
                    "agent_phone",
                ),
            },
        ),
    )

    def image_preview(self, obj):
        """Display a thumbnail of the main image in the list view"""
        main_image = obj.images.filter(is_main=True).first()
        if not main_image:
            main_image = obj.images.first()

        if main_image:
            return format_html(
                '<img src="{}" width="40" height="auto" />', main_image.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"

    def image_gallery(self, obj):
        """Display a gallery of all property images"""
        images = obj.images.all()
        if images:
            gallery_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">'
            for img in images:
                gallery_html += format_html(
                    '<div style="text-align: center; margin-bottom: 10px;">'
                    '<img src="{}" width="100" height="auto" style="margin-bottom: 5px;" />'
                    "<p>{}</p>"
                    "</div>",
                    img.image.url,
                    "Main Image" if img.is_main else "",
                )
            gallery_html += "</div>"
            return format_html(gallery_html)
        return "No Images"

    image_gallery.short_description = "Image Gallery"

    # Add the image gallery to the fieldsets
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # Only show gallery for existing objects
            fieldsets = list(fieldsets)
            fieldsets.insert(1, ("Image Gallery", {"fields": ("image_gallery",)}))
        return fieldsets

    def save_formset(self, request, form, formset, change):
        """Ensure translations have language set before saving"""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, PropertyTranslation):
                # Force set language based on formset prefix
                for lang_code in SECONDARY_LANGUAGES:
                    if lang_code.lower() in formset.prefix.lower():
                        instance.language = lang_code
            instance.save()
        formset.save_m2m()

    def get_list_filter(self, request):
        """Customize list filters based on user permissions"""
        filters = [
            "property_type",
            "deal_type",
            "featured",
            "published",
            "state",
            "agent_name",
        ]

        # Add city filter with reasonable choices
        if len(CITY_CHOICES) > 20:
            # Create a custom filter with major cities when we have many options
            filters.append(("city", admin.AllValuesFieldListFilter))
        else:
            filters.append("city")

        return filters
