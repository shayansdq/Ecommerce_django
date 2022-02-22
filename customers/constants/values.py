from model_utils import Choices
from django.utils.translation import gettext_lazy as _

GENDER_STATUS = Choices(
    (0,'male',_('Male')),
    (1,'female',_('Female')),
    (2,'other',_('Other')),
)

GENDER_STATUS_FORM = (
        (0,'Select your gender'),
        (0,'Male'),
        (1,'Female'),
        (2,'Other')
    )
