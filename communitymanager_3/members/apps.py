from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "communitymanager_3.members"
    verbose_name = _("Members")

    def ready(self):
        try:
            import communitymanager_3.members.signals  # noqa F401
        except ImportError:
            pass
