# Generated by Django 4.1 on 2024-07-01 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_post_comentario"),
    ]

    operations = [
        migrations.CreateModel(
            name="Capital",
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
                ("pais", models.CharField(max_length=100)),
                ("capital", models.CharField(max_length=100)),
            ],
        ),
    ]
