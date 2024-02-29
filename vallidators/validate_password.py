from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class ValidatePassword:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, 'a-z'."))

        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, 'A-Z'."))

        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("The password must contain at least 1 digit, '0-9'."))

        if not any(char in '!@#$%^&*()_+-=[]{};:,.<>?/|\\' for char in password):
            raise ValidationError(_("The password must contain at least 1 special character: "
                                    "'!@#$%^&*()_+-=[]{};:,.<>?/|\\'."))

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, 'a-z', at least 1 uppercase letter, 'A-Z', "
            "at least 1 digit, '0-9', and at least 1 special character: '!@#$%^&*()_+-=[]{};:,.<>?/|\\'."
        )
