from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta


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
    from_language = models.ForeignKey(Language, related_name="translation_from", on_delete=models.PROTECT)
    to_language = models.ForeignKey(Language, related_name="translation_to", on_delete=models.PROTECT)

    def __str__(self):
        return self.input_text


class Deck(models.Model):
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User,related_name="decks",on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def flashcards_to_review(self):
        """Returns deck's flashcards which are ready for review."""
        
        return self.flashcards.filter(next_review__lte=timezone.now().date())
    
    @property
    def has_flashcards_to_review(self):
        """Returns True if the deck has flashcards ready for review, False otherwise."""
        
        return self.flashcards_to_review().exists()
    
    @property
    def number_of_flashcards_reviewed_today(self):
        """Returns the number of flashcards from this deck that were reviewed today."""
        
        return self.flashcards.filter(last_review=timezone.now().date()).count()

    

class Flashcard(models.Model):
    front = models.CharField(max_length=500)
    back = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, related_name="flashcards",on_delete=models.CASCADE)

    # Review algorithm fields
    winning_streak = models.IntegerField(default=0)
    easiness_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=0)
    next_review = models.DateField(default=timezone.now().date())
    last_review = models.DateField(blank=True, null=True, default=None)
    
    # Statistics fields
    number_of_reviews = models.IntegerField(default=0)
    number_of_agains = models.IntegerField(default=0)
    number_of_hard = models.IntegerField(default=0)
    number_of_good = models.IntegerField(default=0)
    number_of_easy = models.IntegerField(default=0)
    total_time = models.FloatField(default=0) # In seconds

    def __str__(self):
        return self.front   

    @property
    def average_time(self):
        if self.number_of_reviews > 0:
            return self.total_time / self.number_of_reviews
        else:
            return 0 

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
            self.interval = 0       

    def update_easiness_factor(self, quality):
        """Updates easiness factor (variable used to determine interval)."""

        self.easiness_factor += 0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02)

    def review_flashcard(self,quality):
        """Updates flashcard easiness factor, calulates interval and sets a date for next review."""

        self.update_easiness_factor(quality)
        self.calculate_interval(quality)
        self.next_review = timezone.now().date() + timedelta(days=self.interval)
        self.last_review = timezone.now().date()
        self.number_of_reviews += 1
