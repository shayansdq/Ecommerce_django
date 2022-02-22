from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone","username")
        field_classes = {'phone': UsernameField}

    def save(self, commit=True):
        self.username = self.phone
        return super().save(commit)
