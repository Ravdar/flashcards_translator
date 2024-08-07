# Generated by Django 4.2.10 on 2024-04-14 08:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0019_alter_flashcard_next_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="flashcard",
            name="from_language",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="flashcard_from_language",
                to="mainapp.language",
            ),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="to_language",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="flashcard_to_language",
                to="mainapp.language",
            ),
        ),
        migrations.AlterField(
            model_name="flashcard",
            name="next_review",
            field=models.DateField(default=datetime.date(2024, 4, 14)),
        ),
    ]
