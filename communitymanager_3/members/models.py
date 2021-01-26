import django_lifecycle
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _

from communitymanager_3.members import tasks


class Metadata(models.Model):
    METADATA_CHOICES = (
        ("membership_level", _("Membership Level")),
        ("community_attributes", _("Community Attribute")),
        ("other", _("Other")),
    )
    type = models.CharField(max_length=64, choices=METADATA_CHOICES)
    value = models.CharField(max_length=64)

    def __str__(self):
        return "{}: {}".format(self.type, self.value)

    class Meta:
        unique_together = ["type", "value"]


class Member(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255, unique=True)
    country = models.CharField(
        max_length=255, null=True, blank=True, help_text=_("Member's coverage country")
    )
    theater = models.CharField(
        max_length=255, null=True, blank=True, help_text=_("Member's coverage theater")
    )
    region = models.CharField(
        max_length=255, null=True, blank=True, help_text=_("Member's coverage region")
    )
    role = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Member's actual role at Cisco"),
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.email)


class Community(models.Model):
    name = models.CharField(max_length=128)
    abreviation = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(
        default=False,
        help_text=_(
            "If 'True' Community will integrate with Webex Teams and Cisco Mailer"
        ),
    )
    is_visible = models.BooleanField(
        default=False,
        help_text=_("If 'True' Community will be displayed on tool's main page"),
    )

    def __str__(self):
        return "({}) {}".format(self.name, self.abreviation)


class Membership(django_lifecycle.LifecycleModelMixin, models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    level = ForeignKey(
        Metadata,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "membership_level"},
    )
    community = ForeignKey(
        Community, on_delete=models.CASCADE, related_name="membership"
    )
    member = ForeignKey(Member, on_delete=models.CASCADE, related_name="membership")

    class Meta:
        unique_together = ["member", "community"]

    def __str__(self):
        return "{}/{} [{}]".format(self.community.abreviation, self.level, self.member)

    def get_meta_values(self):
        try:
            meat_values = CommunityAttributes.objects.filter(
                models.Q(community=self.community),
                models.Q(restriction=None) | models.Q(restriction=self.level),
            )
            return meat_values
        except Community.DoesNotExist:
            return None

    @django_lifecycle.hook(django_lifecycle.AFTER_CREATE)
    def after_create(self):
        meta_list = self.get_meta_values()
        if meta_list:
            for m in meta_list:
                if m.type.value == "wt_room":
                    tasks.add_to_wt_room.delay(email=self.member.email, room_id=m.value)

    @django_lifecycle.hook(
        django_lifecycle.BEFORE_UPDATE, when="level", has_changed=True
    )
    def before_update():
        pass

    @django_lifecycle.hook(
        django_lifecycle.AFTER_UPDATE, when="level", has_changed=True
    )
    def after_update():
        pass

    @django_lifecycle.hook(django_lifecycle.AFTER_DELETE)
    def after_delete():
        pass


class CommunityAttributes(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    community = ForeignKey(
        Community, on_delete=models.CASCADE, related_name="attribute"
    )
    type = ForeignKey(
        Metadata,
        on_delete=models.CASCADE,
        related_name="attribute",
        limit_choices_to={"type": "community_attributes"},
    )
    restriction = ForeignKey(
        Metadata,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="restriction",
        help_text=_(
            "If added this atribute will be 'restriction' significant only. Eg. WT room for Bronze members only"
        ),
    )
    value = models.CharField(max_length=256)
