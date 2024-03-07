from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Translation(models.Model):
    input_text = models.CharField(max_length=500)
    output_text = models.CharField(max_length=500, null=True, blank=True)
    is_flashcard = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_language = models.ForeignKey(Language, related_name="translation_from", on_delete=models.PROTECT)
    to_language = models.ForeignKey(Language, related_name="translation_to", on_delete=models.PROTECT)

    def __str__(self):
        return self.input_text

class Deck(models.Model):
    name = models.CharField(max_length=140)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.ManyToManyField(User,related_name="decks")

    def __str__(self):
        return self.name
    
class Flashcard(models.Model):
    front = models.CharField(max_length=500)
    back = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decks = models.ManyToManyField(Deck, related_name="flashcards")

    def __str__(self):
        return self.front
