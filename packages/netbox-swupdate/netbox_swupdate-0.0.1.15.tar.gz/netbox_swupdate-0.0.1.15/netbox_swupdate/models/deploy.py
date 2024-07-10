from dcim.models import Device
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

from .software import Software

__all__ = ["Deploy"]


class Deploy(NetBoxModel):
    DEPLOY_CHOICES = [
        ("test", "Test"),
        ("production", "Production"),
    ]
    name = models.CharField(max_length=255, help_text="Nombre del despliegue")
    type = models.CharField(
        max_length=50, choices=DEPLOY_CHOICES, help_text="Tipo de despliegue"
    )
    deploy_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha y hora en que se desea realizar el despliegue. Si se "
        "deja en blanco, el despliegue puede realizarse en cualquier "
        "momento.",
    )
    devices = models.ManyToManyField(
        Device, help_text="Dispositivos a los que afectará el despliegue"
    )
    software = models.ForeignKey(
        Software, on_delete=models.CASCADE, help_text="Software asociado al despliegue"
    )

    class Meta:
        ordering = ("pk",)

    def get_absolute_url(self):
        return reverse("plugins:netbox_swupdate:deploy", args=[self.pk])
