# Generated by Django 5.0.1 on 2024-02-02 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_productcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcard',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
