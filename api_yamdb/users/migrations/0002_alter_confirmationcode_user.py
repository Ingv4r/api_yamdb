# Generated by Django 3.2 on 2023-05-26 09:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="confirmationcode",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="activation_code",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
