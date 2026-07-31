from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Student


class AccessForm(forms.Form):
    """
    A form for entering access codes and validating against the Student model.
    """

    # Define a CharField for the entry code input
    entry_code = forms.CharField(
        label="",
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Enter access code"),
                "class": "form-control",
            }
        ),
    )

    def clean_entry_code(self):
        """
        Custom validation method to check the validity of the entry code.
        """
        entry_code = self.cleaned_data.get("entry_code")
        if entry_code:
            entry_code = entry_code.strip()

        try:
            Student.objects.get(entry_code=entry_code)
        except Student.DoesNotExist:
            raise forms.ValidationError(_("Invalid access code. Please crosscheck and try again."))

        return entry_code

