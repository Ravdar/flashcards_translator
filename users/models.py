from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, default="images/default_pp.png", upload_to="images/")
    activity = models.JSONField(default=list)

    def __str__(self):
        return self.user.username
    
    @property
    def total_decks_reviewed_today(self):
        """Returns the total number of decks from which flashcards were reviewed today."""

        total_decks = 0

        for deck in self.user.decks.all():
            if deck.number_of_flashcards_reviewed_today != 0:
                total_decks += 1

        return total_decks

    @property
    def total_flashcards_reviewed_today(self):
        """Returns the total number of flashcards reviewed today."""
        
        total_flashcards = 0
        
        for deck in self.user.decks.all():
            total_flashcards += deck.number_of_flashcards_reviewed_today
        
        return total_flashcards    
    
    @property
    def total_flashcards_to_review_today(self):
        """Returns the total number of flashcards ready for review for today."""
        
        total_flashcards = 0
        
        for deck in self.user.decks.all():
            total_flashcards += deck.flashcards_to_review().count()
        
        return total_flashcards    
    
    @property
    def activity_streak(self):
        """Returns the length of the current streak of consecutive days where the user has used the app."""

        unique_activity = list(set(self.activity))
        unique_activity_dates = [datetime.strptime(date, "%Y-%m-%d") for date in unique_activity]
        unique_activity_dates.sort(reverse=True)

        if len(unique_activity_dates) ==0:
            streak = 0
        if len(unique_activity_dates) == 1:
            streak = 1 
        else:

            streak = 1
            for i in range(1, len(unique_activity_dates)):
                if unique_activity_dates[i-1] - unique_activity_dates[i] == timedelta(days=1):
                    streak += 1
                else:
                    break

        return streak
             

    
            

