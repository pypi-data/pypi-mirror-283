from django.db import models
from artd_partner.models import Partner
from django.utils.translation import gettext_lazy as _

CURRENCIES = (
    ('COP', 'COP'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('BRL', 'BRL')
)
IDENTIFICATION_TYPES = (
    ('1', 'Pasaporte'),
    ('4', 'Cédula de ciudadania'),
    ('5', 'Cédula de extranjeria'),
    ('6', 'NIT')
)

class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        help_text=_("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        help_text=_("Updated at"),
        auto_now=True,
    )
    status = models.BooleanField(
        _("Status"),
        help_text=_("Status"),
        default=True,
    )

    class Meta:
        abstract = True

class PaymentsWayCredential(BaseModel):
    """Model definition for Payments Way Credential."""

    partner = models.OneToOneField(
        Partner,
        verbose_name=_('Partner'),
        on_delete=models.CASCADE,
    )
    merchant_id = models.CharField(
        _("Merchant ID"),
        help_text=_("Merchant ID"),
        max_length=100,
    )
    api_key = models.TextField(
        _("API Key"),
        help_text=_("API Key"),
    )
    redirect = models.CharField(
        _("Redirect"),
        help_text=_("Redirect"),
        max_length=100,
        blank=True, 
        null=True,
    )

    class Meta:
        """Meta definition for Payments Way Credential."""

        verbose_name = _('Payments Way Credential')
        verbose_name_plural = _('Payments Way Credentials')

    def __str__(self):
        """Unicode representation of Payments Way Credential."""
        return f"{self.partner.name} ({self.merchant_id})"


class PaymentsWayTestData(BaseModel):
    """Model definition for Payments Way Test Data."""

    payments_way_credential = models.ForeignKey(
        PaymentsWayCredential,
        verbose_name=_('Payments Way Credential'),
        on_delete=models.CASCADE,
    )
    form_id = models.CharField(
        _("Form ID"),
        help_text=_("Form ID"),
        max_length=100,
    )
    terminal_id = models.CharField(
        _("Terminal ID"),
        help_text=_("Terminal ID"),
        max_length=100,
    )
    order_number = models.CharField(
        _("Order Number"),
        help_text=_("Order Number"),
        max_length=100,
    )
    amount = models.DecimalField(
        _("Amount"),
        help_text=_("Amount"),
        max_digits=10,
        decimal_places=2,
    )
    currency = models.CharField(
        _("Currency"),
        help_text=_("Currency"),
        max_length=3,
        choices=CURRENCIES,
        default='COP',
    )
    order_description = models.TextField(
        _("Order Description"),
        help_text=_("Order Description"),
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=100,
    )
    last_name = models.CharField(
        _("Last Name"),
        help_text=_("Last Name"),
        max_length=100,
    )
    email = models.EmailField(
        _("Email"),
        help_text=_("Email"),
    )
    identification = models.CharField(
        _("Identification"),
        help_text=_("Identification"),
        max_length=100,
    )
    identification_type = models.CharField(
        _("Identification Type"),
        help_text=_("Identification Type"),
        max_length=1,
        choices=IDENTIFICATION_TYPES,
        default='1',
    )
    response_url = models.CharField(
        _("Response URL"),
        help_text=_("Response URL"),
        max_length=255,
    )

    class Meta:
        """Meta definition for Payments Way Test Data."""

        verbose_name = _('Payments Way Test Data')
        verbose_name_plural = _('Payments Way Test Data')

    def __str__(self):
        """Unicode representation of Payments Way Test Data."""
        return self.payments_way_credential.partner.name
