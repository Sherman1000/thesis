import hashlib

from app.exceptions import DoesNotExistException


class StudentEmailHashConverter:
    def __init__(self, student_registry):
        self._student_registry = student_registry

    def student_registry(self):
        return self._student_registry

    def hash_for(self, email):
        return hashlib.md5(email.encode()).hexdigest()

    def recover_email_from(self, hash):
        for student in self.student_registry().all():
            if hash == self.hash_for(student.email()):
                return student.email()
        raise DoesNotExistException('Unable to find email from hash')