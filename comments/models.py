from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from customers.models import Customer
from products.models import Product
from django.utils.translation import gettext_lazy as _


class Comment(BaseModel):
    """

    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ccomments',
                                 verbose_name=_('Customer'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments', verbose_name=_('Product'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', null=True, blank=True,
                              verbose_name=_('Reply'))
    is_reply = models.BooleanField(default=False, verbose_name=_('Is reply'),
                                   help_text=_('Selected if this comment is a reply message from another customer'))
    body = models.TextField(max_length=400, verbose_name=_('Body'))

    class Meta:
        ordering = ['-created']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def clean(self):
        if self.is_reply and not self.reply:
            raise ValidationError({'is_reply': _('This field should not be full if this comment isn\'t reply')})
        if self.reply and not self.is_reply:
            raise ValidationError({'reply': _('This field should not be full if this comment isn\'t reply')})

    def __str__(self):
        return f"{self.customer} - {self.body[:30]}"
