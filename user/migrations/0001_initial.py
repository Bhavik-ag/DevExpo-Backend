# Generated by Django 4.2.2 on 2023-06-24 04:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=500)),
                (
                    "profile_pic",
                    models.ImageField(
                        blank=True,
                        default="profiles/user-default.png",
                        null=True,
                        upload_to="profiles",
                    ),
                ),
                ("github", models.URLField(blank=True, max_length=100)),
                ("linkedin", models.URLField(blank=True, max_length=100)),
                ("twitter", models.URLField(blank=True, max_length=100)),
                ("website", models.URLField(blank=True, max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
