import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Receipt(models.Model):
    uuid = models.UUIDField(
        _("uuid"), default=uuid.uuid4, editable=False, db_index=True
    )
    data = models.JSONField(
        _("data"), null=False, blank=False
    )  # Since we aren't really doing DB stuff, not going to break this out into its parts just store it together
