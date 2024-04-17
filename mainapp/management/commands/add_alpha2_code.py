from django.core.management.base import BaseCommand
from mainapp.models import Language

class Command(BaseCommand):
    help = 'Populate alpha2_code for existing languages'

    def handle(self, *args, **kwargs):
        language_alpha2_codes = {
            'english': 'US',
            'chinese': 'CN',
            'arabic': 'SA',
            'russian': 'RU',
            'french': 'FR',
            'german': 'DE',
            'spanish': 'ES',
            'portuguese': 'PT',
            'italian': 'IT',
            'japanese': 'JP',
            'korean': 'KR',
            'greek': 'GR',
            'dutch': 'NL',
            'hindi': 'IN',
            'turkish': 'TR',
            'malay': 'MY',
            'thai': 'TH',
            'vietnamese': 'VN',
            'indonesian': 'ID',
            'hebrew': 'IL',
            'polish': 'PL',
            'mongolian': 'MN',
            'czech': 'CZ',
            'hungarian': 'HU',
            'estonian': 'EE',
            'bulgarian': 'BG',
            'danish': 'DK',
            'finnish': 'FI',
            'romanian': 'RO',
            'swedish': 'SE',
            'slovenian': 'SI',
            'persian/farsi': 'IR',
            'bosnian': 'BA',
            'serbian': 'RS',
            'filipino': 'PH',
            'catalan': 'ES',
            'croatian': 'HR',
            'latvian': 'LV',
            'lithuanian': 'LT',
            'ukrainian': 'UA',
            'welsh': 'GB',
            'slovak': 'SK',
            'afrikaans': 'ZA',
            'norwegian': 'NO',
            'belarusian': 'BY',
            'esperanto': 'EO',
            'irish': 'IE'
        }

        for language in Language.objects.all():
            language.alpha2_code = language_alpha2_codes.get(language.name.lower(), None)
            language.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated alpha2_code for existing languages'))