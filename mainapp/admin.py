from django.contrib import admin

from users.models import Profile
from.models import Translation,Flashcard,Deck,Language

class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1

class DeckAdmin(admin.ModelAdmin):
    inlines = [FlashcardInline]

# Register your models here.
admin.site.register(Translation)
admin.site.register(Flashcard)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Language)
admin.site.register(Profile)
