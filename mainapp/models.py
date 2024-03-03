from django.db import models

class Translation(models.Model):
    input_text = models.CharField(max_length=500)
    output_text = models.CharField(max_length=500, null=True, blank=True)
    is_flashcard = models.BooleanField()
# Create your models here.

class Flashcard(models.Model):
    front = models.CharField(max_length=500)
    back = models.CharField(max_length=500)

class Deck(models.Model):
    name = models.CharField(max_length=140)
    flashcards = models.ManyToManyField(Flashcard, blank=True, related_name="decks")
