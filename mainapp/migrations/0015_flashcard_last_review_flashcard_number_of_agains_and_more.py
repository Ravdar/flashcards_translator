# Generated by Django 4.2.10 on 2024-03-26 16:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0014_alter_flashcard_deck"),
    ]

    operations = [
        migrations.AddField(
            model_name="flashcard",
            name="last_review",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="number_of_agains",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="number_of_easy",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="number_of_good",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="number_of_hard",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="number_of_reviews",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="flashcard",
            name="next_review",
            field=models.DateField(default=datetime.date(2024, 3, 26)),
        ),
        migrations.AlterField(
            model_name="translation",
            name="from_language",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="translation_from",
                to="mainapp.language",
            ),
        ),
    ]
