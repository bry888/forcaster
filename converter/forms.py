from django import forms

class LinkForm(forms.Form):
    input_links = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 120}))

# NIE DZIALA D;D;D;D;D;

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from re import match

#validate_allegro_links = RegexValidator(regex='')
def validate_allegro_links(link):
    if match('allegro\.pl\/[a-z-\/]+[0-9]+.*|allegro\.pl\/dzial\/[a-z-]+', link):
        raise ValidationError(
            _('%(value)s is not a proper allegro link'),
            params={'value': value},
        )


class AllegroField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split('\r\n')

    def validate(self, value):
        """Check if value consists only of valid links."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for link in value:
            validate_allegro_links(link)

class LinkForm2(forms.Form):
    input_links = AllegroField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 120}))#, validators=[validate_allegro_links])
