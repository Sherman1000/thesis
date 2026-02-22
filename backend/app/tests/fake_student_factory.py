from app.entities.courses import Course
from app.entities.students import StudentRegistrar
from app.models.courses.registries import TransientCourseRegistry, PersistentCourseRegistry
from app.models.registries import FakeRegistry
from app.models.student.registries import PersistentStudiesRegistry, TransientStudentRegistry, \
    PersistentStudentRegistry, PersistentJobRegistry


class FakeStudentFactory:
    def __init__(self):
        self._a_course = Course(quarter=2, year=2021)

        self._course_registry = PersistentCourseRegistry()
        self._course_registry.append(self._a_course)

        self._studies_registry = PersistentStudiesRegistry()

        self._student_registry = PersistentStudentRegistry(self._course_registry)

        self._job_registry = PersistentJobRegistry()

    def student_registry(self):
        return self._student_registry

    def build_a_fake_student(self, from_a_student_request):
        student_registrar = StudentRegistrar(self._student_registry, studies_registry=self._studies_registry,
                                             job_registry=self._job_registry, course=self._course_registry.current())

        student_registrar.process([from_a_student_request])
