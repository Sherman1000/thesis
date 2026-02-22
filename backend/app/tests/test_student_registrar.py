from django.test import TransactionTestCase

from app.entities.courses import Course
from app.entities.students import StudentRegistrar
from app.models.courses.registries import TransientCourseRegistry, PersistentCourseRegistry
from app.models.registries import FakeRegistry
from app.models.student.registries import PersistentStudentRegistry, TransientStudentRegistry, \
    PersistentStudiesRegistry, PersistentJobRegistry


class StudentRegistrarTest(TransactionTestCase):
    def setUp(self):
        self.a_course = Course(quarter=2, year=2021)

        # self.course_registry = PersistentCourseRegistry()
        self.course_registry = TransientCourseRegistry()
        self.course_registry.append(self.a_course)

        # self.studies_registry = PersistentStudiesRegistry()
        self.studies_registry = FakeRegistry()

        # self.student_registry = PersistentStudentRegistry(self.course_registry)
        self.student_registry = TransientStudentRegistry(self.course_registry)

        # self.job_registry = PersistentJobRegistry()
        self.job_registry = FakeRegistry()

        self.student_registrar = StudentRegistrar(self.student_registry, studies_registry=self.studies_registry,
                                                  job_registry=self.job_registry, course=self.course_registry.current())

        self.a_student_request = {
            'Email': 'cwright@gmail.com',
            'Nombre': 'Caro',
            'Apellido': 'Wright',
            'País': 'Argentina',
            'Provincia': 'Buenos Aires',
            'Genero': 'Femenino',
            'Tipo Documento': 'DNI',
            'Número de documento': '234343',
            'Ciudad': 'CABA',
            'Relacion UNSAM': 'No tengo relacion con la UNSAM',
            'Estudiante Ciencia y Tecnologia UNSAM': 'No',
            'Lugar de estudio': 'UBA',
            'Maximo nivel educativo': 'Pregrado (tecnicatura)',
            'Carrera': 'Ciencias de la Computación',
            'Trabajo': 'Eryx',
            'Posicion': 'Desarrolladora',
            'Nivel programacion': 4,
            'Nivel Python': 2
        }

    def test_register_no_student_leaves_no_registry(self):
        self._register(students=[])
        self.assertEqual(self.student_registry.all(), [])

    def test_register_a_student_leaves_that_student_in_registry(self):
        self._register([self.a_student_request])

        self.assertEqual(len(self.student_registry.all()), 1)
        self.assertEqual(self.student_registry.first().name(), 'Caro')
        self.assertEqual(self.student_registry.first().surname(), 'Wright')
        self.assertEqual(self.student_registry.first().country(), 'Argentina')
        self.assertEqual(self.student_registry.first().state(), 'Buenos Aires')
        self.assertEqual(self.student_registry.first().gender(), 'Femenino')

    def test_register_a_student_that_is_already_registered_should_not_add_him_again(self):
        self._register(students=[self.a_student_request])

        self._register(students=[self.a_student_request])

        self.assertEqual(len(self.student_registry.all()), 1)

    def test_register_a_student_adds_him_to_current_course(self):
        self._register(students=[self.a_student_request])

        self.assertEqual(self.student_registry.first().course(), self.course_registry.current())

    def test_register_a_student_that_was_registered_in_an_old_course_should_add_him_to_current_course(self):
        self._register(students=[self.a_student_request])
        student_registrar = self._start_new_semester_and_initialize_current_registrar()

        student_registrar.process([self.a_student_request])

        self.assertEqual(len(self.student_registry.all()), 2)
        self.assertEqual(self.student_registry.first().course(), self.a_course)
        self.assertEqual(self.student_registry.last().course(), self.course_registry.current())

    def test_register_a_student_adds_registry_in_student_studies_registry(self):
        self._register(students=[self.a_student_request])

        self.assertEqual(self.student_registry.first().studies().university(), 'UBA')
        self.assertEqual(self.student_registry.first().studies().career(), 'Ciencias de la Computación')
        self.assertEqual(self.student_registry.first().studies().study_level(), 'Pregrado (tecnicatura)')
        self.assertEqual(self.student_registry.first().studies().programming_skills(), 4)
        self.assertEqual(self.student_registry.first().studies().python_skills(), 2)

    def test_register_a_student_adds_registry_in_working_registry(self):
        self._register(students=[self.a_student_request])

        self.assertEqual(self.student_registry.first().job().business_name(), 'Eryx')
        self.assertEqual(self.student_registry.first().job().position(), 'Desarrolladora')

    def _register(self, students):
        self.student_registrar.process(students)

    def _start_new_semester_and_initialize_current_registrar(self):
        # FIXME: esto esta raro
        self.course_registry.append(Course(quarter=1, year=2022))
        return StudentRegistrar(self.student_registry, studies_registry=self.studies_registry,
                                job_registry=self.job_registry, course=self.course_registry.current())
