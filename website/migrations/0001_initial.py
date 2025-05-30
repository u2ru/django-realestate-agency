# Generated by Django 4.2.10 on 2025-05-13 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_title', models.CharField(help_text='Main headline in Georgian', max_length=200)),
                ('hero_subtitle', models.TextField(blank=True, help_text='Subtitle text in Georgian')),
                ('hero_image', models.ImageField(help_text='Main banner image', upload_to='homepage/')),
                ('hero_cta_text', models.CharField(default='Explore Properties', help_text='Call to action button text in Georgian', max_length=50)),
                ('hero_cta_link', models.CharField(default='/properties/', help_text='Call to action button link', max_length=200)),
                ('about_title', models.CharField(blank=True, help_text='About section title in Georgian', max_length=200)),
                ('about_content', models.TextField(blank=True, help_text='About section content in Georgian')),
                ('about_image', models.ImageField(blank=True, help_text='About section image', null=True, upload_to='homepage/')),
                ('contact_phone', models.CharField(blank=True, help_text='Contact phone number', max_length=50)),
                ('contact_email', models.EmailField(blank=True, help_text='Contact email address', max_length=254)),
                ('contact_address', models.TextField(blank=True, help_text='Physical address')),
                ('facebook_url', models.URLField(blank=True, help_text='Facebook page URL')),
                ('instagram_url', models.URLField(blank=True, help_text='Instagram profile URL')),
                ('twitter_url', models.URLField(blank=True, help_text='Twitter profile URL')),
                ('meta_title', models.CharField(blank=True, help_text='SEO meta title in Georgian', max_length=100)),
                ('meta_description', models.TextField(blank=True, help_text='SEO meta description in Georgian')),
                ('meta_keywords', models.CharField(blank=True, help_text='SEO meta keywords in Georgian, comma separated', max_length=255)),
                ('properties_count', models.PositiveIntegerField(default=0, help_text='Number of properties to display')),
                ('years_experience', models.PositiveIntegerField(default=0, help_text='Years of experience to display')),
                ('happy_customers', models.PositiveIntegerField(default=0, help_text='Number of happy customers to display')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Home Page Content',
                'verbose_name_plural': 'Home Page Content',
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Client name', max_length=100)),
                ('position', models.CharField(blank=True, help_text='Client position or company', max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='testimonials/')),
                ('content', models.TextField(help_text='Testimonial content in Georgian')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='FeaturedSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Section title in Georgian', max_length=200)),
                ('subtitle', models.TextField(blank=True, help_text='Section subtitle in Georgian')),
                ('image', models.ImageField(help_text='Section image', upload_to='homepage/sections/')),
                ('link_text', models.CharField(blank=True, help_text='Link text in Georgian', max_length=50)),
                ('link_url', models.CharField(blank=True, help_text='Link URL', max_length=200)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order')),
                ('home_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_sections', to='website.homepagecontent')),
            ],
            options={
                'verbose_name': 'Featured Section',
                'verbose_name_plural': 'Featured Sections',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TestimonialTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('KA', 'Georgian'), ('RU', 'Russian'), ('EN', 'English')], max_length=2)),
                ('content', models.TextField()),
                ('testimonial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='website.testimonial')),
            ],
            options={
                'verbose_name': 'Testimonial Translation',
                'verbose_name_plural': 'Testimonial Translations',
                'unique_together': {('testimonial', 'language')},
            },
        ),
        migrations.CreateModel(
            name='HomePageContentTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('KA', 'Georgian'), ('RU', 'Russian'), ('EN', 'English')], max_length=2)),
                ('hero_title', models.CharField(max_length=200)),
                ('hero_subtitle', models.TextField(blank=True)),
                ('hero_cta_text', models.CharField(blank=True, max_length=50)),
                ('about_title', models.CharField(blank=True, max_length=200)),
                ('about_content', models.TextField(blank=True)),
                ('meta_title', models.CharField(blank=True, max_length=100)),
                ('meta_description', models.TextField(blank=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('home_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='website.homepagecontent')),
            ],
            options={
                'verbose_name': 'Home Page Translation',
                'verbose_name_plural': 'Home Page Translations',
                'unique_together': {('home_page', 'language')},
            },
        ),
        migrations.CreateModel(
            name='FeaturedSectionTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('KA', 'Georgian'), ('RU', 'Russian'), ('EN', 'English')], max_length=2)),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.TextField(blank=True)),
                ('link_text', models.CharField(blank=True, max_length=50)),
                ('featured_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='website.featuredsection')),
            ],
            options={
                'verbose_name': 'Featured Section Translation',
                'verbose_name_plural': 'Featured Section Translations',
                'unique_together': {('featured_section', 'language')},
            },
        ),
    ]
