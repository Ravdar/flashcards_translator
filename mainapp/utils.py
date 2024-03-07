from .models import Language

def create_language_objects(language_list):
    for lang_dict in language_list:
        Language.objects.create(
            name=lang_dict['name'],
            symbol=lang_dict['symbol']
        )