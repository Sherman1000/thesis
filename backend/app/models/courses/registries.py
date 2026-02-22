from app.entities.courses import Course
from app.models import CourseRecord
from app.models.registries import FakeRegistry


class TransientCourseRegistry(FakeRegistry):
    def current(self):
        return self.last()

    def register_for(self, quarter, year):
        return Course(quarter, year)


class PersistentCourseRegistry:
    def all(self):
        records = list(CourseRecord.objects.all())
        if records is None:
            records = []

        return [self._course_from(record) for record in records]

    def append(self, course):
        CourseRecord.objects.get_or_create(quarter=course.quarter(), year=course.year())

    def current(self):
        # Fixme: puede ser mas inteligente esta logica.
        return self._course_from(CourseRecord.objects.last())

    def register_for(self, quarter, year):
        # FIXME: PASAR ESTO DENTRO DEL STUDENT REGISTRY Y SACAR LA COMPOSICION DE REGISTRIES.
        # FIXME: THIS IS NOT POLIMORPHIC TO TRANSIENTCOURSEREGISTRY
        return CourseRecord.objects.get(quarter=quarter, year=year)

    def _course_from(self, record):
        return Course(quarter=record.quarter, year=record.year)
