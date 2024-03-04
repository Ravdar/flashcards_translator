# Generated by Django 4.2.10 on 2024-03-03 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_alter_translation_output_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="Flashcard",
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
                ("front", models.CharField(max_length=500)),
                ("back", models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name="translation",
            name="is_flashcard",
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Deck",
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
                ("name", models.CharField(max_length=140)),
                (
                    "flashcards",
                    models.ManyToManyField(
                        blank=True, related_name="decks", to="mainapp.flashcard"
                    ),
                ),
            ],
        ),
    ]