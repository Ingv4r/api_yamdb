# Generated by Django 3.2 on 2023-05-28 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_confirmationcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='code',
            field=models.CharField(default='ZCdlLS', max_length=6),
        ),
    ]
