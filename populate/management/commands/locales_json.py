from django.core.management.base import BaseCommand
from common.models import Translate, TranslateLang
import json

PATH = "locales"
KEY_PERCENTAGE = "percentage"


class Command(BaseCommand):
    def handle(self, *args, **options):
        trans = list(Translate.objects.all().prefetch_related("langs"))
        count = len(trans)

        locales = [lang[0] for lang in TranslateLang.lang_choices]

        langs = {}
        missing = {}
        for locale in locales:
            langs[locale] = {}
            missing[locale] = []

        for t in trans:
            keys = t.key.split(".")
            for locale in locales:
                tmp = langs[locale]
                last_key = keys[-1]
                for key in keys[:-1]:
                    if key not in tmp:
                        tmp[key] = {}
                    tmp = tmp[key]
                h = list(filter(lambda x: x.language == locale, t.langs.all()))
                if h:
                    tmp[last_key] = h[0].value
                else:
                    missing[locale].append(t.key)

        print("[ KEY ]")
        for key, value in missing.items():
            if count > 0:
                percentage = int((count - len(value)) * 100 / count)
            else:
                percentage = 0
            langs[key][KEY_PERCENTAGE] = percentage
            print(f"\t{key}: {percentage}%")

        for key, value in langs.items():
            with open(f"{PATH}/{key.lower()}-{key.upper()}.json", "w") as f:
                f.write(json.dumps(value))
