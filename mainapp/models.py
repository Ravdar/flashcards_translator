from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime, timedelta

class Language(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=4)

    def __str__(self):
        return self.name

class Translation(models.Model):
    input_text = models.CharField(max_length=500)
    output_text = models.CharField(max_length=500, null=True, blank=True)
    is_flashcard = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_language = models.ForeignKey(Language, related_name="translation_from", on_delete=models.PROTECT, default=70)
    to_language = models.ForeignKey(Language, related_name="translation_to", on_delete=models.PROTECT)

    def __str__(self):
        return self.input_text

class Deck(models.Model):
    name = models.CharField(max_length=140)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.ManyToManyField(User,related_name="decks")
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def flashcards_to_review(self):
        """Returns deck's flashcards which are ready for review."""
        return self.flashcards.filter(next_review__lte=timezone.now().date())
    
class Flashcard(models.Model):
    front = models.CharField(max_length=500)
    back = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decks = models.ManyToManyField(Deck, related_name="flashcards")
    winning_streak = models.IntegerField(default=0)
    easiness_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=0)
    next_review = models.DateField(default=timezone.now().date())

    def __str__(self):
        return self.front    

    def calculate_interval(self,quality):
        """Updates winning streak and interval (number of days remaining to the flashcards next review)."""

        if quality >= 2:
            if self.winning_streak == 0:
                self.interval += 1
            elif self.winning_streak == 1:
                    self.interval += 5
            else:
                self.interval = round(self.interval * self.easiness_factor)
        else:
            self.winning_streak = 0
            self.interval = 1        

    def update_easiness_factor(self, quality):
        """Updates easiness factor (variable used to determine interval)."""

        self.easiness_factor += 0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02)

    def review_flashcard(self,quality):
        """Updates flashcard easiness factor, calulates interval and sets a date for next review."""

        self.update_easiness_factor(quality)
        self.calculate_interval(self)
        self.next_review = timezone.now().date() + timedelta(days=self.interval)
