from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, default="images/default_pp.png", upload_to="images/")

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

