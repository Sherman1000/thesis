from typing import List


class Result:
    def __init__(self):
        self._errors = []
        self._object = None

    def is_successful(self):
        return not self.has_errors()

    def has_errors(self):
        return 0 < len(self.errors())

    def errors(self):
        return self._errors

    def add_error(self, error):
        self._errors.append(error)

    def add_errors(self, errors):
        for error in errors:
            self.add_error(error)

    def get_object(self):
        return self._object

    def set_object(self, obj):
        self._object = obj

    def copy_from(self, another_result):
        self._errors = another_result.errors()
        self._object = another_result.get_object()


class Validator:
    def validate(self):
        raise NotImplementedError('Should be implemented')


class Command:
    def execute(self):
        result = Result()

        self._shortcut_validation(result)

        if result.is_successful():
            self._execute_from_successful_validation(result)

        return result

    def validators(self):
        raise NotImplementedError('Should be implemented')

    def _shortcut_validation(self, result):
        for validator in self.validators():
            validation_result = validator.validate()

            if validation_result.has_errors():
                result.add_errors(validation_result.errors())
                break

    def _execute_from_successful_validation(self, result):
        raise NotImplementedError('Should be implemented')
