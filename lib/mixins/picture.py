from django.conf import settings


class PictureMixins:

    def to_url(self, field):
        link = getattr(self, field)
        if not link:
            return None
        link = link.url
        if not link[0] == "/":
            return f"{settings.SITE_URL}/{getattr(self, field).url}"
        return f"{settings.SITE_URL}{getattr(self, field).url}"
