from django.db import models

class Translation(models.Model):
    input_text = models.CharField(max_length=500)
    output_text = models.CharField(max_length=500, null=True, blank=True)
    is_flashcard = models.BooleanField()

    def __str__(self):
        return self.input_text

class Flashcard(models.Model):
    front = models.CharField(max_length=500)
    back = models.CharField(max_length=500)

    def __str__(self):
        return self.front

class Deck(models.Model):
    name = models.CharField(max_length=140)
    flashcards = models.ManyToManyField(Flashcard, blank=True, related_name="decks")

    def __str__(self):
        return self.name
