from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from app.commands.base import Validator, Result


class UserExistValidator(Validator):
    def __init__(self, user_id):
        self._user_id = user_id

    def validate(self):
        result = Result()

        try:
            User.objects.get(id=self._user_id)
        except (User.DoesNotExist, ValueError):
            result.add_error(f'User does not exists with id: {self._user_id}')

        return result


class UserIsLoggedValidator(Validator):
    def __init__(self, user):
        self._user = user

    def validate(self):
        result = Result()

        try:
            Token.objects.get(user=self._user)
        except Token.DoesNotExist:
            result.add_error(f'User with: {self._user} is not logged in')

        return result


class UserIsStaffValidator(Validator):
    def __init__(self, user_id):
        self._user_id = user_id

    def validate(self):
        result = Result()

        user = User.objects.get(id=self._user_id)
        if not user.is_staff:
            result.add_error(f'User with: {self._user_id} is not staff')

        return result


class UserIsLoggedInOrIsStaffValidator(Validator):
    def __init__(self, user_id):
        self._user_id = user_id

    def validate(self):
        result = Result()

        logged_in_result = UserIsLoggedValidator(self._user_id).validate()
        is_staff_result = UserIsStaffValidator(self._user_id).validate()

        if logged_in_result.has_errors() and logged_in_result.has_errors():
            result.add_errors(logged_in_result.errors() + is_staff_result.errors())

        return result


class TextLessThanValidator(Validator):
    def __init__(self, text, max_chars):
        self._text = text
        self._max_chars = max_chars

    def validate(self):
        result = Result()

        if len(self._text) > self._max_chars:
            result.add_error(f'Text: "{self._text}" is too long. Max length {self._max_chars}. Current length: {len(self._text)}')

        return result


class NotEmptyStringValidator(Validator):
    def __init__(self, string, field_name):
        self._string = string
        self._field_name = field_name

    def validate(self):
        result = Result()

        valid_length = 1 <= len(str(self._string))
        if not valid_length:
            result.add_error(f'Required field: {self._field_name} is empty')

        return result


class PasswordConfirmationValidator(Validator):
    def __init__(self, password, password_confirmation):
        self._password = password
        self._password_confirmation = password_confirmation

    def validate(self):
        result = Result()

        if self._password != self._password_confirmation:
            result.add_error(f'Incorrect password confirmation')

        return result
