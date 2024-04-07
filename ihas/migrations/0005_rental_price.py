# Generated by Django 5.0.4 on 2024-04-05 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ihas", "0004_rental_end_date_alter_rental_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="rental",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
