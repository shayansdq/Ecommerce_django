from django.utils.translation import gettext_lazy as _
from model_utils import Choices

DISCOUNT_STATUS = Choices(
    (0, 'price', _('Price')),
    (1, 'percent', _('Percent'))
)
