from app.constants import Gender
from app.entities.courses import Course
from app.entities.students import Student, Studies, Job
from app.models import StudentRecord, StudentStudiesRecord, StudentJobRecord
from app.models.registries import FakeRegistry


class TransientStudentRegistry(FakeRegistry):
    def __init__(self, course_registry):
        super(TransientStudentRegistry, self).__init__()
        self._course_registry = course_registry

    def course_registry(self):
        return self._course_registry

    def append(self, student):
        if self._is_not_already_registered_in_same_course(student):
            self._registers.append(student)

    def active_students(self):
        return self.all()

    def _is_not_already_registered_in_same_course(self, student):
        same_course_students = [other_student for other_student in self._registers if
                                student.course() == other_student.course()]
        return student not in same_course_students


class PersistentStudentRegistry:
    def __init__(self, course_registry):
        self._course_registry = course_registry

    def course_registry(self):
        return self._course_registry

    def all(self):
        records = list(StudentRecord.objects.all())
        if records is None:
            # FIXME: NECESITAS ESTO?
            records = []

        return self._students_from(records)

    def active_students(self):
        current_course = self.course_registry().current()
        records = StudentRecord.objects.filter(course__quarter=current_course.quarter(),
                                               course__year=current_course.year())
        return self._students_from(records)

    def _students_from(self, records):
        return [Student.from_request({
            'Email': record.email,
            'Nombre': record.name,
            'Apellido': record.surname,
            'País': record.country,
            'Provincia': record.state,
            'Genero': Gender.description_for(record.gender),
            'Tipo Documento': record.id_type,
            'Número de documento': record.id_number,
            'Ciudad': record.city,
            'course': Course(quarter=record.course.quarter, year=record.course.year),
            'studies': Studies(university=record.studies.university, career=record.studies.career,
                               study_level=record.studies.study_level,
                               programming_skills=record.studies.programming_skills,
                               python_skills=record.studies.python_skills),
            'job': Job(position=record.job.position, business_name=record.job.business_name)
        }) for record in records]

    # FIXME: HACER QUE LA CONSTRUCCION DEL COURSE SEA AUTOMATICA
    def append(self, student):
        course_record = self.course_registry().register_for(quarter=student.course().quarter(), year=student.course().year())
        studies_record = StudentStudiesRecord.objects.get(university=student.studies().university(),
                                                          career=student.studies().career(),
                                                          study_level=student.studies().study_level(),
                                                          programming_skills=student.studies().programming_skills(),
                                                          python_skills=student.studies().python_skills())
        job_record = StudentJobRecord.objects.get(business_name=student.job().business_name(),
                                                  position=student.job().position())
        StudentRecord.objects.get_or_create(email=student.email(), name=student.name(), surname=student.surname(),
                                            gender=Gender.id_for(student.gender()), country=student.country(),
                                            state=student.state(), city=student.city(), id_type=student.id_type(),
                                            id_number=student.id_number(), course=course_record, studies=studies_record,
                                            job=job_record)

    def first(self):
        return self.all()[0]

    def last(self):
        return self.all()[-1]


class PersistentStudiesRegistry:
    def all(self):
        records = list(StudentStudiesRecord.objects.all())
        if records is None:
            records = []

        return [Studies(university=record.university, career=record.career, study_level=record.study_level,
                        programming_skills=record.programming_skills,
                        python_skills=record.python_skills) for record in records]

    def append(self, studies):
        StudentStudiesRecord.objects.get_or_create(university=studies.university(), career=studies.career(),
                                                   study_level=studies.study_level(),
                                                   programming_skills=studies.programming_skills(),
                                                   python_skills=studies.python_skills())

    def last(self):
        return self.all()[-1]


class PersistentJobRegistry:
    def all(self):
        records = list(StudentJobRecord.objects.all())
        if records is None:
            records = []

        return [Job(business_name=record.business_name, position=record.position) for record in records]

    def append(self, job):
        StudentJobRecord.objects.get_or_create(business_name=job.business_name(), position=job.position())

    def last(self):
        return self.all()[-1]