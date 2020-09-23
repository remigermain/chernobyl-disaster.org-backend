from django.apps import AppConfig


class GalleryConfig(AppConfig):
    name = 'gallery'

    def ready(self):
        from django.db.models.signals import post_delete
        from lib.signals import delete_commit
        from gallery.models import Picture, PictureLang, Video, VideoLang, People, PeopleLang
        post_delete.connect(delete_commit, sender=Picture)
        post_delete.connect(delete_commit, sender=PictureLang)
        post_delete.connect(delete_commit, sender=Video)
        post_delete.connect(delete_commit, sender=VideoLang)
        post_delete.connect(delete_commit, sender=People)
        post_delete.connect(delete_commit, sender=PeopleLang)
