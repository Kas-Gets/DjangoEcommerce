# Generated by Django 5.1.1 on 2024-10-09 08:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="promotion",
        ),
        migrations.DeleteModel(
            name="Promotion",
        ),
    ]