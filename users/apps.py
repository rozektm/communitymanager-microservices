from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "communitymanager_3.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import communitymanager_3.users.signals  # noqa F401
        except ImportError:
            pass
